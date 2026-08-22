#!/usr/bin/env python3
"""Fail-closed QA for an admitted translated Lega unit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag


ROOT = Path(__file__).resolve().parents[1]
QA_SPECS = {
    "O005-LEGA-V101-CH01": {
        "unit_type": "chapter",
        "elements": 120,
        "links": 14,
        "math": 14,
        "problems": 7,
        "footnotes": 0,
        "assets": ["assets/modeling-cycle-id.svg"],
        "notebook": "notebooks/problem-07-open-curve-fitting.ipynb",
        "notebook_cells": 12,
        "code_cells": 7,
        "mastery_math": None,
        "lock": "numpy==2.4.4\nscipy==1.17.1\nmatplotlib==3.10.9\n",
    },
    "O005-LEGA-V101-CH02": {
        "unit_type": "chapter",
        "elements": 103,
        "links": 10,
        "math": 92,
        "problems": 7,
        "footnotes": 0,
        "assets": ["assets/the-wave-source.png"],
        "notebook": "notebooks/chapter-02-open-wave-simulation.ipynb",
        "notebook_cells": 15,
        "code_cells": 7,
        "mastery_math": 155,
        "lock": "numpy==2.4.4\nmatplotlib==3.10.9\n",
    },
    "O005-LEGA-V101-PT02": {
        "unit_type": "part",
        "elements": 0,
        "links": 0,
        "math": 0,
        "problems": 0,
        "footnotes": 0,
        "assets": [],
        "notebook": None,
        "notebook_cells": 0,
        "code_cells": 0,
        "mastery_math": 0,
        "lock": None,
        "plain_paragraphs": 3,
    },
    "O005-LEGA-V101-PT03": {
        "unit_type": "part",
        "elements": 1,
        "links": 0,
        "math": 0,
        "problems": 0,
        "footnotes": 0,
        "assets": [],
        "notebook": None,
        "notebook_cells": 0,
        "code_cells": 0,
        "mastery_math": 0,
        "lock": None,
        "plain_paragraphs": 4,
    },
    "O005-LEGA-V101-CH03": {
        "unit_type": "chapter",
        "elements": 423,
        "links": 62,
        "math": 404,
        "target_math": 407,
        "reader_math": 408,
        "math_replacements": {
            101: (
                "\\displaystyle \\frac{d \\theta}{d \\tau} = \\pm \\sqrt{2 \\cos(\\theta) + 2 E}, \\qquad \\displaystyle \\frac{d \\theta}{d t} \\in \\mathbb{R}, \\qquad E \\in [-1,\\infty). \\qquad (3.13)",
                "\\displaystyle \\frac{d \\theta}{d \\tau} = \\pm \\sqrt{2 \\cos(\\theta) + 2 E}, \\qquad \\displaystyle \\frac{d \\theta}{d \\tau} \\in \\mathbb{R}, \\qquad E \\in [-1,\\infty). \\qquad (3.13)",
            ),
            105: ("d \\theta / dt", "d \\theta / d\\tau"),
            107: (
                "[-\\arccos(E)+ 2 m \\pi, \\arccos(E) + 2 m \\pi]",
                "[-\\arccos(-E)+ 2 m \\pi, \\arccos(-E) + 2 m \\pi]",
            ),
            116: ("(1,-\\sin(\\theta))", "(\\Lambda,-\\sin(\\theta))"),
            147: (
                "\\displaystyle \\left[ \\frac{c}{m} \\frac{d \\theta}{d t}\\right] = \\left[ \\frac{1}{l \\, m}\\, c\\, l\\, \\frac{d \\theta}{d t}\\right] = L^{-1} M^{-1} [\\hbox{force}] = L^{-1} M^{-1} M L T^{-2} = T^{-2},",
                "\\displaystyle \\left[ \\frac{c}{m} \\frac{d \\theta}{d t}\\right] = \\left[ \\frac{1}{l \\, m}\\, c\\, l\\, \\frac{d \\theta}{d t}\\right] = L^{-1} M^{-1} [\\hbox{gaya}] = L^{-1} M^{-1} M L T^{-2} = T^{-2},",
            ),
            152: (
                "[\\alpha] = [c] M^{-1} T = [\\hbox{force}] L^{-1} T M^{-1}\\, T = M L T^{-2} \\, L^{-1}\\, T^2\\, M^{-1} = 1.",
                "[\\alpha] = [c] M^{-1} T = [\\hbox{gaya}] L^{-1} T M^{-1}\\, T = M L T^{-2} \\, L^{-1}\\, T^2\\, M^{-1} = 1.",
            ),
            203: ("\\alpha^2 \\gt 4)", "\\alpha^2 \\gt 4"),
            238: ("E &lt; 1", "-1 &lt; E &lt; 1"),
            246: ("A, B \\in \\mathbb{R}", "C, \\phi \\in \\mathbb{R}"),
            248: ("C, \\phi \\in \\mathbb{R}", "A, B \\in \\mathbb{R}"),
            297: (
                "\\displaystyle \\frac{d^2 x}{d t^2} + \\omega^2 x = \\epsilon \\frac{d x}{d t} (1 - x^2), \\qquad \\epsilon \\ge 0.",
                "\\displaystyle \\frac{d^2 x}{d t^2} + \\omega^2 x = \\epsilon \\frac{d x}{d t} (1 - x^2), \\qquad \\epsilon \\ge 0, \\qquad \\omega \\gt 0.",
            ),
            330: (
                "\\bar x \\in [x_0,x]",
                "\\bar x \\in [\\min(x_0,x),\\max(x_0,x)]",
            ),
            359: ("\\min(V) \\lt E \\lt \\max(V)", "\\inf V \\lt E \\lt \\sup V"),
            360: ("\\min(V)", "\\inf V"),
            361: ("\\max(V)", "\\sup V"),
        },
        "math_insertions_before": {237: ["x"], 241: ["E=-1"], 379: ["x"]},
        "problems": 23,
        "footnotes": 3,
        "assets": [
            "assets/nonlinear-pendulum-source.png",
            "assets/phase-portrait-1-source.png",
            "assets/phase-portrait-2-source.png",
            "assets/phase-portrait-construction-id-v3.png",
            "assets/phase-portrait-3-source.png",
            "assets/potential-1-source.png",
            "assets/potential-2-source.png",
            "assets/potential-3-source.png",
            "assets/potential-4-source.png",
        ],
        "notebook": "notebooks/chapter-03-open-phase-plane.ipynb",
        "notebook_cells": 13,
        "code_cells": 7,
        "mastery_math": None,
        "lock": None,
        "lock_sha256": "e0d52933f0d73f273363adb1a77c42b7680a05d3f80ccb9143dac8e079743041",
    },
    "O005-LEGA-V101-CH04": {
        "unit_type": "chapter",
        "elements": 143,
        "links": 22,
        "math": 245,
        "target_math": 258,
        "reader_math": 258,
        "math_replacements": {
            21: (
                "\\displaystyle \\rho_w \\left( \\frac{d \\vec V}{d t} + \\left(\\vec V \\cdot \\vec \\nabla \\right) \\vec V \\right)= - \\nabla p + \\mu \\nabla^2 \\vec V + \\vec f,",
                "\\displaystyle \\rho_w \\left( \\frac{\\partial \\vec V}{\\partial t} + \\left(\\vec V \\cdot \\vec \\nabla \\right) \\vec V \\right)= - \\nabla p + \\mu \\nabla^2 \\vec V + \\vec f,",
            ),
            74: (
                "\\begin{array}{ll}&amp;I_{-y} \\displaystyle \\frac{d \\omega_y}{d t} - \\omega_n \\omega_p (I_n - I_p) = N_{-y}\\\\&amp; \\displaystyle I_n \\frac{d \\omega_n}{d t} - \\omega_p \\omega_{-y} (I_p - I_{-y}) = N_n \\\\ &amp; \\displaystyle I_t \\frac{d \\omega_p}{d t} - \\omega_{-y} \\omega_n (I_{-y} - I_n) = N_p,\\end{array} \\qquad (4.5)",
                "\\begin{array}{ll}&amp;I_{-y} \\displaystyle \\frac{d \\omega_{-y}}{d t} - \\omega_n \\omega_p (I_n - I_p) = N_{-y}\\\\&amp; \\displaystyle I_n \\frac{d \\omega_n}{d t} - \\omega_p \\omega_{-y} (I_p - I_{-y}) = N_n \\\\ &amp; \\displaystyle I_p \\frac{d \\omega_p}{d t} - \\omega_{-y} \\omega_n (I_{-y} - I_n) = N_p,\\end{array} \\qquad (4.5)",
            ),
            88: (
                "\\begin{array} \\displaystyle J_1 \\frac{d \\omega_{-y}}{d t} - \\Omega_0\\, \\omega_p (J_0 - J_1) &amp;= 0 \\\\ \\displaystyle J_1 \\frac{d \\omega_p}{d t} - \\omega_{-y}\\, \\Omega_0 (J_1 - J_0) &amp;= 0, \\end{array} \\qquad (4.7)",
                "\\begin{array}{ll} \\displaystyle J_1 \\frac{d \\omega_{-y}}{d t} - \\Omega_0\\, \\omega_p (J_0 - J_1) &amp;= 0 \\\\ \\displaystyle J_1 \\frac{d \\omega_p}{d t} - \\omega_{-y}\\, \\Omega_0 (J_1 - J_0) &amp;= 0, \\end{array} \\qquad (4.7)",
            ),
            94: (
                "\\theta(t) = \\omega_{-y}(0)\\, t.",
                "\\theta(t) = \\theta(0) + \\omega_{-y}(0)\\, t.",
            ),
            95: ("\\vec y", "-\\vec y"),
            103: (
                "\\theta(t) = \\theta(0) + \\frac{1}{\\delta} \\omega_{-y}(0) \\sin(\\delta t) - \\frac{1}{\\delta} \\omega_p(0) \\cos(\\delta t)",
                "\\theta(t) = \\theta(0) + \\frac{\\omega_{-y}(0)}{\\delta} \\sin(\\delta t) + \\frac{\\omega_p(0)}{\\delta} \\left[1-\\cos(\\delta t)\\right]",
            ),
            108: (
                "\\tau_f = \\frac{2 v_z(0)}{g},",
                "\\tau_f = \\frac{2 v_z(0)}{g}, \\qquad v_z(0) \\gt 0,",
            ),
            130: (
                "{\\mathcal U}(z) = \\int_0^z F(s)\\, ds,",
                "{\\mathcal U}(z) = \\int_0^z {\\mathcal F}(s)\\, ds,",
            ),
            160: (
                "\\begin{align} {\\mathcal W} &amp; \\simeq \\left[ \\text{force along } \\vec x \\right] \\cdot \\left[ \\text{distance covered by the stone along } \\vec x \\right] \\\\ &amp; \\simeq \\vec F \\cdot \\vec x l, \\end{align}",
                "\\begin{align} {\\mathcal W} &amp; \\simeq \\left[ \\text{gaya sepanjang } \\vec x \\right] \\cdot \\left[ \\text{jarak yang ditempuh batu sepanjang } \\vec x \\right] \\\\ &amp; \\simeq \\vec F \\cdot \\vec x l, \\end{align}",
            ),
            199: ("\\theta = 20^o", "\\theta = 20^\\circ"),
            202: ("C_n", "C_f"),
            218: ("y,\\,n", "-y,\\,n"),
            235: (
                "\\displaystyle \\text{where } \\qquad \\omega_0^2 = \\frac{\\left(C_l \\cos(\\theta)-C_f \\sin(\\theta)\\right) \\rho_w v_x(0)^2 a}{2 M \\sin(\\theta)}",
                "\\displaystyle \\text{dengan } \\qquad \\omega_0^2 = \\frac{\\left(C_l \\cos(\\theta)-C_f \\sin(\\theta)\\right) \\rho_w v_x(0)^2 a}{2 M \\sin(\\theta)}",
            ),
            242: (
                "\\displaystyle \\frac{d^2 \\theta}{d t^2} + \\frac{J_0 - J_1}{J_1} (\\theta - \\theta(0)) = \\frac{{\\mathcal M}_\\theta}{J_1},",
                "\\displaystyle \\frac{d^2 \\theta}{d t^2} + \\nu^2 \\left(\\theta - \\theta(0)\\right) = \\frac{{\\mathcal M}_\\theta}{J_1},",
            ),
            243: ("{\\mathcal M}_\\theta", "{\\mathcal M}_\\theta \\equiv N_{-y}"),
            244: ("\\vec y", "-\\vec y"),
        },
        "math_insertions_before": {
            82: ["\\vec p", "\\vec t"],
            230: [
                "t=0",
                "z(0)=0",
                "\\dot z(0)=v_z(0)\\lt 0",
                "-a\\sin(\\theta)\\leq z\\leq 0",
            ],
            236: [
                "h",
                "C \\equiv C_l\\cos(\\theta)-C_f\\sin(\\theta)\\gt 0",
                "v_z(0)=-v_x(0)\\tan(\\beta)",
                "z\\lt 0",
                "|z|\\geq a\\sin(\\theta)",
            ],
            243: ["\\nu = ((J_0-J_1)/J_1)\\,\\Omega_0"],
            245: ["\\nu^2"],
        },
        "problems": 4,
        "footnotes": 4,
        "assets": [
            "assets/stone-collision-id.svg",
            "assets/stone-potential-source.png",
        ],
        "notebook": "notebooks/chapter-04-open-stone-skipping.ipynb",
        "notebook_cells": 20,
        "code_cells": 7,
        "mastery_math": None,
        "lock": None,
        "lock_sha256": "a6a514bccd39c4c2b817b4faf284ef7f1adb9e31593649a76fa6ca3239af6f9e",
    },
    "O005-LEGA-V101-CH05": {
        "unit_type": "chapter",
        "elements": 364,
        "links": 50,
        "math": 389,
        "target_math": 403,
        "reader_math": 403,
        "math_replacements": {
            26: (
                r"N(t + \Delta t) = N(t) + \text{number of births} - \text{number of deaths}.",
                r"N(t + \Delta t) = N(t) + \text{jumlah kelahiran} - \text{jumlah kematian}.",
            ),
            32: (
                r"b = \displaystyle \frac{\text{number of births per }\Delta t}{N(t) \Delta t}, \qquad d = \displaystyle \frac{\text{number of deaths per }\Delta t}{N(t) \Delta t}.",
                r"b = \displaystyle \frac{\text{jumlah kelahiran per }\Delta t}{N(t) \Delta t}, \qquad d = \displaystyle \frac{\text{jumlah kematian per }\Delta t}{N(t) \Delta t}.",
            ),
            37: (
                r"N(t+1) = \kappa\ N(t), \qquad \kappa = \text{constant}.\qquad (5.1)",
                r"N(t+1) = \kappa\ N(t), \qquad \kappa = \text{konstan}.\qquad (5.1)",
            ),
            39: (r"b - d = 0.025", r"b-d=0.025\ \text{tahun}^{-1}"),
            48: (
                r"\displaystyle N(t + \Delta t) = \Big(1 + \kappa \big(N_\infty - N(t)\big)\Big) \cdot N(t) \qquad \kappa = \text{constant},",
                r"\displaystyle N(t + \Delta t) = \Big(1 + \kappa \big(N_\infty - N(t)\big)\Big) \cdot N(t) \qquad \kappa = \text{konstan},",
            ),
            65: (r"k^{\text{th}}", "k"),
            364: ("b", r"b\gt 0"),
            365: ("d_J", r"c\gt 0"),
            366: ("d_A", r"0\leq d_J,d_A\leq 1"),
        },
        "math_insertions_before": {
            52: [r"\kappa\big(N_\infty-N(t)\big)"],
            53: [
                r"\kappa",
                r"[\kappa]=[\text{populasi}]^{-1}",
                r"1+\kappa\bigl(N_\infty-N(t)\bigr)\geq 0",
            ],
            110: [r"x \in [0,1]"],
            180: [r"M_0 \gt 0"],
            186: ["M_0=0"],
            243: [
                r"(d_1+g_1)\Delta t\leq 1",
                r"(d_2+g_2)\Delta t\leq 1",
                r"d_3\Delta t\leq 1",
            ],
            347: ["a=0", "a=4/27"],
            357: ["M(a,0)=M_0(a)", "M(0,t)=B(t)"],
        },
        "problems": 17,
        "footnotes": 7,
        "assets": [
            "assets/redhawk-count-id.svg",
            "assets/redhawk-rate-id.svg",
            "assets/redhawk-return-source.png",
            "assets/cobweb-iterations-source.png",
            "assets/logistic-bifurcation-source.png",
            "assets/logistic-bifurcation-zoom-source.png",
            "assets/one-dimensional-stability-id.svg",
        ],
        "target_image_dimensions": [
            ("300", "213"),
            ("300", "213"),
            ("300", "213"),
            ("287", "300"),
            ("300", "241"),
            ("300", "239"),
            ("300", "220"),
        ],
        "notebook": "notebooks/chapter-05-open-single-species-models.ipynb",
        "data_files": [
            "data/popclockest.txt",
            "data/popclockest.provenance.json",
        ],
        "notebook_cells": 16,
        "code_cells": 7,
        "mastery_math": None,
        "lock": None,
        "lock_sha256": "e0d52933f0d73f273363adb1a77c42b7680a05d3f80ccb9143dac8e079743041",
    },
    "O005-LEGA-V101-CH06": {
        "unit_type": "chapter",
        "elements": 185,
        "links": 31,
        "href_replacements": {
            28: (
                "https://github.com/MathWorks-Teaching-Resources/Phase-Plane-and-Slope-Field",
                "notebooks/chapter-06-open-two-species-models.ipynb",
            ),
            29: (
                "https://github.com/MathWorks-Teaching-Resources/Phase-Plane-and-Slope-Field",
                "notebooks/chapter-06-open-two-species-models.ipynb",
            ),
        },
        "attribute_replacements": {
            111: {"id": (None, "Fig_6.4")},
            115: {"id": ("Fig_6.4", "Fig_6.4_after")},
        },
        "math": 227,
        "target_math": 237,
        "reader_math": 237,
        "math_replacements": {
            35: (r"\tau = 1 / \kappa", r"t_0 = 1 / \kappa"),
            70: (r"b \le 1", r"0 \lt b \lt 1"),
            81: (
                r"\displaystyle J(1 - b, 1) = \left(\begin{array}{cc} -a b &amp; -a \\ 1 - b &amp; 0 \end{array} \right),",
                r"\displaystyle J(1, 1 - b) = \left(\begin{array}{cc} -a b &amp; -a \\ 1 - b &amp; 0 \end{array} \right),",
            ),
            84: (
                r"\det(J) = \lambda_1 \lambda_2 = \det\left[J(1-b,1)\right] = a (1 - b) &gt; 0,",
                r"\det(J) = \lambda_1 \lambda_2 = \det\left[J(1,1-b)\right] = a (1 - b) &gt; 0,",
            ),
            85: (
                r"\hbox{Tr}(J) = \lambda_1 + \lambda_2 = \hbox{Tr}\left[J(1-b,1)\right] = - a b \lt 0.",
                r"\hbox{Tr}(J) = \lambda_1 + \lambda_2 = \hbox{Tr}\left[J(1,1-b)\right] = - a b \lt 0.",
            ),
            129: (
                r"\displaystyle \frac{d f}{d \tau} = a f (1 - s) &gt; 0 \Leftrightarrow s \lt 1 \text{ and }\frac{d s}{d \tau} = s (-1 + f) &gt; 0 \Leftrightarrow f &gt; 1.",
                r"\displaystyle \frac{d f}{d \tau} = a f (1 - s) &gt; 0 \Leftrightarrow s \lt 1 \text{ dan }\frac{d s}{d \tau} = s (-1 + f) &gt; 0 \Leftrightarrow f &gt; 1.",
            ),
            156: (
                r"P_0 = (0,0), \quad P_1 = (1, 0), \quad P_2 = (1, 0), \quad P_3 = \displaystyle \left(\frac{1 - a}{1 - a b},\frac{1 - b}{1 - a b}\right).",
                r"P_0 = (0,0), \quad P_1 = (1, 0), \quad P_2 = (0, 1), \quad P_3 = \displaystyle \left(\frac{1 - a}{1 - a b},\frac{1 - b}{1 - a b}\right).",
            ),
            199: (
                r"T^2 - 4 D = \displaystyle \frac{1}{(1- a b)^2} \left[ (a-1) - c (b-1) \right]^2,",
                r"T^2-4D = \frac{[(a-1)-c(b-1)]^2+4abc(a-1)(b-1)}{(1-ab)^2},",
            ),
            207: (r"a \le 1", r"a \lt 1"),
            208: (r"b \le 1,", r"b \lt 1,"),
        },
        "math_insertions_before": {
            44: [r"a \gt 0", r"b \ge 0"],
            72: [r"P_1 = P_2 = (1,0)"],
            86: [r"0 \lt b \lt 1"],
            207: [r"P_3", r"P_3"],
            210: [r"a = 1", r"b = 1", r"a b = 1"],
            220: [r"x n"],
        },
        "problems": 6,
        "footnotes": 3,
        "assets": [
            "assets/predator-prey-damped-source.png",
            "assets/predator-prey-closed-source.png",
            "assets/competition-coexistence-source.png",
            "assets/competition-exclusion-source.png",
        ],
        "target_image_dimensions": [
            ("800", "612"),
            ("800", "607"),
            ("800", "601"),
            ("800", "602"),
        ],
        "notebook": "notebooks/chapter-06-open-two-species-models.ipynb",
        "notebook_cells": 14,
        "code_cells": 6,
        "mastery_math": 212,
        "lock": None,
        "lock_sha256": "e0d52933f0d73f273363adb1a77c42b7680a05d3f80ccb9143dac8e079743041",
    },
}
BUILDER = ROOT / "scripts" / "build_unit_reader.py"
LATEX_RE = re.compile(r"\$latex\s+(.+?)\$", re.DOTALL)


def configure(unit_id: str) -> None:
    global UNIT_ID, SPEC, SOURCE, TARGET, ASSETS, DATA_FILES, NOTEBOOK, LOCK, MASTERY
    global SEGMENTS, UNIT, BUILD
    UNIT_ID = unit_id
    SPEC = QA_SPECS[unit_id]
    SOURCE = ROOT / "authority" / "units" / UNIT_ID / "content.raw.en.html"
    TARGET = ROOT / "source" / "id-ID" / UNIT_ID / "content.html"
    ASSETS = [ROOT / "source" / "id-ID" / UNIT_ID / path for path in SPEC["assets"]]
    DATA_FILES = [
        ROOT / "source" / "id-ID" / UNIT_ID / path
        for path in SPEC.get("data_files", [])
    ]
    NOTEBOOK = ROOT / "source" / "id-ID" / UNIT_ID / SPEC["notebook"] if SPEC["notebook"] else None
    LOCK = NOTEBOOK.parent / "requirements.lock" if NOTEBOOK else None
    MASTERY = ROOT / "backend" / "mastery" / f"{UNIT_ID}.mastery.json" if SPEC["problems"] else None
    SEGMENTS = ROOT / "backend" / "segments" / f"{UNIT_ID}.segments.jsonl"
    UNIT = ROOT / "backend" / "units" / f"{UNIT_ID}.json"
    BUILD = ROOT / "build" / "reader" / UNIT_ID


configure("O005-LEGA-V101-CH01")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def tags(fragment: str) -> list[Tag]:
    return list(BeautifulSoup(fragment, "html.parser").find_all(True))


def structural_replay() -> dict:
    source_text = SOURCE.read_text(encoding="utf-8")
    target_text = TARGET.read_text(encoding="utf-8")
    source_tags, target_tags = tags(source_text), tags(target_text)
    require(
        len(source_tags) == len(target_tags) == SPEC["elements"],
        f"Expected exact {SPEC['elements']}-element source/target topology",
    )
    require([tag.name for tag in source_tags] == [tag.name for tag in target_tags], "Ordered element topology differs")
    for index, (left, right) in enumerate(zip(source_tags, target_tags), 1):
        left_attrs, right_attrs = dict(left.attrs), dict(right.attrs)
        if left.name == "img":
            left_attrs.pop("src", None); right_attrs.pop("src", None)
            left_attrs.pop("alt", None); right_attrs.pop("alt", None)
            if SPEC.get("target_image_dimensions"):
                left_attrs.pop("width", None); right_attrs.pop("width", None)
                left_attrs.pop("height", None); right_attrs.pop("height", None)
        if left.name == "h3" and right.get("id", "").startswith(f"{UNIT_ID}-P"):
            right_attrs.pop("id", None)
        if left.name == "a":
            left_attrs.pop("href", None); right_attrs.pop("href", None)
        for attribute, (old, new) in SPEC.get("attribute_replacements", {}).get(index - 1, {}).items():
            require(left_attrs.get(attribute) == old, f"Declared source attribute correction surface {index - 1}.{attribute} differs")
            require(right_attrs.get(attribute) == new, f"Declared target attribute correction surface {index - 1}.{attribute} differs")
            left_attrs.pop(attribute, None); right_attrs.pop(attribute, None)
        require(left_attrs == right_attrs, f"Unapproved attribute drift at element {index}: {left.name}")
    if SPEC.get("target_image_dimensions"):
        dimensions = [
            (tag.get("width"), tag.get("height"))
            for tag in target_tags
            if tag.name == "img"
        ]
        require(
            dimensions == SPEC["target_image_dimensions"],
            "Target image dimensions differ from the native-size declaration",
        )
    source_links = [tag["href"] for tag in source_tags if tag.name == "a" and tag.has_attr("href")]
    target_links = [tag["href"] for tag in target_tags if tag.name == "a" and tag.has_attr("href")]
    expected_target_links: list[str] = []
    href_replacements = SPEC.get("href_replacements", {})
    for index, value in enumerate(source_links):
        if index in href_replacements:
            old, new = href_replacements[index]
            require(value == old, f"Declared source href correction surface {index} differs")
            value = new
        expected_target_links.append(value)
    require(
        target_links == expected_target_links and len(source_links) == SPEC["links"],
        "Source/target href sequence differs outside declared corrections",
    )
    source_math = [match.strip() for match in LATEX_RE.findall(source_text)]
    target_math = [match.strip() for match in LATEX_RE.findall(target_text)]
    require(len(source_math) == SPEC["math"], "Frozen source TeX census differs")
    expected_target_math: list[str] = []
    replacements = SPEC.get("math_replacements", {})
    insertions = SPEC.get("math_insertions_before", {})
    for index, value in enumerate(source_math):
        expected_target_math.extend(insertions.get(index, []))
        if index in replacements:
            old, new = replacements[index]
            require(value == old, f"Declared source TeX correction surface {index} differs")
            value = new
        expected_target_math.append(value)
    expected_target_math.extend(insertions.get(len(source_math), []))
    require(
        target_math == expected_target_math
        and len(target_math) == SPEC.get("target_math", SPEC["math"]),
        "Source/target TeX sequence differs outside declared corrections",
    )
    if SPEC.get("plain_paragraphs"):
        source_paragraphs = [part for part in re.split(r"\r?\n\s*\r?\n", source_text.strip()) if part.strip()]
        target_paragraphs = [part for part in re.split(r"\r?\n\s*\r?\n", target_text.strip()) if part.strip()]
        require(
            len(source_paragraphs) == len(target_paragraphs) == SPEC["plain_paragraphs"],
            "Plain-paragraph topology differs",
        )
    require("\ufffd" not in target_text, "Target contains U+FFFD")
    ids = [tag["id"] for tag in target_tags if tag.has_attr("id")]
    require(len(ids) == len(set(ids)), "Duplicate target IDs")
    expected = [f"{UNIT_ID}-P{i:02d}" for i in range(1, SPEC["problems"] + 1)]
    require([tag["id"] for tag in target_tags if tag.name == "h3" and tag.has_attr("id")] == expected, "Problem IDs differ")
    result = {
        "elements": len(source_tags),
        "links": len(source_links),
        "math": len(source_math),
        "problems": len(expected),
    }
    if len(target_math) != len(source_math):
        result["target_math"] = len(target_math)
    return result


def backend_replay() -> dict:
    mastery = json.loads(MASTERY.read_text(encoding="utf-8")) if MASTERY else None
    problems = mastery["problems"] if mastery else []
    if mastery:
        require(mastery["unit_id"] == UNIT_ID and mastery["language"] == "id-ID", "Mastery identity differs")
        require([p["problem_id"] for p in problems] == [f"{UNIT_ID}-P{i:02d}" for i in range(1, SPEC["problems"] + 1)], "Mastery IDs differ")
        require(all(p.get("hint") and p.get("check") and p.get("solution_or_rubric") for p in problems), "Mastery record incomplete")

    records = [json.loads(line) for line in SEGMENTS.read_text(encoding="utf-8").splitlines() if line]
    require(records, "Segment backend is empty")
    for ordinal, record in enumerate(records, 1):
        require(record["segment_id"] == f"{UNIT_ID}-S{ordinal:04d}" and record["ordinal"] == ordinal, "Segment order/ID differs")
        require(record["unit_id"] == UNIT_ID and record["status"] == "translated", "Segment identity/status differs")
        require(record["source_sha256"] == sha_bytes(record["source_text"].encode("utf-8")), "Segment source hash differs")
        require(record["target_sha256"] == sha_bytes(record["target_text"].encode("utf-8")), "Segment target hash differs")

    unit = json.loads(UNIT.read_text(encoding="utf-8"))
    require(unit["unit_id"] == UNIT_ID and unit["segments"]["count"] == len(records), "Unit backend identity/count differs")
    bound_paths = [
        ("source", "content_sha256", SOURCE),
        ("target", "content_sha256", TARGET),
    ]
    if len(ASSETS) == 1:
        bound_paths.append(("target", "figure_sha256", ASSETS[0]))
    for branch, key, path in bound_paths:
        require(unit[branch][key] == sha(path), f"Unit {branch}.{key} differs")
    if len(ASSETS) > 1:
        expected_figures = [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)}
            for path in ASSETS
        ]
        require(unit["target"].get("figures") == expected_figures, "Unit target figure set differs")
    require(unit["segments"]["sha256"] == sha(SEGMENTS), "Unit segment hash differs")
    if MASTERY:
        require(unit["mastery_sha256"] == sha(MASTERY), "Unit mastery hash differs")
    else:
        require("mastery_sha256" not in unit and unit["problems"] == [], "Part unit unexpectedly binds mastery")
    if NOTEBOOK:
        require(unit["notebook_sha256"] == sha(NOTEBOOK), "Unit notebook hash differs")
    else:
        require("notebook_sha256" not in unit, "Part unit unexpectedly binds a notebook")
    expected_data = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha(path),
        }
        for path in DATA_FILES
    ]
    require(unit.get("data", []) == expected_data, "Unit data closure differs")
    return {"segments": len(records), "mastery": len(problems)}


def reader_replay(root: Path) -> dict:
    index = root / "index.html"
    require(index.is_file(), "Reader index is missing")
    soup = BeautifulSoup(index.read_text(encoding="utf-8"), "html.parser")
    require(soup.html and soup.html.get("lang") == "id-ID", "Reader lang is not id-ID")
    require(len(soup.find_all("h1")) == 1, "Reader requires exactly one h1")
    target_math_count = SPEC.get("reader_math", SPEC.get("target_math", SPEC["math"]))
    require(
        len(soup.select(f"article.{SPEC['unit_type']} math")) == target_math_count,
        f"Reader unit requires exactly {target_math_count} MathML formulas",
    )
    mastery_math = len(soup.select("#dukungan-belajar math"))
    if SPEC["mastery_math"] is not None:
        require(mastery_math == SPEC["mastery_math"], "Reader mastery MathML count differs")
    require(len(soup.find_all("details")) == 3 * SPEC["problems"], "Reader mastery disclosure count differs")
    require(
        len(soup.select('span.reader-footnote[role="note"]')) == SPEC["footnotes"],
        "Reader footnote conversion count differs",
    )
    require("[footnote]" not in index.read_text(encoding="utf-8"), "Reader exposes a footnote shortcode")
    ids = [tag["id"] for tag in soup.find_all(id=True)]
    require(len(ids) == len(set(ids)), "Reader contains duplicate IDs")
    local_files: set[Path] = set()
    for tag in soup.find_all(href=True) + soup.find_all(src=True):
        value = tag.get("href") or tag.get("src")
        parsed = urlparse(value)
        if parsed.scheme or value.startswith(("#", "//")):
            if value.startswith("#"):
                require(value[1:] in ids, f"Broken internal fragment: {value}")
            continue
        path = (root / parsed.path).resolve()
        require(root.resolve() in path.parents or path == root.resolve(), f"Reader path escapes root: {value}")
        require(path.is_file(), f"Missing local reader dependency: {value}")
        local_files.add(path)
    for asset in ASSETS:
        expected_asset = (root / "assets" / asset.name).resolve()
        require(expected_asset in local_files, f"Reader does not reference admitted asset: {asset.name}")
    for data_file in DATA_FILES:
        expected_data_file = (root / "data" / data_file.name).resolve()
        require(
            expected_data_file in local_files,
            f"Reader does not expose admitted data file: {data_file.name}",
        )

    manifest_path = root / "PACKAGE_MANIFEST.tsv"
    rows = manifest_path.read_text(encoding="utf-8").splitlines()
    require(rows[0] == "path\tbytes\tsha256", "Package manifest header differs")
    manifest: dict[str, tuple[int, str]] = {}
    for row in rows[1:]:
        rel, size, checksum = row.split("\t")
        require(rel not in manifest, f"Duplicate manifest path: {rel}")
        manifest[rel] = (int(size), checksum)
    actual = sorted(path for path in root.rglob("*") if path.is_file() and path != manifest_path)
    require(set(manifest) == {path.relative_to(root).as_posix() for path in actual}, "Manifest member set differs")
    for path in actual:
        rel = path.relative_to(root).as_posix()
        require(manifest[rel] == (path.stat().st_size, sha(path)), f"Manifest row differs: {rel}")
    public_bytes = b"\n".join(path.read_bytes() for path in actual)
    lowered = public_bytes.lower()
    for forbidden in (
        b"c:" + b"\\" + b"users" + b"\\",
        b"c:" + b"/" + b"users" + b"/",
        b"flo" + b"ris",
        b"github" + b"_pat_",
        b"gh" + b"p_",
        b"s" + b"k-",
    ):
        require(forbidden not in lowered, f"Privacy/secret marker in reader: {forbidden!r}")
    require(b"\xef\xbf\xbd" not in public_bytes, "Reader contains U+FFFD")
    require(not any(path.suffix.lower() == ".m" for path in actual), "Reader ships proprietary-tool source")
    return {
        "files": len(actual),
        "bytes": sum(path.stat().st_size for path in actual),
        "local_dependencies": len(local_files),
        "chapter_mathml": target_math_count,
        "mastery_mathml": mastery_math,
    }


def notebook_replay(execute: bool) -> dict:
    if NOTEBOOK is None:
        return {"cells": 0, "code_cells": 0, "executed": False, "applicable": False}
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    code = [cell for cell in cells if cell.get("cell_type") == "code"]
    require(cells and code, "Notebook has no executable closure")
    if SPEC["notebook_cells"] is not None:
        require(len(cells) == SPEC["notebook_cells"], "Notebook cell census differs")
    if SPEC["code_cells"] is not None:
        require(len(code) == SPEC["code_cells"], "Notebook code-cell census differs")
    require(len({cell.get("id") for cell in cells}) == len(cells), "Notebook cell IDs are not unique")
    require(all(not cell.get("outputs") and cell.get("execution_count") is None for cell in code), "Notebook must remain output-clean")
    if SPEC.get("lock") is not None:
        require(LOCK.read_text(encoding="utf-8") == SPEC["lock"], "Notebook lock differs")
    else:
        require(sha(LOCK) == SPEC["lock_sha256"], "Notebook lock hash differs")
    if execute:
        env = dict(os.environ)
        env["MPLBACKEND"] = "Agg"
        runner = "import json,sys; n=json.load(open(sys.argv[1],encoding='utf-8')); g={}; [exec(compile(''.join(c['source']), c.get('id','cell'), 'exec'),g) for c in n['cells'] if c.get('cell_type')=='code']"
        subprocess.run([sys.executable, "-c", runner, str(NOTEBOOK)], check=True, env=env, timeout=120)
    return {"cells": len(cells), "code_cells": len(code), "executed": execute}


def deterministic_replay() -> dict:
    prefix = UNIT_ID.lower() + "-"
    with tempfile.TemporaryDirectory(prefix=prefix + "a-") as a, tempfile.TemporaryDirectory(prefix=prefix + "b-") as b:
        for output in (a, b):
            subprocess.run([sys.executable, str(BUILDER), "--unit", UNIT_ID, "--output", output], check=True, capture_output=True, text=True, timeout=180)
        left, right = Path(a), Path(b)
        left_files = sorted(path.relative_to(left).as_posix() for path in left.rglob("*") if path.is_file())
        right_files = sorted(path.relative_to(right).as_posix() for path in right.rglob("*") if path.is_file())
        require(left_files == right_files, "Repeated build member sets differ")
        for rel in left_files:
            require((left / rel).read_bytes() == (right / rel).read_bytes(), f"Repeated build bytes differ: {rel}")
        return {"files": len(left_files), "tree_sha256": sha_bytes("\n".join(f"{rel}\t{sha(left / rel)}" for rel in left_files).encode("utf-8"))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", choices=sorted(QA_SPECS), default="O005-LEGA-V101-CH01")
    parser.add_argument("--execute-notebook", action="store_true")
    parser.add_argument("--deterministic-build", action="store_true")
    args = parser.parse_args()
    configure(args.unit)
    result = {
        "schema": "o005-unit-qa-v1",
        "unit_id": UNIT_ID,
        "structure": structural_replay(),
        "backend": backend_replay(),
        "reader": reader_replay(BUILD),
        "notebook": notebook_replay(args.execute_notebook),
        "external_link_reachability_tested": False,
        "audio_or_live_widgets_exercised": False,
    }
    if args.deterministic_build:
        result["deterministic_build"] = deterministic_replay()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
