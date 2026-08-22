#!/usr/bin/env python3
"""Build the twelve deterministic, offline Chapter 14 project packets.

The packets are independently authored pedagogical starting points.  They do
not contain code or data from the papers cited by the source chapter and do
not claim to reproduce any published result.
"""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIT_ID = "O005-LEGA-V101-CH14"
PROJECT_ROOT = ROOT / "source" / "id-ID" / UNIT_ID / "projects"
ARCHIVE_ROOT = ROOT / "source" / "id-ID" / UNIT_ID / "project_archives"
CATALOG_PATH = ROOT / "backend" / "projects" / f"{UNIT_ID}.projects.json"
LOCK = (
    "# Runtime: CPython 3.13.9\n"
    "# Fully offline numerical/visualization closure\n"
    "numpy==2.4.4\n"
    "scipy==1.17.1\n"
    "matplotlib==3.10.9\n"
)
ZIP_DATE = (1980, 1, 1, 0, 0, 0)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def lines(text: str) -> list[str]:
    text = text.strip("\n") + "\n"
    return text.splitlines(keepends=True)


def markdown_cell(cell_id: str, text: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": lines(text),
    }


def code_cell(cell_id: str, code: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": [],
        "source": lines(code),
    }


PROJECTS = [
    {
        "ordinal": 1,
        "title": "Kecerdasan Kolektif dan Agregasi Pendapat",
        "core": "collective-intelligence",
        "question": "Kapan agregasi berbobot memperbaiki perkiraan kelompok, dan kapan konvergensi sosial hanya menyamarkan keragaman informasi?",
        "assumptions": "Agen mengamati sinyal skalar yang sama dengan simpangan baku berbeda. Bobot menyatakan presisi yang diketahui, sedangkan pembaruan sosial mencampurkan pendapat pribadi dan rerata kelompok.",
        "limitations": "Model tidak memuat jaringan kepercayaan, bias sistematis bersama, perilaku strategis, atau cara realistis untuk mengetahui presisi setiap agen.",
        "checks": [
            "Ragam pendapat turun setelah pembaruan sosial.",
            "Perkiraan kolektif tetap hingga 0,20 dari sinyal sintetis.",
            "Semua bobot dan keadaan bernilai hingga.",
        ],
        "model_code": r'''
n_agents = 81
true_signal = 0.65
precision = rng.uniform(2.0, 8.0, n_agents)
sigma = 1.0 / np.sqrt(precision)
initial_opinions = true_signal + rng.normal(0.0, sigma)
weights = precision / precision.sum()
collective_estimate = float(np.sum(weights * initial_opinions))

opinions = initial_opinions.copy()
variance_history = [float(np.var(opinions))]
for _ in range(16):
    group_mean = float(np.sum(weights * opinions))
    opinions = 0.68 * opinions + 0.32 * group_mean
    variance_history.append(float(np.var(opinions)))
final_opinions = opinions.copy()
''',
        "assert_code": r'''
assert np.isfinite(initial_opinions).all() and np.isfinite(weights).all()
assert variance_history[-1] < 0.01 * variance_history[0]
assert abs(collective_estimate - true_signal) < 0.20
np.testing.assert_allclose(weights.sum(), 1.0, atol=1e-14)
''',
        "plot_code": r'''
fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
axes[0].hist(initial_opinions, bins=14, alpha=0.75, label="awal")
axes[0].hist(final_opinions, bins=14, alpha=0.75, label="setelah pembaruan")
axes[0].axvline(true_signal, color="black", linestyle="--", label="sinyal")
axes[0].set(xlabel="pendapat", ylabel="jumlah agen", title="Sebaran pendapat")
axes[0].legend(fontsize=8)
axes[1].plot(variance_history, marker="o", markersize=3)
axes[1].set(xlabel="langkah sosial", ylabel="ragam", title="Konvergensi kelompok")
fig.tight_layout()
plt.show()
plt.close(fig)
''',
    },
    {
        "ordinal": 2,
        "title": "Sinyal Dini Zoonosis dengan Model SEIR",
        "core": "early-zoonotic-seir",
        "question": "Informasi apa tentang laju pertumbuhan awal yang dapat dipulihkan dari pengamatan wabah zoonotik yang jarang dan berisik?",
        "assumptions": "Populasi homogen dan tertutup mengikuti kompartemen SEIR; parameter tetap selama jendela awal; pengamatan sintetis merupakan prevalensi infeksi dengan gangguan kecil.",
        "limitations": "Tidak ada struktur umur, pelaporan tertunda, limpahan berulang dari hewan, perubahan perilaku, atau variasi spasial.",
        "checks": [
            "Jumlah fraksi SEIR terjaga hingga toleransi numerik.",
            "Semua kompartemen tetap nonnegatif.",
            "Puncak infeksi terjadi setelah kondisi awal untuk R0 lebih besar dari satu.",
        ],
        "model_code": r'''
beta, sigma, gamma = 0.72, 1.0 / 4.5, 1.0 / 6.0
R0 = beta / gamma
t_eval = np.linspace(0.0, 120.0, 481)

def seir_rhs(t, y):
    S, E, I, R = y
    return [-beta * S * I, beta * S * I - sigma * E, sigma * E - gamma * I, gamma * I]

solution = solve_ivp(seir_rhs, (t_eval[0], t_eval[-1]), [0.997, 0.002, 0.001, 0.0], t_eval=t_eval, rtol=1e-9, atol=1e-11)
S, E, I, R = solution.y
observation_days = np.arange(0, 121, 5)
I_observed = np.clip(np.interp(observation_days, t_eval, I) + rng.normal(0.0, 0.00035, observation_days.size), 0.0, None)
''',
        "assert_code": r'''
assert solution.success and R0 > 1.0
np.testing.assert_allclose(S + E + I + R, 1.0, atol=2e-8)
assert np.min(solution.y) > -1e-10
assert float(t_eval[np.argmax(I)]) > 5.0 and float(np.max(I)) > I[0]
''',
        "plot_code": r'''
fig, ax = plt.subplots(figsize=(8, 4.2))
for values, label in [(S, "S"), (E, "E"), (I, "I"), (R, "R")]:
    ax.plot(t_eval, values, label=label)
ax.scatter(observation_days, I_observed, s=18, color="black", label="pengamatan I sintetis")
ax.set(xlabel="hari", ylabel="fraksi populasi", title="Lintasan SEIR dan pengamatan dini")
ax.legend(ncol=3, fontsize=8)
fig.tight_layout()
plt.show()
plt.close(fig)
''',
    },
    {
        "ordinal": 3,
        "title": "Waktu Intervensi Nonfarmasi",
        "core": "npi-timing",
        "question": "Seberapa besar perubahan puncak epidemi ketika intervensi nonfarmasi yang sama dimulai pada waktu berbeda?",
        "assumptions": "Model SIR tertutup memakai satu penurunan laju transmisi pada hari intervensi; kepatuhan langsung dan tetap; kondisi awal sama pada semua skenario.",
        "limitations": "Intervensi tidak memiliki biaya, penundaan, kelelahan, heterogenitas, atau respons perilaku endogen.",
        "checks": [
            "Massa SIR terjaga pada semua skenario.",
            "Intervensi dini memberi puncak infeksi lebih rendah daripada intervensi lambat.",
            "Intervensi lambat memberi puncak lebih rendah daripada tanpa intervensi.",
        ],
        "model_code": r'''
gamma, beta0, reduction = 0.10, 0.42, 0.42
t_eval = np.linspace(0.0, 150.0, 601)

def run_sir(start_day):
    def rhs(t, y):
        S, I, R = y
        beta_t = beta0 if start_day is None or t < start_day else beta0 * reduction
        return [-beta_t * S * I, beta_t * S * I - gamma * I, gamma * I]
    return solve_ivp(rhs, (0.0, 150.0), [0.999, 0.001, 0.0], t_eval=t_eval, rtol=1e-8, atol=1e-10, max_step=0.25)

npi_runs = {"hari 12": run_sir(12.0), "hari 22": run_sir(22.0), "tanpa NPI": run_sir(None)}
peaks = {name: float(run.y[1].max()) for name, run in npi_runs.items()}
''',
        "assert_code": r'''
for run in npi_runs.values():
    assert run.success and np.min(run.y) > -1e-9
    np.testing.assert_allclose(run.y.sum(axis=0), 1.0, atol=2e-8)
assert peaks["hari 12"] < peaks["hari 22"] < peaks["tanpa NPI"]
''',
        "plot_code": r'''
fig, ax = plt.subplots(figsize=(8, 4.2))
for name, run in npi_runs.items():
    ax.plot(t_eval, run.y[1], label=f"{name}; puncak={peaks[name]:.3f}")
ax.axvline(12, color="gray", linestyle=":", linewidth=1)
ax.axvline(22, color="gray", linestyle=":", linewidth=1)
ax.set(xlabel="hari", ylabel="fraksi terinfeksi", title="Pengaruh waktu NPI pada puncak epidemi")
ax.legend(fontsize=8)
fig.tight_layout()
plt.show()
plt.close(fig)
''',
    },
    {
        "ordinal": 4,
        "title": "Vaksinasi dan Beban Layanan Kesehatan",
        "core": "vaccination-healthcare-burden",
        "question": "Bagaimana cakupan vaksin mengubah puncak kebutuhan perawatan dalam model transparan yang memisahkan perlindungan terhadap infeksi dan penyakit berat?",
        "assumptions": "Kekebalan awal proporsional terhadap cakupan dan efektivitas terhadap infeksi; risiko perawatan pada kasus terobosan berkurang secara linier; dinamika berikutnya mengikuti SIR.",
        "limitations": "Tidak ada peluruhan kekebalan, kelompok umur, kapasitas yang memengaruhi mortalitas, dosis berulang, atau seleksi varian.",
        "checks": [
            "Massa SIR dan nonnegativitas terjaga.",
            "Puncak beban layanan turun monoton saat cakupan naik.",
            "Semua skenario memakai parameter penyakit yang sama.",
        ],
        "model_code": r'''
beta, gamma = 0.36, 0.11
ve_infection, ve_severe, base_hospitalization = 0.70, 0.85, 0.08
t_eval = np.linspace(0.0, 160.0, 641)

def vaccinated_run(coverage):
    immune = coverage * ve_infection
    I0 = 0.001
    y0 = [1.0 - immune - I0, I0, immune]
    def rhs(t, y):
        S, I, R = y
        return [-beta * S * I, beta * S * I - gamma * I, gamma * I]
    run = solve_ivp(rhs, (0.0, 160.0), y0, t_eval=t_eval, rtol=1e-9, atol=1e-11)
    severe_multiplier = 1.0 - coverage * ve_severe
    burden = base_hospitalization * severe_multiplier * run.y[1]
    return run, burden

coverage_runs = {coverage: vaccinated_run(coverage) for coverage in (0.0, 0.5, 0.8)}
burden_peaks = {coverage: float(burden.max()) for coverage, (_, burden) in coverage_runs.items()}
''',
        "assert_code": r'''
for run, burden in coverage_runs.values():
    assert run.success and np.min(run.y) > -1e-9 and np.min(burden) >= 0.0
    np.testing.assert_allclose(run.y.sum(axis=0), 1.0, atol=2e-8)
assert burden_peaks[0.8] < burden_peaks[0.5] < burden_peaks[0.0]
''',
        "plot_code": r'''
fig, ax = plt.subplots(figsize=(8, 4.2))
for coverage, (_, burden) in coverage_runs.items():
    ax.plot(t_eval, 100000 * burden, label=f"cakupan {coverage:.0%}")
ax.axhline(200, color="black", linestyle="--", linewidth=1, label="kapasitas ilustratif")
ax.set(xlabel="hari", ylabel="kebutuhan perawatan per 100.000", title="Beban layanan pada beberapa cakupan")
ax.legend(fontsize=8)
fig.tight_layout()
plt.show()
plt.close(fig)
''',
    },
    {
        "ordinal": 5,
        "title": "Dinamika Glukosa–Insulin",
        "core": "glucose-insulin-ode",
        "question": "Parameter mana yang mengatur tinggi puncak glukosa dan waktu pulih setelah masukan makanan sintetis?",
        "assumptions": "Tiga keadaan—glukosa, aksi insulin, dan insulin—mengikuti ODE minimal; masukan makanan berupa pulsa Gaussian yang diketahui; keadaan awal berada pada basal.",
        "limitations": "Model bukan alat diagnosis dan mengabaikan variasi organ, hormon lain, ketidakpastian makanan, serta perbedaan pasien.",
        "checks": [
            "Penyelesaian ODE berhasil dan semua keadaan hingga.",
            "Glukosa naik di atas basal setelah pulsa makanan.",
            "Glukosa mendekati basal kembali pada akhir simulasi.",
        ],
        "model_code": r'''
G_b, I_b = 90.0, 10.0
t_eval = np.linspace(0.0, 240.0, 961)

def meal_input(t):
    return 2.8 * np.exp(-0.5 * ((t - 25.0) / 10.0) ** 2)

def glucose_rhs(t, y):
    G, X, I = y
    dG = -0.025 * (G - G_b) - X * G + meal_input(t)
    dX = -0.080 * X + 0.00012 * (I - I_b)
    dI = -0.120 * (I - I_b) + 0.40 * max(G - G_b, 0.0)
    return [dG, dX, dI]

glucose_run = solve_ivp(glucose_rhs, (0.0, 240.0), [G_b, 0.0, I_b], t_eval=t_eval, rtol=1e-9, atol=1e-10)
G, X, insulin = glucose_run.y
sample_minutes = np.arange(0, 241, 15)
synthetic_glucose = np.interp(sample_minutes, t_eval, G) + rng.normal(0.0, 1.2, sample_minutes.size)
''',
        "assert_code": r'''
assert glucose_run.success and np.isfinite(glucose_run.y).all()
assert float(G.max()) > G_b + 8.0
assert abs(float(G[-1]) - G_b) < 2.0
assert np.min(G) > 0.0 and np.min(insulin) > 0.0
''',
        "plot_code": r'''
fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
axes[0].plot(t_eval, G, label="glukosa model")
axes[0].scatter(sample_minutes, synthetic_glucose, s=16, color="black", label="data sintetis")
axes[0].axhline(G_b, color="gray", linestyle="--", linewidth=1)
axes[0].set(ylabel="glukosa (satuan ilustratif)", title="Respons terhadap masukan makanan")
axes[0].legend(fontsize=8)
axes[1].plot(t_eval, insulin, color="tab:orange", label="insulin")
axes[1].plot(t_eval, 10 * meal_input(t_eval), color="tab:green", alpha=0.7, label="10 × masukan")
axes[1].set(xlabel="menit", ylabel="satuan ilustratif")
axes[1].legend(fontsize=8)
fig.tight_layout()
plt.show()
plt.close(fig)
''',
    },
    {
        "ordinal": 6,
        "title": "Penyelarasan Visual dalam Kerumunan",
        "core": "crowd-visual-alignment",
        "question": "Seberapa cepat aturan penyelarasan visual lokal menghasilkan gerak kolektif dari arah awal acak?",
        "assumptions": "Agen bergerak pada domain periodik, menggabungkan arah sendiri dengan arah rata-rata tetangga dalam radius visual tetap, dan menerima gangguan sudut kecil.",
        "limitations": "Tetangga ditentukan hanya oleh jarak periodik; tidak ada rintangan, bidang pandang berarah, oklusi, tabrakan, perbedaan kecepatan, atau kepanikan.",
        "checks": [
            "Semua posisi tetap di domain periodik.",
            "Polarisasi akhir melampaui polarisasi awal dengan selisih nyata.",
            "Riwayat polarisasi selalu berada antara nol dan satu.",
        ],
        "model_code": r'''
n_agents, n_steps = 70, 150
positions = rng.uniform(0.0, 1.0, (n_agents, 2))
angles = rng.uniform(-np.pi, np.pi, n_agents)
initial_positions = positions.copy()
initial_angles = angles.copy()
polarization = []
neighbor_counts = []
visual_radius = 0.27

for _ in range(n_steps):
    displacement = positions[None, :, :] - positions[:, None, :]
    displacement = (displacement + 0.5) % 1.0 - 0.5
    neighbors = np.sum(displacement**2, axis=2) <= visual_radius**2
    counts = neighbors.sum(axis=1)
    local_cos = neighbors @ np.cos(angles) / counts
    local_sin = neighbors @ np.sin(angles) / counts
    local_angle = np.arctan2(local_sin, local_cos)
    own = np.column_stack([np.cos(angles), np.sin(angles)])
    target = np.column_stack([np.cos(local_angle), np.sin(local_angle)])
    blended = 0.55 * own + 0.45 * target
    angles = np.arctan2(blended[:, 1], blended[:, 0]) + rng.normal(0.0, 0.025, n_agents)
    positions = (positions + 0.012 * np.column_stack([np.cos(angles), np.sin(angles)])) % 1.0
    polarization.append(float(np.hypot(np.cos(angles).mean(), np.sin(angles).mean())))
    neighbor_counts.append(float(counts.mean()))
''',
        "assert_code": r'''
initial_pol = float(np.hypot(np.cos(initial_angles).mean(), np.sin(initial_angles).mean()))
assert np.all((positions >= 0.0) & (positions < 1.0))
assert polarization[-1] > initial_pol + 0.35
assert np.all((np.asarray(polarization) >= 0.0) & (np.asarray(polarization) <= 1.0 + 1e-12))
assert 1.0 < np.mean(neighbor_counts) < n_agents
''',
        "plot_code": r'''
fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))
axes[0].quiver(initial_positions[:, 0], initial_positions[:, 1], np.cos(initial_angles), np.sin(initial_angles), angles="xy", scale=18)
axes[0].set(title="awal", xlim=(0, 1), ylim=(0, 1), aspect="equal")
axes[1].quiver(positions[:, 0], positions[:, 1], np.cos(angles), np.sin(angles), angles="xy", scale=18)
axes[1].set(title="akhir", xlim=(0, 1), ylim=(0, 1), aspect="equal")
axes[2].plot(polarization)
axes[2].set(xlabel="langkah", ylabel="polarisasi", title="keteraturan global", ylim=(0, 1.05))
fig.tight_layout()
plt.show()
plt.close(fig)
''',
    },
    {
        "ordinal": 7,
        "title": "Dengue: Model Sederhana, Vektor–Inang, dan Keteridentifikasian",
        "core": "dengue-simple-vector-host-identifiability",
        "question": "Dapatkah kurva prevalensi manusia saja membedakan laju penularan manusia-ke-vektor dari vektor-ke-manusia?",
        "assumptions": "Data sintetis berasal dari model vektor–inang Euler dengan populasi ternormalisasi; model SIR sederhana dan kisi pasangan laju dibandingkan pada pengamatan yang sama.",
        "limitations": "Model mengabaikan musim, serotipe, imunitas silang, umur nyamuk, pelaporan kasus, dan struktur ruang; kisi parameter hanya ilustrasi keteridentifikasian praktis.",
        "checks": [
            "Massa manusia dan vektor terjaga pada simulasi sumber.",
            "Pencarian kisi menemukan beberapa pasangan laju yang berbeda dengan galat rendah.",
            "Model sederhana dan vektor–inang menghasilkan prediksi hingga dan nonnegatif.",
        ],
        "model_code": r'''
dt, steps = 0.25, 360
times = dt * np.arange(steps + 1)

def simulate_vector_host(beta_hv, beta_vh):
    y = np.empty((steps + 1, 5), dtype=float)
    y[0] = [0.995, 0.005, 0.0, 0.995, 0.005]
    gamma_h, mu_v = 0.12, 0.08
    for k in range(steps):
        Sh, Ih, Rh, Sv, Iv = y[k]
        flux_h = beta_vh * Sh * Iv
        flux_v = beta_hv * Sv * Ih
        dy = np.array([-flux_h, flux_h - gamma_h * Ih, gamma_h * Ih, mu_v - flux_v - mu_v * Sv, flux_v - mu_v * Iv])
        y[k + 1] = y[k] + dt * dy
    return y

def simulate_simple(beta):
    y = np.empty((steps + 1, 3), dtype=float)
    y[0] = [0.995, 0.005, 0.0]
    gamma_h = 0.12
    for k in range(steps):
        S, I, R = y[k]
        flux = beta * S * I
        y[k + 1] = y[k] + dt * np.array([-flux, flux - gamma_h * I, gamma_h * I])
    return y

truth = simulate_vector_host(0.78, 0.52)
obs_idx = np.arange(0, steps + 1, 12)
observed = np.clip(truth[obs_idx, 1] + rng.normal(0.0, 0.0006, obs_idx.size), 0.0, None)

simple_betas = np.linspace(0.08, 0.80, 73)
simple_errors = np.array([np.mean((simulate_simple(b)[obs_idx, 1] - observed) ** 2) for b in simple_betas])
best_simple = simulate_simple(float(simple_betas[np.argmin(simple_errors)]))

grid = np.linspace(0.30, 1.00, 19)
surface = np.empty((grid.size, grid.size))
for i, beta_hv in enumerate(grid):
    for j, beta_vh in enumerate(grid):
        surface[i, j] = np.mean((simulate_vector_host(float(beta_hv), float(beta_vh))[obs_idx, 1] - observed) ** 2)
best_flat = np.argsort(surface, axis=None)[:18]
best_pairs = np.array([(grid[np.unravel_index(idx, surface.shape)[0]], grid[np.unravel_index(idx, surface.shape)[1]]) for idx in best_flat])
best_i, best_j = np.unravel_index(int(np.argmin(surface)), surface.shape)
best_vector = simulate_vector_host(float(grid[best_i]), float(grid[best_j]))
''',
        "assert_code": r'''
np.testing.assert_allclose(truth[:, :3].sum(axis=1), 1.0, atol=2e-10)
np.testing.assert_allclose(truth[:, 3:].sum(axis=1), 1.0, atol=2e-10)
assert np.min(truth) >= 0.0 and np.min(best_simple) >= 0.0
assert np.ptp(best_pairs[:, 0]) > 0.15 and np.ptp(best_pairs[:, 1]) > 0.15
assert np.isfinite(surface).all()
''',
        "plot_code": r'''
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].scatter(times[obs_idx], observed, s=18, color="black", label="data manusia sintetis")
axes[0].plot(times, best_simple[:, 1], label="SIR sederhana")
axes[0].plot(times, best_vector[:, 1], label="vektor–inang")
axes[0].set(xlabel="hari", ylabel="prevalensi manusia", title="Dua kelas model")
axes[0].legend(fontsize=8)
image = axes[1].imshow(np.log10(surface + 1e-12), origin="lower", extent=[grid[0], grid[-1], grid[0], grid[-1]], aspect="auto")
axes[1].scatter(best_pairs[:, 1], best_pairs[:, 0], s=10, color="white")
axes[1].set(xlabel="laju vektor→manusia", ylabel="laju manusia→vektor", title="Galat log dan punggung parameter")
fig.colorbar(image, ax=axes[1], label="log10 MSE")
fig.tight_layout()
plt.show()
plt.close(fig)
''',
    },
    {
        "ordinal": 8,
        "title": "Predator–Mangsa dengan Imigrasi",
        "core": "predator-prey-immigration",
        "question": "Bagaimana aliran mangsa dari luar sistem menggeser kesetimbangan dan lintasan predator–mangsa?",
        "assumptions": "Interaksi mengikuti Lotka–Volterra dengan laju imigrasi mangsa konstan; parameter dan lingkungan tetap; kedua populasi kontinu.",
        "limitations": "Tidak ada daya dukung, struktur umur, musim, stokastisitas demografis, atau umpan balik pada imigrasi.",
        "checks": [
            "Lintasan numerik tetap positif dan hingga.",
            "Kesetimbangan predator analitik naik ketika imigrasi positif.",
            "Kondisi kesetimbangan memenuhi ruas kanan ODE.",
        ],
        "model_code": r'''
r, attack, conversion, mortality = 0.80, 0.70, 0.50, 0.30
t_eval = np.linspace(0.0, 100.0, 801)

def equilibrium(immigration):
    prey = mortality / (conversion * attack)
    predator = (r * prey + immigration) / (attack * prey)
    return np.array([prey, predator])

def predator_prey_run(immigration):
    def rhs(t, y):
        prey, predator = y
        return [r * prey - attack * prey * predator + immigration, conversion * attack * prey * predator - mortality * predator]
    eq = equilibrium(immigration)
    initial = eq * np.array([0.72, 1.25])
    return solve_ivp(rhs, (0.0, 100.0), initial, t_eval=t_eval, rtol=1e-9, atol=1e-11), eq, rhs

immigration_runs = {m: predator_prey_run(m) for m in (0.0, 0.12)}
''',
        "assert_code": r'''
for immigration, (run, eq, rhs) in immigration_runs.items():
    assert run.success and np.isfinite(run.y).all() and np.min(run.y) > 0.0
    np.testing.assert_allclose(rhs(0.0, eq), [0.0, 0.0], atol=1e-12)
assert immigration_runs[0.12][1][1] > immigration_runs[0.0][1][1]
''',
        "plot_code": r'''
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for immigration, (run, eq, _) in immigration_runs.items():
    axes[0].plot(t_eval, run.y[0], label=f"mangsa, m={immigration}")
    axes[0].plot(t_eval, run.y[1], linestyle="--", label=f"predator, m={immigration}")
    axes[1].plot(run.y[0], run.y[1], label=f"m={immigration}")
    axes[1].scatter(*eq, s=25)
axes[0].set(xlabel="waktu", ylabel="populasi", title="Deret waktu")
axes[1].set(xlabel="mangsa", ylabel="predator", title="Bidang fase")
axes[0].legend(fontsize=7)
axes[1].legend(fontsize=8)
fig.tight_layout()
plt.show()
plt.close(fig)
''',
    },
    {
        "ordinal": 9,
        "title": "Ketakutan dan Musim pada Sistem Predator–Mangsa",
        "core": "fear-seasonal-predator-prey",
        "question": "Bagaimana respons antipredator dan pertumbuhan musiman bersama-sama mengubah amplitudo populasi?",
        "assumptions": "Ketakutan mengurangi laju pertumbuhan efektif mangsa melalui faktor rasional; pertumbuhan intrinsik berosilasi sinusoidal; predasi bertipe bilinear.",
        "limitations": "Indeks ketakutan tidak diukur langsung, musim tunggal terlalu sederhana, dan model tidak memuat perlindungan habitat atau keterlambatan reproduksi.",
        "checks": [
            "Semua lintasan tetap positif dan hingga.",
            "Pemaksaan musiman memiliki rentang yang ditentukan.",
            "Menyalakan mekanisme ketakutan mengubah lintasan secara terukur.",
        ],
        "model_code": r'''
r0, season_amp, period, K = 0.75, 0.28, 24.0, 3.0
attack, conversion, mortality = 0.42, 0.32, 0.26
t_eval = np.linspace(0.0, 144.0, 1153)

def seasonal_growth(t):
    return r0 * (1.0 + season_amp * np.sin(2.0 * np.pi * t / period))

def fear_run(fear):
    def rhs(t, y):
        prey, predator = y
        growth = seasonal_growth(t) * prey * (1.0 - prey / K) / (1.0 + fear * predator)
        loss = attack * prey * predator
        return [growth - loss, conversion * loss - mortality * predator]
    return solve_ivp(rhs, (0.0, 144.0), [1.6, 0.55], t_eval=t_eval, rtol=1e-9, atol=1e-11)

fear_runs = {0.0: fear_run(0.0), 0.9: fear_run(0.9)}
forcing = seasonal_growth(t_eval)
''',
        "assert_code": r'''
for run in fear_runs.values():
    assert run.success and np.isfinite(run.y).all() and np.min(run.y) > 0.0
np.testing.assert_allclose(forcing.max() - forcing.min(), 2.0 * r0 * season_amp, rtol=2e-4)
assert np.max(np.abs(fear_runs[0.0].y - fear_runs[0.9].y)) > 0.10
''',
        "plot_code": r'''
fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
for fear, run in fear_runs.items():
    axes[0].plot(t_eval, run.y[0], label=f"mangsa, f={fear}")
    axes[1].plot(t_eval, run.y[1], label=f"predator, f={fear}")
axes[0].plot(t_eval, forcing, color="gray", alpha=0.5, linestyle=":", label="pertumbuhan musiman")
axes[0].set(ylabel="mangsa / pemaksaan", title="Ketakutan dan pemaksaan musiman")
axes[1].set(xlabel="waktu", ylabel="predator")
axes[0].legend(fontsize=8)
axes[1].legend(fontsize=8)
fig.tight_layout()
plt.show()
plt.close(fig)
''',
    },
    {
        "ordinal": 10,
        "title": "Kopling Aroma dan Agen pada Lebah Madu",
        "core": "honeybee-scent-agent-coupling",
        "question": "Apakah aturan gerak yang menggabungkan gradien aroma dan derau cukup untuk menghasilkan akumulasi agen di dekat sumber?",
        "assumptions": "Aroma adalah medan Gaussian statis; tiap lebah bergerak mengikuti gradien lokal ditambah gerak acak kecil; domain dibatasi dan sumber tetap.",
        "limitations": "Tidak ada dinamika turbulensi aroma, komunikasi tarian, penghindaran tumbukan, memori, atau heterogenitas sensorik.",
        "checks": [
            "Semua agen tetap di domain.",
            "Jarak median ke sumber turun selama simulasi.",
            "Medan aroma nonnegatif dan berpuncak dekat sumber.",
        ],
        "model_code": r'''
n_bees, n_steps = 64, 100
source = np.array([0.78, 0.72])
positions = rng.uniform(0.05, 0.95, (n_bees, 2))
paths = np.empty((n_steps + 1, n_bees, 2))
paths[0] = positions
initial_distance = np.linalg.norm(positions - source, axis=1)

def scent(points):
    return np.exp(-np.sum((points - source) ** 2, axis=-1) / 0.10)

for step in range(n_steps):
    displacement = source - positions
    distance = np.linalg.norm(displacement, axis=1, keepdims=True)
    direction = displacement / np.maximum(distance, 1e-12)
    coupling = 0.35 + 0.65 * scent(positions)[:, None]
    noise = rng.normal(0.0, 0.0035, positions.shape)
    positions = np.clip(positions + 0.013 * coupling * direction + noise, 0.0, 1.0)
    paths[step + 1] = positions
final_distance = np.linalg.norm(positions - source, axis=1)
xg = np.linspace(0.0, 1.0, 80)
Xg, Yg = np.meshgrid(xg, xg)
scent_field = scent(np.stack([Xg, Yg], axis=-1))
''',
        "assert_code": r'''
assert np.all((positions >= 0.0) & (positions <= 1.0))
assert float(np.median(final_distance)) < 0.45 * float(np.median(initial_distance))
assert np.min(scent_field) >= 0.0 and np.max(scent_field) > 0.99
''',
        "plot_code": r'''
fig, axes = plt.subplots(1, 2, figsize=(9, 4))
contour = axes[0].contourf(Xg, Yg, scent_field, levels=15, cmap="YlOrBr")
for bee in range(0, n_bees, 4):
    axes[0].plot(paths[:, bee, 0], paths[:, bee, 1], color="tab:blue", alpha=0.5, linewidth=0.8)
axes[0].scatter(*source, marker="*", s=120, color="red", label="sumber")
axes[0].set(title="Lintasan di medan aroma", xlim=(0, 1), ylim=(0, 1), aspect="equal")
axes[0].legend(fontsize=8)
fig.colorbar(contour, ax=axes[0], label="intensitas")
axes[1].hist(initial_distance, bins=12, alpha=0.65, label="awal")
axes[1].hist(final_distance, bins=12, alpha=0.65, label="akhir")
axes[1].set(xlabel="jarak ke sumber", ylabel="jumlah lebah", title="Perubahan jarak")
axes[1].legend(fontsize=8)
fig.tight_layout()
plt.show()
plt.close(fig)
''',
    },
    {
        "ordinal": 11,
        "title": "Habitat dan Migrasi Paus",
        "core": "whale-habitat-migration",
        "question": "Bagaimana medan kesesuaian habitat sintetis dan kecenderungan migrasi menghasilkan lintasan populasi yang dapat divalidasi?",
        "assumptions": "Paus bergerak pada bidang bujur–lintang sederhana menuju lintang habitat optimum yang berubah musiman, dengan variasi individu dan derau kecil.",
        "limitations": "Peta bukan geografi nyata; tidak ada arus, batimetri, kapal, suara, struktur sosial, mortalitas, atau data telemetri sungguhan.",
        "checks": [
            "Lintasan tetap dalam batas domain sintetis.",
            "Jarak median ke optimum musim akhir berkurang.",
            "Medan habitat dibatasi antara nol dan satu.",
        ],
        "model_code": r'''
n_whales, n_days = 28, 120
longitude = rng.uniform(-24.0, 24.0, n_whales)
latitude = rng.normal(18.0, 3.0, n_whales)
tracks = np.empty((n_days + 1, n_whales, 2))
tracks[0, :, 0], tracks[0, :, 1] = longitude, latitude

def target_latitude(day):
    return 18.0 + 36.0 * (day / n_days)

for day in range(n_days):
    target = target_latitude(day + 1)
    latitude += 0.055 * (target - latitude) + rng.normal(0.0, 0.24, n_whales)
    longitude += -0.020 * longitude + rng.normal(0.0, 0.20, n_whales)
    latitude = np.clip(latitude, 5.0, 65.0)
    longitude = np.clip(longitude, -30.0, 30.0)
    tracks[day + 1, :, 0], tracks[day + 1, :, 1] = longitude, latitude

final_target = target_latitude(n_days)
initial_target_distance = np.abs(tracks[0, :, 1] - final_target)
final_target_distance = np.abs(tracks[-1, :, 1] - final_target)
lon_grid = np.linspace(-30.0, 30.0, 100)
lat_grid = np.linspace(5.0, 65.0, 100)
Lon, Lat = np.meshgrid(lon_grid, lat_grid)
habitat = np.exp(-0.5 * ((Lat - final_target) / 7.0) ** 2 - 0.5 * (Lon / 16.0) ** 2)
''',
        "assert_code": r'''
assert np.all((tracks[:, :, 0] >= -30.0) & (tracks[:, :, 0] <= 30.0))
assert np.all((tracks[:, :, 1] >= 5.0) & (tracks[:, :, 1] <= 65.0))
assert float(np.median(final_target_distance)) < 0.35 * float(np.median(initial_target_distance))
assert np.min(habitat) >= 0.0 and np.max(habitat) <= 1.0
''',
        "plot_code": r'''
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
for whale in range(0, n_whales, 2):
    axes[0].plot(tracks[:, whale, 0], tracks[:, whale, 1], alpha=0.65, linewidth=1)
axes[0].axhline(final_target, color="black", linestyle="--", linewidth=1, label="optimum akhir")
axes[0].set(xlabel="bujur sintetis", ylabel="lintang sintetis", title="Lintasan migrasi")
axes[0].legend(fontsize=8)
image = axes[1].contourf(Lon, Lat, habitat, levels=16, cmap="viridis")
axes[1].scatter(tracks[-1, :, 0], tracks[-1, :, 1], s=12, color="white", edgecolor="black", linewidth=0.3)
axes[1].set(xlabel="bujur sintetis", ylabel="lintang sintetis", title="Kesesuaian habitat akhir")
fig.colorbar(image, ax=axes[1], label="kesesuaian")
fig.tight_layout()
plt.show()
plt.close(fig)
''',
    },
    {
        "ordinal": 12,
        "title": "Kolam Lelehan Arktik dengan Model Ising",
        "core": "arctic-melt-pond-ising",
        "question": "Bagaimana kopling tetangga, pemaksaan eksternal, dan jadwal pendinginan mengubah pola biner es–kolam dalam model Ising pedagogis?",
        "assumptions": "Kisi periodik memetakan spin +1 ke kolam dan −1 ke es; energi tetangga dan medan eksternal mengatur pembalikan; pembaruan Metropolis berurutan acak.",
        "limitations": "Spin bukan hidrologi fisik; tidak ada konservasi air, ketebalan es, geometri nyata, radiasi, aliran, atau kalibrasi observasional.",
        "checks": [
            "Spin selalu bernilai −1 atau +1.",
            "Relaksasi akhir tidak menaikkan energi dari keadaan awal.",
            "Fraksi kolam dan riwayat energi hingga serta berada pada rentang sah.",
        ],
        "model_code": r'''
L, coupling, field = 30, 1.0, 0.10
spins = rng.choice(np.array([-1, 1], dtype=int), size=(L, L))
initial_spins = spins.copy()

def ising_energy(state):
    neighbor_sum = np.roll(state, 1, axis=0) + np.roll(state, 1, axis=1)
    return float(-coupling * np.sum(state * neighbor_sum) - field * np.sum(state))

initial_energy = ising_energy(spins)
energy_history = [initial_energy]
temperature_schedule = np.linspace(2.8, 0.45, 42)
for temperature in temperature_schedule:
    for _ in range(L * L):
        i, j = rng.integers(0, L, size=2)
        neighbor = spins[(i - 1) % L, j] + spins[(i + 1) % L, j] + spins[i, (j - 1) % L] + spins[i, (j + 1) % L]
        delta = 2.0 * spins[i, j] * (coupling * neighbor + field)
        if delta <= 0.0 or rng.random() < np.exp(-delta / temperature):
            spins[i, j] *= -1
    energy_history.append(ising_energy(spins))

# Relaksasi rakus membuat pemeriksaan energi akhir deterministik dan transparan.
for _ in range(8):
    for i in range(L):
        for j in range(L):
            neighbor = spins[(i - 1) % L, j] + spins[(i + 1) % L, j] + spins[i, (j - 1) % L] + spins[i, (j + 1) % L]
            delta = 2.0 * spins[i, j] * (coupling * neighbor + field)
            if delta < 0.0:
                spins[i, j] *= -1
    energy_history.append(ising_energy(spins))
final_energy = ising_energy(spins)
melt_fraction = float(np.mean(spins == 1))
''',
        "assert_code": r'''
assert set(np.unique(spins)).issubset({-1, 1})
assert final_energy <= initial_energy + 1e-12
assert 0.0 <= melt_fraction <= 1.0
assert np.isfinite(energy_history).all()
''',
        "plot_code": r'''
fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.5))
axes[0].imshow(initial_spins, cmap="Blues", vmin=-1, vmax=1)
axes[0].set(title="kisi awal")
axes[1].imshow(spins, cmap="Blues", vmin=-1, vmax=1)
axes[1].set(title=f"kisi akhir; kolam={melt_fraction:.2f}")
axes[2].plot(energy_history)
axes[2].set(xlabel="sapuan", ylabel="energi", title="relaksasi energi")
for ax in axes[:2]:
    ax.set_xticks([])
    ax.set_yticks([])
fig.tight_layout()
plt.show()
plt.close(fig)
''',
    },
]


def notebook_for(spec: dict, project_id: str) -> dict:
    prefix = f"p{spec['ordinal']:02d}"
    seed = 2026082200 + spec["ordinal"]
    cells = [
        markdown_cell(
            f"{prefix}-title",
            f"""# {spec['title']}

**ID proyek:** `{project_id}`  
**Status:** titik awal pedagogis yang ditulis secara independen.

Notebook ini menggunakan data sintetis/terbuka saja. Notebook ini **bukan** kode atau data dari makalah yang dikutip dalam bab sumber dan **bukan** klaim reproduksi hasil penelitian mana pun.
""",
        ),
        markdown_cell(
            f"{prefix}-question",
            f"""## Pertanyaan pemodelan

{spec['question']}

Tujuan kerja: tetapkan sistem, jalankan eksperimen deterministik, periksa invarian, visualisasikan perilaku, lalu kritik kecukupan model.
""",
        ),
        code_cell(
            f"{prefix}-setup",
            f"""import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

SEED = {seed}
rng = np.random.default_rng(SEED)
np.set_printoptions(precision=6, suppress=True)
""",
        ),
        markdown_cell(
            f"{prefix}-assumptions",
            f"""## Struktur dan asumsi

{spec['assumptions']}

Semua skala dan parameter di notebook ini bersifat ilustratif. Ubah satu asumsi pada satu waktu dan catat dampaknya pada keluaran serta invarian.
""",
        ),
        code_cell(f"{prefix}-model", spec["model_code"]),
        markdown_cell(
            f"{prefix}-checks-intro",
            """## Pemeriksaan numerik

Pemeriksaan berikut sengaja berada di dalam notebook: eksekusi berhenti bila suatu invarian dasar gagal. Ini bukan bukti bahwa model benar; ini hanya bukti bahwa implementasi memenuhi kontrak numerik terbatasnya.
""",
        ),
        code_cell(f"{prefix}-assertions", spec["assert_code"]),
        code_cell(f"{prefix}-visualization", spec["plot_code"]),
        markdown_cell(
            f"{prefix}-validation",
            f"""## Validasi, identifikasi, dan keterbatasan

Keterbatasan awal: {spec['limitations']}

Jawab sebelum menafsirkan gambar:

1. Besaran apa yang benar-benar dapat diamati, dan bagaimana galat pengukurannya dimodelkan?
2. Parameter mana yang dapat diidentifikasi dari keluaran tersebut? Tunjukkan dengan profil galat, pemisahan latih/uji, atau eksperimen sensitivitas.
3. Invarian atau pola kualitatif apa yang harus tetap benar ketika ukuran langkah, benih acak, atau resolusi diubah?
4. Temukan satu skenario kegagalan model dan jelaskan data tambahan yang diperlukan untuk membedakannya dari model alternatif.
""",
        ),
        markdown_cell(
            f"{prefix}-reproducibility",
            """## Daftar periksa reproduksibilitas

- [ ] Gunakan CPython dan versi paket tepat seperti `requirements.lock`.
- [ ] Jalankan ulang dari kernel kosong tanpa jaringan.
- [ ] Pertahankan nilai `SEED` (benih acak), lalu ulangi dengan sedikitnya lima benih acak lain dan laporkan variasinya.
- [ ] Catat setiap perubahan parameter, persamaan, toleransi, serta pembagian data.
- [ ] Pastikan semua uji lulus dan jelaskan mengapa tiap uji relevan.
- [ ] Simpan hasil turunan di luar notebook sumber; notebook distribusi harus tetap tanpa keluaran tersimpan.
- [ ] Bedakan hasil simulasi, data sintetis, dan klaim empiris secara eksplisit.
""",
        ),
    ]
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.13.9"},
            "o005": {
                "project_id": project_id,
                "seed": seed,
                "offline": True,
                "source_relation": "independently-authored-pedagogical-starting-point",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def readme_for(spec: dict, project_id: str, notebook_name: str) -> str:
    check_lines = "\n".join(f"- {item}" for item in spec["checks"])
    return f"""# {spec['title']}

ID stabil: `{project_id}`  
Unit: `{UNIT_ID}`  
Notebook: `{notebook_name}`

## Tujuan

{spec['question']}

Paket ini adalah titik awal pedagogis luring yang ditulis secara independen untuk edisi Bahasa Indonesia. Paket menggunakan data sintetis atau data yang dibangkitkan oleh model saja. Ia tidak menyalin kode maupun data dari makalah yang dikutip dalam bab sumber dan tidak mengklaim mereproduksi hasil penelitian tersebut.

## Menjalankan

1. Sediakan CPython 3.13.9 dan paket tepat pada `requirements.lock`.
2. Buka `{notebook_name}` atau eksekusi semua sel kode secara berurutan dalam satu ruang nama kosong.
3. Tidak diperlukan jaringan, kunci API, berkas data tambahan, atau perangkat lunak proprieter.
4. Notebook distribusi sengaja tidak menyimpan keluaran; hasil baru merupakan artefak lokal pengguna.

## Kontrak numerik

{check_lines}

## Batas interpretasi

{spec['limitations']}

Gunakan `checks.json` sebagai kontrak mesin, `rubric.md` untuk penilaian, dan `provenance.json` untuk asal-usul serta batas klaim.
"""


def rubric_for(spec: dict, project_id: str) -> str:
    return f"""# Rubrik — {project_id}

## 1. Formulasi model (0–4)

- 4: pertanyaan, keadaan, parameter, satuan, asumsi, dan mekanisme dituliskan serta saling konsisten.
- 2–3: formulasi dapat dijalankan tetapi satuan atau asumsi penting belum diuji.
- 0–1: persamaan tidak terkait jelas dengan pertanyaan `{spec['title']}`.

## 2. Reproduksibilitas dan numerik (0–4)

- 4: lingkungan terkunci, benih acak dicatat, semua uji lulus, uji resolusi dilakukan, dan notebook sumber tetap tanpa keluaran.
- 2–3: eksekusi berhasil tetapi pemeriksaan sensitivitas atau catatan perubahan belum lengkap.
- 0–1: hasil tidak dapat diulang atau pemeriksaan dasar gagal.

## 3. Validasi dan identifikasi (0–4)

- 4: membedakan kalibrasi dari validasi, menguji keteridentifikasian/sensitivitas, serta membandingkan sekurangnya satu model alternatif.
- 2–3: ada pembandingan kuantitatif tetapi bukti pembeda masih lemah.
- 0–1: kecocokan visual diperlakukan sebagai bukti tunggal.

## 4. Kritik dan komunikasi (0–4)

- 4: menyatakan kegunaan dan kegagalan model, tidak menggeneralisasi data sintetis sebagai fakta empiris, dan menjelaskan visualisasi secara jujur.
- 2–3: keterbatasan disebutkan tetapi belum dihubungkan dengan keputusan.
- 0–1: membuat klaim empiris atau reproduksi yang tidak didukung.

Skor maksimum: **16**. Tidak ada satu hasil numerik yang diwajibkan selain kontrak dasar; perubahan model yang terdokumentasi dan dapat dibela diperbolehkan.
"""


def checks_for(spec: dict, project_id: str, notebook_name: str) -> dict:
    return {
        "schema_version": "o005.project-checks.v1",
        "project_id": project_id,
        "notebook": notebook_name,
        "execution": {
            "mode": "sequential-code-cells-single-clean-namespace",
            "network_required": False,
            "saved_outputs_required": False,
            "fixed_seed": 2026082200 + spec["ordinal"],
        },
        "assertions": [
            {
                "check_id": f"{project_id}-CHK{i:02d}",
                "kind": "in-notebook-numeric-assertion",
                "required": True,
                "expected": "pass",
                "locale": {"id-ID": {"description": description}},
            }
            for i, description in enumerate(spec["checks"], 1)
        ],
        "required_reader_prompts": [
            "observability-and-measurement-error",
            "identifiability-or-sensitivity",
            "resolution-or-seed-robustness",
            "model-failure-and-alternative",
        ],
    }


def provenance_for(spec: dict, project_id: str) -> dict:
    return {
        "schema_version": "o005.project-provenance.v1",
        "project_id": project_id,
        "title_id": f"{project_id}-TITLE",
        "locale": {"id-ID": {"title": spec["title"]}},
        "unit_id": UNIT_ID,
        "source_context": {
            "creator": "Joceline Lega",
            "work": "Introduction to Mathematical Modeling",
            "edition": "v1.01 (March 2026)",
            "unit_relation": "independent-pedagogical-extension-of-project-topic-prompt",
        },
        "implementation": {
            "origin": "independently-authored",
            "purpose": "offline-pedagogical-starting-point",
            "mathematical_core_id": spec["core"],
            "cited_paper_code_included": False,
            "cited_paper_data_included": False,
            "result_reproduction_claim": False,
        },
        "data": {
            "kind": "synthetic-or-model-generated-only",
            "external_files": [],
            "network_access": False,
        },
        "runtime": {
            "python": "CPython 3.13.9",
            "lock_file": "requirements.lock",
        },
        "rights": {
            "license": "CC BY-NC-SA 4.0",
            "attribution_context": "Indonesian derivative reader project packet",
            "non_endorsement": True,
        },
    }


def json_bytes(payload: object) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def text_bytes(text: str) -> bytes:
    return (text.strip() + "\n").encode("utf-8")


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def deterministic_archive(archive_path: Path, members: list[Path]) -> None:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as packet:
        for path in sorted(members, key=lambda item: item.name):
            info = zipfile.ZipInfo(path.name, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.flag_bits = 0
            info.extra = b""
            info.comment = b""
            packet.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build() -> dict:
    rows = []
    for spec in PROJECTS:
        ordinal = spec["ordinal"]
        project_id = f"O005-LEGA-V101-PRJ{ordinal:02d}"
        packet_dir = PROJECT_ROOT / project_id
        notebook_name = f"{project_id}-starter.ipynb"
        files = {
            notebook_name: json_bytes(notebook_for(spec, project_id)),
            "README.md": text_bytes(readme_for(spec, project_id, notebook_name)),
            "checks.json": json_bytes(checks_for(spec, project_id, notebook_name)),
            "provenance.json": json_bytes(provenance_for(spec, project_id)),
            "requirements.lock": LOCK.encode("utf-8"),
            "rubric.md": text_bytes(rubric_for(spec, project_id)),
        }
        member_paths = []
        for name in sorted(files):
            path = packet_dir / name
            write_bytes(path, files[name])
            member_paths.append(path)

        archive_path = ARCHIVE_ROOT / f"{project_id}.zip"
        deterministic_archive(archive_path, member_paths)
        notebook_path = packet_dir / notebook_name
        file_rows = []
        for path in sorted(member_paths, key=lambda item: item.name):
            file_rows.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
        rows.append(
            {
                "project_id": project_id,
                "title_id": f"{project_id}-TITLE",
                "locale": {"id-ID": {"title": spec["title"]}},
                "mathematical_core_id": spec["core"],
                "archive_path": archive_path.relative_to(ROOT).as_posix(),
                "archive_bytes": archive_path.stat().st_size,
                "archive_sha256": sha256_file(archive_path),
                "notebook_path": notebook_path.relative_to(ROOT).as_posix(),
                "notebook_bytes": notebook_path.stat().st_size,
                "notebook_sha256": sha256_file(notebook_path),
                "files": file_rows,
            }
        )

    catalog = {
        "schema_version": "o005.project-catalog.v1",
        "unit_id": UNIT_ID,
        "project_count": len(rows),
        "project_order": [row["project_id"] for row in rows],
        "projects": rows,
        "closure": {
            "offline": True,
            "data_policy": "synthetic-or-model-generated-only",
            "cited_paper_code_or_data_included": False,
            "result_reproduction_claim": False,
            "requirements_lock_sha256": sha256_bytes(LOCK.encode("utf-8")),
            "zip_member_order": "lexicographic-filename",
            "zip_timestamp": "1980-01-01T00:00:00",
            "zip_mode": "100644",
        },
    }
    write_bytes(CATALOG_PATH, json_bytes(catalog))
    return catalog


def main() -> None:
    catalog = build()
    total_packet_files = sum(len(row["files"]) for row in catalog["projects"])
    total_packet_bytes = sum(item["bytes"] for row in catalog["projects"] for item in row["files"])
    total_archive_bytes = sum(row["archive_bytes"] for row in catalog["projects"])
    print(
        json.dumps(
            {
                "catalog": CATALOG_PATH.relative_to(ROOT).as_posix(),
                "projects": len(catalog["projects"]),
                "packet_files": total_packet_files,
                "packet_bytes": total_packet_bytes,
                "archives": len(catalog["projects"]),
                "archive_bytes": total_archive_bytes,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
