# Bukti Build dan QA Publik — Edisi Lengkap

Tanggal batas: 2026-08-23

Dokumen ini adalah kontrol publik yang mengikat untuk batas lengkap edisi
Bahasa Indonesia *Pengantar Pemodelan Matematika*. Semua 22 unit turunan
sumber dan empat modul jembatan orisinal telah selesai, dibangun, dan
diverifikasi. Modul jembatan adalah tambahan independen; tidak diklaim sebagai
bagian, ulasan, atau dukungan dari Joceline Lega maupun University of Arizona.

## Otoritas, lisensi, dan provenance

- Joceline Lega, *Introduction to Mathematical Modeling*, University of
  Arizona Pressbooks v1.01 (Maret 2026), CC BY-NC-SA 4.0.
- Sumber resmi: https://opentextbooks.library.arizona.edu/mathematicalmodeling/
- Edisi ini mempertahankan atribusi, pemberitahuan perubahan, NonCommercial,
  ShareAlike, hak komponen, dan non-endorsement. Berkas sumber resmi, aset
  pihak ketiga, dan batas lisensi tiap komponen tetap terikat di
  `RIGHTS_AND_PROVENANCE.md` dan manifes otoritas.
- Provenance produksi yang tampak pada reader dan artefak adalah tepat:
  `OpenAI Codex gpt-5.6-sol, Ultra.`
- QA istilah dibatasi pada saksi TeX Indonesia arXiv:2001.05854v1; identitas
  arsip dan TeX serta keputusan propagasinya tercatat di
  `TERMINOLOGY_QA_INDONESIAN_FIELD_SOURCE_20260822.md`.

## Cakupan lengkap

- Unit: 22 unit turunan sumber + `O005-BRIDGE-C1` sampai `C4` (26 reader).
- Segmen berpasangan: 3.448 unit sumber + 657 unit jembatan = 4.105 total;
  semua ID stabil,
  topology, formula, tautan, catatan kaki, aset, dan deskripsi dipertahankan.
- Dukungan mastery: 113 record soal sumber + 28 record jembatan = 141 record;
  setiap record memiliki petunjuk, pemeriksaan/jawaban, dan solusi kerja atau
  rubrik yang jujur.
- Notebook: 10 notebook bab + 12 notebook proyek + 4 notebook jembatan = 26;
  12 paket proyek mandiri dengan data sintetis/terbuka dan lockfile.
- Semua notebook jembatan lulus kernel bersih, cabang konfigurasi terganggu,
  pemeriksaan `python -O`, dekode PNG, dan build deterministik bertahap.

## Build reader dan browser QA

- PDF lengkap:
  `output/pdf/01_Pengantar_Pemodelan_Matematika_Edisi_Bahasa_Indonesia_Lengkap.pdf`
  — 43.463.488 byte, SHA-256
  `f62218d51c97bd86f94ac80c6fe179a2b535be5cd8f8bcf2f402764421597cf3`, 355
  halaman A4, tagged structure, `/Lang id`, 28 markah, tanpa form, JavaScript,
  atau suspects. Metadata judul, penulis, subjek, dan model cocok dengan
  receipt build.
- Receipt build PDF: 18.978 byte, SHA-256
  `e979ef2ac745b45ba50a15f43ab71864fc2e21c02151b7fa13592b0716ef9619`.
  Receipt mengikat seluruh 26 input reader, 141 mastery record, outline,
  HTML gabungan, pagination artifacts, dan identitas PDF.
- Semua 26 unit dibangun ulang setelah perbaikan CSS tabel responsif; static,
  optimized-static, kernel segar, konfigurasi terganggu, dan deterministic
  double-build QA lulus. Konten, mastery, notebook, dan formula tidak diubah
  oleh perbaikan ini.
- Browser QA desktop (1280 px): shell 1.152 px dan artikel 768 px terpusat;
  semua gambar termuat, ID unik, dan tidak ada page overflow.
- Browser QA mobile (390 px): artikel 357,507 px terpusat; `scrollWidth` dokumen
  sama dengan lebar klien untuk C2, C3, dan C4. Keempat belas tabel jembatan
  memakai `responsive-table` dan `tabindex="0"`; tabel lebar dapat digulir
  secara keyboard/touch tanpa melebarkan halaman. CSS salinan cocok byte dengan
  sumber, SHA-256 `c70e6b334ace189002d73ad8add7df1cf83d520548e86cb5e2bf609b9b2210f2`.
- Sampul, status/lisensi, daftar isi, batas setiap unit, halaman rumus/gambar,
  mastery, proyek, dan halaman penutup telah dirender dengan Poppler dan
  diperiksa. Tidak ditemukan clipping, overlap, formula ASCII mentah, atau
  transisi unit rusak.

## Package gate

At every substantial boundary, build the complete package into a new
no-overwrite directory under `release/zenodo/` with a distinct matching
version label. Mode lengkap wajib menghasilkan tepat enam berkas: PDF reader
(primer), ZIP sumber ringkas, receipt build, LICENSE, RELEASE_MANIFEST, dan
CHECKSUMS. ZIP wajib CRC-valid, path aman, dan seluruh payload di bawah
500.000.000 byte. Kontrol, receipt publikasi, cache, render sementara, dan
credential tidak boleh masuk payload.

## Public preservation boundary

Zenodo concept DOI `10.5281/zenodo.22059939` kini menunjuk ke versi publik
terbaru yang telah dikoreksi; identitas record dan DOI versi tertentu dicatat
di receipt terpisah. Setiap berkas telah dibaca kembali secara anonim dan
dicocokkan dengan nama, byte, dan SHA-256 lokal. Figshare tetap merupakan
rute metadata/link CC0 saja karena
platform tidak menawarkan CC BY-NC-SA 4.0, tetapi akun yang disediakan kini
nonaktif (HTTP 403) dan artikel lama melaporkan telah dihapus. Jangan membuat
item duplikat atau mengunggah byte karya di bawah lisensi pengganti; lanjutkan
artikel `33314769` dan collection `8668413` hanya setelah akun dipulihkan.
GitHub tetap tidak disentuh selama suspensi akun.
## Complete reader publication boundary — 2026-08-23

- The latest Zenodo version under concept `10.5281/zenodo.22059939` supersedes
  the earlier complete version because the public segment census was corrected;
  the exact version DOI is in the release receipt.
- The six-file reader-first package is reader-first and below the preservation
  cap. The complete PDF is 355 tagged A4 pages and hashes to
  `f62218d51c97bd86f94ac80c6fe179a2b535be5cd8f8bcf2f402764421597cf3`.
- The package contains 3,448 source segments and 657 bridge segments (4,105
  total). Anonymous downloads of all six files match the current package
  byte-for-byte; the exact versioned receipt is retained in `00_control`.
- Figshare update is externally blocked: the supplied account token returns
  HTTP 403 `InactiveAccount`, the prior article page is removed, and current
  project/collection pages have no content. No duplicate or substitute-license
  upload was made. See
  `FIGSHARE_PUBLICATION_RECEIPT_COMPLETE_20260823.json`.
