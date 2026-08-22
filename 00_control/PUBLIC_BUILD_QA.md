# Bukti Build dan QA Publik — Batas Kemajuan Bab 14

Tanggal batas: 2026-08-22

Dokumen ini merangkum bukti publik yang dapat direproduksi untuk batas
kemajuan edisi Bahasa Indonesia *Pengantar Pemodelan Matematika*. Edisi ini
masih dalam pengerjaan: Bab 1–14 dan pengantar Bagian 2–5 telah selesai,
sedangkan pengantar Bagian 1, materi awal/akhir, dan empat modul jembatan asli
belum selesai.

## Otoritas sumber

- Joceline Lega, *Introduction to Mathematical Modeling*, University of
  Arizona Pressbooks v1.01 (Maret 2026), CC BY-NC-SA 4.0.
- Bab 14: record Pressbooks 555, *Modeling Projects*, slug warisan
  `examples-of-project-topics`.
- Record kanonis: 38.887 byte, SHA-256
  `cb9e10a0a6df089194f2bb90bc335d641230cce00dc47c90b6d1802dd6769013`.
- HTML mentah: 18.737 byte, SHA-256
  `337ce752f17b70d3677216b114792685a84acded115dfdc06213bb469dd5761a`.
- HTML render: 18.394 byte, SHA-256
  `3487086799c2562006c975c587dcd61f573f80e0b8f71caa6129dc242c57d0f9`.

## Terjemahan dan backend Bab 14

- Sasaran *Proyek Pemodelan*: 19.110 byte, SHA-256
  `9a08e5a663685a52c4551a560ee68ea4f4dad9675b3aea04702dfa8416d719b4`.
- Replay struktur: 252/252 elemen, 16/16 tautan, 12/12 proyek, 95/95 butir
  daftar, dan nol rumus, soal, gambar, atau catatan kaki.
- Backend: 247 segmen berpasangan, 135.384 byte, SHA-256
  `8074b66de970f9381056a7c5c71d9bff2806337813606b7a68bf244305d7ad7f`.
- Catatan unit: 4.492 byte, SHA-256
  `e11be3dcf3907d84e6fffc9c9a78c7195ca32b517920e3c62a3c2f99d7d5028a`.

## Dua belas paket proyek terbuka

- Generator deterministik: 47.402 byte, SHA-256
  `62eeb904b4c06800f64758454e7a8db78ab89ae4dfb2ff2220e877ca5194f2c5`.
- Sumber paket: 72 berkas / 156.596 byte; arsip: 12 ZIP / 72.815 byte;
  katalog: 26.966 byte, SHA-256
  `9107863aee7cc9013b024e10d0091e227fdd3135b8913f5e103cc1157ce92e56`.
- Setiap paket memuat tepat satu notebook, README, pemeriksaan, rubrik,
  catatan provenance, dan `requirements.lock`. Semua arsip memakai urutan
  leksikografis, waktu tetap 1980-01-01, mode `0644`, jalur aman, CRC valid,
  serta byte yang sama dengan sumber longgar.
- Kedua belas notebook berjumlah 120 sel / 48 sel kode. Semuanya tanpa
  keluaran tersimpan dan berhasil dieksekusi dengan CPython 3.13.9,
  NumPy 2.4.4, SciPy 1.17.1, dan Matplotlib 3.10.9.
- Audit independen memperbaiki model kerumunan agar benar-benar memakai
  tetangga lokal yang dihitung ulang pada domain periodik. Uji benih tetap dan
  20 benih alternatif lulus seluruhnya; istilah yang tampil kepada pembaca
  juga dinormalisasi ke Bahasa Indonesia.
- Paket menggunakan data sintetis atau yang dihasilkan model. Artikel, kode,
  dan data yang dirujuk tidak didistribusikan ulang; tidak ada klaim bahwa
  paket mereproduksi hasil artikel.

## Pembaca dan determinisme

- Pembaca Bab 14: 17 berkas muatan / 268.890 byte, di luar manifes.
- Manifes paket: 1.878 byte, SHA-256
  `1be6f14f57da0ed950fd484c0c7e07291d981e4f4b76b2c8f3be49520507b597`.
- Dua build bersih menghasilkan 18 berkas yang identik byte demi byte;
  SHA-256 pohon QA kanonis:
  `da7aa599e38559f33553872f7e1663de6d555ebc478b6b598dc7aa1d4bf6c347`.
- QA browser pada 1280×900 menemukan shell 1.152 px, artikel 768 px, dan panel
  paket 960 px yang semuanya terpusat; pada 390×844, shell, artikel, dan panel
  menjadi kolom terpusat 357,5 px. Lebar gulir dokumen sama dengan lebar
  klien, tidak ada elemen yang keluar halaman, semua 17 ID unik, semua fragmen
  utuh, kedua belas tautan unduhan tampil, dan log peringatan/kesalahan kosong.

## Regresi unit yang telah selesai

Setelah perubahan pembaca bersama, seluruh 17 unit terdahulu dibangun ulang
secara deterministik dan lulus; notebook Bab 1–10 juga dieksekusi ulang.

| Unit | SHA-256 pohon QA |
|---|---|
| CH01 | `343ed0659f61ac2f8fad621c34a6cf7a676a24c791768837ec57fddd7baa5570` |
| CH02 | `da563b4dabb2cf0ee67278902fd045c12364cbb49f9aacd5988cdb4ebce92e8b` |
| CH03 | `1cc9ea306020bb19f02e8fe9e9b92fe6220110cc30afc4e86fb263ef0b635c81` |
| CH04 | `ae0af4c114547add1850c959d091fd7c98a15fa3c4953db50a60731c301494b9` |
| CH05 | `58b1770d618b315e731835ef53ace3eca45a2683289c394ff0daa9e2beb03711` |
| CH06 | `59256ab07fb600a26e288f474a6f9d3b972368cc1291bd588b54a95f25a17138` |
| CH07 | `8db3a1ea6666e686bbc306a15659cfb62bcfa17270b57e824fe84d3bd11ba615` |
| CH08 | `8045de1e1b58ae1b2e9fe52c32b61fac8b61b6be696d73da875eb5ad0d6f16f8` |
| CH09 | `c63676e0e174e6d681658dde23964fdc92fece55f6a3458303501603c2cb536a` |
| CH10 | `a4816135b5f8e4d1b073a21a0f65021276486a13287cdcd4e8884e6495be2e08` |
| CH11 | `45df98c3ec6ac845bd4311c8fd387cd80a0534f44dc2b0d4d8f7c2e6e88b48b0` |
| CH12 | `6f7119069e063be2507c154ef4dcde92aa319521ce0c5b5efadb7d832feffafa` |
| CH13 | `49c581e9c133255189b5f3e42b6766f1c91113ac7d2adc543fe40c20d8c2cc46` |
| PT02 | `9a5dfb8651f6e3be8a360874dc789cdd6e515f61c2ea77e75867c7552cc2a65c` |
| PT03 | `37bfd3d8f4a5dc76e58a5c1817add6f7c4de7c1d0a1cb063c2605f1c2797cdc1` |
| PT04 | `b52af2494af8020e7c3b8c0c18f6f77da2df089e005cee1a65306aba2eb3891d` |
| PT05 | `845ad33767a139e8a338a4500c21ee839ad90eeb3d5945a4b2bb6d95e6d730e7` |

Jangkauan tautan eksternal dan widget audio/live tidak diuji. Bab 14 tidak
memiliki audio atau widget live; keenam belas tautan eksternalnya dipertahankan
sebagai sitasi dan tidak diperlukan untuk pembaca luring.

## Preservasi publik

Batas ini diterbitkan sebagai
[Zenodo 10.5281/zenodo.22059940](https://doi.org/10.5281/zenodo.22059940)
dalam garis versi konsep
[10.5281/zenodo.22059939](https://doi.org/10.5281/zenodo.22059939).
Ketiga berkas publik diunduh kembali secara anonim; nama, jumlah byte, dan
SHA-256 seluruhnya sama dengan artefak lokal. SHA-256 inventaris publik:
`4d8b2b825076cdb91ce28032a4d836554e2ddb53751bba485078dbd6add7445f`.
