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

from bs4 import BeautifulSoup
from pypdf import PdfReader

from o005_release_constants import (
    CANONICAL_TITLE,
    COMPLETE_SUBJECT,
    MODEL_IDENTIFICATION,
    SOURCE_AUTHOR,
)


ROOT = Path(__file__).resolve().parents[1]
PUBLISHED_OUTPUT = ROOT / "release" / "zenodo" / "reader-first-CH14"
PUBLISHED_VERSION = "v1.01-id-progress-CH14-reader-20260822"
PROGRESS_PDF_SOURCE = (
    ROOT
    / "output"
    / "pdf"
    / "01_Pengantar_Pemodelan_Matematika_Edisi_Bahasa_Indonesia_CH14.pdf"
)
COMPLETE_PDF_SOURCE = (
    ROOT
    / "output"
    / "pdf"
    / "01_Pengantar_Pemodelan_Matematika_Edisi_Bahasa_Indonesia_Lengkap.pdf"
)
COMPLETE_BUILD_RECEIPT_SOURCE = COMPLETE_PDF_SOURCE.with_suffix(".build.json")
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)

PROGRESS_UNIT_IDS = tuple(
    f"O005-LEGA-V101-{short}"
    for short in (
        "CH01", "CH02", "PT02", "CH03", "CH04", "PT03", "CH05",
        "CH06", "CH07", "PT04", "CH08", "CH09", "CH10", "PT05",
        "CH11", "CH12", "CH13", "CH14",
    )
)

COMPLETE_UNIT_IDS = (
    "O005-LEGA-V101-FM01",
    "O005-LEGA-V101-PT01",
    "O005-LEGA-V101-CH01",
    "O005-LEGA-V101-CH02",
    "O005-LEGA-V101-PT02",
    "O005-LEGA-V101-CH03",
    "O005-LEGA-V101-CH04",
    "O005-LEGA-V101-PT03",
    "O005-LEGA-V101-CH05",
    "O005-LEGA-V101-CH06",
    "O005-LEGA-V101-CH07",
    "O005-LEGA-V101-PT04",
    "O005-LEGA-V101-CH08",
    "O005-LEGA-V101-CH09",
    "O005-LEGA-V101-CH10",
    "O005-LEGA-V101-PT05",
    "O005-LEGA-V101-CH11",
    "O005-LEGA-V101-CH12",
    "O005-LEGA-V101-CH13",
    "O005-LEGA-V101-CH14",
    "O005-LEGA-V101-BM01",
    "O005-LEGA-V101-BM02",
    "O005-BRIDGE-C1",
    "O005-BRIDGE-C2",
    "O005-BRIDGE-C3",
    "O005-BRIDGE-C4",
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
    "scripts/build_bridge_unit.py",
    "scripts/build_ch14_project_packets.py",
    "scripts/build_progress_pdf.py",
    "scripts/build_reader_first_release.py",
    "scripts/build_unit_reader.py",
    "scripts/execute_bridge_notebook_jupyter.py",
    "scripts/freeze_pressbooks.py",
    "scripts/generate_bridge_c1.py",
    "scripts/generate_bridge_c2.py",
    "scripts/generate_bridge_c3.py",
    "scripts/generate_bridge_c4.py",
    "scripts/o005_release_constants.py",
    "scripts/prepare_unit.py",
    "scripts/qa_bridge_unit.py",
    "scripts/qa_unit.py",
)

BACKEND_DIRS = (
    "backend/mastery",
    "backend/projects",
    "backend/schema",
    "backend/segment-ids",
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


def require_complete_pdf_receipt(
    reader: PdfReader, pdf_source: Path, unit_ids: tuple[str, ...]
) -> dict[str, object]:
    if not COMPLETE_BUILD_RECEIPT_SOURCE.is_file():
        raise FileNotFoundError(COMPLETE_BUILD_RECEIPT_SOURCE)
    receipt = json.loads(COMPLETE_BUILD_RECEIPT_SOURCE.read_text(encoding="utf-8"))
    expected_header = {
        "schema": "o005-complete-pdf-build-receipt-v1",
        "mode": "complete",
        "title": CANONICAL_TITLE,
        "author": SOURCE_AUTHOR,
        "subject": COMPLETE_SUBJECT,
        "model_identification": MODEL_IDENTIFICATION,
    }
    for key, expected in expected_header.items():
        if receipt.get(key) != expected:
            raise RuntimeError(f"complete PDF receipt differs for {key}")
    if receipt.get("ordered_unit_ids") != list(unit_ids):
        raise RuntimeError("complete PDF receipt unit order differs")

    inputs = receipt.get("reader_inputs")
    if not isinstance(inputs, list) or len(inputs) != len(unit_ids):
        raise RuntimeError("complete PDF receipt reader-input closure differs")
    source_mastery_records = 0
    bridge_mastery_records = 0
    for unit_id, record in zip(unit_ids, inputs, strict=True):
        if not isinstance(record, dict) or record.get("unit_id") != unit_id:
            raise RuntimeError("complete PDF receipt reader-input order differs")
        for key, path in (
            ("index", ROOT / "build" / "reader" / unit_id / "index.html"),
            (
                "package_manifest",
                ROOT / "build" / "reader" / unit_id / "PACKAGE_MANIFEST.tsv",
            ),
        ):
            identity = record.get(key)
            if not isinstance(identity, dict) or not path.is_file():
                raise RuntimeError(f"complete PDF receipt lacks {key} for {unit_id}")
            expected_identity = {
                "path": relative(path),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            if identity != expected_identity:
                raise RuntimeError(
                    f"complete PDF receipt is stale for {unit_id} {key}"
                )
        index_path = ROOT / "build" / "reader" / unit_id / "index.html"
        soup = BeautifulSoup(index_path.read_text(encoding="utf-8"), "lxml")
        mastery_record_count = len(soup.select(".mastery-record"))
        if record.get("mastery_record_count") != mastery_record_count:
            raise RuntimeError(
                f"complete PDF receipt mastery count differs for {unit_id}"
            )
        if unit_id.startswith("O005-BRIDGE-"):
            bridge_mastery_records += mastery_record_count
        else:
            source_mastery_records += mastery_record_count

    expected_mastery = {
        "source_records": 113,
        "bridge_records": 28,
        "total_records": 141,
    }
    actual_mastery = {
        "source_records": source_mastery_records,
        "bridge_records": bridge_mastery_records,
        "total_records": source_mastery_records + bridge_mastery_records,
    }
    if actual_mastery != expected_mastery:
        raise RuntimeError(
            f"complete reader mastery-record closure differs: {actual_mastery!r}"
        )
    if receipt.get("mastery_records") != actual_mastery:
        raise RuntimeError("complete PDF receipt mastery summary differs")

    joined_html = receipt.get("joined_html")
    if (
        not isinstance(joined_html, dict)
        or not isinstance(joined_html.get("bytes"), int)
        or joined_html["bytes"] <= 0
        or not re.fullmatch(r"[0-9a-f]{64}", str(joined_html.get("sha256", "")))
    ):
        raise RuntimeError("complete PDF receipt joined-HTML identity is invalid")

    pdf_identity = receipt.get("pdf")
    expected_pdf_identity = {
        "path": pdf_source.name,
        "bytes": pdf_source.stat().st_size,
        "sha256": sha256_file(pdf_source),
        "pages": len(reader.pages),
        "tagged": True,
        "language": "id",
    }
    if pdf_identity != expected_pdf_identity:
        raise RuntimeError("complete PDF receipt PDF identity differs")

    metadata = reader.metadata
    expected_metadata = {
        "/Title": CANONICAL_TITLE,
        "/Author": SOURCE_AUTHOR,
        "/Creator": MODEL_IDENTIFICATION,
        "/Subject": COMPLETE_SUBJECT,
    }
    if metadata is None or any(
        metadata.get(key) != expected for key, expected in expected_metadata.items()
    ):
        raise RuntimeError("complete PDF metadata differs")
    if reader.root_object.get("/Lang") != "id":
        raise RuntimeError("complete PDF language is not Indonesian")
    mark_info = reader.root_object.get("/MarkInfo")
    if mark_info is None or not bool(mark_info.get_object().get("/Marked")):
        raise RuntimeError("complete PDF /MarkInfo is not marked")
    struct_tree = reader.root_object.get("/StructTreeRoot")
    if struct_tree is None:
        raise RuntimeError("complete PDF is not tagged")
    struct_tree = struct_tree.get_object()
    if not struct_tree.get("/K") or struct_tree.get("/ParentTree") is None:
        raise RuntimeError("complete PDF structure tree is incomplete")
    for page_index, page in enumerate(reader.pages):
        if page.get("/StructParents") is None:
            raise RuntimeError(
                f"complete PDF page {page_index + 1} lacks /StructParents"
            )
        if page_index > 0 and not has_pagination_footer_artifact(page):
            raise RuntimeError(
                f"complete PDF footer on page {page_index + 1} is not an artifact"
            )

    outline = reader.outline
    if any(isinstance(item, list) for item in outline):
        raise RuntimeError("complete PDF outline is not flat")
    actual_outline = [
        {
            "title": str(getattr(item, "title", "")),
            "page_index": reader.get_destination_page_number(item),
        }
        for item in outline
    ]
    if actual_outline != receipt.get("outline"):
        raise RuntimeError("complete PDF outline differs from its build receipt")
    if len(actual_outline) != 2 + len(unit_ids):
        raise RuntimeError("complete PDF outline closure differs")
    if any(
        item["page_index"] < 0 or item["page_index"] >= len(reader.pages)
        for item in actual_outline
    ):
        raise RuntimeError("complete PDF outline has an invalid page destination")

    visible_text = " ".join(
        " ".join((page.extract_text() or "").split()) for page in reader.pages
    )
    if MODEL_IDENTIFICATION not in visible_text:
        raise RuntimeError("complete PDF lacks visible model provenance")
    return receipt


def has_pagination_footer_artifact(page: object) -> bool:
    contents = page.get_contents()
    if contents is None:
        return False
    footer_depth: int | None = None
    marked_depth = 0
    for operands, operator in contents.operations:
        if operator in {b"BDC", b"BMC"}:
            marked_depth += 1
            if operator == b"BDC" and footer_depth is None and len(operands) >= 2:
                properties = operands[1]
                if hasattr(properties, "get_object"):
                    properties = properties.get_object()
                if (
                    str(operands[0]) == "/Artifact"
                    and hasattr(properties, "get")
                    and str(properties.get("/Type")) == "/Pagination"
                    and str(properties.get("/Subtype")) == "/Footer"
                ):
                    footer_depth = marked_depth
        elif operator == b"EMC":
            if footer_depth == marked_depth:
                return True
            if marked_depth > 0:
                marked_depth -= 1
    return False


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


def source_files(unit_ids: tuple[str, ...]) -> list[Path]:
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
    for unit_id in unit_ids:
        files.extend(collect_tree(f"source/id-ID/{unit_id}"))
        files.extend(collect_tree(f"authority/units/{unit_id}"))
    ordered = sorted(set(files), key=relative)
    if any(not include_file(path) for path in ordered):
        raise RuntimeError("source allowlist contains an excluded path")
    return ordered


def segment_counts(unit_ids: tuple[str, ...]) -> dict[str, int]:
    """Count the canonical backend segment records for the selected units.

    Counts are derived from the exact JSONL files that enter the compact source
    package, so release metadata cannot lag behind a newly admitted unit.
    """
    counts = {"source": 0, "bridge": 0}
    for unit_id in unit_ids:
        path = ROOT / "backend" / "segments" / f"{unit_id}.segments.jsonl"
        if not path.is_file():
            raise FileNotFoundError(path)
        count = sum(
            1 for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
        bucket = "bridge" if unit_id.startswith("O005-BRIDGE-") else "source"
        counts[bucket] += count
    counts["total"] = counts["source"] + counts["bridge"]
    return counts


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


def scan_public_reader_and_pdf_surfaces(
    reader: PdfReader, pdf_source: Path, unit_ids: tuple[str, ...]
) -> dict[str, int]:
    text_files = 0
    text_bytes = 0
    for unit_id in unit_ids:
        for name in ("index.html", "PACKAGE_MANIFEST.tsv"):
            path = ROOT / "build" / "reader" / unit_id / name
            if not path.is_file():
                raise FileNotFoundError(path)
            text_bytes += scan_text(path.read_bytes(), relative(path))
            text_files += 1

    extracted_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    extracted_payload = extracted_text.encode("utf-8")
    text_bytes += scan_text(extracted_payload, "complete PDF extracted text")

    metadata_payload = json.dumps(
        {str(key): str(value) for key, value in (reader.metadata or {}).items()},
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    text_bytes += scan_text(metadata_payload, "complete PDF metadata")

    uris: list[str] = []
    for page in reader.pages:
        for annotation_ref in page.get("/Annots") or []:
            annotation = annotation_ref.get_object()
            action_ref = annotation.get("/A")
            if action_ref is None:
                continue
            action = action_ref.get_object()
            uri = action.get("/URI")
            if uri is not None:
                uris.append(str(uri))
    uri_payload = json.dumps(uris, ensure_ascii=False, sort_keys=True).encode("utf-8")
    text_bytes += scan_text(uri_payload, "complete PDF URI annotations")

    raw_pdf_value = pdf_source.read_bytes().decode("latin-1")
    for name, pattern in PRIVATE_PATTERNS.items():
        if name == "ttp_prose":
            # A three-byte prose token can occur accidentally in compressed
            # streams; meaningful text/metadata/URI surfaces are scanned above.
            continue
        if pattern.search(raw_pdf_value):
            raise RuntimeError(
                f"private/publication marker {name} in complete PDF raw bytes"
            )

    return {
        "reader_files": 2 * len(unit_ids),
        "reader_and_pdf_text_surfaces": 2 * len(unit_ids) + 3,
        "reader_and_pdf_text_bytes": text_bytes,
        "pdf_uri_annotations": len(uris),
        "pdf_raw_bytes": pdf_source.stat().st_size,
    }


def privacy_scan(files: list[tuple[Path, bytes]]) -> dict[str, int]:
    scanned_files = 0
    scanned_bytes = 0
    for path, payload in files:
        if path.suffix.lower() in TEXT_SUFFIXES:
            scanned_bytes += scan_text(payload, relative(path))
            scanned_files += 1
    return {"text_files": scanned_files, "text_bytes": scanned_bytes}


def package_manifest(files: list[tuple[Path, bytes]]) -> bytes:
    rows = ["path\tbytes\tsha256"]
    for path, payload in files:
        rows.append(f"{relative(path)}\t{len(payload)}\t{sha256_bytes(payload)}")
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
    output: Path, files: list[tuple[Path, bytes]], release_label: str
) -> dict[str, object]:
    archive_path = output / (
        f"02_O005_LEGA_v1.01_id_{release_label}_compact_source.zip"
    )
    manifest = package_manifest(files)
    with zipfile.ZipFile(
        archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        archive.writestr(zip_info("SOURCE_PACKAGE_MANIFEST.tsv"), manifest)
        for path, payload in files:
            archive.writestr(zip_info(relative(path)), payload)

    expected = [
        "SOURCE_PACKAGE_MANIFEST.tsv", *(relative(path) for path, _ in files)
    ]
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
        for path, payload in files:
            archived = archive.read(relative(path))
            if archived != payload:
                raise RuntimeError(f"archived bytes differ: {relative(path)}")
            if path.suffix.lower() in TEXT_SUFFIXES:
                scan_text(archived, relative(path))
    return {
        "path": archive_path.name,
        "bytes": archive_path.stat().st_size,
        "sha256": sha256_file(archive_path),
        "members": len(expected),
        "payload_files": len(files),
        "payload_bytes": sum(len(payload) for _, payload in files),
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


def build(
    output: Path,
    version: str,
    release_label: str,
    complete: bool = False,
) -> dict[str, object]:
    if not version.strip():
        raise RuntimeError("version must not be empty")
    if version == PUBLISHED_VERSION:
        raise RuntimeError(
            "the published CH14 version label is immutable and reserved"
        )
    if not re.fullmatch(r"[A-Za-z0-9._-]+", release_label):
        raise RuntimeError("release label contains unsafe characters")
    unit_ids = COMPLETE_UNIT_IDS if complete else PROGRESS_UNIT_IDS
    pdf_source = COMPLETE_PDF_SOURCE if complete else PROGRESS_PDF_SOURCE
    source_paths = source_files(unit_ids)
    files = [(path, path.read_bytes()) for path in source_paths]
    privacy = privacy_scan(files)
    segments = segment_counts(unit_ids)

    reader = PdfReader(pdf_source, strict=True)
    page_count = len(reader.pages)
    validated_receipt: dict[str, object] | None = None
    if complete:
        if page_count <= 297:
            raise RuntimeError("complete reader did not grow beyond the CH14 checkpoint")
        validated_receipt = require_complete_pdf_receipt(
            reader, pdf_source, unit_ids
        )
    elif page_count != 297:
        raise RuntimeError("expected 297-page reader")
    if reader.root_object.get("/Lang") != "id":
        raise RuntimeError("reader PDF language is not Indonesian")
    if not reader.root_object.get("/StructTreeRoot"):
        raise RuntimeError("reader PDF is not tagged")
    expected_outline_entries = 2 + len(unit_ids)
    if len(reader.outline) != expected_outline_entries:
        raise RuntimeError("reader PDF outline closure differs")
    public_surface_privacy = scan_public_reader_and_pdf_surfaces(
        reader, pdf_source, unit_ids
    )

    prepare_output(output)
    pdf_artifact = copy_exact(pdf_source, output / pdf_source.name)
    if complete:
        if validated_receipt is None:
            raise RuntimeError("complete PDF receipt validation was not retained")
        receipt_pdf = validated_receipt.get("pdf")
        if not isinstance(receipt_pdf, dict) or any(
            pdf_artifact.get(key) != receipt_pdf.get(key)
            for key in ("bytes", "sha256")
        ):
            raise RuntimeError("copied complete PDF differs from validated receipt")
    pdf_artifact.update(
        {
            "role": "primary_reader",
            "pages": page_count,
            "language": "id",
            "tagged": True,
            "outline_entries": expected_outline_entries,
        }
    )
    source_artifact = build_source_zip(output, files, release_label)
    source_artifact["role"] = "compact_resumable_source"
    release_artifacts = [pdf_artifact, source_artifact]
    if complete:
        receipt_artifact = copy_exact(
            COMPLETE_BUILD_RECEIPT_SOURCE,
            output / "03_O005_LEGA_v1.01_id_complete_pdf_build_receipt.json",
        )
        scan_text(
            (output / str(receipt_artifact["path"])).read_bytes(),
            str(receipt_artifact["path"]),
        )
        copied_receipt_path = output / str(receipt_artifact["path"])
        copied_receipt = json.loads(copied_receipt_path.read_text(encoding="utf-8"))
        if copied_receipt != validated_receipt:
            raise RuntimeError("copied PDF receipt differs from validated receipt")
        receipt_artifact["role"] = "pdf_build_receipt"
        release_artifacts.append(receipt_artifact)
    license_artifact = copy_exact(ROOT / "LICENSE.md", output / "LICENSE.md")
    license_artifact["role"] = "license"
    release_artifacts.append(license_artifact)

    release = {
        "schema": (
            "o005-reader-first-complete-release-v1"
            if complete
            else "o005-reader-first-progress-release-v1"
        ),
        "title": CANONICAL_TITLE,
        "version": version,
        "status": "complete" if complete else "partial",
        "language": "id-ID",
        "license": "CC BY-NC-SA 4.0",
        "production_model": MODEL_IDENTIFICATION,
        "source": {
            "creator": SOURCE_AUTHOR,
            "work": "Introduction to Mathematical Modeling",
            "edition": "University of Arizona Pressbooks v1.01 (March 2026)",
            "url": "https://opentextbooks.library.arizona.edu/mathematicalmodeling/",
        },
        "coverage": {
            "completed_units": list(unit_ids),
            "chapters": "1–14",
            "part_introductions": "1–5" if complete else "2–5",
            "source_unit_records": 22 if complete else 18,
            "original_bridge_modules": 4 if complete else 0,
            "source_problems_with_mastery_support": 113,
            "bridge_problems_with_mastery_support": 28 if complete else 0,
            "total_problems_with_mastery_support": 141 if complete else 113,
            "chapter_notebooks": 10,
            "project_notebooks": 12,
            "project_packets": 12,
            "bridge_notebooks": 4 if complete else 0,
            "total_notebooks": 26 if complete else 22,
            "source_segments": segments["source"],
            "bridge_segments": segments["bridge"],
            "total_segments": segments["total"],
        },
        "remaining": [] if complete else [
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
        "public_surface_privacy_scan": public_surface_privacy,
        "artifacts": release_artifacts,
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
        "source_payload_bytes": sum(len(payload) for _, payload in files),
        "privacy_scan": privacy,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--release-label", required=True)
    parser.add_argument(
        "--complete",
        action="store_true",
        help="Package the complete 22-source-unit plus four-bridge reader",
    )
    args = parser.parse_args()
    output = args.output.resolve()
    print(
        json.dumps(
            build(output, args.version, args.release_label, complete=args.complete),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
