# Current State — O005/C120

Updated: 2026-08-21 Europe/Berlin

## Status

Lega Pressbooks v1.01 is selected and admitted. Source selection is closed.
The official PDF and EPUB are frozen locally, and the coordinator's complete
22-record semantic snapshot and 45-asset manifest have been copied verbatim
into this lane. Chapters 1–3 and the visible Part 2 introduction are
translated, built, and verified. Production now moves to Chapter 4,
Pressbooks record 39, *Stone-Skipping*. The earlier
cursor's record 29 / “Dimensional Analysis” pair was invalid and has been
corrected from the frozen TOC.

## Verified authority

- Official root: <https://opentextbooks.library.arizona.edu/mathematicalmodeling/>
- Version: 1.01, March 2026.
- License: CC BY-NC-SA 4.0, with empty section-level overrides in the frozen
  record closure.
- PDF: 9,761,231 bytes, SHA-256
  `6622c9e8fabe3a96e5c4df2836c464ec0d465a5f1acadc2235141cdbf6fb3ec6`.
- EPUB: 8,082,717 bytes, SHA-256
  `ef87bf69657ce97d2f2b81696bb47e73b0ad1556f4a7d3659c716eebb6f97c6f`.
- Semantic manifest: 22 records, 986,818 canonical bytes, SHA-256
  `d40956f8bd4cca1545c4ec7a809bfb8d20c18c4ed84b101b39e8262e2f42eba5`.
- Asset manifest: 45 assets / 5,042,424 bytes, SHA-256
  `6bdfc501e3134de338fc9862feb4abbbd503037295ab8c701a627cb33550c740`.

## Admitted Chapter 1 boundary

- Pressbooks chapter 25, *On the Nature of Mathematical Modeling*; target
  *Tentang Hakikat Pemodelan Matematika*; canonical record 37,918 bytes,
  SHA-256
  `0286cb444c7f2f4a2db83865f948d3d3dc00147e2280fa665a1abc68ad804826`.
- Complete natural id-ID fragment: 18,153 bytes, SHA-256
  `4525a8ff80cc1d05c4d86cc11b00b53ec2d0430b9e404715625f248a7758fee3`.
- Accessible Indonesian SVG: 3,756 bytes, SHA-256
  `d7183e2bfe20bb2bc72da3a39943c34feb66d60522792bbe967b2a8c89ac1d2a`.
- Seven-record mastery layer: 29,810 bytes, SHA-256
  `58f5c0aff94d3d6290775906ebfb4f81e9fafb50b31d60aa8b21080541c77a6d`.
- Open Problem 7 notebook: 14,942 bytes, SHA-256
  `75eb7a3b4e5f67bf12c689aa3162ee8ba49149cd00c96e53cae119a524d11a5e`.
- Modular segment layer: 125 records / 83,591 bytes, SHA-256
  `5fdfc7baca4367ceab409b6e55cc6a8144fd9fe39161d1b5174731420f7c9e7a`.
- Reader package: eight payload files / 217,460 bytes, excluding the manifest;
  manifest SHA-256
  `04cb3ff2c58600389010d965190e52288a40e3dc1a6088c6bb90063a0fc2e87a`.
- Exact structure replay: 120/120 elements, 14/14 links, 14/14 TeX
  expressions, seven/seven problems; no unexplained drift.
- Notebook: all seven code cells executed with the pinned environment; all
  deterministic numerical/model-selection assertions passed.
- The generic reader renders 14 chapter and 46 mastery MathML nodes. Repeated
  clean builds were byte-identical across nine files, canonical tree SHA-256
  `6cfa3acae2b7ef23e0265eee6c7ce7b9d59a4266f61a31300510ccc7363a1e67`.
- Browser QA: centered 768 px article at 1280 px; clean 390 px mobile layout;
  zero horizontal overflow at both sizes. Audio/live widgets do not exist and
  were not exercised; external-link reachability was not tested.

## Admitted Chapter 2 boundary

- Source record: Pressbooks chapter 27, *First Steps: Modeling the Wave*;
  target title *Langkah Awal: Memodelkan Gelombang*; modified
  `2026-03-27T02:10:41Z`.
- Canonical record: 39,193 bytes, SHA-256
  `428a143edeec7843d3f4a2e2f02e5aa50fcde2cff366ca976988ecfa4191e69b`;
  authority manifest: 875 bytes, SHA-256
  `9eb2513778b61f33c07d84442ad93803c90969448fbe9e20633e258ba9738840`.
- Scope: 2,650 words in the frozen TOC, seven exercises, 92 TeX occurrences,
  one source figure, and ten preserved `href` occurrences.
- Complete natural id-ID fragment: 19,538 bytes, SHA-256
  `e044dbfde28c561f43922fabf24af41cc47b2fb4e3307fb6146646b700cf8c4c`.
- Source-derived figure: 80,026 bytes, byte-identical to the frozen asset,
  SHA-256
  `9abe8e17abd593811c14a1d6ea72b3ff727682ba58d000a87ece4056332769b6`.
- Seven-record mastery layer: 27,962 bytes, SHA-256
  `46c7f337c6fe93a0adfce03d65df4f35c9f0341b5c4c0f486bc14145f85b6296`.
- Independent open-wave notebook: 23,026 bytes, SHA-256
  `8e31dc2dfaa61b3e0f76dd04b29867fcadd303490622a8ea0e1f5ad77f2ce517`.
- Modular segment layer: 121 records / 84,773 bytes, SHA-256
  `0e1dd86ab9c5dc0d2e6338a2ae8909e5d5825f4d8b5866ca7eab88dfb0246b6a`.
- Reader package: eight payload files / 358,731 bytes, excluding the manifest;
  manifest SHA-256
  `9b4cbf27e7b433299e235aec2bbf13d9a00a4dbf47566474f125c9d127316288`.
- Exact structure replay: 103/103 elements, 10/10 links, 92/92 protected
  TeX expressions, and seven/seven problems; no unexplained drift.
- Notebook: all seven code cells and 23 assertions passed with fixed seed
  `20260821`; the baseline produced a 15-seat median width and measured speed
  20 seats/second with regression R-squared 1.0.
- Repeated clean builds were byte-identical across nine files, canonical tree
  SHA-256 `568dc4dcc92fb005702a40106fde0821e61ec30341a662f72d17bc252240137e`.
- Browser QA: centered 768 px article at 1280 px and 357.5 px article at
  390 px; zero horizontal overflow, missing images, raw mastery TeX, or
  unlabeled images. External-link reachability and audio/live widgets were not
  exercised.

## Admitted Part 2 introduction boundary

- Source record: visible Pressbooks part 28, *Models from Classical
  Mechanics*; target title *Model-Model dari Mekanika Klasik*; modified
  `2024-06-29T02:57:03Z`.
- Canonical record: 2,296 bytes, SHA-256
  `03ead95b0ebcfb470c92bb7e48a85ce45d7639ec0aafb00f981eaf90ffd3f1e9`;
  authority manifest: 657 bytes, SHA-256
  `888785538e02b410ec91b1e1a4f2906c5ffeb1525c8b14408c2547b2b7d868a5`.
- Scope: 121 source words in three visible paragraphs, with no formula, link,
  asset, exercise, mastery, or notebook surface.
- Complete natural id-ID fragment: 713 bytes, SHA-256
  `c7351c8342d7334116e69fbd16b7e19030c9492237e00c99713bcca0697e4087`.
- Modular segment layer: three paragraph records / 2,733 bytes, SHA-256
  `63492fc25014f6872dc8c5c4a90fad31813be679a7a0d78332e61ec1c77f7d54`.
- Reader package: four payload files / 11,145 bytes, excluding the manifest;
  manifest SHA-256
  `32e6dcc39f2c980e5b33b8befb788b7eab4310e05d3cf725130c418be3dd3f32`.
- Exact replay: zero/zero source-target elements, links, formulas, and
  problems; three/three paragraph boundaries and segment hashes exact.
- Repeated clean builds were byte-identical across five files, canonical tree
  SHA-256 `42a2af70218424bca7f768e665c10c429fcd3e68db40da41eecc4cd423c93cdd`.
- Browser QA: the article is centered at 768 px in a 1,280 px desktop viewport
  and 357.5 px in a 390 px mobile viewport; zero horizontal overflow or broken
  assets. The navigation and official-source label correctly identify a
  section rather than a chapter. External-link reachability and audio/live
  widgets were not exercised.

## Admitted Chapter 3 boundary

- Source record: Pressbooks chapter 38, *The Nonlinear Pendulum*; target title
  *Pendulum Nonlinear*; modified `2026-03-27T02:14:38Z`.
- Canonical record: 128,063 bytes, SHA-256
  `240a00176ea39c067c36393facf35308bdbee11925dbc293bad2ce33ca9c339c`;
  authority manifest: 2,716 bytes, SHA-256
  `77d490822fd1ba9fcfab559ffe9d8941f8d483d0adaa79eb60c5f621c23c673b`.
- Scope: 7,125 source words, 423 source elements, 62 links, 404 protected TeX
  occurrences, 23 problems, three footnotes, and nine source figures with
  complete local asset closure.
- Complete natural id-ID fragment: 57,724 bytes, SHA-256
  `37c0b3df486f20fa29929d983fc70f92beb386cb980937a3cb032e6995e7cac3`.
- Twenty-three-record mastery layer: 77,899 bytes, SHA-256
  `c9375f9c54b0e67ba301b495763d235ece03aaaa2fd12ac6b88aaaacaadc915e`.
- Independent open phase-plane notebook: 19,642 bytes, SHA-256
  `45bb23aaf15fc03d5f7e878995c9cd0a38a31c2bf64f325b3fdb1e204939505f`;
  pinned environment lock: 276 bytes, SHA-256
  `e0d52933f0d73f273363adb1a77c42b7680a05d3f80ccb9143dac8e079743041`.
- Modular segment layer: 449 records / 285,519 bytes, SHA-256
  `0008a0facb9d0616b8f0c13876c8c8089458069c78aba4b65b1c5a7159bba39e`.
- The reader uses eight byte-identical source figures and one localized
  Figure 3.4 adaptation (131,859 bytes, SHA-256
  `76172508b59ddce827f57d8e76d7c89c49dc9b56294a7ef32c6287e4228fe975`),
  with the unchanged source bitmap and an exact adaptation receipt retained.
- Reader package: 16 payload files / 2,025,454 bytes, excluding the 1,670-byte
  manifest; manifest SHA-256
  `1957c32aab44de6589f8c5509da0393848f845c56deb15bd48234577893d7be5`.
- Exact structure replay: 423/423 elements, 62/62 links, 404 source TeX
  occurrences mapped to 406 declared target occurrences, and 23/23 stable
  problems; no unexplained drift.
- Notebook: 13 cells / seven code cells / 19 assertions. NumPy 2.4.4,
  SciPy 1.17.1, and Matplotlib 3.10.9 executed successfully; conservative
  energy drift was `1.943e-15`, the damped energy never increased, and the
  dissipation-balance error was `1.559e-05`.
- Reader renders 408 chapter MathML nodes and 455 mastery MathML nodes, resolves
  all nine figures and the notebook/lock locally, and exposes all three
  footnotes as Indonesian notes. Repeated clean builds were byte-identical
  across 17 files, canonical tree SHA-256
  `427eabd4cd6a5f4e40c7df02c713f6c0f29d47949807ab39a64da2036bcd71c1`.
  Final-byte structural, locality, responsive-CSS, and accessibility checks
  pass; bounded browser evidence and its explicit limits are in `BUILD_QA.md`.

## Next action

Prepare and translate Chapter 4, Pressbooks chapter record 39,
*Stone-Skipping*, as `O005-LEGA-V101-CH04`, preserving the hybrid
free-flight/collision model, rigid-body equations, four problems, formulas,
links, footnotes, both figures and descriptions, and the replacement/redraw
boundary for Figure 4.1. Do not return to source selection.
