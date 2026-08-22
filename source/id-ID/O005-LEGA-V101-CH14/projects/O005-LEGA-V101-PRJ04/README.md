# Vaksinasi dan Beban Layanan Kesehatan

ID stabil: `O005-LEGA-V101-PRJ04`  
Unit: `O005-LEGA-V101-CH14`  
Notebook: `O005-LEGA-V101-PRJ04-starter.ipynb`

## Tujuan

Bagaimana cakupan vaksin mengubah puncak kebutuhan perawatan dalam model transparan yang memisahkan perlindungan terhadap infeksi dan penyakit berat?

Paket ini adalah titik awal pedagogis luring yang ditulis secara independen untuk edisi Bahasa Indonesia. Paket menggunakan data sintetis atau data yang dibangkitkan oleh model saja. Ia tidak menyalin kode maupun data dari makalah yang dikutip dalam bab sumber dan tidak mengklaim mereproduksi hasil penelitian tersebut.

## Menjalankan

1. Sediakan CPython 3.13.9 dan paket tepat pada `requirements.lock`.
2. Buka `O005-LEGA-V101-PRJ04-starter.ipynb` atau eksekusi semua sel kode secara berurutan dalam satu ruang nama kosong.
3. Tidak diperlukan jaringan, kunci API, berkas data tambahan, atau perangkat lunak proprieter.
4. Notebook distribusi sengaja tidak menyimpan keluaran; hasil baru merupakan artefak lokal pengguna.

## Kontrak numerik

- Massa SIR dan nonnegativitas terjaga.
- Puncak beban layanan turun monoton saat cakupan naik.
- Semua skenario memakai parameter penyakit yang sama.

## Batas interpretasi

Tidak ada peluruhan kekebalan, kelompok umur, kapasitas yang memengaruhi mortalitas, dosis berulang, atau seleksi varian.

Gunakan `checks.json` sebagai kontrak mesin, `rubric.md` untuk penilaian, dan `provenance.json` untuk asal-usul serta batas klaim.
