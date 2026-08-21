#!/usr/bin/env python3
"""Build the deterministic id-ID reader and modular backend for Lega Chapter 1."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag


ROOT = Path(__file__).resolve().parents[1]
UNIT_ID = "O005-LEGA-V101-CH01"
SOURCE_URL = "https://opentextbooks.library.arizona.edu/mathematicalmodeling/chapter/chapter-1/"
SOURCE_FRAGMENT = ROOT / "authority" / "units" / UNIT_ID / "content.raw.en.html"
TARGET_FRAGMENT = ROOT / "source" / "id-ID" / UNIT_ID / "content.html"
TARGET_SVG = ROOT / "source" / "id-ID" / UNIT_ID / "assets" / "modeling-cycle-id.svg"
NOTEBOOK = ROOT / "source" / "id-ID" / UNIT_ID / "notebooks" / "problem-07-open-curve-fitting.ipynb"
NOTEBOOK_LOCK = ROOT / "source" / "id-ID" / UNIT_ID / "notebooks" / "requirements.lock"
MASTERY = ROOT / "backend" / "mastery" / f"{UNIT_ID}.mastery.json"
SEGMENTS = ROOT / "backend" / "segments" / f"{UNIT_ID}.segments.jsonl"
UNIT_RECORD = ROOT / "backend" / "units" / f"{UNIT_ID}.json"
CSS = ROOT / "source" / "reader" / "reader.css"
DEFAULT_OUTPUT = ROOT / "build" / "reader" / UNIT_ID

LATEX_RE = re.compile(r"\$latex\s+(.+?)\$", re.DOTALL)
CAPTION_RE = re.compile(r"\[caption\s+([^\]]*)\](.*?)\[/caption\]", re.DOTALL)
BLOCK_LINE_RE = re.compile(
    r"^</?(?:address|article|aside|blockquote|details|div|dl|fieldset|figcaption|figure|"
    r"footer|form|h[1-6]|header|hr|li|main|nav|ol|p|pre|section|table|ul)\b",
    re.IGNORECASE,
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_text(value: str) -> str:
    return " ".join(value.replace("\u00a0", " ").split())


def pandoc_version() -> str:
    proc = subprocess.run(
        ["pandoc", "--version"], check=True, capture_output=True, text=True, encoding="utf-8"
    )
    return proc.stdout.splitlines()[0].strip()


def render_math(tex: str) -> str:
    proc = subprocess.run(
        ["pandoc", "--from=markdown+tex_math_dollars", "--to=html5", "--mathml"],
        input=f"${tex}$",
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    soup = BeautifulSoup(proc.stdout, "html.parser")
    math_node = soup.find("math")
    if math_node is None:
        raise RuntimeError(f"Pandoc did not produce MathML for: {tex!r}")
    span = soup.new_tag("span")
    span["class"] = "math inline"
    span["data-tex"] = tex
    math_node["aria-label"] = f"Rumus matematika: {tex}"
    span.append(math_node.extract())
    return str(span)


def replace_pressbooks_markup(fragment: str) -> str:
    matches = list(CAPTION_RE.finditer(fragment))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one Pressbooks caption shortcode, found {len(matches)}")

    def caption(match: re.Match[str]) -> str:
        attributes, inner = match.groups()
        ident = re.search(r'id="([^"]+)"', attributes)
        image = re.search(r"<img\b[^>]*?/?>", inner, re.DOTALL)
        if image is None:
            raise RuntimeError("Caption shortcode has no image")
        caption_html = inner[image.end():].strip()
        caption_html = re.sub(r"\[\s*(<a\b.*?</a>)\s*\]\s*$", r"\1", caption_html, flags=re.DOTALL)
        figure_id = html.escape(ident.group(1) if ident else "figure-1-1", quote=True)
        return (
            f'<figure id="{figure_id}" class="reader-figure">{image.group(0)}'
            f'<figcaption>{caption_html}</figcaption></figure>'
        )

    fragment = CAPTION_RE.sub(caption, fragment)
    fragment = LATEX_RE.sub(lambda m: render_math(m.group(1).strip()), fragment)
    return fragment.replace("&nbsp;", " ")


def wrap_inline_runs(fragment: str) -> BeautifulSoup:
    """Promote each Pressbooks raw prose line to a paragraph.

    The frozen raw field keeps every prose paragraph on one physical line and
    separates paragraphs with blank lines.  Treating the whole fragment as a
    generic HTML tree would merge adjacent raw paragraphs because they lack
    explicit ``p`` wrappers.  This line-aware promotion retains those authored
    paragraph boundaries while leaving every existing block element intact.
    """
    normalized: list[str] = []
    for line in fragment.splitlines():
        stripped = line.strip()
        if not stripped or stripped in {"&nbsp;", "&#160;"}:
            continue
        if BLOCK_LINE_RE.match(stripped):
            normalized.append(stripped)
        else:
            normalized.append(f"<p>{stripped}</p>")
    return BeautifulSoup("\n".join(normalized), "html.parser")


def harden_links(soup: BeautifulSoup) -> None:
    for anchor in soup.find_all("a", href=True):
        href = str(anchor["href"])
        if href.startswith(("http://", "https://")):
            anchor["rel"] = "external noopener noreferrer"


def render_value(soup: BeautifulSoup, value: object) -> Tag:
    if isinstance(value, dict):
        dl = soup.new_tag("dl")
        dl["class"] = "record-fields"
        for key, child in value.items():
            if key == "type":
                continue
            dt = soup.new_tag("dt")
            dt.string = {
                "final_answer": "Pemeriksaan akhir",
                "required_evidence": "Bukti yang diperlukan",
                "quick_check": "Cek cepat",
                "tolerances": "Toleransi",
                "dimensions": "Dimensi penilaian",
                "model_response_outline": "Garis besar jawaban",
                "exemplar_questions": "Contoh pertanyaan",
                "steps": "Langkah penyelesaian",
                "assumption": "Asumsi",
                "conclusion": "Simpulan",
                "plot_check": "Pemeriksaan grafik",
                "notebook_check": "Pemeriksaan notebook",
            }.get(key, key.replace("_", " ").capitalize())
            dd = soup.new_tag("dd")
            dd.append(render_value(soup, child))
            dl.extend([dt, dd])
        return dl
    if isinstance(value, list):
        listing = soup.new_tag("ol" if all(isinstance(item, str) for item in value) else "ul")
        for child in value:
            li = soup.new_tag("li")
            li.append(render_value(soup, child))
            listing.append(li)
        return listing
    paragraph = soup.new_tag("p")
    paragraph.string = str(value)
    return paragraph


def mastery_section(mastery: dict) -> str:
    soup = BeautifulSoup("", "html.parser")
    section = soup.new_tag("section", id="dukungan-belajar")
    section["aria-labelledby"] = "dukungan-title"
    title = soup.new_tag("h2", id="dukungan-title")
    title.string = "Petunjuk, pemeriksaan, dan pembahasan"
    section.append(title)
    intro = soup.new_tag("p")
    intro.string = (
        "Bagian tambahan ini ditulis untuk edisi Bahasa Indonesia. Bukalah seperlunya setelah "
        "Anda berusaha menyelesaikan soal secara mandiri."
    )
    section.append(intro)
    for problem in mastery["problems"]:
        pid = problem["problem_id"]
        article = soup.new_tag("article", id=f"{pid}-DUKUNGAN")
        article["class"] = "mastery-record"
        heading = soup.new_tag("h3")
        link = soup.new_tag("a", href=f"#{pid}")
        link.string = f"Dukungan untuk Soal {problem['ordinal']}"
        heading.append(link)
        article.append(heading)
        for label, value in (
            ("Petunjuk", problem["hint"]),
            ("Periksa jawaban", problem["check"]),
            ("Pembahasan atau rubrik", problem["solution_or_rubric"]),
        ):
            details = soup.new_tag("details")
            summary = soup.new_tag("summary")
            summary.string = label
            details.append(summary)
            details.append(render_value(soup, value))
            article.append(details)
        if problem["ordinal"] == 7:
            p = soup.new_tag("p")
            a = soup.new_tag("a", href="downloads/problem-07-open-curve-fitting.ipynb", download=True)
            a.string = "Unduh notebook Python terbuka untuk Soal 7"
            p.append(a)
            article.append(p)
        section.append(article)
    return str(section)


def text_slots(fragment: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(fragment, "html.parser")
    slots: list[tuple[str, str]] = []
    counters: dict[str, int] = {}

    def walk(node: Tag, path: str) -> None:
        local_counts: dict[str, int] = {}
        for child in node.children:
            if isinstance(child, NavigableString):
                value = canonical_text(str(child))
                if value:
                    counters[path] = counters.get(path, 0) + 1
                    slots.append((f"{path}/text()[{counters[path]}]", value))
            elif isinstance(child, Tag):
                local_counts[child.name] = local_counts.get(child.name, 0) + 1
                walk(child, f"{path}/{child.name}[{local_counts[child.name]}]")

    root = soup.new_tag("root")
    for child in list(soup.contents):
        root.append(child.extract())
    walk(root, "/fragment")
    return slots


def write_backend(source: str, target: str, mastery: dict, pandoc: str) -> tuple[int, str]:
    source_slots = text_slots(source)
    target_slots = text_slots(target)
    if [path for path, _ in source_slots] != [path for path, _ in target_slots]:
        raise RuntimeError("Source and target text-slot topology differs")
    SEGMENTS.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    for ordinal, ((path, source_text), (_, target_text)) in enumerate(zip(source_slots, target_slots), 1):
        record = {
            "schema": "o005-segment-v1",
            "segment_id": f"{UNIT_ID}-S{ordinal:04d}",
            "unit_id": UNIT_ID,
            "ordinal": ordinal,
            "html_path": path,
            "source_language": "en",
            "target_language": "id-ID",
            "source_text": source_text,
            "target_text": target_text,
            "source_sha256": hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
            "target_sha256": hashlib.sha256(target_text.encode("utf-8")).hexdigest(),
            "status": "translated",
        }
        lines.append(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    payload = ("\n".join(lines) + "\n").encode("utf-8")
    SEGMENTS.write_bytes(payload)
    segment_sha = hashlib.sha256(payload).hexdigest()
    unit = {
        "schema": "o005-unit-v1",
        "unit_id": UNIT_ID,
        "course_id": "C120",
        "resource_id": "O005",
        "language": "id-ID",
        "source_language": "en",
        "source": {
            "work": "Introduction to Mathematical Modeling",
            "author": "Joceline Lega",
            "edition": "v1.01 (Maret 2026)",
            "chapter": "On the Nature of Mathematical Modeling",
            "url": SOURCE_URL,
            "license": "CC BY-NC-SA 4.0",
            "content_sha256": digest(SOURCE_FRAGMENT),
        },
        "target": {
            "title": "Tentang Hakikat Pemodelan Matematika",
            "content_path": TARGET_FRAGMENT.relative_to(ROOT).as_posix(),
            "content_sha256": digest(TARGET_FRAGMENT),
            "figure_path": TARGET_SVG.relative_to(ROOT).as_posix(),
            "figure_sha256": digest(TARGET_SVG),
        },
        "segments": {
            "count": len(lines),
            "path": SEGMENTS.relative_to(ROOT).as_posix(),
            "sha256": segment_sha,
        },
        "problems": [problem["problem_id"] for problem in mastery["problems"]],
        "mastery_path": MASTERY.relative_to(ROOT).as_posix(),
        "mastery_sha256": digest(MASTERY),
        "notebook_path": NOTEBOOK.relative_to(ROOT).as_posix(),
        "notebook_sha256": digest(NOTEBOOK),
        "build": {"script": Path(__file__).relative_to(ROOT).as_posix(), "pandoc": pandoc},
    }
    UNIT_RECORD.parent.mkdir(parents=True, exist_ok=True)
    UNIT_RECORD.write_text(json.dumps(unit, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return len(lines), segment_sha


def build_reader(output: Path) -> dict:
    required = [SOURCE_FRAGMENT, TARGET_FRAGMENT, TARGET_SVG, NOTEBOOK, NOTEBOOK_LOCK, MASTERY, CSS]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing inputs: " + ", ".join(missing))
    source = SOURCE_FRAGMENT.read_text(encoding="utf-8")
    target = TARGET_FRAGMENT.read_text(encoding="utf-8")
    mastery = json.loads(MASTERY.read_text(encoding="utf-8"))
    if [p["problem_id"] for p in mastery["problems"]] != [f"{UNIT_ID}-P{i:02d}" for i in range(1, 8)]:
        raise RuntimeError("Mastery problem IDs are not the exact ordered P01-P07 set")
    pandoc = pandoc_version()
    if pandoc != "pandoc 3.9.0.2":
        raise RuntimeError(f"Expected pandoc 3.9.0.2, found {pandoc}")
    segment_count, segment_sha = write_backend(source, target, mastery, pandoc)

    body = wrap_inline_runs(replace_pressbooks_markup(target))
    harden_links(body)
    notebook_sha = digest(NOTEBOOK)
    page = f'''<!doctype html>
<html lang="id-ID">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Bab 1 edisi Bahasa Indonesia Introduction to Mathematical Modeling karya Joceline Lega.">
  <title>Tentang Hakikat Pemodelan Matematika — Joceline Lega</title>
  <link rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
  <link rel="stylesheet" href="assets/reader.css">
</head>
<body>
  <a class="skip-link" href="#isi">Lewati ke isi utama</a>
  <header class="reader-header">
    <p class="eyebrow">O005 · C120 · Bab 1</p>
    <h1>Tentang Hakikat Pemodelan Matematika</h1>
    <p class="byline">Joceline Lega · Edisi Bahasa Indonesia</p>
  </header>
  <nav class="unit-nav" aria-label="Navigasi unit">
    <a href="#isi">Isi bab</a>
    <a href="#dukungan-belajar">Dukungan belajar</a>
    <a href="downloads/problem-07-open-curve-fitting.ipynb">Notebook Python</a>
  </nav>
  <main id="isi" tabindex="-1">
    <aside class="edition-notice" aria-labelledby="edition-notice-title">
      <h2 id="edition-notice-title">Tentang edisi ini</h2>
      <p>Terjemahan Bahasa Indonesia independen dari <cite>Introduction to Mathematical Modeling</cite>, v1.01 (Maret 2026), oleh Joceline Lega, University of Arizona. <a href="{SOURCE_URL}" rel="external noopener noreferrer">Baca sumber resmi bab ini</a>.</p>
      <p>Sumber dan terjemahan dilisensikan dengan <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" rel="license external noopener noreferrer">CC BY-NC-SA 4.0</a>. Perubahan mencakup penerjemahan, gambar ulang aksesibel, pengindeksan modular, dan pendamping Python terbuka. Edisi ini tidak disokong atau disahkan oleh penulis maupun University of Arizona.</p>
    </aside>
    <article class="chapter" aria-label="Bab 1">
{str(body)}
    </article>
    {mastery_section(mastery)}
  </main>
  <footer>
    <p>Unit <code>{UNIT_ID}</code> · {segment_count} segmen berpasangan · notebook SHA-256 <code>{notebook_sha}</code>.</p>
  </footer>
</body>
</html>
'''

    if output.exists():
        shutil.rmtree(output)
    (output / "assets").mkdir(parents=True)
    (output / "downloads").mkdir()
    (output / "data").mkdir()
    (output / "index.html").write_text(page, encoding="utf-8", newline="\n")
    shutil.copyfile(CSS, output / "assets" / "reader.css")
    shutil.copyfile(TARGET_SVG, output / "assets" / "modeling-cycle-id.svg")
    shutil.copyfile(NOTEBOOK, output / "downloads" / NOTEBOOK.name)
    shutil.copyfile(NOTEBOOK_LOCK, output / "downloads" / NOTEBOOK_LOCK.name)
    shutil.copyfile(MASTERY, output / "data" / MASTERY.name)
    shutil.copyfile(SEGMENTS, output / "data" / SEGMENTS.name)
    shutil.copyfile(UNIT_RECORD, output / "data" / UNIT_RECORD.name)

    files = sorted((path for path in output.rglob("*") if path.is_file()), key=lambda p: p.relative_to(output).as_posix())
    rows = ["path\tbytes\tsha256"]
    total = 0
    for path in files:
        rel = path.relative_to(output).as_posix()
        total += path.stat().st_size
        rows.append(f"{rel}\t{path.stat().st_size}\t{digest(path)}")
    manifest = "\n".join(rows) + "\n"
    (output / "PACKAGE_MANIFEST.tsv").write_text(manifest, encoding="utf-8", newline="\n")
    return {
        "schema": "o005-reader-build-v1",
        "unit_id": UNIT_ID,
        "files_excluding_manifest": len(files),
        "bytes_excluding_manifest": total,
        "segment_count": segment_count,
        "segment_manifest_sha256": segment_sha,
        "pandoc": pandoc,
        "package_manifest_sha256": digest(output / "PACKAGE_MANIFEST.tsv"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = build_reader(args.output.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
