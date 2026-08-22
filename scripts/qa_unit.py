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
import zipfile
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
        "mastery_math": 46,
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
    "O005-LEGA-V101-PT04": {
        "unit_type": "part",
        "elements": 6,
        "links": 0,
        "math": 11,
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
    "O005-LEGA-V101-PT05": {
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
        "plain_paragraphs": 2,
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
    "O005-LEGA-V101-CH07": {
        "unit_type": "chapter",
        "elements": 126,
        "links": 29,
        "math": 150,
        "target_math": 160,
        "reader_math": 160,
        "math_replacements": {
            46: (r"\beta \ge 0", r"\beta \gt 0"),
            81: (
                r"\displaystyle \lim_{t \rightarrow \infty} i = 0.",
                r"\displaystyle \lim_{\tau \rightarrow \infty} i = 0.",
            ),
            95: (
                r"P_1 = (1, 0) \qquad \text{and} \qquad P_2 = \left(\eta + \delta, \displaystyle \frac{\eta (1 - \eta - \delta)}{\eta + \delta}\right).",
                r"P_1 = (1, 0) \qquad \text{dan} \qquad P_2 = \left(\eta + \delta, \displaystyle \frac{\eta (1 - \eta - \delta)}{\eta + \delta}\right).",
            ),
            122: (r"\eta = 0.2", r"\eta = 0.1"),
            123: (r"\delta=0.1", r"\delta=0.2"),
        },
        "math_insertions_before": {
            103: [r"\eta + \delta = 1", r"P_2=P_1=(1,0)"],
            111: [
                r"\displaystyle \frac{d i}{d\tau}=i[s-(\eta+\delta)]\le i[1-(\eta+\delta)]",
                r"i",
                r"s",
                r"\mathcal T",
                r"P_1",
            ],
            121: [r"\mathcal T"],
            132: [r"s+i &gt; 1"],
            135: [r"s+i &gt; 1"],
        },
        "problems": 5,
        "footnotes": 1,
        "assets": [
            "assets/sir-phase-source.png",
            "assets/endemic-phase-1-source.png",
            "assets/endemic-phase-2-source.png",
        ],
        "target_image_dimensions": [
            ("800", "594"),
            ("800", "593"),
            ("800", "593"),
        ],
        "notebook": "notebooks/chapter-07-open-epidemiology.ipynb",
        "notebook_cells": 14,
        "code_cells": 6,
        "mastery_math": 151,
        "lock": None,
        "lock_sha256": "e0d52933f0d73f273363adb1a77c42b7680a05d3f80ccb9143dac8e079743041",
    },
    "O005-LEGA-V101-CH08": {
        "unit_type": "chapter",
        "elements": 179,
        "links": 28,
        "math": 186,
        "target_math": 186,
        "reader_math": 186,
        "problems": 13,
        "footnotes": 6,
        "assets": [
            "assets/brusselator-phase-source.png",
            "assets/brusselator-time-series-source.png",
            "assets/oregonator-phase-source.png",
        ],
        "target_image_dimensions": [
            ("800", "535"),
            ("800", "684"),
            ("800", "525"),
        ],
        "notebook": "notebooks/chapter-08-open-chemical-reactions.ipynb",
        "notebook_cells": 16,
        "code_cells": 7,
        "mastery_math": 321,
        "lock": None,
        "lock_sha256": "e0d52933f0d73f273363adb1a77c42b7680a05d3f80ccb9143dac8e079743041",
    },
    "O005-LEGA-V101-CH09": {
        "unit_type": "chapter",
        "elements": 166,
        "links": 27,
        "math": 213,
        "target_math": 214,
        "reader_math": 214,
        "problems": 7,
        "footnotes": 5,
        "assets": [
            "assets/diffusion-random-walk-source.png",
            "assets/fisher-traveling-wave-phase-1-source.png",
            "assets/fisher-traveling-wave-phase-2-source.png",
        ],
        "target_image_dimensions": [
            ("300", "261"),
            ("800", "604"),
            ("800", "593"),
        ],
        "math_replacements": {
            18: ("N_i", "F"),
            26: ("\\Omega", "\\partial \\Omega"),
            38: (
                "\\displaystyle 0 = \\iiint_\\Omega \\left[-\\frac{\\partial F}{\\partial t} + R(x,y,z,t) - \\vec \\nabla \\cdot \\vec \\jmath \\right] \\ dV.",
                "\\displaystyle 0 = \\iiint_\\Omega \\left[-\\frac{\\partial F}{\\partial t} + R(x,y,z,t,F) - \\vec \\nabla \\cdot \\vec \\jmath \\right] \\ dV.",
            ),
            84: (
                "|\\vec r_1|^2 = l^2, \\qquad \\hbox{and} \\qquad \\langle |\\vec r_1|^2 \\rangle = l^2,",
                "|\\vec r_1|^2 = l^2, \\qquad \\hbox{dan} \\qquad \\langle |\\vec r_1|^2 \\rangle = l^2,",
            ),
            98: (
                "\\begin{array}{ll} \\langle \\vec r_n \\cdot (\\vec r_{n+1}-\\vec r_n) \\rangle &amp;= l\\, (\\vec r_n \\cdot \\vec \\imath) \\langle \\cos(\\theta_{n+1}) \\rangle + l\\, (\\vec r_n \\cdot \\vec \\jmath) \\langle \\sin(\\theta_{n+1}) \\rangle \\\\ &amp;= 0, \\end{array}",
                "\\begin{array}{ll} \\left\\langle \\vec r_n \\cdot (\\vec r_{n+1}-\\vec r_n) \\mid \\vec r_n \\right\\rangle &amp;= l\\, (\\vec r_n \\cdot \\vec \\imath) \\langle \\cos(\\theta_{n+1}) \\rangle + l\\, (\\vec r_n \\cdot \\vec \\jmath) \\langle \\sin(\\theta_{n+1}) \\rangle \\\\ &amp;= 0, \\end{array}",
            ),
            124: (
                "\\displaystyle n = \\frac{N}{K}, \\qquad x = X \\sqrt \\frac{r}{D}, \\qquad y = Y\\sqrt \\frac{r}{D}, \\qquad \\tau = r\\, t,",
                "\\displaystyle n = \\frac{N}{K}, \\qquad x = X \\sqrt \\frac{r}{D}, \\qquad \\tau = r\\, t,",
            ),
            128: ("n(x,t) = v (\\xi)", "n(x,\\tau) = v (\\xi)"),
            129: ("\\xi = x - c t", "\\xi = x - c \\tau"),
            131: (
                "\\displaystyle \\frac{\\partial n}{\\partial t} = - c \\frac{d v}{d \\xi}, \\qquad \\frac{\\partial n}{\\partial x} = \\frac{d v}{d \\xi},",
                "\\displaystyle \\frac{\\partial n}{\\partial \\tau} = - c \\frac{d v}{d \\xi}, \\qquad \\frac{\\partial n}{\\partial x} = \\frac{d v}{d \\xi},",
            ),
            167: ("0 &lt; c &lt; 2.", "0 &lt; c &lt; 2"),
            198: (
                "\\vec \\jmath = \\chi \\vec \\nabla n - D \\vec \\nabla b,",
                "\\vec \\jmath = \\chi b \\vec \\nabla n - D \\vec \\nabla b,",
            ),
        },
        "math_insertions_before": {73: ["\\vec \\mu=(\\xi,\\zeta,\\eta)"]},
        "notebook": "notebooks/chapter-09-open-diffusion.ipynb",
        "notebook_cells": 10,
        "code_cells": 4,
        "mastery_math": 189,
        "footnote_links": [
            "https://doi.org/10.1016/j.physrep.2003.08.001",
        ],
        "descriptive_links": [
            "https://doi.org/10.1126/science.230.4726.661",
        ],
        "lock": None,
        "lock_sha256": "e0d52933f0d73f273363adb1a77c42b7680a05d3f80ccb9143dac8e079743041",
    },
    "O005-LEGA-V101-CH10": {
        "unit_type": "chapter",
        "elements": 116,
        "links": 24,
        "math": 77,
        "target_math": 78,
        "reader_math": 78,
        "problems": 6,
        "footnotes": 13,
        "assets": [
            "assets/pattern-stripes-independent.svg",
            "assets/swift-hohenberg-patterns-source.png",
            "assets/pattern-growth-rates-source.png",
        ],
        "data_files": [
            "assets/pattern-stripes-independent.provenance.json",
        ],
        "target_image_dimensions": [
            ("800", "560"),
            ("300", "141"),
            ("300", "142"),
        ],
        "math_replacements": {
            10: (
                "\\lambda_{\\vec k}\\ u_{\\vec k}",
                "\\lambda_{\\vec k}",
            ),
            12: (
                "\\sigma_k = \\Re e(\\lambda_{\\vec k}) = \\mu - \\alpha (\\Omega - k^2)^2,",
                "\\sigma_k = \\operatorname{Re}(\\lambda_{\\vec k}) = \\mu - \\alpha (\\Omega - k^2)^2,",
            ),
            54: (
                "\\psi(x,t) = \\exp[i(\\omega t + q x + p y)], \\qquad \\omega,\\, q,\\,p\\, \\in \\mathbb{R}.",
                "\\psi(x,y,t) = \\exp[i(\\omega t + q x + p y)], \\qquad \\omega,\\, q,\\,p\\, \\in \\mathbb{R}.",
            ),
            58: (
                "\\psi(x,t) = \\exp[i(\\omega t + q x + p y)], \\qquad \\omega,\\, q,\\,p\\, \\in \\mathbb{R}.",
                "\\psi(x,y,t) = \\exp[i(\\omega t + q x + p y)], \\qquad \\omega,\\, q,\\,p\\, \\in \\mathbb{R}.",
            ),
            63: (
                "\\psi(x,t) = \\exp[\\lambda t + i(\\omega t + q x + p y)], \\qquad \\lambda,\\,\\omega,\\, q,\\,p\\, \\in \\mathbb{R}",
                "\\psi(x,y,t) = \\exp[\\lambda t + i(\\omega t + q x + p y)], \\qquad \\lambda,\\,\\omega,\\, q,\\,p\\, \\in \\mathbb{R}",
            ),
        },
        "math_insertions_before": {65: ["\\lambda"]},
        "notebook": "notebooks/chapter-10-open-pattern-formation.ipynb",
        "notebook_cells": None,
        "code_cells": None,
        "mastery_math": None,
        "footnote_links": [
            "https://doi.org/10.1126/science.284.5421.1826",
        ],
        "descriptive_links": [
            "https://doi.org/10.1103/PhysRevLett.73.2978",
        ],
        "lock": None,
        "lock_sha256": "e0d52933f0d73f273363adb1a77c42b7680a05d3f80ccb9143dac8e079743041",
    },
    "O005-LEGA-V101-CH11": {
        "unit_type": "chapter",
        "elements": 127,
        "links": 0,
        "math": 165,
        "target_math": 165,
        "reader_math": 165,
        "math_replacements": {
            1: (
                r"\begin{align*} &amp; \forall x, y \in {\mathcal S}, x+y \in {\mathcal S} \\ &amp; \forall x \in {\mathcal S}, \forall \alpha \in \mathbb{R} \text{ (resp. }\mathbb{C}), \alpha x \in {\mathcal S}. \end{align*}",
                r"\begin{align*} &amp; \forall x, y \in {\mathcal S}, x+y \in {\mathcal S} \\ &amp; \forall x \in {\mathcal S}, \forall \alpha \in \mathbb{R} \text{ (atau }\mathbb{C}), \alpha x \in {\mathcal S}. \end{align*}",
            ),
            2: (
                r"\{u_i \in S, i=1 \dots n\}",
                r"\{u_i\in\mathcal S\mid i=1,\dots,n\}",
            ),
            3: (
                r"\begin{align*} \forall &amp;\{\alpha_i, i=1, \dots n \} \subset \mathbb{R} \text { (or } \mathbb{C}),\\ &amp;\sum_{i=1}^n \alpha_i\,u_i = 0 \Longrightarrow \alpha_i = 0, \forall i=1, \dots n. \end{align*}",
                r"\begin{align*} &amp;\forall\,\alpha_1,\dots,\alpha_n \in \mathbb{R} \text{ (atau } \mathbb{C}),\\ &amp;\sum_{i=1}^n \alpha_i\,u_i = 0 \Longrightarrow \alpha_i = 0,\ \forall i=1,\dots,n. \end{align*}",
            ),
            41: (r"i^{\hbox{th}}", "i"),
            42: (r"j^{\hbox{th}}", "j"),
            48: (r"(A^T_{ij}) = (A_{ji})", r"(A^T)_{ij}=A_{ji}"),
            88: ("A X = b", "A x = b"),
            104: (r"m \ne 1", r"m \ge 1"),
            105: (
                r"(A - a I_n) f \ne 0, \qquad (A - a I_n)^m f = 0, \qquad f \ne 0.",
                r"(A - a I_n)^{m-1} f \ne 0, \qquad (A - a I_n)^m f = 0, \qquad f \ne 0.",
            ),
            112: (
                r"\det (A - a I)= 0, \qquad (A1.2)",
                r"\det (A - a I_n)= 0, \qquad (A1.2)",
            ),
            143: (
                r"{\mathcal T}(\vec x) = \left[\begin{array}{c} 0 \\ 2 x_1 - 4 x_2 + x_5 \\ x_2 + x_3 + x_5 \end{array}\right], \qquad \text{where} \qquad \vec x = \left[\begin{array}{c}x_1 \\ x_2 \\ x_3 \\ x_4 \\ x_5 \end{array}\right].",
                r"{\mathcal T}(\vec x) = \left[\begin{array}{c} 0 \\ 2 x_1 - 4 x_2 + x_5 \\ x_2 + x_3 + x_5 \end{array}\right], \qquad \text{dengan} \qquad \vec x = \left[\begin{array}{c}x_1 \\ x_2 \\ x_3 \\ x_4 \\ x_5 \end{array}\right].",
            ),
            163: (
                r"\begin{align*} &amp;\vec v_1 = \left[\begin{array}{cccc} 1 \\ 2 \\ 3 \\ 4\end{array}\right],\qquad \vec v_2 = \left[\begin{array}{cccc} 0 \\ 1 \\ 0 \\ -1\end{array}\right],\qquad \vec v_3 = \left[\begin{array}{cccc} 1 \\ 0 \\ 1 \\ 0\end{array}\right],\\ &amp; \vec v_4 = \left[\begin{array}{cccc} 1 \\ 1 \\ 1 \\ -2\end{array}\right],\qquad \vec v_5 = \left[\begin{array}{cccc} 1 \\ 1 \\ 1 \\ 1\end{array}\right]. \end{align*}",
                r"\begin{align*} &amp;\vec v_1 = \left[\begin{array}{c} 1 \\ 2 \\ 3 \\ 4\end{array}\right],\qquad \vec v_2 = \left[\begin{array}{c} 0 \\ 1 \\ 0 \\ -1\end{array}\right],\qquad \vec v_3 = \left[\begin{array}{c} 1 \\ 0 \\ 1 \\ 0\end{array}\right],\\ &amp; \vec v_4 = \left[\begin{array}{c} 1 \\ 1 \\ 1 \\ -2\end{array}\right],\qquad \vec v_5 = \left[\begin{array}{c} 1 \\ 1 \\ 1 \\ 1\end{array}\right]. \end{align*}",
            ),
        },
        "problems": 7,
        "footnotes": 0,
        "assets": [],
        "notebook": None,
        "notebook_cells": 0,
        "code_cells": 0,
        "mastery_math": 156,
        "lock": None,
    },
    "O005-LEGA-V101-CH12": {
        "unit_type": "chapter",
        "elements": 85,
        "links": 0,
        "math": 161,
        "target_math": 165,
        "reader_math": 165,
        "math_replacements": {
            49: (
                r"\displaystyle W = \int_{t_0}^{t_1} m\ \frac{d^2 \vec r}{d t^2} \cdot \frac{d \vec r}{d t}\ dt = \left[\frac{1}{2} m \left(\frac{d \vec r}{d t}\right)^2 \right]_{t_0}^{t_1} = \left[ \frac{1}{2} m v^2 \right]_{t_0}^{t_1},",
                r"\displaystyle W = \int_{t_0}^{t_1} m\ \frac{d^2 \vec r}{d t^2} \cdot \frac{d \vec r}{d t}\ dt = \left[\frac{1}{2} m \left\|\frac{d \vec r}{d t}\right\|^2 \right]_{t_0}^{t_1} = \left[ \frac{1}{2} m v^2 \right]_{t_0}^{t_1},",
            ),
            69: (r"V(r)", r"V(\vec r)"),
            94: (
                r"\displaystyle \iint_S \vec F \cdot d\vec S = \iint_R \vec F\left(x,y,z(x,y)\right)\cdot \left[-\frac{\partial f}{\partial x} \vec \imath - \frac{\partial f}{\partial y} \vec \jmath + \vec k \right] dx dy,",
                r"\displaystyle \iint_S \vec F \cdot d\vec S = \iint_R \vec F\left(x,y,f(x,y)\right)\cdot \left[-\frac{\partial f}{\partial x} \vec \imath - \frac{\partial f}{\partial y} \vec \jmath + \vec k \right] dx dy,",
            ),
            134: (
                r"\text{div} \vec F = \displaystyle \lim_{W \rightarrow 0} \frac{\int_S \vec F \cdot d \vec A} {\hbox{volume of }W}.",
                r"\text{div} \vec F(P) = \displaystyle \lim_{\varepsilon \rightarrow 0} \frac{\iint_{\partial B_\varepsilon(P)} \vec F \cdot \vec n\, dS}{\operatorname{vol}(B_\varepsilon(P))}.",
            ),
        },
        "math_insertions_before": {
            50: [r"v"],
            134: [r"B_\varepsilon(P)", r"\partial B_\varepsilon(P)", r"\vec n"],
        },
        "problems": 0,
        "footnotes": 0,
        "assets": [],
        "notebook": None,
        "notebook_cells": 0,
        "code_cells": 0,
        "mastery_math": 0,
        "lock": None,
    },
    "O005-LEGA-V101-CH13": {
        "unit_type": "chapter",
        "elements": 456,
        "links": 39,
        "math": 524,
        "target_math": 528,
        "reader_math": 528,
        "math_replacements": {
            15: (
                r"\displaystyle Y = \left(y,\frac{dy}{d x},\frac{d^2 y}{d x}, \cdots, \frac{d^{n-1} y}{d x^{n-1}}\right)",
                r"\displaystyle Y = \left(y,\frac{dy}{d x},\frac{d^2 y}{d x^2}, \cdots, \frac{d^{n-1} y}{d x^{n-1}}\right)",
            ),
            51: (
                r"\displaystyle \frac{\partial u}{\partial x}=M(x,y) \qquad \text{and} \qquad \frac{\partial u}{\partial y}=N(x,y).",
                r"\displaystyle \frac{\partial u}{\partial x}=M(x,y) \qquad \text{dan} \qquad \frac{\partial u}{\partial y}=N(x,y).",
            ),
            56: (
                r"\displaystyle \frac{\partial u}{\partial x}=M(x,y) \quad \text{ and } \quad \frac{\partial u}{\partial y}=N(x,y).",
                r"\displaystyle \frac{\partial u}{\partial x}=M(x,y) \quad \text{ dan } \quad \frac{\partial u}{\partial y}=N(x,y).",
            ),
            67: (
                r"\rho(x,y)=f(x).",
                r"\rho(x)=\exp\left(\int f(x)\,dx\right).",
            ),
            70: (
                r"\rho(x,y)=f(y).",
                r"\rho(y)=\exp\left(-\int f(y)\,dy\right).",
            ),
            105: (
                r"y = c x + f(c), \qquad c=\text{ constant}",
                r"y = c x + f(c), \qquad c=\text{ konstan}",
            ),
            157: (
                r"y_1(x)=\exp(r_1 x) \qquad {\rm and} \qquad y_2(x)=\exp(r_2 x).",
                r"y_1(x)=\exp(r_1 x) \qquad \text{dan} \qquad y_2(x)=\exp(r_2 x).",
            ),
            168: (
                r"a_2 x^2 y^{\prime\prime} + a_1 x y^\prime+ a_0 y=0, \quad a_2, a_1, \text{and }a_0 \text{ constants},",
                r"a_2 x^2 y^{\prime\prime} + a_1 x y^\prime+ a_0 y=0, \quad a_2, a_1, \text{dan }a_0 \text{ konstan},",
            ),
            315: (
                r"x_1(t)=\alpha_1, x_2(t)=\alpha_2,\dots, x_n(t)=\alpha_n",
                r"x_1(t_0)=\alpha_1, x_2(t_0)=\alpha_2,\dots, x_n(t_0)=\alpha_n",
            ),
            363: (
                "X_i(t)=\\Re e[\\exp(\\alpha+i \\beta)\n\\xi]",
                "X_i(t)=\\operatorname{Re}[\\exp((\\alpha+i\\beta)t)\n\\xi]",
            ),
            364: (
                r"X_{i+1}(t)=\Im m[\exp(\alpha+i \beta) \xi]",
                r"X_{i+1}(t)=\operatorname{Im}[\exp((\alpha+i\beta)t) \xi]",
            ),
            386: (r"\Re e(X_p)", r"\operatorname{Re}(X_p)"),
            387: (r"\Im m(X_p)", r"\operatorname{Im}(X_p)"),
            429: (
                r"Y = \left(\begin{array}{c}x \\ y \end{array} \right), \qquad F(X) = \left(\begin{array}{c} F_1(x,y) \\ F_2(x,y) \end{array} \right), \qquad Y_0 = \left(\begin{array}{c}x_0 \\ y_0 \end{array} \right).",
                r"Y = \left(\begin{array}{c}x \\ y \end{array} \right), \qquad F(Y) = \left(\begin{array}{c} F_1(x,y) \\ F_2(x,y) \end{array} \right), \qquad Y_0 = \left(\begin{array}{c}x_0 \\ y_0 \end{array} \right).",
            ),
            461: (
                r"\det(A)&gt;0",
                r"\det(A)\ge 0",
            ),
            505: (
                r"A = \left( \begin{array}{cc} 7 &amp; 6 \\ 2 &amp; 6 \end{array} \right) \quad \text{and} \quad B = \left(\begin{array}{c} -70 \\ 35 \end{array} \right) \exp(3 t).",
                r"A = \left( \begin{array}{cc} 7 &amp; 6 \\ 2 &amp; 6 \end{array} \right) \quad \text{dan} \quad B = \left(\begin{array}{c} -70 \\ 35 \end{array} \right) \exp(3 t).",
            ),
            520: (
                r"\displaystyle \left\{ \begin{array}{l} x = C_1 \cos(t) e^{2 t} + C_2 \sin(t) e^{2 t} - 2 e^t \\ y = -C_1 \sin(t) e^{2 t} + C_2 \cos(t) e^{2 t} - e^t \end{array} \right. .",
                r"\displaystyle \left\{ \begin{array}{l} x = 2 \cos(t) e^{2 t} + 2 \sin(t) e^{2 t} - 2 e^t \\ y = -2 \sin(t) e^{2 t} + 2 \cos(t) e^{2 t} - e^t \end{array} \right. .",
            ),
        },
        "math_insertions_before": {
            47: [r"y=-x"],
            90: [r"y=0"],
            104: [r"y=x"],
            121: [r"y=C"],
        },
        "problems": 11,
        "answer_headings": 11,
        "footnotes": 0,
        "assets": [
            "assets/phase-stable-node-source.png",
            "assets/phase-stable-star-source.png",
            "assets/phase-stable-degenerate-node-source.png",
            "assets/phase-stable-spiral-source.png",
            "assets/phase-saddle-source.png",
            "assets/phase-line-fixed-points-source.png",
            "assets/phase-center-source.png",
            "assets/fixed-point-classification-source.png",
        ],
        "target_image_dimensions": [
            ("150", "109"),
            ("150", "109"),
            ("150", "109"),
            ("150", "109"),
            ("150", "127"),
            ("150", "109"),
            ("100", "125"),
            ("1024", "690"),
        ],
        "notebook": None,
        "notebook_cells": 0,
        "code_cells": 0,
        "mastery_math": None,
        "lock": None,
    },
    "O005-LEGA-V101-CH14": {
        "unit_type": "chapter",
        "elements": 252,
        "links": 16,
        "math": 0,
        "target_math": 0,
        "reader_math": 0,
        "math_replacements": {},
        "math_insertions_before": {},
        "problems": 0,
        "footnotes": 0,
        "assets": [],
        "notebook": None,
        "notebook_cells": 0,
        "code_cells": 0,
        "mastery_math": 0,
        "lock": None,
        "project_headings": 12,
        "project_id_prefix": "O005-LEGA-V101-PRJ",
        "project_catalog": "backend/projects/O005-LEGA-V101-CH14.projects.json",
        "project_archives": [
            "source/id-ID/O005-LEGA-V101-CH14/project_archives/O005-LEGA-V101-PRJ01.zip",
            "source/id-ID/O005-LEGA-V101-CH14/project_archives/O005-LEGA-V101-PRJ02.zip",
            "source/id-ID/O005-LEGA-V101-CH14/project_archives/O005-LEGA-V101-PRJ03.zip",
            "source/id-ID/O005-LEGA-V101-CH14/project_archives/O005-LEGA-V101-PRJ04.zip",
            "source/id-ID/O005-LEGA-V101-CH14/project_archives/O005-LEGA-V101-PRJ05.zip",
            "source/id-ID/O005-LEGA-V101-CH14/project_archives/O005-LEGA-V101-PRJ06.zip",
            "source/id-ID/O005-LEGA-V101-CH14/project_archives/O005-LEGA-V101-PRJ07.zip",
            "source/id-ID/O005-LEGA-V101-CH14/project_archives/O005-LEGA-V101-PRJ08.zip",
            "source/id-ID/O005-LEGA-V101-CH14/project_archives/O005-LEGA-V101-PRJ09.zip",
            "source/id-ID/O005-LEGA-V101-CH14/project_archives/O005-LEGA-V101-PRJ10.zip",
            "source/id-ID/O005-LEGA-V101-CH14/project_archives/O005-LEGA-V101-PRJ11.zip",
            "source/id-ID/O005-LEGA-V101-CH14/project_archives/O005-LEGA-V101-PRJ12.zip",
        ],
        "attribute_replacements": {
            164: {"class": (None, ["uacm-text-center"])},
            184: {"class": (None, ["uacm-text-center"])},
            208: {"class": (None, ["uacm-text-center"])},
            228: {"class": (None, ["uacm-text-center"])},
        },
    },
}
BUILDER = ROOT / "scripts" / "build_unit_reader.py"
LATEX_RE = re.compile(r"\$latex\s+(.+?)\$", re.DOTALL)


def configure(unit_id: str) -> None:
    global UNIT_ID, SPEC, SOURCE, TARGET, ASSETS, DATA_FILES, NOTEBOOK, LOCK, MASTERY
    global SEGMENTS, UNIT, BUILD, PROJECT_CATALOG, PROJECT_ARCHIVES, PROJECT_NOTEBOOKS
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
    project_catalog = SPEC.get("project_catalog")
    PROJECT_CATALOG = ROOT / project_catalog if project_catalog else None
    PROJECT_ARCHIVES = [ROOT / path for path in SPEC.get("project_archives", [])]
    PROJECT_NOTEBOOKS = []
    if PROJECT_CATALOG and PROJECT_CATALOG.is_file():
        catalog = json.loads(PROJECT_CATALOG.read_text(encoding="utf-8"))
        PROJECT_NOTEBOOKS = [ROOT / row["notebook_path"] for row in catalog["projects"]]


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
        if left.name == "h3" and right.get("id", "").startswith((f"{UNIT_ID}-P", f"{UNIT_ID}-A")):
            right_attrs.pop("id", None)
        if left.name == "h2" and right.get("id", "").startswith(SPEC.get("project_id_prefix", f"{UNIT_ID}-PRJ")):
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
    expected_answer_ids = [
        f"{UNIT_ID}-A{i:02d}"
        for i in range(1, SPEC.get("answer_headings", 0) + 1)
    ]
    require(
        [tag["id"] for tag in target_tags if tag.name == "h3" and tag.has_attr("id")]
        == expected + expected_answer_ids,
        "Problem/answer heading IDs differ",
    )
    project_count = int(SPEC.get("project_headings", 0))
    if project_count:
        project_prefix = SPEC.get("project_id_prefix", f"{UNIT_ID}-PRJ")
        require(
            [tag["id"] for tag in target_tags if tag.name == "h2" and tag.has_attr("id")]
            == [f"{project_prefix}{i:02d}" for i in range(1, project_count + 1)],
            "Project heading IDs differ",
        )
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
    project_count = int(SPEC.get("project_headings", 0))
    if project_count:
        require(PROJECT_CATALOG and PROJECT_CATALOG.is_file(), "Project catalog is missing")
        require(len(PROJECT_ARCHIVES) == project_count, "Project archive count differs")
        catalog = json.loads(PROJECT_CATALOG.read_text(encoding="utf-8"))
        expected_ids = [f"O005-LEGA-V101-PRJ{i:02d}" for i in range(1, project_count + 1)]
        require(catalog.get("schema_version") == "o005.project-catalog.v1", "Project catalog schema differs")
        require(catalog.get("unit_id") == UNIT_ID, "Project catalog unit differs")
        require(catalog.get("project_count") == project_count, "Project catalog count differs")
        require(catalog.get("project_order") == expected_ids, "Project catalog order differs")
        require([row["project_id"] for row in catalog["projects"]] == expected_ids, "Project catalog ID sequence differs")
        expected_projects = {
            "count": project_count,
            "catalog_path": PROJECT_CATALOG.relative_to(ROOT).as_posix(),
            "catalog_sha256": sha(PROJECT_CATALOG),
            "archives": [
                {
                    "project_id": project_id,
                    "path": archive.relative_to(ROOT).as_posix(),
                    "bytes": archive.stat().st_size,
                    "sha256": sha(archive),
                }
                for project_id, archive in zip(expected_ids, PROJECT_ARCHIVES)
            ],
        }
        require(unit.get("projects") == expected_projects, "Unit project closure differs")
    else:
        require("projects" not in unit, "Unit unexpectedly binds projects")
    return {"segments": len(records), "mastery": len(problems), "projects": project_count}


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
    for href in SPEC.get("footnote_links", []):
        link = soup.find("a", href=href)
        require(link is not None, f"Required footnote link is missing: {href}")
        require(
            link.find_parent("span", class_="reader-footnote") is not None,
            f"Required link escaped its rendered footnote: {href}",
        )
    for href in SPEC.get("descriptive_links", []):
        link = soup.find("a", href=href)
        require(link is not None, f"Required descriptive link is missing: {href}")
        require(
            len(" ".join(link.get_text(" ", strip=True).split())) >= 20,
            f"Link text is not descriptive enough: {href}",
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
    if PROJECT_CATALOG:
        expected_catalog = (root / "data" / PROJECT_CATALOG.name).resolve()
        require(expected_catalog in local_files, "Reader does not expose project catalog")
        packet_links = soup.select("#paket-proyek a[download]")
        require(len(packet_links) == len(PROJECT_ARCHIVES), "Reader project-download count differs")
        expected_hrefs = [
            f"downloads/projects/{archive.name}" for archive in PROJECT_ARCHIVES
        ]
        require([link.get("href") for link in packet_links] == expected_hrefs, "Reader project-download order differs")
        for archive in PROJECT_ARCHIVES:
            packaged = (root / "downloads" / "projects" / archive.name).resolve()
            require(packaged in local_files, f"Reader does not expose project archive: {archive.name}")

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
    if PROJECT_NOTEBOOKS:
        require(len(PROJECT_NOTEBOOKS) == len(PROJECT_ARCHIVES) == 12, "Project notebook/archive count differs")
        catalog = json.loads(PROJECT_CATALOG.read_text(encoding="utf-8"))
        total_cells = 0
        total_code = 0
        lock_payloads: list[bytes] = []
        runner = "import json,sys; n=json.load(open(sys.argv[1],encoding='utf-8')); g={}; [exec(compile(''.join(c['source']), c.get('id','cell'), 'exec'),g) for c in n['cells'] if c.get('cell_type')=='code']"
        env = dict(os.environ)
        env["MPLBACKEND"] = "Agg"
        for ordinal, (row, notebook, archive) in enumerate(
            zip(catalog["projects"], PROJECT_NOTEBOOKS, PROJECT_ARCHIVES), 1
        ):
            project_id = f"O005-LEGA-V101-PRJ{ordinal:02d}"
            require(row["project_id"] == project_id, f"Project {ordinal} identity differs")
            require(row["title_id"] == f"{project_id}-TITLE", f"Project {ordinal} title identity differs")
            require(notebook.is_file() and archive.is_file(), f"Project {ordinal} executable closure is missing")
            require(row["notebook_path"] == notebook.relative_to(ROOT).as_posix(), f"Project {ordinal} notebook path differs")
            require(row["notebook_bytes"] == notebook.stat().st_size and row["notebook_sha256"] == sha(notebook), f"Project {ordinal} notebook identity differs")
            require(row["archive_path"] == archive.relative_to(ROOT).as_posix(), f"Project {ordinal} archive path differs")
            require(row["archive_bytes"] == archive.stat().st_size and row["archive_sha256"] == sha(archive), f"Project {ordinal} archive identity differs")
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            cells = payload.get("cells", [])
            code = [cell for cell in cells if cell.get("cell_type") == "code"]
            require(cells and code, f"Project {ordinal} notebook has no executable closure")
            require(len({cell.get("id") for cell in cells}) == len(cells), f"Project {ordinal} notebook cell IDs differ")
            require(all(not cell.get("outputs") and cell.get("execution_count") is None for cell in code), f"Project {ordinal} notebook is not output-clean")
            lock = notebook.parent / "requirements.lock"
            require(lock.is_file(), f"Project {ordinal} lock is missing")
            lock_payloads.append(lock.read_bytes())
            declared_files = row.get("files", [])
            require(len(declared_files) == 6, f"Project {ordinal} loose-file closure differs")
            declared_names: list[str] = []
            for declared in declared_files:
                loose = ROOT / declared["path"]
                require(loose.parent == notebook.parent and loose.is_file(), f"Project {ordinal} loose path differs")
                require(
                    declared["bytes"] == loose.stat().st_size and declared["sha256"] == sha(loose),
                    f"Project {ordinal} loose-file identity differs",
                )
                declared_names.append(loose.name)
            require(len(set(declared_names)) == 6, f"Project {ordinal} loose-file names differ")
            with zipfile.ZipFile(archive) as packet:
                require(packet.testzip() is None, f"Project {ordinal} archive CRC failure")
                names = packet.namelist()
                require(names == sorted(names), f"Project {ordinal} archive order is not deterministic")
                require(all(not name.startswith(("/", "\\")) and ".." not in Path(name).parts for name in names), f"Project {ordinal} archive path is unsafe")
                required_names = {"README.md", "checks.json", "rubric.md", "provenance.json", "requirements.lock", notebook.name}
                require(set(names) == required_names == set(declared_names), f"Project {ordinal} archive closure is incomplete")
                for info in packet.infolist():
                    require(info.date_time == (1980, 1, 1, 0, 0, 0), f"Project {ordinal} ZIP timestamp differs")
                    require(((info.external_attr >> 16) & 0o777) == 0o644, f"Project {ordinal} ZIP mode differs")
                    loose = notebook.parent / info.filename
                    require(packet.read(info.filename) == loose.read_bytes(), f"Project {ordinal} archived bytes differ")
            if execute:
                subprocess.run([sys.executable, "-c", runner, str(notebook)], check=True, env=env, timeout=120)
            total_cells += len(cells)
            total_code += len(code)
        require(len(set(lock_payloads)) == 1, "Project requirement locks differ")
        lock_text = lock_payloads[0].decode("utf-8")
        for pinned in ("numpy==2.4.4", "scipy==1.17.1", "matplotlib==3.10.9"):
            require(pinned in lock_text, f"Project lock omits {pinned}")
        return {
            "applicable": True,
            "projects": len(PROJECT_NOTEBOOKS),
            "cells": total_cells,
            "code_cells": total_code,
            "executed": execute,
        }
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
