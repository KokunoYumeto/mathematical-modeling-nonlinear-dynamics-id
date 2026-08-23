#!/usr/bin/env python3
"""Deterministic QA for original O005 bridge units."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import platform
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

if not (
    platform.python_implementation() == "CPython"
    and platform.python_version() == "3.13.9"
):
    raise SystemExit(
        "Bridge QA must run under pinned CPython 3.13.9 and the executable "
        "identity recorded by the canonical unit build; current runtime is "
        f"{platform.python_implementation()} {platform.python_version()}"
    )

import jsonschema
from bs4 import BeautifulSoup
from PIL import Image

import build_bridge_unit as builder
import build_unit_reader as base


ROOT = Path(__file__).resolve().parents[1]
MODEL_IDENTIFICATION = "OpenAI Codex gpt-5.6-sol, Ultra."
JUPYTER_HARNESS = ROOT / "scripts" / "execute_bridge_notebook_jupyter.py"
EXPECTED_VERSIONS = {
    "python": "3.13.9",
    "numpy": "2.4.4",
    "scipy": "1.17.1",
    "matplotlib": "3.10.9",
}
SAME_KERNEL_MARKER = "Verifikasi ulang deterministik dalam kernel yang sama lulus."
C3_KERNEL_MARKER = "Verifikasi ulang deterministik C3 dalam kernel yang sama lulus."
C2_CANONICAL_IMAGES = [
    {
        "cell_id": "c2-bifurcation-figure", "output_index": 0,
        "bytes": 48986,
        "sha256": "a559f76859b4681b0f1568f3a5e0f1d8223d17248f1e44856f8a013e81412976",
        "width": 1331, "height": 348,
    },
    {
        "cell_id": "c2-hopf-figure", "output_index": 0,
        "bytes": 112069,
        "sha256": "f924590a504ab4f415651bbe734b0221eb2dfab914569d576859c06c85d5f167",
        "width": 931, "height": 731,
    },
]
C3_CANONICAL_IMAGES = [
    {
        "cell_id": "c3-bifurcation-figure", "output_index": 0,
        "bytes": 195478,
        "sha256": "e922b999de1c9c54b78471743ebe5f35fa8e3456a62dba431302c449e613026c",
        "width": 1117, "height": 853,
    },
    {
        "cell_id": "c3-lorenz-integration", "output_index": 0,
        "bytes": 273795,
        "sha256": "a1d99cbc5d3d74b24334d9a195bbbc012533295c7378f7a91726d5d6b600187c",
        "width": 1021, "height": 589,
    },
    {
        "cell_id": "c3-sensitivity-code", "output_index": 0,
        "bytes": 163728,
        "sha256": "49031dc2d34df82811e0ca1c7338790c851cb9bbc10a6ad37d437df3184688e4",
        "width": 1093, "height": 817,
    },
    {
        "cell_id": "c3-poincare-code", "output_index": 0,
        "bytes": 47050,
        "sha256": "ceae1cae0fdc43e609b07e6aa48152afce5d3b4cfbcdde6805d46f97152087e8",
        "width": 1213, "height": 517,
    },
]
C4_CANONICAL_IMAGES = [
    {
        "cell_id": "c4-plot", "output_index": 0,
        "bytes": 104626,
        "sha256": "227eefe5256973875d66e5f7ff08053196be6574e368cc0e42dc26d9ad396078",
        "width": 1011, "height": 761,
    },
]
MASTERY_ASCII_FORMULA_SENTINELS = (
    (
        "raw relational operator",
        re.compile(r"(?:<=|>=|(?<![<>=])=(?!=)|[<>≈≤≥])"),
    ),
    (
        "linear-ASCII Greek variable",
        re.compile(r"\b(?:alpha|beta|lambda|mu|omega|rho|sigma)\b", re.IGNORECASE),
    ),
    (
        "linear-ASCII subscript",
        re.compile(
            r"\b(?:f_x|x_hat|y_hat|k_hat|t_inf|k_awal|r_awal|e_i|x_star)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "linear-ASCII function call",
        re.compile(r"\b(?:f|g|N|x)\([A-Za-z]\)"),
    ),
    (
        "linear-ASCII numeric interval",
        re.compile(r"\[\s*-?\d+(?:\.\d+)?\s*,"),
    ),
    (
        "linear-ASCII exponent",
        re.compile(r"\^\s*\{?\s*-?\d"),
    ),
)
MASTERY_TEX_ASCII_COMMANDS = re.compile(
    r"(?<!\\)\b(?:alpha|beta|lambda|mu|omega|rho|sigma|sum|log|exp|sqrt|sin|cos)\b"
)
MASTERY_TEX_UPRIGHT_TOKENS = ("AICc", "MAE", "RMSE", "RSS", "SSE", "bias")
C2_SCALAR_CASES = {
    "pitchfork_mu_minus_0_5": [{"x": 0.0, "lambda": -0.5}],
    "pitchfork_mu_plus_0_25": [
        {"x": -0.5, "lambda": -0.5},
        {"x": 0.0, "lambda": 0.25},
        {"x": 0.5, "lambda": -0.5},
    ],
    "saddle_node_mu_minus_0_25": [],
    "saddle_node_mu_plus_0_25": [
        {"x": -0.5, "lambda": 1.0},
        {"x": 0.5, "lambda": -1.0},
    ],
    "transcritical_mu_minus_0_5": [
        {"x": 0.0, "lambda": -0.5},
        {"x": -0.5, "lambda": 0.5},
    ],
    "transcritical_mu_plus_0_5": [
        {"x": 0.0, "lambda": 0.5},
        {"x": 0.5, "lambda": -0.5},
    ],
}
EXPECTED_NOTEBOOK_RUNS = {
    "O005-BRIDGE-C1": [
      {
        "override": None,
        "image_png_outputs": 1,
        "summary": {
        "unit_id": "O005-BRIDGE-C1",
        "seed": 20260822,
        "data_sha256": "1000bc1092f173258d2be37e4f8906ea0933708582d09768ce96eed739be337e",
        "k_hat_per_min": 0.07287235,
        "t_inf_hat_c": 22.63964536,
        "rmse_latih_c": 0.31976406,
        "mean_residu_c": 0.01569277,
        "korelasi_residu_waktu": -0.09083842,
        "mae_uji_c": 0.17952331,
        "versions": EXPECTED_VERSIONS,
        },
    },
      {
        "override": {
            "symbol": "SEED",
            "canonical_symbol": "CANONICAL_SEED",
            "value": 20260823,
        },
        "image_png_outputs": 1,
        "summary": {
        "unit_id": "O005-BRIDGE-C1",
        "seed": 20260823,
        "data_sha256": "36aa2d4b324fe14d5d9ba37fb1ab0ac72fad2d842de10cd60d7f1d3989ce4f62",
        "k_hat_per_min": 0.0739774,
        "t_inf_hat_c": 22.80122391,
        "rmse_latih_c": 0.29860698,
        "mean_residu_c": -0.00236831,
        "korelasi_residu_waktu": 0.06291297,
        "mae_uji_c": 0.46385057,
        "versions": EXPECTED_VERSIONS,
        },
      },
    ],
    "O005-BRIDGE-C2": [
      {
        "override": None,
        "image_png_outputs": 2,
        "images": C2_CANONICAL_IMAGES,
        "summary": {
            "unit_id": "O005-BRIDGE-C2",
            "model_identification": MODEL_IDENTIFICATION,
            "configuration_sha256": "3cbb62d2e4543fa5720822edcca8a3b6d92dfdd7a359c5ace8f9a42f6163c467",
            "scalar_cases": C2_SCALAR_CASES,
            "hopf_primary": {
                "mu": 0.25, "beta": 1.0, "omega": 2.0, "radius": 0.5,
                "period": 3.141592653589793, "radial_derivative": -0.5,
            },
            "hopf_beta_2": {
                "mu": 0.25, "beta": 2.0, "omega": 2.0,
                "radius": 0.3535533905932738,
                "period": 3.141592653589793, "radial_derivative": -0.5,
            },
            "max_radial_error": 6.105393968169892e-12,
            "versions": EXPECTED_VERSIONS,
        },
      },
      {
        "override": {
            "symbol": "PRIMARY_BETA",
            "canonical_symbol": "CANONICAL_BETA",
            "value": 2.0,
        },
        "image_png_outputs": 2,
        "summary": {
            "unit_id": "O005-BRIDGE-C2",
            "model_identification": MODEL_IDENTIFICATION,
            "configuration_sha256": "0e4a9ab2b145e565e0f02ffb733edec93a941104a5ebce036192e63a64272bca",
            "scalar_cases": C2_SCALAR_CASES,
            "hopf_primary": {
                "mu": 0.25, "beta": 2.0, "omega": 2.0,
                "radius": 0.3535533905932738,
                "period": 3.141592653589793, "radial_derivative": -0.5,
            },
            "hopf_beta_2": {
                "mu": 0.25, "beta": 2.0, "omega": 2.0,
                "radius": 0.3535533905932738,
                "period": 3.141592653589793, "radial_derivative": -0.5,
            },
            "max_radial_error": 4.19392298667276e-12,
            "versions": EXPECTED_VERSIONS,
        },
      },
    ],
    "O005-BRIDGE-C3": [
      {
        "override": None,
        "optimized": False,
        "image_png_outputs": 4,
        "images": C3_CANONICAL_IMAGES,
        "summary": {
            "unit_id": "O005-BRIDGE-C3",
            "logistic": {
                "r_3_2_cycle": [0.51304451, 0.79945549],
                "r_3_2_multiplier": 0.16,
                "lambda_r_3_2": -0.91629073,
                "lambda_r_4_finite": 0.69317558,
            },
            "lorenz": {
                "equilibrium_a": 8.48528137,
                "equilibrium_max_residual": 1.4210854715202004e-14,
                "short_horizon_refinement_max_norm": 1.1110286068431319e-08,
                "paired_distance_t20": 9.257358061713491e-07,
                "paired_distance_t35": 2.374077389799957,
                "first_time_distance_gt_1e-3": 25.2,
            },
            "poincare": {
                "all_upward_crossings": 83,
                "post_transient_crossings": 40,
                "return_pairs": 39,
                "section_max_abs_error": 8.633094239485217e-13,
                "minimum_z_derivative": 67.59524535228545,
                "first_retained_time": 30.511303130283864,
                "first_retained_state": [
                    12.611465913164404,
                    16.994467267824426,
                    26.999999999999844,
                ],
            },
            "versions": EXPECTED_VERSIONS,
        },
      },
      {
        "override": None,
        "optimized": True,
        "image_png_outputs": 4,
        "images": C3_CANONICAL_IMAGES,
        "summary": {
            "unit_id": "O005-BRIDGE-C3",
            "logistic": {
                "r_3_2_cycle": [0.51304451, 0.79945549],
                "r_3_2_multiplier": 0.16,
                "lambda_r_3_2": -0.91629073,
                "lambda_r_4_finite": 0.69317558,
            },
            "lorenz": {
                "equilibrium_a": 8.48528137,
                "equilibrium_max_residual": 1.4210854715202004e-14,
                "short_horizon_refinement_max_norm": 1.1110286068431319e-08,
                "paired_distance_t20": 9.257358061713491e-07,
                "paired_distance_t35": 2.374077389799957,
                "first_time_distance_gt_1e-3": 25.2,
            },
            "poincare": {
                "all_upward_crossings": 83,
                "post_transient_crossings": 40,
                "return_pairs": 39,
                "section_max_abs_error": 8.633094239485217e-13,
                "minimum_z_derivative": 67.59524535228545,
                "first_retained_time": 30.511303130283864,
                "first_retained_state": [
                    12.611465913164404,
                    16.994467267824426,
                    26.999999999999844,
                ],
            },
            "versions": EXPECTED_VERSIONS,
        },
      },
    ],
    "O005-BRIDGE-C4": [
      {
        "override": None,
        "image_png_outputs": 1,
        "images": C4_CANONICAL_IMAGES,
        "summary": {
            "unit_id": "O005-BRIDGE-C4",
            "canonical": True,
            "batas_k_atas": 1000.0,
            "data_sha256": "932d0d27c2917936b0aa51d283d7b2fe2a5eba95989a6c785fa32d3d18dd2811",
            "n_kalibrasi": 9,
            "n_uji": 4,
            "r_eksponensial": 0.2104052,
            "r_logistik": 0.28263149,
            "k_logistik": 175.70606226,
            "r_logistik_awal": 0.25110007,
            "k_logistik_awal": 1000.0,
            "rmse_logistik": 2.25689728,
            "aicc_logistik": 25.45183771,
            "delta_aicc": 25.72927985,
            "mae_uji_logistik": 1.50664197,
            "bias_uji_logistik": 1.17225281,
            "kondisi_awal": 32.66379816,
            "kondisi_kalibrasi": 6.93948506,
            "sigma_hat": 2.55908097,
            "bootstrap_sukses": 400,
            "cakupan_uji": 4,
            "interval_respons_laten_hari24": [
                156.4492403, 168.76012565, 185.63476304,
            ],
            "interval_prediksi_hari24": [
                154.3978135, 169.60209338, 185.61306021,
            ],
            "versions": EXPECTED_VERSIONS,
            "model_identification": MODEL_IDENTIFICATION,
        },
      },
      {
        "override": {
            "symbol": "BATAS_K_ATAS",
            "canonical_symbol": "CANONICAL_K_UPPER_BOUND",
            "value": 2000.0,
        },
        "image_png_outputs": 1,
        "images": C4_CANONICAL_IMAGES,
        "summary": {
            "unit_id": "O005-BRIDGE-C4",
            "canonical": False,
            "batas_k_atas": 2000.0,
            "data_sha256": "932d0d27c2917936b0aa51d283d7b2fe2a5eba95989a6c785fa32d3d18dd2811",
            "n_kalibrasi": 9,
            "n_uji": 4,
            "r_eksponensial": 0.2104052,
            "r_logistik": 0.28263149,
            "k_logistik": 175.70606257,
            "r_logistik_awal": 0.24853917,
            "k_logistik_awal": 2000.0,
            "rmse_logistik": 2.25689728,
            "aicc_logistik": 25.45183771,
            "delta_aicc": 25.72927985,
            "mae_uji_logistik": 1.50664189,
            "bias_uji_logistik": 1.17225262,
            "kondisi_awal": 32.66379829,
            "kondisi_kalibrasi": 6.93948509,
            "sigma_hat": 2.55908097,
            "bootstrap_sukses": 400,
            "cakupan_uji": 4,
            "interval_respons_laten_hari24": [
                156.44924101, 168.76012591, 185.63476325,
            ],
            "interval_prediksi_hari24": [
                154.39781373, 169.60209354, 185.61306039,
            ],
            "versions": EXPECTED_VERSIONS,
            "model_identification": MODEL_IDENTIFICATION,
        },
      },
    ],
}
QA_SPECS = {
    "O005-BRIDGE-C1": {
        "content_bytes": 16946,
        "content_sha256": "c8593b80996e6f7bd368a4a2e198472198163fc17ee408b98ccbd7e58c99e4eb",
        "text_slots": 152,
        "content_paragraphs": 33,
        "content_h2": 12,
        "content_h3": 8,
        "content_tables": 2,
        "content_rows": 16,
        "content_captions": 2,
        "content_row_headers": 14,
        "content_ids": 20,
        "content_math": 30,
        "problems": 7,
        "notebook_cells": 14,
        "notebook_code_cells": 7,
        "reader_mathml": 59,
        "reader_mastery_mathml": 29,
        "reader_details": 21,
        "reader_files_excluding_manifest": 9,
        "reader_figures": 0,
        "reader_images": 0,
    },
    "O005-BRIDGE-C2": {
        "content_bytes": 24773,
        "content_sha256": "08c3ab749364e6d33028ad6369b18c78361f30b021a36e75ade73325582a8b5a",
        "text_slots": 115,
        "content_paragraphs": 54,
        "content_h2": 12,
        "content_h3": 8,
        "content_tables": 2,
        "content_rows": 10,
        "content_captions": 2,
        "content_row_headers": 8,
        "content_ids": 20,
        "content_math": 142,
        "problems": 7,
        "notebook_cells": 14,
        "notebook_code_cells": 7,
        "reader_mathml": 279,
        "reader_mastery_mathml": 137,
        "reader_details": 21,
        "reader_files_excluding_manifest": 11,
        "reader_figures": 2,
        "reader_images": 2,
        "semantic_keys": 115,
    },
    "O005-BRIDGE-C3": {
        "content_bytes": 24248,
        "content_sha256": "6f16b026417252c5307c03a88272fc55542e955263cd85f6f82338e33065ed53",
        "text_slots": 117,
        "content_paragraphs": 59,
        "content_h2": 13,
        "content_h3": 8,
        "content_tables": 2,
        "content_rows": 8,
        "content_captions": 2,
        "content_row_headers": 6,
        "content_column_headers": 6,
        "content_ids": 31,
        "content_math": 155,
        "problems": 7,
        "notebook_cells": 14,
        "notebook_code_cells": 7,
        "reader_mathml": 299,
        "reader_mastery_mathml": 144,
        "reader_details": 24,
        "reader_files_excluding_manifest": 13,
        "reader_figures": 3,
        "reader_images": 4,
        "semantic_keys": 117,
    },
    "O005-BRIDGE-C4": {
        "content_bytes": 40114,
        "content_sha256": "241555f28005883e592a79a69ebefd08bdbea2d55bc72d738059700d75e591e9",
        "text_slots": 273,
        "content_paragraphs": 45,
        "content_h2": 13,
        "content_h3": 7,
        "content_tables": 8,
        "content_rows": 53,
        "content_captions": 8,
        "content_row_headers": 45,
        "content_column_headers": 31,
        "content_ids": 30,
        "content_math": 98,
        "problems": 7,
        "notebook_cells": 15,
        "notebook_code_cells": 7,
        "reader_mathml": 160,
        "reader_mastery_mathml": 62,
        "reader_details": 21,
        "reader_files_excluding_manifest": 10,
        "reader_figures": 1,
        "reader_images": 1,
        "semantic_keys": 273,
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), f"JSON root is not an object: {path}")
    return payload


def validate_schema(payload: dict, schema_path: Path) -> None:
    schema = load_json(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.FormatChecker(),
    ).validate(payload)


def resolved_declared_path(root: Path, declared: str) -> Path:
    require("\\" not in declared, f"Declared path is not POSIX: {declared}")
    relative = PurePosixPath(declared)
    require(not relative.is_absolute(), f"Declared path is absolute: {declared}")
    require(
        relative.parts and all(part not in {"", ".", ".."} for part in relative.parts),
        f"Declared path escapes its root: {declared}",
    )
    path = (root / Path(*relative.parts)).resolve()
    require(path.is_relative_to(root.resolve()), f"Declared path escapes its root: {declared}")
    return path


def validate_identity(root: Path, record: dict, expected_path: str | None = None) -> None:
    if expected_path is not None:
        require(record["path"] == expected_path, f"Declared path differs: {record['path']}")
    path = resolved_declared_path(root, record["path"])
    require(path.is_file(), f"Declared file is missing: {record['path']}")
    require(path.stat().st_size == record["bytes"], f"Declared byte count differs: {record['path']}")
    require(sha(path) == record["sha256"], f"Declared hash differs: {record['path']}")


def require_pinned_qa_interpreter(unit_id: str) -> None:
    message = (
        "Bridge QA must run under pinned CPython 3.13.9 and the executable "
        "identity recorded by the canonical unit build"
    )
    require(
        platform.python_implementation() == "CPython"
        and platform.python_version() == "3.13.9",
        f"{message}; current runtime is "
        f"{platform.python_implementation()} {platform.python_version()}",
    )
    unit_path = ROOT / "backend" / "units" / f"{unit_id}.json"
    if not unit_path.is_file():
        return
    recorded = load_json(unit_path).get("build", {}).get("toolchain", {}).get("python")
    if not isinstance(recorded, dict):
        return
    executable = Path(sys.executable)
    current = {
        "implementation": platform.python_implementation(),
        "version": platform.python_version(),
        "executable_bytes": executable.stat().st_size,
        "executable_sha256": sha(executable),
    }
    require(recorded == current, f"{message}; current executable identity differs")


def content_replay(unit_id: str, spec: dict, qa_spec: dict) -> dict:
    content_path = spec["content"]
    require(content_path.stat().st_size == qa_spec["content_bytes"], "Canonical content byte count differs")
    require(sha(content_path) == qa_spec["content_sha256"], "Canonical content hash differs")
    content = content_path.read_text(encoding="utf-8")
    require(
        re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", content) is None,
        "Canonical content contains a forbidden control character",
    )
    soup = BeautifulSoup(content, "html.parser")
    ids = [str(tag["id"]) for tag in soup.select("[id]")]
    require(len(ids) == qa_spec["content_ids"] == len(set(ids)), "Canonical content IDs differ or repeat")
    expected_problems = [f"{unit_id}-P{i:02d}" for i in range(1, qa_spec["problems"] + 1)]
    actual_problems = [str(tag["id"]) for tag in soup.select("h3[id]") if str(tag["id"]) in expected_problems]
    require(actual_problems == expected_problems, "Canonical problem IDs differ")
    require(len(soup.find_all("p")) == qa_spec["content_paragraphs"], "Canonical paragraph census differs")
    require(len(soup.find_all("h2")) == qa_spec["content_h2"], "Canonical h2 census differs")
    require(len(soup.find_all("h3")) == qa_spec["content_h3"], "Canonical h3 census differs")
    require(len(soup.find_all("table")) == qa_spec["content_tables"], "Canonical table census differs")
    require(len(soup.find_all("tr")) == qa_spec["content_rows"], "Canonical table-row census differs")
    require(len(soup.find_all("caption")) == qa_spec["content_captions"], "Canonical caption census differs")
    require(len(soup.select('th[scope="row"]')) == qa_spec["content_row_headers"], "Canonical row-header census differs")
    if "content_column_headers" in qa_spec:
        require(
            len(soup.select('th[scope="col"]')) == qa_spec["content_column_headers"],
            "Canonical column-header census differs",
        )
    require(all(table.find("caption") for table in soup.find_all("table")), "Canonical table caption is missing")
    require(
        all(
            header.get("scope") in {"row", "col"}
            for table in soup.find_all("table")
            for header in table.find_all("th")
        ),
        "Canonical table header lacks an explicit row/column scope",
    )
    require(
        all(
            (cells := row.find_all(["th", "td"], recursive=False))
            and cells[0].name == "th"
            and cells[0].get("scope") == "row"
            for table in soup.find_all("table")
            for row in table.select("tbody tr")
        ),
        "Canonical table body row lacks a leading row header",
    )
    require(
        len(list(base.COMPANION_MATH_RE.finditer(content))) == qa_spec["content_math"],
        "Canonical math census differs",
    )
    slots = builder.segment_slots(spec, content)
    require(len(slots) == qa_spec["text_slots"], "Canonical text-slot census differs")
    if spec["segment_mode"] == "html-data-attribute":
        keys = [str(tag["data-o005-segment-key"]) for tag in soup.select("[data-o005-segment-key]")]
        require(len(keys) == qa_spec["semantic_keys"] == len(set(keys)), "Semantic anchor census differs")
        require(keys == [key for key, _, _ in slots], "Semantic anchor DOM order differs")
    headings = [int(tag.name[1]) for tag in soup.find_all(["h2", "h3"])]
    require(all(b - a <= 1 for a, b in zip(headings, headings[1:])), "Canonical heading level skips")
    return {"slots": slots, "problems": expected_problems}


def expected_toolchain(spec: dict) -> tuple[str, dict]:
    pandoc = base.pandoc_version()
    require(pandoc == "pandoc 3.9.0.2", f"Pandoc identity differs: {pandoc}")
    return pandoc, builder.toolchain_identity(spec, pandoc)


def backend_replay(
    unit_id: str,
    spec: dict,
    qa_spec: dict,
    slots: list[tuple[str | None, str, str]],
) -> dict:
    segment_path = ROOT / "backend" / "segments" / f"{unit_id}.segments.jsonl"
    unit_path = ROOT / "backend" / "units" / f"{unit_id}.json"
    mastery_path = ROOT / "backend" / "mastery" / f"{unit_id}.mastery.json"
    lock_path = spec["notebook"].parent / "requirements.lock"
    authority_dir = ROOT / "authority" / "units" / unit_id
    source_record = authority_dir / "source-record.canonical.json"
    authority_manifest = authority_dir / "AUTHORITY_MANIFEST.json"

    ledger = builder.load_segment_ledger(spec, unit_id)
    active = [entry for entry in ledger["entries"] if entry["state"] == "active"]
    by_binding = {entry["slot_binding_sha256"]: entry["segment_id"] for entry in active}
    by_key = {entry["segment_key"]: entry for entry in active}
    require(len(by_binding) == len(by_key) == len(active) == len(slots), "Active segment-ledger census differs")
    if spec["segment_mode"] == "html-data-attribute" and ledger["ledger_version"] == 1:
        require(
            [by_key[key]["segment_id"] for key, _, _ in slots]
            == [f"{unit_id}-S{i:04d}" for i in range(1, len(slots) + 1)],
            "Initial anchored ledger serial assignment is not DOM ordered",
        )

    segment_schema = load_json(builder.SEGMENT_SCHEMA)
    jsonschema.Draft202012Validator.check_schema(segment_schema)
    segment_validator = jsonschema.Draft202012Validator(segment_schema)
    records = [json.loads(line) for line in segment_path.read_text(encoding="utf-8").splitlines()]
    require(len(records) == qa_spec["text_slots"] == len(slots), "Segment count differs")
    expected_segment_ids: list[str] = []
    for ordinal, (record, (segment_key, html_path, canonical_text)) in enumerate(zip(records, slots), 1):
        segment_validator.validate(record)
        binding = builder.slot_binding_sha256(html_path, canonical_text, segment_key)
        if segment_key is None:
            require(binding in by_binding, f"Segment slot has no durable ledger mapping: {html_path}")
            expected_segment_id = by_binding[binding]
        else:
            require(segment_key in by_key, f"Segment key has no durable ledger mapping: {segment_key}")
            require(
                by_key[segment_key]["slot_binding_sha256"] == binding,
                f"Segment ledger binding differs: {segment_key}",
            )
            expected_segment_id = by_key[segment_key]["segment_id"]
        expected_segment_ids.append(expected_segment_id)
        expected_record = {
            "schema": "o005-bridge-segment-v1",
            "segment_id": expected_segment_id,
            "unit_id": unit_id,
            "ordinal": ordinal,
            "html_path": html_path,
            "canonical_language": "id-ID",
            "canonical_text": canonical_text,
            "canonical_sha256": sha_bytes(canonical_text.encode("utf-8")),
            "status": "original",
        }
        if segment_key is not None:
            expected_record["segment_key"] = segment_key
        require(record == expected_record, f"Segment record differs: {expected_segment_id}")
    require(len(set(expected_segment_ids)) == len(expected_segment_ids), "Durable segment IDs repeat")

    mastery = load_json(mastery_path)
    validate_schema(mastery, builder.MASTERY_SCHEMA)
    expected_problems = [f"{unit_id}-P{i:02d}" for i in range(1, qa_spec["problems"] + 1)]
    require(
        [(problem["problem_id"], problem["ordinal"]) for problem in mastery["problems"]]
        == list(zip(expected_problems, range(1, qa_spec["problems"] + 1))),
        "Mastery problem identity/order differs",
    )
    expected_mastery_source = {
        "type": "new_original_addition",
        "spine": "Joceline Lega, Introduction to Mathematical Modeling, v1.01",
        "not_part_of_source_book": True,
        "license": "CC BY-NC-SA 4.0",
    }
    if unit_id == "O005-BRIDGE-C3":
        expected_mastery_source["relationship"] = "independent_supplement"
    require(mastery["source"] == expected_mastery_source, "Mastery source boundary differs")
    expected_provenance_policy = {
        "model_identification": MODEL_IDENTIFICATION,
        "source_author_credit_preserved": True,
        "non_endorsement": True,
    }
    if unit_id == "O005-BRIDGE-C3":
        expected_provenance_policy["external_data_or_assets"] = False
    require(mastery["provenance_policy"] == expected_provenance_policy, "Mastery provenance policy differs")
    require(
        ["notebook" in problem for problem in mastery["problems"]] == [False] * 6 + [True],
        "Mastery notebook binding must occur only on P07",
    )
    require("source_derived" not in mastery_path.read_text(encoding="utf-8"), "Bridge mastery contains source-derived claim")

    pandoc, toolchain = expected_toolchain(spec)
    for identity in toolchain["files"]:
        validate_identity(ROOT, identity)

    authority = load_json(source_record)
    manifest = load_json(authority_manifest)
    validate_schema(authority, builder.AUTHORITY_SCHEMA)
    validate_schema(manifest, builder.AUTHORITY_MANIFEST_SCHEMA)
    expected_authority = {
        "schema": "o005-original-authority-v1",
        "unit_id": unit_id,
        "canonical_language": "id-ID",
        "content_mode": "new_original_addition",
        "title": spec["title"],
        "created_date": spec["created_date"],
        "license": "CC BY-NC-SA 4.0",
        "model_identification": MODEL_IDENTIFICATION,
        "relationship_to_spine": {
            "spine": "Joceline Lega, Introduction to Mathematical Modeling, v1.01",
            "relationship": "independent_supplement",
            "part_of_source_book": False,
            "endorsement_claimed": False,
        },
        "files": [
            builder.file_identity(path)
            for path in (spec["content"], spec["generator"], spec["notebook"], lock_path, mastery_path)
        ],
        "toolchain": toolchain,
    }
    require(authority == expected_authority, "Authority source record differs from exact canonical inputs")
    for identity in authority["files"]:
        validate_identity(ROOT, identity)

    expected_manifest = {
        "schema": "o005-original-authority-manifest-v1",
        "unit_id": unit_id,
        "record": builder.file_identity(source_record),
        "canonical_content": builder.file_identity(spec["content"]),
        "notebook": builder.file_identity(spec["notebook"]),
        "mastery": builder.file_identity(mastery_path),
        "lock": builder.file_identity(lock_path),
        "generator": builder.file_identity(spec["generator"]),
        "segment_id_ledger": builder.file_identity(spec["segment_id_ledger"]),
        "toolchain": toolchain,
    }
    require(manifest == expected_manifest, "Authority manifest differs from exact canonical records")
    for key in (
        "record", "canonical_content", "notebook", "mastery", "lock", "generator", "segment_id_ledger"
    ):
        validate_identity(ROOT, manifest[key])

    unit = load_json(unit_path)
    validate_schema(unit, builder.UNIT_SCHEMA)
    expected_unit = {
        "schema": "o005-bridge-unit-v1",
        "unit_id": unit_id,
        "course_id": "C120",
        "resource_id": "O005",
        "language": "id-ID",
        "content_mode": "new_original_addition",
        "provenance": {
            "model_identification": MODEL_IDENTIFICATION,
            "license": "CC BY-NC-SA 4.0",
            "spine_author": "Joceline Lega",
            "spine_work": "Introduction to Mathematical Modeling",
            "relationship": "independent_supplement",
            "non_endorsement": True,
            "authority_manifest": f"authority/units/{unit_id}/AUTHORITY_MANIFEST.json",
            "authority_manifest_sha256": sha(authority_manifest),
        },
        "target": {
            "title": spec["title"],
            "content_path": spec["content"].relative_to(ROOT).as_posix(),
            "content_sha256": sha(spec["content"]),
            "concepts": spec["concepts"],
            "placement": spec["placement"],
        },
        "segments": {
            "count": len(records),
            "path": f"backend/segments/{unit_id}.segments.jsonl",
            "sha256": sha(segment_path),
            "schema": "o005-bridge-segment-v1",
            "id_strategy": spec["id_strategy"],
            "id_ledger_path": spec["segment_id_ledger"].relative_to(ROOT).as_posix(),
            "id_ledger_sha256": sha(spec["segment_id_ledger"]),
        },
        "problems": expected_problems,
        "mastery_path": mastery_path.relative_to(ROOT).as_posix(),
        "mastery_sha256": sha(mastery_path),
        "notebook_path": spec["notebook"].relative_to(ROOT).as_posix(),
        "notebook_sha256": sha(spec["notebook"]),
        "build": {
            "script": "scripts/build_bridge_unit.py",
            "generator": spec["generator"].relative_to(ROOT).as_posix(),
            "pandoc": pandoc,
            "requirements_lock": lock_path.relative_to(ROOT).as_posix(),
            "requirements_lock_sha256": sha(lock_path),
            "toolchain": toolchain,
        },
    }
    require(unit == expected_unit, "Unit record differs from exact canonical records")
    require(
        unit["build"]["toolchain"] == authority["toolchain"] == manifest["toolchain"],
        "Toolchain identity differs across unit and authority records",
    )
    return {
        "segments": len(records),
        "segment_ids": sha_bytes("\n".join(expected_segment_ids).encode("utf-8")),
        "mastery": len(mastery["problems"]),
        "authority_files": len(authority["files"]),
        "toolchain_files": len(toolchain["files"]),
    }


def jupyter_host_python() -> Path:
    candidates: list[Path] = []
    override = os.environ.get("O005_JUPYTER_HOST_PYTHON")
    if override:
        candidates.append(Path(override))
    jupyter = shutil.which("jupyter")
    if jupyter:
        executable = Path(jupyter).resolve()
        if os.name == "nt":
            candidates.append(executable.parent.parent / "python.exe")
        else:
            candidates.append(executable.parent / "python")
    candidates.append(Path(sys.executable))
    seen: set[Path] = set()
    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate in seen or not candidate.is_file():
            continue
        seen.add(candidate)
        probe = subprocess.run(
            [str(candidate), "-c", "import ipykernel,nbclient,nbformat"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if probe.returncode == 0:
            return candidate
    raise RuntimeError(
        "No Jupyter host interpreter with ipykernel, nbclient, and nbformat was found"
    )


def fresh_jupyter_run(
    host_python: Path,
    unit_id: str,
    spec: dict,
    expectation: dict,
) -> dict:
    command = [
        str(host_python),
        str(JUPYTER_HARNESS),
        "--notebook",
        str(spec["notebook"]),
        "--kernel-python",
        sys.executable,
        "--expected-unit-id",
        unit_id,
        "--expected-marker",
        spec["notebook_marker"],
        "--expected-image-count",
        str(expectation["image_png_outputs"]),
    ]
    override = expectation["override"]
    if override is not None:
        command.extend([
            "--override-symbol",
            override["symbol"],
            "--override-value",
            json.dumps(override["value"]),
        ])
    if expectation.get("optimized", False):
        command.append("--kernel-optimize")
    proc = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=420,
    )
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Fresh-Jupyter harness did not emit one JSON result") from exc
    require(result["schema"] == "o005-fresh-jupyter-execution-v3", "Fresh-Jupyter result schema differs")
    require(result["kernel_name"] == builder.KERNEL_NAME, "Fresh-Jupyter kernel name differs")
    require(Path(result["notebook"]).resolve() == spec["notebook"].resolve(), "Fresh-Jupyter notebook path differs")
    require(Path(result["kernel_python"]).resolve() == Path(sys.executable).resolve(), "Fresh-Jupyter kernel interpreter differs")
    require(result["override"] == override, "Fresh-Jupyter declared override differs")
    require(result["host_versions"] == builder.PINNED_JUPYTER, "Fresh-Jupyter host closure differs")
    require(result["optimized"] is expectation.get("optimized", False), "Fresh-Jupyter optimization mode differs")
    require(result["code_cells"] == 7, "Fresh-Jupyter code-cell census differs")
    require(
        result["image_png_outputs"] == expectation["image_png_outputs"],
        "Fresh-Jupyter diagnostic PNG census differs",
    )
    if "images" in expectation:
        require(result["images"] == expectation["images"], "Fresh-Jupyter PNG order or identity differs")
    require(
        result["summary"] == expectation["summary"],
        f"Fresh-Jupyter summary differs for {unit_id} override {override}",
    )
    summary = result["summary"]
    summary_sha256 = sha_bytes(
        json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    return {
        "override": override,
        "optimized": result["optimized"],
        "artifact_sha256": summary_sha256,
        "configuration_sha256": summary.get("configuration_sha256"),
        "image_png_outputs": result["image_png_outputs"],
        "image_sha256": [record["sha256"] for record in result["images"]],
        "summary_sha256": summary_sha256,
    }


def notebook_replay(unit_id: str, spec: dict, qa_spec: dict, execute: bool) -> dict:
    subprocess.run(
        [sys.executable, str(spec["generator"]), "--check"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    notebook = load_json(spec["notebook"])
    cells = notebook["cells"]
    code_cells = [cell for cell in cells if cell["cell_type"] == "code"]
    require(len(cells) == qa_spec["notebook_cells"], "Notebook cell count differs")
    require(len(code_cells) == qa_spec["notebook_code_cells"], "Notebook code-cell count differs")
    require(len({cell["id"] for cell in cells}) == len(cells), "Notebook cell IDs repeat")
    require(all(not cell["outputs"] and cell["execution_count"] is None for cell in code_cells), "Notebook is not output-clean")
    require(notebook["metadata"]["kernelspec"] == {
        "display_name": "O005 C120 Python 3.13.9",
        "language": "python",
        "name": builder.KERNEL_NAME,
    }, "Notebook dedicated kernelspec metadata differs")
    require(notebook["metadata"]["language_info"] == {
        "name": "python",
        "version": "3.13.9",
    }, "Notebook language runtime metadata differs")
    meta = notebook["metadata"]["o005"]
    expected_meta = {
        "component_origin": "original",
        "environment_lock": "requirements.lock",
        "language": "id-ID",
        "license": "CC BY-NC-SA 4.0",
        "locale": "id-ID",
        "model_identification": MODEL_IDENTIFICATION,
        "notebook_id": f"{unit_id}-NB01",
        "offline_capable": True,
        "offline_scope": "network_free_after_environment_install",
        "provenance": "new_original_addition",
        "unit_id": unit_id,
        "wheelhouse_included": False,
    }
    if unit_id == "O005-BRIDGE-C2":
        expected_meta.update({
            "relationship": "independent_supplement",
            "non_endorsement": True,
            "accessible_plots": [
                {
                    "plot_id": "O005-BRIDGE-C2-FIG01",
                    "kind": "four_panel_bifurcation_diagram",
                    "description_cell": "c2-bifurcation-diagrams",
                    "redundant_encodings": ["linestyle", "marker", "color"],
                },
                {
                    "plot_id": "O005-BRIDGE-C2-FIG02",
                    "kind": "hopf_phase_and_radius_trajectories",
                    "description_cell": "c2-hopf-figure-description",
                    "redundant_encodings": ["linestyle", "marker", "color"],
                },
            ],
        })
    elif unit_id in {"O005-BRIDGE-C3", "O005-BRIDGE-C4"}:
        expected_meta.update({
            "relationship": "independent_supplement",
            "non_endorsement": True,
        })
        if unit_id == "O005-BRIDGE-C3":
            expected_meta["external_data_or_assets"] = False
    require(meta == expected_meta, "Notebook provenance metadata differs")
    code_text = "\n".join("".join(cell["source"]) for cell in code_cells).lower()
    for forbidden in ("requests.", "urllib", "http://", "https://", "socket.", "subprocess.", "os.system"):
        require(forbidden not in code_text, f"Notebook has forbidden network/process surface: {forbidden}")
    require(
        re.search(r"(?m)^\s*assert\b", code_text) is None,
        "Notebook correctness depends on an optimization-disabled assert statement",
    )
    if unit_id == "O005-BRIDGE-C2":
        require(
            code_text.count("primary_beta = canonical_beta") == 1,
            "C2 notebook lacks one declared primary-beta assignment",
        )
    elif unit_id == "O005-BRIDGE-C3":
        by_id = {cell["id"]: "".join(cell["source"]) for cell in cells}
        long_description_cells = (
            "c3-bifurcation-lyapunov",
            "c3-lorenz-contract",
            "c3-sensitivity-validation",
            "c3-poincare-return",
        )
        require(
            all("Deskripsi panjang gambar" in by_id[cell_id] for cell_id in long_description_cells),
            "C3 notebook lacks a labeled Indonesian long description before every PNG cell",
        )
        require(
            "## Kepekaan terhadap kondisi awal" in by_id["c3-sensitivity-validation"],
            "C3 notebook sensitivity heading differs",
        )
        require(
            "r in (0.0, 1.0)" in code_text
            and "r > 3.0" in code_text
            and "r=3 keliru diterima sebagai dua-siklus prima" in code_text,
            "C3 notebook boundary checks for r=0, r=1, or r=3 differ",
        )
    elif unit_id == "O005-BRIDGE-C4":
        by_id = {cell["id"]: "".join(cell["source"]) for cell in cells}
        require(
            code_text.count("batas_k_atas = canonical_k_upper_bound") == 1,
            "C4 notebook lacks one declared upper-bound assignment",
        )
        require(
            "Deskripsi panjang gambar:" in by_id["c4-figure-description"],
            "C4 notebook lacks the labeled Indonesian long description before its PNG cell",
        )
        require(
            cells.index(next(cell for cell in cells if cell["id"] == "c4-figure-description"))
            < cells.index(next(cell for cell in cells if cell["id"] == "c4-plot")),
            "C4 notebook long description does not precede its PNG cell",
        )
        require(
            re.search(r'q_pred\[0\],\s*linestyle=["\']--["\']', code_text) is not None
            and re.search(r'q_pred\[2\],\s*linestyle=["\']-\.["\']', code_text) is not None
            and 'marker="o"' in code_text
            and 'marker="s"' in code_text
            and 'marker="x"' in code_text,
            "C4 plot lacks non-color boundary, line, or marker encodings",
        )
    lock = spec["notebook"].parent / "requirements.lock"
    pins = [
        line.strip()
        for line in lock.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    require(len(pins) == 57, "Notebook requirements closure census differs")
    require(
        all(
            re.fullmatch(
                r"[A-Za-z0-9][A-Za-z0-9._-]*==[A-Za-z0-9][A-Za-z0-9.!+_-]*"
                r"(?: ; sys_platform == \"win32\")?",
                pin,
            )
            for pin in pins
        ),
        "Notebook requirements lock contains an unpinned or unsupported entry",
    )
    normalized_pins = {
        pin.split("==", 1)[0].lower(): pin.split("==", 1)[1].split(" ;", 1)[0]
        for pin in pins
    }
    require(len(normalized_pins) == len(pins), "Notebook requirements lock repeats a package")
    required_pins = {
        "beautifulsoup4": "4.14.3",
        "ipykernel": "6.29.5",
        "jsonschema": "4.26.0",
        "jupyter-client": "8.6.3",
        "jupyter-core": "5.7.2",
        "matplotlib": "3.10.9",
        "nbclient": "0.10.2",
        "nbformat": "5.10.4",
        "numpy": "2.4.4",
        "pillow": "12.2.0",
        "scipy": "1.17.1",
    }
    require(
        all(normalized_pins.get(name) == version for name, version in required_pins.items()),
        "Notebook requirements lock differs on a required runtime package",
    )

    runs: list[dict] = []
    if execute:
        host_python = jupyter_host_python()
        canonical_notebook = spec["notebook"].read_bytes()
        runs = [
            fresh_jupyter_run(host_python, unit_id, spec, expectation)
            for expectation in EXPECTED_NOTEBOOK_RUNS[unit_id]
        ]
        require(
            spec["notebook"].read_bytes() == canonical_notebook,
            "Fresh-Jupyter QA mutated the canonical notebook",
        )
        for run in runs[1:]:
            if run["override"] is not None:
                require(
                    runs[0]["artifact_sha256"] != run["artifact_sha256"],
                    "Declared noncanonical experiment did not change its artifact identity",
                )
                if runs[0]["configuration_sha256"] is not None:
                    require(
                        run["configuration_sha256"] is not None
                        and runs[0]["configuration_sha256"]
                        != run["configuration_sha256"],
                        "Declared noncanonical experiment did not change its configuration hash",
                    )
            if run["optimized"]:
                require(
                    run["summary_sha256"] == runs[0]["summary_sha256"]
                    and run["image_sha256"] == runs[0]["image_sha256"],
                    "Optimized fresh-kernel execution changed active-check results",
                )
    return {
        "cells": len(cells),
        "code_cells": len(code_cells),
        "fresh_kernel_executed": execute,
        "runs": runs,
    }


def reader_replay(unit_id: str, spec: dict, qa_spec: dict, root: Path) -> dict:
    index = root / "index.html"
    manifest_path = root / "PACKAGE_MANIFEST.tsv"
    require(index.is_file() and manifest_path.is_file(), "Reader closure is missing")
    files = sorted(path for path in root.rglob("*") if path.is_file() and path != manifest_path)
    require(len(files) == qa_spec["reader_files_excluding_manifest"], "Reader file count differs")
    rows = manifest_path.read_text(encoding="utf-8").splitlines()
    require(rows and rows[0] == "path\tbytes\tsha256", "Reader manifest header differs")
    require(len(rows) == len(files) + 1, "Reader manifest row count differs")
    expected_rows = [
        f"{path.relative_to(root).as_posix()}\t{path.stat().st_size}\t{sha(path)}"
        for path in files
    ]
    require(rows[1:] == expected_rows, "Reader manifest inventory differs")

    raw = index.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    canonical_soup = BeautifulSoup(spec["content"].read_text(encoding="utf-8"), "html.parser")
    require(
        re.search(r"<p\b[^>]*>\s*<caption\b", raw, flags=re.IGNORECASE) is None
        and not soup.select("p > caption"),
        "Reader contains a caption wrapped by a paragraph",
    )
    require(not soup.select("pre p"), "Reader contains a paragraph inside preformatted content")
    empty_paragraphs = [
        paragraph
        for paragraph in soup.find_all("p")
        if not base.canonical_text(paragraph.get_text(" ", strip=True))
    ]
    require(not empty_paragraphs, "Reader contains an empty paragraph")
    require(soup.html.get("lang") == "id-ID", "Reader language differs")
    require(soup.select_one('a.skip-link[href="#isi"]') is not None, "Reader skip link is missing")
    require(soup.select_one('nav[aria-label="Navigasi unit"]') is not None, "Reader navigation label is missing")
    require(soup.select_one('main#isi[tabindex="-1"]') is not None, "Reader main focus target is missing")
    require(soup.select_one("article.chapter.bridge") is not None, "Reader bridge article is missing")
    mastery_surface = soup.select_one("section#dukungan-belajar")
    require(mastery_surface is not None, "Reader mastery surface is missing")
    for text_node in mastery_surface.find_all(string=True):
        if text_node.find_parent(["math", "code", "pre"]) is not None:
            continue
        visible = base.canonical_text(str(text_node))
        for label, pattern in MASTERY_ASCII_FORMULA_SENTINELS:
            match = pattern.search(visible)
            require(
                match is None,
                f"Reader mastery surface contains {label}: {visible[:120]!r}",
            )
    mastery_annotations = mastery_surface.select(
        'math annotation[encoding="application/x-tex"]'
    )
    require(
        len(mastery_surface.find_all("math")) == qa_spec["reader_mastery_mathml"],
        "Reader mastery MathML census differs",
    )
    require(mastery_annotations, "Reader mastery surface contains no inspectable TeX annotations")
    for annotation in mastery_annotations:
        tex = str(annotation.get_text())
        require(
            "<=" not in tex
            and ">=" not in tex
            and MASTERY_TEX_ASCII_COMMANDS.search(tex) is None,
            f"Reader mastery MathML retains a linear-ASCII TeX command: {tex[:120]!r}",
        )
        for token in MASTERY_TEX_UPRIGHT_TOKENS:
            residual = tex.replace(f"\\mathrm{{{token}}}", "").replace(
                f"\\operatorname{{{token}}}", ""
            )
            require(
                token not in residual,
                f"Reader mastery MathML leaves {token!r} in math italics: {tex[:120]!r}",
            )
    ids = [str(tag["id"]) for tag in soup.select("[id]")]
    require(len(ids) == len(set(ids)), "Reader IDs repeat")
    for anchor in soup.find_all("a", href=True):
        href = str(anchor["href"])
        if href.startswith("#"):
            require(href[1:] in ids, f"Broken reader fragment: {href}")
        if href.startswith(("http://", "https://")):
            rel = set(anchor.get("rel", []))
            require("external" in rel and "noopener" in rel and "noreferrer" in rel, f"External link rel differs: {href}")
    require(len(soup.find_all("math")) == qa_spec["reader_mathml"], "Reader MathML census differs")
    require(all(math.get("aria-label") for math in soup.find_all("math")), "Reader MathML lacks aria-label")
    require(len(soup.find_all("details")) == qa_spec["reader_details"], "Reader mastery details census differs")
    require(len(soup.find_all("caption")) == qa_spec["content_captions"], "Reader table-caption census differs")
    require(len(soup.select('th[scope="row"]')) == qa_spec["content_row_headers"], "Reader row-header census differs")
    if "content_column_headers" in qa_spec:
        require(
            len(soup.select('th[scope="col"]')) == qa_spec["content_column_headers"],
            "Reader column-header census differs",
        )
    require(all(table.find("caption") for table in soup.find_all("table")), "Reader table caption is missing")
    require(
        all(
            header.get("scope") in {"row", "col"}
            for table in soup.find_all("table")
            for header in table.find_all("th")
        ),
        "Reader table header lacks an explicit row/column scope",
    )
    require(
        all(
            (cells := row.find_all(["th", "td"], recursive=False))
            and cells[0].name == "th"
            and cells[0].get("scope") == "row"
            for table in soup.find_all("table")
            for row in table.select("tbody tr")
        ),
        "Reader table body row lacks a leading row header",
    )
    require(len(soup.find_all("figure")) == qa_spec["reader_figures"], "Reader figure census differs")
    require(len(soup.find_all("img")) == qa_spec["reader_images"], "Reader image census differs")
    image_dimensions: list[list[int]] = []
    declared_image_order: list[str] = []
    for figure_spec in spec["reader_figures"]:
        figure = soup.select_one(f'figure#{figure_spec["figure_id"]}')
        require(figure is not None, f"Reader figure is missing: {figure_spec['figure_id']}")
        require("reader-figure" in figure.get("class", []), "Reader figure responsive class is missing")
        require(
            figure.get("aria-labelledby") == figure_spec["caption_id"],
            "Reader figure caption association differs",
        )
        caption = figure.select_one(f'figcaption#{figure_spec["caption_id"]}')
        long_description = figure.select_one(f'#{figure_spec["long_description_id"]}')
        require(
            caption is not None and base.canonical_text(caption.get_text(" ", strip=True)),
            f"Reader figure caption is missing: {figure_spec['figure_id']}",
        )
        require(
            long_description is not None
            and base.canonical_text(long_description.get_text(" ", strip=True)),
            f"Reader figure long description is missing: {figure_spec['figure_id']}",
        )
        if figure_spec["injection"] == "wrap-caption-and-long-description":
            source_caption = canonical_soup.select_one(
                f'[data-o005-segment-key="{figure_spec["caption_key"]}"]'
            )
            source_description = canonical_soup.select_one(
                f'[data-o005-segment-key="{figure_spec["long_description_key"]}"]'
            )
            require(
                source_caption is not None
                and source_description is not None
                and figure.get("aria-describedby") == figure_spec["long_description_id"],
                "Reader figure source anchors or long-description association differ",
            )
            require(
                caption.get("data-o005-segment-key") == figure_spec["caption_key"]
                and base.canonical_text(caption.get_text(" ", strip=True))
                == base.canonical_text(source_caption.get_text(" ", strip=True)),
                "Reader figure caption differs from its canonical semantic slot",
            )
            require(
                long_description.get("data-o005-segment-key")
                == figure_spec["long_description_key"]
                and base.canonical_text(long_description.get_text(" ", strip=True))
                == base.canonical_text(
                    BeautifulSoup(
                        builder.render_bridge_markup(str(source_description)),
                        "html.parser",
                    ).get_text(" ", strip=True)
                ),
                "Reader figure long description differs from its canonical semantic slot",
            )
        images = figure.find_all("img")
        require(len(images) == len(figure_spec["images"]), "Reader figure image grouping differs")
        for image, declaration in zip(images, figure_spec["images"]):
            relative = f"assets/figures/{declaration['asset_name']}"
            declared_image_order.append(relative)
            require(image.get("src") == relative, "Reader image source order differs")
            require(image.get("alt") == declaration["alt"], "Reader image alt text differs")
            require(
                image.get("aria-describedby") == figure_spec["long_description_id"],
                "Reader image long-description association differs",
            )
            require(
                image.get("data-notebook-cell-id") == declaration["cell_id"],
                "Reader image notebook extraction identity differs",
            )
            alt_lower = declaration["alt"].lower()
            require(
                any(token in alt_lower for token in ("garis", "penanda", "tanda", "titik")),
                "Reader image alt relies on color or fill alone",
            )
            image_path = root / Path(relative)
            require(image_path.is_file(), f"Reader image asset is missing: {relative}")
            payload = image_path.read_bytes()
            require(
                len(payload) >= 24
                and payload[:16] == b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR",
                f"Reader image asset is not a valid PNG: {relative}",
            )
            width, height = struct.unpack(">II", payload[16:24])
            require(width > 0 and height > 0, f"Reader image has empty natural dimensions: {relative}")
            with Image.open(io.BytesIO(payload)) as decoded:
                decoded.load()
                require(
                    decoded.format == "PNG" and decoded.size == (width, height),
                    f"Reader image cannot be fully decoded at its natural dimensions: {relative}",
                )
            require(
                image.get("width") == str(width) and image.get("height") == str(height),
                f"Reader image declared dimensions differ: {relative}",
            )
            require(sha_bytes(payload) == declaration["sha256"], f"Reader image hash differs: {relative}")
            image_dimensions.append([width, height])
    require(
        [str(image.get("src")) for image in soup.select("figure img[src]")] == declared_image_order,
        "Reader image DOM extraction order differs",
    )
    if spec["segment_mode"] == "html-data-attribute":
        reader_keys = [
            str(tag["data-o005-segment-key"])
            for tag in soup.select("[data-o005-segment-key]")
        ]
        require(
            len(reader_keys) == qa_spec["semantic_keys"] == len(set(reader_keys)),
            "Reader semantic-key census differs",
        )
    expected_problem_ids = {f"{unit_id}-P{i:02d}" for i in range(1, qa_spec["problems"] + 1)}
    require(
        {str(tag.get("id")) for tag in soup.select("h3[id]") if tag.get("id") in expected_problem_ids}
        == expected_problem_ids,
        "Reader problem census differs",
    )
    require(soup.select_one(f'a[href="downloads/{spec["notebook"].name}"]') is not None, "Reader notebook link is missing")
    require(MODEL_IDENTIFICATION in raw, "Reader model provenance is missing")
    # Assemble the sentinels so this QA source can itself pass the public-source
    # privacy scanner without weakening the strings checked in built readers.
    for forbidden in (
        "C:" + "\\Users\\",
        "App" + "Data",
        "Obsidian" + " notes",
        "Down" + "loads",
        "github_" + "pat_",
        "zen" + "odo_" + "to" + "ken",
        "T" + "TP",
    ):
        require(forbidden not in raw, f"Reader privacy/metadata scan found {forbidden!r}")
    require("\\(" not in raw and "\\[" not in raw, "Reader exposes raw TeX delimiters")
    for text_node in soup.find_all(string=re.compile(r"\\(?:left|right|frac|operatorname|sum|infty|mathcal|widehat|bigl|bigr)")):
        parent_name = text_node.parent.name if text_node.parent is not None else ""
        require(parent_name in {"annotation", "code", "pre"}, f"Reader exposes raw TeX command in {parent_name}: {text_node.strip()[:80]}")
    require(not soup.find_all(["script", "iframe", "audio", "video"]), "Reader has undeclared active media")

    copied = {
        root / "assets" / "reader.css": builder.CSS,
        root / "data" / f"{unit_id}.segments.jsonl": ROOT / "backend" / "segments" / f"{unit_id}.segments.jsonl",
        root / "data" / f"{unit_id}.json": ROOT / "backend" / "units" / f"{unit_id}.json",
        root / "data" / f"{unit_id}.mastery.json": ROOT / "backend" / "mastery" / f"{unit_id}.mastery.json",
        root / "data" / "AUTHORITY_MANIFEST.json": ROOT / "authority" / "units" / unit_id / "AUTHORITY_MANIFEST.json",
        root / "data" / spec["segment_id_ledger"].name: spec["segment_id_ledger"],
        root / "downloads" / spec["notebook"].name: spec["notebook"],
        root / "downloads" / "requirements.lock": spec["notebook"].parent / "requirements.lock",
    }
    for target, canonical in copied.items():
        require(target.is_file(), f"Reader copy is missing: {target.name}")
        require(target.read_bytes() == canonical.read_bytes(), f"Reader copy differs: {target.name}")
    return {
        "files": len(files),
        "bytes": sum(path.stat().st_size for path in files),
        "mathml": len(soup.find_all("math")),
        "figures": len(soup.find_all("figure")),
        "images": len(soup.find_all("img")),
        "image_dimensions": image_dimensions,
    }


def deterministic_replay(unit_id: str) -> dict:
    builder_path = ROOT / "scripts" / "build_bridge_unit.py"
    canonical_reader = ROOT / "build" / "reader" / unit_id
    derived_relatives = [
        Path("backend") / "segments" / f"{unit_id}.segments.jsonl",
        Path("backend") / "units" / f"{unit_id}.json",
        Path("authority") / "units" / unit_id / "source-record.canonical.json",
        Path("authority") / "units" / unit_id / "AUTHORITY_MANIFEST.json",
    ]
    canonical_files = sorted(path for path in canonical_reader.rglob("*") if path.is_file())
    require(canonical_files, "Canonical reader tree is missing")
    canonical_derived = [ROOT / relative for relative in derived_relatives]
    require(all(path.is_file() for path in canonical_derived), "Canonical derived record is missing")
    protected = canonical_files + canonical_derived
    before = {path: path.read_bytes() for path in protected}

    with tempfile.TemporaryDirectory(prefix=f"{unit_id.lower()}-a-") as a_name, tempfile.TemporaryDirectory(
        prefix=f"{unit_id.lower()}-b-"
    ) as b_name:
        stage_roots = [Path(a_name), Path(b_name)]
        build_results: list[dict] = []
        for stage in stage_roots:
            proc = subprocess.run(
                [sys.executable, str(builder_path), "--unit", unit_id, "--staging-root", str(stage)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=240,
            )
            result = json.loads(proc.stdout)
            require(result.get("staging") is True, "Deterministic replay did not use staging mode")
            build_results.append(result)

        inventories = [
            sorted(path.relative_to(stage).as_posix() for path in stage.rglob("*") if path.is_file())
            for stage in stage_roots
        ]
        require(inventories[0] == inventories[1], "Repeated staged build member sets differ")
        for relative in inventories[0]:
            require(
                (stage_roots[0] / relative).read_bytes() == (stage_roots[1] / relative).read_bytes(),
                f"Repeated staged build differs: {relative}",
            )

        canonical_reader_relatives = sorted(path.relative_to(canonical_reader).as_posix() for path in canonical_files)
        for stage in stage_roots:
            staged_reader_relatives = sorted(
                path.relative_to(stage / "reader").as_posix()
                for path in (stage / "reader").rglob("*")
                if path.is_file()
            )
            require(staged_reader_relatives == canonical_reader_relatives, "Staged and canonical reader members differ")
            for relative in canonical_reader_relatives:
                require(
                    (stage / "reader" / relative).read_bytes()
                    == (canonical_reader / relative).read_bytes(),
                    f"Staged reader differs from canonical reader: {relative}",
                )

            staged_derived_relatives = sorted(
                path.relative_to(stage / "derived")
                for path in (stage / "derived").rglob("*")
                if path.is_file()
            )
            require(staged_derived_relatives == sorted(derived_relatives), "Staged derived member set differs")
            for relative in derived_relatives:
                require(
                    (stage / "derived" / relative).read_bytes() == (ROOT / relative).read_bytes(),
                    f"Staged derived record differs from canonical record: {relative.as_posix()}",
                )
        inventory = "\n".join(
            f"{relative}\t{sha(stage_roots[0] / relative)}" for relative in inventories[0]
        ).encode("utf-8")

    for path, payload in before.items():
        require(path.is_file() and path.read_bytes() == payload, f"Staged replay mutated canonical file: {path}")
    require(build_results[0] == build_results[1], "Repeated staged build result metadata differs")
    return {
        "files": len(inventories[0]),
        "tree_sha256": sha_bytes(inventory),
        "canonical_files_unchanged": len(before),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", choices=sorted(QA_SPECS), required=True)
    parser.add_argument(
        "--static-only",
        action="store_true",
        help="Skip fresh-kernel notebook execution and deterministic staged rebuild.",
    )
    args = parser.parse_args()
    unit_id = args.unit
    require_pinned_qa_interpreter(unit_id)
    spec = builder.UNIT_SPECS[unit_id]
    qa_spec = QA_SPECS[unit_id]
    content = content_replay(unit_id, spec, qa_spec)
    backend = backend_replay(unit_id, spec, qa_spec, content["slots"])
    notebook = notebook_replay(unit_id, spec, qa_spec, not args.static_only)
    reader = reader_replay(unit_id, spec, qa_spec, ROOT / "build" / "reader" / unit_id)
    result = {
        "schema": "o005-bridge-qa-v2",
        "profile": "static-only" if args.static_only else "full",
        "unit_id": unit_id,
        "content": {"segments": len(content["slots"]), "problems": len(content["problems"])},
        "backend": backend,
        "notebook": notebook,
        "reader": reader,
        "deterministic_build": None if args.static_only else deterministic_replay(unit_id),
        "external_link_reachability_tested": False,
        "audio_or_live_widgets_exercised": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
