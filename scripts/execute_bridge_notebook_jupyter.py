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
import base64
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import site
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


MODEL_IDENTIFICATION = "OpenAI Codex gpt-5.6-sol, Ultra."
KERNEL_NAME = "o005-c120-py3139"
PINNED_IMPLEMENTATION = "CPython"
PINNED_PYTHON = "3.13.9"
PINNED_JUPYTER = {
    "ipykernel": "6.29.5",
    "jupyter-client": "8.6.3",
    "nbclient": "0.10.2",
    "nbformat": "5.10.4",
}
DECLARED_OVERRIDES = {
    "O005-BRIDGE-C1": {
        "symbol": "SEED",
        "canonical_symbol": "CANONICAL_SEED",
        "value": 20260823,
    },
    "O005-BRIDGE-C2": {
        "symbol": "PRIMARY_BETA",
        "canonical_symbol": "CANONICAL_BETA",
        "value": 2.0,
    },
    "O005-BRIDGE-C3": None,
    "O005-BRIDGE-C4": {
        "symbol": "BATAS_K_ATAS",
        "canonical_symbol": "CANONICAL_K_UPPER_BOUND",
        "value": 2000.0,
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def jupyter_host_site() -> Path:
    candidates = [Path(value).resolve() for value in site.getsitepackages()]
    for candidate in candidates:
        if (candidate / "ipykernel").is_dir():
            return candidate
    raise RuntimeError("The Jupyter host has no importable ipykernel site-packages")


def extract_summary(stream_text: str, expected_unit_id: str) -> dict:
    decoder = json.JSONDecoder()
    for match in re.finditer(r"(?m)^\{", stream_text):
        try:
            candidate, _ = decoder.raw_decode(stream_text[match.start():])
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict) and candidate.get("unit_id") == expected_unit_id:
            return candidate
    raise RuntimeError("Executed notebook did not emit its declared unit JSON summary")


def parse_override(unit_id: str, symbol: str | None, raw_value: str | None) -> dict | None:
    if symbol is None and raw_value is None:
        return None
    require(symbol is not None and raw_value is not None, "Override symbol and value must be supplied together")
    declaration = DECLARED_OVERRIDES[unit_id]
    require(declaration is not None, f"No notebook override is declared for {unit_id}")
    require(symbol == declaration["symbol"], f"Override {symbol!r} is not declared for {unit_id}")
    try:
        value = json.loads(raw_value)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Override value must be one JSON number") from exc
    require(isinstance(value, (int, float)) and not isinstance(value, bool), "Override value must be numeric")
    require(value == value and abs(value) != float("inf"), "Override value must be finite")
    require(
        type(value) is type(declaration["value"]) and value == declaration["value"],
        f"Override value {value!r} is not the declared experiment for {unit_id}",
    )
    return {
        "symbol": symbol,
        "canonical_symbol": declaration["canonical_symbol"],
        "value": value,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--notebook", type=Path, required=True)
    parser.add_argument("--kernel-python", type=Path, required=True)
    parser.add_argument("--expected-unit-id", choices=sorted(DECLARED_OVERRIDES), required=True)
    parser.add_argument("--expected-marker", required=True)
    parser.add_argument("--expected-image-count", type=int, required=True)
    parser.add_argument("--override-symbol")
    parser.add_argument("--override-value")
    parser.add_argument("--kernel-optimize", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    notebook_path = args.notebook.resolve()
    kernel_python = args.kernel_python.resolve()
    require(notebook_path.is_file(), f"Notebook is missing: {notebook_path}")
    require(kernel_python.is_file(), f"Kernel interpreter is missing: {kernel_python}")
    host_versions = {
        package: importlib.metadata.version(package)
        for package in PINNED_JUPYTER
    }
    require(
        host_versions == PINNED_JUPYTER,
        f"Jupyter host package closure differs: {host_versions!r} != {PINNED_JUPYTER!r}",
    )
    runtime = subprocess.run(
        [
            str(kernel_python),
            "-c",
            "import platform; print(platform.python_implementation()); print(platform.python_version())",
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    ).stdout.splitlines()
    require(
        runtime == [PINNED_IMPLEMENTATION, PINNED_PYTHON],
        "Bridge QA must run the notebook under pinned CPython 3.13.9 and its "
        f"recorded executable identity; selected kernel reported {runtime!r}",
    )

    with notebook_path.open("r", encoding="utf-8") as stream:
        notebook = nbformat.read(stream, as_version=4)
    nbformat.validate(notebook)
    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    require(
        all(cell.execution_count is None and not cell.outputs for cell in code_cells),
        "Canonical notebook is not output-clean",
    )

    override = parse_override(args.expected_unit_id, args.override_symbol, args.override_value)
    if override is not None:
        canonical_source = f"{override['symbol']} = {override['canonical_symbol']}"
        replacement = f"{override['symbol']} = {json.dumps(override['value'])}"
        replacements = 0
        for cell in code_cells:
            source = cell.source
            changed = source.replace(canonical_source, replacement)
            if changed != source:
                replacements += 1
                cell.source = changed
        require(replacements == 1, "Declared override did not replace exactly one assignment")

    kernel_name = notebook.metadata.kernelspec.name
    require(kernel_name == KERNEL_NAME, "Notebook kernelspec identity differs")
    host_site = jupyter_host_site()
    bootstrap = (
        "import site,runpy; "
        f"site.addsitedir({str(host_site)!r}); "
        "runpy.run_module('ipykernel_launcher',run_name='__main__')"
    )

    temp_prefix = args.expected_unit_id.lower().replace("_", "-") + "-jupyter-"
    with tempfile.TemporaryDirectory(prefix=temp_prefix) as temp_name:
        temp_root = Path(temp_name)
        data_dir = temp_root / "data"
        config_dir = temp_root / "config"
        runtime_dir = temp_root / "runtime"
        kernel_dir = data_dir / "kernels" / kernel_name
        for directory in (kernel_dir, config_dir, runtime_dir):
            directory.mkdir(parents=True, exist_ok=True)
        kernel_argv = [str(kernel_python)]
        if args.kernel_optimize:
            kernel_argv.append("-O")
        kernel_argv.extend(["-c", bootstrap, "-f", "{connection_file}"])
        kernel_spec = {
            "argv": kernel_argv,
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
    image_records: list[dict] = []
    for cell in executed_code:
        for output_index, output in enumerate(cell.outputs):
            if (
                output.output_type not in {"display_data", "execute_result"}
                or "image/png" not in output.get("data", {})
            ):
                continue
            png = base64.b64decode(output["data"]["image/png"], validate=True)
            require(
                len(png) >= 24 and png[:16] == b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR",
                f"Notebook emitted an invalid PNG in cell {cell.id}",
            )
            width, height = struct.unpack(">II", png[16:24])
            require(width > 0 and height > 0, f"Notebook emitted an empty PNG in cell {cell.id}")
            image_records.append({
                "cell_id": cell.id,
                "output_index": output_index,
                "bytes": len(png),
                "sha256": hashlib.sha256(png).hexdigest(),
                "width": width,
                "height": height,
            })
    image_outputs = len(image_records)
    summary = extract_summary(stream_text, args.expected_unit_id)
    require(summary.get("unit_id") == args.expected_unit_id, "Notebook summary unit differs")
    require(
        summary.get("versions", {}).get("python") == PINNED_PYTHON,
        "Bridge QA must run under pinned CPython 3.13.9 and the recorded executable "
        f"identity; notebook reported {summary.get('versions', {}).get('python')!r}",
    )
    require(
        image_outputs == args.expected_image_count,
        f"Fresh Jupyter image count differs: {image_outputs} != {args.expected_image_count}",
    )
    require(
        args.expected_marker in stream_text,
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
                "schema": "o005-fresh-jupyter-execution-v3",
                "notebook": notebook_path.as_posix(),
                "kernel_python": str(kernel_python),
                "kernel_name": kernel_name,
                "host_versions": host_versions,
                "optimized": args.kernel_optimize,
                "override": override,
                "code_cells": len(executed_code),
                "image_png_outputs": image_outputs,
                "images": image_records,
                "summary": summary,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
