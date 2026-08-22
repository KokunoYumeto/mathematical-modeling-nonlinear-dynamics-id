#!/usr/bin/env python3
"""Build the reader-first Indonesian CH14 progress PDF.

The source of truth is the already validated per-unit HTML reader closure.  The
builder joins only the human-facing chapter/part and mastery-support surfaces,
rewrites local figure paths into one temporary print tree, prints with Chromium,
then adds stable metadata, outlines, and folios with pypdf/reportlab.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import io
import json
import os
import shutil
import subprocess
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup, Tag
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, ByteStringObject
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


LANE_ROOT = Path(__file__).resolve().parents[1]
READER_ROOT = LANE_ROOT / "build" / "reader"
TMP_ROOT = LANE_ROOT / "tmp" / "pdfs"
OUTPUT_ROOT = LANE_ROOT / "output" / "pdf"
FINAL_PDF = OUTPUT_ROOT / (
    "01_Pengantar_Pemodelan_Matematika_"
    "Edisi_Bahasa_Indonesia_CH14.pdf"
)

UNITS = [
    ("O005-LEGA-V101-CH01", "Bab 1"),
    ("O005-LEGA-V101-CH02", "Bab 2"),
    ("O005-LEGA-V101-PT02", "Bagian 2"),
    ("O005-LEGA-V101-CH03", "Bab 3"),
    ("O005-LEGA-V101-CH04", "Bab 4"),
    ("O005-LEGA-V101-PT03", "Bagian 3"),
    ("O005-LEGA-V101-CH05", "Bab 5"),
    ("O005-LEGA-V101-CH06", "Bab 6"),
    ("O005-LEGA-V101-CH07", "Bab 7"),
    ("O005-LEGA-V101-PT04", "Bagian 4"),
    ("O005-LEGA-V101-CH08", "Bab 8"),
    ("O005-LEGA-V101-CH09", "Bab 9"),
    ("O005-LEGA-V101-CH10", "Bab 10"),
    ("O005-LEGA-V101-PT05", "Bagian 5"),
    ("O005-LEGA-V101-CH11", "Bab 11"),
    ("O005-LEGA-V101-CH12", "Bab 12"),
    ("O005-LEGA-V101-CH13", "Bab 13"),
    ("O005-LEGA-V101-CH14", "Bab 14"),
]

EDGE_CANDIDATES = [
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]

FIXED_PDF_DATE = "D:20260822000000+02'00'"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_browser() -> Path:
    for candidate in EDGE_CANDIDATES:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("No supported Edge/Chrome executable found")


def safe_clean_tmp() -> None:
    resolved = TMP_ROOT.resolve()
    expected_parent = (LANE_ROOT / "tmp").resolve()
    if resolved.parent != expected_parent or resolved.name != "pdfs":
        raise RuntimeError(f"Refusing to clean unexpected path: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True, exist_ok=True)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def unit_title(soup: BeautifulSoup) -> str:
    heading = soup.select_one("header.reader-header h1")
    if heading is None:
        raise ValueError("Reader has no header title")
    return heading.get_text(" ", strip=True)


def prefix_fragment_ids(container: Tag, prefix: str) -> None:
    mapping: dict[str, str] = {}
    for element in container.select("[id]"):
        old = element.get("id")
        if old:
            new = f"{prefix}-{old}"
            mapping[old] = new
            element["id"] = new
    for link in container.select('a[href^="#"]'):
        target = unquote(link.get("href", "")[1:])
        if target in mapping:
            link["href"] = f"#{mapping[target]}"
    for element in container.select("[aria-labelledby], [aria-describedby]"):
        for attribute in ("aria-labelledby", "aria-describedby"):
            value = element.get(attribute)
            if value:
                element[attribute] = " ".join(
                    mapping.get(token, token) for token in value.split()
                )
    for element in container.select("label[for]"):
        target = element.get("for")
        if target in mapping:
            element["for"] = mapping[target]


def rewrite_assets(container: Tag, unit_id: str, source_dir: Path) -> None:
    asset_out = TMP_ROOT / "assets" / unit_id
    for element in container.select("img[src], source[src], source[srcset]"):
        for attribute in ("src", "srcset"):
            value = element.get(attribute)
            if not value:
                continue
            first = value.split(",", 1)[0].strip().split(" ", 1)[0]
            parsed = urlparse(first)
            if parsed.scheme or first.startswith("//"):
                continue
            source = (source_dir / unquote(parsed.path)).resolve()
            if not source.is_file() or source_dir.resolve() not in source.parents:
                raise FileNotFoundError(
                    f"Missing or unsafe local asset for {unit_id}: {value}"
                )
            asset_out.mkdir(parents=True, exist_ok=True)
            destination = asset_out / source.name
            shutil.copy2(source, destination)
            relative = destination.relative_to(TMP_ROOT).as_posix()
            element[attribute] = relative


def normalize_reader_content(container: Tag, unit_id: str) -> None:
    prefix_fragment_ids(container, unit_id)
    for details in container.select("details"):
        details["open"] = ""
    for link in container.select("a[href]"):
        href = link.get("href", "")
        parsed = urlparse(href)
        if href.startswith("#") or parsed.scheme in {"http", "https", "mailto"}:
            continue
        link["href"] = "#sumber-digital"
        link.attrs.pop("download", None)
        link["class"] = list(link.get("class", [])) + ["digital-resource-link"]
    for math_span in container.select(".math[data-tex]"):
        tex = math_span.get("data-tex", "")
        if len(tex) >= 150:
            math_span["class"] = list(math_span.get("class", [])) + ["math--very-long"]
        elif len(tex) >= 95:
            math_span["class"] = list(math_span.get("class", [])) + ["math--long"]
    for element in container.select("script, iframe, audio, video"):
        element.decompose()


def extract_units() -> list[dict[str, object]]:
    extracted: list[dict[str, object]] = []
    for unit_id, label in UNITS:
        source_dir = READER_ROOT / unit_id
        index_path = source_dir / "index.html"
        if not index_path.is_file():
            raise FileNotFoundError(index_path)
        soup = BeautifulSoup(index_path.read_text(encoding="utf-8"), "lxml")
        main = soup.find("main")
        if main is None:
            raise ValueError(f"Reader has no main element: {index_path}")
        title = unit_title(soup)
        selected: list[Tag] = []
        article = main.find("article", class_="chapter", recursive=False)
        if article is None:
            raise ValueError(f"Reader has no direct chapter article: {index_path}")
        selected.append(article.extract())
        for section in main.find_all("section", recursive=False):
            selected.append(section.extract())
        wrapper = soup.new_tag("div")
        for node in selected:
            wrapper.append(node)
        normalize_reader_content(wrapper, unit_id)
        rewrite_assets(wrapper, unit_id, source_dir)
        extracted.append(
            {
                "unit_id": unit_id,
                "label": label,
                "title": title,
                "is_part": "-PT" in unit_id,
                "html": str(wrapper),
            }
        )
    return extracted


PRINT_CSS = r"""
@page { size: A4; margin: 18mm 18mm 22mm 18mm; }
@page:first { margin: 0; }
:root {
  --ink: #18232a;
  --muted: #53616a;
  --accent: #145e75;
  --accent-dark: #0b3f51;
  --soft: #eaf3f5;
  --line: #aebdc4;
  font-family: Georgia, "Noto Serif", "Times New Roman", serif;
}
* { box-sizing: border-box; }
html { background: #fff; }
body { margin: 0; color: var(--ink); background: #fff; font-size: 10.15pt; line-height: 1.46; }
a { color: #075e83; text-decoration-thickness: .05em; text-underline-offset: .12em; }
p, li, dd { widows: 3; orphans: 3; }
h1, h2, h3, h4, summary, figcaption, table { break-after: avoid; }
h2, h3, h4 { font-family: Arial, "Noto Sans", sans-serif; line-height: 1.22; color: var(--accent-dark); }
h2 { margin: 1.5em 0 .55em; font-size: 16pt; }
h3 { margin: 1.25em 0 .45em; font-size: 12.3pt; }
h4 { margin: 1em 0 .35em; font-size: 10.7pt; }
.cover {
  height: 297mm; margin: -18mm; padding: 30mm 25mm 24mm;
  color: white; background: linear-gradient(145deg, #0b3f51 0%, #145e75 62%, #73a8b6 100%);
  display: flex; flex-direction: column; justify-content: space-between;
}
.cover .kicker { font: 700 10pt/1.3 Arial, sans-serif; letter-spacing: .13em; text-transform: uppercase; }
.cover h1 { margin: 0; max-width: 17ch; font: 700 34pt/1.06 Georgia, serif; }
.cover .subtitle { max-width: 36ch; margin-top: 9mm; font: 16pt/1.35 Arial, sans-serif; }
.cover .credit { max-width: 46ch; font: 11pt/1.55 Arial, sans-serif; }
.frontmatter { break-before: page; }
.frontmatter h1 { margin: 0 0 1em; font: 700 25pt/1.1 Georgia, serif; color: var(--accent-dark); }
.status-box, .license-box, .digital-box { margin: 1.4em 0; padding: 1em 1.15em; border-left: 4px solid var(--accent); background: var(--soft); }
.status-box h2, .license-box h2, .digital-box h2 { margin-top: 0; font-size: 13pt; }
.toc { columns: 2; column-gap: 12mm; padding: 0; list-style: none; }
.toc li { break-inside: avoid; margin: 0 0 .65em; }
.toc .label { display: block; color: var(--muted); font: 700 8.4pt/1.2 Arial, sans-serif; letter-spacing: .04em; text-transform: uppercase; }
.unit { break-before: page; }
.unit-heading { margin: 0 0 10mm; padding-bottom: 5mm; border-bottom: 2px solid var(--accent); break-inside: avoid-page; break-after: avoid; }
.unit-heading .label { margin: 0 0 2mm; color: var(--accent); font: 700 9pt/1.2 Arial, sans-serif; letter-spacing: .08em; text-transform: uppercase; }
.unit-heading h1 { margin: 0; font: 700 24pt/1.1 Georgia, serif; color: var(--accent-dark); }
.unit-heading .unit-code { margin: 2.5mm 0 0; color: var(--muted); font: 7.2pt/1.2 Consolas, "Courier New", monospace; }
.unit--part .unit-heading { min-height: 95mm; display: flex; flex-direction: column; justify-content: flex-end; padding: 15mm; color: white; border: 0; background: linear-gradient(145deg, var(--accent-dark), var(--accent)); }
.unit--part .unit-heading .label, .unit--part .unit-heading h1, .unit--part .unit-heading .unit-code { color: white; }
.unit--part .chapter { font-size: 11pt; }
.chapter, #dukungan-belajar { width: 100%; }
.chapter > h2:first-child { margin-top: 0; }
.textbox { margin: 1.25em 0; border: .7pt solid var(--line); border-radius: 3px; }
.textbox__header { padding: .35em .8em; color: white; background: var(--accent-dark); }
.textbox__header h2, .textbox__header h3 { margin: .2em 0; color: white; font-size: 11.5pt; }
.textbox__content { padding: .15em .85em .65em; }
.reader-figure { margin: 1.35em 0; break-inside: avoid; }
.reader-figure img { display: block; width: auto; max-width: 100%; max-height: 175mm; margin: 0 auto; background: #fff; object-fit: contain; }
.reader-figure figcaption { margin-top: .45em; color: var(--muted); font: 8.6pt/1.35 Arial, sans-serif; }
.math { max-width: 100%; vertical-align: middle; white-space: nowrap; }
.math math { font-size: .94em; }
.math--long math { font-size: .79em; }
.math--very-long math { font-size: .66em; }
.mastery-record { margin: 1.1em 0; padding: .8em .9em; border: .7pt solid var(--line); border-radius: 3px; }
.mastery-record h3 { margin-top: 0; }
details { margin: .55em 0; padding: .5em .65em; background: #f4f8f9; }
details > * { display: block; }
summary { color: var(--accent-dark); font: 700 9.5pt/1.35 Arial, sans-serif; }
.record-fields { margin: .5em 0 0; }
.record-fields dt { margin-top: .55em; font-weight: 700; }
.record-fields dd { margin-left: 1em; }
table { width: 100%; border-collapse: collapse; font-size: 8.8pt; }
th, td { padding: .35em .45em; border: .6pt solid var(--line); vertical-align: top; }
pre, code { font-family: Consolas, "Courier New", monospace; font-size: .88em; overflow-wrap: anywhere; }
blockquote { margin: 1em 1.4em; color: #33434c; }
.digital-resource-link::after { content: " [paket sumber]"; color: var(--muted); font: 7.8pt Arial, sans-serif; }
.project-packets { break-before: page; }
.provenance-tail { break-before: page; }
.small { color: var(--muted); font-size: 8.8pt; }
"""


def build_html(units: list[dict[str, object]]) -> Path:
    toc_items = []
    unit_sections = []
    for unit in units:
        unit_id = str(unit["unit_id"])
        title = html.escape(str(unit["title"]))
        label = html.escape(str(unit["label"]))
        toc_items.append(
            f'<li><a href="#{unit_id}"><span class="label">{label}</span>{title}</a></li>'
        )
        class_name = "unit unit--part" if unit["is_part"] else "unit"
        unit_sections.append(
            f'<section class="{class_name}" id="{unit_id}">'
            f'<header class="unit-heading"><p class="label">{label}</p><h1>{title}</h1>'
            f'<p class="unit-code">{unit_id}</p></header>'
            f'{unit["html"]}</section>'
        )

    document = f"""<!doctype html>
<html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pengantar Pemodelan Matematika - Edisi Bahasa Indonesia</title>
<style>{PRINT_CSS}</style></head><body>
<section class="cover">
  <div><p class="kicker">Checkpoint pembaca terverifikasi - Bab 14</p>
  <h1>Pengantar Pemodelan Matematika</h1>
  <p class="subtitle">Edisi Bahasa Indonesia independen</p></div>
  <div class="credit"><p><strong>Joceline Lega</strong><br>
  University of Arizona Pressbooks v1.01 (Maret 2026)</p>
  <p>Terjemahan dan adaptasi Bahasa Indonesia, 22 Agustus 2026</p></div>
</section>

<section class="frontmatter" id="status-edisi"><h1>Status edisi</h1>
  <div class="status-box"><h2>Checkpoint parsial yang dapat dibaca</h2>
  <p>PDF ini memuat terjemahan lengkap Bab 1-14 dan pengantar Bagian 2-5,
  termasuk semua soal pada unit-unit tersebut, dukungan penguasaan, gambar
  yang diizinkan, dan uraian proyek. Prakata, pengantar Bagian 1, Pernyataan
  Aksesibilitas, Riwayat Versi, serta empat modul jembatan orisinal masih dalam
  pengerjaan. Karena itu, berkas ini bukan edisi final.</p></div>
  <div class="license-box"><h2>Lisensi, atribusi, dan perubahan</h2>
  <p>Karya sumber: Joceline Lega, <cite>Introduction to Mathematical
  Modeling</cite>, University of Arizona Pressbooks v1.01 (Maret 2026).
  Karya sumber, terjemahan, dan adaptasi ini dilisensikan dengan
  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons
  Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)</a>.</p>
  <p>Perubahan meliputi penerjemahan, pengindeksan modular, gambar ulang
  aksesibel, petunjuk/pemeriksaan/pembahasan baru, serta implementasi Python
  terbuka untuk latihan komputasi. Edisi independen ini tidak disokong atau
  disahkan oleh Joceline Lega maupun University of Arizona. Komponen pihak
  ketiga yang hanya ditautkan tidak disalin dan tetap berada di bawah ketentuan
  penerbit masing-masing.</p></div>
  <div class="digital-box" id="sumber-digital"><h2>Sumber digital pendamping</h2>
  <p>Notebook Python, data, paket proyek, backend ber-ID stabil, sumber HTML,
  manifest, dan checksum tersedia dalam arsip sumber ringkas yang diterbitkan
  bersama PDF ini. Penanda <em>[paket sumber]</em> menunjukkan sumber daya
  tersebut.</p></div>
  <p class="small">Sumber resmi:
  <a href="https://opentextbooks.library.arizona.edu/mathematicalmodeling/">opentextbooks.library.arizona.edu/mathematicalmodeling/</a>.</p>
</section>

<section class="frontmatter" id="daftar-isi"><h1>Daftar isi</h1>
<ol class="toc">{''.join(toc_items)}</ol></section>

{''.join(unit_sections)}

<section class="provenance-tail" id="catatan-akhir"><h1>Catatan edisi</h1>
<p>Checkpoint ini mempertahankan struktur, rumus, rujukan, soal, dan identitas
unit sumber yang telah selesai. Dukungan penguasaan dan komputasi Python
ditulis secara independen untuk edisi Bahasa Indonesia dan ditandai dalam
sumber pendamping. Untuk status terperinci dan identitas kriptografis, gunakan
manifest serta berkas checksum yang diterbitkan bersama PDF ini.</p>
</section></body></html>"""
    output = TMP_ROOT / "progress-reader.html"
    output.write_text(document, encoding="utf-8", newline="\n")
    return output


def print_html(html_path: Path, browser: Path) -> Path:
    raw_pdf = TMP_ROOT / "progress-reader.raw.pdf"
    profile = TMP_ROOT / "edge-profile"
    command = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-sync",
        "--no-first-run",
        "--no-default-browser-check",
        "--allow-file-access-from-files",
        "--export-tagged-pdf",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--user-data-dir={profile}",
        f"--print-to-pdf={raw_pdf}",
        html_path.resolve().as_uri(),
    ]
    completed = subprocess.run(
        command,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=240,
    )
    if completed.returncode != 0 or not raw_pdf.is_file():
        raise RuntimeError(
            f"Browser PDF render failed ({completed.returncode}):\n{completed.stdout[-4000:]}"
        )
    for _ in range(40):
        try:
            size_a = raw_pdf.stat().st_size
            time.sleep(0.1)
            size_b = raw_pdf.stat().st_size
            if size_a == size_b and size_a > 0:
                break
        except FileNotFoundError:
            time.sleep(0.1)
    return raw_pdf


def page_for_title(reader: PdfReader, title: str, start: int) -> int:
    # Chromium may split a heading into independently positioned text runs.
    # Compare Unicode-normalized alphanumeric content so visual line wrapping
    # does not prevent deterministic outline discovery.
    def key(value: str) -> str:
        normalized = unicodedata.normalize("NFKC", value).casefold()
        return "".join(character for character in normalized if character.isalnum())

    normalized = key(title)
    for page_index in range(start, len(reader.pages)):
        text_value = key(reader.pages[page_index].extract_text() or "")
        if normalized in text_value:
            return page_index
    raise ValueError(f"Could not find unit heading in rendered PDF: {title}")


def overlay_pdf(reader: PdfReader) -> PdfReader:
    footer_font_path = Path(r"C:\Windows\Fonts\arial.ttf")
    if not footer_font_path.is_file():
        raise FileNotFoundError(f"Footer font unavailable: {footer_font_path}")
    footer_font_name = "ArialEmbedded"
    if footer_font_name not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(footer_font_name, str(footer_font_path)))

    buffer = io.BytesIO()
    folio = canvas.Canvas(
        buffer,
        pageCompression=0,
        invariant=1,
        initialFontName=footer_font_name,
        initialFontSize=7.2,
    )
    for page_index, page in enumerate(reader.pages):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        folio.setPageSize((width, height))
        if page_index > 0:
            y = 30
            folio.setStrokeColorRGB(0.68, 0.74, 0.77)
            folio.setLineWidth(0.45)
            folio.line(51, y + 11, width - 51, y + 11)
            folio.setFillColorRGB(0.28, 0.34, 0.37)
            folio.setFont(footer_font_name, 7.2)
            folio.drawString(
                51,
                y,
                "Pengantar Pemodelan Matematika - Edisi Bahasa Indonesia",
            )
            folio.drawRightString(width - 51, y, str(page_index + 1))
        folio.showPage()
    folio.save()
    buffer.seek(0)
    return PdfReader(buffer)


def finalize_pdf(raw_pdf: Path, units: list[dict[str, object]]) -> dict[str, object]:
    reader = PdfReader(raw_pdf)
    # Locate structural headings before overlay merging mutates page content
    # streams and makes some extractors lose their text ordering.
    toc_page = page_for_title(reader, "Daftar isi", 1)
    search_from = toc_page + 1
    unit_pages: list[int] = []
    for unit in units:
        page_index = page_for_title(reader, str(unit["unit_id"]), search_from)
        unit_pages.append(page_index)
        search_from = page_index + 1

    overlay = overlay_pdf(reader)
    writer = PdfWriter(clone_from=reader)
    for page_index, page in enumerate(writer.pages):
        page.merge_page(overlay.pages[page_index], over=False)

    writer.add_metadata(
        {
            "/Title": "Pengantar Pemodelan Matematika - Edisi Bahasa Indonesia",
            "/Author": "Joceline Lega",
            "/Subject": "Checkpoint parsial terverifikasi sampai Bab 14",
            "/Keywords": (
                "pemodelan matematika, dinamika nonlinear, Bahasa Indonesia, "
                "CC BY-NC-SA 4.0"
            ),
            "/Creator": "Edisi Bahasa Indonesia independen",
            "/Producer": "Chromium, pypdf, dan ReportLab",
            "/CreationDate": FIXED_PDF_DATE,
            "/ModDate": FIXED_PDF_DATE,
        }
    )
    writer._ID = ArrayObject(
        [
            ByteStringObject(bytes.fromhex("b6f68302800882ca60a5553a7b82986a")),
            ByteStringObject(bytes.fromhex("b6f68302800882ca60a5553a7b82986a")),
        ]
    )

    writer.add_outline_item("Status edisi", 1)
    writer.add_outline_item("Daftar isi", toc_page)
    for unit, page_index in zip(units, unit_pages, strict=True):
        title = str(unit["title"])
        writer.add_outline_item(f'{unit["label"]}: {title}', page_index)

    pypdf_output = TMP_ROOT / "progress-reader.finalize-unoptimized.pdf"
    with pypdf_output.open("wb") as stream:
        writer.write(stream)

    mutool = shutil.which("mutool")
    if not mutool:
        raise FileNotFoundError("mutool is required to normalize the final PDF xref")
    completed = subprocess.run(
        [mutool, "clean", str(pypdf_output), str(FINAL_PDF)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=240,
    )
    if completed.returncode != 0 or not FINAL_PDF.is_file():
        raise RuntimeError(
            f"mutool PDF normalization failed ({completed.returncode}):\n"
            f"{completed.stdout[-4000:]}"
        )

    final_reader = PdfReader(FINAL_PDF, strict=True)
    if len(final_reader.pages) != len(reader.pages):
        raise RuntimeError("Final page count differs from raw render")
    if not final_reader.metadata or not final_reader.metadata.title:
        raise RuntimeError("Final PDF metadata missing")
    if final_reader.root_object.get("/Lang") != "id":
        raise RuntimeError("Final PDF language is not Indonesian")
    if not final_reader.root_object.get("/StructTreeRoot"):
        raise RuntimeError("Final PDF lost its tagged structure tree")
    return {
        "path": str(FINAL_PDF),
        "bytes": FINAL_PDF.stat().st_size,
        "sha256": sha256(FINAL_PDF),
        "pages": len(final_reader.pages),
        "outline_entries": 2 + len(units),
        "tagged": True,
        "language": "id",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep the temporary HTML/raw PDF tree for bounded QA",
    )
    args = parser.parse_args()
    safe_clean_tmp()
    units = extract_units()
    html_path = build_html(units)
    raw_pdf = print_html(html_path, find_browser())
    result = finalize_pdf(raw_pdf, units)
    result["source_units"] = [unit["unit_id"] for unit in units]
    result["html_sha256"] = sha256(html_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not args.keep_temp:
        safe_clean_tmp()
    return 0


if __name__ == "__main__":
    sys.exit(main())
