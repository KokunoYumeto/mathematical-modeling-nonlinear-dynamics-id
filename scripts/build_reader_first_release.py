#!/usr/bin/env python3
"""Build a new immutable compact reader-first preservation payload.

The payload intentionally excludes raw download/extraction trees, generated
HTML readers, generated project ZIPs, caches, QA renders, and publication
receipts.  It retains the smallest closure that can regenerate and verify the
completed Indonesian units: translated source, exact unit authority witnesses,
stable-ID backend, open notebooks/data/assets, rights/corrections, and builders.

The already-published CH14 byte replica is protected.  Every later run must
name a new direct child of ``release/zenodo`` and a distinct public version;
an existing output directory is never deleted or overwritten.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path, PurePosixPath

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PUBLISHED_OUTPUT = ROOT / "release" / "zenodo" / "reader-first-CH14"
PUBLISHED_VERSION = "v1.01-id-progress-CH14-reader-20260822"
PDF_SOURCE = (
    ROOT
    / "output"
    / "pdf"
    / "01_Pengantar_Pemodelan_Matematika_Edisi_Bahasa_Indonesia_CH14.pdf"
)
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)

UNIT_IDS = tuple(
    f"O005-LEGA-V101-{short}"
    for short in (
        "CH01", "CH02", "PT02", "CH03", "CH04", "PT03", "CH05",
        "CH06", "CH07", "PT04", "CH08", "CH09", "CH10", "PT05",
        "CH11", "CH12", "CH13", "CH14",
    )
)

ROOT_FILES = (
    ".gitattributes",
    ".gitignore",
    "LICENSE.md",
    "README.md",
)

CONTROL_FILES = (
    "00_control/PUBLIC_BUILD_QA.md",
    "00_control/RIGHTS_AND_PROVENANCE.md",
    "00_control/SOURCE_CORRECTIONS.csv",
    "00_control/TERMINOLOGY.csv",
    "00_control/TERMINOLOGY_QA_INDONESIAN_FIELD_SOURCE_20260822.md",
)

TERMINOLOGY_WITNESS_FILES = (
    "authority/terminology/arxiv-2001.05854v1/SOURCE_MANIFEST.json",
    "authority/terminology/arxiv-2001.05854v1/LICENSE-NOTICE.md",
)

SCRIPT_FILES = (
    "scripts/assemble_unit_fragments.py",
    "scripts/build_ch14_project_packets.py",
    "scripts/build_progress_pdf.py",
    "scripts/build_reader_first_release.py",
    "scripts/build_unit_reader.py",
    "scripts/freeze_pressbooks.py",
    "scripts/prepare_unit.py",
    "scripts/qa_unit.py",
)

BACKEND_DIRS = (
    "backend/mastery",
    "backend/projects",
    "backend/schema",
    "backend/segments",
    "backend/units",
)

TEXT_SUFFIXES = {
    ".css", ".csv", ".html", ".ipynb", ".js", ".json", ".jsonl",
    ".md", ".py", ".svg", ".tsv", ".txt", ".xml",
}

# PRIVACY_PATTERN_DEFINITIONS_START
_USER_DIR = "Us" + "ers"
_TOKEN_WORD = "to" + "ken"
_TTP_LABEL = "TT" + "P"
_TTP_EXPANSION = "Translation and " + "Transcription Project"

PRIVATE_PATTERNS = {
    "windows_user_path": re.compile(
        r"C:" + re.escape("\\") + _USER_DIR + re.escape("\\"),
        re.IGNORECASE,
    ),
    "mac_user_path": re.compile("/" + _USER_DIR + "/", re.IGNORECASE),
    "private_folder": re.compile(
        r"[\\/](?:AppData|Obsidian(?: notes)?|Downloads)[\\/]",
        re.IGNORECASE,
    ),
    "codex_link": re.compile("codex" + "://", re.IGNORECASE),
    "credential": re.compile(
        r"(?:authorization\s*:\s*(?:bearer|" + _TOKEN_WORD + r")|"
        r"access[_ -]?" + _TOKEN_WORD + r"|"
        r"api[_ -]?key|github_pat_|ghp_[A-Za-z0-9])",
        re.IGNORECASE,
    ),
    "credential_filename": re.compile(
        r"(?:zenodo|github|figshare).{0,24}" + _TOKEN_WORD, re.IGNORECASE
    ),
    "ttp_prose": re.compile(r"\b" + _TTP_LABEL + r"\b|" + _TTP_EXPANSION),
}
# PRIVACY_PATTERN_DEFINITIONS_END

CH03_SUPERSEDED = {
    "source/id-ID/O005-LEGA-V101-CH03/assets/phase-portrait-construction-id.png",
    "source/id-ID/O005-LEGA-V101-CH03/assets/phase-portrait-construction-id.provenance.json",
    "source/id-ID/O005-LEGA-V101-CH03/assets/phase-portrait-construction-id-v2.png",
    "source/id-ID/O005-LEGA-V101-CH03/assets/phase-portrait-construction-id-v2.provenance.json",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def include_file(path: Path) -> bool:
    rel = relative(path)
    parts = path.relative_to(ROOT).parts
    return (
        path.is_file()
        and not path.is_symlink()
        and "__pycache__" not in parts
        and ".pytest_cache" not in parts
        and path.suffix.lower() not in {".pyc", ".pyo"}
        and rel not in CH03_SUPERSEDED
        and "/project_archives/" not in f"/{rel}/"
    )


def collect_tree(relative_root: str) -> list[Path]:
    root = ROOT / relative_root
    if not root.is_dir():
        raise FileNotFoundError(root)
    return [path for path in root.rglob("*") if include_file(path)]


def source_files() -> list[Path]:
    files: list[Path] = []
    for name in (
        *ROOT_FILES,
        *CONTROL_FILES,
        *TERMINOLOGY_WITNESS_FILES,
        *SCRIPT_FILES,
    ):
        path = ROOT / name
        if not path.is_file():
            raise FileNotFoundError(path)
        files.append(path)
    files.extend(collect_tree("source/reader"))
    for backend_dir in BACKEND_DIRS:
        files.extend(collect_tree(backend_dir))
    for unit_id in UNIT_IDS:
        files.extend(collect_tree(f"source/id-ID/{unit_id}"))
        files.extend(collect_tree(f"authority/units/{unit_id}"))
    ordered = sorted(set(files), key=relative)
    if any(not include_file(path) for path in ordered):
        raise RuntimeError("source allowlist contains an excluded path")
    return ordered


def scan_text(payload: bytes, label: str) -> int:
    try:
        value = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"declared text is not UTF-8: {label}") from exc
    if label == "scripts/build_reader_first_release.py":
        value = re.sub(
            r"# PRIVACY_PATTERN_DEFINITIONS_START.*?"
            r"# PRIVACY_PATTERN_DEFINITIONS_END",
            "",
            value,
            flags=re.DOTALL,
        )
    for name, pattern in PRIVATE_PATTERNS.items():
        if pattern.search(value):
            raise RuntimeError(f"private/publication marker {name} in {label}")
    return len(payload)


def privacy_scan(files: list[Path]) -> dict[str, int]:
    scanned_files = 0
    scanned_bytes = 0
    for path in files:
        if path.suffix.lower() in TEXT_SUFFIXES:
            scanned_bytes += scan_text(path.read_bytes(), relative(path))
            scanned_files += 1
    return {"text_files": scanned_files, "text_bytes": scanned_bytes}


def package_manifest(files: list[Path]) -> bytes:
    rows = ["path\tbytes\tsha256"]
    for path in files:
        rows.append(f"{relative(path)}\t{path.stat().st_size}\t{sha256_file(path)}")
    return ("\n".join(rows) + "\n").encode("utf-8")


def zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (0o100644 & 0xFFFF) << 16
    return info


def safe_zip_info(info: zipfile.ZipInfo) -> None:
    path = PurePosixPath(info.filename)
    if path.is_absolute() or ".." in path.parts or "\\" in info.filename:
        raise RuntimeError(f"unsafe ZIP member: {info.filename}")
    mode = (info.external_attr >> 16) & 0xFFFF
    if mode and (mode & 0o170000) == 0o120000:
        raise RuntimeError(f"symlink ZIP member: {info.filename}")


def build_source_zip(
    output: Path, files: list[Path], release_label: str
) -> dict[str, object]:
    archive_path = output / (
        f"02_O005_LEGA_v1.01_id_{release_label}_compact_source.zip"
    )
    manifest = package_manifest(files)
    with zipfile.ZipFile(
        archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        archive.writestr(zip_info("SOURCE_PACKAGE_MANIFEST.tsv"), manifest)
        for path in files:
            archive.writestr(zip_info(relative(path)), path.read_bytes())

    expected = ["SOURCE_PACKAGE_MANIFEST.tsv", *(relative(path) for path in files)]
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if names != expected or len(names) != len(set(names)):
            raise RuntimeError("ZIP closure, order, or member uniqueness differs")
        if archive.testzip() is not None:
            raise RuntimeError("ZIP CRC verification failed")
        for info in archive.infolist():
            safe_zip_info(info)
        if archive.read("SOURCE_PACKAGE_MANIFEST.tsv") != manifest:
            raise RuntimeError("embedded source manifest differs")
        for path in files:
            if archive.read(relative(path)) != path.read_bytes():
                raise RuntimeError(f"archived bytes differ: {relative(path)}")
    return {
        "path": archive_path.name,
        "bytes": archive_path.stat().st_size,
        "sha256": sha256_file(archive_path),
        "members": len(expected),
        "payload_files": len(files),
        "payload_bytes": sum(path.stat().st_size for path in files),
        "embedded_manifest_sha256": sha256_bytes(manifest),
    }


def copy_exact(source: Path, destination: Path) -> dict[str, object]:
    shutil.copyfile(source, destination)
    if source.read_bytes() != destination.read_bytes():
        raise RuntimeError(f"copy differs: {destination}")
    return {
        "path": destination.name,
        "bytes": destination.stat().st_size,
        "sha256": sha256_file(destination),
    }


def prepare_output(output: Path) -> None:
    resolved = output.resolve()
    release_root = (ROOT / "release" / "zenodo").resolve()
    if resolved.parent != release_root or not resolved.name.startswith(
        "reader-first-"
    ):
        raise RuntimeError(f"refusing unexpected output: {resolved}")
    if resolved == PUBLISHED_OUTPUT.resolve():
        raise RuntimeError(
            "refusing to overwrite the published CH14 byte replica"
        )
    if resolved.exists():
        raise RuntimeError(f"refusing to overwrite existing output: {resolved}")
    resolved.mkdir(parents=True)


def build(output: Path, version: str, release_label: str) -> dict[str, object]:
    if not version.strip():
        raise RuntimeError("version must not be empty")
    if version == PUBLISHED_VERSION:
        raise RuntimeError(
            "the published CH14 version label is immutable and reserved"
        )
    if not re.fullmatch(r"[A-Za-z0-9._-]+", release_label):
        raise RuntimeError("release label contains unsafe characters")
    prepare_output(output)
    files = source_files()
    privacy = privacy_scan(files)

    reader = PdfReader(PDF_SOURCE, strict=True)
    if len(reader.pages) != 297:
        raise RuntimeError("expected 297-page reader")
    if reader.root_object.get("/Lang") != "id":
        raise RuntimeError("reader PDF language is not Indonesian")
    if not reader.root_object.get("/StructTreeRoot"):
        raise RuntimeError("reader PDF is not tagged")
    if len(reader.outline) != 20:
        raise RuntimeError("reader PDF outline closure differs")

    pdf_artifact = copy_exact(PDF_SOURCE, output / PDF_SOURCE.name)
    pdf_artifact.update(
        {"role": "primary_reader", "pages": 297, "language": "id", "tagged": True}
    )
    source_artifact = build_source_zip(output, files, release_label)
    source_artifact["role"] = "compact_resumable_source"
    license_artifact = copy_exact(ROOT / "LICENSE.md", output / "LICENSE.md")
    license_artifact["role"] = "license"

    release = {
        "schema": "o005-reader-first-progress-release-v1",
        "title": "Pengantar Pemodelan Matematika — Edisi Bahasa Indonesia",
        "version": version,
        "status": "partial",
        "language": "id-ID",
        "license": "CC BY-NC-SA 4.0",
        "source": {
            "creator": "Joceline Lega",
            "work": "Introduction to Mathematical Modeling",
            "edition": "University of Arizona Pressbooks v1.01 (March 2026)",
            "url": "https://opentextbooks.library.arizona.edu/mathematicalmodeling/",
        },
        "coverage": {
            "completed_units": list(UNIT_IDS),
            "chapters": "1–14",
            "part_introductions": "2–5",
            "problems_with_mastery_support": 113,
            "chapter_notebooks": 10,
            "project_notebooks": 12,
            "project_packets": 12,
        },
        "remaining": [
            "Preface",
            "Part 1 introduction",
            "Accessibility Statement",
            "Version History",
            "four original bridge modules",
        ],
        "non_endorsement": (
            "Independent Indonesian edition; not endorsed by Joceline Lega "
            "or the University of Arizona."
        ),
        "privacy_scan": privacy,
        "artifacts": [pdf_artifact, source_artifact, license_artifact],
    }
    manifest_path = output / "RELEASE_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(release, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    scan_text(manifest_path.read_bytes(), manifest_path.name)

    checksum_targets = [
        output / str(item["path"]) for item in release["artifacts"]
    ] + [manifest_path]
    checksums_path = output / "CHECKSUMS.sha256"
    checksums_path.write_text(
        "".join(
            f"{sha256_file(path)}  {path.name}\n" for path in checksum_targets
        ),
        encoding="ascii",
        newline="\n",
    )

    public_files = [*checksum_targets, checksums_path]
    total_bytes = sum(path.stat().st_size for path in public_files)
    if total_bytes > 500_000_000:
        raise RuntimeError(f"payload exceeds 500,000,000 bytes: {total_bytes}")
    for path in public_files:
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f"missing/empty release file: {path}")

    result = {
        "output": str(output),
        "public_files": [
            {
                "path": path.name,
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in public_files
        ],
        "public_file_count": len(public_files),
        "public_total_bytes": total_bytes,
        "source_payload_files": len(files),
        "source_payload_bytes": sum(path.stat().st_size for path in files),
        "privacy_scan": privacy,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--release-label", required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    print(
        json.dumps(
            build(output, args.version, args.release_label),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
