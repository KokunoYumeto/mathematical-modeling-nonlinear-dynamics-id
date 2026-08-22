# Pemodelan Matematika dan Dinamika Nonlinear — Bahasa Indonesia

Repositori kerja ini memuat edisi Bahasa Indonesia independen dari Joceline
Lega, *Introduction to Mathematical Modeling*, University of Arizona
Pressbooks v1.01 (Maret 2026). Sumber dan terjemahan berada di bawah lisensi
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Edisi ini tidak disokong atau disahkan oleh penulis maupun University of
Arizona.

Status saat ini: **Bab 1–7 dari 14 serta pengantar Bagian 2–4 telah diterjemahkan,
dibangun, dan lolos QA.**
Pekerjaan berlanjut secara berurutan; repositori ini belum merupakan edisi
lengkap atau terbitan final.

## Baca unit yang selesai

- Bab 1 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH01/content.html); [pembaca HTML](build/reader/O005-LEGA-V101-CH01/index.html); [notebook pencocokan kurva](source/id-ID/O005-LEGA-V101-CH01/notebooks/problem-07-open-curve-fitting.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH01.mastery.json).
- Bab 2 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH02/content.html); [pembaca HTML](build/reader/O005-LEGA-V101-CH02/index.html); [notebook simulasi gelombang](source/id-ID/O005-LEGA-V101-CH02/notebooks/chapter-02-open-wave-simulation.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH02.mastery.json).
- Pengantar Bagian 2 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-PT02/content.html); [pembaca HTML](build/reader/O005-LEGA-V101-PT02/index.html).
- Bab 3 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH03/content.html); [pembaca HTML](build/reader/O005-LEGA-V101-CH03/index.html); [notebook bidang fase](source/id-ID/O005-LEGA-V101-CH03/notebooks/chapter-03-open-phase-plane.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH03.mastery.json).
- Bab 4 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH04/content.html); [pembaca HTML](build/reader/O005-LEGA-V101-CH04/index.html); [notebook pemantulan batu](source/id-ID/O005-LEGA-V101-CH04/notebooks/chapter-04-open-stone-skipping.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH04.mastery.json).
- Pengantar Bagian 3 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-PT03/content.html); [pembaca HTML](build/reader/O005-LEGA-V101-PT03/index.html).
- Bab 5 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH05/content.html); [pembaca HTML](build/reader/O005-LEGA-V101-CH05/index.html); [notebook dinamika populasi satu spesies](source/id-ID/O005-LEGA-V101-CH05/notebooks/chapter-05-open-single-species-models.ipynb); [data Sensus resmi](source/id-ID/O005-LEGA-V101-CH05/data/popclockest.txt); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH05.mastery.json).
- Bab 6 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH06/content.html); [pembaca HTML](build/reader/O005-LEGA-V101-CH06/index.html); [notebook model dua spesies](source/id-ID/O005-LEGA-V101-CH06/notebooks/chapter-06-open-two-species-models.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH06.mastery.json).
- Bab 7 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH07/content.html); [pembaca HTML](build/reader/O005-LEGA-V101-CH07/index.html); [notebook epidemiologi terbuka](source/id-ID/O005-LEGA-V101-CH07/notebooks/chapter-07-open-epidemiology.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH07.mastery.json).
- Pengantar Bagian 4 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-PT04/content.html); [pembaca HTML](build/reader/O005-LEGA-V101-PT04/index.html).

## Backend modular

Setiap unit menggunakan ID stabil yang netral terhadap bahasa. Tujuh bab dan
tiga pengantar bagian yang selesai memiliki 1.748 segmen Inggris–Indonesia yang
berpasangan, 69 ID soal tetap, tujuh notebook terbuka, catatan unit berhash,
serta jalur eksplisit menuju aset, notebook, dan
dukungan belajar. Lapisan ini dimaksudkan untuk memungkinkan pemindahan unit
yang sama ke bahasa lain tanpa menjadikan Bahasa Indonesia sebagai kunci
struktur.

## Bangun dan periksa

Build memerlukan Python, Beautiful Soup 4, dan Pandoc 3.9.0.2. Notebook memakai
versi NumPy/SciPy/Matplotlib yang tercantum dalam `requirements.lock` masing-masing.

```powershell
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH01
python scripts/qa_unit.py --unit O005-LEGA-V101-CH01 --execute-notebook --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH02
python scripts/qa_unit.py --unit O005-LEGA-V101-CH02 --execute-notebook --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-PT02
python scripts/qa_unit.py --unit O005-LEGA-V101-PT02 --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH03
python scripts/qa_unit.py --unit O005-LEGA-V101-CH03 --execute-notebook --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH04
python scripts/qa_unit.py --unit O005-LEGA-V101-CH04 --execute-notebook --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-PT03
python scripts/qa_unit.py --unit O005-LEGA-V101-PT03 --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH05
python scripts/qa_unit.py --unit O005-LEGA-V101-CH05 --execute-notebook --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH06
python scripts/qa_unit.py --unit O005-LEGA-V101-CH06 --execute-notebook --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH07
python scripts/qa_unit.py --unit O005-LEGA-V101-CH07 --execute-notebook --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-PT04
python scripts/qa_unit.py --unit O005-LEGA-V101-PT04 --deterministic-build
```

QA memeriksa kesetaraan struktur sumber–target, rumus dan tautan yang
dilindungi, penutupan aset lokal, ID dan fragmen, backend berhash, eksekusi
notebook, privasi, serta hasil build berulang yang identik.

## Atribusi dan perubahan

Sumber resmi tersedia di
<https://opentextbooks.library.arizona.edu/mathematicalmodeling/>. Perubahan
yang telah dibuat meliputi penerjemahan ke Bahasa Indonesia, gambar ulang
aksesibel untuk siklus pemodelan, pengindeksan modular, dukungan belajar baru,
penggantian prompt MATLAB pada Soal 7 Bab 1, dan rekonstruksi terbuka simulasi
gelombang Bab 2, notebook bidang fase terbuka Bab 3, serta lokalisasi berjejak
untuk empat label penjelas pada Gambar 3.4. Bab 4 menambahkan gambar ulang SVG
aksesibel untuk Gambar 4.1, koreksi matematika yang tercatat, dan notebook
pemantulan batu terbuka. Bab 5 mempertahankan tujuh gambar sumber, menambahkan
tiga adaptasi label berbahasa Indonesia, paket data Sensus Amerika Serikat
yang terverifikasi, koreksi matematika tercatat, serta notebook dinamika
populasi terbuka. Semua notebook ditulis secara independen. Rincian
sumber, lisensi, keputusan, dan hash berada di `00_control/`. Bab 6
mempertahankan empat gambar sumber, memperbaiki kekeliruan matematika dan
aksesibilitas yang tercatat, mengganti dua rujukan aplikasi bidang fase
proprietari dengan satu notebook Python terbuka, dan menambahkan enam paket
petunjuk, pemeriksaan jawaban, serta solusi atau rubrik. Bab 7 mempertahankan
tiga potret fase sumber, memberikan latar putih agar notasi hitam pada raster
transparan tetap terbaca, mencatat koreksi model dan aksesibilitas secara
eksplisit, serta menambahkan notebook epidemiologi terbuka dan lima paket
dukungan belajar lengkap. Pengantar Bagian 4 mempertahankan empat paragraf,
sebelas rumus, dan enam penekanan sumber tanpa menambahkan komponen yang tidak
berlaku.
