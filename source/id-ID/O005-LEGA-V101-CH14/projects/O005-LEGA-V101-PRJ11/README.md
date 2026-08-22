# Habitat dan Migrasi Paus

ID stabil: `O005-LEGA-V101-PRJ11`  
Unit: `O005-LEGA-V101-CH14`  
Notebook: `O005-LEGA-V101-PRJ11-starter.ipynb`

## Tujuan

Bagaimana medan kesesuaian habitat sintetis dan kecenderungan migrasi menghasilkan lintasan populasi yang dapat divalidasi?

Paket ini adalah titik awal pedagogis luring yang ditulis secara independen untuk edisi Bahasa Indonesia. Paket menggunakan data sintetis atau data yang dibangkitkan oleh model saja. Ia tidak menyalin kode maupun data dari makalah yang dikutip dalam bab sumber dan tidak mengklaim mereproduksi hasil penelitian tersebut.

## Menjalankan

1. Sediakan CPython 3.13.9 dan paket tepat pada `requirements.lock`.
2. Buka `O005-LEGA-V101-PRJ11-starter.ipynb` atau eksekusi semua sel kode secara berurutan dalam satu ruang nama kosong.
3. Tidak diperlukan jaringan, kunci API, berkas data tambahan, atau perangkat lunak proprieter.
4. Notebook distribusi sengaja tidak menyimpan keluaran; hasil baru merupakan artefak lokal pengguna.

## Kontrak numerik

- Lintasan tetap dalam batas domain sintetis.
- Jarak median ke optimum musim akhir berkurang.
- Medan habitat dibatasi antara nol dan satu.

## Batas interpretasi

Peta bukan geografi nyata; tidak ada arus, batimetri, kapal, suara, struktur sosial, mortalitas, atau data telemetri sungguhan.

Gunakan `checks.json` sebagai kontrak mesin, `rubric.md` untuk penilaian, dan `provenance.json` untuk asal-usul serta batas klaim.
