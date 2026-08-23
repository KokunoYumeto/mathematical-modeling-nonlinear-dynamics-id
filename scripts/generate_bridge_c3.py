#!/usr/bin/env python3
"""Generate the deterministic C3 notebook, mastery layer, and lock file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIT_ID = "O005-BRIDGE-C3"
NOTEBOOK = (
    ROOT
    / "source"
    / "id-ID"
    / UNIT_ID
    / "notebooks"
    / "bridge-c3-chaos-and-return-maps.ipynb"
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
            "c3-title",
            r"""# O005-BRIDGE-C3 — Penggandaan Periode, Kekacauan, dan Peta Balik

Notebook ini merupakan tambahan independen untuk edisi Bahasa Indonesia *Introduction to Mathematical Modeling*. Ia membangun diagram bifurkasi dan eksponen Lyapunov peta logistik, mengintegrasikan sistem Lorenz, memeriksa kepekaan terhadap kondisi awal, serta membentuk penampang Poincaré dan proyeksi peta balik. Semua data numerik dibuat dari persamaan yang tertulis; tidak ada data atau aset eksternal.

Produksi dan QA: OpenAI Codex gpt-5.6-sol, Ultra. Kredit Joceline Lega dan University of Arizona untuk buku sumber tetap terpisah dan tidak menyiratkan dukungan terhadap tambahan ini. Distribusi mengikuti CC BY-NC-SA 4.0.""",
        ),
        code(
            "c3-environment",
            """import json
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

require(VERSIONS == EXPECTED, f"Lingkungan berbeda: {VERSIONS!r} != {EXPECTED!r}")
matplotlib.rcParams["figure.dpi"] = 120
matplotlib.rcParams["savefig.dpi"] = 120""",
        ),
        markdown(
            "c3-logistic-contract",
            r"""## Peta logistik, orbit periodik, dan pengali

Untuk $x_n\in[0,1]$ dan $0\le r\le4$,

$$x_{n+1}=f_r(x_n)=r x_n(1-x_n)$$

tetap berada dalam interval yang sama. Titik tetap menarik bila nilai mutlak pengalinya kurang dari satu. Pada $r=3$, rumus calon dua-siklus berimpit di titik tetap $2/3$; dua titik berbeda dengan periode prima dua baru ada untuk $r>3$. Notebook memeriksa batas ini serta rumus dua-siklus secara analitik dan numerik sebelum membuat diagram untuk banyak nilai parameter.""",
        ),
        code(
            "c3-logistic-analysis",
            """X0_LOGISTIK = 0.123456789
R_DUA_SIKLUS = 3.2
TRANSIEN_LYAPUNOV = 2000
ITERASI_LYAPUNOV = 20000

def peta_logistik(x, r):
    return r * x * (1.0 - x)

def turunan_logistik(x, r):
    return r * (1.0 - 2.0 * x)

def orbit_logistik(r, x0, jumlah):
    hasil = np.empty(jumlah + 1, dtype=float)
    hasil[0] = float(x0)
    for indeks in range(jumlah):
        hasil[indeks + 1] = peta_logistik(hasil[indeks], r)
    return hasil

def titik_tetap_logistik(r):
    r = float(r)
    require(np.isfinite(r), "Parameter titik tetap harus berhingga")
    if r in (0.0, 1.0):
        return np.array([0.0])
    return np.array([0.0, 1.0 - 1.0 / r])

def estimasi_lyapunov_peta(r, x0, transien, jumlah):
    x = float(x0)
    for _ in range(transien):
        x = peta_logistik(x, r)
    jumlah_log = 0.0
    for _ in range(jumlah):
        besar_turunan = abs(turunan_logistik(x, r))
        if besar_turunan == 0.0:
            return float("-inf")
        jumlah_log += float(np.log(besar_turunan))
        x = peta_logistik(x, r)
    return jumlah_log / jumlah

def dua_siklus_analitik(r):
    r = float(r)
    require(np.isfinite(r) and r > 3.0, "Dua titik berbeda berperiode prima dua memerlukan r>3")
    akar = np.sqrt((r - 3.0) * (r + 1.0))
    return np.array([(r + 1.0 - akar) / (2.0 * r), (r + 1.0 + akar) / (2.0 * r)])

SIKLUS_R32 = dua_siklus_analitik(R_DUA_SIKLUS)
PENGALI_R32 = float(np.prod(turunan_logistik(SIKLUS_R32, R_DUA_SIKLUS)))
LAMBDA_R32_ANALITIK = float(0.5 * np.log(abs(PENGALI_R32)))
LAMBDA_R32 = estimasi_lyapunov_peta(R_DUA_SIKLUS, X0_LOGISTIK, TRANSIEN_LYAPUNOV, ITERASI_LYAPUNOV)
LAMBDA_R4 = estimasi_lyapunov_peta(4.0, X0_LOGISTIK, TRANSIEN_LYAPUNOV, ITERASI_LYAPUNOV)

grid_uji = np.linspace(0.0, 1.0, 1001)
for r_uji in (0.0, 1.0, 2.8, 3.2, 4.0):
    citra = peta_logistik(grid_uji, r_uji)
    require(np.all(citra >= -1e-15) and np.all(citra <= 1.0 + 1e-15), "Interval invarian gagal")
require(np.array_equal(titik_tetap_logistik(0.0), np.array([0.0])), "Kasus titik tetap r=0 berubah")
require(np.array_equal(titik_tetap_logistik(1.0), np.array([0.0])), "Cabang titik tetap r=1 tidak berimpit")
require(np.allclose(titik_tetap_logistik(3.0), np.array([0.0, 2.0 / 3.0]), rtol=0.0, atol=1e-15), "Titik tetap r=3 berubah")
try:
    dua_siklus_analitik(3.0)
except RuntimeError:
    pass
else:
    raise RuntimeError("r=3 keliru diterima sebagai dua-siklus prima")
require(np.allclose(peta_logistik(SIKLUS_R32, R_DUA_SIKLUS), SIKLUS_R32[::-1], rtol=0.0, atol=1e-14), "Rumus dua-siklus gagal")
require(np.all(np.abs(peta_logistik(SIKLUS_R32, R_DUA_SIKLUS) - SIKLUS_R32) > 0.1), "Titik dua-siklus keliru menjadi titik tetap")
require(abs(PENGALI_R32 - 0.16) < 1e-12, "Pengali dua-siklus berubah")
require(abs(LAMBDA_R32 - LAMBDA_R32_ANALITIK) < 1e-10, "Eksponen Lyapunov r=3.2 tidak cocok dengan rumus periodik")
require(abs(LAMBDA_R4 - np.log(2.0)) < 5e-3, "Estimasi eksponen Lyapunov r=4 keluar dari batas")""",
        ),
        markdown(
            "c3-bifurcation-lyapunov",
            r"""## Diagram bifurkasi dan eksponen Lyapunov

Untuk setiap nilai parameter, 1.500 iterasi dibuang dan 200 iterasi berikutnya dipertahankan. Panel bifurkasi memakai titik, sedangkan panel Lyapunov memakai garis utuh, garis nol putus-putus, dan penanda vertikal dengan pola berbeda. Kepadatan pita bukan ukuran probabilitas. Nilai positif berhingga merupakan bukti kepekaan lokal, bukan bukti tunggal tentang seluruh sistem.

**Deskripsi panjang gambar:** cabang tunggal terbelah menjadi dua di sekitar $r=3$, lalu terbelah berulang sebelum membentuk pita rapat yang diselingi jendela periodik. Kurva Lyapunov negatif di banyak daerah periodik dan positif di banyak pita kacau; ia kembali negatif di sejumlah jendela periodik.""",
        ),
        code(
            "c3-bifurcation-figure",
            """R_GRID = np.linspace(2.8, 4.0, 801)
TRANSIEN_DIAGRAM = 1500
SIMPAN_DIAGRAM = 200
x_grid = np.full(R_GRID.shape, X0_LOGISTIK, dtype=float)
for _ in range(TRANSIEN_DIAGRAM):
    x_grid = peta_logistik(x_grid, R_GRID)

ORBIT_DIAGRAM = np.empty((SIMPAN_DIAGRAM, R_GRID.size), dtype=float)
JUMLAH_LOG_GRID = np.zeros(R_GRID.shape, dtype=float)
for indeks in range(SIMPAN_DIAGRAM):
    besar_turunan = np.abs(turunan_logistik(x_grid, R_GRID))
    with np.errstate(divide="ignore", invalid="ignore"):
        JUMLAH_LOG_GRID += np.log(besar_turunan)
    x_grid = peta_logistik(x_grid, R_GRID)
    ORBIT_DIAGRAM[indeks] = x_grid
LAMBDA_GRID = JUMLAH_LOG_GRID / SIMPAN_DIAGRAM

require(np.all((ORBIT_DIAGRAM >= -1e-14) & (ORBIT_DIAGRAM <= 1.0 + 1e-14)), "Orbit diagram keluar dari interval invarian")
require(not np.isnan(LAMBDA_GRID).any(), "Kurva Lyapunov mengandung NaN")
require(not np.isposinf(LAMBDA_GRID).any(), "Kurva Lyapunov mengandung +tak hingga")

fig1, (ax11, ax12) = plt.subplots(2, 1, figsize=(9.2, 7.0), sharex=True, constrained_layout=True)
ax11.scatter(np.tile(R_GRID, SIMPAN_DIAGRAM), ORBIT_DIAGRAM.ravel(), s=0.16, marker=".", color="#202020", rasterized=True)
ax11.set(ylabel="$x_n$ setelah transien", title="Diagram bifurkasi peta logistik")
lambda_tampil = np.where(np.isfinite(LAMBDA_GRID), LAMBDA_GRID, np.nan)
ax12.plot(R_GRID, lambda_tampil, color="#5b2a86", linewidth=1.2, linestyle="-", label=r"estimasi $\\lambda_N$")
ax12.axhline(0.0, color="#202020", linewidth=1.0, linestyle="--", label=r"$\\lambda=0$")
penanda = ((3.0, "-", "$r=3$"), (1.0 + np.sqrt(6.0), "--", r"$1+\\sqrt{6}$"), (3.569945672, ":", r"$r_\\infty$"))
for nilai, pola, label in penanda:
    ax11.axvline(nilai, color="#7a7a7a", linewidth=0.9, linestyle=pola)
    ax12.axvline(nilai, color="#7a7a7a", linewidth=0.9, linestyle=pola, label=label)
ax12.set(xlabel="parameter kendali $r$", ylabel="eksponen Lyapunov per iterasi")
ax12.legend(ncol=2, fontsize=8)
fig1.canvas.draw()
if matplotlib.get_backend().lower() != "agg":
    plt.show()
plt.close(fig1)""",
        ),
        markdown(
            "c3-lorenz-contract",
            r"""## Sistem Lorenz dan titik kesetimbangan

Notebook mengintegrasikan

$$\dot x=\sigma(y-x),\qquad \dot y=x(\rho-z)-y,\qquad \dot z=xy-\beta z$$

dengan $\sigma=10$, $\rho=28$, $\beta=8/3$, dan kondisi awal $(1,1,1)$. Integrator DOP853 memakai `rtol=1e-10`, `atol=1e-12`, dan `max_step=0.02`. Tiga titik kesetimbangan diperoleh secara analitik dan diperiksa dengan substitusi. Proyeksi $x$–$z$ memperlihatkan dua lobus tanpa mengklaim bahwa lintasan jangka panjang dapat direproduksi titik demi titik pada setiap arsitektur.

**Deskripsi panjang gambar proyeksi Lorenz:** garis lintasan membentuk dua lobus pada bidang $x$–$z$ dan berpindah tidak teratur di antara keduanya. Penanda silang menunjukkan dua titik kesetimbangan tak nol di sekitar $(x,z)=(\pm8.485,27)$, sehingga lintasan dan kesetimbangan dapat dibedakan tanpa mengandalkan warna.""",
        ),
        code(
            "c3-lorenz-integration",
            """SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0
KONDISI_AWAL_LORENZ = np.array([1.0, 1.0, 1.0])
T_LORENZ = np.linspace(0.0, 60.0, 6001)

def ruas_kanan_lorenz(t, keadaan, sigma=SIGMA, rho=RHO, beta=BETA):
    x, y, z = keadaan
    return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])

def perpotongan_z27_naik(t, keadaan):
    return keadaan[2] - 27.0

perpotongan_z27_naik.direction = 1.0
perpotongan_z27_naik.terminal = False

def jalankan_lorenz():
    return solve_ivp(
        ruas_kanan_lorenz,
        (0.0, 60.0),
        KONDISI_AWAL_LORENZ,
        method="DOP853",
        t_eval=T_LORENZ,
        events=perpotongan_z27_naik,
        rtol=1e-10,
        atol=1e-12,
        max_step=0.02,
    )

akar_kesetimbangan = float(np.sqrt(BETA * (RHO - 1.0)))
KESETIMBANGAN = np.array([
    [0.0, 0.0, 0.0],
    [akar_kesetimbangan, akar_kesetimbangan, RHO - 1.0],
    [-akar_kesetimbangan, -akar_kesetimbangan, RHO - 1.0],
])
RESIDU_KESETIMBANGAN = np.array([np.linalg.norm(ruas_kanan_lorenz(0.0, titik)) for titik in KESETIMBANGAN])
SOLUSI_LORENZ = jalankan_lorenz()

require(np.max(RESIDU_KESETIMBANGAN) < 1e-12, "Titik kesetimbangan gagal memenuhi persamaan Lorenz")
require(SOLUSI_LORENZ.success, f"Integrasi Lorenz gagal: {SOLUSI_LORENZ.message}")
require(SOLUSI_LORENZ.y.shape == (3, 6001), "Sensus keluaran Lorenz berbeda")
require(np.isfinite(SOLUSI_LORENZ.y).all(), "Solusi Lorenz mengandung nilai tak hingga atau NaN")

fig2, ax2 = plt.subplots(figsize=(8.4, 4.8), constrained_layout=True)
ax2.plot(SOLUSI_LORENZ.y[0], SOLUSI_LORENZ.y[2], color="#1d5f8a", linewidth=0.55, linestyle="-", label="lintasan")
ax2.scatter(KESETIMBANGAN[1:, 0], KESETIMBANGAN[1:, 2], color="#9c2f2f", marker="x", s=55, label="titik kesetimbangan tak nol")
ax2.set(xlabel="$x$", ylabel="$z$", title="Proyeksi $x$–$z$ lintasan Lorenz")
ax2.legend()
fig2.canvas.draw()
if matplotlib.get_backend().lower() != "agg":
    plt.show()
plt.close(fig2)""",
        ),
        markdown(
            "c3-sensitivity-validation",
            r"""## Kepekaan terhadap kondisi awal setelah pemeriksaan numerik

Solusi utama dibandingkan dengan integrasi yang lebih ketat pada $0\le t\le10$. Setelah selisih rentang pendek berada di bawah ambang, dua kondisi awal yang berbeda hanya $10^{-9}$ pada koordinat $x$ diintegrasikan sebagai satu sistem enam dimensi. Garis utuh dan putus-putus membedakan lintasan tanpa mengandalkan warna; jarak Euklides digambar pada skala logaritmik.

**Deskripsi panjang gambar:** kedua kurva $x(t)$ mula-mula bertumpuk, lalu terpisah secara terlihat. Jarak mulai dekat $10^{-9}$, bertumbuh beberapa orde besaran, melampaui $10^{-3}$ sekitar $t=25.2$, dan menjadi berorde satu sebelum $t=35$. Setelah saturasi, jarak bukan lagi ukuran pertumbuhan gangguan linear.""",
        ),
        code(
            "c3-sensitivity-code",
            """T_PENDEK = np.linspace(0.0, 10.0, 1001)
SOLUSI_HALUS = solve_ivp(
    ruas_kanan_lorenz,
    (0.0, 10.0),
    KONDISI_AWAL_LORENZ,
    method="DOP853",
    t_eval=T_PENDEK,
    rtol=1e-12,
    atol=1e-14,
    max_step=0.01,
)
SELISIH_PEMURNIAN = np.linalg.norm(SOLUSI_LORENZ.y[:, :1001].T - SOLUSI_HALUS.y.T, axis=1)
GALAT_PEMURNIAN_MAKS = float(np.max(SELISIH_PEMURNIAN))

def ruas_kanan_pasangan(t, keadaan):
    return np.concatenate((ruas_kanan_lorenz(t, keadaan[:3]), ruas_kanan_lorenz(t, keadaan[3:])))

T_PASANGAN = np.linspace(0.0, 40.0, 4001)
AWAL_PASANGAN = np.concatenate((KONDISI_AWAL_LORENZ, KONDISI_AWAL_LORENZ + np.array([1e-9, 0.0, 0.0])))
SOLUSI_PASANGAN = solve_ivp(
    ruas_kanan_pasangan,
    (0.0, 40.0),
    AWAL_PASANGAN,
    method="DOP853",
    t_eval=T_PASANGAN,
    rtol=1e-10,
    atol=1e-12,
    max_step=0.02,
)
JARAK_PASANGAN = np.linalg.norm(SOLUSI_PASANGAN.y[:3].T - SOLUSI_PASANGAN.y[3:].T, axis=1)
indeks_ambang = np.flatnonzero(JARAK_PASANGAN > 1e-3)
WAKTU_AMBANG_1E3 = float(T_PASANGAN[indeks_ambang[0]]) if indeks_ambang.size else float("nan")

require(SOLUSI_HALUS.success and SOLUSI_PASANGAN.success, "Integrasi validasi Lorenz gagal")
require(GALAT_PEMURNIAN_MAKS < 1e-6, "Pemurnian integrator tidak konvergen pada rentang pendek")
require(abs(JARAK_PASANGAN[0] - 1e-9) < 1e-15, "Jarak awal pasangan berubah")
require(JARAK_PASANGAN[2000] < 1e-4, "Pasangan terpisah terlalu cepat untuk kontrak kanonik")
require(JARAK_PASANGAN[3500] > 1e-1, "Kepekaan terhadap kondisi awal tidak tampak pada t=35")
require(20.0 < WAKTU_AMBANG_1E3 < 30.0, "Waktu lintas ambang pasangan keluar dari batas")

fig3, (ax31, ax32) = plt.subplots(2, 1, figsize=(9.0, 6.7), sharex=True, constrained_layout=True)
ax31.plot(T_PASANGAN, SOLUSI_PASANGAN.y[0], color="#1d5f8a", linestyle="-", linewidth=0.8, label="kondisi awal pertama")
ax31.plot(T_PASANGAN, SOLUSI_PASANGAN.y[3], color="#a24b2a", linestyle="--", linewidth=0.8, label="kondisi awal kedua")
ax31.set(ylabel="$x(t)$", title="Dua lintasan Lorenz yang mula-mula berdekatan")
ax31.legend()
ax32.semilogy(T_PASANGAN, JARAK_PASANGAN, color="#202020", linestyle="-", linewidth=1.1, label="jarak keadaan")
ax32.axhline(1e-3, color="#7a7a7a", linestyle="--", linewidth=0.9, label="ambang $10^{-3}$")
ax32.set(xlabel="waktu $t$", ylabel="jarak Euklides")
ax32.legend()
fig3.canvas.draw()
if matplotlib.get_backend().lower() != "agg":
    plt.show()
plt.close(fig3)""",
        ),
        markdown(
            "c3-poincare-return",
            r"""## Penampang Poincaré dan proyeksi peta balik

Penampang yang dipakai adalah $z=27$ dengan arah naik, yaitu $\dot z>0$. Perpotongan sebelum $t=30$ dibuang sebagai transien. Peta Poincaré penuh membawa $(x_n,y_n)$ ke $(x_{n+1},y_{n+1})$. Plot kedua hanya memakai $u_n=x_n$, sehingga harus disebut proyeksi peta balik dan tidak selalu merupakan fungsi satu dimensi yang tunggal.

**Deskripsi panjang gambar:** panel kiri memperlihatkan lingkaran pada dua gugus penampang, satu dengan $x<0$ dan satu dengan $x>0$. Panel kanan memperlihatkan segitiga pada pasangan $(x_n,x_{n+1})$ serta garis diagonal putus-putus. Cabang yang berbeda menunjukkan pergantian atau pengulangan lobus; proyeksi dapat menumpuk titik yang berbeda dalam koordinat $y$.""",
        ),
        code(
            "c3-poincare-code",
            """WAKTU_PERPOTONGAN_SEMUA = SOLUSI_LORENZ.t_events[0]
KEADAAN_PERPOTONGAN_SEMUA = SOLUSI_LORENZ.y_events[0]
mask_transien = WAKTU_PERPOTONGAN_SEMUA >= 30.0
WAKTU_PERPOTONGAN = WAKTU_PERPOTONGAN_SEMUA[mask_transien]
KEADAAN_PERPOTONGAN = KEADAAN_PERPOTONGAN_SEMUA[mask_transien]
TURUNAN_Z_PERPOTONGAN = np.array([
    ruas_kanan_lorenz(t, keadaan)[2]
    for t, keadaan in zip(WAKTU_PERPOTONGAN, KEADAAN_PERPOTONGAN)
])
GALAT_BIDANG_MAKS = float(np.max(np.abs(KEADAAN_PERPOTONGAN[:, 2] - 27.0)))
X_PERPOTONGAN = KEADAAN_PERPOTONGAN[:, 0]
PASANGAN_BALIK = np.column_stack((X_PERPOTONGAN[:-1], X_PERPOTONGAN[1:]))

require(WAKTU_PERPOTONGAN.size >= 30, "Perpotongan setelah transien terlalu sedikit")
require(np.all(np.diff(WAKTU_PERPOTONGAN) > 0.0), "Waktu perpotongan tidak meningkat ketat")
require(GALAT_BIDANG_MAKS < 1e-8, "Interpolasi perpotongan tidak berada pada z=27")
require(np.all(TURUNAN_Z_PERPOTONGAN > 0.0), "Penampang memuat perpotongan dengan arah yang salah")
require(np.min(X_PERPOTONGAN) < -8.0 and np.max(X_PERPOTONGAN) > 8.0, "Kedua lobus Lorenz tidak terwakili")
require(PASANGAN_BALIK.shape == (WAKTU_PERPOTONGAN.size - 1, 2), "Sensus pasangan balik berbeda")
require(np.isfinite(PASANGAN_BALIK).all(), "Peta balik mengandung nilai tak hingga atau NaN")

fig4, (ax41, ax42) = plt.subplots(1, 2, figsize=(10.0, 4.2), constrained_layout=True)
ax41.scatter(KEADAAN_PERPOTONGAN[:, 0], KEADAAN_PERPOTONGAN[:, 1], marker="o", facecolors="none", edgecolors="#1d5f8a", label="perpotongan naik")
ax41.set(xlabel="$x$ pada $z=27$", ylabel="$y$ pada $z=27$", title="Penampang Poincaré")
ax41.legend()
ax42.scatter(PASANGAN_BALIK[:, 0], PASANGAN_BALIK[:, 1], marker="^", color="#8b2e4f", label="pasangan berurutan")
batas = float(np.max(np.abs(PASANGAN_BALIK)))
ax42.plot([-batas, batas], [-batas, batas], color="#303030", linestyle="--", linewidth=0.9, label="$x_{n+1}=x_n$")
ax42.set(xlabel="$x_n$", ylabel="$x_{n+1}$", title="Proyeksi peta balik")
ax42.legend()
fig4.canvas.draw()
if matplotlib.get_backend().lower() != "agg":
    plt.show()
plt.close(fig4)""",
        ),
        markdown(
            "c3-summary-replay",
            r"""## Ringkasan dan verifikasi ulang

Ringkasan membedakan sidik numerik lingkungan kanonik dari gerbang ilmiah yang lebih portabel. Hitungan perpotongan tepat dan perpotongan pertama dicatat sebagai sidik lingkungan, bukan sebagai invarians matematika. Sel terakhir mengulang perhitungan inti melalui fungsi murni dalam kernel yang sama; gerbang QA eksternal tetap harus memulai kernel Jupyter baru.""",
        ),
        code(
            "c3-summary-replay-code",
            """RINGKASAN = {
    "unit_id": "O005-BRIDGE-C3",
    "logistic": {
        "r_3_2_cycle": [round(float(nilai), 8) for nilai in SIKLUS_R32],
        "r_3_2_multiplier": round(PENGALI_R32, 8),
        "lambda_r_3_2": round(LAMBDA_R32, 8),
        "lambda_r_4_finite": round(LAMBDA_R4, 8),
    },
    "lorenz": {
        "equilibrium_a": round(akar_kesetimbangan, 8),
        "equilibrium_max_residual": float(np.max(RESIDU_KESETIMBANGAN)),
        "short_horizon_refinement_max_norm": GALAT_PEMURNIAN_MAKS,
        "paired_distance_t20": float(JARAK_PASANGAN[2000]),
        "paired_distance_t35": float(JARAK_PASANGAN[3500]),
        "first_time_distance_gt_1e-3": WAKTU_AMBANG_1E3,
    },
    "poincare": {
        "all_upward_crossings": int(WAKTU_PERPOTONGAN_SEMUA.size),
        "post_transient_crossings": int(WAKTU_PERPOTONGAN.size),
        "return_pairs": int(PASANGAN_BALIK.shape[0]),
        "section_max_abs_error": GALAT_BIDANG_MAKS,
        "minimum_z_derivative": float(np.min(TURUNAN_Z_PERPOTONGAN)),
        "first_retained_time": float(WAKTU_PERPOTONGAN[0]),
        "first_retained_state": [float(nilai) for nilai in KEADAAN_PERPOTONGAN[0]],
    },
    "versions": VERSIONS,
}

require(RINGKASAN["logistic"]["r_3_2_cycle"] == [0.51304451, 0.79945549], "Sidik dua-siklus berubah")
require(RINGKASAN["logistic"]["r_3_2_multiplier"] == 0.16, "Sidik pengali berubah")
require(RINGKASAN["logistic"]["lambda_r_3_2"] == -0.91629073, "Sidik lambda r=3.2 berubah")
require(RINGKASAN["logistic"]["lambda_r_4_finite"] == 0.69317558, "Sidik lambda r=4 berubah")

SIKLUS_ULANG = dua_siklus_analitik(R_DUA_SIKLUS)
LAMBDA_R32_ULANG = estimasi_lyapunov_peta(R_DUA_SIKLUS, X0_LOGISTIK, TRANSIEN_LYAPUNOV, ITERASI_LYAPUNOV)
LAMBDA_R4_ULANG = estimasi_lyapunov_peta(4.0, X0_LOGISTIK, TRANSIEN_LYAPUNOV, ITERASI_LYAPUNOV)
SOLUSI_LORENZ_ULANG = jalankan_lorenz()
require(np.array_equal(SIKLUS_ULANG, SIKLUS_R32), "Dua-siklus berubah dalam kernel yang sama")
require(LAMBDA_R32_ULANG == LAMBDA_R32 and LAMBDA_R4_ULANG == LAMBDA_R4, "Estimasi Lyapunov berubah dalam kernel yang sama")
require(np.array_equal(SOLUSI_LORENZ_ULANG.y, SOLUSI_LORENZ.y), "Lintasan Lorenz berubah dalam kernel yang sama")
require(np.array_equal(SOLUSI_LORENZ_ULANG.t_events[0], WAKTU_PERPOTONGAN_SEMUA), "Kejadian Poincaré berubah dalam kernel yang sama")

print("RINGKASAN_C3_JSON")
print(json.dumps(RINGKASAN, ensure_ascii=False, sort_keys=True, indent=2))
print("Verifikasi ulang deterministik C3 dalam kernel yang sama lulus.")""",
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
                "notebook_id": "O005-BRIDGE-C3-NB01",
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
                "external_data_or_assets": False,
                "model_identification": "OpenAI Codex gpt-5.6-sol, Ultra.",
                "license": "CC BY-NC-SA 4.0",
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
            "problem_summary": "Buktikan invariansi interval keadaan peta logistik dan identifikasi batas parameter yang dipakai.",
            "article_link_ids": [],
            "source_formula_occurrences": [
                r"\(x_{n+1}=r x_n(1-x_n)\)",
                r"\(0\le x(1-x)\le \frac{1}{4}\)",
            ],
            "provenance": provenance(),
            "hint": {"text": r"Cari nilai minimum dan maksimum \(x(1-x)\) pada interval \([0,1]\), lalu kalikan dengan \(r\)."},
            "check": {
                "type": "structured",
                "final_answer": r"Untuk \(0 \le r \le 4\) dan \(x \in [0,1]\), berlaku \(0 \le f_r(x) \le \frac{r}{4} \le 1\); jika \(r>4\), batas atas \(\frac{r}{4} \le 1\) tidak lagi tersedia.",
                "required_evidence": [
                    r"\(x(1-x)\) tidak negatif pada \([0,1]\).",
                    r"Nilai maksimum \(x(1-x)\) adalah \(\frac{1}{4}\) pada \(x=\frac{1}{2}\).",
                    "Kesimpulan berlaku untuk setiap iterasi melalui induksi.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    r"Faktorkan \(x(1-x)\) dan gunakan \(0 \le x \le 1\) untuk memperoleh ketaknegatifan.",
                    r"Turunan \(1-2x\) lenyap pada \(x=\frac{1}{2}\), tempat maksimum bernilai \(\frac{1}{4}\).",
                    r"Maka \(0 \le r x(1-x) \le \frac{r}{4} \le 1\) ketika \(0 \le r \le 4\).",
                    r"Jika satu keadaan berada di \([0,1]\), keadaan berikutnya juga; induksi mempertahankan seluruh orbit.",
                    r"Untuk \(r>4\), \(x=\frac{1}{2}\) dipetakan ke \(\frac{r}{4}>1\), sehingga interval tidak invarian.",
                ],
                "conclusion": r"\([0,1]\) adalah interval invarian tepat di bawah kontrak parameter yang dinyatakan.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P02",
            "ordinal": 2,
            "problem_summary": "Turunkan titik tetap peta logistik dan interval kestabilan lokalnya.",
            "article_link_ids": [],
            "source_formula_occurrences": [
                r"\(x^\ast=r x^\ast(1-x^\ast)\)",
                r"\(f_r'(x)=r(1-2x)\)",
            ],
            "provenance": provenance(),
            "hint": {"text": "Faktorkan persamaan titik tetap, lalu terapkan syarat nilai mutlak pengali kurang dari satu."},
            "check": {
                "type": "quantitative",
                "final_answer": r"Untuk \(r=0\) hanya \(x^\ast=0\) dan rumus \(1-\frac{1}{r}\) tidak terdefinisi. Titik \(x^\ast=0\) stabil pada \(0 \le r<1\). Pada \(r=1\) cabang kedua berimpit dengan \(x^\ast=0\) dan pengali \(+1\) membuat titik itu nonhiperbolik. Untuk \(r>0\), titik \(x^\ast=1-\frac{1}{r}\) stabil pada \(1<r<3\). Pada \(r=3\) pengalinya \(-1\), titik tetap nonhiperbolik, dan rumus calon dua-siklus berimpit di \(x^\ast=\frac{2}{3}\); dua titik berbeda berperiode prima dua baru ada untuk \(r>3\).",
                "required_evidence": [
                    r"Kasus \(r=0\) dipisahkan sebelum pembagian dengan \(r\); hanya \(x^\ast=0\) yang berlaku.",
                    r"Untuk \(r>0\), kedua solusi persamaan \(x^\ast=f_r(x^\ast)\) diperoleh.",
                    r"Pengali masing-masing adalah \(r\) dan \(2-r\).",
                    r"Syarat \(\lvert\mu\rvert<1\) diterapkan tanpa memasukkan titik batas.",
                    r"Pada \(r=3\), akar calon dua-siklus berimpit di \(\frac{2}{3}\) dan belum membentuk orbit prima dua.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    r"Tulis \(x^\ast[r(1-x^\ast)-1]=0\); untuk \(r=0\) persamaan hanya memberi \(x^\ast=0\), sedangkan untuk \(r>0\) solusi kedua adalah \(x^\ast=1-\frac{1}{r}\).",
                    r"Evaluasi \(f_r'(x)=r(1-2x)\) di kedua titik.",
                    r"Untuk titik nol, \(\lvert r\rvert<1\) memberi \(0 \le r<1\) dalam domain fisik.",
                    r"Untuk titik tak nol, \(\lvert 2-r\rvert<1\) memberi \(1<r<3\).",
                    r"Pada \(r=1\) atau \(r=3\), pengali masing-masing \(+1\) atau \(-1\) sehingga uji hiperbolik tidak memutuskan kestabilan melalui pertidaksamaan ketat.",
                    r"Substitusi \(r=3\) ke rumus calon dua-siklus memberi dua akar sama, \(\frac{2}{3}\); dua titik berbeda berperiode prima dua memerlukan \(r>3\).",
                ],
                "conclusion": r"Kasus \(r=0\) harus dipisahkan dari rumus yang membagi dengan \(r\); pada \(r=3\) cabang calon dua-siklus baru berimpit dan orbit prima dua yang berbeda muncul hanya untuk \(r>3\).",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P03",
            "ordinal": 3,
            "problem_summary": r"Hitung orbit dua-siklus, pengali, dan eksponen Lyapunov pada \(r=3.2\).",
            "article_link_ids": [],
            "source_formula_occurrences": [
                r"\(x_{\pm}=\frac{r+1\pm\sqrt{(r-3)(r+1)}}{2r}\)",
                r"\(\lambda=\frac{1}{2}\log\lvert\mu_2\rvert\)",
            ],
            "provenance": provenance(),
            "hint": {"text": "Gunakan rumus dua-siklus, lalu kalikan turunan pada kedua titik sebelum mengambil setengah logaritma."},
            "check": {
                "type": "quantitative",
                "final_answer": r"\(x_-=0.51304451\), \(x_+=0.79945549\), \(\mu_2=0.16\), dan \(\lambda=-0.91629073\) per iterasi.",
                "tolerances": {
                    "state_absolute": 1e-8,
                    "multiplier_absolute": 1e-12,
                    "lyapunov_absolute": 1e-8,
                },
                "formula": r"\mu_2=f'(x_-)f'(x_+);\quad \lambda=\frac{1}{2}\log\lvert\mu_2\rvert",
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    r"Substitusikan \(r=3.2\) ke rumus \(x_\pm\).",
                    r"Periksa \(f(x_-)=x_+\) dan \(f(x_+)=x_-\).",
                    r"Gunakan \(\mu_2=-r^2+2r+4\) untuk memperoleh \(0.16\).",
                    r"Hitung \(\lambda=\frac{1}{2}\log(0.16)=-0.9162907319\).",
                ],
                "conclusion": r"Orbit berganti titik pada setiap iterasi, tetapi \(\lvert\mu_2\rvert<1\) membuat gangguan menyusut setelah satu putaran dua langkah.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P04",
            "ordinal": 4,
            "problem_summary": "Bandingkan eksponen Lyapunov periodik dan kacau serta batasi klaim dari estimasi berhingga.",
            "article_link_ids": [],
            "source_formula_occurrences": [
                r"\(\lambda_N=\frac{1}{N}\sum \log\lvert f_r'(x_n)\rvert\)"
            ],
            "provenance": provenance(),
            "hint": {"text": r"Pisahkan arti tanda estimasi dari kekuatan logis bukti yang hanya memakai satu orbit dan \(N\) berhingga."},
            "check": {
                "type": "structured",
                "final_answer": r"Nilai negatif pada \(r=3.2\) menunjukkan kontraksi menuju dua-siklus; nilai positif sekitar \(\log 2\) pada \(r=4\) menunjukkan pemisahan lokal rata-rata, tetapi hasil berhingga tidak mencakup semua kondisi awal atau membuktikan seluruh struktur asimtotik.",
                "required_evidence": [
                    r"Nilai \(r=3.2\) sekitar \(-0.91629073\).",
                    r"Nilai \(r=4\) sekitar \(0.69317558\) dan dekat \(\log 2\).",
                    "Transien, panjang orbit, kondisi awal khusus, dan presisi terbatas disebut sebagai batas.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    r"Hubungkan \(\lambda<0\) dengan kontraksi rata-rata pada orbit periodik.",
                    r"Hubungkan \(\lambda>0\) dengan pertumbuhan gangguan kecil secara lokal.",
                    r"Bandingkan estimasi pada \(r=4\) dengan \(\log 2\) menggunakan toleransi, bukan kesamaan digit mutlak.",
                    "Nyatakan bahwa satu orbit berhingga tidak mengecualikan kondisi awal istimewa atau jendela periodik pada parameter lain.",
                ],
                "conclusion": "Eksponen Lyapunov adalah diagnostik kuat ketika kontraknya jelas, bukan label otomatis dari satu grafik.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P05",
            "ordinal": 5,
            "problem_summary": "Turunkan dan periksa titik kesetimbangan sistem Lorenz kanonik.",
            "article_link_ids": [],
            "source_formula_occurrences": [
                r"\(\dot{x}=\sigma(y-x)\)",
                r"\(\dot{y}=x(\rho-z)-y\)",
                r"\(\dot{z}=xy-\beta z\)",
            ],
            "provenance": provenance(),
            "hint": {"text": r"Dari \(\dot{x}=0\) peroleh \(y=x\); kemudian pisahkan kasus \(x=0\) dan \(x\ne0\)."},
            "check": {
                "type": "quantitative",
                "final_answer": r"Titiknya \((0,0,0)\) dan \((\pm\sqrt{72},\pm\sqrt{72},27)\), dengan \(\sqrt{72}=8.48528137\); norma residu numerik kurang dari \(10^{-12}\).",
                "tolerances": {"state_absolute": 1e-8, "residual_norm_max": 1e-12},
                "formula": r"(0,0,0),\ (\pm\sqrt{\beta(\rho-1)},\pm\sqrt{\beta(\rho-1)},\rho-1)",
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    r"Dari \(\sigma(y-x)=0\) dan \(\sigma\ne0\), tetapkan \(y=x\).",
                    r"Persamaan kedua menjadi \(x(\rho-z-1)=0\).",
                    r"Kasus \(x=0\) memberi \(y=z=0\).",
                    r"Kasus \(x\ne0\) memberi \(z=\rho-1\) dan \(x^2=\beta(\rho-1)\).",
                    r"Substitusi parameter memberi \(z=27\) dan \(x=y=\pm\sqrt{72}\).",
                ],
                "conclusion": "Ketiga titik membuat ruas kanan nol dalam toleransi aritmetika pecahan mengambang.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P06",
            "ordinal": 6,
            "problem_summary": "Bedakan ketidakakuratan integrator dari kepekaan dinamik pada sistem Lorenz.",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": "Bandingkan solusi untuk keadaan awal yang sama terlebih dahulu; baru setelah konvergensi rentang pendek lulus, bandingkan keadaan awal yang berbeda."},
            "check": {
                "type": "structured",
                "final_answer": r"Notebook menuntut selisih solusi utama dan solusi dipermurni kurang dari \(10^{-6}\) pada \(t \le 10\), lalu menunjukkan pasangan berjarak awal \(10^{-9}\) masih dekat pada \(t=20\) tetapi berjarak lebih dari \(0.1\) pada \(t=35\).",
                "required_evidence": [
                    "Metode, rtol, atol, dan max_step kedua integrasi disebutkan.",
                    "Dua kondisi awal diintegrasikan sebagai satu sistem enam dimensi dengan riwayat langkah bersama.",
                    "Pertumbuhan setelah konvergensi rentang pendek tidak disamakan dengan galat solver.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Integrasikan kondisi awal yang sama dengan konfigurasi utama dan konfigurasi lebih ketat.",
                    r"Periksa norma selisih maksimum pada rentang pendek terhadap ambang \(10^{-6}\).",
                    r"Integrasikan dua kondisi awal yang berbeda \(10^{-9}\) dalam satu sistem gabungan.",
                    r"Periksa bahwa jarak pada \(t=20\) masih di bawah \(10^{-4}\) dan jarak pada \(t=35\) di atas \(10^{-1}\).",
                    "Batasi kesimpulan setelah jarak mencapai skala atraktor karena pendekatan linear telah jenuh.",
                ],
                "conclusion": "Urutan pemeriksaan memungkinkan kepekaan dinamik dibedakan dari kegagalan konvergensi numerik.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P07",
            "ordinal": 7,
            "problem_summary": "Jalankan seluruh alur C3 dan audit penampang serta proyeksi peta balik.",
            "article_link_ids": [],
            "source_formula_occurrences": [
                r"\(S=\{(x,y,z)\mid z=27,\ \dot{z}>0\}\)",
                r"\(P(x_n,y_n)=(x_{n+1},y_{n+1})\)",
            ],
            "provenance": provenance(),
            "hint": {"text": "Bedakan sidik lingkungan kanonik—misalnya jumlah tepat—dari gerbang struktural seperti arah, galat bidang, dan keberadaan kedua lobus."},
            "check": {
                "type": "executable",
                "final_answer": r"Lingkungan kanonik memberi \(\lambda=-0.91629073\) dan \(\lambda=0.69317558\), galat pemurnian sekitar \(1.11\times10^{-8}\), ambang jarak pada \(t=25.2\), 40 perpotongan setelah transien, galat bidang di bawah \(10^{-8}\), dan 39 pasangan balik.",
                "notebook_check": "Semua sel berjalan dari kernel baru, menghasilkan empat keluaran PNG, memenuhi gerbang portabel, dan menyelesaikan verifikasi ulang deterministik.",
                "required_evidence": [
                    r"Semua perpotongan mempunyai waktu meningkat, \(z\approx27\), dan \(\dot{z}>0\).",
                    r"Nilai \(x\) perpotongan mencakup kedua tanda dan kedua lobus.",
                    "Jumlah pasangan balik tepat satu kurang dari jumlah perpotongan.",
                    r"Plot \(x_{n+1}\) terhadap \(x_n\) disebut proyeksi karena koordinat \(y\) dibuang.",
                ],
                "tolerances": {
                    "lyapunov_absolute": 1e-8,
                    "solver_norm_max": 1e-6,
                    "section_absolute": 1e-8,
                    "time_absolute": 0.1,
                },
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Mulai kernel baru dan jalankan semua sel secara berurutan.",
                    r"Cocokkan dua eksponen Lyapunov dan pastikan pemeriksaan analitik pada \(r=3.2\) lulus.",
                    "Catat galat pemurnian dan waktu lintas ambang pasangan.",
                    "Periksa orientasi, residu bidang, kedua lobus, dan sensus perpotongan.",
                    r"Bentuk pasangan \((x_n,x_{n+1})\) dan bandingkan jumlahnya dengan sensus perpotongan.",
                    r"Jelaskan bahwa peta penuh bekerja pada pasangan \((x,y)\), sehingga proyeksi \(x\) dapat kehilangan informasi.",
                ],
                "conclusion": "Alur yang lulus mengikat gambar pada persamaan, konfigurasi solver, peristiwa berarah, dan pemeriksaan numerik yang dinyatakan.",
            },
            "notebook": {
                "path": "source/id-ID/O005-BRIDGE-C3/notebooks/bridge-c3-chaos-and-return-maps.ipynb",
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
            "relationship": "independent_supplement",
            "license": "CC BY-NC-SA 4.0",
        },
        "provenance_policy": {
            "model_identification": "OpenAI Codex gpt-5.6-sol, Ultra.",
            "source_author_credit_preserved": True,
            "non_endorsement": True,
            "external_data_or_assets": False,
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
        raise SystemExit("Generated C3 inputs differ: " + ", ".join(mismatches))


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
