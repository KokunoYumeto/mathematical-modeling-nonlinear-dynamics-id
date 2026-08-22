#!/usr/bin/env python3
"""Build deterministic Zenodo preservation artifacts for an admitted boundary."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
SNAPSHOT_ROOTS = (
    "authority/coordinator-snapshot-20260821",
    "authority/units",
    "backend",
    "build/reader",
    "qa",
    "scripts",
    "source",
)
SNAPSHOT_FILES = (
    ".gitattributes",
    "LICENSE.md",
    "README.md",
    "authority/archives/lega-v1.01.epub",
    "authority/archives/lega-v1.01.pdf",
    "00_control/PUBLIC_BUILD_QA.md",
    "00_control/RIGHTS_AND_PROVENANCE.md",
    "00_control/SOURCE_CORRECTIONS.csv",
    "00_control/TERMINOLOGY.csv",
)
TEXT_SUFFIXES = {
    ".css", ".csv", ".html", ".ipynb", ".js", ".json", ".jsonl", ".md",
    ".py", ".svg", ".tsv", ".txt", ".xml",
}
PRIVATE_PATTERNS = {
    "windows_user_path": re.compile(r"C:\\Users\\", re.IGNORECASE),
    "mac_user_path": re.compile(r"/Users/", re.IGNORECASE),
    "private_folder": re.compile(r"[\\/](?:AppData|Obsidian(?: notes)?|Downloads)[\\/]", re.IGNORECASE),
    "codex_link": re.compile(r"codex://", re.IGNORECASE),
    "bearer_header": re.compile(r"Authorization\s*:\s*Bearer", re.IGNORECASE),
    "token_label": re.compile(r"(?:access[_ -]?token|api[_ -]?key|github_pat_|ghp_[A-Za-z0-9])", re.IGNORECASE),
    "credential_filename": re.compile(r"(?:zenodo|github).{0,20}token", re.IGNORECASE),
}
PUBLIC_EXCLUDED_PATHS = {
    "scripts/build_zenodo_progress_release.py",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def included(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    rel = path.relative_to(ROOT).as_posix()
    return (
        rel not in PUBLIC_EXCLUDED_PATHS
        and
        "__pycache__" not in parts
        and ".pytest_cache" not in parts
        and path.suffix.lower() not in {".pyc", ".pyo"}
        and not path.is_symlink()
    )


def snapshot_files() -> list[Path]:
    files: list[Path] = []
    for name in SNAPSHOT_FILES:
        path = ROOT / name
        if not path.is_file():
            raise FileNotFoundError(path)
        files.append(path)
    for name in SNAPSHOT_ROOTS:
        root = ROOT / name
        if not root.is_dir():
            raise FileNotFoundError(root)
        files.extend(path for path in root.rglob("*") if path.is_file() and included(path))
    return sorted(set(files), key=lambda path: path.relative_to(ROOT).as_posix())


def safe_zip_members(archive: zipfile.ZipFile, label: str) -> list[zipfile.ZipInfo]:
    infos = archive.infolist()
    names = [info.filename for info in infos]
    if len(names) != len(set(names)):
        raise RuntimeError(f"duplicate member in {label}")
    for info in infos:
        pure = PurePosixPath(info.filename)
        if pure.is_absolute() or ".." in pure.parts or "\\" in info.filename:
            raise RuntimeError(f"unsafe member path in {label}: {info.filename}")
        mode = (info.external_attr >> 16) & 0xFFFF
        if mode and (mode & 0o170000) == 0o120000:
            raise RuntimeError(f"symlink member in {label}: {info.filename}")
    return infos


def scan_text(payload: bytes, label: str) -> int:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"declared text is not UTF-8: {label}") from exc
    for name, pattern in PRIVATE_PATTERNS.items():
        if pattern.search(text):
            raise RuntimeError(f"private marker {name} in {label}")
    return len(payload)


def privacy_scan(files: list[Path]) -> dict[str, int]:
    text_files = 0
    text_bytes = 0
    nested_archives = 0
    nested_members = 0
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in TEXT_SUFFIXES:
            text_bytes += scan_text(path.read_bytes(), rel)
            text_files += 1
        if path.suffix.lower() == ".zip":
            nested_archives += 1
            with zipfile.ZipFile(path) as archive:
                if archive.testzip() is not None:
                    raise RuntimeError(f"CRC failure in nested archive {rel}")
                for info in safe_zip_members(archive, rel):
                    nested_members += 1
                    if PurePosixPath(info.filename).suffix.lower() in TEXT_SUFFIXES:
                        text_bytes += scan_text(archive.read(info), f"{rel}!/{info.filename}")
                        text_files += 1
    return {
        "text_files": text_files,
        "text_bytes": text_bytes,
        "nested_archives": nested_archives,
        "nested_members": nested_members,
    }


def reader_files() -> list[Path]:
    root = ROOT / "build" / "reader"
    if not root.is_dir():
        raise FileNotFoundError(root)
    return sorted(
        (path for path in root.rglob("*") if path.is_file() and included(path)),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )


def manifest_tsv(files: list[Path]) -> bytes:
    rows = ["path\tbytes\tsha256"]
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        rows.append(f"{rel}\t{path.stat().st_size}\t{sha256_file(path)}")
    return ("\n".join(rows) + "\n").encode("utf-8")


def zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (0o100644 & 0xFFFF) << 16
    return info


def build_zip(path: Path, files: list[Path], embedded_manifest: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.writestr(zip_info("SNAPSHOT_MANIFEST.tsv"), embedded_manifest)
        for source in files:
            archive.writestr(
                zip_info(source.relative_to(ROOT).as_posix()), source.read_bytes()
            )


def verify_zip(path: Path, files: list[Path], embedded_manifest: bytes) -> dict[str, object]:
    expected = ["SNAPSHOT_MANIFEST.tsv"] + [
        item.relative_to(ROOT).as_posix() for item in files
    ]
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise RuntimeError(f"CRC failure in {path}")
        safe_zip_members(archive, path.name)
        if archive.namelist() != expected:
            raise RuntimeError(f"member order or closure differs in {path}")
        if archive.read("SNAPSHOT_MANIFEST.tsv") != embedded_manifest:
            raise RuntimeError(f"embedded manifest differs in {path}")
        for source in files:
            rel = source.relative_to(ROOT).as_posix()
            if archive.read(rel) != source.read_bytes():
                raise RuntimeError(f"archived bytes differ: {rel}")
    return {
        "path": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "members": len(expected),
        "payload_files": len(files),
        "payload_bytes": sum(item.stat().st_size for item in files),
        "embedded_manifest_sha256": sha256_bytes(embedded_manifest),
    }


def build(boundary: str, output: Path) -> dict[str, object]:
    snapshot = snapshot_files()
    readers = reader_files()
    snapshot_privacy = privacy_scan(snapshot)
    reader_privacy = privacy_scan(readers)
    snapshot_manifest = manifest_tsv(snapshot)
    reader_manifest = manifest_tsv(readers)
    stem = f"O005_LEGA_v1.01_id_progress_{boundary}"
    repository_zip = output / f"{stem}_repository.zip"
    readers_zip = output / f"{stem}_readers.zip"
    build_zip(repository_zip, snapshot, snapshot_manifest)
    build_zip(readers_zip, readers, reader_manifest)
    result = {
        "schema": "o005-zenodo-progress-release-v1",
        "boundary": boundary,
        "status": "in_progress",
        "source_edition": "Joceline Lega, Introduction to Mathematical Modeling, v1.01 (March 2026)",
        "language": "id-ID",
        "license": "CC BY-NC-SA 4.0",
        "privacy_scan": {
            "repository": snapshot_privacy,
            "readers": reader_privacy,
        },
        "artifacts": [
            verify_zip(repository_zip, snapshot, snapshot_manifest),
            verify_zip(readers_zip, readers, reader_manifest),
        ],
    }
    manifest_path = output / f"{stem}_RELEASE_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    result["manifest"] = {
        "path": manifest_path.name,
        "bytes": manifest_path.stat().st_size,
        "sha256": sha256_file(manifest_path),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--boundary", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if ROOT.resolve() not in output.parents:
        raise RuntimeError("release output must remain inside the lane")
    first = build(args.boundary, output)
    hashes = {row["path"]: row["sha256"] for row in first["artifacts"]}
    second = build(args.boundary, output)
    if hashes != {row["path"]: row["sha256"] for row in second["artifacts"]}:
        raise RuntimeError("release rebuild is not byte-identical")
    print(json.dumps(second, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
