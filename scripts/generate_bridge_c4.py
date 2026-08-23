#!/usr/bin/env python3
"""Generate the deterministic C4 notebook, mastery layer, and 57-entry lock."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIT_ID = "O005-BRIDGE-C4"
NOTEBOOK = (
    ROOT
    / "source"
    / "id-ID"
    / UNIT_ID
    / "notebooks"
    / "bridge-c4-calibration-validation-uncertainty.ipynb"
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
            "c4-title",
            """# O005-BRIDGE-C4 — Kalibrasi, Identifiabilitas, Validasi, dan Ketidakpastian Model

Notebook ini adalah tambahan independen untuk edisi Bahasa Indonesia *Introduction to Mathematical Modeling*. Satu contoh populasi sintetis dipakai dari awal hingga akhir untuk membedakan identifiabilitas struktural dan praktis, mengalibrasi model eksponensial serta logistik, memeriksa residu dan data uji, membandingkan AICc, dan menghitung ketidakpastian kondisional. Data sintetis bukan bukti biologis.

Produksi dan QA: OpenAI Codex gpt-5.6-sol, Ultra. Kredit Joceline Lega dan University of Arizona untuk buku sumber tetap terpisah dan tidak tersirat sebagai dukungan terhadap tambahan ini. Distribusi mengikuti CC BY-NC-SA 4.0.""",
        ),
        code(
            "c4-environment",
            """import hashlib
import json
import platform

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.optimize import least_squares

EXPECTED_VERSIONS = {
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

require(VERSIONS == EXPECTED_VERSIONS, f"Lingkungan berbeda: {VERSIONS!r} != {EXPECTED_VERSIONS!r}")""",
        ),
        markdown(
            "c4-contract",
            r"""## Pertanyaan dan kontrak model

Pertanyaannya ialah apakah model yang dikalibrasi pada hari 0–16 dapat memprediksi populasi pada hari 18–24. Pengamatan mengikuti $y_i=N(t_i)+\varepsilon_i$, dengan galat normal yang saling bebas, bererata nol, dan bervarians konstan. Nilai $N_0=5$ juta sel diketahui secara independen, sedangkan $y_0$ tetap merupakan pengamatan bising.

Kandidat eksponensial dan logistik adalah

$$N_E(t;r)=N_0e^{rt},\qquad N_L(t;r,K)=\frac{K}{1+(K/N_0-1)e^{-rt}}.$$

Parameter pembangkit data hanya berfungsi sebagai asal-usul data sintetis; estimator tidak membacanya sebagai masukan.""",
        ),
        code(
            "c4-functions",
            """UNIT_ID = "O005-BRIDGE-C4"
DATA_SEED = 20260823
BOOTSTRAP_SEED = 20260824
BOOTSTRAP_REPLICATES = 400
N0_MILLION = 5.0
TRUE_R_PER_DAY = 0.28
TRUE_K_MILLION = 180.0
TRUE_NOISE_SD_MILLION = 2.5
CANONICAL_K_UPPER_BOUND = 1000.0
# Gerbang QA boleh mengganti hanya nilai berikut menjadi 2000.0.
BATAS_K_ATAS = CANONICAL_K_UPPER_BOUND
CANONICAL_DATA_SHA256 = "932d0d27c2917936b0aa51d283d7b2fe2a5eba95989a6c785fa32d3d18dd2811"

SOLVER_OPTIONS = {
    "xtol": 1e-13,
    "ftol": 1e-13,
    "gtol": 1e-13,
    "max_nfev": 10000,
}

def model_eksponensial(waktu_hari, r_per_hari, n0_juta=N0_MILLION):
    waktu = np.asarray(waktu_hari, dtype=float)
    return n0_juta * np.exp(r_per_hari * waktu)

def model_logistik(waktu_hari, r_per_hari, k_juta, n0_juta=N0_MILLION):
    waktu = np.asarray(waktu_hari, dtype=float)
    penyebut = 1.0 + (k_juta / n0_juta - 1.0) * np.exp(-r_per_hari * waktu)
    return k_juta / penyebut

def serialisasi_csv(waktu_hari, populasi_juta):
    baris = ["time_day,population_million_cells"]
    baris.extend(f"{t:.1f},{y:.6f}" for t, y in zip(waktu_hari, populasi_juta))
    return "\\n".join(baris) + "\\n"

def buat_data(seed=DATA_SEED):
    rng = np.random.default_rng(seed)
    waktu = np.arange(0.0, 26.0, 2.0)
    bersih = model_logistik(waktu, TRUE_R_PER_DAY, TRUE_K_MILLION)
    # Nilai yang dianalisis sama persis dengan nilai enam-desimal yang di-hash.
    amatan = np.round(bersih + rng.normal(0.0, TRUE_NOISE_SD_MILLION, waktu.size), 6)
    csv_text = serialisasi_csv(waktu, amatan)
    identitas = hashlib.sha256(csv_text.encode("utf-8")).hexdigest()
    return waktu, amatan, csv_text, identitas

def pasang_eksponensial(waktu, amatan, indeks):
    hasil = least_squares(
        lambda q: model_eksponensial(waktu[indeks], q[0]) - amatan[indeks],
        x0=np.array([0.2]),
        bounds=(np.array([0.01]), np.array([1.0])),
        **SOLVER_OPTIONS,
    )
    require(hasil.success, f"Pencocokan eksponensial gagal: {hasil.message}")
    return hasil

def pasang_logistik(waktu, amatan, indeks, batas_k_atas):
    hasil = least_squares(
        lambda q: model_logistik(waktu[indeks], q[0], q[1]) - amatan[indeks],
        x0=np.array([0.25, 150.0]),
        bounds=(np.array([0.01, 10.0]), np.array([1.0, batas_k_atas])),
        x_scale="jac",
        **SOLVER_OPTIONS,
    )
    require(hasil.success, f"Pencocokan logistik gagal: {hasil.message}")
    return hasil

def ringkas_model(waktu, amatan, indeks_kalibrasi, indeks_uji, prediksi, jumlah_parameter_dinamik):
    residu_kalibrasi = amatan[indeks_kalibrasi] - prediksi[indeks_kalibrasi]
    residu_uji = amatan[indeks_uji] - prediksi[indeks_uji]
    rss = float(residu_kalibrasi @ residu_kalibrasi)
    n = int(indeks_kalibrasi.size)
    k_aicc = int(jumlah_parameter_dinamik + 1)  # termasuk varians residu
    aicc = float(n * np.log(rss / n) + 2 * k_aicc + 2 * k_aicc * (k_aicc + 1) / (n - k_aicc - 1))
    return {
        "rss": rss,
        "rmse_kalibrasi": float(np.sqrt(np.mean(residu_kalibrasi**2))),
        "rerata_residu_kalibrasi": float(np.mean(residu_kalibrasi)),
        "kemiringan_residu_waktu": float(np.polyfit(waktu[indeks_kalibrasi], residu_kalibrasi, 1)[0]),
        "mae_uji": float(np.mean(np.abs(residu_uji))),
        "bias_uji": float(np.mean(residu_uji)),
        "galat_uji_maksimum": float(np.max(np.abs(residu_uji))),
        "aicc": aicc,
        "residu_kalibrasi": residu_kalibrasi,
        "residu_uji": residu_uji,
    }

def sensitivitas_log_parameter(waktu, r_per_hari, k_juta):
    waktu = np.asarray(waktu, dtype=float)
    eksponen = np.exp(-r_per_hari * waktu)
    penyebut = 1.0 + (k_juta / N0_MILLION - 1.0) * eksponen
    turunan_r = k_juta * (k_juta / N0_MILLION - 1.0) * waktu * eksponen / penyebut**2
    turunan_k = (1.0 - eksponen) / penyebut**2
    return np.column_stack((r_per_hari * turunan_r, k_juta * turunan_k))

def bootstrap_parametrik(waktu, indeks_kalibrasi, indeks_uji, parameter_hat, sigma_hat, batas_k_atas):
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    parameter = []
    respons_laten = []
    pengamatan_mendatang = []
    keberhasilan = 0
    pusat_kalibrasi = model_logistik(waktu[indeks_kalibrasi], *parameter_hat)
    for _ in range(BOOTSTRAP_REPLICATES):
        semu = pusat_kalibrasi + rng.normal(0.0, sigma_hat, indeks_kalibrasi.size)
        hasil = least_squares(
            lambda q: model_logistik(waktu[indeks_kalibrasi], q[0], q[1]) - semu,
            x0=np.asarray(parameter_hat, dtype=float),
            bounds=(np.array([0.01, 10.0]), np.array([1.0, batas_k_atas])),
            x_scale="jac",
            **SOLVER_OPTIONS,
        )
        if hasil.success:
            keberhasilan += 1
        parameter.append(hasil.x)
        laten = model_logistik(waktu[indeks_uji], *hasil.x)
        respons_laten.append(laten)
        # Urutan konsumsi RNG ini merupakan bagian dari kontrak kanonik.
        pengamatan_mendatang.append(laten + rng.normal(0.0, sigma_hat, indeks_uji.size))
    return {
        "parameter": np.asarray(parameter),
        "respons_laten": np.asarray(respons_laten),
        "pengamatan_mendatang": np.asarray(pengamatan_mendatang),
        "keberhasilan": keberhasilan,
    }

def jalankan_analisis(batas_k_atas=BATAS_K_ATAS):
    waktu, amatan, csv_text, data_sha256 = buat_data()
    indeks_kalibrasi = np.flatnonzero(waktu <= 16.0)
    indeks_uji = np.flatnonzero(waktu >= 18.0)
    indeks_awal = np.flatnonzero(waktu <= 10.0)

    fit_eksponensial = pasang_eksponensial(waktu, amatan, indeks_kalibrasi)
    fit_logistik = pasang_logistik(waktu, amatan, indeks_kalibrasi, batas_k_atas)
    fit_logistik_awal = pasang_logistik(waktu, amatan, indeks_awal, batas_k_atas)
    prediksi_eksponensial = model_eksponensial(waktu, *fit_eksponensial.x)
    prediksi_logistik = model_logistik(waktu, *fit_logistik.x)
    metrik_eksponensial = ringkas_model(
        waktu, amatan, indeks_kalibrasi, indeks_uji, prediksi_eksponensial, 1
    )
    metrik_logistik = ringkas_model(
        waktu, amatan, indeks_kalibrasi, indeks_uji, prediksi_logistik, 2
    )

    sensitivitas_awal = sensitivitas_log_parameter(waktu[indeks_awal], *fit_logistik.x)
    sensitivitas_kalibrasi = sensitivitas_log_parameter(waktu[indeks_kalibrasi], *fit_logistik.x)
    kondisi_awal = float(np.linalg.cond(sensitivitas_awal))
    kondisi_kalibrasi = float(np.linalg.cond(sensitivitas_kalibrasi))

    derajat_bebas = indeks_kalibrasi.size - fit_logistik.x.size
    sigma_hat = float(np.sqrt(metrik_logistik["rss"] / derajat_bebas))
    kovariansi = sigma_hat**2 * np.linalg.inv(fit_logistik.jac.T @ fit_logistik.jac)
    galat_baku = np.sqrt(np.diag(kovariansi))
    korelasi_parameter = float(kovariansi[0, 1] / (galat_baku[0] * galat_baku[1]))

    bootstrap = bootstrap_parametrik(
        waktu, indeks_kalibrasi, indeks_uji, fit_logistik.x, sigma_hat, batas_k_atas
    )
    kuantil_parameter = np.quantile(
        bootstrap["parameter"], [0.025, 0.5, 0.975], axis=0, method="linear"
    )
    kuantil_laten = np.quantile(
        bootstrap["respons_laten"], [0.025, 0.5, 0.975], axis=0, method="linear"
    )
    kuantil_prediksi = np.quantile(
        bootstrap["pengamatan_mendatang"], [0.025, 0.5, 0.975], axis=0, method="linear"
    )
    tercakup = (
        (amatan[indeks_uji] >= kuantil_prediksi[0])
        & (amatan[indeks_uji] <= kuantil_prediksi[2])
    )

    return {
        "waktu": waktu,
        "amatan": amatan,
        "csv_text": csv_text,
        "data_sha256": data_sha256,
        "indeks_kalibrasi": indeks_kalibrasi,
        "indeks_uji": indeks_uji,
        "indeks_awal": indeks_awal,
        "fit_eksponensial": fit_eksponensial,
        "fit_logistik": fit_logistik,
        "fit_logistik_awal": fit_logistik_awal,
        "prediksi_eksponensial": prediksi_eksponensial,
        "prediksi_logistik": prediksi_logistik,
        "metrik_eksponensial": metrik_eksponensial,
        "metrik_logistik": metrik_logistik,
        "sensitivitas_awal": sensitivitas_awal,
        "sensitivitas_kalibrasi": sensitivitas_kalibrasi,
        "kondisi_awal": kondisi_awal,
        "kondisi_kalibrasi": kondisi_kalibrasi,
        "sigma_hat": sigma_hat,
        "galat_baku": galat_baku,
        "korelasi_parameter": korelasi_parameter,
        "bootstrap": bootstrap,
        "kuantil_parameter": kuantil_parameter,
        "kuantil_laten": kuantil_laten,
        "kuantil_prediksi": kuantil_prediksi,
        "tercakup": tercakup,
        "batas_k_atas": float(batas_k_atas),
    }""",
        ),
        markdown(
            "c4-data-split",
            """## Data, pembagian, dan kalibrasi

Tiga belas waktu pengamatan ditentukan terlebih dahulu. Sembilan titik hingga hari ke-16 menjadi data kalibrasi dan empat titik setelahnya menjadi data uji temporal. Subset hari 0–10 dipakai hanya untuk menguji apakah jendela awal membatasi $K$; ia bukan pembagian alternatif yang dipilih setelah hasil terlihat.

RSS diminimalkan hanya pada data kalibrasi. Dalam AICc, jumlah parameter mencakup varians residu: $k=2$ untuk eksponensial dan $k=3$ untuk logistik. Konstanta Gaussian yang sama dihilangkan dari kedua nilai.""",
        ),
        code(
            "c4-run-analysis",
            """HASIL = jalankan_analisis(BATAS_K_ATAS)

require(HASIL["waktu"].size == HASIL["amatan"].size == 13, "Sensus data berubah")
require(len(HASIL["csv_text"].encode("utf-8")) == 228, "Ukuran CSV berubah")
require(HASIL["data_sha256"] == CANONICAL_DATA_SHA256, "Hash data sintetis berubah")
require(HASIL["indeks_kalibrasi"].size == 9, "Jumlah data kalibrasi berubah")
require(HASIL["indeks_uji"].size == 4, "Jumlah data uji berubah")
require(HASIL["indeks_awal"].size == 6, "Jumlah data subset awal berubah")
require(
    np.intersect1d(HASIL["indeks_kalibrasi"], HASIL["indeks_uji"]).size == 0,
    "Data kalibrasi dan data uji bertumpang tindih",
)
require(np.all(HASIL["waktu"][HASIL["indeks_kalibrasi"]] <= 16.0), "Batas kalibrasi berubah")
require(np.all(HASIL["waktu"][HASIL["indeks_uji"]] >= 18.0), "Batas data uji berubah")""",
        ),
        markdown(
            "c4-identifiability",
            r"""## Identifiabilitas struktural dan praktis

Dalam parameterisasi $dN/dt=\alpha\beta N(1-N/K)$, transformasi $(\alpha,\beta)\mapsto(c\alpha,\beta/c)$ tidak mengubah hasil kali $r=\alpha\beta$ atau lintasan. Karena itu, pengamatan $N(t)$ saja tidak dapat memisahkan $\alpha$ dan $\beta$, bahkan tanpa galat.

Setelah reparameterisasi, $r$ dan $K$ dapat dibedakan pada lintasan ideal yang cukup bervariasi. Namun, pada waktu awal $N/K$ kecil dan model hampir eksponensial. Notebook memeriksa masalah praktis ini melalui sensitivitas log-parameter dan eksperimen batas atas.""",
        ),
        code(
            "c4-identifiability-check",
            """alpha = 0.4
beta = 0.7
c = 2.0
alpha_baru = c * alpha
beta_baru = beta / c
require(np.isclose(alpha * beta, alpha_baru * beta_baru), "Invariansi hasil kali gagal")
require(
    np.array_equal(
        model_logistik(HASIL["waktu"], alpha * beta, TRUE_K_MILLION),
        model_logistik(HASIL["waktu"], alpha_baru * beta_baru, TRUE_K_MILLION),
    ),
    "Transformasi struktural mengubah lintasan",
)
require(HASIL["fit_logistik_awal"].active_mask[1] == 1, "Batas atas K subset awal tidak aktif")
require(
    np.isclose(HASIL["fit_logistik_awal"].x[1], BATAS_K_ATAS, rtol=0.0, atol=BATAS_K_ATAS * 1e-8),
    "Estimasi K subset awal tidak mengikuti batas atas",
)
require(HASIL["fit_logistik"].active_mask[1] == 0, "Estimasi K utama menyentuh batas")
require(HASIL["kondisi_awal"] > 4.0 * HASIL["kondisi_kalibrasi"], "Perbaikan kondisi jadwal menghilang")""",
        ),
        markdown(
            "c4-uncertainty",
            """## Diagnostik, ketidakpastian, dan batas validasi

Residu didefinisikan sebagai pengamatan dikurangi prediksi. MAE data uji mengukur besar galat, sedangkan bias mempertahankan tanda. Bootstrap parametrik menggunakan 400 replikasi dengan benih 20260824. Dalam setiap replikasi, notebook membuat data kalibrasi semu, mengestimasi ulang model, lalu membuat satu pengamatan baru pada setiap waktu data uji.

Interval yang dihasilkan bersifat titik-demi-titik dan kondisional pada model logistik, galat normal yang saling bebas dan bervarians konstan, serta jadwal pengamatan. Interval tersebut tidak mencakup ketaksesuaian bentuk model, perubahan proses, atau ketidakpastian eksternal.""",
        ),
        markdown(
            "c4-figure-description",
            """## Gambar diagnostik terpadu

**Deskripsi panjang gambar:** Panel A menampilkan sembilan lingkaran data kalibrasi hingga hari ke-16, empat persegi data uji pada hari ke-18 sampai ke-24, kurva logistik utuh yang mendatar mendekati 176 juta sel, dan kurva eksponensial putus-putus yang meningkat hingga sekitar 780 juta sel pada hari ke-24. Panel B menampilkan residu kalibrasi: residu logistik berupa lingkaran tersebar dekat garis nol, sedangkan residu eksponensial berupa tanda silang membentuk pola melengkung dan menjadi sangat negatif pada akhir jendela. Panel C menampilkan besar sensitivitas terskala terhadap $r$ dengan lingkaran dan terhadap $K$ dengan persegi; sensitivitas $K$ hampir nol pada waktu awal lalu meningkat ketika pertumbuhan melambat. Panel D menampilkan pita prediksi titik-demi-titik 95%, garis median, dan empat persegi pengamatan data uji; semua persegi berada di dalam pita.""",
        ),
        code(
            "c4-plot",
            """waktu = HASIL["waktu"]
amatan = HASIL["amatan"]
kal = HASIL["indeks_kalibrasi"]
uji = HASIL["indeks_uji"]
waktu_rapat = np.linspace(0.0, 24.0, 241)

fig, axes = plt.subplots(2, 2, figsize=(10.0, 7.5), constrained_layout=True)
ax_a, ax_b, ax_c, ax_d = axes.flat

ax_a.scatter(waktu[kal], amatan[kal], marker="o", label="data kalibrasi")
ax_a.scatter(waktu[uji], amatan[uji], marker="s", label="data uji")
ax_a.plot(
    waktu_rapat,
    model_logistik(waktu_rapat, *HASIL["fit_logistik"].x),
    linestyle="-",
    color="black",
    label="logistik",
)
ax_a.plot(
    waktu_rapat,
    model_eksponensial(waktu_rapat, *HASIL["fit_eksponensial"].x),
    linestyle="--",
    color="tab:red",
    label="eksponensial",
)
ax_a.axvline(17.0, linestyle=":", color="0.4", label="batas pembagian")
ax_a.set(title="A. Data dan prediksi", xlabel="waktu (hari)", ylabel="populasi (juta sel)")
ax_a.legend(fontsize="small")

ax_b.axhline(0.0, color="black", linewidth=1)
ax_b.scatter(
    waktu[kal], HASIL["metrik_logistik"]["residu_kalibrasi"], marker="o", label="logistik"
)
ax_b.scatter(
    waktu[kal], HASIL["metrik_eksponensial"]["residu_kalibrasi"], marker="x", label="eksponensial"
)
ax_b.set(title="B. Residu kalibrasi", xlabel="waktu (hari)", ylabel="residu (juta sel)")
ax_b.legend(fontsize="small")

sensitivitas_semua = sensitivitas_log_parameter(waktu, *HASIL["fit_logistik"].x)
ax_c.plot(waktu, np.abs(sensitivitas_semua[:, 0]), marker="o", linestyle="-", label="terhadap r")
ax_c.plot(waktu, np.abs(sensitivitas_semua[:, 1]), marker="s", linestyle="--", label="terhadap K")
ax_c.axvline(17.0, linestyle=":", color="0.4")
ax_c.set(title="C. Sensitivitas terskala", xlabel="waktu (hari)", ylabel="besar sensitivitas")
ax_c.legend(fontsize="small")

q_pred = HASIL["kuantil_prediksi"]
ax_d.fill_between(waktu[uji], q_pred[0], q_pred[2], color="0.8", label="interval prediksi 95%")
ax_d.plot(waktu[uji], q_pred[0], linestyle="--", color="black", label="batas bawah 95%")
ax_d.plot(waktu[uji], q_pred[2], linestyle="-.", color="black", label="batas atas 95%")
ax_d.plot(waktu[uji], q_pred[1], marker="o", linestyle="-", color="black", label="median prediksi")
ax_d.scatter(waktu[uji], amatan[uji], marker="s", color="tab:blue", label="data uji")
ax_d.set(title="D. Prediksi data uji", xlabel="waktu (hari)", ylabel="populasi (juta sel)")
ax_d.legend(fontsize="small")

fig.canvas.draw()
if matplotlib.get_backend().lower() != "agg":
    plt.show()
plt.close(fig)""",
        ),
        markdown(
            "c4-failure-analysis",
            """## Analisis kegagalan

Pesan “optimasi berhasil” hanya menyatakan bahwa algoritma memenuhi kriteria berhenti. Estimasi yang mengikuti batas, bilangan kondisi yang besar, residu berpola, atau galat data uji yang melonjak tetap merupakan kegagalan evidensial. Model eksponensial memperlihatkan kegagalan bentuk: ia tidak memiliki mekanisme perlambatan dan mengekstrapolasi hingga sekitar 780 juta sel pada hari ke-24.

Jika data uji digunakan untuk merevisi model, data tersebut tidak lagi menjadi evaluasi akhir yang independen. Kumpulkan data baru untuk pengujian berikutnya. Jika semua kandidat gagal, memperkecil toleransi optimasi bukan solusi; perbaiki himpunan model, pengukuran, atau pertanyaan.""",
        ),
        code(
            "c4-same-kernel-replay",
            """HASIL_ULANG = jalankan_analisis(BATAS_K_ATAS)

require(HASIL_ULANG["csv_text"].encode("utf-8") == HASIL["csv_text"].encode("utf-8"), "Byte data berubah")
require(np.array_equal(HASIL_ULANG["amatan"], HASIL["amatan"]), "Data berubah dalam kernel yang sama")
require(
    np.allclose(HASIL_ULANG["fit_logistik"].x, HASIL["fit_logistik"].x, rtol=0.0, atol=1e-12),
    "Estimasi logistik berubah dalam kernel yang sama",
)
require(
    np.array_equal(HASIL_ULANG["bootstrap"]["parameter"], HASIL["bootstrap"]["parameter"]),
    "Bootstrap parameter berubah dalam kernel yang sama",
)
require(
    np.array_equal(
        HASIL_ULANG["bootstrap"]["pengamatan_mendatang"],
        HASIL["bootstrap"]["pengamatan_mendatang"],
    ),
    "Bootstrap prediksi berubah dalam kernel yang sama",
)
print("Verifikasi ulang deterministik dalam kernel yang sama lulus.")""",
        ),
        markdown(
            "c4-summary",
            """## Ringkasan yang dapat diperiksa

Pemeriksaan berikut mempertahankan invarian struktur, keterhinggaan, pembagian data, dan keberhasilan bootstrap untuk eksekusi kanonik maupun eksperimen batas 2000. Sidik numerik kanonik hanya diwajibkan ketika batas atas $K$ bernilai 1000. Toleransi numerik menangkap perubahan substantif tanpa menuntut kesamaan bit pecahan mengambang.""",
        ),
        code(
            "c4-canonical-checks",
            """m_exp = HASIL["metrik_eksponensial"]
m_log = HASIL["metrik_logistik"]
fit_exp = HASIL["fit_eksponensial"].x
fit_log = HASIL["fit_logistik"].x
fit_awal = HASIL["fit_logistik_awal"].x
q_par = HASIL["kuantil_parameter"]
q_lat = HASIL["kuantil_laten"]
q_pred = HASIL["kuantil_prediksi"]

require(np.isfinite(fit_exp).all() and np.isfinite(fit_log).all() and np.isfinite(fit_awal).all(), "Parameter tidak hingga")
require(np.isfinite(q_par).all() and np.isfinite(q_lat).all() and np.isfinite(q_pred).all(), "Kuantil tidak hingga")
require(HASIL["bootstrap"]["keberhasilan"] == BOOTSTRAP_REPLICATES, "Ada pencocokan bootstrap yang gagal")
require(np.all(np.diff(q_par, axis=0) >= 0.0), "Urutan kuantil parameter rusak")
require(np.all(np.diff(q_lat, axis=0) >= 0.0), "Urutan kuantil respons laten rusak")
require(np.all(np.diff(q_pred, axis=0) >= 0.0), "Urutan kuantil prediksi rusak")
require(int(np.sum(HASIL["tercakup"])) == 4, "Cakupan data uji kanonik berubah")
require(m_exp["aicc"] - m_log["aicc"] > 20.0, "Pemisahan AICc kandidat menyusut")
require(m_log["mae_uji"] < 3.0, "MAE data uji logistik terlalu besar")
require(m_exp["mae_uji"] > 100.0, "Kegagalan eksponensial tidak terdeteksi")
require(abs(HASIL["korelasi_parameter"]) < 1.0, "Korelasi parameter tidak sah")
require(HASIL["sigma_hat"] > 0.0, "Estimasi simpangan baku tidak positif")

is_canonical = np.isclose(BATAS_K_ATAS, CANONICAL_K_UPPER_BOUND, rtol=0.0, atol=0.0)
is_bound_2000 = np.isclose(BATAS_K_ATAS, 2000.0, rtol=0.0, atol=0.0)
if is_canonical:
    require(np.isclose(fit_exp[0], 0.210405202646, rtol=0.0, atol=1e-6), "Estimasi r eksponensial berubah")
    require(np.isclose(fit_log[0], 0.282631488027, rtol=0.0, atol=1e-6), "Estimasi r logistik berubah")
    require(np.isclose(fit_log[1], 175.706062263, rtol=0.0, atol=1e-3), "Estimasi K logistik berubah")
    require(np.isclose(fit_awal[0], 0.251100074027, rtol=0.0, atol=1e-6), "Estimasi r subset awal berubah")
    require(np.isclose(fit_awal[1], 1000.0, rtol=0.0, atol=1e-5), "Estimasi K subset awal berubah")
    require(np.isclose(m_log["rmse_kalibrasi"], 2.256897277059, rtol=0.0, atol=1e-5), "RMSE logistik berubah")
    require(np.isclose(m_log["mae_uji"], 1.506641970024, rtol=0.0, atol=1e-5), "MAE logistik berubah")
    require(np.isclose(m_log["aicc"], 25.451837707595, rtol=0.0, atol=1e-5), "AICc logistik berubah")
    require(np.isclose(m_exp["aicc"] - m_log["aicc"], 25.729279853259, rtol=0.0, atol=1e-5), "Selisih AICc berubah")
    require(np.isclose(HASIL["kondisi_awal"], 32.66379816, rtol=0.0, atol=1e-4), "Kondisi jadwal awal berubah")
    require(np.isclose(HASIL["kondisi_kalibrasi"], 6.93948506, rtol=0.0, atol=1e-4), "Kondisi jadwal kalibrasi berubah")
    require(np.allclose(q_par[:, 0], [0.27231855, 0.28260638, 0.29399270], rtol=0.0, atol=5e-4), "Kuantil r berubah")
    require(np.allclose(q_par[:, 1], [160.82788727, 175.22741952, 195.85394556], rtol=0.0, atol=0.25), "Kuantil K berubah")
    require(np.allclose(q_lat[:, -1], [156.44924030, 168.76012565, 185.63476304], rtol=0.0, atol=0.25), "Interval respons laten hari 24 berubah")
    require(np.allclose(q_pred[:, -1], [154.39781350, 169.60209338, 185.61306021], rtol=0.0, atol=0.25), "Interval prediksi hari 24 berubah")
elif is_bound_2000:
    require(np.isclose(fit_awal[0], 0.24853917, rtol=0.0, atol=1e-6), "Estimasi r subset awal batas 2000 berubah")
    require(np.isclose(fit_awal[1], 2000.0, rtol=0.0, atol=1e-3), "Estimasi K subset awal batas 2000 berubah")
    require(np.isclose(fit_log[0], 0.282631488027, rtol=0.0, atol=1e-6), "Estimasi r utama batas 2000 berubah")
    require(np.isclose(fit_log[1], 175.706062263, rtol=0.0, atol=1e-3), "Estimasi K utama batas 2000 berubah")
    require(np.allclose(q_par[:, 1], [160.82788727, 175.22741952, 195.85394556], rtol=0.0, atol=0.25), "Kuantil K batas 2000 berubah")
    print("Eksekusi nonkanonik tervalidasi: BATAS_K_ATAS=2000.0.")
else:
    raise ValueError("BATAS_K_ATAS yang didukung hanya 1000.0 (kanonik) atau 2000.0 (uji kepekaan)")

RINGKASAN = {
    "unit_id": UNIT_ID,
    "canonical": bool(is_canonical),
    "batas_k_atas": float(BATAS_K_ATAS),
    "data_sha256": HASIL["data_sha256"],
    "n_kalibrasi": int(HASIL["indeks_kalibrasi"].size),
    "n_uji": int(HASIL["indeks_uji"].size),
    "r_eksponensial": round(float(fit_exp[0]), 8),
    "r_logistik": round(float(fit_log[0]), 8),
    "k_logistik": round(float(fit_log[1]), 8),
    "r_logistik_awal": round(float(fit_awal[0]), 8),
    "k_logistik_awal": round(float(fit_awal[1]), 8),
    "rmse_logistik": round(float(m_log["rmse_kalibrasi"]), 8),
    "aicc_logistik": round(float(m_log["aicc"]), 8),
    "delta_aicc": round(float(m_exp["aicc"] - m_log["aicc"]), 8),
    "mae_uji_logistik": round(float(m_log["mae_uji"]), 8),
    "bias_uji_logistik": round(float(m_log["bias_uji"]), 8),
    "kondisi_awal": round(float(HASIL["kondisi_awal"]), 8),
    "kondisi_kalibrasi": round(float(HASIL["kondisi_kalibrasi"]), 8),
    "sigma_hat": round(float(HASIL["sigma_hat"]), 8),
    "bootstrap_sukses": int(HASIL["bootstrap"]["keberhasilan"]),
    "cakupan_uji": int(np.sum(HASIL["tercakup"])),
    "interval_respons_laten_hari24": [round(float(x), 8) for x in q_lat[:, -1]],
    "interval_prediksi_hari24": [round(float(x), 8) for x in q_pred[:, -1]],
    "versions": VERSIONS,
    "model_identification": "OpenAI Codex gpt-5.6-sol, Ultra.",
}
print(json.dumps(RINGKASAN, ensure_ascii=False, sort_keys=True, indent=2))""",
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
                "notebook_id": "O005-BRIDGE-C4-NB01",
                "language": "id-ID",
                "locale": "id-ID",
                "provenance": "new_original_addition",
                "component_origin": "original",
                "offline_capable": True,
                "offline_scope": "network_free_after_environment_install",
                "environment_lock": "requirements.lock",
                "wheelhouse_included": False,
                "model_identification": "OpenAI Codex gpt-5.6-sol, Ultra.",
                "license": "CC BY-NC-SA 4.0",
                "relationship": "independent_supplement",
                "non_endorsement": True,
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
            "problem_summary": "Buktikan ketakidentifikasian struktural dua parameter yang hanya muncul sebagai hasil kali.",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": r"Pilih \(c=2\) dan pertahankan hasil kali \(\alpha\beta\)."},
            "check": {
                "type": "structured",
                "final_answer": r"Pasangan \((0.8,0.35)\) memberi hasil kali \(0.28\) yang sama dengan \((0.4,0.7)\), sehingga lintasan identik.",
                "required_evidence": [
                    r"\(0.4(0.7)=0.8(0.35)=0.28\ \text{hari}^{-1}\).",
                    "Persamaan hanya bergantung pada hasil kali, bukan kedua faktor secara terpisah.",
                    "Pemisahan memerlukan pengukuran salah satu faktor atau keluaran tambahan yang bergantung berbeda pada keduanya.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    r"Ambil \(c=2\), sehingga \(\alpha^{\prime}=2(0.4)=0.8\) dan \(\beta^{\prime}=0.7/2=0.35\).",
                    "Hitung kedua hasil kali dan peroleh 0.28.",
                    r"Karena ruas kanan persamaan identik untuk setiap \(N\), kondisi awal yang sama menghasilkan lintasan yang sama.",
                    r"Ukur \(\alpha\) atau \(\beta\) secara independen, atau tambahkan keluaran yang merespons kedua parameter secara berbeda.",
                ],
                "conclusion": r"Lebih banyak pengamatan \(N(t)\) dengan jenis yang sama tidak memecahkan ketakidentifikasian struktural.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P02",
            "ordinal": 2,
            "problem_summary": "Hitung faktor pembatas logistik dan hubungkan dengan lemahnya informasi awal tentang daya dukung.",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": r"Substitusikan \(N/K\) ke faktor \(1-N/K\) dan bandingkan jaraknya dari satu."},
            "check": {
                "type": "quantitative",
                "final_answer": r"Pada \(N=20\) faktornya \(0.8889\); pada \(N=100\) faktornya \(0.4444\).",
                "formula": r"1-\frac{20}{180}=\frac{8}{9}\quad\text{dan}\quad 1-\frac{100}{180}=\frac{4}{9}",
                "tolerances": {"absolute": 0.0001},
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    r"Hitung \(1-\frac{20}{180}=\frac{160}{180}=\frac{8}{9}\approx0.8889\).",
                    r"Hitung \(1-\frac{100}{180}=\frac{80}{180}=\frac{4}{9}\approx0.4444\).",
                    r"Pada populasi kecil faktor mendekati satu, sehingga perubahan \(K\) hanya sedikit mengubah laju.",
                    r"Pengamatan mendekati perlambatan pertumbuhan memberi pengaruh \(K\) yang lebih besar.",
                ],
                "conclusion": r"Memperpanjang jendela menuju daerah saturasi dapat memperbaiki identifiabilitas praktis \(K\).",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P03",
            "ordinal": 3,
            "problem_summary": "Tafsirkan perubahan bilangan kondisi sensitivitas akibat jendela pengamatan yang lebih panjang.",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": "Bilangan kondisi membandingkan pemisahan arah sensitivitas, bukan mutu model secara keseluruhan."},
            "check": {
                "type": "qualitative",
                "final_answer": r"Penurunan dari 32.6638 menjadi 6.93949 menunjukkan jadwal 0–16 memisahkan efek \(r\) dan \(K\) dengan lebih baik.",
                "required_evidence": [
                    "Nilai lebih kecil berarti dua arah sensitivitas kurang segaris.",
                    r"Waktu mendekati perlambatan pertumbuhan terutama menambah informasi tentang \(K\).",
                    "Tidak ada ambang universal; batas parameter, residu, dan ketidakpastian tetap perlu diperiksa.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Bandingkan rasio nilai singular untuk kedua jadwal.",
                    "Kenali bahwa jadwal awal terutama melihat pertumbuhan yang hampir eksponensial.",
                    "Tambahkan pengamatan sekitar pembelokan dan pendekatan ke daya dukung.",
                    "Periksa kembali hasil dengan profil, batas, atau bootstrap sebelum menyatakan parameter tajam.",
                ],
                "conclusion": "Jadwal 0–16 lebih informatif, bukan otomatis sempurna.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P04",
            "ordinal": 4,
            "problem_summary": r"Hitung \(\mathrm{AICc}\) dua kandidat dengan konvensi parameter yang dinyatakan.",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": r"Gunakan \(\mathrm{AICc}=n\log(\mathrm{RSS}/n)+2k+\frac{2k(k+1)}{n-k-1}\) untuk setiap model."},
            "check": {
                "type": "quantitative",
                "final_answer": r"\(\mathrm{AICc}\) eksponensial 51.18111756, \(\mathrm{AICc}\) logistik 25.45183771, dan selisih 25.72927985 mendukung logistik di antara dua kandidat.",
                "formula": r"\mathrm{AICc}=n\log(\mathrm{RSS}/n)+2k+\frac{2k(k+1)}{n-k-1}",
                "tolerances": {"aicc_absolute": 0.000001},
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    r"Substitusikan \(n=9\), \(\mathrm{RSS}=1362.87095600\), dan \(k=2\) untuk eksponensial.",
                    r"Substitusikan \(n=9\), \(\mathrm{RSS}=45.84226787\), dan \(k=3\) untuk logistik.",
                    "Kurangkan nilai logistik dari nilai eksponensial.",
                    "Tafsirkan hasil sebagai perbandingan relatif, bukan bukti bahwa model logistik benar.",
                ],
                "conclusion": r"\(\mathrm{AICc}\) hanya memilih di antara kandidat yang diberikan dengan data dan konvensi yang sama.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P05",
            "ordinal": 5,
            "problem_summary": "Hitung dan tafsirkan tiga diagnostik dari residu data uji.",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": r"\(\mathrm{MAE}\) memakai nilai absolut, bias mempertahankan tanda, dan maksimum memilih besar residu terbesar."},
            "check": {
                "type": "quantitative",
                "final_answer": r"\(\mathrm{MAE}=1.50664197\), \(\mathrm{bias}=1.17225281\), dan galat absolut maksimum \(=2.84222916\) juta sel.",
                "formula": r"\mathrm{MAE}=\frac{1}{4}\sum_{i=1}^{4}|e_i|,\qquad \mathrm{bias}=\frac{1}{4}\sum_{i=1}^{4}e_i",
                "tolerances": {"metric_absolute": 0.00000001},
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Jumlahkan nilai absolut empat residu lalu bagi empat.",
                    "Jumlahkan residu bertanda lalu bagi empat.",
                    "Pilih nilai absolut terbesar.",
                    r"Karena residu didefinisikan \(y-\widehat{y}\), bias positif berarti pengamatan rata-rata berada di atas prediksi.",
                ],
                "conclusion": "Metrik besar dan arah harus dilaporkan bersama, bukan dipertukarkan.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P06",
            "ordinal": 6,
            "problem_summary": "Bedakan interval parameter, respons laten, dan pengamatan mendatang serta batas interpretasinya.",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": "Tanyakan apakah galat pengamatan baru ditambahkan dan apakah ketaksesuaian bentuk model diwakili."},
            "check": {
                "type": "structured",
                "final_answer": r"Interval \(K\) mengukur variasi estimasi parameter; interval laten mempropagasi parameter; interval pengamatan juga menambahkan galat ukur baru.",
                "required_evidence": [
                    r"Interval \(K\) adalah \([160.82788727,175.22741952,195.85394556]\) juta sel pada kuantil 2.5%, 50%, dan 97.5%.",
                    r"Interval respons laten hari 24 adalah \([156.44924030,168.76012565,185.63476304]\) juta sel pada kuantil yang sama.",
                    r"Interval pengamatan hari 24 adalah \([154.39781350,169.60209338,185.61306021]\) juta sel pada kuantil yang sama.",
                    "Cakupan satu pengamatan tidak membuktikan bentuk model benar.",
                    "Asumsi bersyarat mencakup model logistik, galat normal independen bervarians konstan, dan proses yang tidak berubah.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    r"Kenali bahwa interval \(K\), yaitu \([160.82788727,195.85394556]\), hidup pada ruang parameter.",
                    r"Hitung respons laten dari setiap parameter bootstrap tanpa menambahkan galat baru; pada hari 24 intervalnya \([156.44924030,185.63476304]\) juta sel.",
                    r"Tambahkan satu galat pengamatan baru untuk interval prediksi pengamatan; pada hari 24 intervalnya \([154.39781350,185.61306021]\) juta sel.",
                    "Nyatakan bahwa semuanya kondisional dan titik-demi-titik, bukan interval simultan atau validasi eksternal.",
                ],
                "conclusion": "Interval yang lebih lebar dapat mewakili lebih banyak sumber variasi, tetapi masih dapat mengabaikan ketaksesuaian model.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P07",
            "ordinal": 7,
            "problem_summary": r"Jalankan notebook bersih dan uji kepekaan estimasi subset awal terhadap batas atas \(K\).",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": "Bandingkan estimasi subset awal dengan estimasi jendela 0–16 sebelum dan sesudah hanya batas atas diubah."},
            "check": {
                "type": "executable",
                "final_answer": r"Batas 1000 memberi \(K_{\mathrm{awal}}=1000\) dan \(r_{\mathrm{awal}}=0.25110007\); batas 2000 memberi \(K_{\mathrm{awal}}=2000\) dan \(r_{\mathrm{awal}}=0.24853917\), sedangkan estimasi utama tetap sekitar \(r=0.28263149\) dan \(K=175.70606\).",
                "notebook_check": "Semua sel berjalan dari kernel bersih, menghasilkan tepat satu PNG, 400/400 pencocokan bootstrap berhasil, dan pemeriksaan require lulus pada kedua batas.",
                "required_evidence": [
                    "Hash data tetap 932d0d27c2917936b0aa51d283d7b2fe2a5eba95989a6c785fa32d3d18dd2811.",
                    r"Eksekusi batas 2000 ditandai nonkanonik dan mempunyai sidik numerik khusus untuk estimasi subset awal, estimasi utama, serta kuantil \(K\).",
                    "Struktur, keterhinggaan, pembagian data, batas aktif, bootstrap, dan cakupan tetap diperiksa; batas selain 1000 atau 2000 ditolak.",
                    "Perpindahan estimasi mengikuti batas merupakan bukti identifiabilitas praktis yang lemah pada subset awal.",
                ],
                "tolerances": {
                    "r_absolute": 0.000001,
                    "k_main_absolute": 0.001,
                    "bootstrap_quantile_k_absolute": 0.25,
                },
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Mulai kernel baru dan jalankan seluruh notebook dengan batas kanonik 1000.",
                    "Cocokkan hash, parameter utama, metrik, bilangan kondisi, 400 keberhasilan bootstrap, dan interval hari 24.",
                    "Ubah hanya BATAS_K_ATAS menjadi 2000 lalu mulai kernel baru dan jalankan semua sel.",
                    r"Amati bahwa \(K\) subset awal kembali berada di batas, sedangkan parameter jendela penuh berubah kurang dari toleransi.",
                    "Simpan hasil kedua sebagai eksperimen nonkanonik, bukan pengganti identitas rilis.",
                ],
                "conclusion": "Keberhasilan algoritma tidak mengubah batas arbitrer menjadi informasi dari data.",
            },
            "notebook": {
                "path": "source/id-ID/O005-BRIDGE-C4/notebooks/bridge-c4-calibration-validation-uncertainty.ipynb",
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
    print(
        json.dumps(
            {
                "unit_id": UNIT_ID,
                "mode": "check" if args.check else "write",
                "files": [path.relative_to(ROOT).as_posix() for path in expected_files()],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
