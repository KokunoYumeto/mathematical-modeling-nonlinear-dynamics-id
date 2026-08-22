# Dengue: Model Sederhana, Vektor–Inang, dan Keteridentifikasian

ID stabil: `O005-LEGA-V101-PRJ07`  
Unit: `O005-LEGA-V101-CH14`  
Notebook: `O005-LEGA-V101-PRJ07-starter.ipynb`

## Tujuan

Dapatkah kurva prevalensi manusia saja membedakan laju penularan manusia-ke-vektor dari vektor-ke-manusia?

Paket ini adalah titik awal pedagogis luring yang ditulis secara independen untuk edisi Bahasa Indonesia. Paket menggunakan data sintetis atau data yang dibangkitkan oleh model saja. Ia tidak menyalin kode maupun data dari makalah yang dikutip dalam bab sumber dan tidak mengklaim mereproduksi hasil penelitian tersebut.

## Menjalankan

1. Sediakan CPython 3.13.9 dan paket tepat pada `requirements.lock`.
2. Buka `O005-LEGA-V101-PRJ07-starter.ipynb` atau eksekusi semua sel kode secara berurutan dalam satu ruang nama kosong.
3. Tidak diperlukan jaringan, kunci API, berkas data tambahan, atau perangkat lunak proprieter.
4. Notebook distribusi sengaja tidak menyimpan keluaran; hasil baru merupakan artefak lokal pengguna.

## Kontrak numerik

- Massa manusia dan vektor terjaga pada simulasi sumber.
- Pencarian kisi menemukan beberapa pasangan laju yang berbeda dengan galat rendah.
- Model sederhana dan vektor–inang menghasilkan prediksi hingga dan nonnegatif.

## Batas interpretasi

Model mengabaikan musim, serotipe, imunitas silang, umur nyamuk, pelaporan kasus, dan struktur ruang; kisi parameter hanya ilustrasi keteridentifikasian praktis.

Gunakan `checks.json` sebagai kontrak mesin, `rubric.md` untuk penilaian, dan `provenance.json` untuk asal-usul serta batas klaim.
