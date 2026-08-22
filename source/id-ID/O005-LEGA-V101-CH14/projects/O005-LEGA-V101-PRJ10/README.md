# Kopling Aroma dan Agen pada Lebah Madu

ID stabil: `O005-LEGA-V101-PRJ10`  
Unit: `O005-LEGA-V101-CH14`  
Notebook: `O005-LEGA-V101-PRJ10-starter.ipynb`

## Tujuan

Apakah aturan gerak yang menggabungkan gradien aroma dan derau cukup untuk menghasilkan akumulasi agen di dekat sumber?

Paket ini adalah titik awal pedagogis luring yang ditulis secara independen untuk edisi Bahasa Indonesia. Paket menggunakan data sintetis atau data yang dibangkitkan oleh model saja. Ia tidak menyalin kode maupun data dari makalah yang dikutip dalam bab sumber dan tidak mengklaim mereproduksi hasil penelitian tersebut.

## Menjalankan

1. Sediakan CPython 3.13.9 dan paket tepat pada `requirements.lock`.
2. Buka `O005-LEGA-V101-PRJ10-starter.ipynb` atau eksekusi semua sel kode secara berurutan dalam satu ruang nama kosong.
3. Tidak diperlukan jaringan, kunci API, berkas data tambahan, atau perangkat lunak proprieter.
4. Notebook distribusi sengaja tidak menyimpan keluaran; hasil baru merupakan artefak lokal pengguna.

## Kontrak numerik

- Semua agen tetap di domain.
- Jarak median ke sumber turun selama simulasi.
- Medan aroma nonnegatif dan berpuncak dekat sumber.

## Batas interpretasi

Tidak ada dinamika turbulensi aroma, komunikasi tarian, penghindaran tumbukan, memori, atau heterogenitas sensorik.

Gunakan `checks.json` sebagai kontrak mesin, `rubric.md` untuk penilaian, dan `provenance.json` untuk asal-usul serta batas klaim.
