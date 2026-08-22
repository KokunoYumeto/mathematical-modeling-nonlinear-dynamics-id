# Waktu Intervensi Nonfarmasi

ID stabil: `O005-LEGA-V101-PRJ03`  
Unit: `O005-LEGA-V101-CH14`  
Notebook: `O005-LEGA-V101-PRJ03-starter.ipynb`

## Tujuan

Seberapa besar perubahan puncak epidemi ketika intervensi nonfarmasi yang sama dimulai pada waktu berbeda?

Paket ini adalah titik awal pedagogis luring yang ditulis secara independen untuk edisi Bahasa Indonesia. Paket menggunakan data sintetis atau data yang dibangkitkan oleh model saja. Ia tidak menyalin kode maupun data dari makalah yang dikutip dalam bab sumber dan tidak mengklaim mereproduksi hasil penelitian tersebut.

## Menjalankan

1. Sediakan CPython 3.13.9 dan paket tepat pada `requirements.lock`.
2. Buka `O005-LEGA-V101-PRJ03-starter.ipynb` atau eksekusi semua sel kode secara berurutan dalam satu ruang nama kosong.
3. Tidak diperlukan jaringan, kunci API, berkas data tambahan, atau perangkat lunak proprieter.
4. Notebook distribusi sengaja tidak menyimpan keluaran; hasil baru merupakan artefak lokal pengguna.

## Kontrak numerik

- Massa SIR terjaga pada semua skenario.
- Intervensi dini memberi puncak infeksi lebih rendah daripada intervensi lambat.
- Intervensi lambat memberi puncak lebih rendah daripada tanpa intervensi.

## Batas interpretasi

Intervensi tidak memiliki biaya, penundaan, kelelahan, heterogenitas, atau respons perilaku endogen.

Gunakan `checks.json` sebagai kontrak mesin, `rubric.md` untuk penilaian, dan `provenance.json` untuk asal-usul serta batas klaim.
