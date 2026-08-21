# Current State — O005/C120

Updated: 2026-08-21 Europe/Berlin

## Status

Lega Pressbooks v1.01 is selected and admitted. Source selection is closed.
The official PDF and EPUB are frozen locally, and the coordinator's complete
22-record semantic snapshot and 45-asset manifest have been copied verbatim
into this lane. The complete Chapter 1 and Chapter 2 units,
`O005-LEGA-V101-CH01` and `O005-LEGA-V101-CH02`, are translated, built, and
verified. Production now moves to the visible Part 2 introduction, Pressbooks
record 28, before Chapter 3. The earlier cursor's record 29 / “Dimensional
Analysis” pair was invalid and has been corrected from the frozen TOC.

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
- Reader package: eight payload files / 217,390 bytes, excluding the manifest;
  manifest SHA-256
  `1ba10f670dab0b4cf78b30ef17e25984f21e486ac95f98db50d5f3d899d96cb9`.
- Exact structure replay: 120/120 elements, 14/14 links, 14/14 TeX
  expressions, seven/seven problems; no unexplained drift.
- Notebook: all seven code cells executed with the pinned environment; all
  deterministic numerical/model-selection assertions passed.
- The generic reader renders 14 chapter and 46 mastery MathML nodes. Repeated
  clean builds were byte-identical across nine files, canonical tree SHA-256
  `29ceb15656b43f45da8b801ccefab60b20a9d4f3d00a55a73dcbdb941770d082`.
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
- Reader package: eight payload files / 358,661 bytes, excluding the manifest;
  manifest SHA-256
  `5296b09661d64f4c33aaaa4736404f0d87eb5ea4bc51e5e8660719607da2dace`.
- Exact structure replay: 103/103 elements, 10/10 links, 92/92 protected
  TeX expressions, and seven/seven problems; no unexplained drift.
- Notebook: all seven code cells and 23 assertions passed with fixed seed
  `20260821`; the baseline produced a 15-seat median width and measured speed
  20 seats/second with regression R-squared 1.0.
- Repeated clean builds were byte-identical across nine files, canonical tree
  SHA-256 `b0f14a66e0a4e3ed39c79e39daa3ee3b46a6b5af75bb1856247caf4aca0c05b2`.
- Browser QA: centered 768 px article at 1280 px and 357.5 px article at
  390 px; zero horizontal overflow, missing images, raw mastery TeX, or
  unlabeled images. External-link reachability and audio/live widgets were not
  exercised.

## Next action

Prepare and translate the exact visible Part 2 introduction, Pressbooks part
record 28, *Models from Classical Mechanics*, as `O005-LEGA-V101-PT02` before
proceeding to Chapter 3, record 38, *The Nonlinear Pendulum*. Do not return to
source selection.
