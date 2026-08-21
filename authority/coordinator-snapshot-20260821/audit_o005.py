from __future__ import annotations

import csv
import hashlib
import json
import mimetypes
import re
import sys
import time
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup


ROOT = "https://opentextbooks.library.arizona.edu/mathematicalmodeling/"
API = urljoin(ROOT, "wp-json/pressbooks/v2/")
OUT = Path(__file__).resolve().parent / "snapshot"
EPUB = Path(__file__).resolve().parent / "Lega_Introduction_to_Mathematical_Modeling_v1.01.epub"
UA = "Mozilla/5.0 (compatible; curriculum-source-audit/1.0)"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Referer": ROOT})


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj: object) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def get(url: str) -> requests.Response:
    last = None
    for attempt in range(4):
        try:
            response = SESSION.get(url, timeout=90)
            response.raise_for_status()
            return response
        except Exception as exc:  # pragma: no cover - bounded network retry
            last = exc
            if attempt != 3:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"GET failed after retries: {url}: {last}")


def clean_url(url: str, base: str = ROOT) -> str:
    absolute = urljoin(base, url.strip())
    parts = urlsplit(absolute)
    # Fragments never change the downloaded byte object. Queries are preserved,
    # because Pressbooks may use them to identify a distinct rendition.
    return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))


def semantic_projection(record: dict) -> dict:
    keep = (
        "id",
        "date",
        "date_gmt",
        "guid",
        "modified",
        "modified_gmt",
        "slug",
        "status",
        "type",
        "link",
        "title",
        "content",
        "author",
        "menu_order",
        "template",
        "meta",
        "front-matter-type",
        "chapter-type",
        "back-matter-type",
        "contributor",
        "license",
        "part",
    )
    return {key: record[key] for key in keep if key in record}


def toc_records(toc: dict) -> list[tuple[str, dict]]:
    result: list[tuple[str, dict]] = []
    result.extend(("front-matter", item) for item in toc.get("front-matter", []))
    for part in toc.get("parts", []):
        result.append(("parts", part))
        result.extend(("chapters", item) for item in part.get("chapters", []))
    result.extend(("back-matter", item) for item in toc.get("back-matter", []))
    return result


def html_assets_and_audit(records: list[dict], metadata: dict):
    assets: set[str] = set()
    external_embeds: set[str] = set()
    upload_links: set[str] = set()
    all_links: set[str] = set()
    figures: list[dict] = []
    headings: list[dict] = []
    textboxes: list[dict] = []
    keyword_hits: list[dict] = []
    problems: list[dict] = []
    projects: list[dict] = []
    tag_counts: Counter[str] = Counter()
    keyword_pattern = re.compile(
        r"\b(MATLAB|PPLANE|Excel|Python|SciPy|SymPy|Jupyter|Mathematica|"
        r"Maple|GeoGebra|Wolfram|RStudio|GNU Octave|Octave|Desmos|"
        r"Phase Plane App|The_Wave\.m|Patterns GUI|Diffusion GUI)\b",
        re.I,
    )
    rights_pattern = re.compile(
        r"\b(credit|courtesy|copyright|license|licensed|permission|adapted|"
        r"modified from|reproduced|source:|photo by|image by|figure by|"
        r"wikimedia|unsplash|pixabay|flickr)\b",
        re.I,
    )

    if metadata.get("image"):
        assets.add(clean_url(metadata["image"]))

    for record in records:
        content = record.get("content") or {}
        raw = content.get("raw") or ""
        soup = BeautifulSoup(raw, "html.parser")
        unit = f"{record.get('type')}:{record.get('id')}:{record.get('slug')}"
        for tag in soup.find_all(True):
            tag_counts[tag.name] += 1
            for attr in ("src", "poster", "data-src", "data-lazy-src"):
                value = tag.get(attr)
                if value:
                    u = clean_url(value, record.get("link") or ROOT)
                    if "/app/uploads/" in u:
                        assets.add(u)
                    elif tag.name in {"iframe", "embed", "object", "audio", "video", "source"}:
                        external_embeds.add(u)
            for attr in ("srcset", "data-srcset"):
                value = tag.get(attr)
                if value:
                    for candidate in value.split(","):
                        candidate_url = candidate.strip().split()[0]
                        u = clean_url(candidate_url, record.get("link") or ROOT)
                        if "/app/uploads/" in u:
                            assets.add(u)
            if tag.name == "a" and tag.get("href"):
                u = clean_url(tag["href"], record.get("link") or ROOT)
                all_links.add(u)
                if "/app/uploads/" in u:
                    assets.add(u)
                    upload_links.add(u)

        for figure in soup.find_all(["figure", "img"]):
            if figure.name == "img" and figure.find_parent("figure") is not None:
                continue
            image = figure if figure.name == "img" else figure.find("img")
            caption = ""
            if figure.name == "figure":
                cap = figure.find("figcaption")
                if cap:
                    caption = " ".join(cap.get_text(" ", strip=True).split())
            figures.append(
                {
                    "unit": unit,
                    "src": clean_url(image.get("src"), record.get("link") or ROOT)
                    if image and image.get("src")
                    else "",
                    "alt": image.get("alt", "") if image else "",
                    "title": image.get("title", "") if image else "",
                    "caption": caption,
                    "rights_signal": bool(rights_pattern.search(caption)),
                }
            )

        for heading in soup.find_all(re.compile(r"^h[1-6]$")):
            text = " ".join(heading.get_text(" ", strip=True).split())
            headings.append(
                {
                    "unit": unit,
                    "level": heading.name,
                    "id": heading.get("id", ""),
                    "classes": " ".join(heading.get("class", [])),
                    "text": text,
                }
            )

        for heading in soup.find_all("h3"):
            title_text = " ".join(heading.get_text(" ", strip=True).split())
            problem_match = re.fullmatch(r"Problem\s+(\d+)", title_text, re.I)
            if not problem_match or heading.find_parent("div", class_="textbox--exercises") is None:
                continue
            nodes = []
            for sibling in heading.next_siblings:
                if getattr(sibling, "name", None) == "h3" and re.fullmatch(
                    r"Problem\s+\d+",
                    " ".join(sibling.get_text(" ", strip=True).split()),
                    re.I,
                ):
                    break
                nodes.append(sibling)
            problem_text = " ".join(
                " ".join(
                    (node.get_text(" ", strip=True) if hasattr(node, "get_text") else str(node)).split()
                )
                for node in nodes
            ).strip()
            problem_links = sorted(
                {
                    clean_url(anchor["href"], record.get("link") or ROOT)
                    for node in nodes
                    for anchor in (node.find_all("a", href=True) if hasattr(node, "find_all") else [])
                }
            )
            problems.append(
                {
                    "unit": unit,
                    "number": int(problem_match.group(1)),
                    "word_count": len(re.findall(r"\b\w+\b", problem_text)),
                    "software": sorted(
                        {match.group(0).lower() for match in keyword_pattern.finditer(problem_text)}
                    ),
                    "links": problem_links,
                    "text": problem_text,
                }
            )

        if record.get("id") == 555:
            for heading in soup.find_all("h2"):
                title_text = " ".join(heading.get_text(" ", strip=True).split())
                project_match = re.fullmatch(r"(\d+)\.\s+(.+)", title_text)
                if not project_match:
                    continue
                nodes = []
                for sibling in heading.next_siblings:
                    if getattr(sibling, "name", None) == "h2":
                        break
                    nodes.append(sibling)
                project_text = " ".join(
                    " ".join(
                        (node.get_text(" ", strip=True) if hasattr(node, "get_text") else str(node)).split()
                    )
                    for node in nodes
                ).strip()
                project_links = sorted(
                    {
                        clean_url(anchor["href"], record.get("link") or ROOT)
                        for node in nodes
                        for anchor in (node.find_all("a", href=True) if hasattr(node, "find_all") else [])
                    }
                )
                projects.append(
                    {
                        "unit": unit,
                        "number": int(project_match.group(1)),
                        "title": project_match.group(2),
                        "word_count": len(re.findall(r"\b\w+\b", project_text)),
                        "software": sorted(
                            {match.group(0).lower() for match in keyword_pattern.finditer(project_text)}
                        ),
                        "links": project_links,
                        "text": project_text,
                    }
                )

        for box in soup.select("div.textbox"):
            box_title_node = box.select_one(".textbox__title") or box.find(re.compile(r"^h[1-6]$"))
            box_title = (
                " ".join(box_title_node.get_text(" ", strip=True).split())
                if box_title_node
                else ""
            )
            textboxes.append(
                {
                    "unit": unit,
                    "classes": " ".join(box.get("class", [])),
                    "title": box_title,
                    "text_prefix": " ".join(box.get_text(" ", strip=True).split())[:300],
                }
            )

        plain = " ".join(soup.get_text(" ", strip=True).split())
        for match in keyword_pattern.finditer(plain):
            start = max(0, match.start() - 100)
            end = min(len(plain), match.end() + 160)
            keyword_hits.append(
                {
                    "unit": unit,
                    "keyword": match.group(0),
                    "context": plain[start:end],
                }
            )

    return {
        "assets": sorted(assets),
        "external_embeds": sorted(external_embeds),
        "upload_links": sorted(upload_links),
        "all_links": sorted(all_links),
        "figures": figures,
        "headings": headings,
        "textboxes": textboxes,
        "keyword_hits": keyword_hits,
        "problems": problems,
        "projects": projects,
        "tag_counts": dict(sorted(tag_counts.items())),
    }


def fetch_assets(urls: list[str]) -> list[dict]:
    rows: list[dict] = []
    for index, url in enumerate(urls, start=1):
        try:
            response = get(url)
            data = response.content
            row = {
                "url": url,
                "final_url": response.url,
                "status": response.status_code,
                "content_type": response.headers.get("Content-Type", ""),
                "last_modified": response.headers.get("Last-Modified", ""),
                "etag": response.headers.get("ETag", ""),
                "bytes": len(data),
                "sha256": sha256(data),
            }
        except Exception as exc:
            row = {
                "url": url,
                "final_url": "",
                "status": "ERROR",
                "content_type": "",
                "last_modified": "",
                "etag": "",
                "bytes": 0,
                "sha256": "",
                "error": str(exc),
            }
        rows.append(row)
        print(f"asset {index}/{len(urls)} {row['status']} {url}", file=sys.stderr)
    return rows


def epub_audit(path: Path) -> dict:
    rows: list[dict] = []
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        for info in sorted(zf.infolist(), key=lambda item: item.filename):
            data = zf.read(info.filename)
            rows.append(
                {
                    "path": info.filename,
                    "bytes": len(data),
                    "compressed_bytes": info.compress_size,
                    "crc32": f"{info.CRC:08x}",
                    "sha256": sha256(data),
                }
            )
    lines = [
        f"{r['path']}\t{r['bytes']}\t{r['compressed_bytes']}\t{r['crc32']}\t{r['sha256']}"
        for r in rows
    ]
    manifest = ("\n".join(lines) + "\n").encode("utf-8")
    return {
        "zip_test": "PASS" if bad is None else f"FAIL:{bad}",
        "file_bytes": path.stat().st_size,
        "file_sha256": sha256(path.read_bytes()),
        "entry_count": len(rows),
        "entry_bytes": sum(r["bytes"] for r in rows),
        "manifest_sha256": sha256(manifest),
        "extension_counts": dict(
            sorted(Counter((Path(r["path"]).suffix.lower() or "[none]") for r in rows).items())
        ),
        "entries": rows,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    acquired = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    metadata = get(urljoin(API, "metadata")).json()
    toc = get(urljoin(API, "toc")).json()

    record_rows: list[dict] = []
    records: list[dict] = []
    for kind, toc_record in toc_records(toc):
        record_id = toc_record["id"]
        endpoint = urljoin(API, f"{kind}/{record_id}")
        record = get(endpoint).json()
        projected = semantic_projection(record)
        body = canonical_json(projected)
        records.append(projected)
        record_rows.append(
            {
                "kind": kind,
                "id": record_id,
                "slug": record.get("slug", ""),
                "title": (record.get("title") or {}).get("rendered", ""),
                "modified_gmt": record.get("modified_gmt", ""),
                "canonical_bytes": len(body),
                "sha256": sha256(body),
                "endpoint": endpoint,
            }
        )

    metadata_bytes = canonical_json(metadata)
    # Pressbooks emits a fresh anti-CSRF clone_token on every TOC request. It is
    # not book content and would make a content manifest deliberately unstable.
    toc_semantic = {key: value for key, value in toc.items() if key != "clone_token"}
    toc_bytes = canonical_json(toc_semantic)
    closure_lines = [
        f"metadata\t0\tmetadata\t\t{len(metadata_bytes)}\t{sha256(metadata_bytes)}\t{urljoin(API, 'metadata')}",
        f"toc\t0\ttoc\t\t{len(toc_bytes)}\t{sha256(toc_bytes)}\t{urljoin(API, 'toc')}",
    ]
    closure_lines.extend(
        f"{r['kind']}\t{r['id']}\t{r['slug']}\t{r['modified_gmt']}\t{r['canonical_bytes']}\t{r['sha256']}\t{r['endpoint']}"
        for r in record_rows
    )
    closure_manifest = ("\n".join(closure_lines) + "\n").encode("utf-8")

    html_audit = html_assets_and_audit(records, metadata)
    asset_rows = fetch_assets(html_audit["assets"])
    asset_lines = [
        f"{r['url']}\t{r['final_url']}\t{r['status']}\t{r['content_type']}\t{r['last_modified']}\t{r['etag']}\t{r['bytes']}\t{r['sha256']}"
        for r in asset_rows
    ]
    asset_manifest = ("\n".join(asset_lines) + "\n").encode("utf-8")

    epub = epub_audit(EPUB)
    summary = {
        "acquired_utc": acquired,
        "authority_root": ROOT,
        "api_root": API,
        "semantic_closure": {
            "record_count": len(record_rows),
            "front_matter": sum(r["kind"] == "front-matter" for r in record_rows),
            "parts": sum(r["kind"] == "parts" for r in record_rows),
            "chapters": sum(r["kind"] == "chapters" for r in record_rows),
            "back_matter": sum(r["kind"] == "back-matter" for r in record_rows),
            "manifest_bytes": len(closure_manifest),
            "manifest_sha256": sha256(closure_manifest),
            "canonical_record_bytes": sum(r["canonical_bytes"] for r in record_rows)
            + len(metadata_bytes)
            + len(toc_bytes),
        },
        "asset_closure": {
            "asset_count": len(asset_rows),
            "successful": sum(r["status"] == 200 for r in asset_rows),
            "bytes": sum(r["bytes"] for r in asset_rows),
            "manifest_bytes": len(asset_manifest),
            "manifest_sha256": sha256(asset_manifest),
            "content_types": dict(
                sorted(Counter(r["content_type"] for r in asset_rows).items())
            ),
        },
        "html_audit": {
            key: value
            for key, value in html_audit.items()
            if key
            not in {
                "assets",
                "headings",
                "figures",
                "textboxes",
                "keyword_hits",
                "problems",
                "projects",
            }
        },
        "epub": {key: value for key, value in epub.items() if key != "entries"},
    }

    (OUT / "metadata.canonical.json").write_bytes(metadata_bytes + b"\n")
    (OUT / "toc.canonical.json").write_bytes(toc_bytes + b"\n")
    (OUT / "records.canonical.json").write_bytes(canonical_json(records) + b"\n")
    (OUT / "semantic_closure_manifest.tsv").write_bytes(closure_manifest)
    (OUT / "asset_manifest.tsv").write_bytes(asset_manifest)
    (OUT / "record_manifest.json").write_text(
        json.dumps(record_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "headings.json").write_text(
        json.dumps(html_audit["headings"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT / "textboxes.json").write_text(
        json.dumps(html_audit["textboxes"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT / "figures.json").write_text(
        json.dumps(html_audit["figures"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT / "keyword_hits.json").write_text(
        json.dumps(html_audit["keyword_hits"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT / "problems.json").write_text(
        json.dumps(html_audit["problems"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT / "projects.json").write_text(
        json.dumps(html_audit["projects"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT / "epub_entry_manifest.json").write_text(
        json.dumps(epub, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
