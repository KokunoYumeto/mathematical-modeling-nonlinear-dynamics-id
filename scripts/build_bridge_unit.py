#!/usr/bin/env python3
"""Build original O005 bridge units without mislabeling them as translations."""

from __future__ import annotations

import argparse
import hashlib
import html
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

import jsonschema
from bs4 import BeautifulSoup

import build_unit_reader as base


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "source" / "reader" / "reader.css"
MODEL_IDENTIFICATION = "OpenAI Codex gpt-5.6-sol, Ultra."
KERNEL_NAME = "o005-c120-py3139"
SCHEMA_DIR = ROOT / "backend" / "schema"
UNIT_SCHEMA = SCHEMA_DIR / "o005-bridge-unit.schema.json"
SEGMENT_SCHEMA = SCHEMA_DIR / "o005-bridge-segment.schema.json"
MASTERY_SCHEMA = SCHEMA_DIR / "o005-bridge-mastery.schema.json"
AUTHORITY_SCHEMA = SCHEMA_DIR / "o005-original-authority.schema.json"
AUTHORITY_MANIFEST_SCHEMA = SCHEMA_DIR / "o005-original-authority-manifest.schema.json"
SEGMENT_LEDGER_SCHEMA = SCHEMA_DIR / "o005-segment-id-ledger.schema.json"

UNIT_SPECS = {
    "O005-BRIDGE-C1": {
        "title": "Alur Kerja Python/Jupyter yang Reprodusibel",
        "display_label": "Modul Jembatan C1",
        "problem_count": 7,
        "generator": ROOT / "scripts" / "generate_bridge_c1.py",
        "content": ROOT / "source" / "id-ID" / "O005-BRIDGE-C1" / "content.html",
        "notebook": ROOT
        / "source"
        / "id-ID"
        / "O005-BRIDGE-C1"
        / "notebooks"
        / "bridge-c1-reproducible-workflow.ipynb",
        "segment_id_ledger": ROOT
        / "backend"
        / "segment-ids"
        / "O005-BRIDGE-C1.segment-ids.v1.json",
        "placement": "after_source_record_closure_before_bridge_c2",
        "concepts": [
            "reproducible-computing",
            "data-provenance",
            "model-contract",
            "deterministic-randomness",
            "parameter-estimation",
            "residual-diagnostics",
            "holdout-data",
            "artifact-hashing",
        ],
    }
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def file_identity(path: Path, logical_path: str | None = None) -> dict:
    return {
        "path": logical_path or path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }


def derived_path(derived_root: Path, relative_path: str) -> Path:
    return derived_root / Path(relative_path)


def slot_binding_sha256(html_path: str, canonical_text: str) -> str:
    payload = f"{html_path}\0{canonical_text}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def segment_serial(segment_id: str) -> int:
    return int(segment_id.rsplit("S", 1)[1])


def load_segment_ledger(spec: dict, unit_id: str) -> dict:
    ledger_path = spec["segment_id_ledger"]
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    schema = json.loads(SEGMENT_LEDGER_SCHEMA.read_text(encoding="utf-8"))
    ledger_root = (ROOT / "backend" / "segment-ids").resolve()
    expected_content_path = spec["content"].relative_to(ROOT).as_posix()

    def validate_payload(path: Path, payload: dict) -> None:
        jsonschema.validate(payload, schema)
        if payload["unit_id"] != unit_id:
            raise RuntimeError("Segment-ID ledger unit identity differs")
        if payload["content_path"] != expected_content_path:
            raise RuntimeError("Segment-ID ledger content path differs")
        expected_name = f"{unit_id}.segment-ids.v{payload['ledger_version']}.json"
        if path.name != expected_name:
            raise RuntimeError("Segment-ID ledger filename/version binding differs")
        entries = payload["entries"]
        keys = [entry["segment_key"] for entry in entries]
        ids = [entry["segment_id"] for entry in entries]
        if len(set(keys)) != len(keys) or len(set(ids)) != len(ids):
            raise RuntimeError("Segment-ID ledger repeats a durable key or ID")
        if payload["next_serial"] <= max(segment_serial(segment_id) for segment_id in ids):
            raise RuntimeError("Segment-ID ledger next_serial would reuse an allocated ID")

    validate_payload(ledger_path, ledger)
    if ledger["content_sha256"] != digest(spec["content"]):
        raise RuntimeError("Segment-ID ledger is not bound to the current canonical content")

    current_path = ledger_path.resolve()
    current = ledger
    visited = {current_path}
    while current["previous"] is not None:
        predecessor = current["previous"]
        previous_path = (ROOT / predecessor["path"]).resolve()
        if (
            not previous_path.is_relative_to(ledger_root)
            or not previous_path.is_file()
            or previous_path in visited
        ):
            raise RuntimeError("Segment-ID ledger predecessor path is invalid or cyclic")
        if file_identity(previous_path) != predecessor:
            raise RuntimeError("Segment-ID ledger predecessor identity differs")
        previous = json.loads(previous_path.read_text(encoding="utf-8"))
        validate_payload(previous_path, previous)
        if current["ledger_version"] != previous["ledger_version"] + 1:
            raise RuntimeError("Segment-ID ledger version is not consecutive")

        previous_by_key = {entry["segment_key"]: entry for entry in previous["entries"]}
        current_by_key = {entry["segment_key"]: entry for entry in current["entries"]}
        for key, old_entry in previous_by_key.items():
            new_entry = current_by_key.get(key)
            if new_entry is None or new_entry["segment_id"] != old_entry["segment_id"]:
                raise RuntimeError(f"Segment-ID ledger changed or removed durable mapping: {key}")
            if old_entry["state"] == "retired" and new_entry["state"] != "retired":
                raise RuntimeError(f"Segment-ID ledger reactivated a retired key: {key}")
        for key, entry in current_by_key.items():
            if key not in previous_by_key and segment_serial(entry["segment_id"]) < previous["next_serial"]:
                raise RuntimeError(f"Segment-ID ledger reused a previously allocated serial: {key}")
        if current["next_serial"] < previous["next_serial"]:
            raise RuntimeError("Segment-ID ledger next_serial moved backwards")

        visited.add(previous_path)
        current_path = previous_path
        current = previous
    if current["ledger_version"] != 1:
        raise RuntimeError("Only the first Segment-ID ledger may omit a predecessor")
    return ledger


def pandoc_identity(pandoc_version: str) -> dict:
    executable = shutil.which("pandoc")
    if executable is None:
        raise RuntimeError("Pandoc executable is unavailable")
    path = Path(executable).resolve()
    return {
        "version": pandoc_version,
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }


def toolchain_file_paths(spec: dict) -> list[Path]:
    return [
        ROOT / "scripts" / "build_bridge_unit.py",
        ROOT / "scripts" / "build_unit_reader.py",
        ROOT / "scripts" / "qa_bridge_unit.py",
        ROOT / "scripts" / "execute_bridge_notebook_jupyter.py",
        CSS,
        spec["notebook"].parent / "requirements.lock",
        UNIT_SCHEMA,
        SEGMENT_SCHEMA,
        MASTERY_SCHEMA,
        AUTHORITY_SCHEMA,
        AUTHORITY_MANIFEST_SCHEMA,
        SEGMENT_LEDGER_SCHEMA,
        spec["segment_id_ledger"],
    ]


def toolchain_identity(spec: dict, pandoc_version: str) -> dict:
    return {
        "files": [file_identity(path) for path in toolchain_file_paths(spec)],
        "pandoc": pandoc_identity(pandoc_version),
        "python": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
            "executable_bytes": Path(sys.executable).stat().st_size,
            "executable_sha256": digest(Path(sys.executable)),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
        },
        "dependencies": {
            "beautifulsoup4": importlib.metadata.version("beautifulsoup4"),
            "jsonschema": importlib.metadata.version("jsonschema"),
        },
    }


def configure(unit_id: str) -> dict:
    try:
        return UNIT_SPECS[unit_id]
    except KeyError as exc:
        raise SystemExit(f"Unknown bridge unit: {unit_id}") from exc


def render_bridge_markup(fragment: str) -> str:
    """Render TeX without invoking source-specific Pressbooks censuses."""
    rendered = base.COMPANION_MATH_RE.sub(
        lambda match: base.render_math((match.group(1) or match.group(2)).strip()),
        fragment,
    )
    rendered = base.LATEX_RE.sub(lambda match: base.render_math(match.group(1).strip()), rendered)
    return rendered.replace("&nbsp;", " ")


def validate_inputs(unit_id: str, spec: dict) -> tuple[dict, dict]:
    generator = spec["generator"]
    subprocess.run(
        [sys.executable, str(generator), "--check"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    notebook = spec["notebook"]
    lock = notebook.parent / "requirements.lock"
    mastery_path = ROOT / "backend" / "mastery" / f"{unit_id}.mastery.json"
    required = [
        CSS,
        spec["content"],
        notebook,
        lock,
        mastery_path,
        generator,
        *toolchain_file_paths(spec),
    ]
    required = list(dict.fromkeys(required))
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing bridge inputs: " + ", ".join(missing))

    mastery = json.loads(mastery_path.read_text(encoding="utf-8"))
    jsonschema.validate(
        mastery,
        json.loads(MASTERY_SCHEMA.read_text(encoding="utf-8")),
    )
    expected_ids = [f"{unit_id}-P{i:02d}" for i in range(1, spec["problem_count"] + 1)]
    actual_ids = [problem["problem_id"] for problem in mastery["problems"]]
    if actual_ids != expected_ids:
        raise RuntimeError("Bridge mastery problem IDs are not exact and contiguous")
    if mastery["unit_id"] != unit_id or mastery["language"] != "id-ID":
        raise RuntimeError("Bridge mastery identity or language differs")
    if mastery["source"].get("not_part_of_source_book") is not True:
        raise RuntimeError("Bridge mastery must preserve the original-addition boundary")

    notebook_payload = json.loads(notebook.read_text(encoding="utf-8"))
    cells = notebook_payload.get("cells", [])
    code_cells = [cell for cell in cells if cell.get("cell_type") == "code"]
    if len(cells) != 14 or len(code_cells) != 7:
        raise RuntimeError("Bridge notebook cell census differs")
    if len({cell.get("id") for cell in cells}) != len(cells):
        raise RuntimeError("Bridge notebook cell IDs are not unique")
    if any(cell.get("outputs") or cell.get("execution_count") is not None for cell in code_cells):
        raise RuntimeError("Bridge notebook must remain output-clean")
    meta = notebook_payload.get("metadata", {}).get("o005", {})
    if (
        meta.get("unit_id") != unit_id
        or meta.get("notebook_id") != f"{unit_id}-NB01"
        or meta.get("provenance") != "new_original_addition"
        or meta.get("offline_capable") is not True
        or meta.get("locale") != "id-ID"
    ):
        raise RuntimeError("Bridge notebook provenance differs")
    if meta.get("model_identification") != MODEL_IDENTIFICATION:
        raise RuntimeError("Bridge notebook model identification differs")
    kernelspec = notebook_payload.get("metadata", {}).get("kernelspec", {})
    if kernelspec.get("name") != KERNEL_NAME:
        raise RuntimeError(f"Bridge notebook must declare kernelspec {KERNEL_NAME}")

    load_segment_ledger(spec, unit_id)
    return mastery, notebook_payload


def write_segments(unit_id: str, spec: dict, content: str, derived_root: Path) -> tuple[int, str, Path]:
    slots = base.text_slots(content)
    if not slots:
        raise RuntimeError("Bridge content has no machine-indexable text slots")
    ledger = load_segment_ledger(spec, unit_id)
    active_entries = [entry for entry in ledger["entries"] if entry["state"] == "active"]
    bindings = {entry["slot_binding_sha256"]: entry["segment_id"] for entry in active_entries}
    if len(bindings) != len(active_entries):
        raise RuntimeError("Segment-ID ledger repeats a slot binding")
    current_bindings = [slot_binding_sha256(html_path, text) for html_path, text in slots]
    if len(set(current_bindings)) != len(current_bindings):
        raise RuntimeError("Canonical content contains duplicate segment slot bindings")
    missing = [binding for binding in current_bindings if binding not in bindings]
    stale = sorted(set(bindings) - set(current_bindings))
    if missing or stale or len(current_bindings) != len(bindings):
        raise RuntimeError(
            "Segment-ID ledger differs from canonical slots; create a versioned ledger update "
            f"(missing={len(missing)}, stale={len(stale)})"
        )
    segment_ids = [bindings[binding] for binding in current_bindings]
    if len(set(segment_ids)) != len(segment_ids):
        raise RuntimeError("Segment-ID ledger repeats a durable segment ID")
    segment_path = derived_path(derived_root, f"backend/segments/{unit_id}.segments.jsonl")
    lines: list[str] = []
    for ordinal, ((html_path, canonical_text), segment_id) in enumerate(zip(slots, segment_ids), 1):
        record = {
            "schema": "o005-bridge-segment-v1",
            "segment_id": segment_id,
            "unit_id": unit_id,
            "ordinal": ordinal,
            "html_path": html_path,
            "canonical_language": "id-ID",
            "canonical_text": canonical_text,
            "canonical_sha256": hashlib.sha256(canonical_text.encode("utf-8")).hexdigest(),
            "status": "original",
        }
        lines.append(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    payload = ("\n".join(lines) + "\n").encode("utf-8")
    segment_path.parent.mkdir(parents=True, exist_ok=True)
    segment_path.write_bytes(payload)
    return len(lines), hashlib.sha256(payload).hexdigest(), segment_path


def write_authority(
    unit_id: str,
    spec: dict,
    mastery_path: Path,
    lock: Path,
    derived_root: Path,
    toolchain: dict,
) -> tuple[Path, Path]:
    authority_rel = f"authority/units/{unit_id}"
    authority_dir = derived_path(derived_root, authority_rel)
    source_record = authority_dir / "source-record.canonical.json"
    manifest = authority_dir / "AUTHORITY_MANIFEST.json"
    inputs = [spec["content"], spec["generator"], spec["notebook"], lock, mastery_path]
    record = {
        "schema": "o005-original-authority-v1",
        "unit_id": unit_id,
        "canonical_language": "id-ID",
        "content_mode": "new_original_addition",
        "title": spec["title"],
        "created_date": "2026-08-22",
        "license": "CC BY-NC-SA 4.0",
        "model_identification": MODEL_IDENTIFICATION,
        "relationship_to_spine": {
            "spine": "Joceline Lega, Introduction to Mathematical Modeling, v1.01",
            "relationship": "independent_supplement",
            "part_of_source_book": False,
            "endorsement_claimed": False,
        },
        "files": [file_identity(path) for path in inputs],
        "toolchain": toolchain,
    }
    jsonschema.validate(record, json.loads(AUTHORITY_SCHEMA.read_text(encoding="utf-8")))
    write_json(source_record, record)
    manifest_payload = {
        "schema": "o005-original-authority-manifest-v1",
        "unit_id": unit_id,
        "record": file_identity(source_record, f"{authority_rel}/source-record.canonical.json"),
        "canonical_content": file_identity(spec["content"]),
        "notebook": file_identity(spec["notebook"]),
        "mastery": file_identity(mastery_path),
        "lock": file_identity(lock),
        "generator": file_identity(spec["generator"]),
        "segment_id_ledger": file_identity(spec["segment_id_ledger"]),
        "toolchain": toolchain,
    }
    jsonschema.validate(
        manifest_payload,
        json.loads(AUTHORITY_MANIFEST_SCHEMA.read_text(encoding="utf-8")),
    )
    write_json(manifest, manifest_payload)
    return source_record, manifest


def write_unit_record(
    unit_id: str,
    spec: dict,
    segment_count: int,
    segment_sha: str,
    segment_path: Path,
    mastery_path: Path,
    lock: Path,
    authority_manifest: Path,
    pandoc: str,
    derived_root: Path,
    toolchain: dict,
) -> Path:
    unit_path = derived_path(derived_root, f"backend/units/{unit_id}.json")
    problems = [f"{unit_id}-P{i:02d}" for i in range(1, spec["problem_count"] + 1)]
    unit = {
        "schema": "o005-bridge-unit-v1",
        "unit_id": unit_id,
        "course_id": "C120",
        "resource_id": "O005",
        "language": "id-ID",
        "content_mode": "new_original_addition",
        "provenance": {
            "model_identification": MODEL_IDENTIFICATION,
            "license": "CC BY-NC-SA 4.0",
            "spine_author": "Joceline Lega",
            "spine_work": "Introduction to Mathematical Modeling",
            "relationship": "independent_supplement",
            "non_endorsement": True,
            "authority_manifest": f"authority/units/{unit_id}/AUTHORITY_MANIFEST.json",
            "authority_manifest_sha256": digest(authority_manifest),
        },
        "target": {
            "title": spec["title"],
            "content_path": spec["content"].relative_to(ROOT).as_posix(),
            "content_sha256": digest(spec["content"]),
            "concepts": spec["concepts"],
            "placement": spec["placement"],
        },
        "segments": {
            "count": segment_count,
            "path": f"backend/segments/{unit_id}.segments.jsonl",
            "sha256": segment_sha,
            "schema": "o005-bridge-segment-v1",
            "id_strategy": "versioned-semantic-ledger-v1",
            "id_ledger_path": spec["segment_id_ledger"].relative_to(ROOT).as_posix(),
            "id_ledger_sha256": digest(spec["segment_id_ledger"]),
        },
        "problems": problems,
        "mastery_path": mastery_path.relative_to(ROOT).as_posix(),
        "mastery_sha256": digest(mastery_path),
        "notebook_path": spec["notebook"].relative_to(ROOT).as_posix(),
        "notebook_sha256": digest(spec["notebook"]),
        "build": {
            "script": "scripts/build_bridge_unit.py",
            "generator": spec["generator"].relative_to(ROOT).as_posix(),
            "pandoc": pandoc,
            "requirements_lock": lock.relative_to(ROOT).as_posix(),
            "requirements_lock_sha256": digest(lock),
            "toolchain": toolchain,
        },
    }
    jsonschema.validate(unit, json.loads(UNIT_SCHEMA.read_text(encoding="utf-8")))
    write_json(unit_path, unit)
    return unit_path


def render_page(
    unit_id: str,
    spec: dict,
    content: str,
    mastery: dict,
    segment_count: int,
    notebook: Path,
    lock: Path,
) -> str:
    body = base.wrap_inline_runs(render_bridge_markup(content))
    base.harden_links(body)
    mastery_html = base.mastery_section(mastery)
    title = html.escape(spec["title"])
    return f'''<!doctype html>
<html lang="id-ID">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Modul orisinal edisi Bahasa Indonesia tentang alur kerja Python/Jupyter yang reprodusibel untuk pemodelan matematika.">
  <title>{title}</title>
  <link rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
  <link rel="stylesheet" href="assets/reader.css">
</head>
<body>
  <a class="skip-link" href="#isi">Lewati ke isi utama</a>
  <header class="reader-header">
    <p class="eyebrow">O005 · C120 · {spec['display_label']}</p>
    <h1>{title}</h1>
    <p class="byline">Tambahan independen untuk edisi Bahasa Indonesia</p>
  </header>
  <nav class="unit-nav" aria-label="Navigasi unit">
    <a href="#isi">Isi modul</a>
    <a href="#dukungan-belajar">Dukungan belajar</a>
    <a href="downloads/{notebook.name}" download>Notebook Python</a>
    <a href="downloads/{lock.name}" download>Unduh requirements.lock</a>
  </nav>
  <main id="isi" tabindex="-1">
    <aside class="edition-notice" aria-labelledby="edition-notice-title">
      <h2 id="edition-notice-title">Tentang modul ini</h2>
      <p>Modul ini merupakan tambahan orisinal yang disusun secara independen untuk melengkapi edisi Bahasa Indonesia <cite>Introduction to Mathematical Modeling</cite>, v1.01, karya Joceline Lega. Modul ini bukan bagian dari buku sumber dan tidak disokong atau disahkan oleh Joceline Lega maupun University of Arizona. <a href="https://opentextbooks.library.arizona.edu/mathematicalmodeling/" rel="external noopener noreferrer">Baca buku sumber resmi</a>.</p>
      <p>Buku sumber, terjemahan, dan tambahan ini didistribusikan dengan <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" rel="license external noopener noreferrer">CC BY-NC-SA 4.0</a>. Produksi dan QA tambahan: {MODEL_IDENTIFICATION}</p>
    </aside>
    <article class="chapter bridge" aria-label="{spec['display_label']}">
{str(body)}
    </article>
    {mastery_html}
  </main>
  <footer>
    <p>Unit <code>{unit_id}</code> · {segment_count} segmen kanonik id-ID · notebook SHA-256 <code>{digest(notebook)}</code>.</p>
  </footer>
</body>
</html>
'''


def resolve_build_destinations(
    unit_id: str,
    output: Path | None,
    staging_root: Path | None,
) -> tuple[Path, Path, bool]:
    canonical_output = ROOT / "build" / "reader" / unit_id
    if staging_root is None:
        requested_output = output or canonical_output
        if requested_output.resolve() != canonical_output.resolve():
            raise RuntimeError(
                "Bridge output deletion is restricted to the canonical unit reader; "
                "use --staging-root for an isolated build"
            )
        return canonical_output, ROOT, False

    if output is not None:
        raise RuntimeError("--output and --staging-root are mutually exclusive")
    stage = staging_root.resolve()
    if not stage.is_dir():
        raise RuntimeError("Staging root must be an existing directory")
    if any(stage.iterdir()):
        raise RuntimeError("Staging root must be empty and dedicated to this build")
    return stage / "reader", stage / "derived", True


def reset_verified_output(unit_id: str, output: Path, staging: bool) -> None:
    canonical_output = ROOT / "build" / "reader" / unit_id
    if staging:
        if output.name != "reader" or output.parent == Path(output.anchor):
            raise RuntimeError("Unverified bridge staging output")
    elif output != canonical_output:
        raise RuntimeError("Refusing to replace an unverified bridge output path")
    protected_chain = [output]
    if not staging:
        protected_chain.extend([ROOT / "build", ROOT / "build" / "reader"])
    for candidate in protected_chain:
        is_junction = getattr(candidate, "is_junction", lambda: False)()
        if candidate.is_symlink() or is_junction:
            raise RuntimeError(f"Refusing to replace a linked bridge output: {candidate}")
    if output.exists():
        shutil.rmtree(output)


def build(
    unit_id: str,
    output: Path | None = None,
    *,
    staging_root: Path | None = None,
) -> dict:
    spec = configure(unit_id)
    output, derived_root, staging = resolve_build_destinations(unit_id, output, staging_root)
    mastery, _ = validate_inputs(unit_id, spec)
    notebook = spec["notebook"]
    lock = notebook.parent / "requirements.lock"
    mastery_path = ROOT / "backend" / "mastery" / f"{unit_id}.mastery.json"
    content = spec["content"].read_text(encoding="utf-8")
    expected_ids = [f"{unit_id}-P{i:02d}" for i in range(1, spec["problem_count"] + 1)]
    problem_ids = [
        tag.get("id")
        for tag in BeautifulSoup(content, "html.parser").select("h3[id]")
        if tag.get("id") in expected_ids
    ]
    if problem_ids != expected_ids:
        raise RuntimeError("Bridge content problem IDs are not exact and contiguous")
    pandoc = base.pandoc_version()
    if pandoc != "pandoc 3.9.0.2":
        raise RuntimeError(f"Expected pandoc 3.9.0.2, found {pandoc}")
    toolchain = toolchain_identity(spec, pandoc)
    segment_count, segment_sha, segment_path = write_segments(unit_id, spec, content, derived_root)
    _, authority_manifest = write_authority(
        unit_id,
        spec,
        mastery_path,
        lock,
        derived_root,
        toolchain,
    )
    unit_path = write_unit_record(
        unit_id,
        spec,
        segment_count,
        segment_sha,
        segment_path,
        mastery_path,
        lock,
        authority_manifest,
        pandoc,
        derived_root,
        toolchain,
    )
    page = render_page(unit_id, spec, content, mastery, segment_count, notebook, lock)

    reset_verified_output(unit_id, output, staging)
    (output / "assets").mkdir(parents=True)
    (output / "data").mkdir()
    (output / "downloads").mkdir()
    (output / "index.html").write_text(page, encoding="utf-8", newline="\n")
    shutil.copyfile(CSS, output / "assets" / "reader.css")
    shutil.copyfile(mastery_path, output / "data" / mastery_path.name)
    shutil.copyfile(segment_path, output / "data" / segment_path.name)
    shutil.copyfile(unit_path, output / "data" / unit_path.name)
    shutil.copyfile(authority_manifest, output / "data" / authority_manifest.name)
    shutil.copyfile(
        spec["segment_id_ledger"],
        output / "data" / spec["segment_id_ledger"].name,
    )
    shutil.copyfile(notebook, output / "downloads" / notebook.name)
    shutil.copyfile(lock, output / "downloads" / lock.name)

    files = sorted(
        (path for path in output.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(output).as_posix(),
    )
    rows = ["path\tbytes\tsha256"]
    total = 0
    for path in files:
        rel = path.relative_to(output).as_posix()
        total += path.stat().st_size
        rows.append(f"{rel}\t{path.stat().st_size}\t{digest(path)}")
    manifest = "\n".join(rows) + "\n"
    package_manifest = output / "PACKAGE_MANIFEST.tsv"
    package_manifest.write_text(manifest, encoding="utf-8", newline="\n")
    return {
        "schema": "o005-bridge-reader-build-v1",
        "unit_id": unit_id,
        "files_excluding_manifest": len(files),
        "bytes_excluding_manifest": total,
        "segment_count": segment_count,
        "segment_manifest_sha256": segment_sha,
        "notebook_sha256": digest(notebook),
        "pandoc": pandoc,
        "staging": staging,
        "package_manifest_sha256": digest(package_manifest),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", choices=sorted(UNIT_SPECS), required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--staging-root", type=Path)
    args = parser.parse_args()
    result = build(args.unit, args.output, staging_root=args.staging_root)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
