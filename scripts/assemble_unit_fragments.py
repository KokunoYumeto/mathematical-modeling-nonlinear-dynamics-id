#!/usr/bin/env python3
"""Assemble reviewed contiguous translation fragments deterministically."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPECS = {
    "O005-LEGA-V101-CH03": {
        "source_lines": 410,
        "problem_count": 23,
        "fragments": [
            "01-main-through-nonlinear.html",
            "02-friction-summary-descriptions.html",
            "03-problems.html",
        ],
        "replacements": [
            (
                "merupakan simpul stabil (jika $latex \\alpha^2 \\gt 4)$ atau spiral stabil (jika $latex \\alpha^2 \\lt 4$).",
                "merupakan simpul stabil (jika $latex \\alpha^2 \\gt 4$), simpul stabil degenerat pada kasus kesamaan di batas 4, atau spiral stabil (jika $latex \\alpha^2 \\lt 4$).",
                1,
            ),
            (
                "simpul stabil degenerat pada kasus kesamaan di batas 4",
                "simpul stabil degenerat pada kasus kritis ketika kuadrat koefisien redaman sama dengan 4",
                1,
            ),
            (
                "manifold tak stabil dari $latex ((2 p + 1) \\pi,0)$ memuat titik-titik tetap stabil $latex (2 p \\pi,0)$ dan $latex ((2 p + 2) \\pi,0)$.",
                "cabang-cabang manifold tak stabil dari $latex ((2 p + 1) \\pi,0)$ mendekati titik-titik tetap stabil $latex (2 p \\pi,0)$ dan $latex ((2 p + 2) \\pi,0)$; kedua titik itu berada dalam penutupan manifold tersebut.",
                1,
            ),
            (
                "$latex A, B \\in \\mathbb{R}$",
                "$latex C, \\phi \\in \\mathbb{R}$",
                1,
            ),
            (
                "$latex (1,-\\sin(\\theta))$",
                "$latex (\\Lambda,-\\sin(\\theta))$",
                1,
            ),
            (
                "ruas kiri Persamaan (<a href=\"#sol_curv\">3.13</a>) bernilai real",
                "ruas kanan Persamaan (<a href=\"#sol_curv\">3.13</a>) bernilai real",
                1,
            ),
            (
                "merupakan titik ekstrem $latex V(x)$",
                "merupakan titik kritis $latex V(x)$",
                1,
            ),
            (
                "Dapat diperiksa bahwa titik minimum $latex V$ bersesuaian dengan <em>pusat</em> dan titik maksimum $latex V$ dengan <em>titik pelana</em> (lihat soal-soal).",
                "Jika titik-titik kritis tersebut nondegenerat, dapat diperiksa bahwa titik minimum $latex V$ bersesuaian dengan <em>pusat</em> dan titik maksimum $latex V$ dengan <em>titik pelana</em> (lihat soal-soal).",
                1,
            ),
            (
                "Lintasan-lintasan ini memiliki garis singgung vertikal pada titik potong tersebut (lihat soal-soal).",
                "Apabila turunan potensial tidak nol di titik potong tersebut, lintasan-lintasan ini memiliki garis singgung vertikal di sana (lihat soal-soal).",
                1,
            ),
            (
                "dapat diduga bahwa lintasan dengan $latex d \\theta / d \\tau \\ne 0$ akan konvergen menuju solusi berenergi $latex E = -1$.",
                "dapat diduga bahwa lintasan generik yang bukan kesetimbangan—sehingga $latex d \\theta / d \\tau \\ne 0$ setidaknya pada sebagian waktu—dan tidak terletak pada manifold stabil titik pelana akan konvergen menuju solusi berenergi $latex E = -1$.",
                1,
            ),
            (
                "sebanding dengan negatif dari kecepatan massa",
                "berlawanan arah dan sebanding dengan kecepatan massa",
                1,
            ),
            (
                "sistem dinamika dua dimensi nonkonservatif",
                "sistem dinamik dua dimensi nonkonservatif",
                1,
            ),
            (
                "disebut <em>Jacobian</em> sistem",
                "disebut <em>matriks Jacobi</em> sistem",
                1,
            ),
            (
                "dengan $latex C, \\phi \\in \\mathbb{R}$, jika $latex A$ dan $latex B$ dinyatakan",
                "dengan $latex A, B \\in \\mathbb{R}$, jika $latex A$ dan $latex B$ dinyatakan",
                1,
            ),
            (
                "$latex \\bar x \\in [x_0,x]$",
                "$latex \\bar x \\in [\\min(x_0,x),\\max(x_0,x)]$",
                1,
            ),
            (
                "Perhatikan persamaan diferensial berikut, $latex \\displaystyle \\frac{d x}{d t} = \\lambda x - \\gamma x^3.$",
                "Perhatikan persamaan diferensial berikut, $latex \\displaystyle \\frac{d x}{d t} = \\lambda x - \\gamma x^3.$ Untuk penskalaan real, perlakukan secara terpisah kasus ketika salah satu parameter nol; jika keduanya tidak nol, besar parameternya dapat diserap, tetapi tandanya tetap menentukan kelas dinamika.",
                1,
            ),
            (
                "untuk “menghilangkan” parameter $latex \\lambda$.",
                "untuk menghilangkan besar parameter $latex \\lambda$ ketika parameter itu tidak nol. Jelaskan pula apa yang terjadi ketika λ = 0 dan besaran diskret apa yang masih tersisa ketika λ ≠ 0.",
                1,
            ),
            (
                "Dapatkah Anda menemukan perubahan variabel yang juga memungkinkan Anda menghilangkan $latex \\gamma$?",
                "Jika γ ≠ 0, dapatkah Anda menemukan perubahan variabel yang juga menghilangkan besar $latex \\gamma$? Jelaskan peran tanda γ dan kasus γ = 0.",
                1,
            ),
            ("[\\hbox{force}]", "[\\hbox{gaya}]", 2),
            ("merujuk ke", "merujuk pada", 1),
            ("dikerahkan", "diberikan", 3),
            ("dalam vektor", "dalam basis vektor", 2),
            ("dalam sudut", "sebagai fungsi sudut", 1),
            ("persamaan(-persamaan)", "persamaan-persamaan", 1),
            ("bernilai real", "bernilai riil", 2),
            ("orde dua", "orde kedua", 5),
            ("keseimbangan", "kesetimbangan", 1),
            ("kerapatan gaya badan", "gaya badan per satuan volume", 1),
            (
                "menyatakan turunan pertama dan kedua vektor posisi $latex \\vec x$ dalam basis vektor $latex \\vec r$ dan $latex \\vec \\theta$, serta dalam turunan-turunan sudut $latex \\theta$",
                "menyatakan turunan pertama dan kedua vektor posisi $latex \\vec x$ dalam bentuk vektor $latex \\vec r$, $latex \\vec \\theta$, dan turunan sudut $latex \\theta$",
                1,
            ),
            ("uraikan ruas kanannya", "uraikan ruas-ruas kanannya", 1),
            ("sistem dinamis", "sistem dinamik", 3),
            ("sistem dinamika", "sistem dinamik", 1),
            ("orde satu", "orde pertama", 3),
            (
                "$latex \\displaystyle \\frac{d^2 x}{d t^2} + \\omega^2 x = \\epsilon \\frac{d x}{d t} (1 - x^2), \\qquad \\epsilon \\ge 0.$",
                "$latex \\displaystyle \\frac{d^2 x}{d t^2} + \\omega^2 x = \\epsilon \\frac{d x}{d t} (1 - x^2), \\qquad \\epsilon \\ge 0, \\qquad \\omega \\gt 0.$",
                1,
            ),
            (
                "$latex \\min(V) \\lt E \\lt \\max(V)$",
                "$latex \\inf V \\lt E \\lt \\sup V$",
                1,
            ),
            ("$latex \\min(V)$", "$latex \\inf V$", 1),
            ("$latex \\max(V)$", "$latex \\sup V$", 1),
            (
                "lintasan horizontal bergelombang di bagian atas dan bawah bingkai. [",
                "lintasan horizontal bergelombang di bagian atas dan bawah bingkai. Catatan: label vertikal pada gambar sumber menggunakan dθ/dt, sedangkan model tak berdimensi dalam teks menggunakan dθ/dτ. [",
                1,
            ),
            (
                '[caption id="attachment_33" align="alignleft" width="300"]',
                '[caption id="attachment_29" align="alignleft" width="300"]',
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Mech_pot1-1-300x218.png",
                "assets/potential-1-source.png",
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Mech_pot2-1-300x166.png",
                "assets/potential-2-source.png",
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Mech_pot3-1-300x271.png",
                "assets/potential-3-source.png",
                1,
            ),
            (
                "https://opentextbooks.library.arizona.edu/app/uploads/sites/217/2022/09/Mech_pot4-1-300x160.png",
                "assets/potential-4-source.png",
                1,
            ),
            (
                "assets/phase-portrait-construction-source.png",
                "assets/phase-portrait-construction-id-v3.png",
                1,
            ),
            (
                'alt="Shape of the potential V. Long description below."',
                'alt="Bentuk potensial V. Deskripsi panjang tersedia di bawah."',
                4,
            ),
            ("$x$", "$latex x$", 2),
        ],
    },
    "O005-LEGA-V101-CH04": {
        "source_lines": 185,
        "problem_count": 4,
        "fragments": [
            "01-model-and-equations.html",
            "02-analysis-summary-descriptions.html",
            "03-problems.html",
        ],
        "replacements": [
            (
                "Memberikan alasan bagi pendekatan-pendekatan yang digunakan untuk menyederhanakan persamaan gerak.",
                "Menjelaskan alasan penggunaan aproksimasi untuk menyederhanakan persamaan gerak.",
                1,
            ),
            (
                "batu tipis, pipih (planar), homogen, dan simetris",
                "batu tipis, pipih, homogen, dan simetris",
                1,
            ),
            (
                r"\frac{d \vec V}{d t}",
                r"\frac{\partial \vec V}{\partial t}",
                1,
            ),
            (
                r"\frac{d \omega_y}{d t}",
                r"\frac{d \omega_{-y}}{d t}",
                1,
            ),
            (
                r"\displaystyle I_t \frac{d \omega_p}{d t}",
                r"\displaystyle I_p \frac{d \omega_p}{d t}",
                1,
            ),
            (
                "Rotasi benda tegar batu terhadap pusat massanya diberikan oleh persamaan Euler,",
                "Gerak rotasi batu sebagai benda tegar terhadap pusat massanya diberikan oleh persamaan Euler,",
                1,
            ),
            (
                "Kerangka ortonormal $latex (-\\vec y, \\vec n, \\vec p)$ melekat pada pusat massa batu dan berotasi bersamanya.",
                "Kerangka ortonormal $latex (-\\vec y, \\vec n, \\vec p)$ melekat pada pusat massa batu dan berotasi bersamanya. Dalam penampang pada Gambar 4.1, arah $latex \\vec p$ berimpit dengan arah tangensial $latex \\vec t$.",
                1,
            ),
            (
                r"\begin{array} \displaystyle J_1",
                r"\begin{array}{ll} \displaystyle J_1",
                1,
            ),
            (
                r"$latex \theta(t) = \omega_{-y}(0)\, t.$",
                r"$latex \theta(t) = \theta(0) + \omega_{-y}(0)\, t.$",
                1,
            ),
            (
                r"$latex \theta(t) = \theta(0) + \frac{1}{\delta} \omega_{-y}(0) \sin(\delta t) - \frac{1}{\delta} \omega_p(0) \cos(\delta t)$",
                r"$latex \theta(t) = \theta(0) + \frac{\omega_{-y}(0)}{\delta} \sin(\delta t) + \frac{\omega_p(0)}{\delta} \left[1-\cos(\delta t)\right]$",
                1,
            ),
            (
                "rotasi terhadap sumbu $latex \\vec y$",
                "rotasi terhadap sumbu $latex -\\vec y$",
                1,
            ),
            (
                r"$latex \tau_f = \frac{2 v_z(0)}{g},$",
                r"$latex \tau_f = \frac{2 v_z(0)}{g}, \qquad v_z(0) \gt 0,$",
                1,
            ),
            (
                r"$latex {\mathcal U}(z) = \int_0^z F(s)\, ds,$",
                r"$latex {\mathcal U}(z) = \int_0^z {\mathcal F}(s)\, ds,$",
                1,
            ),
            (
                "Kehilangan energi bertanda $latex \\mathcal W$ sama dengan usaha yang dilakukan oleh gaya gesek air pada batu.",
                "Perubahan energi selama tumbukan, yang dinyatakan dengan $latex \\mathcal W$, sama dengan usaha yang dilakukan oleh gaya gesek air pada batu dan bernilai negatif untuk disipasi.",
                1,
            ),
            (r"$latex \theta = 20^o$", r"$latex \theta = 20^\circ$", 1),
            (r"$latex C_n$", r"$latex C_f$", 1),
            (
                "parameter sudut untuk kemiringan batu ($latex \\theta$), vektor kecepatan ($latex \\vec{v}$), dan sudut tumbukan ($latex \\beta$)",
                "sudut kemiringan batu ($latex \\theta$), vektor kecepatan batu ($latex \\vec{v}$), dan sudut datang ($latex \\beta$)",
                1,
            ),
            (
                "$latex \\alpha$ masing-masing bernilai $latex y,\\,n$, dan $latex p$.",
                "$latex \\alpha$ masing-masing bernilai $latex -y,\\,n$, dan $latex p$.",
                1,
            ),
            (
                "Perhatikan Persamaan (<a href=\"#Stone_New5\">4.11</a>) dan anggap bahwa batu berbentuk persegi.",
                "Perhatikan Persamaan (<a href=\"#Stone_New5\">4.11</a>) dan anggap bahwa batu berbentuk persegi. Ambil $latex t=0$ pada awal tumbukan, dengan kondisi awal $latex z(0)=0$ dan $latex \\dot z(0)=v_z(0)\\lt 0$. Rumus luas terendam pada soal ini berlaku selama perendaman parsial, yaitu $latex -a\\sin(\\theta)\\leq z\\leq 0$.",
                1,
            ),
            (
                "Dinamika sisi batu persegi yang terendam selama fase tumbukan dideskripsikan oleh (lihat Soal 2)",
                "Dinamika sisi batu persegi yang terendam selama fase tumbukan dideskripsikan oleh (lihat Soal 2). Untuk bagian-bagian berikut, abaikan ketebalan $latex h$, tetapkan $latex C \\equiv C_l\\cos(\\theta)-C_f\\sin(\\theta)\\gt 0$, gunakan $latex v_z(0)=-v_x(0)\\tan(\\beta)$, dan asumsikan ruas dalam tanda kurung siku pada hasil akhir positif. Dengan konvensi $latex z\\lt 0$ di bawah permukaan, batu mulai terendam seluruhnya ketika $latex |z|\\geq a\\sin(\\theta)$.",
                1,
            ),
            (
                r"$latex \displaystyle \frac{d^2 \theta}{d t^2} + \frac{J_0 - J_1}{J_1} (\theta - \theta(0)) = \frac{{\mathcal M}_\theta}{J_1},$",
                r"$latex \displaystyle \frac{d^2 \theta}{d t^2} + \nu^2 \left(\theta - \theta(0)\right) = \frac{{\mathcal M}_\theta}{J_1},$",
                1,
            ),
            (
                "dengan $latex {\\mathcal M}_\\theta$ sebagai proyeksi torsi yang dikerahkan air pada batu ke sumbu $latex \\vec y$.",
                "dengan $latex \\nu = ((J_0-J_1)/J_1)\\,\\Omega_0$, sedangkan $latex {\\mathcal M}_\\theta \\equiv N_{-y}$ adalah komponen torsi yang diberikan air pada batu dalam arah peningkatan sudut kemiringan (sumbu $latex -\\vec y$). Bentuk ini mempertahankan kuadrat frekuensi $latex \\nu^2$ pada Persamaan (20) artikel sumber.",
                1,
            ),
        ],
    },
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def assemble(unit_id: str, *, write: bool) -> dict[str, object]:
    spec = SPECS[unit_id]
    unit_root = ROOT / "source" / "id-ID" / unit_id
    fragment_root = unit_root / "fragments"
    paths = [fragment_root / name for name in spec["fragments"]]
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing translation fragments: " + ", ".join(missing))

    payloads: list[bytes] = []
    fragment_rows: list[dict[str, object]] = []
    for path in paths:
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            raise RuntimeError(f"UTF-8 BOM is not permitted: {path}")
        data.decode("utf-8")
        if not data.endswith(b"\n"):
            raise RuntimeError(f"Fragment lacks terminal LF: {path}")
        payloads.append(data)
        fragment_rows.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": len(data),
                "lines": len(data.splitlines()),
                "sha256": sha256(data),
            }
        )

    payload = b"".join(payloads)
    for old, new, expected_count in spec.get("replacements", []):
        old_bytes = old.encode("utf-8")
        if payload.count(old_bytes) != expected_count:
            raise RuntimeError(
                f"Expected {expected_count} declared correction surface(s): {old!r}"
            )
        payload = payload.replace(old_bytes, new.encode("utf-8"))
    text = payload.decode("utf-8")
    problem_heading = re.compile(
        r"<h3(?P<attrs>[^>]*)>(?P<body>(?:(?!</h3>).)*Soal (?P<number>\d+)(?:(?!</h3>).)*)</h3>"
    )
    matches = list(problem_heading.finditer(text))
    expected_numbers = list(range(1, spec.get("problem_count", 0) + 1))
    actual_numbers = [int(match.group("number")) for match in matches]
    if actual_numbers != expected_numbers:
        raise RuntimeError("Translated problem-heading sequence differs")

    def add_problem_id(match: re.Match[str]) -> str:
        number = int(match.group("number"))
        attrs = match.group("attrs")
        if re.search(r"\bid\s*=", attrs):
            raise RuntimeError("Translation fragment already has a problem-heading ID")
        return (
            f'<h3{attrs} id="{unit_id}-P{number:02d}">'
            f'{match.group("body")}</h3>'
        )

    payload = problem_heading.sub(add_problem_id, text).encode("utf-8")
    source = ROOT / "authority" / "units" / unit_id / "content.raw.en.html"
    if len(source.read_bytes().splitlines()) != spec["source_lines"]:
        raise RuntimeError("Frozen source line census differs")
    if len(payload.splitlines()) != spec["source_lines"]:
        raise RuntimeError("Assembled target line census differs")

    output = unit_root / "content.html"
    if write:
        output.write_bytes(payload)
    elif not output.is_file() or output.read_bytes() != payload:
        raise RuntimeError("Assembled content.html is absent or stale")
    return {
        "unit_id": unit_id,
        "bytes": len(payload),
        "lines": len(payload.splitlines()),
        "sha256": sha256(payload),
        "fragments": fragment_rows,
        "written": write,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", choices=sorted(SPECS), required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    import json

    print(json.dumps(assemble(args.unit, write=args.write), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
