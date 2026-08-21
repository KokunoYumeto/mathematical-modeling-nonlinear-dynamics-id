#!/usr/bin/env python3
"""Freeze and verify the official LibreTexts semantic source for O005/C120.

The authoritative unit is the public page graph for LibreTexts book ``math-7767``.
The script records the raw HTTP representations, a deterministic serialization of
each semantic content section, every referenced reader asset, and canonical CSV
manifests.  It intentionally does not use Git or any authenticated endpoint.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import Request, urlopen

from lxml import etree, html


BOOK_ID = "math-7767"
METADATA_URL = f"https://commons.libretexts.org/api/v1/commons/book/{BOOK_ID}"
TOC_URL = f"https://commons.libretexts.org/api/v1/commons/book/{BOOK_ID}/toc"
USER_AGENT = "O005-C120-source-freezer/1.0 (+noncommercial translation QA)"
MAX_PAGE_BYTES = 4_000_000
MAX_ASSET_BYTES = 80_000_000
MAX_TOTAL_ASSET_BYTES = 800_000_000
EXPECTED_LICENSE = "ccbyncsa"
EXPECTED_LICENSE_VERSION = "30"
CC_BY_NC_SA_30 = "https://creativecommons.org/licenses/by-nc-sa/3.0"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str, limit: int) -> tuple[bytes, str, str]:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Encoding": "identity",
        },
    )
    with urlopen(request, timeout=90) as response:
        final_url = response.geturl()
        content_type = response.headers.get("Content-Type", "")
        data = response.read(limit + 1)
    if len(data) > limit:
        raise RuntimeError(f"response exceeds {limit} bytes: {url}")
    return data, final_url, content_type


def flatten_toc(root: dict) -> list[dict]:
    rows: list[dict] = []

    def visit(node: dict, depth: int, parent_id: str) -> None:
        page_id = str(node.get("id", ""))
        title = node.get("title")
        url = node.get("url")
        if not page_id.isdigit() or not isinstance(title, str) or not isinstance(url, str):
            raise RuntimeError(f"invalid TOC node: {node!r}")
        rows.append(
            {
                "ordinal": len(rows) + 1,
                "depth": depth,
                "parent_id": parent_id,
                "page_id": page_id,
                "title": title,
                "url": url,
            }
        )
        children = node.get("children") or []
        if not isinstance(children, list):
            raise RuntimeError(f"invalid children for page {page_id}")
        for child in children:
            visit(child, depth + 1, page_id)

    visit(root, 0, "")
    ids = [row["page_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate LibreTexts page IDs")
    return rows


def canonical_csv(fieldnames: list[str], rows: list[dict]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def safe_asset_name(url: str) -> str:
    parsed = urlparse(url)
    basename = unquote(Path(parsed.path).name) or "asset"
    basename = re.sub(r"[^A-Za-z0-9._-]+", "_", basename).strip("._") or "asset"
    return f"{sha256(url.encode('utf-8'))[:16]}-{basename}"


def parse_page(body: bytes, expected_id: str, base_url: str) -> tuple[bytes, dict, set[str]]:
    text = body.decode("utf-8")
    page_id_match = re.search(r'"pageId"\s*:\s*(\d+)', text)
    revision_match = re.search(r'"pageRevision"\s*:\s*"(\d+)"', text)
    if not page_id_match or page_id_match.group(1) != expected_id:
        raise RuntimeError(f"page-ID mismatch for {base_url}")
    if not revision_match:
        raise RuntimeError(f"missing page revision for {base_url}")

    document = html.fromstring(text)
    sections = document.xpath(
        "//section[contains(concat(' ', normalize-space(@class), ' '), "
        "' mt-content-container ')]"
    )
    if len(sections) != 1:
        raise RuntimeError(f"expected one semantic content section for {base_url}, got {len(sections)}")
    section = sections[0]
    fragment = etree.tostring(section, encoding="utf-8", method="html", with_tail=False)

    modified = document.xpath("string(//meta[@property='article:modified_time']/@content)")
    published = document.xpath("string(//meta[@property='article:published_time']/@content)")
    canonical = document.xpath("string(//link[@rel='canonical']/@href)")
    if canonical.rstrip("/") != base_url.rstrip("/"):
        raise RuntimeError(f"canonical URL mismatch for page {expected_id}")

    license_links = {
        href.rstrip("/")
        for href in section.xpath(".//a[contains(@href, 'creativecommons.org/licenses')]/@href")
    }
    if license_links and license_links != {CC_BY_NC_SA_30}:
        raise RuntimeError(f"unexpected page license for {expected_id}: {sorted(license_links)}")

    assets: set[str] = set()
    for element in section.xpath(".//*[@src or @poster or @data]"):
        for attribute in ("src", "poster", "data"):
            value = element.get(attribute)
            if value and not value.startswith(("data:", "javascript:", "#")):
                resolved = urljoin(base_url, value)
                if "/@api/deki/files/" in resolved or element.tag in {
                    "img",
                    "audio",
                    "video",
                    "source",
                    "object",
                }:
                    assets.add(resolved)
    for href in section.xpath(".//a[@href]/@href"):
        resolved = urljoin(base_url, href)
        if "/@api/deki/files/" in resolved:
            assets.add(resolved)

    return fragment, {
        "revision": revision_match.group(1),
        "published": published,
        "modified": modified,
        "license": CC_BY_NC_SA_30 if license_links else "",
    }, assets


def write_exact(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def hash_tree(root: Path) -> list[dict]:
    rows = []
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda p: p.relative_to(root).as_posix()):
        data = path.read_bytes()
        rows.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": len(data),
                "sha256": sha256(data),
            }
        )
    return rows


def freeze(lane: Path) -> None:
    archives = lane / "authority" / "archives"
    raw_root = lane / "authority" / "extracted" / "libretexts-html-raw"
    fragment_root = lane / "authority" / "extracted" / "libretexts-html-fragments"
    asset_root = lane / "authority" / "extracted" / "libretexts-assets"
    for path in (raw_root, fragment_root, asset_root):
        if path.exists() and any(path.iterdir()):
            raise RuntimeError(f"refusing to overwrite nonempty frozen directory: {path}")
        path.mkdir(parents=True, exist_ok=True)

    metadata_bytes, metadata_final, metadata_type = fetch(METADATA_URL, 2_000_000)
    toc_bytes, toc_final, toc_type = fetch(TOC_URL, 8_000_000)
    metadata_payload = json.loads(metadata_bytes)
    toc_payload = json.loads(toc_bytes)
    if metadata_payload.get("err") is not False or not isinstance(metadata_payload.get("book"), dict):
        raise RuntimeError("invalid book-metadata API response")
    metadata = metadata_payload["book"]
    if metadata.get("bookID") != BOOK_ID:
        raise RuntimeError("unexpected LibreTexts book ID")
    library_tags = metadata.get("libraryTags") or []
    license_versions = {
        tag.split(":", 1)[1]
        for tag in library_tags
        if isinstance(tag, str) and tag.startswith("licenseversion:")
    }
    if metadata.get("license") != EXPECTED_LICENSE or license_versions != {EXPECTED_LICENSE_VERSION}:
        raise RuntimeError("unexpected book-level license metadata")
    if toc_payload.get("err") is not False or not isinstance(toc_payload.get("toc"), dict):
        raise RuntimeError("invalid TOC API response")
    toc_rows = flatten_toc(toc_payload["toc"])

    write_exact(archives / "libretexts-book-metadata.json", metadata_bytes)
    write_exact(archives / "libretexts-toc.json", toc_bytes)

    page_rows: list[dict] = []
    asset_urls: set[str] = set()
    for row in toc_rows:
        ordinal = int(row["ordinal"])
        page_id = row["page_id"]
        body, final_url, content_type = fetch(row["url"], MAX_PAGE_BYTES)
        if "text/html" not in content_type.lower():
            raise RuntimeError(f"non-HTML page {page_id}: {content_type}")
        if final_url.rstrip("/") != row["url"].rstrip("/"):
            raise RuntimeError(f"page redirect for {page_id}: {final_url}")
        fragment, parsed, page_assets = parse_page(body, page_id, row["url"])
        name = f"{ordinal:03d}_{page_id}.html"
        write_exact(raw_root / name, body)
        write_exact(fragment_root / name, fragment)
        page_rows.append(
            {
                **row,
                **parsed,
                "raw_path": f"authority/extracted/libretexts-html-raw/{name}",
                "raw_bytes": len(body),
                "raw_sha256": sha256(body),
                "fragment_path": f"authority/extracted/libretexts-html-fragments/{name}",
                "fragment_bytes": len(fragment),
                "fragment_sha256": sha256(fragment),
                "asset_refs": len(page_assets),
            }
        )
        asset_urls.update(page_assets)
        time.sleep(0.08)

    asset_rows: list[dict] = []
    total_asset_bytes = 0
    for ordinal, url in enumerate(sorted(asset_urls), 1):
        body, final_url, content_type = fetch(url, MAX_ASSET_BYTES)
        total_asset_bytes += len(body)
        if total_asset_bytes > MAX_TOTAL_ASSET_BYTES:
            raise RuntimeError("asset closure exceeds total-byte bound")
        name = safe_asset_name(url)
        write_exact(asset_root / name, body)
        asset_rows.append(
            {
                "ordinal": ordinal,
                "url": url,
                "final_url": final_url,
                "content_type": content_type,
                "path": f"authority/extracted/libretexts-assets/{name}",
                "bytes": len(body),
                "sha256": sha256(body),
            }
        )
        time.sleep(0.08)

    page_fields = [
        "ordinal", "depth", "parent_id", "page_id", "title", "url", "revision",
        "published", "modified", "license", "raw_path", "raw_bytes", "raw_sha256",
        "fragment_path", "fragment_bytes", "fragment_sha256", "asset_refs",
    ]
    asset_fields = ["ordinal", "url", "final_url", "content_type", "path", "bytes", "sha256"]
    write_exact(lane / "qa" / "LIBRETEXTS_PAGE_MANIFEST.csv", canonical_csv(page_fields, page_rows))
    write_exact(lane / "qa" / "LIBRETEXTS_ASSET_MANIFEST.csv", canonical_csv(asset_fields, asset_rows))

    snapshot = {
        "schema": "o005-authority-snapshot-v1",
        "book_id": BOOK_ID,
        "metadata_url": METADATA_URL,
        "metadata_final_url": metadata_final,
        "metadata_content_type": metadata_type,
        "metadata_bytes": len(metadata_bytes),
        "metadata_sha256": sha256(metadata_bytes),
        "toc_url": TOC_URL,
        "toc_final_url": toc_final,
        "toc_content_type": toc_type,
        "toc_bytes": len(toc_bytes),
        "toc_sha256": sha256(toc_bytes),
        "page_count": len(page_rows),
        "raw_page_bytes": sum(int(row["raw_bytes"]) for row in page_rows),
        "fragment_bytes": sum(int(row["fragment_bytes"]) for row in page_rows),
        "asset_count": len(asset_rows),
        "asset_bytes": total_asset_bytes,
        "license_code": EXPECTED_LICENSE,
        "license_version": EXPECTED_LICENSE_VERSION,
        "license_url": CC_BY_NC_SA_30,
        "lxml_version": etree.LXML_VERSION,
    }
    write_exact(
        lane / "qa" / "LIBRETEXTS_AUTHORITY_SNAPSHOT.json",
        (json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )


def verify(lane: Path) -> None:
    roots = [
        lane / "authority" / "archives",
        lane / "authority" / "extracted" / "libretexts-html-raw",
        lane / "authority" / "extracted" / "libretexts-html-fragments",
        lane / "authority" / "extracted" / "libretexts-assets",
    ]
    for root in roots:
        if not root.is_dir():
            raise RuntimeError(f"missing frozen root: {root}")
    pages = list(csv.DictReader((lane / "qa" / "LIBRETEXTS_PAGE_MANIFEST.csv").open(encoding="utf-8", newline="")))
    assets = list(csv.DictReader((lane / "qa" / "LIBRETEXTS_ASSET_MANIFEST.csv").open(encoding="utf-8", newline="")))
    if not pages or not assets:
        raise RuntimeError("empty source manifest")
    for row in pages + assets:
        path_key = "raw_path" if "raw_path" in row else "path"
        bytes_key = "raw_bytes" if "raw_bytes" in row else "bytes"
        hash_key = "raw_sha256" if "raw_sha256" in row else "sha256"
        path = lane / row[path_key]
        data = path.read_bytes()
        if len(data) != int(row[bytes_key]) or sha256(data) != row[hash_key]:
            raise RuntimeError(f"manifest mismatch: {path}")
        if "fragment_path" in row:
            fragment = (lane / row["fragment_path"]).read_bytes()
            if len(fragment) != int(row["fragment_bytes"]) or sha256(fragment) != row["fragment_sha256"]:
                raise RuntimeError(f"fragment mismatch: {row['fragment_path']}")
    print(
        json.dumps(
            {
                "status": "PASS",
                "pages": len(pages),
                "assets": len(assets),
                "raw_page_bytes": sum(int(row["raw_bytes"]) for row in pages),
                "fragment_bytes": sum(int(row["fragment_bytes"]) for row in pages),
                "asset_bytes": sum(int(row["bytes"]) for row in assets),
            },
            sort_keys=True,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    lane = args.lane.resolve()
    if args.write:
        freeze(lane)
    verify(lane)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
