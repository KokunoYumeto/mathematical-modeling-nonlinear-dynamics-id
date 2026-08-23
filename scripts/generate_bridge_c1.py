#!/usr/bin/env python3
"""Generate the deterministic C1 notebook, mastery layer, and lock file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIT_ID = "O005-BRIDGE-C1"
NOTEBOOK = (
    ROOT
    / "source"
    / "id-ID"
    / UNIT_ID
    / "notebooks"
    / "bridge-c1-reproducible-workflow.ipynb"
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
            "c1-title",
            """# O005-BRIDGE-C1 — Alur Kerja Python/Jupyter yang Reprodusibel

Notebook ini adalah tambahan independen untuk edisi Bahasa Indonesia *Introduction to Mathematical Modeling*. Ia memperagakan rantai bukti komputasional dengan model pendinginan sederhana. Data dibuat secara sintetis dan tidak merupakan bukti eksperimen.

Produksi dan QA: OpenAI Codex gpt-5.6-sol, Ultra. Kredit Joceline Lega dan University of Arizona untuk buku sumber tetap terpisah dan tidak tersirat sebagai dukungan terhadap tambahan ini. Distribusi mengikuti CC BY-NC-SA 4.0.""",
        ),
        code(
            "c1-environment",
            """import hashlib
import json
import platform

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.optimize import curve_fit

CANONICAL_SEED = 20260822
SEED = CANONICAL_SEED
CANONICAL_DATA_SHA256 = "1000bc1092f173258d2be37e4f8906ea0933708582d09768ce96eed739be337e"
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
            "c1-model-contract",
            """## Kontrak model

Dengan waktu $t$ dalam menit dan suhu dalam derajat Celsius,

$$T(t)=T_{\\infty}+(T_0-T_{\\infty})e^{-kt}.$$

Notebook menetapkan $T_0=92$, mensyaratkan $k>0$, dan mengestimasi $k$ serta $T_{\\infty}$. Fungsi model tidak membaca keadaan global yang tersembunyi: setiap masukan yang berubah dicantumkan sebagai argumen atau konstanta bernama.""",
        ),
        code(
            "c1-model-functions",
            """T0_C = 92.0
TRUE_K_PER_MIN = 0.073
TRUE_T_INF_C = 22.4
NOISE_SD_C = 0.35

def suhu_pendinginan(waktu_menit, laju_per_menit, suhu_lingkungan_c, suhu_awal_c=T0_C):
    waktu = np.asarray(waktu_menit, dtype=float)
    return suhu_lingkungan_c + (suhu_awal_c - suhu_lingkungan_c) * np.exp(-laju_per_menit * waktu)

def serialisasi_csv(waktu_menit, suhu_c):
    baris = ["time_min,temperature_c"]
    baris.extend(f"{t:.1f},{y:.6f}" for t, y in zip(waktu_menit, suhu_c))
    return "\\n".join(baris) + "\\n"

require(np.isclose(suhu_pendinginan(0.0, TRUE_K_PER_MIN, TRUE_T_INF_C), T0_C), "Kondisi awal model gagal")
require(suhu_pendinginan(50.0, TRUE_K_PER_MIN, TRUE_T_INF_C) > TRUE_T_INF_C, "Solusi pendinginan melewati suhu lingkungan")""",
        ),
        markdown(
            "c1-data-provenance",
            """## Data sintetis dan asal-usulnya

Sebelas waktu pengamatan ditentukan terlebih dahulu. Pembangkit acak lokal memakai benih eksplisit. Aturan serialisasi—nama kolom, satu angka desimal untuk waktu, enam angka desimal untuk suhu, UTF-8, dan satu baris akhir—merupakan bagian dari identitas data.""",
        ),
        code(
            "c1-generate-data",
            """def buat_data(seed=SEED):
    rng = np.random.default_rng(seed)
    waktu = np.arange(0.0, 55.0, 5.0)
    suhu_bersih = suhu_pendinginan(waktu, TRUE_K_PER_MIN, TRUE_T_INF_C)
    # The serialized values are also the values used for estimation, so the
    # published SHA-256 binds the exact analyzed data rather than a hidden
    # higher-precision array.
    suhu_amatan = np.round(suhu_bersih + rng.normal(0.0, NOISE_SD_C, waktu.size), 6)
    csv_text = serialisasi_csv(waktu, suhu_amatan)
    data_sha256 = hashlib.sha256(csv_text.encode("utf-8")).hexdigest()
    return waktu, suhu_amatan, csv_text, data_sha256

waktu_menit, suhu_amatan_c, csv_text, DATA_SHA256 = buat_data()
require(waktu_menit.size == suhu_amatan_c.size == 11, "Sensus data sintetis berbeda")
require(len(csv_text.encode("utf-8")) == 186, "Ukuran CSV sintetis berbeda")
if SEED == CANONICAL_SEED:
    require(DATA_SHA256 == CANONICAL_DATA_SHA256, "Hash data kanonik berbeda")
else:
    require(DATA_SHA256 != CANONICAL_DATA_SHA256, "Benih nonkanonik tidak mengubah identitas data")
    print(f"Benih nonkanonik {SEED}; identitas data berubah menjadi {DATA_SHA256}.")""",
        ),
        markdown(
            "c1-split-estimate",
            """## Pisahkan dahulu, lalu estimasi

Indeks 0–7 menjadi data latih. Tiga pengamatan terakhir disisihkan sebagai data uji dan tidak ikut menentukan parameter. Pemisahan berurutan ini menguji prediksi ke waktu yang lebih lanjut; ia bukan satu-satunya desain validasi yang mungkin.""",
        ),
        code(
            "c1-fit-model",
            """INDEKS_LATIH = np.arange(0, 8)
INDEKS_UJI = np.arange(8, 11)

def estimasi_parameter(waktu, suhu):
    parameter, kovariansi = curve_fit(
        lambda t, k, t_inf: suhu_pendinginan(t, k, t_inf),
        waktu[INDEKS_LATIH],
        suhu[INDEKS_LATIH],
        p0=(0.05, 20.0),
        bounds=([0.001, 0.0], [0.5, 50.0]),
        maxfev=10000,
    )
    return parameter, kovariansi

parameter_hat, kovariansi_hat = estimasi_parameter(waktu_menit, suhu_amatan_c)
k_hat, t_inf_hat = parameter_hat
prediksi_c = suhu_pendinginan(waktu_menit, k_hat, t_inf_hat)
residu_latih_c = suhu_amatan_c[INDEKS_LATIH] - prediksi_c[INDEKS_LATIH]""",
        ),
        markdown(
            "c1-diagnostics",
            """## Pemeriksaan numerik dan visual

RMSE data latih memadatkan besar residu, korelasi residu–waktu memeriksa satu pola sederhana, dan MAE data uji yang disisihkan (*holdout*) mengukur kesalahan pada titik yang tidak dipakai dalam estimasi. Ketiganya harus dibaca bersama grafik dan kontrak model; tidak satu pun merupakan uji kecukupan universal.

**Deskripsi panjang gambar:** panel kiri memperlihatkan delapan titik data latih, tiga titik data uji pada waktu paling akhir, dan kurva pendinginan terestimasi yang menurun menuju suhu lingkungan. Panel kanan memperlihatkan residu data latih terhadap waktu di sekitar garis nol; tidak tampak tren satu arah yang kuat pada realisasi sintetis ini.""",
        ),
        code(
            "c1-diagnostics-code",
            """RMSE_LATIH_C = float(np.sqrt(np.mean(residu_latih_c**2)))
MEAN_RESIDU_C = float(np.mean(residu_latih_c))
KORELASI_RESIDU_WAKTU = float(np.corrcoef(waktu_menit[INDEKS_LATIH], residu_latih_c)[0, 1])
MAE_UJI_C = float(np.mean(np.abs(suhu_amatan_c[INDEKS_UJI] - prediksi_c[INDEKS_UJI])))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.5), constrained_layout=True)
ax1.scatter(waktu_menit[INDEKS_LATIH], suhu_amatan_c[INDEKS_LATIH], marker="o", label="data latih")
ax1.scatter(waktu_menit[INDEKS_UJI], suhu_amatan_c[INDEKS_UJI], marker="s", label="data uji")
ax1.plot(waktu_menit, prediksi_c, color="black", label="model terestimasi")
ax1.set(xlabel="waktu (menit)", ylabel="suhu (°C)")
ax1.legend()
ax2.axhline(0.0, color="black", linewidth=1)
ax2.scatter(waktu_menit[INDEKS_LATIH], residu_latih_c)
ax2.set(xlabel="waktu (menit)", ylabel="residu data latih (°C)")
fig.canvas.draw()
if matplotlib.get_backend().lower() != "agg":
    plt.show()
plt.close(fig)

require(np.isfinite([RMSE_LATIH_C, MEAN_RESIDU_C, KORELASI_RESIDU_WAKTU, MAE_UJI_C]).all(), "Diagnostik mengandung nilai tak hingga atau NaN")""",
        ),
        markdown(
            "c1-manifest",
            """## Ringkasan yang dapat diperiksa

Ringkasan berikut menggunakan nama dan pembulatan tetap. Pemeriksaan numerik memakai nilai tak dibulatkan. Toleransi sengaja lebih longgar daripada digit terakhir pecahan mengambang, tetapi cukup ketat untuk menangkap perubahan data, model, pembagian, atau algoritma.""",
        ),
        code(
            "c1-assertions",
            """RINGKASAN = {
    "unit_id": "O005-BRIDGE-C1",
    "seed": SEED,
    "data_sha256": DATA_SHA256,
    "k_hat_per_min": round(float(k_hat), 8),
    "t_inf_hat_c": round(float(t_inf_hat), 8),
    "rmse_latih_c": round(RMSE_LATIH_C, 8),
    "mean_residu_c": round(MEAN_RESIDU_C, 8),
    "korelasi_residu_waktu": round(KORELASI_RESIDU_WAKTU, 8),
    "mae_uji_c": round(MAE_UJI_C, 8),
    "versions": VERSIONS,
}

if SEED == CANONICAL_SEED:
    require(abs(k_hat - TRUE_K_PER_MIN) < 0.003, "Estimasi k keluar dari batas")
    require(abs(t_inf_hat - TRUE_T_INF_C) < 0.8, "Estimasi T_inf keluar dari batas")
    require(RMSE_LATIH_C < 0.5, "RMSE data latih keluar dari batas")
    require(abs(MEAN_RESIDU_C) < 0.1, "Rerata residu keluar dari batas")
    require(abs(KORELASI_RESIDU_WAKTU) < 0.3, "Korelasi residu-waktu keluar dari batas")
    require(MAE_UJI_C < 0.4, "MAE data uji keluar dari batas")
    require(RINGKASAN["k_hat_per_min"] == 0.07287235, "Nilai kanonik k berubah")
    require(RINGKASAN["t_inf_hat_c"] == 22.63964536, "Nilai kanonik T_inf berubah")
    require(RINGKASAN["rmse_latih_c"] == 0.31976406, "Nilai kanonik RMSE berubah")
    require(RINGKASAN["mae_uji_c"] == 0.17952331, "Nilai kanonik MAE berubah")
print(json.dumps(RINGKASAN, ensure_ascii=False, sort_keys=True, indent=2))""",
        ),
        markdown(
            "c1-same-kernel-rerun",
            """## Verifikasi ulang deterministik dalam kernel yang sama

Sel terakhir mengulang pembuatan data dan estimasi melalui fungsi yang sama, lalu membandingkan byte data dan parameter dengan hasil pertama. Pemeriksaan ini mendeteksi ketidakdeterministikan dalam satu kernel, tetapi bukan pengganti gerbang QA eksternal yang memulai kernel Jupyter baru dan menjalankan semua sel secara berurutan.""",
        ),
        code(
            "c1-same-kernel-rerun-check",
            """waktu_ulang, suhu_ulang, csv_ulang, hash_ulang = buat_data(SEED)
parameter_ulang, _ = estimasi_parameter(waktu_ulang, suhu_ulang)

require(csv_ulang.encode("utf-8") == csv_text.encode("utf-8"), "Byte CSV berubah dalam kernel yang sama")
require(hash_ulang == DATA_SHA256, "Hash data berubah dalam kernel yang sama")
require(np.array_equal(waktu_ulang, waktu_menit), "Grid waktu berubah dalam kernel yang sama")
require(np.array_equal(suhu_ulang, suhu_amatan_c), "Data sintetis berubah dalam kernel yang sama")
require(np.allclose(parameter_ulang, parameter_hat, rtol=0.0, atol=1e-12), "Estimasi berubah dalam kernel yang sama")
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
                "notebook_id": "O005-BRIDGE-C1-NB01",
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
            "problem_summary": "Identifikasi informasi yang hilang dari laporan yang hanya menyertakan gambar simulasi dan keterangan bahwa Python digunakan.",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": "Telusuri rantai dari pertanyaan dan data hingga kode, lingkungan, parameter, serta keluaran."},
            "check": {
                "type": "qualitative",
                "final_answer": "Jawaban lengkap menyebut sedikitnya lima unsur yang membuat klaim dapat ditelusuri dan dijalankan ulang.",
                "required_evidence": [
                    "Identitas dan asal-usul data.",
                    "Persamaan, asumsi, parameter, serta satuan model.",
                    "Kode dan urutan eksekusi.",
                    "Versi Python/pustaka dan benih acak bila ada.",
                    "Nilai numerik atau manifest yang mengikat gambar pada keluaran tepat.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Nyatakan pertanyaan dan tujuan penggunaan simulasi.",
                    "Berikan data atau cara deterministik untuk memperolehnya beserta hash dan lisensi.",
                    "Tuliskan model, asumsi, satuan, parameter, kondisi awal, dan domain.",
                    "Sertakan kode lengkap serta urutan menjalankan dari keadaan bersih.",
                    "Patok lingkungan dan sumber keacakan, lalu catat keluaran numerik yang mendasari gambar.",
                ],
                "conclusion": "Kalimat “dibuat dengan Python” hanya menyebut alat; ia tidak mengidentifikasi perhitungan yang dilakukan.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P02",
            "ordinal": 2,
            "problem_summary": "Rancang struktur proyek untuk data populasi mingguan dan bedakan input yang tidak boleh disunting dari keluaran yang dapat dibuat ulang.",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": "Pisahkan data mentah, data turunan, kode transformasi, notebook, keluaran, dan dokumentasi."},
            "check": {
                "type": "structured",
                "final_answer": "Data mentah dipertahankan byte demi byte; data turunan, gambar, dan tabel harus dapat dibuat ulang.",
                "required_evidence": [
                    "Direktori raw dan derived dipisahkan.",
                    "Transformasi disimpan sebagai kode.",
                    "Manifest sekurang-kurangnya memuat jalur relatif, jumlah byte, dan SHA-256.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Simpan unduhan asli di data/raw tanpa penyuntingan manual.",
                    "Tulis skrip yang membaca raw dan menghasilkan data/derived.",
                    "Tempatkan fungsi model di src, narasi di notebooks, dan artefak yang dapat dibuat ulang di outputs.",
                    "Buat README, requirements.lock, dan manifest.tsv yang diurutkan secara deterministik.",
                ],
                "conclusion": "Pemisahan ini memungkinkan keluaran dihapus dan dibangun ulang tanpa kehilangan saksi sumber.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P03",
            "ordinal": 3,
            "problem_summary": "Periksa satuan dan tanda parameter laju dalam hukum pendinginan Newton.",
            "article_link_ids": [],
            "source_formula_occurrences": [
                "\\(k\\)",
                "\\(kt\\)",
                "\\(\\frac{dT}{dt}=-k(T-T_\\infty)\\)",
            ],
            "provenance": provenance(),
            "hint": {"text": "Eksponen harus tak berdimensi dan kedua ruas persamaan diferensial harus memiliki satuan suhu per waktu."},
            "check": {
                "type": "quantitative",
                "final_answer": "Jika waktu dalam menit, maka \\([k]=\\mathrm{menit}^{-1}\\); \\(kt\\) tak berdimensi; \\(k>0\\) membuat selisih suhu menyusut menuju nol.",
                "required_evidence": [
                    "\\(\\left[\\frac{dT}{dt}\\right]=\\frac{\\mathrm{suhu}}{\\mathrm{waktu}}\\).",
                    "\\([k(T-T_\\infty)]=\\mathrm{waktu}^{-1}\\times\\mathrm{suhu}\\).",
                    "Untuk \\(T>T_\\infty\\) dan \\(k>0\\), turunan suhu negatif.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Karena \\(T\\) dan \\(T_\\infty\\) bersatuan °C, selisihnya juga bersatuan °C.",
                    "Agar ruas kanan bersatuan °C/menit, \\(k\\) harus bersatuan \\(\\mathrm{menit}^{-1}\\).",
                    "Maka \\(kt\\) tidak memiliki satuan dan sah berada di dalam fungsi eksponensial.",
                    "Untuk \\(T>T_\\infty\\), \\(k>0\\) memberi \\(\\frac{dT}{dt}<0\\); untuk \\(T<T_\\infty\\), \\(\\frac{dT}{dt}>0\\).",
                ],
                "conclusion": "Solusi mendekati \\(T_\\infty\\) ketika \\(t\\) bertambah.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P04",
            "ordinal": 4,
            "problem_summary": "Bandingkan keadaan acak global dengan pembangkit acak lokal yang berbenih eksplisit.",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": "Tanyakan kode mana saja yang dapat mengonsumsi urutan acak yang sama tanpa terlihat."},
            "check": {
                "type": "qualitative",
                "final_answer": "Pembangkit lokal membatasi keadaan dan dependensi ke objek yang diteruskan secara eksplisit, sehingga urutan konsumsi lebih mudah dilacak.",
                "required_evidence": [
                    "Keadaan global dapat diubah oleh fungsi atau pustaka lain.",
                    "Objek Generator dapat diberi nama, diteruskan, dan diuji secara lokal.",
                    "Benih tetap mengulang satu realisasi, bukan membuktikan keterwakilan statistik.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "np.random.seed mengubah keadaan bersama dalam modul lama.",
                    "default_rng membuat objek Generator yang memiliki keadaan sendiri.",
                    "Perubahan konsumsi acak di komponen lain tidak menggeser urutan objek lokal jika objek tidak dibagikan.",
                    "Untuk menilai kestabilan terhadap keacakan, jalankan beberapa benih dan laporkan semuanya secara terpisah.",
                ],
                "conclusion": "Pembangkit lokal biasanya memberi batas dependensi yang lebih jelas.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P05",
            "ordinal": 5,
            "problem_summary": "Hitung prediksi suhu model pada \\(t=10\\) menit untuk parameter yang diberikan.",
            "article_link_ids": [],
            "source_formula_occurrences": [
                "\\(T(t)=T_\\infty+(T_0-T_\\infty)e^{-kt}\\)"
            ],
            "provenance": provenance(),
            "hint": {"text": "Substitusikan selisih awal \\(92-22=70\\) dan hitung \\(e^{-0.7}\\)."},
            "check": {
                "type": "quantitative",
                "final_answer": "56.76 °C",
                "tolerances": {"absolute_c": 0.01},
                "formula": "T(10)=22+70e^{-0.7}",
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Hitung \\(kt=0.07(10)=0.7\\).",
                    "Hitung \\(e^{-0.7}\\approx0.496585\\).",
                    "Kalikan dengan 70 untuk memperoleh sekitar 34.7610.",
                    "Tambahkan suhu lingkungan 22 °C.",
                ],
                "conclusion": "\\(T(10)\\approx56.76\\) °C.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P06",
            "ordinal": 6,
            "problem_summary": "Jelaskan kebocoran informasi ketika data uji dipilih setelah seluruh hasil dilihat.",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": "Jika pilihan data uji dipengaruhi oleh hasil, data itu telah memengaruhi keputusan pemodelan walaupun tidak masuk ke fungsi objektif."},
            "check": {
                "type": "qualitative",
                "final_answer": "Pemisahan harus ditetapkan sebelum estimasi dan sebelum melihat metrik kandidat; data uji baru dibuka setelah alur analisis dibekukan.",
                "required_evidence": [
                    "Pilihan pascahasil menyesuaikan evaluasi terhadap data yang sudah diketahui.",
                    "Urutan aman: tetapkan tujuan, bagi data, kembangkan prosedur dengan data latih, bekukan prosedur, lalu evaluasi data uji.",
                    "Setelah data uji dipakai untuk revisi, ia bukan lagi evaluasi akhir yang independen.",
                ],
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Tentukan unit pembagian dan aturan pemisahan data sebelum pencocokan.",
                    "Simpan indeks data latih dan data uji sebagai bagian dari konfigurasi.",
                    "Gunakan data latih untuk estimasi serta pengembangan prosedur.",
                    "Bekukan kode dan ambang pemeriksaan sebelum membuka metrik data uji.",
                    "Jika hasil evaluasi pada data uji memicu revisi, nyatakan hal itu dan buat evaluasi baru dengan data lain bila tersedia.",
                ],
                "conclusion": "Kebocoran adalah pengaruh informasi yang tidak tercatat, bukan hanya baris data yang dimasukkan langsung ke estimator.",
            },
        },
        {
            "problem_id": f"{UNIT_ID}-P07",
            "ordinal": 7,
            "problem_summary": "Jalankan notebook bersih, cocokkan identitas dan diagnostik, lalu jelaskan dampak perubahan benih.",
            "article_link_ids": [],
            "source_formula_occurrences": [],
            "provenance": provenance(),
            "hint": {"text": "Bedakan kontrak yang tetap—model, waktu, parameter simulasi, dan aturan serialisasi—dari realisasi galat acak yang berubah."},
            "check": {
                "type": "executable",
                "final_answer": "Benih 20260822 menghasilkan hash 1000bc1092f173258d2be37e4f8906ea0933708582d09768ce96eed739be337e, \\(\\hat{k}=0.07287235\\), \\(\\hat{T}_\\infty=22.63964536\\) °C, \\(\\mathrm{RMSE}=0.31976406\\) °C, dan \\(\\mathrm{MAE}_{\\text{data uji}}=0.17952331\\) °C.",
                "notebook_check": "Semua sel kode berjalan dari keadaan bersih dan semua pemeriksaan eksplisit lulus.",
                "required_evidence": [
                    "Benih baru mengubah realisasi galat, hash data, estimasi, dan metrik numerik.",
                    "Model, waktu pengamatan, parameter pembangkit data, serta aturan serialisasi tetap sama.",
                    "Perubahan benih harus diungkapkan karena mengubah identitas data dan hasil yang dilaporkan.",
                ],
                "tolerances": {
                    "k_absolute": 0.00000001,
                    "temperature_absolute_c": 0.00000001,
                    "metric_absolute_c": 0.00000001,
                },
            },
            "solution_or_rubric": {
                "type": "worked_solution",
                "steps": [
                    "Mulai ulang kernel, hapus keluaran, dan jalankan semua sel berurutan.",
                    "Cocokkan hash, parameter, RMSE, dan MAE dengan pemeriksaan notebook.",
                    "Ubah hanya benih, lalu jalankan ulang seluruh notebook.",
                    "Hash data, realisasi suhu, estimasi, dan metrik berubah; fungsi model, satuan, waktu pengamatan, serta aturan serialisasi tetap.",
                    "Catat benih baru dan jangan menyajikan keluaran baru sebagai byte yang sama dengan keluaran lama.",
                ],
                "conclusion": "Perubahan yang disengaja sah apabila identitas konfigurasi dan artefaknya ikut berubah secara terlihat.",
            },
            "notebook": {
                "path": "source/id-ID/O005-BRIDGE-C1/notebooks/bridge-c1-reproducible-workflow.ipynb",
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
