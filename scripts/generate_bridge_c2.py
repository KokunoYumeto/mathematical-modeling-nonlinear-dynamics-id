#!/usr/bin/env python3
"""Generate the deterministic C2 notebook, mastery layer, and exact lock file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIT_ID = "O005-BRIDGE-C2"
NOTEBOOK = (
    ROOT
    / "source"
    / "id-ID"
    / UNIT_ID
    / "notebooks"
    / "bridge-c2-local-bifurcations.ipynb"
)
LOCK = NOTEBOOK.parent / "requirements.lock"
MASTERY = ROOT / "backend" / "mastery" / f"{UNIT_ID}.mastery.json"
LOCK_TEXT = """# Lingkungan eksekusi tervalidasi: CPython 3.13.9.
# Notebook tidak memakai jaringan setelah lingkungan ini terpasang.
asttokens==3.0.0
attrs==26.1.0
beautifulsoup4==4.14.3
bleach==6.2.0
colorama==0.4.6
comm==0.2.2
contourpy==1.3.3
cycler==0.12.1
debugpy==1.8.12
decorator==5.2.1
defusedxml==0.7.1
executing==2.2.0
fastjsonschema==2.21.1
fonttools==4.63.0
ipykernel==6.29.5
ipython==8.32.0
jedi==0.19.2
Jinja2==3.1.6
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
jupyter-client==8.6.3
jupyter-core==5.7.2
jupyterlab-pygments==0.3.0
kiwisolver==1.5.0
MarkupSafe==3.0.3
matplotlib==3.10.9
matplotlib-inline==0.1.7
mistune==3.1.2
nbclient==0.10.2
nbconvert==7.16.6
nbformat==5.10.4
nest-asyncio==1.6.0
numpy==2.4.4
packaging==25.0
pandocfilters==1.5.1
parso==0.8.4
pillow==12.2.0
platformdirs==4.5.0
prompt-toolkit==3.0.50
psutil==7.2.2
pure-eval==0.2.3
Pygments==2.19.2
pyparsing==3.3.2
python-dateutil==2.9.0.post0
pywin32==311 ; sys_platform == "win32"
pyzmq==26.2.1
referencing==0.37.0
rpds-py==2026.5.1
scipy==1.17.1
six==1.17.0
soupsieve==2.8.4
stack-data==0.6.3
tornado==6.4.2
traitlets==5.14.3
typing-extensions==4.15.0
wcwidth==0.2.13
webencodings==0.5.1
"""


def markdown(cell_id: str, text: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": [line + "\n" for line in text.rstrip().split("\n")],
    }


def code(cell_id: str, text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.rstrip().split("\n")],
    }


def notebook_payload() -> dict:
    cells = [
        markdown(
            "c2-title",
            """# O005-BRIDGE-C2 — Bifurkasi Lokal: Perubahan Kestabilan dan Munculnya Osilasi

Notebook ini merupakan tambahan independen untuk edisi Bahasa Indonesia *Introduction to Mathematical Modeling*. Ia memeriksa bentuk normal saddle-node, transkritis, pitchfork, dan Hopf secara deterministik; notebook ini bukan bagian dari buku sumber.

Produksi dan QA: OpenAI Codex gpt-5.6-sol, Ultra. Kredit Joceline Lega dan University of Arizona tetap terpisah dan tidak menyiratkan dukungan terhadap tambahan ini. Distribusi mengikuti CC BY-NC-SA 4.0.""",
        ),
        code(
            "c2-environment",
            """import hashlib
import json
import platform

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.integrate import solve_ivp

EXPECTED = {
    "python": "3.13.9",
    "numpy": "2.4.4",
    "scipy": "1.17.1",
    "matplotlib": "3.10.9",
}
VERSIONS = {
    "python": platform.python_version(),
    "numpy": np.__version__,
    "scipy": scipy.__version__,
    "matplotlib": matplotlib.__version__,
}

def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)

require(VERSIONS == EXPECTED, f"Lingkungan berbeda: {VERSIONS!r} != {EXPECTED!r}")""",
        ),
        markdown(
            "c2-scalar-contract",
            r"""## Cabang kesetimbangan dan kestabilan bentuk normal skalar

Untuk $\dot x=f(x;\mu)$, kesetimbangan memenuhi $f(x_*;\mu)=0$ dan nilai eigen skalarnya adalah $\lambda=f_x(x_*;\mu)$. Nilai negatif berarti stabil asimtotik secara lokal; nilai positif berarti tidak stabil. Nilai nol hanya menandai bahwa uji linear tidak memberi keputusan.

Keluarga $\dot x=-x^3-\mu^2x$ dipakai sebagai contoh tandingan: $x=0$ nonhiperbolik pada $\mu=0$, tetapi tetap stabil dan tidak mengalami bifurkasi.""",
        ),
        code(
            "c2-scalar-census",
            """def scalar_equilibria(family, mu):
    if family == "saddle_node":
        return [] if mu < 0.0 else ([0.0] if mu == 0.0 else [-np.sqrt(mu), np.sqrt(mu)])
    if family == "transcritical":
        return [0.0, float(mu)]
    if family == "pitchfork":
        return [0.0] if mu < 0.0 else ([0.0] if mu == 0.0 else [-np.sqrt(mu), 0.0, np.sqrt(mu)])
    if family == "counterexample":
        return [0.0]
    raise ValueError(f"Keluarga tidak dikenal: {family}")

def scalar_eigenvalue(family, x_star, mu):
    if family == "saddle_node":
        return -2.0 * x_star
    if family == "transcritical":
        return mu - 2.0 * x_star
    if family == "pitchfork":
        return mu - 3.0 * x_star**2
    if family == "counterexample":
        return -3.0 * x_star**2 - mu**2
    raise ValueError(f"Keluarga tidak dikenal: {family}")

def census(family, mu):
    return [
        {"x": round(float(x), 12), "lambda": round(float(scalar_eigenvalue(family, x, mu)), 12)}
        for x in scalar_equilibria(family, mu)
    ]

SCALAR_CASES = {
    "saddle_node_mu_minus_0_25": census("saddle_node", -0.25),
    "saddle_node_mu_plus_0_25": census("saddle_node", 0.25),
    "transcritical_mu_minus_0_5": census("transcritical", -0.5),
    "transcritical_mu_plus_0_5": census("transcritical", 0.5),
    "pitchfork_mu_minus_0_5": census("pitchfork", -0.5),
    "pitchfork_mu_plus_0_25": census("pitchfork", 0.25),
}

require(SCALAR_CASES["saddle_node_mu_minus_0_25"] == [], "Sensus saddle-node untuk mu negatif salah")
require(SCALAR_CASES["saddle_node_mu_plus_0_25"] == [{"x": -0.5, "lambda": 1.0}, {"x": 0.5, "lambda": -1.0}], "Kasus saddle-node kanonik berbeda")
require(SCALAR_CASES["transcritical_mu_minus_0_5"] == [{"x": 0.0, "lambda": -0.5}, {"x": -0.5, "lambda": 0.5}], "Kasus transkritis negatif berbeda")
require(SCALAR_CASES["transcritical_mu_plus_0_5"] == [{"x": 0.0, "lambda": 0.5}, {"x": 0.5, "lambda": -0.5}], "Kasus transkritis positif berbeda")
require(SCALAR_CASES["pitchfork_mu_minus_0_5"] == [{"x": 0.0, "lambda": -0.5}], "Kasus pitchfork negatif berbeda")
require(SCALAR_CASES["pitchfork_mu_plus_0_25"] == [{"x": -0.5, "lambda": -0.5}, {"x": 0.0, "lambda": 0.25}, {"x": 0.5, "lambda": -0.5}], "Kasus pitchfork positif berbeda")
for mu in (-0.5, 0.0, 0.5):
    require(scalar_equilibria("counterexample", mu) == [0.0], "Cabang contoh tandingan berubah")
require((-0.1**3 - 0.0**2 * 0.1) < 0.0 and (-(-0.1)**3 - 0.0**2 * (-0.1)) > 0.0, "Arah medan contoh tandingan salah")""",
        ),
        markdown(
            "c2-bifurcation-diagrams",
            r"""## Gambar 1 — Empat diagram bifurkasi

**Deskripsi panjang:** panel saddle-node kosong untuk parameter negatif lalu bercabang menjadi cabang bawah tidak stabil dan cabang atas stabil. Panel transkritis memperlihatkan dua garis yang berpotongan dan bertukar kestabilan pada nol. Panel pitchfork memperlihatkan cabang nol stabil untuk parameter negatif, lalu tidak stabil ketika dua cabang stabil simetris muncul. Panel Hopf memperlihatkan keadaan asal yang kehilangan kestabilan serta selubung amplitudo atas–bawah $\pm r_*$ yang tumbuh seperti akar kuadrat untuk parameter positif; kedua selubung menggambarkan satu siklus. Garis utuh dengan lingkaran menandai objek stabil; garis putus-putus dengan silang menandai objek tidak stabil; wajik menandai titik kritis.""",
        ),
        code(
            "c2-bifurcation-figure",
            r"""STABLE = {"linestyle": "-", "marker": "o", "markevery": 18, "linewidth": 2.0, "markersize": 4}
UNSTABLE = {"linestyle": "--", "marker": "x", "markevery": 18, "linewidth": 1.8, "markersize": 5}

def critical_marker(ax):
    ax.plot([0.0], [0.0], linestyle="none", marker="D", markerfacecolor="white", markeredgecolor="black", markersize=7, label="titik kritis")

fig1, axes = plt.subplots(1, 4, figsize=(13.2, 3.4), constrained_layout=True, sharex=True)
mu_neg = np.linspace(-0.8, 0.0, 121)
mu_pos = np.linspace(0.0, 0.8, 121)

axes[0].plot(mu_pos, np.sqrt(mu_pos), color="#176d45", label="stabil", **STABLE)
axes[0].plot(mu_pos, -np.sqrt(mu_pos), color="#9b2f2f", label="tidak stabil", **UNSTABLE)
critical_marker(axes[0])
axes[0].set_title("saddle-node")

axes[1].plot(mu_neg, np.zeros_like(mu_neg), color="#176d45", label="stabil", **STABLE)
axes[1].plot(mu_pos, np.zeros_like(mu_pos), color="#9b2f2f", label="tidak stabil", **UNSTABLE)
axes[1].plot(mu_neg, mu_neg, color="#9b2f2f", **UNSTABLE)
axes[1].plot(mu_pos, mu_pos, color="#176d45", **STABLE)
critical_marker(axes[1])
axes[1].set_title("transkritis")

axes[2].plot(mu_neg, np.zeros_like(mu_neg), color="#176d45", label="stabil", **STABLE)
axes[2].plot(mu_pos, np.zeros_like(mu_pos), color="#9b2f2f", label="tidak stabil", **UNSTABLE)
axes[2].plot(mu_pos, np.sqrt(mu_pos), color="#176d45", **STABLE)
axes[2].plot(mu_pos, -np.sqrt(mu_pos), color="#176d45", **STABLE)
critical_marker(axes[2])
axes[2].set_title("pitchfork superkritis")

axes[3].plot(mu_neg, np.zeros_like(mu_neg), color="#176d45", label="asal stabil", **STABLE)
axes[3].plot(mu_pos, np.zeros_like(mu_pos), color="#9b2f2f", label="asal tidak stabil", **UNSTABLE)
axes[3].plot(mu_pos, np.sqrt(mu_pos), color="#315ca8", label="siklus stabil", **STABLE)
axes[3].plot(mu_pos, -np.sqrt(mu_pos), color="#315ca8", **STABLE)
critical_marker(axes[3])
axes[3].set_title("Hopf: amplitudo")

for ax in axes:
    ax.axvline(0.0, color="0.65", linewidth=0.8)
    ax.axhline(0.0, color="0.65", linewidth=0.8)
    ax.set(xlabel=r"parameter $\mu$", xlim=(-0.8, 0.8), ylim=(-0.95, 0.95))
axes[0].set_ylabel("kesetimbangan / amplitudo")
handles, labels = axes[3].get_legend_handles_labels()
fig1.legend(handles, labels, loc="outside lower center", ncol=4)
fig1.canvas.draw()
if matplotlib.get_backend().lower() != "agg":
    plt.show()
plt.close(fig1)""",
        ),
        markdown(
            "c2-hopf-integration",
            r"""## Bentuk normal Hopf dan pembanding eksak

Dengan $r^2=x^2+y^2$, $\beta,\omega>0$,

$$\dot x=\mu x-\omega y-\beta r^2x,\qquad
\dot y=\omega x+\mu y-\beta r^2y.$$

Persamaan polar adalah $\dot r=\mu r-\beta r^3$ dan $\dot\theta=\omega$. Untuk $\mu>0$, siklus stabil mempunyai $r_*=\sqrt{\mu/\beta}$, periode $2\pi/\omega$, dan turunan radial $-2\mu$. Integrasi numerik menggunakan DOP853 pada 801 titik tetap dan dibandingkan dengan solusi eksak radial.""",
        ),
        code(
            "c2-hopf-solve",
            """T_EVAL = np.linspace(0.0, 40.0, 801)
RTOL = 1e-11
ATOL = 1e-13
OMEGA = 2.0
CANONICAL_BETA = 1.0
PRIMARY_BETA = CANONICAL_BETA
PRIMARY_BETA = float(PRIMARY_BETA)
CANONICAL_MU_VALUES = (-0.25, 0.25)
INITIAL_RADII = (0.12, 0.35, 0.80)
require(PRIMARY_BETA in (CANONICAL_BETA, 2.0), "Beta utama harus 1 atau 2")

def hopf_rhs(_t, state, mu, beta, omega):
    x, y = state
    radius_squared = x*x + y*y
    return [mu*x - omega*y - beta*radius_squared*x,
            omega*x + mu*y - beta*radius_squared*y]

def exact_radius(t, r0, mu, beta):
    t = np.asarray(t, dtype=float)
    q0 = float(r0)**2
    if mu == 0.0:
        q = q0 / (1.0 + 2.0*beta*q0*t)
    else:
        q = mu*q0 / (beta*q0 + (mu - beta*q0)*np.exp(-2.0*mu*t))
    return np.sqrt(q)

def integrate_hopf(mu, beta, r0, omega=OMEGA):
    solution = solve_ivp(
        hopf_rhs,
        (float(T_EVAL[0]), float(T_EVAL[-1])),
        [float(r0), 0.0],
        args=(float(mu), float(beta), float(omega)),
        method="DOP853",
        t_eval=T_EVAL,
        rtol=RTOL,
        atol=ATOL,
    )
    require(solution.success, f"Integrasi Hopf gagal: {solution.message}")
    require(np.array_equal(solution.t, T_EVAL), "Grid keluaran integrasi berubah")
    numeric_radius = np.hypot(solution.y[0], solution.y[1])
    analytic_radius = exact_radius(T_EVAL, r0, mu, beta)
    max_error = float(np.max(np.abs(numeric_radius - analytic_radius)))
    require(np.isfinite(solution.y).all(), "Integrasi menghasilkan nilai tak hingga atau NaN")
    require(max_error < 1e-9, f"Galat solusi radial terlalu besar: {max_error:.3e}")
    return solution, numeric_radius, analytic_radius, max_error

RUNS = {}
for mu in CANONICAL_MU_VALUES:
    for r0 in INITIAL_RADII:
        RUNS[(mu, r0)] = integrate_hopf(mu, PRIMARY_BETA, r0)

MAX_RADIAL_ERROR = max(item[3] for item in RUNS.values())
require(MAX_RADIAL_ERROR < 1e-9, "Batas galat radial kanonik gagal")""",
        ),
        markdown(
            "c2-hopf-figure-description",
            r"""## Gambar 2 — Potret fase dan lintasan jari-jari Hopf

**Deskripsi panjang:** empat panel membandingkan $\mu=-0.25$ dan $\mu=0.25$. Pada pasangan panel parameter negatif, lintasan berputar berlawanan arah jarum jam dan semua jari-jari turun menuju nol. Pada pasangan parameter positif, lintasan yang dimulai di dalam maupun di luar lingkaran $r_*=\sqrt{0.25/\mathtt{PRIMARY\_BETA}}$ mendekati lingkaran tersebut. Jari-jari ini bernilai $0.5$ pada konfigurasi kanonik $\beta=1$ dan $0.3535533905932738$ pada eksperimen terdeklarasi $\beta=2$. Jenis garis membedakan jari-jari awal; lingkaran menandai keadaan awal, persegi menandai keadaan akhir, dan penanda wajik berkala menunjukkan solusi radial eksak.""",
        ),
        code(
            "c2-hopf-figure",
            r"""fig2, axes2 = plt.subplots(2, 2, figsize=(9.2, 7.2), constrained_layout=True)
LINESTYLES = ("-", "--", "-.")
COLORS = ("#315ca8", "#a04a22", "#3f7d3c")

for column, mu in enumerate(CANONICAL_MU_VALUES):
    ax_phase = axes2[0, column]
    ax_radius = axes2[1, column]
    for index, r0 in enumerate(INITIAL_RADII):
        solution, numeric_radius, analytic_radius, _ = RUNS[(mu, r0)]
        style = LINESTYLES[index]
        color = COLORS[index]
        label = f"r(0)={r0:.2f}"
        ax_phase.plot(solution.y[0], solution.y[1], linestyle=style, color=color, label=label)
        ax_phase.plot(solution.y[0, 0], solution.y[1, 0], linestyle="none", marker="o", color=color)
        ax_phase.plot(solution.y[0, -1], solution.y[1, -1], linestyle="none", marker="s", color=color)
        ax_radius.plot(T_EVAL, numeric_radius, linestyle=style, color=color, label=f"numerik {label}")
        ax_radius.plot(T_EVAL[::80], analytic_radius[::80], linestyle="none", marker="D", markerfacecolor="white", markeredgecolor=color, markersize=4, label=f"eksak {label}")
    if mu > 0.0:
        radius_star = np.sqrt(mu/PRIMARY_BETA)
        angle = np.linspace(0.0, 2.0*np.pi, 361)
        radius_label = f"r*={radius_star:.8f}"
        ax_phase.plot(radius_star*np.cos(angle), radius_star*np.sin(angle), color="black", linestyle=":", linewidth=2.0, label=f"siklus {radius_label}")
        ax_radius.axhline(radius_star, color="black", linestyle=":", linewidth=2.0, label=radius_label)
    else:
        ax_phase.plot([0.0], [0.0], linestyle="none", marker="D", markerfacecolor="white", markeredgecolor="black", markersize=6, label="asal stabil")
        ax_radius.axhline(0.0, color="black", linestyle=":", linewidth=1.5, label="r=0")
    ax_phase.set(aspect="equal", xlabel="x", ylabel="y", title=fr"potret fase, $\mu={mu:+.2f}$", xlim=(-0.85, 0.85), ylim=(-0.85, 0.85))
    ax_radius.set(xlabel="waktu", ylabel="jari-jari r(t)", title=fr"lintasan radial, $\mu={mu:+.2f}$", xlim=(0.0, 40.0), ylim=(-0.02, 0.85))
    ax_phase.legend(fontsize=7, loc="upper right")
    ax_radius.legend(fontsize=6, ncol=2, loc="best")

fig2.canvas.draw()
if matplotlib.get_backend().lower() != "agg":
    plt.show()
plt.close(fig2)""",
        ),
        markdown(
            "c2-canonical-summary",
            r"""## Ringkasan kanonik dan variasi parameter

Ringkasan berikut mengikat kasus skalar, parameter integrator, sifat siklus Hopf, dan galat terhadap solusi radial eksak. Variasi $\beta=2$ memeriksa pemisahan pengaruh: $\beta$ mengubah amplitudo, tetapi tidak mengubah frekuensi sudut atau turunan radial $-2\mu$ pada siklus.""",
        ),
        code(
            "c2-summary-checks",
            """def hopf_cycle_properties(mu, beta, omega):
    require(mu > 0.0 and beta > 0.0 and omega > 0.0, "Parameter siklus Hopf harus positif")
    radius = np.sqrt(mu/beta)
    period = 2.0*np.pi/omega
    radial_derivative_direct = mu - 3.0*beta*radius**2
    radial_derivative_reduced = -2.0*mu
    require(abs(radial_derivative_direct - radial_derivative_reduced) < 1e-14, "Dua bentuk turunan radial tidak cocok")
    return float(radius), float(period), float(radial_derivative_reduced)

canonical_radius, canonical_period, canonical_radial_derivative = hopf_cycle_properties(0.25, 1.0, 2.0)
variant_radius, variant_period, variant_radial_derivative = hopf_cycle_properties(0.25, 2.0, 2.0)
primary_radius, primary_period, primary_radial_derivative = hopf_cycle_properties(0.25, PRIMARY_BETA, 2.0)

require(abs(canonical_radius - 0.5) < 1e-15, "Jari-jari Hopf kanonik berubah")
require(abs(canonical_period - np.pi) < 1e-15, "Periode Hopf kanonik berubah")
require(abs(canonical_radial_derivative + 0.5) < 1e-15, "Turunan radial kanonik berubah")
require(abs(variant_radius - 0.3535533905932738) < 1e-15, "Jari-jari variasi beta berubah")
require(abs(variant_period - np.pi) < 1e-15, "Periode variasi beta berubah")
require(abs(variant_radial_derivative + 0.5) < 1e-15, "Turunan radial variasi beta berubah")

CONFIGURATION = {
    "atol": ATOL,
    "beta": PRIMARY_BETA,
    "initial_radii": list(INITIAL_RADII),
    "method": "DOP853",
    "mu_values": list(CANONICAL_MU_VALUES),
    "omega": OMEGA,
    "rtol": RTOL,
    "t_points": int(T_EVAL.size),
    "t_span": [float(T_EVAL[0]), float(T_EVAL[-1])],
}
CONFIGURATION_JSON = json.dumps(CONFIGURATION, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
CONFIGURATION_SHA256 = hashlib.sha256(CONFIGURATION_JSON.encode("utf-8")).hexdigest()
CANONICAL_CONFIGURATION_SHA256 = "3cbb62d2e4543fa5720822edcca8a3b6d92dfdd7a359c5ace8f9a42f6163c467"
if PRIMARY_BETA == CANONICAL_BETA:
    require(CONFIGURATION_SHA256 == CANONICAL_CONFIGURATION_SHA256, "Identitas konfigurasi kanonik berubah")
else:
    require(CONFIGURATION_SHA256 != CANONICAL_CONFIGURATION_SHA256, "Eksperimen beta nonkanonik tidak mengubah identitas konfigurasi")
RINGKASAN = {
    "unit_id": "O005-BRIDGE-C2",
    "model_identification": "OpenAI Codex gpt-5.6-sol, Ultra.",
    "configuration_sha256": CONFIGURATION_SHA256,
    "scalar_cases": SCALAR_CASES,
    "hopf_primary": {
        "mu": 0.25,
        "beta": PRIMARY_BETA,
        "omega": 2.0,
        "radius": round(primary_radius, 16),
        "period": round(primary_period, 16),
        "radial_derivative": round(primary_radial_derivative, 16),
    },
    "hopf_beta_2": {
        "mu": 0.25,
        "beta": 2.0,
        "omega": 2.0,
        "radius": round(variant_radius, 16),
        "period": round(variant_period, 16),
        "radial_derivative": round(variant_radial_derivative, 16),
    },
    "max_radial_error": MAX_RADIAL_ERROR,
    "versions": VERSIONS,
}
require(RINGKASAN["hopf_beta_2"]["radius"] == 0.3535533905932738, "Pembulatan jari-jari variasi berbeda")
if PRIMARY_BETA == CANONICAL_BETA:
    require(RINGKASAN["hopf_primary"]["radius"] == 0.5, "Jari-jari utama kanonik berbeda")
else:
    require(RINGKASAN["hopf_primary"] == RINGKASAN["hopf_beta_2"], "Kasus utama beta=2 tidak cocok dengan pembanding eksak")
print(json.dumps(RINGKASAN, ensure_ascii=False, sort_keys=True, indent=2))""",
        ),
        markdown(
            "c2-same-kernel-replay",
            """## Verifikasi ulang deterministik dalam kernel yang sama

Sel terakhir mengulang keenam integrasi dari input yang sama. Ia membandingkan seluruh larik keadaan dan galat maksimum dengan hasil pertama. Pemeriksaan ini mendeteksi perubahan keadaan dalam kernel, tetapi QA eksternal tetap harus memulai kernel Jupyter baru dan menjalankan semua sel secara berurutan.""",
        ),
        code(
            "c2-same-kernel-check",
            """REPLAY_ERRORS = []
for mu in CANONICAL_MU_VALUES:
    for r0 in INITIAL_RADII:
        replay_solution, replay_numeric, replay_exact, replay_error = integrate_hopf(mu, PRIMARY_BETA, r0)
        original_solution, original_numeric, original_exact, original_error = RUNS[(mu, r0)]
        require(np.array_equal(replay_solution.y, original_solution.y), f"Keadaan numerik berubah untuk mu={mu}, r0={r0}")
        require(np.array_equal(replay_numeric, original_numeric), f"Jari-jari numerik berubah untuk mu={mu}, r0={r0}")
        require(np.array_equal(replay_exact, original_exact), f"Solusi eksak berubah untuk mu={mu}, r0={r0}")
        require(replay_error == original_error, f"Galat maksimum berubah untuk mu={mu}, r0={r0}")
        REPLAY_ERRORS.append(replay_error)
require(max(REPLAY_ERRORS) == MAX_RADIAL_ERROR, "Ringkasan galat berubah pada pengulangan")
print("Verifikasi ulang deterministik dalam kernel yang sama lulus.")""",
        ),
    ]
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "O005 C120 Python 3.13.9",
                "language": "python",
                "name": "o005-c120-py3139",
            },
            "language_info": {"name": "python", "version": "3.13.9"},
            "o005": {
                "unit_id": UNIT_ID,
                "notebook_id": "O005-BRIDGE-C2-NB01",
                "language": "id-ID",
                "locale": "id-ID",
                "provenance": "new_original_addition",
                "component_origin": "original",
                "relationship": "independent_supplement",
                "non_endorsement": True,
                "offline_capable": True,
                "offline_scope": "network_free_after_environment_install",
                "environment_lock": "requirements.lock",
                "wheelhouse_included": False,
                "model_identification": "OpenAI Codex gpt-5.6-sol, Ultra.",
                "license": "CC BY-NC-SA 4.0",
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
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def mastery_payload() -> dict:
    def provenance() -> dict:
        return {
            "problem_summary": "new_original",
            "hint": "new_original",
            "check": "new_original",
            "solution_or_rubric": "new_original",
        }

    problems = [
        {
            "problem_id": f"{UNIT_ID}-P01",
            "ordinal": 1,
            "problem_summary": "Gunakan keluarga \\(-x^3-\\mu^2x\\) untuk membuktikan bahwa nonhiperbolisitas tidak cukup bagi bifurkasi.",
            "article_link_ids": [],
            "source_formula_occurrences": [
                "\\(\\frac{dx}{dt}=-x^3-\\mu^2x\\)",
                "\\(\\lambda=-\\mu^2\\)",
            ],
            "provenance": provenance(),
            "hint": {"text": "Faktorkan persamaan kesetimbangan dan periksa tanda medan di kedua sisi nol, terutama ketika \\(\\mu=0\\)."},
            "check": {
                "type": "qualitative",
                "final_answer": "\\(x=0\\) adalah satu-satunya cabang untuk semua \\(\\mu\\); \\(\\lambda=-\\mu^2\\) dan menjadi nol hanya pada \\(\\mu=0\\); arah medan tetap menuju nol, sehingga tidak ada perubahan cabang atau kestabilan.",
                "required_evidence": [
                    "Persamaan \\(x(-x^2-\\mu^2)=0\\) tidak mempunyai akar riil nonnol.",
                    "Untuk \\(\\mu\\ne0\\), \\(\\lambda=-\\mu^2<0\\).",
                    "Pada \\(\\mu=0\\), \\(-x^3\\) mengarah ke nol dari kedua sisi.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Selesaikan \\(-x^3-\\mu^2x=-x(x^2+\\mu^2)=0\\).",
                    "Karena \\(x^2+\\mu^2\\ge0\\), satu-satunya cabang riil adalah \\(x=0\\); pada \\(\\mu=0\\) faktor itu hanya menambah kemultiplikasian akar.",
                    "Hitung \\(f_x=-3x^2-\\mu^2\\), sehingga \\(\\lambda=-\\mu^2\\) pada cabang nol.",
                    "Pada titik kritis, \\(x>0\\) memberi \\(\\dot{x}<0\\) dan \\(x<0\\) memberi \\(\\dot{x}>0\\).",
                ],
                "conclusion": "Linearisasi nol memerlukan analisis nonlinear; ia bukan sertifikat bifurkasi.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P02",
            "ordinal": 2,
            "problem_summary": "Buat sensus kesetimbangan dan kestabilan saddle-node, termasuk titik semistabil.",
            "article_link_ids": [],
            "source_formula_occurrences": [
                "\\(\\frac{dx}{dt}=\\mu-x^2\\)",
                "\\(x=\\pm\\sqrt{\\mu}\\)",
                "\\(\\lambda=-2x\\)",
            ],
            "provenance": provenance(),
            "hint": {"text": "Pisahkan tiga rezim tanda \\(\\mu\\); ketika \\(\\mu=0\\), uji arah \\(-x^2\\) dari kiri dan kanan."},
            "check": {
                "type": "structured",
                "final_answer": "Tidak ada kesetimbangan untuk \\(\\mu<0\\); \\(x=0\\) semistabil untuk \\(\\mu=0\\); untuk \\(\\mu>0\\), \\(-\\sqrt{\\mu}\\) tidak stabil dan \\(+\\sqrt{\\mu}\\) stabil.",
                "required_evidence": [
                    "Akar diperoleh dari \\(x^2=\\mu\\).",
                    "\\(\\lambda=-2x\\) memberi tanda berlawanan pada dua cabang.",
                    "Pada \\(\\mu=0\\), aliran dari kanan menuju nol tetapi dari kiri menjauh.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Untuk \\(\\mu<0\\), \\(x^2=\\mu\\) tidak mempunyai solusi riil.",
                    "Untuk \\(\\mu>0\\), substitusikan \\(x=-\\sqrt{\\mu}\\) dan \\(x=+\\sqrt{\\mu}\\) ke \\(\\lambda=-2x\\).",
                    "Untuk \\(\\mu=0\\), gunakan \\(\\dot{x}=-x^2\\): kecepatan selalu negatif kecuali di nol.",
                ],
                "conclusion": "Pada nilai kritis, pasangan stabil–tidak stabil bertemu dalam kesetimbangan semistabil.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P03",
            "ordinal": 3,
            "problem_summary": "Tunjukkan pertukaran kestabilan transkritis dan terapkan batas populasi tak negatif.",
            "article_link_ids": [],
            "source_formula_occurrences": [
                "\\(\\frac{dx}{dt}=x(\\mu-x)\\)",
                "\\(x=0\\)",
                "\\(x=\\mu\\)",
            ],
            "provenance": provenance(),
            "hint": {"text": "Nilai eigen pada cabang \\(x=0\\) adalah \\(\\mu\\), sedangkan pada cabang \\(x=\\mu\\) adalah \\(-\\mu\\)."},
            "check": {
                "type": "structured",
                "final_answer": "Pada \\(\\mu=-0.5\\), \\(x=0\\) stabil dan \\(x=-0.5\\) tidak stabil; pada \\(\\mu=0.5\\), \\(x=0\\) tidak stabil dan \\(x=0.5\\) stabil. Cabang \\(x=\\mu\\) untuk \\(\\mu<0\\) dikeluarkan dari domain populasi \\(x\\ge0\\).",
                "required_evidence": [
                    "\\(f_x=\\mu-2x\\) dievaluasi pada kedua cabang.",
                    "Tanda nilai eigen bertukar ketika \\(\\mu\\) melewati nol.",
                    "Cabang matematis negatif dibedakan dari keadaan fisik populasi.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Faktorkan \\(f=x(\\mu-x)\\) untuk memperoleh \\(x=0\\) dan \\(x=\\mu\\).",
                    "Pada \\(x=0\\), \\(\\lambda=\\mu\\); pada \\(x=\\mu\\), \\(\\lambda=-\\mu\\).",
                    "Substitusikan \\(\\mu=-0.5\\) dan \\(\\mu=0.5\\) untuk memperoleh tanda yang diminta.",
                    "Terapkan \\(x\\ge0\\) setelah cabang matematis disensus.",
                ],
                "conclusion": "Diagram garis riil menunjukkan pertukaran penuh, sedangkan model populasi hanya memakai bagian yang dapat diterima secara fisik.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P04",
            "ordinal": 4,
            "problem_summary": "Hitung cabang pitchfork pada \\(\\mu=\\pm0.36\\) dan jelaskan simetrinya.",
            "article_link_ids": [],
            "source_formula_occurrences": [
                "\\(\\frac{dx}{dt}=\\mu x-x^3\\)",
                "\\(x=\\pm\\sqrt{\\mu}\\)",
                "\\(\\lambda=\\mu-3x^2\\)",
            ],
            "provenance": provenance(),
            "hint": {"text": "Faktorkan \\(x(\\mu-x^2)\\), lalu evaluasi \\(\\mu-3x^2\\) pada setiap akar."},
            "check": {
                "type": "quantitative",
                "final_answer": "Pada \\(\\mu=-0.36\\) hanya \\(x=0\\) dengan \\(\\lambda=-0.36\\); pada \\(\\mu=0.36\\) terdapat \\(x=-0.6\\) dan \\(x=0.6\\) dengan \\(\\lambda=-0.72\\) serta \\(x=0\\) dengan \\(\\lambda=0.36\\).",
                "required_evidence": [
                    "Kedua cabang luar stabil dan cabang nol tidak stabil untuk \\(\\mu\\) positif.",
                    "Invariansi terhadap \\(x\\mapsto-x\\) menjelaskan pasangan cabang luar.",
                    "Gangguan yang merusak simetri dapat memecah pitchfork sempurna.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Akar \\(x(\\mu-x^2)=0\\) adalah \\(x=0\\) dan, jika \\(\\mu\\ge0\\), \\(x=\\pm\\sqrt{\\mu}\\).",
                    "Untuk \\(\\mu=-0.36\\), hanya \\(x=0\\) dan \\(\\lambda=\\mu=-0.36\\).",
                    "Untuk \\(\\mu=0.36\\), akar luar adalah \\(x=\\pm0.6\\); substitusi ke \\(\\lambda=\\mu-3x^2\\) memberi \\(0.36-1.08=-0.72\\).",
                    "Pergantian \\(x\\) menjadi \\(-x\\) tidak mengubah ruas kanan selain transformasi yang sama pada \\(\\dot{x}\\).",
                ],
                "conclusion": "Kehilangan kestabilan keadaan simetris bertepatan dengan lahirnya dua keadaan stabil yang simetris.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P05",
            "ordinal": 5,
            "problem_summary": "Turunkan sifat siklus pada bentuk normal Hopf superkritis.",
            "article_link_ids": [],
            "source_formula_occurrences": [
                "\\(\\dot{r}=\\mu r-\\beta r^3\\)",
                "\\(\\dot{\\theta}=\\omega\\)",
                "\\(r^*=\\sqrt{\\frac{\\mu}{\\beta}}\\)",
                "\\(P=\\frac{2\\pi}{\\omega}\\)",
            ],
            "provenance": provenance(),
            "hint": {"text": "Gunakan \\(\\dot{r}=\\frac{x\\dot{x}+y\\dot{y}}{r}\\) dan \\(\\dot{\\theta}=\\frac{x\\dot{y}-y\\dot{x}}{r^2}\\)."},
            "check": {
                "type": "quantitative",
                "final_answer": "Untuk \\(\\mu=0.25,\\ \\beta=1,\\ \\omega=2\\): \\(r^*=0.5\\), \\(P=\\pi\\), dan turunan radial \\(\\mu-3\\beta(r^*)^2=-0.5\\), sehingga siklus stabil.",
                "required_evidence": [
                    "Suku rotasi saling menghapus dalam \\(\\dot{r}\\).",
                    "\\(\\dot{\\theta}=\\omega\\) memberi periode \\(\\frac{2\\pi}{\\omega}\\).",
                    "Tanda negatif turunan radial menyusutkan gangguan amplitudo.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Hitung \\(r^*\\) dari \\(r(\\mu-\\beta r^2)=0\\) dan pilih akar nonnol positif.",
                    "Hitung \\(r^*=\\sqrt{\\frac{0.25}{1}}=0.5\\).",
                    "Karena \\(\\theta\\) bertambah dengan laju 2, satu putaran memerlukan \\(\\frac{2\\pi}{2}=\\pi\\).",
                    "Evaluasi \\(\\mu-3\\beta(r^*)^2=0.25-3(0.25)=-0.5\\).",
                ],
                "conclusion": "Bentuk normal melahirkan siklus limit kecil yang stabil ketika \\(\\mu\\) menjadi positif.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P06",
            "ordinal": 6,
            "problem_summary": "Bedakan cabang diagram bifurkasi dari lintasan waktu.",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": "Tanyakan apa arti sumbu mendatar dan apakah parameter dipertahankan tetap selama simulasi."},
            "check": {
                "type": "qualitative",
                "final_answer": "Cabang membandingkan objek invarian dari sistem berbeda pada nilai parameter berbeda; lintasan waktu bergerak dalam ruang keadaan dengan parameter yang biasanya tetap.",
                "required_evidence": [
                    "Diagram bifurkasi memakai parameter sebagai sumbu.",
                    "Potret fase atau integrasi dengan kondisi awal diperlukan untuk mengetahui gerak pada satu parameter.",
                    "Parameter yang berubah terhadap waktu merupakan model nonotonom tambahan.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Pilih satu nilai \\(\\mu\\) pada diagram; titik cabang menunjukkan kesetimbangan atau amplitudo asimtotik untuk sistem itu.",
                    "Tentukan kondisi awal dan integrasikan persamaan pada \\(\\mu\\) yang dipilih untuk memperoleh lintasan waktu.",
                    "Gunakan potret fase untuk menampilkan arah aliran dan cekungan tarikan.",
                    "Jika \\(\\mu\\) dibuat bergantung pada waktu, tulis fungsi \\(\\mu(t)\\) dan analisis masalah baru secara eksplisit.",
                ],
                "conclusion": "Membaca cabang dari kiri ke kanan bukan simulasi waktu.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P07",
            "ordinal": 7,
            "problem_summary": "Jalankan notebook kanonik, verifikasi solusi radial, lalu ubah \\(\\beta\\) dari satu menjadi dua.",
            "article_link_ids": [],
            "source_formula_occurrences": [
                "\\(r^*=\\sqrt{\\frac{\\mu}{\\beta}}\\)",
                "\\(P=\\frac{2\\pi}{\\omega}\\)",
                "\\(\\left.\\frac{\\partial\\dot{r}}{\\partial r}\\right|_{r=r^*}=-2\\mu\\)",
            ],
            "provenance": provenance(),
            "hint": {"text": "Pisahkan rumus yang memuat \\(\\beta\\) dari rumus yang hanya memuat \\(\\omega\\) atau \\(\\mu\\)."},
            "check": {
                "type": "executable",
                "final_answer": "Kasus kanonik memberi \\(r^*=0.5\\), \\(P=\\pi\\), turunan radial \\(-0.5\\), dan galat radial maksimum kurang dari \\(10^{-9}\\). Pada \\(\\beta=2\\), \\(r^*=0.3535533905932738\\), sedangkan \\(P=\\pi\\) dan turunan radial \\(-0.5\\).",
                "notebook_check": "Semua 7 sel kode berjalan dari kernel bersih, menghasilkan tepat dua gambar PNG, dan seluruh require() lulus.",
                "required_evidence": [
                    "Integrator DOP853 memakai \\(t\\in[0,40]\\), 801 titik, \\(\\mathrm{rtol}=10^{-11}\\), dan \\(\\mathrm{atol}=10^{-13}\\).",
                    "Enam lintasan radial numerik dibandingkan dengan solusi eksak dan masing-masing mempunyai galat maksimum kurang dari \\(10^{-9}\\).",
                    "Mengubah \\(\\beta\\) memengaruhi \\(\\sqrt{\\frac{\\mu}{\\beta}}\\), tetapi tidak memengaruhi \\(\\frac{2\\pi}{\\omega}\\) atau \\(-2\\mu\\).",
                ],
                "tolerances": {
                    "closed_form_absolute": 1e-15,
                    "radial_solution_max_absolute": 1e-9
                },
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Mulai ulang kernel dan jalankan semua sel secara berurutan.",
                    "Pastikan sensus skalar, dua gambar, ringkasan JSON, dan pengulangan dalam kernel lulus.",
                    "Cocokkan jari-jari numerik dengan solusi radial eksak pada keenam pasangan \\(\\mu\\) dan \\(r(0)\\).",
                    "Ubah hanya \\(\\beta\\) menjadi 2 pada evaluasi sifat siklus.",
                    "Hitung \\(\\sqrt{\\frac{0.25}{2}}=0.3535533905932738\\); \\(\\omega\\) dan \\(\\mu\\) tidak berubah sehingga periode dan turunan radial tetap.",
                ],
                "conclusion": "Variasi satu parameter harus mengubah hanya besaran yang bergantung padanya dan harus tetap terlihat dalam konfigurasi keluaran.",
            },
            "notebook": {
                "path": "source/id-ID/O005-BRIDGE-C2/notebooks/bridge-c2-local-bifurcations.ipynb",
                "provenance": "new_original",
            },
        },
    ]
    return {
        "schema": "o005-bridge-mastery-v1",
        "schema_version": "1.0.0",
        "unit_id": UNIT_ID,
        "language": "id-ID",
        "source": {
            "type": "new_original_addition",
            "spine": "Joceline Lega, Introduction to Mathematical Modeling, v1.01",
            "not_part_of_source_book": True,
            "license": "CC BY-NC-SA 4.0",
        },
        "provenance_policy": {
            "model_identification": "OpenAI Codex gpt-5.6-sol, Ultra.",
            "source_author_credit_preserved": True,
            "non_endorsement": True,
        },
        "article_link_catalog": {},
        "problems": problems,
    }


def render_json(payload: dict) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def expected_files() -> dict[Path, bytes]:
    return {
        NOTEBOOK: render_json(notebook_payload()),
        MASTERY: render_json(mastery_payload()),
        LOCK: LOCK_TEXT.encode("utf-8"),
    }


def generate(check: bool = False) -> None:
    mismatches: list[str] = []
    for path, payload in expected_files().items():
        if check:
            if not path.is_file() or path.read_bytes() != payload:
                mismatches.append(path.relative_to(ROOT).as_posix())
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    if mismatches:
        raise SystemExit("Generated bridge inputs differ: " + ", ".join(mismatches))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generate(check=args.check)
    print(json.dumps({
        "unit_id": UNIT_ID,
        "mode": "check" if args.check else "write",
        "files": [path.relative_to(ROOT).as_posix() for path in expected_files()],
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
