# Penyelarasan Visual dalam Kerumunan

ID stabil: `O005-LEGA-V101-PRJ06`  
Unit: `O005-LEGA-V101-CH14`  
Notebook: `O005-LEGA-V101-PRJ06-starter.ipynb`

## Tujuan

Seberapa cepat aturan penyelarasan visual lokal menghasilkan gerak kolektif dari arah awal acak?

Paket ini adalah titik awal pedagogis luring yang ditulis secara independen untuk edisi Bahasa Indonesia. Paket menggunakan data sintetis atau data yang dibangkitkan oleh model saja. Ia tidak menyalin kode maupun data dari makalah yang dikutip dalam bab sumber dan tidak mengklaim mereproduksi hasil penelitian tersebut.

## Menjalankan

1. Sediakan CPython 3.13.9 dan paket tepat pada `requirements.lock`.
2. Buka `O005-LEGA-V101-PRJ06-starter.ipynb` atau eksekusi semua sel kode secara berurutan dalam satu ruang nama kosong.
3. Tidak diperlukan jaringan, kunci API, berkas data tambahan, atau perangkat lunak proprieter.
4. Notebook distribusi sengaja tidak menyimpan keluaran; hasil baru merupakan artefak lokal pengguna.

## Kontrak numerik

- Semua posisi tetap di domain periodik.
- Polarisasi akhir melampaui polarisasi awal dengan selisih nyata.
- Riwayat polarisasi selalu berada antara nol dan satu.

## Batas interpretasi

Tetangga ditentukan hanya oleh jarak periodik; tidak ada rintangan, bidang pandang berarah, oklusi, tabrakan, perbedaan kecepatan, atau kepanikan.

Gunakan `checks.json` sebagai kontrak mesin, `rubric.md` untuk penilaian, dan `provenance.json` untuk asal-usul serta batas klaim.
