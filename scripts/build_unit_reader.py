#!/usr/bin/env python3
"""Build a deterministic id-ID reader and modular backend for an admitted unit."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "source" / "reader" / "reader.css"

UNIT_SPECS = {
    "O005-LEGA-V101-CH01": {
        "unit_type": "chapter",
        "unit_number": 1,
        "chapter_number": 1,
        "source_title": "On the Nature of Mathematical Modeling",
        "target_title": "Tentang Hakikat Pemodelan Matematika",
        "source_url": "https://opentextbooks.library.arizona.edu/mathematicalmodeling/chapter/chapter-1/",
        "target_asset": "assets/modeling-cycle-id.svg",
        "notebook": "notebooks/problem-07-open-curve-fitting.ipynb",
        "problem_count": 7,
        "plain_paragraphs": False,
        "change_note": "penerjemahan, gambar ulang aksesibel, pengindeksan modular, dan pendamping Python terbuka",
    },
    "O005-LEGA-V101-CH02": {
        "unit_type": "chapter",
        "unit_number": 2,
        "chapter_number": 2,
        "source_title": "First Steps: Modeling the Wave",
        "target_title": "Langkah Awal: Memodelkan Gelombang",
        "source_url": "https://opentextbooks.library.arizona.edu/mathematicalmodeling/chapter/first-steps-modeling-the-wave/",
        "target_asset": "assets/the-wave-source.png",
        "notebook": "notebooks/chapter-02-open-wave-simulation.ipynb",
        "problem_count": 7,
        "plain_paragraphs": False,
        "change_note": "penerjemahan, pengindeksan modular, dan implementasi ulang simulasi dengan Python terbuka",
    },
    "O005-LEGA-V101-PT02": {
        "unit_type": "part",
        "unit_number": 2,
        "source_title": "Models from Classical Mechanics",
        "target_title": "Model-Model dari Mekanika Klasik",
        "source_url": "https://opentextbooks.library.arizona.edu/mathematicalmodeling/part/part-2-models-from-classical-mechanics/",
        "target_asset": None,
        "notebook": None,
        "problem_count": 0,
        "plain_paragraphs": True,
        "change_note": "penerjemahan dan pengindeksan modular",
    },
}


def configure(unit_id: str) -> None:
    global UNIT_ID, UNIT_SPEC, SOURCE_URL, SOURCE_FRAGMENT, TARGET_FRAGMENT
    global TARGET_ASSET, NOTEBOOK, NOTEBOOK_LOCK, MASTERY, SEGMENTS, UNIT_RECORD
    global DEFAULT_OUTPUT, PROBLEM_COUNT
    UNIT_ID = unit_id
    UNIT_SPEC = UNIT_SPECS[unit_id]
    SOURCE_URL = UNIT_SPEC["source_url"]
    SOURCE_FRAGMENT = ROOT / "authority" / "units" / UNIT_ID / "content.raw.en.html"
    TARGET_FRAGMENT = ROOT / "source" / "id-ID" / UNIT_ID / "content.html"
    PROBLEM_COUNT = UNIT_SPEC["problem_count"]
    target_asset = UNIT_SPEC["target_asset"]
    notebook = UNIT_SPEC["notebook"]
    TARGET_ASSET = ROOT / "source" / "id-ID" / UNIT_ID / target_asset if target_asset else None
    NOTEBOOK = ROOT / "source" / "id-ID" / UNIT_ID / notebook if notebook else None
    NOTEBOOK_LOCK = NOTEBOOK.parent / "requirements.lock" if NOTEBOOK else None
    MASTERY = ROOT / "backend" / "mastery" / f"{UNIT_ID}.mastery.json" if PROBLEM_COUNT else None
    SEGMENTS = ROOT / "backend" / "segments" / f"{UNIT_ID}.segments.jsonl"
    UNIT_RECORD = ROOT / "backend" / "units" / f"{UNIT_ID}.json"
    DEFAULT_OUTPUT = ROOT / "build" / "reader" / UNIT_ID


configure("O005-LEGA-V101-CH01")

LATEX_RE = re.compile(r"\$latex\s+(.+?)\$", re.DOTALL)
COMPANION_MATH_RE = re.compile(r"\\\((.+?)\\\)|\\\[(.+?)\\\]", re.DOTALL)
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


@lru_cache(maxsize=None)
def render_math(tex: str) -> str:
    source_tex = tex
    tex = html.unescape(tex)
    # Pandoc does not convert the two legacy Pressbooks array idioms used in
    # Chapter 2.  Normalize them losslessly for MathML, while retaining the
    # exact frozen/source TeX in data-tex and the aligned backend.
    tex = tex.replace(r"\left\{ \begin{array}{ll}", r"\begin{cases}")
    tex = tex.replace(r"\end{array} \right.", r"\end{cases}")
    tex = tex.replace(r"\begin{array}{c}", r"\substack{")
    tex = tex.replace(r"\end{array}", "}")
    tex = tex.replace(r"\hbox{if }", r"\text{jika }")
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
    span["data-tex"] = source_tex
    math_node["aria-label"] = f"Rumus matematika: {tex}"
    span.append(math_node.extract())
    return str(span)


def replace_pressbooks_markup(fragment: str) -> str:
    matches = list(CAPTION_RE.finditer(fragment))
    expected = 1 if TARGET_ASSET else 0
    if len(matches) != expected:
        raise RuntimeError(f"Expected {expected} Pressbooks caption shortcode(s), found {len(matches)}")

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


def append_companion_text(soup: BeautifulSoup, parent: Tag, value: str) -> None:
    cursor = 0
    for match in COMPANION_MATH_RE.finditer(value):
        if match.start() > cursor:
            parent.append(NavigableString(value[cursor:match.start()]))
        tex = (match.group(1) or match.group(2)).strip()
        rendered = BeautifulSoup(render_math(tex), "html.parser")
        for child in list(rendered.contents):
            parent.append(child.extract())
        cursor = match.end()
    if cursor < len(value):
        parent.append(NavigableString(value[cursor:]))


def render_value(soup: BeautifulSoup, value: object, field: str | None = None) -> Tag:
    if isinstance(value, dict):
        visible_keys = set(value) - {"type"}
        if visible_keys == {"text"}:
            return render_value(soup, value["text"], field="text")
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
                "criterion": "Kriteria",
                "full_credit": "Jawaban lengkap",
                "partial_credit": "Jawaban sebagian",
                "explanation": "Penjelasan",
                "formula": "Rumus",
                "comparison_baseline": "Dasar perbandingan",
                "relationship": "Hubungan",
                "runtime": "Lingkungan eksekusi",
                "open_stack": "Perangkat lunak terbuka",
                "slope_absolute": "Toleransi mutlak kemiringan",
                "intercept_absolute": "Toleransi mutlak intersep",
                "sse_absolute": "Toleransi mutlak SSE",
                "path": "Lokasi berkas",
            }.get(key, key.replace("_", " ").capitalize())
            dd = soup.new_tag("dd")
            dd.append(render_value(soup, child, field=key))
            dl.extend([dt, dd])
        return dl
    if isinstance(value, list):
        listing = soup.new_tag("ol" if all(isinstance(item, str) for item in value) else "ul")
        for child in value:
            li = soup.new_tag("li")
            li.append(render_value(soup, child, field=field))
            listing.append(li)
        return listing
    paragraph = soup.new_tag("p")
    if field == "formula":
        rendered = BeautifulSoup(render_math(str(value)), "html.parser")
        for child in list(rendered.contents):
            paragraph.append(child.extract())
    else:
        append_companion_text(soup, paragraph, str(value))
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
        notebook = problem.get("notebook")
        if notebook:
            p = soup.new_tag("p")
            notebook_name = Path(notebook["path"]).name
            a = soup.new_tag("a", href=f"downloads/{notebook_name}", download=True)
            a.string = f"Unduh notebook Python terbuka untuk Soal {problem['ordinal']}"
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


def unit_text_slots(fragment: str) -> list[tuple[str, str]]:
    if UNIT_SPEC["plain_paragraphs"]:
        paragraphs = [canonical_text(part) for part in re.split(r"\r?\n\s*\r?\n", fragment.strip())]
        return [(f"/fragment/p[{index}]/text()[1]", text) for index, text in enumerate(paragraphs, 1) if text]
    return text_slots(fragment)


def write_backend(source: str, target: str, mastery: dict | None, pandoc: str) -> tuple[int, str]:
    source_slots = unit_text_slots(source)
    target_slots = unit_text_slots(target)
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
    source_record = {
        "work": "Introduction to Mathematical Modeling",
        "author": "Joceline Lega",
        "edition": "v1.01 (Maret 2026)",
        UNIT_SPEC["unit_type"]: UNIT_SPEC["source_title"],
        "url": SOURCE_URL,
        "license": "CC BY-NC-SA 4.0",
        "content_sha256": digest(SOURCE_FRAGMENT),
    }
    target_record = {
        "title": UNIT_SPEC["target_title"],
        "content_path": TARGET_FRAGMENT.relative_to(ROOT).as_posix(),
        "content_sha256": digest(TARGET_FRAGMENT),
    }
    if TARGET_ASSET:
        target_record.update(
            {
                "figure_path": TARGET_ASSET.relative_to(ROOT).as_posix(),
                "figure_sha256": digest(TARGET_ASSET),
            }
        )
    unit = {
        "schema": "o005-unit-v1",
        "unit_id": UNIT_ID,
        "course_id": "C120",
        "resource_id": "O005",
        "language": "id-ID",
        "source_language": "en",
        "source": source_record,
        "target": target_record,
        "segments": {
            "count": len(lines),
            "path": SEGMENTS.relative_to(ROOT).as_posix(),
            "sha256": segment_sha,
        },
        "problems": [problem["problem_id"] for problem in mastery["problems"]] if mastery else [],
        "build": {"script": Path(__file__).relative_to(ROOT).as_posix(), "pandoc": pandoc},
    }
    if UNIT_SPEC["unit_type"] != "chapter":
        unit["unit_type"] = UNIT_SPEC["unit_type"]
    if mastery and MASTERY:
        unit.update(
            {
                "mastery_path": MASTERY.relative_to(ROOT).as_posix(),
                "mastery_sha256": digest(MASTERY),
            }
        )
    if NOTEBOOK:
        unit.update(
            {
                "notebook_path": NOTEBOOK.relative_to(ROOT).as_posix(),
                "notebook_sha256": digest(NOTEBOOK),
            }
        )
    UNIT_RECORD.parent.mkdir(parents=True, exist_ok=True)
    UNIT_RECORD.write_text(json.dumps(unit, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return len(lines), segment_sha


def build_reader(output: Path) -> dict:
    required = [SOURCE_FRAGMENT, TARGET_FRAGMENT, CSS]
    required.extend(path for path in (TARGET_ASSET, NOTEBOOK, NOTEBOOK_LOCK, MASTERY) if path is not None)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing inputs: " + ", ".join(missing))
    source = SOURCE_FRAGMENT.read_text(encoding="utf-8")
    target = TARGET_FRAGMENT.read_text(encoding="utf-8")
    mastery = json.loads(MASTERY.read_text(encoding="utf-8")) if MASTERY else None
    if mastery and [p["problem_id"] for p in mastery["problems"]] != [f"{UNIT_ID}-P{i:02d}" for i in range(1, PROBLEM_COUNT + 1)]:
        raise RuntimeError("Mastery problem IDs are not the exact ordered problem set")
    pandoc = pandoc_version()
    if pandoc != "pandoc 3.9.0.2":
        raise RuntimeError(f"Expected pandoc 3.9.0.2, found {pandoc}")
    segment_count, segment_sha = write_backend(source, target, mastery, pandoc)

    body = wrap_inline_runs(replace_pressbooks_markup(target))
    harden_links(body)
    unit_label = "Bab" if UNIT_SPEC["unit_type"] == "chapter" else "Bagian"
    source_unit_label = "bab" if UNIT_SPEC["unit_type"] == "chapter" else "bagian"
    unit_number = UNIT_SPEC["unit_number"]
    article_class = "chapter" if UNIT_SPEC["unit_type"] == "chapter" else "chapter part"
    nav_lines = ['    <a href="#isi">Isi bab</a>' if unit_label == "Bab" else '    <a href="#isi">Isi bagian</a>']
    if mastery:
        nav_lines.append('    <a href="#dukungan-belajar">Dukungan belajar</a>')
    if NOTEBOOK:
        nav_lines.append(f'    <a href="downloads/{NOTEBOOK.name}">Notebook Python</a>')
    navigation = "\n".join(nav_lines)
    mastery_html = mastery_section(mastery) if mastery else ""
    if NOTEBOOK:
        footer_detail = f" · notebook SHA-256 <code>{digest(NOTEBOOK)}</code>"
    else:
        footer_detail = ""
    page = f'''<!doctype html>
<html lang="id-ID">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{unit_label} {unit_number} edisi Bahasa Indonesia Introduction to Mathematical Modeling karya Joceline Lega.">
  <title>{UNIT_SPEC['target_title']} — Joceline Lega</title>
  <link rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
  <link rel="stylesheet" href="assets/reader.css">
</head>
<body>
  <a class="skip-link" href="#isi">Lewati ke isi utama</a>
  <header class="reader-header">
    <p class="eyebrow">O005 · C120 · {unit_label} {unit_number}</p>
    <h1>{UNIT_SPEC['target_title']}</h1>
    <p class="byline">Joceline Lega · Edisi Bahasa Indonesia</p>
  </header>
  <nav class="unit-nav" aria-label="Navigasi unit">
{navigation}
  </nav>
  <main id="isi" tabindex="-1">
    <aside class="edition-notice" aria-labelledby="edition-notice-title">
      <h2 id="edition-notice-title">Tentang edisi ini</h2>
      <p>Terjemahan Bahasa Indonesia independen dari <cite>Introduction to Mathematical Modeling</cite>, v1.01 (Maret 2026), oleh Joceline Lega, University of Arizona. <a href="{SOURCE_URL}" rel="external noopener noreferrer">Baca sumber resmi {source_unit_label} ini</a>.</p>
      <p>Sumber dan terjemahan dilisensikan dengan <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" rel="license external noopener noreferrer">CC BY-NC-SA 4.0</a>. Perubahan mencakup {UNIT_SPEC['change_note']}. Edisi ini tidak disokong atau disahkan oleh penulis maupun University of Arizona.</p>
    </aside>
    <article class="{article_class}" aria-label="{unit_label} {unit_number}">
{str(body)}
    </article>
    {mastery_html}
  </main>
  <footer>
    <p>Unit <code>{UNIT_ID}</code> · {segment_count} segmen berpasangan{footer_detail}.</p>
  </footer>
</body>
</html>
'''

    if output.exists():
        shutil.rmtree(output)
    (output / "assets").mkdir(parents=True)
    (output / "data").mkdir()
    (output / "index.html").write_text(page, encoding="utf-8", newline="\n")
    shutil.copyfile(CSS, output / "assets" / "reader.css")
    if TARGET_ASSET:
        shutil.copyfile(TARGET_ASSET, output / "assets" / TARGET_ASSET.name)
    if NOTEBOOK and NOTEBOOK_LOCK:
        (output / "downloads").mkdir()
        shutil.copyfile(NOTEBOOK, output / "downloads" / NOTEBOOK.name)
        shutil.copyfile(NOTEBOOK_LOCK, output / "downloads" / NOTEBOOK_LOCK.name)
    if MASTERY:
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
    parser.add_argument("--unit", choices=sorted(UNIT_SPECS), default="O005-LEGA-V101-CH01")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    configure(args.unit)
    output = args.output.resolve() if args.output else DEFAULT_OUTPUT
    result = build_reader(output)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
