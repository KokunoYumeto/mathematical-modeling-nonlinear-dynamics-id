# Pemodelan Matematika dan Dinamika Nonlinear — Bahasa Indonesia

Repositori kerja ini memuat edisi Bahasa Indonesia independen dari Joceline
Lega, *Introduction to Mathematical Modeling*, University of Arizona
Pressbooks v1.01 (Maret 2026). Sumber dan terjemahan berada di bawah lisensi
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Edisi ini tidak disokong atau disahkan oleh penulis maupun University of
Arizona.

Status saat ini: **Bab 1 dari 14 telah diterjemahkan, dibangun, dan lolos QA.**
Pekerjaan berlanjut secara berurutan; repositori ini belum merupakan edisi
lengkap atau terbitan final.

## Baca unit yang selesai

- Sumber terjemahan: [`source/id-ID/O005-LEGA-V101-CH01/content.html`](source/id-ID/O005-LEGA-V101-CH01/content.html)
- Pembaca HTML hasil build: [`build/reader/O005-LEGA-V101-CH01/index.html`](build/reader/O005-LEGA-V101-CH01/index.html)
- Notebook Python Soal 7: [`source/id-ID/O005-LEGA-V101-CH01/notebooks/problem-07-open-curve-fitting.ipynb`](source/id-ID/O005-LEGA-V101-CH01/notebooks/problem-07-open-curve-fitting.ipynb)
- Petunjuk, pemeriksaan, dan pembahasan: [`backend/mastery/O005-LEGA-V101-CH01.mastery.json`](backend/mastery/O005-LEGA-V101-CH01.mastery.json)

## Backend modular

Setiap unit menggunakan ID stabil yang netral terhadap bahasa. Bab 1 memiliki
125 segmen Inggris–Indonesia yang berpasangan, tujuh ID soal tetap, catatan
unit berhash, serta jalur eksplisit menuju aset, notebook, dan dukungan belajar.
Lapisan ini dimaksudkan untuk memungkinkan pemindahan unit yang sama ke bahasa
lain tanpa menjadikan Bahasa Indonesia sebagai kunci struktur.

## Bangun dan periksa

Build memerlukan Python, Beautiful Soup 4, dan Pandoc 3.9.0.2. Notebook memakai
versi NumPy/SciPy/Matplotlib yang tercantum dalam `requirements.lock`.

```powershell
python scripts/build_ch01_reader.py
python scripts/qa_ch01.py --execute-notebook --deterministic-build
```

QA memeriksa kesetaraan struktur sumber–target, rumus dan tautan yang
dilindungi, penutupan aset lokal, ID dan fragmen, backend berhash, eksekusi
notebook, privasi, serta hasil build berulang yang identik.

## Atribusi dan perubahan

Sumber resmi tersedia di
<https://opentextbooks.library.arizona.edu/mathematicalmodeling/>. Perubahan
yang telah dibuat meliputi penerjemahan ke Bahasa Indonesia, gambar ulang
aksesibel untuk siklus pemodelan, pengindeksan modular, dukungan belajar baru,
dan penggantian prompt MATLAB pada Soal 7 dengan notebook Python terbuka yang
ditulis secara independen. Rincian sumber, lisensi, keputusan, dan hash berada
di `00_control/`.
