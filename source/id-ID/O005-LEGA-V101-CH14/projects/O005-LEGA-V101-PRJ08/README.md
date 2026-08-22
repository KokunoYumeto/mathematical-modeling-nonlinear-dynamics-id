# Predator–Mangsa dengan Imigrasi

ID stabil: `O005-LEGA-V101-PRJ08`  
Unit: `O005-LEGA-V101-CH14`  
Notebook: `O005-LEGA-V101-PRJ08-starter.ipynb`

## Tujuan

Bagaimana aliran mangsa dari luar sistem menggeser kesetimbangan dan lintasan predator–mangsa?

Paket ini adalah titik awal pedagogis luring yang ditulis secara independen untuk edisi Bahasa Indonesia. Paket menggunakan data sintetis atau data yang dibangkitkan oleh model saja. Ia tidak menyalin kode maupun data dari makalah yang dikutip dalam bab sumber dan tidak mengklaim mereproduksi hasil penelitian tersebut.

## Menjalankan

1. Sediakan CPython 3.13.9 dan paket tepat pada `requirements.lock`.
2. Buka `O005-LEGA-V101-PRJ08-starter.ipynb` atau eksekusi semua sel kode secara berurutan dalam satu ruang nama kosong.
3. Tidak diperlukan jaringan, kunci API, berkas data tambahan, atau perangkat lunak proprieter.
4. Notebook distribusi sengaja tidak menyimpan keluaran; hasil baru merupakan artefak lokal pengguna.

## Kontrak numerik

- Lintasan numerik tetap positif dan hingga.
- Kesetimbangan predator analitik naik ketika imigrasi positif.
- Kondisi kesetimbangan memenuhi ruas kanan ODE.

## Batas interpretasi

Tidak ada daya dukung, struktur umur, musim, stokastisitas demografis, atau umpan balik pada imigrasi.

Gunakan `checks.json` sebagai kontrak mesin, `rubric.md` untuk penilaian, dan `provenance.json` untuk asal-usul serta batas klaim.
