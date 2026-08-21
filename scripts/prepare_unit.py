#!/usr/bin/env python3
"""Materialize an admitted unit from the frozen Lega v1.01 authority.

The constants below are deliberately exact.  Adding a unit requires first
computing its canonical record and asset identities from the already frozen
coordinator snapshot, then reviewing those identities before admission.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
SNAPSHOT = LANE / "authority" / "coordinator-snapshot-20260821" / "snapshot"
RECORDS = SNAPSHOT / "records.canonical.json"
EPUB = LANE / "authority" / "archives" / "lega-v1.01.epub"

UNIT_SPECS = {
    "O005-LEGA-V101-CH01": {
        "record_id": 25,
        "modified_gmt": "2026-03-27T02:08:36",
        "record_bytes": 37918,
        "record_sha256": "0286cb444c7f2f4a2db83865f948d3d3dc00147e2280fa665a1abc68ad804826",
        "assets": [
            {
                "path": "assets/modeling-cycle-source.png",
                "epub_member": "EPUB/assets/Modeling_Cycle-1024x508.png",
                "bytes": 75844,
                "sha256": "29c1df3263dd7fe76769803e54c23ddcd198198e86edbfd7e4d6f0c618f708e3",
            }
        ],
    },
    "O005-LEGA-V101-CH02": {
        "record_id": 27,
        "modified_gmt": "2026-03-27T02:10:41",
        "record_bytes": 39193,
        "record_sha256": "428a143edeec7843d3f4a2e2f02e5aa50fcde2cff366ca976988ecfa4191e69b",
        "assets": [
            {
                "path": "assets/the-wave-source.png",
                "epub_member": "EPUB/assets/The_Wave.png",
                "bytes": 80026,
                "sha256": "9abe8e17abd593811c14a1d6ea72b3ff727682ba58d000a87ece4056332769b6",
            }
        ],
    },
    "O005-LEGA-V101-PT02": {
        "record_id": 28,
        "modified_gmt": "2024-06-29T02:57:03",
        "record_bytes": 2296,
        "record_sha256": "03ead95b0ebcfb470c92bb7e48a85ce45d7639ec0aafb00f981eaf90ffd3f1e9",
        "assets": [],
    },
}


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


def checked_bytes(data: bytes, *, size: int, digest: str, label: str) -> bytes:
    if len(data) != size or sha256(data) != digest:
        raise RuntimeError(f"{label} does not match admitted authority")
    return data


def prepare(unit_id: str) -> dict:
    spec = UNIT_SPECS[unit_id]
    records = json.loads(RECORDS.read_text(encoding="utf-8"))
    matches = [record for record in records if record.get("id") == spec["record_id"]]
    if len(matches) != 1:
        raise RuntimeError(
            f"expected one record {spec['record_id']}, found {len(matches)}"
        )
    record = matches[0]
    record_bytes = checked_bytes(
        canonical_json(record),
        size=spec["record_bytes"],
        digest=spec["record_sha256"],
        label=f"canonical {unit_id} record",
    )
    if record.get("modified_gmt") != spec["modified_gmt"]:
        raise RuntimeError(f"unexpected {unit_id} modification instant")
    content = record.get("content") or {}
    raw = content.get("raw")
    rendered = content.get("rendered")
    if not isinstance(raw, str) or not isinstance(rendered, str):
        raise RuntimeError(f"{unit_id} lacks raw/rendered semantic source")
    raw_bytes = raw.encode("utf-8")
    rendered_bytes = rendered.encode("utf-8")

    unit = LANE / "authority" / "units" / unit_id
    write_checked(unit / "source-record.canonical.json", record_bytes)
    write_checked(unit / "content.raw.en.html", raw_bytes)
    write_checked(unit / "content.rendered.en.html", rendered_bytes)

    asset_rows = []
    with zipfile.ZipFile(EPUB) as archive:
        bad = archive.testzip()
        if bad is not None:
            raise RuntimeError(f"EPUB CRC failure at {bad}")
        for asset in spec["assets"]:
            data = checked_bytes(
                archive.read(asset["epub_member"]),
                size=asset["bytes"],
                digest=asset["sha256"],
                label=f"{unit_id} asset {asset['epub_member']}",
            )
            write_checked(unit / asset["path"], data)
            asset_rows.append(
                {
                    "path": asset["path"],
                    "bytes": len(data),
                    "sha256": sha256(data),
                    "epub_member": asset["epub_member"],
                }
            )

    manifest = {
        "schema": "o005-unit-authority-v1",
        "unit_id": unit_id,
        "source_record_id": spec["record_id"],
        "source_modified_gmt": spec["modified_gmt"] + "Z",
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
        "assets": asset_rows,
    }
    payload = (
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    write_checked(unit / "AUTHORITY_MANIFEST.json", payload)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("unit_id", choices=sorted(UNIT_SPECS))
    args = parser.parse_args()
    print(json.dumps(prepare(args.unit_id), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
