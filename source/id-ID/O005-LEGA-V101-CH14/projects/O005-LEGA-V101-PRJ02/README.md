# Sinyal Dini Zoonosis dengan Model SEIR

ID stabil: `O005-LEGA-V101-PRJ02`  
Unit: `O005-LEGA-V101-CH14`  
Notebook: `O005-LEGA-V101-PRJ02-starter.ipynb`

## Tujuan

Informasi apa tentang laju pertumbuhan awal yang dapat dipulihkan dari pengamatan wabah zoonotik yang jarang dan berisik?

Paket ini adalah titik awal pedagogis luring yang ditulis secara independen untuk edisi Bahasa Indonesia. Paket menggunakan data sintetis atau data yang dibangkitkan oleh model saja. Ia tidak menyalin kode maupun data dari makalah yang dikutip dalam bab sumber dan tidak mengklaim mereproduksi hasil penelitian tersebut.

## Menjalankan

1. Sediakan CPython 3.13.9 dan paket tepat pada `requirements.lock`.
2. Buka `O005-LEGA-V101-PRJ02-starter.ipynb` atau eksekusi semua sel kode secara berurutan dalam satu ruang nama kosong.
3. Tidak diperlukan jaringan, kunci API, berkas data tambahan, atau perangkat lunak proprieter.
4. Notebook distribusi sengaja tidak menyimpan keluaran; hasil baru merupakan artefak lokal pengguna.

## Kontrak numerik

- Jumlah fraksi SEIR terjaga hingga toleransi numerik.
- Semua kompartemen tetap nonnegatif.
- Puncak infeksi terjadi setelah kondisi awal untuk R0 lebih besar dari satu.

## Batas interpretasi

Tidak ada struktur umur, pelaporan tertunda, limpahan berulang dari hewan, perubahan perilaku, atau variasi spasial.

Gunakan `checks.json` sebagai kontrak mesin, `rubric.md` untuk penilaian, dan `provenance.json` untuk asal-usul serta batas klaim.
