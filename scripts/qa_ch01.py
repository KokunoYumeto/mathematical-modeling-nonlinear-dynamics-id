#!/usr/bin/env python3
"""Fail-closed QA for the first translated Lega unit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag


ROOT = Path(__file__).resolve().parents[1]
UNIT_ID = "O005-LEGA-V101-CH01"
SOURCE = ROOT / "authority" / "units" / UNIT_ID / "content.raw.en.html"
TARGET = ROOT / "source" / "id-ID" / UNIT_ID / "content.html"
SVG = ROOT / "source" / "id-ID" / UNIT_ID / "assets" / "modeling-cycle-id.svg"
NOTEBOOK = ROOT / "source" / "id-ID" / UNIT_ID / "notebooks" / "problem-07-open-curve-fitting.ipynb"
LOCK = ROOT / "source" / "id-ID" / UNIT_ID / "notebooks" / "requirements.lock"
MASTERY = ROOT / "backend" / "mastery" / f"{UNIT_ID}.mastery.json"
SEGMENTS = ROOT / "backend" / "segments" / f"{UNIT_ID}.segments.jsonl"
UNIT = ROOT / "backend" / "units" / f"{UNIT_ID}.json"
BUILD = ROOT / "build" / "reader" / UNIT_ID
BUILDER = ROOT / "scripts" / "build_ch01_reader.py"
LATEX_RE = re.compile(r"\$latex\s+(.+?)\$", re.DOTALL)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def tags(fragment: str) -> list[Tag]:
    return list(BeautifulSoup(fragment, "html.parser").find_all(True))


def structural_replay() -> dict:
    source_text = SOURCE.read_text(encoding="utf-8")
    target_text = TARGET.read_text(encoding="utf-8")
    source_tags, target_tags = tags(source_text), tags(target_text)
    require(len(source_tags) == len(target_tags) == 120, "Expected exact 120-element source/target topology")
    require([tag.name for tag in source_tags] == [tag.name for tag in target_tags], "Ordered element topology differs")
    for index, (left, right) in enumerate(zip(source_tags, target_tags), 1):
        left_attrs, right_attrs = dict(left.attrs), dict(right.attrs)
        if left.name == "img":
            left_attrs.pop("src", None); right_attrs.pop("src", None)
            left_attrs.pop("alt", None); right_attrs.pop("alt", None)
        if left.name == "h3" and right.get("id", "").startswith(f"{UNIT_ID}-P"):
            right_attrs.pop("id", None)
        require(left_attrs == right_attrs, f"Unapproved attribute drift at element {index}: {left.name}")
    source_links = [tag["href"] for tag in source_tags if tag.name == "a" and tag.has_attr("href")]
    target_links = [tag["href"] for tag in target_tags if tag.name == "a" and tag.has_attr("href")]
    require(source_links == target_links and len(source_links) == 14, "Source/target href sequence differs")
    source_math = [match.strip() for match in LATEX_RE.findall(source_text)]
    target_math = [match.strip() for match in LATEX_RE.findall(target_text)]
    require(source_math == target_math and len(source_math) == 14, "Source/target TeX sequence differs")
    require("MATLAB" not in target_text and "Matlab" not in target_text, "Proprietary MATLAB prompt remains active")
    require("NumPy/SciPy" in target_text, "Open Python replacement is missing")
    require("\ufffd" not in target_text, "Target contains U+FFFD")
    ids = [tag["id"] for tag in target_tags if tag.has_attr("id")]
    require(len(ids) == len(set(ids)), "Duplicate target IDs")
    expected = [f"{UNIT_ID}-P{i:02d}" for i in range(1, 8)]
    require([tag["id"] for tag in target_tags if tag.name == "h3" and tag.has_attr("id")] == expected, "Problem IDs differ")
    return {"elements": len(source_tags), "links": len(source_links), "math": len(source_math), "problems": len(expected)}


def backend_replay() -> dict:
    mastery = json.loads(MASTERY.read_text(encoding="utf-8"))
    require(mastery["unit_id"] == UNIT_ID and mastery["language"] == "id-ID", "Mastery identity differs")
    problems = mastery["problems"]
    require([p["problem_id"] for p in problems] == [f"{UNIT_ID}-P{i:02d}" for i in range(1, 8)], "Mastery IDs differ")
    require(all(p.get("hint") and p.get("check") and p.get("solution_or_rubric") for p in problems), "Mastery record incomplete")
    require(problems[-1]["notebook"]["path"] == NOTEBOOK.relative_to(ROOT).as_posix(), "Notebook pointer differs")

    records = [json.loads(line) for line in SEGMENTS.read_text(encoding="utf-8").splitlines() if line]
    require(len(records) == 125, "Expected 125 aligned segment records")
    for ordinal, record in enumerate(records, 1):
        require(record["segment_id"] == f"{UNIT_ID}-S{ordinal:04d}" and record["ordinal"] == ordinal, "Segment order/ID differs")
        require(record["unit_id"] == UNIT_ID and record["status"] == "translated", "Segment identity/status differs")
        require(record["source_sha256"] == sha_bytes(record["source_text"].encode("utf-8")), "Segment source hash differs")
        require(record["target_sha256"] == sha_bytes(record["target_text"].encode("utf-8")), "Segment target hash differs")

    unit = json.loads(UNIT.read_text(encoding="utf-8"))
    require(unit["unit_id"] == UNIT_ID and unit["segments"]["count"] == len(records), "Unit backend identity/count differs")
    for branch, key, path in (
        ("source", "content_sha256", SOURCE),
        ("target", "content_sha256", TARGET),
        ("target", "figure_sha256", SVG),
    ):
        require(unit[branch][key] == sha(path), f"Unit {branch}.{key} differs")
    require(unit["segments"]["sha256"] == sha(SEGMENTS), "Unit segment hash differs")
    require(unit["mastery_sha256"] == sha(MASTERY), "Unit mastery hash differs")
    require(unit["notebook_sha256"] == sha(NOTEBOOK), "Unit notebook hash differs")
    return {"segments": len(records), "mastery": len(problems)}


def reader_replay(root: Path) -> dict:
    index = root / "index.html"
    require(index.is_file(), "Reader index is missing")
    soup = BeautifulSoup(index.read_text(encoding="utf-8"), "html.parser")
    require(soup.html and soup.html.get("lang") == "id-ID", "Reader lang is not id-ID")
    require(len(soup.find_all("h1")) == 1, "Reader requires exactly one h1")
    require(len(soup.find_all("math")) == 14, "Reader requires exactly 14 MathML formulas")
    require(len(soup.find_all("details")) == 21, "Reader requires 21 hint/check/solution disclosures")
    ids = [tag["id"] for tag in soup.find_all(id=True)]
    require(len(ids) == len(set(ids)), "Reader contains duplicate IDs")
    local_files: set[Path] = set()
    for tag in soup.find_all(href=True) + soup.find_all(src=True):
        value = tag.get("href") or tag.get("src")
        parsed = urlparse(value)
        if parsed.scheme or value.startswith(("#", "//")):
            if value.startswith("#"):
                require(value[1:] in ids, f"Broken internal fragment: {value}")
            continue
        path = (root / parsed.path).resolve()
        require(root.resolve() in path.parents or path == root.resolve(), f"Reader path escapes root: {value}")
        require(path.is_file(), f"Missing local reader dependency: {value}")
        local_files.add(path)

    manifest_path = root / "PACKAGE_MANIFEST.tsv"
    rows = manifest_path.read_text(encoding="utf-8").splitlines()
    require(rows[0] == "path\tbytes\tsha256", "Package manifest header differs")
    manifest: dict[str, tuple[int, str]] = {}
    for row in rows[1:]:
        rel, size, checksum = row.split("\t")
        require(rel not in manifest, f"Duplicate manifest path: {rel}")
        manifest[rel] = (int(size), checksum)
    actual = sorted(path for path in root.rglob("*") if path.is_file() and path != manifest_path)
    require(set(manifest) == {path.relative_to(root).as_posix() for path in actual}, "Manifest member set differs")
    for path in actual:
        rel = path.relative_to(root).as_posix()
        require(manifest[rel] == (path.stat().st_size, sha(path)), f"Manifest row differs: {rel}")
    public_bytes = b"\n".join(path.read_bytes() for path in actual)
    lowered = public_bytes.lower()
    for forbidden in (
        b"c:" + b"\\" + b"users" + b"\\",
        b"c:" + b"/" + b"users" + b"/",
        b"flo" + b"ris",
        b"github" + b"_pat_",
        b"gh" + b"p_",
        b"s" + b"k-",
    ):
        require(forbidden not in lowered, f"Privacy/secret marker in reader: {forbidden!r}")
    require(b"\xef\xbf\xbd" not in public_bytes, "Reader contains U+FFFD")
    return {"files": len(actual), "bytes": sum(path.stat().st_size for path in actual), "local_dependencies": len(local_files)}


def notebook_replay(execute: bool) -> dict:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    code = [cell for cell in cells if cell.get("cell_type") == "code"]
    require(len(cells) == 12 and len(code) == 7, "Notebook cell census differs")
    require(len({cell.get("id") for cell in cells}) == len(cells), "Notebook cell IDs are not unique")
    require(all(not cell.get("outputs") and cell.get("execution_count") is None for cell in code), "Notebook must remain output-clean")
    require(LOCK.read_text(encoding="utf-8") == "numpy==2.4.4\nscipy==1.17.1\nmatplotlib==3.10.9\n", "Notebook lock differs")
    if execute:
        env = dict(os.environ)
        env["MPLBACKEND"] = "Agg"
        runner = "import json,sys; n=json.load(open(sys.argv[1],encoding='utf-8')); g={}; [exec(compile(''.join(c['source']), c.get('id','cell'), 'exec'),g) for c in n['cells'] if c.get('cell_type')=='code']"
        subprocess.run([sys.executable, "-c", runner, str(NOTEBOOK)], check=True, env=env, timeout=120)
    return {"cells": len(cells), "code_cells": len(code), "executed": execute}


def deterministic_replay() -> dict:
    with tempfile.TemporaryDirectory(prefix="o005-ch01-a-") as a, tempfile.TemporaryDirectory(prefix="o005-ch01-b-") as b:
        for output in (a, b):
            subprocess.run([sys.executable, str(BUILDER), "--output", output], check=True, capture_output=True, text=True, timeout=120)
        left, right = Path(a), Path(b)
        left_files = sorted(path.relative_to(left).as_posix() for path in left.rglob("*") if path.is_file())
        right_files = sorted(path.relative_to(right).as_posix() for path in right.rglob("*") if path.is_file())
        require(left_files == right_files, "Repeated build member sets differ")
        for rel in left_files:
            require((left / rel).read_bytes() == (right / rel).read_bytes(), f"Repeated build bytes differ: {rel}")
        return {"files": len(left_files), "tree_sha256": sha_bytes("\n".join(f"{rel}\t{sha(left / rel)}" for rel in left_files).encode("utf-8"))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute-notebook", action="store_true")
    parser.add_argument("--deterministic-build", action="store_true")
    args = parser.parse_args()
    result = {
        "schema": "o005-ch01-qa-v1",
        "unit_id": UNIT_ID,
        "structure": structural_replay(),
        "backend": backend_replay(),
        "reader": reader_replay(BUILD),
        "notebook": notebook_replay(args.execute_notebook),
        "external_link_reachability_tested": False,
        "audio_or_live_widgets_exercised": False,
    }
    if args.deterministic_build:
        result["deterministic_build"] = deterministic_replay()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
