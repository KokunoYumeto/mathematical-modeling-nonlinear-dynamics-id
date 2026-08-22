# Dinamika Glukosa–Insulin

ID stabil: `O005-LEGA-V101-PRJ05`  
Unit: `O005-LEGA-V101-CH14`  
Notebook: `O005-LEGA-V101-PRJ05-starter.ipynb`

## Tujuan

Parameter mana yang mengatur tinggi puncak glukosa dan waktu pulih setelah masukan makanan sintetis?

Paket ini adalah titik awal pedagogis luring yang ditulis secara independen untuk edisi Bahasa Indonesia. Paket menggunakan data sintetis atau data yang dibangkitkan oleh model saja. Ia tidak menyalin kode maupun data dari makalah yang dikutip dalam bab sumber dan tidak mengklaim mereproduksi hasil penelitian tersebut.

## Menjalankan

1. Sediakan CPython 3.13.9 dan paket tepat pada `requirements.lock`.
2. Buka `O005-LEGA-V101-PRJ05-starter.ipynb` atau eksekusi semua sel kode secara berurutan dalam satu ruang nama kosong.
3. Tidak diperlukan jaringan, kunci API, berkas data tambahan, atau perangkat lunak proprieter.
4. Notebook distribusi sengaja tidak menyimpan keluaran; hasil baru merupakan artefak lokal pengguna.

## Kontrak numerik

- Penyelesaian ODE berhasil dan semua keadaan hingga.
- Glukosa naik di atas basal setelah pulsa makanan.
- Glukosa mendekati basal kembali pada akhir simulasi.

## Batas interpretasi

Model bukan alat diagnosis dan mengabaikan variasi organ, hormon lain, ketidakpastian makanan, serta perbedaan pasien.

Gunakan `checks.json` sebagai kontrak mesin, `rubric.md` untuk penilaian, dan `provenance.json` untuk asal-usul serta batas klaim.
