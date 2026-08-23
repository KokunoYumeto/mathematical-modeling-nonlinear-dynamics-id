# Pengantar Pemodelan Matematika — Edisi Bahasa Indonesia

Repositori kerja ini memuat edisi Bahasa Indonesia independen dari Joceline
Lega, *Introduction to Mathematical Modeling*, University of Arizona
Pressbooks v1.01 (Maret 2026). Sumber dan terjemahan berada di bawah lisensi
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Edisi ini tidak disokong atau disahkan oleh penulis maupun University of
Arizona.

Provenance model untuk penerjemahan, adaptasi teknis, dan QA: OpenAI Codex gpt-5.6-sol, Ultra.
Pernyataan ini tidak menggantikan kredit kepada Joceline
Lega, University of Arizona, atau kontributor manusia yang tercatat.

Status saat ini: **edisi pembaca lengkap telah diproduksi dan lolos QA.**
Cakupannya adalah seluruh 22 unit sumber—Prakata, pengantar Bagian 1–5, Bab
1–14, Pernyataan Aksesibilitas, dan Riwayat Versi—serta empat modul jembatan
orisinal. Seluruh 113 soal sumber dan 28 soal jembatan memiliki petunjuk,
pemeriksaan, dan pembahasan atau rubrik; 26 notebook Python terbuka melengkapi
pembaca.

- [Baca edisi HTML](https://kokunoyumeto.github.io/mathematical-modeling-nonlinear-dynamics-id/)
- [Unduh rilis lengkap v1.01-r5](https://github.com/KokunoYumeto/mathematical-modeling-nonlinear-dynamics-id/releases/tag/v1.01-id-complete-reader-20260823-r5)

Versi pembaca lengkap ini dipertahankan dalam garis versi konsep Zenodo
[10.5281/zenodo.22059939](https://doi.org/10.5281/zenodo.22059939); tautan DOI
konsep selalu mengarah ke versi publik terbaru. Arsip setiap versi menyimpan
identitas, checksum, dan riwayat koreksinya sendiri.
Figshare sebelumnya memiliki catatan metadata CC0 tanpa salinan berkas—lisensi
karya yang ditautkan tetap CC BY-NC-SA 4.0—di artikel
[10.6084/m9.figshare.33314769.v2](https://doi.org/10.6084/m9.figshare.33314769.v2).
Pada pemeriksaan 2026-08-23, artikel tersebut melaporkan telah dihapus dan
akun API yang diperlukan untuk menerbitkan pembaruan berada dalam status
nonaktif; tidak ada salinan berkas yang diunggah ke Figshare. Bukti dan prosedur
kelanjutan dicatat di `00_control/FIGSHARE_PUBLICATION_RECEIPT_COMPLETE_20260823.json`;
collection yang diperiksa adalah [Indonesian Mathematics — Reader PDFs](https://doi.org/10.6084/m9.figshare.c.8668413),
yang saat ini tidak memiliki isi publik.

## Baca unit yang selesai

Direktori `build/reader/` dan arsip proyek adalah keluaran yang dapat dibuat
ulang, sehingga paket sumber ringkas tidak menggandakannya. Tautan berikut
menunjuk pada sumber kanonis, notebook, backend dukungan, dan katalog proyek.

- Bab 1 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH01/content.html); [notebook pencocokan kurva](source/id-ID/O005-LEGA-V101-CH01/notebooks/problem-07-open-curve-fitting.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH01.mastery.json).
- Prakata — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-FM01/content.html).
- Pengantar Bagian 1 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-PT01/content.html).
- Bab 2 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH02/content.html); [notebook simulasi gelombang](source/id-ID/O005-LEGA-V101-CH02/notebooks/chapter-02-open-wave-simulation.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH02.mastery.json).
- Pengantar Bagian 2 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-PT02/content.html).
- Bab 3 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH03/content.html); [notebook bidang fase](source/id-ID/O005-LEGA-V101-CH03/notebooks/chapter-03-open-phase-plane.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH03.mastery.json).
- Bab 4 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH04/content.html); [notebook pemantulan batu](source/id-ID/O005-LEGA-V101-CH04/notebooks/chapter-04-open-stone-skipping.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH04.mastery.json).
- Pengantar Bagian 3 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-PT03/content.html).
- Bab 5 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH05/content.html); [notebook dinamika populasi satu spesies](source/id-ID/O005-LEGA-V101-CH05/notebooks/chapter-05-open-single-species-models.ipynb); [data Sensus resmi](source/id-ID/O005-LEGA-V101-CH05/data/popclockest.txt); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH05.mastery.json).
- Bab 6 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH06/content.html); [notebook model dua spesies](source/id-ID/O005-LEGA-V101-CH06/notebooks/chapter-06-open-two-species-models.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH06.mastery.json).
- Bab 7 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH07/content.html); [notebook epidemiologi terbuka](source/id-ID/O005-LEGA-V101-CH07/notebooks/chapter-07-open-epidemiology.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH07.mastery.json).
- Pengantar Bagian 4 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-PT04/content.html).
- Bab 8 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH08/content.html); [notebook reaksi kimia terbuka](source/id-ID/O005-LEGA-V101-CH08/notebooks/chapter-08-open-chemical-reactions.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH08.mastery.json).
- Bab 9 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH09/content.html); [notebook difusi terbuka](source/id-ID/O005-LEGA-V101-CH09/notebooks/chapter-09-open-diffusion.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH09.mastery.json).
- Bab 10 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH10/content.html); [notebook pembentukan pola terbuka](source/id-ID/O005-LEGA-V101-CH10/notebooks/chapter-10-open-pattern-formation.ipynb); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH10.mastery.json).
- Pengantar Bagian 5 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-PT05/content.html).
- Bab 11 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH11/content.html); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH11.mastery.json).
- Bab 12 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH12/content.html).
- Bab 13 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH13/content.html); [dukungan belajar](backend/mastery/O005-LEGA-V101-CH13.mastery.json).
- Bab 14 — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-CH14/content.html); [katalog 12 proyek](backend/projects/O005-LEGA-V101-CH14.projects.json); sumber dua belas paket berada di [`projects/`](source/id-ID/O005-LEGA-V101-CH14/projects/).
- Pernyataan Aksesibilitas — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-BM01/content.html).
- Riwayat Versi — sumber: [`content.html`](source/id-ID/O005-LEGA-V101-BM02/content.html).
- Modul Jembatan C1 — [alur kerja Python/Jupyter yang reprodusibel](source/id-ID/O005-BRIDGE-C1/content.html); [notebook](source/id-ID/O005-BRIDGE-C1/notebooks/bridge-c1-reproducible-workflow.ipynb); [dukungan belajar](backend/mastery/O005-BRIDGE-C1.mastery.json).
- Modul Jembatan C2 — [bifurkasi lokal](source/id-ID/O005-BRIDGE-C2/content.html); [notebook](source/id-ID/O005-BRIDGE-C2/notebooks/bridge-c2-local-bifurcations.ipynb); [dukungan belajar](backend/mastery/O005-BRIDGE-C2.mastery.json).
- Modul Jembatan C3 — [penggandaan periode, kekacauan, dan peta balik](source/id-ID/O005-BRIDGE-C3/content.html); [notebook](source/id-ID/O005-BRIDGE-C3/notebooks/bridge-c3-chaos-and-return-maps.ipynb); [dukungan belajar](backend/mastery/O005-BRIDGE-C3.mastery.json).
- Modul Jembatan C4 — [kalibrasi, identifiabilitas, validasi, dan ketidakpastian](source/id-ID/O005-BRIDGE-C4/content.html); [notebook](source/id-ID/O005-BRIDGE-C4/notebooks/bridge-c4-calibration-validation-uncertainty.ipynb); [dukungan belajar](backend/mastery/O005-BRIDGE-C4.mastery.json).

## Backend modular

Setiap unit menggunakan ID stabil yang netral terhadap bahasa. Seluruh 22 unit
sumber memiliki 3.448 segmen Inggris–Indonesia yang berpasangan. Empat modul
jembatan menambahkan 657 segmen kanonik id-ID dengan ledger semantik berversi,
sehingga keseluruhan backend memuat 4.105 segmen. Backend juga mengikat 141 ID
soal tetap, sepuluh notebook bab, dua belas notebook proyek dalam dua belas
paket mandiri, empat notebook jembatan, catatan unit berhash, serta jalur
eksplisit menuju aset, notebook, proyek, dan dukungan belajar. Lapisan ini
memungkinkan unit yang sama dipindahkan ke bahasa lain tanpa menjadikan Bahasa
Indonesia sebagai kunci struktur.

## Bangun dan periksa

Build HTML memerlukan Python, Beautiful Soup 4, dan Pandoc 3.9.0.2. PDF gabungan
memerlukan pypdf, ReportLab, Chromium atau Edge, MuPDF `mutool`, dan Poppler
untuk QA visual. Notebook memakai versi NumPy/SciPy/Matplotlib yang tercantum
dalam `requirements.lock` masing-masing.

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
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH08
python scripts/qa_unit.py --unit O005-LEGA-V101-CH08 --execute-notebook --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH09
python scripts/qa_unit.py --unit O005-LEGA-V101-CH09 --execute-notebook --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH10
python scripts/qa_unit.py --unit O005-LEGA-V101-CH10 --execute-notebook --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-PT05
python scripts/qa_unit.py --unit O005-LEGA-V101-PT05 --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH11
python scripts/qa_unit.py --unit O005-LEGA-V101-CH11 --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH12
python scripts/qa_unit.py --unit O005-LEGA-V101-CH12 --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH13
python scripts/qa_unit.py --unit O005-LEGA-V101-CH13 --deterministic-build
python scripts/build_ch14_project_packets.py
python scripts/build_unit_reader.py --unit O005-LEGA-V101-CH14
python scripts/qa_unit.py --unit O005-LEGA-V101-CH14 --execute-notebook --deterministic-build
python scripts/build_unit_reader.py --unit O005-LEGA-V101-FM01
python scripts/build_unit_reader.py --unit O005-LEGA-V101-PT01
python scripts/build_unit_reader.py --unit O005-LEGA-V101-BM01
python scripts/build_unit_reader.py --unit O005-LEGA-V101-BM02
python scripts/qa_unit.py --unit O005-LEGA-V101-FM01 --deterministic-build
python scripts/qa_unit.py --unit O005-LEGA-V101-PT01 --deterministic-build
python scripts/qa_unit.py --unit O005-LEGA-V101-BM01 --deterministic-build
python scripts/qa_unit.py --unit O005-LEGA-V101-BM02 --deterministic-build
python scripts/build_bridge_unit.py --unit O005-BRIDGE-C1
python scripts/build_bridge_unit.py --unit O005-BRIDGE-C2
python scripts/build_bridge_unit.py --unit O005-BRIDGE-C3
python scripts/build_bridge_unit.py --unit O005-BRIDGE-C4
python scripts/qa_bridge_unit.py --unit O005-BRIDGE-C1 --execute-notebook --deterministic-build
python scripts/qa_bridge_unit.py --unit O005-BRIDGE-C2 --execute-notebook --deterministic-build
python scripts/qa_bridge_unit.py --unit O005-BRIDGE-C3 --execute-notebook --deterministic-build
python scripts/qa_bridge_unit.py --unit O005-BRIDGE-C4 --execute-notebook --deterministic-build
python scripts/build_progress_pdf.py --complete
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
berlaku. Bab 8 mempertahankan tiga potret fase sumber, mencatat koreksi
matematika dan bibliografi secara eksplisit, mengganti ketergantungan PPLANE,
MAPLE, serta MATHEMATICA dengan satu notebook NumPy/SciPy/Matplotlib terbuka,
dan menambahkan tiga belas paket dukungan belajar lengkap.
Bab 9 mempertahankan tiga gambar sumber, memperbaiki derivasi kontinuitas,
argumen gerak acak, ambang laju Fisher–KPP, fluks kemotaksis, markup catatan,
dan aksesibilitas sitasi secara berjejak, serta menambahkan notebook difusi
NumPy/SciPy/Matplotlib dan tujuh paket dukungan belajar lengkap.
Bab 10 mempertahankan dua raster ilmiah sumber, mengganti kolase foto yang
tidak memiliki kredit komponen dengan SVG aksesibel yang dibuat independen,
mencatat koreksi matematis secara eksplisit, serta menambahkan notebook
pembentukan pola terbuka dan enam paket dukungan belajar lengkap. Pengantar
Bagian 5 mempertahankan kedua paragraf sumber tanpa komponen tambahan yang
tidak berlaku. Bab 11 mempertahankan seluruh struktur dan 165 rumus sumber,
mencatat tiga belas koreksi aljabar linear secara berjejak, serta menambahkan
tujuh paket petunjuk, pemeriksaan, dan pembahasan yang dihitung secara
independen; bab ini tidak memerlukan notebook atau aset.
Bab 12 mempertahankan seluruh struktur kalkulus vektor dan memetakan 161 rumus
sumber ke 165 rumus sasaran yang seluruh perbedaannya dinyatakan secara
berjejak; bab ini tidak memiliki soal, aset, tautan, catatan kaki, notebook,
atau komponen dukungan belajar untuk dibuat.
Bab 13 mempertahankan seluruh struktur PDB, 39 tautan fragmen, dan delapan
gambar sumber lokal beserta deskripsi panjangnya; 524 rumus sumber dipetakan
ke 528 rumus sasaran melalui koreksi yang seluruhnya dinyatakan dalam ledger.
Sebelas kelompok jawaban tercetak tetap dibedakan dari sebelas paket petunjuk,
pemeriksaan, dan pembahasan yang dihitung serta ditulis baru; bab penyegaran ini
tidak memiliki permukaan komputasi yang perlu diganti dengan notebook.
Bab 14 mempertahankan seluruh direktori dua belas proyek dan keenam belas
tautan rujukan tanpa menyalin artikel, kode, atau data yang dirujuk. Dua belas
paket Python yang ditulis secara independen menyediakan notebook tanpa keluaran
tersimpan, pemeriksaan deterministik, rubrik, provenance, lingkungan terpaku,
serta data sintetis atau yang dihasilkan model; paket-paket tersebut tidak
mengklaim mereproduksi hasil artikel sumber.
Prakata, pengantar Bagian 1, Pernyataan Aksesibilitas, dan Riwayat Versi
menutup seluruh permukaan pembaca sumber. Modul C1–C4 menambahkan alur kerja
reprodusibel, bifurkasi lokal, kekacauan dan peta balik, serta kalibrasi,
validasi, identifiabilitas, dan ketidakpastian. Keempat modul itu ditulis baru,
ditandai sebagai tambahan independen, dan tidak dipresentasikan sebagai materi
Lega atau University of Arizona.
