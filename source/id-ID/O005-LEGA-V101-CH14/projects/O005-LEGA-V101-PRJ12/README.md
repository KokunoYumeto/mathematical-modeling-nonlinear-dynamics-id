# Kolam Lelehan Arktik dengan Model Ising

ID stabil: `O005-LEGA-V101-PRJ12`  
Unit: `O005-LEGA-V101-CH14`  
Notebook: `O005-LEGA-V101-PRJ12-starter.ipynb`

## Tujuan

Bagaimana kopling tetangga, pemaksaan eksternal, dan jadwal pendinginan mengubah pola biner es–kolam dalam model Ising pedagogis?

Paket ini adalah titik awal pedagogis luring yang ditulis secara independen untuk edisi Bahasa Indonesia. Paket menggunakan data sintetis atau data yang dibangkitkan oleh model saja. Ia tidak menyalin kode maupun data dari makalah yang dikutip dalam bab sumber dan tidak mengklaim mereproduksi hasil penelitian tersebut.

## Menjalankan

1. Sediakan CPython 3.13.9 dan paket tepat pada `requirements.lock`.
2. Buka `O005-LEGA-V101-PRJ12-starter.ipynb` atau eksekusi semua sel kode secara berurutan dalam satu ruang nama kosong.
3. Tidak diperlukan jaringan, kunci API, berkas data tambahan, atau perangkat lunak proprieter.
4. Notebook distribusi sengaja tidak menyimpan keluaran; hasil baru merupakan artefak lokal pengguna.

## Kontrak numerik

- Spin selalu bernilai −1 atau +1.
- Relaksasi akhir tidak menaikkan energi dari keadaan awal.
- Fraksi kolam dan riwayat energi hingga serta berada pada rentang sah.

## Batas interpretasi

Spin bukan hidrologi fisik; tidak ada konservasi air, ketebalan es, geometri nyata, radiasi, aliran, atau kalibrasi observasional.

Gunakan `checks.json` sebagai kontrak mesin, `rubric.md` untuk penilaian, dan `provenance.json` untuk asal-usul serta batas klaim.
