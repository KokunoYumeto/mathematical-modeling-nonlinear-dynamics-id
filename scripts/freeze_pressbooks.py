#!/usr/bin/env python3
"""Freeze the public Pressbooks authoring closure for Lega v1.01.

The Pressbooks REST API exposes the raw, editable HTML for every exported book
component.  This script records those exact JSON responses, extracts the raw HTML
without rewriting it, downloads all reader assets referenced by that source, and
emits canonical manifests.  It uses no authenticated endpoint and no Git data.
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

from lxml import html


SITE = "https://opentextbooks.library.arizona.edu/mathematicalmodeling"
API = f"{SITE}/wp-json/pressbooks/v2"
ENDPOINTS = {
    "metadata": f"{API}/metadata",
    "toc": f"{API}/toc",
    "theme": f"{API}/theme",
    "styles": f"{API}/styles",
    "front-matter": f"{API}/front-matter?per_page=100&context=view",
    "parts": f"{API}/parts?per_page=100&context=view",
    "chapters": f"{API}/chapters?per_page=100&context=view",
    "back-matter": f"{API}/back-matter?per_page=100&context=view",
}
USER_AGENT = "O005-C120-Pressbooks-freezer/1.0 (+noncommercial translation QA)"
EXPECTED_TITLE = "Introduction to Mathematical Modeling"
EXPECTED_AUTHOR = "Joceline Lega"
EXPECTED_LICENSE = "https://creativecommons.org/licenses/by-nc-sa/4.0/"
MAX_JSON_BYTES = 8_000_000
MAX_ASSET_BYTES = 80_000_000
MAX_TOTAL_ASSET_BYTES = 800_000_000


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str, limit: int) -> tuple[bytes, str, str]:
    request = Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"},
    )
    with urlopen(request, timeout=90) as response:
        final_url = response.geturl()
        content_type = response.headers.get("Content-Type", "")
        data = response.read(limit + 1)
    if len(data) > limit:
        raise RuntimeError(f"response exceeds {limit} bytes: {url}")
    return data, final_url, content_type


def canonical_csv(fieldnames: list[str], rows: list[dict]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-.")
    return value or "untitled"


def safe_asset_name(url: str) -> str:
    basename = unquote(Path(urlparse(url).path).name) or "asset"
    return f"{sha256(url.encode('utf-8'))[:16]}-{slugify(basename)}"


def write_exact(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def toc_sequence(toc: dict) -> list[dict]:
    rows: list[dict] = []

    def add(kind: str, item: dict, parent_id: str = "") -> None:
        post_id = item.get("id")
        if not isinstance(post_id, int) or post_id <= 0:
            raise RuntimeError(f"invalid TOC ID: {item!r}")
        rows.append(
            {
                "ordinal": len(rows) + 1,
                "kind": kind,
                "id": post_id,
                "parent_id": parent_id,
                "title": item.get("title", ""),
                "slug": item.get("slug", ""),
                "word_count": item.get("word_count", 0),
                "export": item.get("export"),
                "link": item.get("link", ""),
            }
        )

    for item in toc.get("front-matter", []):
        add("front-matter", item)
    for part in toc.get("parts", []):
        add("parts", part)
        for chapter in part.get("chapters", []):
            add("chapters", chapter, str(part["id"]))
    for item in toc.get("back-matter", []):
        add("back-matter", item)

    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate TOC post ID")
    if any(row["export"] is not True for row in rows):
        raise RuntimeError("TOC includes a non-exported component")
    return rows


def collect_assets(raw_html: str, base_url: str) -> set[str]:
    wrapped = f"<div>{raw_html}</div>"
    document = html.fromstring(wrapped)
    assets: set[str] = set()
    for element in document.xpath(".//*[@src or @poster or @data]"):
        for attribute in ("src", "poster", "data"):
            value = element.get(attribute)
            if value and not value.startswith(("data:", "javascript:", "#")):
                assets.add(urljoin(base_url, value))
    for value in document.xpath(".//*[@srcset]/@srcset"):
        for candidate in value.split(","):
            url = candidate.strip().split(" ", 1)[0]
            if url and not url.startswith("data:"):
                assets.add(urljoin(base_url, url))
    for value in document.xpath(".//a[@href]/@href"):
        resolved = urljoin(base_url, value)
        parsed = urlparse(resolved)
        if parsed.netloc == urlparse(SITE).netloc and "/app/uploads/" in parsed.path:
            assets.add(resolved)
    return assets


def freeze(lane: Path) -> None:
    archive_root = lane / "authority" / "archives"
    source_root = lane / "authority" / "extracted" / "lega-pressbooks-source"
    asset_root = lane / "authority" / "extracted" / "lega-pressbooks-assets"
    for root in (source_root, asset_root):
        if root.exists() and any(root.iterdir()):
            raise RuntimeError(f"refusing to overwrite nonempty frozen directory: {root}")
        root.mkdir(parents=True, exist_ok=True)

    payloads: dict[str, object] = {}
    endpoint_rows: list[dict] = []
    for name, url in ENDPOINTS.items():
        data, final_url, content_type = fetch(url, MAX_JSON_BYTES)
        if "application/json" not in content_type.lower():
            raise RuntimeError(f"non-JSON response for {name}: {content_type}")
        payloads[name] = json.loads(data)
        filename = f"lega-pressbooks-{name}.json"
        write_exact(archive_root / filename, data)
        endpoint_rows.append(
            {
                "name": name,
                "url": url,
                "final_url": final_url,
                "path": f"authority/archives/{filename}",
                "bytes": len(data),
                "sha256": sha256(data),
            }
        )

    metadata = payloads["metadata"]
    if not isinstance(metadata, dict):
        raise RuntimeError("metadata is not an object")
    authors = metadata.get("author") or []
    if metadata.get("name") != EXPECTED_TITLE or [author.get("name") for author in authors] != [EXPECTED_AUTHOR]:
        raise RuntimeError("unexpected Pressbooks title or author")
    if (metadata.get("license") or {}).get("url") != EXPECTED_LICENSE:
        raise RuntimeError("unexpected Pressbooks book license")

    toc = payloads["toc"]
    if not isinstance(toc, dict):
        raise RuntimeError("TOC is not an object")
    ordered = toc_sequence(toc)
    collections = {
        name: {int(item["id"]): item for item in payloads[name]}
        for name in ("front-matter", "parts", "chapters", "back-matter")
    }
    for name, collection in collections.items():
        if len(collection) != len(payloads[name]):
            raise RuntimeError(f"duplicate IDs in {name}")

    source_rows: list[dict] = []
    asset_urls = {metadata["image"]}
    for toc_row in ordered:
        item = collections[toc_row["kind"]].get(toc_row["id"])
        if item is None:
            raise RuntimeError(f"TOC component missing from API collection: {toc_row}")
        if item.get("status") != "publish" or item.get("link") != toc_row["link"]:
            raise RuntimeError(f"publication-state mismatch for post {toc_row['id']}")
        raw = (item.get("content") or {}).get("raw")
        if not isinstance(raw, str):
            raise RuntimeError(f"missing raw editable HTML for post {toc_row['id']}")
        raw_bytes = raw.encode("utf-8")
        name = (
            f"{int(toc_row['ordinal']):03d}_{toc_row['kind']}_{toc_row['id']}_"
            f"{slugify(str(toc_row['slug']))}.html"
        )
        write_exact(source_root / name, raw_bytes)
        asset_urls.update(collect_assets(raw, toc_row["link"]))
        source_rows.append(
            {
                **toc_row,
                "modified_gmt": item.get("modified_gmt", ""),
                "date_gmt": item.get("date_gmt", ""),
                "license_override": (item.get("meta") or {}).get("pb_section_license", ""),
                "source_path": f"authority/extracted/lega-pressbooks-source/{name}",
                "source_bytes": len(raw_bytes),
                "source_sha256": sha256(raw_bytes),
                "id_attributes": len(re.findall(r'\bid\s*=\s*["\'][^"\']+["\']', raw, re.I)),
                "image_elements": len(re.findall(r"<img\b", raw, re.I)),
                "asset_refs": len(collect_assets(raw, toc_row["link"])),
            }
        )

    collection_ids = set().union(*(set(collection) for collection in collections.values()))
    toc_ids = {int(row["id"]) for row in ordered}
    if collection_ids != toc_ids:
        raise RuntimeError(
            f"TOC/API collection mismatch: extra={sorted(collection_ids-toc_ids)}, missing={sorted(toc_ids-collection_ids)}"
        )

    asset_rows: list[dict] = []
    total_asset_bytes = 0
    for ordinal, url in enumerate(sorted(asset_urls), 1):
        data, final_url, content_type = fetch(url, MAX_ASSET_BYTES)
        total_asset_bytes += len(data)
        if total_asset_bytes > MAX_TOTAL_ASSET_BYTES:
            raise RuntimeError("asset closure exceeds total-byte bound")
        name = safe_asset_name(url)
        write_exact(asset_root / name, data)
        asset_rows.append(
            {
                "ordinal": ordinal,
                "url": url,
                "final_url": final_url,
                "content_type": content_type,
                "path": f"authority/extracted/lega-pressbooks-assets/{name}",
                "bytes": len(data),
                "sha256": sha256(data),
            }
        )
        time.sleep(0.05)

    endpoint_fields = ["name", "url", "final_url", "path", "bytes", "sha256"]
    source_fields = [
        "ordinal", "kind", "id", "parent_id", "title", "slug", "word_count", "export", "link",
        "modified_gmt", "date_gmt", "license_override", "source_path", "source_bytes", "source_sha256",
        "id_attributes", "image_elements", "asset_refs",
    ]
    asset_fields = ["ordinal", "url", "final_url", "content_type", "path", "bytes", "sha256"]
    write_exact(lane / "qa" / "LEGA_API_ENDPOINT_MANIFEST.csv", canonical_csv(endpoint_fields, endpoint_rows))
    write_exact(lane / "qa" / "LEGA_SOURCE_MANIFEST.csv", canonical_csv(source_fields, source_rows))
    write_exact(lane / "qa" / "LEGA_ASSET_MANIFEST.csv", canonical_csv(asset_fields, asset_rows))

    snapshot = {
        "schema": "o005-lega-authority-snapshot-v1",
        "site": SITE,
        "title": EXPECTED_TITLE,
        "author": EXPECTED_AUTHOR,
        "date_published": metadata.get("datePublished"),
        "license": EXPECTED_LICENSE,
        "source_components": len(source_rows),
        "source_words_from_toc": sum(int(row["word_count"]) for row in source_rows),
        "source_bytes": sum(int(row["source_bytes"]) for row in source_rows),
        "asset_count": len(asset_rows),
        "asset_bytes": total_asset_bytes,
        "theme_name": payloads["theme"].get("name"),
        "theme_version": payloads["theme"].get("version"),
        "pdf_engine": payloads["theme"].get("options", {}).get("pdf", {}).get("pdf_prince_version"),
    }
    write_exact(
        lane / "qa" / "LEGA_AUTHORITY_SNAPSHOT.json",
        (json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )


def verify(lane: Path) -> None:
    sources = list(csv.DictReader((lane / "qa" / "LEGA_SOURCE_MANIFEST.csv").open(encoding="utf-8", newline="")))
    assets = list(csv.DictReader((lane / "qa" / "LEGA_ASSET_MANIFEST.csv").open(encoding="utf-8", newline="")))
    endpoints = list(csv.DictReader((lane / "qa" / "LEGA_API_ENDPOINT_MANIFEST.csv").open(encoding="utf-8", newline="")))
    if not sources or not assets or len(endpoints) != len(ENDPOINTS):
        raise RuntimeError("incomplete frozen manifests")
    for row in sources:
        data = (lane / row["source_path"]).read_bytes()
        if len(data) != int(row["source_bytes"]) or sha256(data) != row["source_sha256"]:
            raise RuntimeError(f"source mismatch: {row['source_path']}")
    for row in assets + endpoints:
        data = (lane / row["path"]).read_bytes()
        if len(data) != int(row["bytes"]) or sha256(data) != row["sha256"]:
            raise RuntimeError(f"frozen artifact mismatch: {row['path']}")
    print(
        json.dumps(
            {
                "status": "PASS",
                "source_components": len(sources),
                "source_words": sum(int(row["word_count"]) for row in sources),
                "source_bytes": sum(int(row["source_bytes"]) for row in sources),
                "assets": len(assets),
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
