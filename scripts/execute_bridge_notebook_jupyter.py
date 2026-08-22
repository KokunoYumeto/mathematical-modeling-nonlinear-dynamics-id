#!/usr/bin/env python3
"""Execute one bridge notebook in a fresh, isolated Jupyter kernel.

Run this harness with a Python installation that provides nbclient, nbformat,
and ipykernel.  The kernel itself is launched with ``--kernel-python`` so the
scientific environment being tested need not also host the Jupyter frontend.
The temporary kernelspec appends only the host's site-packages after the
kernel interpreter's own paths; the notebook's version gate proves which
NumPy/SciPy/Matplotlib stack actually ran.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import site
import sys
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


MODEL_IDENTIFICATION = "OpenAI Codex gpt-5.6-sol, Ultra."
CANONICAL_SEED_SOURCE = "SEED = CANONICAL_SEED"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def jupyter_host_site() -> Path:
    candidates = [Path(value).resolve() for value in site.getsitepackages()]
    for candidate in candidates:
        if (candidate / "ipykernel").is_dir():
            return candidate
    raise RuntimeError("The Jupyter host has no importable ipykernel site-packages")


def extract_summary(stream_text: str) -> dict:
    marker = '{\n  "data_sha256"'
    start = stream_text.find(marker)
    require(start >= 0, "Executed notebook did not emit its JSON summary")
    summary, _ = json.JSONDecoder().raw_decode(stream_text[start:])
    require(isinstance(summary, dict), "Notebook summary is not an object")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--notebook", type=Path, required=True)
    parser.add_argument("--kernel-python", type=Path, required=True)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    notebook_path = args.notebook.resolve()
    kernel_python = args.kernel_python.resolve()
    require(notebook_path.is_file(), f"Notebook is missing: {notebook_path}")
    require(kernel_python.is_file(), f"Kernel interpreter is missing: {kernel_python}")

    with notebook_path.open("r", encoding="utf-8") as stream:
        notebook = nbformat.read(stream, as_version=4)
    nbformat.validate(notebook)
    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    require(
        all(cell.execution_count is None and not cell.outputs for cell in code_cells),
        "Canonical notebook is not output-clean",
    )

    if args.seed is not None:
        replacements = 0
        for cell in code_cells:
            source = cell.source
            changed = source.replace(CANONICAL_SEED_SOURCE, f"SEED = {args.seed}")
            if changed != source:
                replacements += 1
                cell.source = changed
        require(replacements == 1, "Seed override did not replace exactly one assignment")

    kernel_name = notebook.metadata.kernelspec.name
    require(kernel_name == "o005-c120-py3139", "Notebook kernelspec identity differs")
    host_site = jupyter_host_site()
    bootstrap = (
        "import site,runpy; "
        f"site.addsitedir({str(host_site)!r}); "
        "runpy.run_module('ipykernel_launcher',run_name='__main__')"
    )

    with tempfile.TemporaryDirectory(prefix="o005-c1-jupyter-") as temp_name:
        temp_root = Path(temp_name)
        data_dir = temp_root / "data"
        config_dir = temp_root / "config"
        runtime_dir = temp_root / "runtime"
        kernel_dir = data_dir / "kernels" / kernel_name
        for directory in (kernel_dir, config_dir, runtime_dir):
            directory.mkdir(parents=True, exist_ok=True)
        kernel_spec = {
            "argv": [str(kernel_python), "-c", bootstrap, "-f", "{connection_file}"],
            "display_name": "O005 C120 Python 3.13.9",
            "language": "python",
            "metadata": {
                "model_identification": MODEL_IDENTIFICATION,
                "temporary_qa_kernel": True,
            },
        }
        (kernel_dir / "kernel.json").write_text(
            json.dumps(kernel_spec, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        previous = {
            key: os.environ.get(key)
            for key in ("JUPYTER_DATA_DIR", "JUPYTER_CONFIG_DIR", "JUPYTER_RUNTIME_DIR", "PYTHONHASHSEED")
        }
        os.environ.update(
            {
                "JUPYTER_DATA_DIR": str(data_dir),
                "JUPYTER_CONFIG_DIR": str(config_dir),
                "JUPYTER_RUNTIME_DIR": str(runtime_dir),
                "PYTHONHASHSEED": "0",
            }
        )
        try:
            client = NotebookClient(
                notebook,
                timeout=args.timeout,
                kernel_name=kernel_name,
                resources={"metadata": {"path": str(notebook_path.parent)}},
                allow_errors=False,
            )
            executed = client.execute()
        finally:
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    executed_code = [cell for cell in executed.cells if cell.cell_type == "code"]
    stream_text = "".join(
        output.get("text", "")
        for cell in executed_code
        for output in cell.outputs
        if output.output_type == "stream" and output.get("name") == "stdout"
    )
    image_outputs = sum(
        1
        for cell in executed_code
        for output in cell.outputs
        if output.output_type in {"display_data", "execute_result"}
        and "image/png" in output.get("data", {})
    )
    summary = extract_summary(stream_text)
    require(summary.get("unit_id") == "O005-BRIDGE-C1", "Notebook summary unit differs")
    require(summary.get("versions", {}).get("python") == "3.13.9", "Kernel Python version differs")
    require(image_outputs >= 1, "Fresh Jupyter execution emitted no diagnostic PNG")
    require(
        "Verifikasi ulang deterministik dalam kernel yang sama lulus." in stream_text,
        "Same-kernel deterministic replay did not finish",
    )

    if args.output is not None:
        output_path = args.output.resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="\n") as stream:
            nbformat.write(executed, stream)

    print(
        json.dumps(
            {
                "schema": "o005-fresh-jupyter-execution-v1",
                "notebook": notebook_path.as_posix(),
                "kernel_python": str(kernel_python),
                "kernel_name": kernel_name,
                "seed_override": args.seed,
                "code_cells": len(executed_code),
                "image_png_outputs": image_outputs,
                "summary": summary,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
