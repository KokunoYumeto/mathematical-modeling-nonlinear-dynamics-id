#!/usr/bin/env python3
"""Extract the exact admitted Chapter 1 unit from the frozen O005 authority."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
SNAPSHOT = LANE / "authority" / "coordinator-snapshot-20260821" / "snapshot"
RECORDS = SNAPSHOT / "records.canonical.json"
EPUB = LANE / "authority" / "archives" / "lega-v1.01.epub"
UNIT = LANE / "authority" / "units" / "O005-LEGA-V101-CH01"
EXPECTED_RECORD_SHA256 = "0286cb444c7f2f4a2db83865f948d3d3dc00147e2280fa665a1abc68ad804826"
EXPECTED_RECORD_BYTES = 37918
FIGURE_MEMBER = "EPUB/assets/Modeling_Cycle-1024x508.png"
EXPECTED_FIGURE_SHA256 = "29c1df3263dd7fe76769803e54c23ddcd198198e86edbfd7e4d6f0c618f708e3"
EXPECTED_FIGURE_BYTES = 75844


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_checked(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != data:
        raise RuntimeError(f"refusing to overwrite different bytes: {path}")
    path.write_bytes(data)


def main() -> None:
    records = json.loads(RECORDS.read_text(encoding="utf-8"))
    matches = [record for record in records if record.get("id") == 25]
    if len(matches) != 1:
        raise RuntimeError(f"expected one record 25, found {len(matches)}")
    record = matches[0]
    record_bytes = canonical_json(record)
    if len(record_bytes) != EXPECTED_RECORD_BYTES or sha256(record_bytes) != EXPECTED_RECORD_SHA256:
        raise RuntimeError("canonical Chapter 1 record does not match admitted authority")
    if record.get("modified_gmt") != "2026-03-27T02:08:36":
        raise RuntimeError("unexpected Chapter 1 modification instant")
    content = record.get("content") or {}
    raw = content.get("raw")
    rendered = content.get("rendered")
    if not isinstance(raw, str) or not isinstance(rendered, str):
        raise RuntimeError("Chapter 1 lacks raw/rendered semantic source")
    raw_bytes = raw.encode("utf-8")
    rendered_bytes = rendered.encode("utf-8")

    with zipfile.ZipFile(EPUB) as archive:
        bad = archive.testzip()
        if bad is not None:
            raise RuntimeError(f"EPUB CRC failure at {bad}")
        figure = archive.read(FIGURE_MEMBER)
    if len(figure) != EXPECTED_FIGURE_BYTES or sha256(figure) != EXPECTED_FIGURE_SHA256:
        raise RuntimeError("Chapter 1 figure does not match admitted asset")

    write_checked(UNIT / "source-record.canonical.json", record_bytes)
    write_checked(UNIT / "content.raw.en.html", raw_bytes)
    write_checked(UNIT / "content.rendered.en.html", rendered_bytes)
    write_checked(UNIT / "assets" / "modeling-cycle-source.png", figure)

    manifest = {
        "schema": "o005-unit-authority-v1",
        "unit_id": "O005-LEGA-V101-CH01",
        "source_record_id": 25,
        "source_modified_gmt": "2026-03-27T02:08:36Z",
        "record": {
            "path": "source-record.canonical.json",
            "bytes": len(record_bytes),
            "sha256": sha256(record_bytes),
        },
        "content_raw": {
            "path": "content.raw.en.html",
            "bytes": len(raw_bytes),
            "sha256": sha256(raw_bytes),
        },
        "content_rendered": {
            "path": "content.rendered.en.html",
            "bytes": len(rendered_bytes),
            "sha256": sha256(rendered_bytes),
        },
        "figure": {
            "path": "assets/modeling-cycle-source.png",
            "bytes": len(figure),
            "sha256": sha256(figure),
            "epub_member": FIGURE_MEMBER,
        },
    }
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    write_checked(UNIT / "AUTHORITY_MANIFEST.json", manifest_bytes)
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
