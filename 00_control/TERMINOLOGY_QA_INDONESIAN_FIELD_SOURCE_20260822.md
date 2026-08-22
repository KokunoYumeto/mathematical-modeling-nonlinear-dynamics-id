# Indonesian field-terminology QA — 2026-08-22

## Decision

The edition passed a bounded terminology comparison against a genuine
Indonesian mathematical-modeling source with downloadable TeX. The comparison
did justify several refinements: mathematical boundary conditions are now
consistently `syarat batas`; reader-facing dynamical-system prose is normalized
to `sistem dinamik`; and the matrix is consistently `matriks Jacobi` while the
lowercase program identifier `jacobian` remains unchanged. Eight affected
units were rebuilt and passed deterministic structural QA.

This audit did not import prose, formulas, figures, or code from the witness
into the edition. It used the witness only as terminology evidence.

## Primary witness

- Natanael Karjanto, *A theoretical study on a two-dimensional flap-type
  wavemaker*, arXiv:2001.05854v1, submitted 2020-01-11 06:15:42 UTC, DOI
  `10.48550/arXiv.2001.05854`.
- Official record: <https://arxiv.org/abs/2001.05854v1>.
- Official source: <https://arxiv.org/src/2001.05854v1>.
- Official record scope: 94 pages, with an English translation and the complete
  original 47-page Indonesian version; subject `physics.flu-dyn` and MSC
  classes include boundary-value and differential-equation classifications.
- Official license: CC BY-SA 4.0. This separate witness license does not alter
  the Lega edition's CC BY-NC-SA 4.0 boundary.
- Frozen source archive: 144,585 bytes, SHA-256
  `520cd160b47664dda32e57df87a6eb028348154e4d7a7494d230e8e517891d53`.
- Indonesian TeX `2001arXivTA-Indonesian.tex`: 91,655 bytes, 2,076 physical
  lines, SHA-256
  `03f7e68801badc84255df3323078ae00eee7ecff8a9f118cba064ce5d46ff2f2`.
- Full safe 20-member inventory: `authority/terminology/arxiv-2001.05854v1/SOURCE_MANIFEST.json`.

The witness is representative for this bounded purpose because the Indonesian
text develops a mathematical wave model using ideal-fluid assumptions,
Laplace's equation, PDEs, boundary-value formulation, linearization, dispersion
relations, and Newton–Raphson computation. It is not merely an Indonesian
abstract.

## Terms inspected directly in the TeX

| Source-attested form | Edition decision |
|---|---|
| `Pemodelan Matematika`, `pemodelan secara matematis`, `model matematis` | Retain `pemodelan matematika` for the discipline/process and `model matematika` in ordinary reader prose. The exact discipline form is directly attested. |
| `asumsi`; section title `Anggapan Dasar` | Retain `asumsi` as the default. Treat `anggapan dasar` as an acceptable contextual heading, not a global replacement. |
| `persamaan diferensial pengatur` | Admit as the preferred form for *governing differential equation*. |
| `masalah nilai batas`; repeated `syarat batas` | Retain `masalah nilai batas` and normalize all mathematical boundary-condition occurrences from `kondisi batas` to `syarat batas`. |
| `persamaan diferensial parsial`; `persamaan kontinuitas` | Retain the existing exact forms. |
| `proses linearisasi` | Retain `linearisasi`. The witness's mixed 2001 spelling of `non-linear` is not adopted as a modern orthographic rule. |
| `metode numerik`; `iterasi Newton-Raphson`; `tebakan awal`; `akar persamaan`; `galat` | Retain/admit these forms. Use `galat numerik` when the kind of error must be distinguished from model discrepancy. |
| `relasi dispersi` | Retain the existing Chapter 10 form. |
| `kekonvergenan` once | Do not replace modern `konvergensi`; the single older derivative is evidence of usage, not sufficient reason to regress current terminology. |

## Additional internal consistency decisions

- `initial condition`: the witness does not attest this term. The edition now
  records `kondisi awal` as the preferred running-prose form because it is the
  dominant natural form in the completed reader; `syarat awal` remains valid
  when a sentence stresses a mathematical constraint. `Masalah nilai awal`
  remains the fixed term for *initial-value problem*. No blind replacement was
  made.
- `dynamical system`: normalize reader-facing variants `sistem dinamis` and
  `sistem dinamika` to the established glossary form `sistem dinamik`.
- `Jacobian matrix`: normalize reader-facing `Jacobian` to `matriks Jacobi`.
  The lowercase `jacobian` function name remains untouched so executable code
  and API identity do not drift.
- `equilibrium` versus `fixed point`: document rather than collapse the
  distinction. Use `keadaan kesetimbangan` for a physical/epidemiological
  state, `titik kesetimbangan` when represented as a point, and `titik tetap`
  for a fixed point of a map or flow.
- `gelombang progresif` in the fluid-mechanics witness does not replace the
  established `gelombang berjalan` for a formal traveling-wave solution in
  Fisher–KPP context; the meanings overlap but the disciplinary contexts differ.

## Propagation

Canonical wording and generated backends/readers were updated only in the
affected units:

- CH01: `sistem dinamik`.
- CH02: four mastery-layer boundary-condition occurrences.
- CH04: one translated exercise occurrence and one notebook heading.
- CH05: three mastery-layer `matriks Jacobi` occurrences.
- CH06: chapter and mastery `matriks Jacobi` occurrences.
- CH07: `sistem dinamik` and `matriks Jacobi` throughout chapter/mastery prose.
- CH10: notebook/mastery `syarat batas` and `matriks Jacobi` occurrences.
- CH13: `sistem dinamik` throughout chapter prose.

After regeneration, canonical reader-facing source/mastery/notebook files have
zero residual occurrences of `kondisi batas`, uppercase `Jacobian`, `sistem
dinamis`, or `sistem dinamika`. Three lowercase `jacobian` occurrences remain
only as the Chapter 3 Python function identifier and calls.

## Deterministic QA

All affected units passed exact source-target topology, formula/link/problem
censuses, local dependency checks, backend hash binding, and repeated
byte-identical builds. No notebook code cell was changed or executed in this
terminology-only audit.

| Unit | Structure retained | Deterministic tree SHA-256 |
|---|---:|---|
| CH01 | 120 elements / 14 links / 14 formulas / 7 problems | `b846f4aa5e42610b740bbfc61cab374ef62a69a9ea93976dc2cfc8f9dc9b7dc7` |
| CH02 | 103 / 10 / 92 / 7 | `f6f50a235a5dca62cebd5e18d9fe8ee1c5285933620454d720ffbca3195c87d9` |
| CH04 | 143 / 22 / 245 source formulas / 4 | `54290028a7e86ca0d4e12614d4d82d757c8b9ca89d530e5a4b3c8f42ff4c5ca3` |
| CH05 | 364 / 50 / 389 source formulas / 17 | `63e643c8e9307d62f914bd073eadc94b407e81f0fce77bd1a466a9425d9001ed` |
| CH06 | 185 / 31 / 227 source formulas / 6 | `4bbc34547434cd3fd27d31d8c8fd2dd6737e75fe556ae4276d41633e4bbd2306` |
| CH07 | 126 / 29 / 150 source formulas / 5 | `2ba1b2952d7738db5b52dc095847e4c026c838a1d10853fac0ed5d2871d38097` |
| CH10 | 116 / 24 / 77 source formulas / 6 | `aad8611f1b58f3ce1d6191c7646b61ee2a180b1491c51c14e57466133ea280a5` |
| CH13 | 456 / 39 / 524 source formulas / 11 | `b5f6903b1a08b80d0e0e154c22f41c2dce59f0270e39f6ca312789be862b684e` |

## Model-provenance check

The exact identification `OpenAI Codex gpt-5.6-sol, Ultra.` is now present in
the repository README, the rights/provenance control, Zenodo record
`10.5281/zenodo.22061640`, and Figshare article
`10.6084/m9.figshare.33314769.v2`. Existing source, author, and human-contributor
credits remain intact. The public Zenodo release bytes predate this metadata
note and were not misrepresented as containing the later local README edit.

## Next action

Resume the selected O005 production cursor at `O005-LEGA-V101-FM01`, the
Pressbooks Preface, only after this QA boundary and the public preservation
receipts are sealed in the durable controls.
