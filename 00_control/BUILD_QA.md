# Build and QA Log — O005/C120

## Admitted build — O005-LEGA-V101-CH01 — 2026-08-21

- Builder: `scripts/build_unit_reader.py --unit O005-LEGA-V101-CH01`, Pandoc
  3.9.0.2, native MathML for both chapter and mastery mathematics.
- QA: `scripts/qa_unit.py --unit O005-LEGA-V101-CH01 --execute-notebook
  --deterministic-build`, exit 0.
- Structural replay: 120 source / 120 target elements; ordered tags exact;
  attributes exact after only the localized image source/alt and seven stable
  problem IDs; 14 hrefs and 14 protected TeX expressions exact and ordered.
- Backend: 125 paired translation segments and seven complete mastery records;
  every segment text hash and every unit component hash replayed.
- Notebook: 12 cells / seven code cells; clean stored outputs; fixed seed
  `20260821`; NumPy 2.4.4, SciPy 1.17.1, Matplotlib 3.10.9; every cell and all
  numerical, parameter-recovery, model-selection, and reproducibility
  assertions passed under the existing Miniconda environment.
- Reader: eight payload files / 217,460 bytes excluding
  `PACKAGE_MANIFEST.tsv`; 14 chapter MathML nodes and 46 mastery MathML nodes;
  no missing local dependency, duplicate ID, broken
  fragment, local profile path, personal-name leak, token shape, or U+FFFD.
- Reader manifest: 820 bytes, SHA-256
  `04cb3ff2c58600389010d965190e52288a40e3dc1a6088c6bb90063a0fc2e87a`.
- Deterministic double build: nine files including manifest, byte-identical;
  canonical tree SHA-256
  `6cfa3acae2b7ef23e0265eee6c7ce7b9d59a4266f61a31300510ccc7363a1e67`.
- Browser visual QA: at 1280×720 the main shell was 1,152 px and centered,
  article 768 px and centered, with zero horizontal overflow; at 390×844 the
  article was 357.5 px wide with zero overflow. Header, notice, objectives,
  figure, native MathML, and disclosure styling were inspected in dark mode.
- External scholarly/news link reachability was not tested. No audio or live
  widget exists in this unit; none was exercised.

## Standing unit gates

Required gates for each translated chapter unit:

- canonical source record/hash and extracted `content.raw` binding;
- source/target semantic topology and attribute preservation;
- every protected TeX occurrence replayed or explicitly corrected in the
  source-correction ledger;
- every source figure resolved locally with meaningful Indonesian alternative
  text and its available long description;
- every source link preserved and every source exercise mapped to one stable
  problem ID;
- one hint, check/final answer, and worked solution or honest rubric for every
  source problem;
- Python notebook executes from a clean pinned environment with deterministic
  numerical assertions and no proprietary dependency;
- HTML language, headings, landmarks, keyboard links, contrast, responsive
  layout, privacy, local-asset closure, and offline behavior;
- deterministic clean rebuild yields the same artifact manifest and hashes.

## Admitted build — O005-LEGA-V101-CH02 — 2026-08-21

- Builder: `scripts/build_unit_reader.py --unit O005-LEGA-V101-CH02`, Pandoc
  3.9.0.2, native MathML for both chapter and mastery mathematics.
- QA: `scripts/qa_unit.py --unit O005-LEGA-V101-CH02 --execute-notebook
  --deterministic-build`, exit 0.
- Structural replay: 103 source / 103 target elements; ordered tags exact;
  attributes exact after only the localized image source/alt and seven stable
  problem IDs; 10 hrefs and 92 protected TeX expressions exact and ordered.
- Backend: 121 paired translation segments and seven complete mastery records;
  every segment text hash and every unit component hash replayed.
- Notebook: 15 cells / seven code cells / 23 assertions; clean stored outputs;
  fixed seed `20260821`; NumPy 2.4.4 and Matplotlib 3.10.9. Baseline median
  width was 15 seats, measured speed 20 seats/second, and speed-regression
  R-squared 1.0; direction reversal and extinction parameter cases passed.
- Reader: eight payload files / 358,731 bytes excluding
  `PACKAGE_MANIFEST.tsv`; 92 chapter MathML nodes, 155 mastery MathML nodes,
  and three local dependency classes; no missing local dependency, duplicate
  ID, broken fragment, raw mastery TeX, local profile path, personal-name leak,
  token shape, or U+FFFD.
- Reader manifest: 822 bytes, SHA-256
  `9b4cbf27e7b433299e235aec2bbf13d9a00a4dbf47566474f125c9d127316288`.
- Deterministic double build: nine files including manifest, byte-identical;
  canonical tree SHA-256
  `568dc4dcc92fb005702a40106fde0821e61ec30341a662f72d17bc252240137e`.
- Browser visual QA: at 1280×720 the article was 768 px and centered; at
  390×844 it was 357.5 px wide. Both layouts had zero horizontal overflow and
  zero broken or unlabeled images. The source formula renders `jika`, while
  exact source TeX remains in backend/provenance fields.
- External scholarly link reachability was not tested. No audio or live widget
  exists in this unit; none was exercised.

## Admitted build — O005-LEGA-V101-PT02 — 2026-08-21

- Builder: `scripts/build_unit_reader.py --unit O005-LEGA-V101-PT02`, Pandoc
  3.9.0.2; no mathematics conversion was applicable.
- QA: `scripts/qa_unit.py --unit O005-LEGA-V101-PT02
  --deterministic-build`, exit 0.
- Structural replay: source and target each contain three plain-text paragraph
  units and no parser-visible element, href, TeX expression, or problem. All
  three ordered source/target segment hashes replayed.
- Backend: three paired translation segments; stable unit type `part`; empty
  problem set; mastery, notebook, and asset fields correctly absent rather
  than represented by dummy files.
- Reader: four payload files / 11,145 bytes excluding
  `PACKAGE_MANIFEST.tsv`; one local CSS dependency; no missing dependency,
  duplicate ID, broken fragment, local profile path, personal-name leak,
  token shape, proprietary-tool source, or U+FFFD.
- Reader manifest: 397 bytes, SHA-256
  `32e6dcc39f2c980e5b33b8befb788b7eab4310e05d3cf725130c418be3dd3f32`.
- Deterministic double build: five files including manifest, byte-identical;
  canonical tree SHA-256
  `42a2af70218424bca7f768e665c10c429fcd3e68db40da41eecc4cd423c93cdd`.
- Existing-unit regression: current generalized builder reproduced all nine
  existing Chapter 1 files and all nine existing Chapter 2 files byte-for-byte.
- Browser visual QA: 768 px centered article at 1280×720 and 357.5 px article
  at 390×844; zero horizontal overflow or broken images. Navigation, header,
  article label, and official-source link all identify the unit as a section.
- External source-link reachability was not tested. No audio, live widget,
  formula, mastery, or notebook surface exists in this unit.

## Admitted build — O005-LEGA-V101-CH03 — 2026-08-21

- Builder: `scripts/build_unit_reader.py --unit O005-LEGA-V101-CH03`, Pandoc
  3.9.0.2, native MathML for chapter and mastery mathematics.
- QA: `scripts/qa_unit.py --unit O005-LEGA-V101-CH03 --execute-notebook
  --deterministic-build`, exit 0.
- Structural replay: 423 source / 423 target elements, 62 / 62 links, 404
  ordered source TeX occurrences mapped to 407 declared target occurrences,
  and 23 / 23 source problems with stable IDs. The three extra target formulas
  are explicit mathematical corrections recorded in `SOURCE_CORRECTIONS.csv`.
- Backend: 449 paired segments / 285,519 bytes, SHA-256
  `0008a0facb9d0616b8f0c13876c8c8089458069c78aba4b65b1c5a7159bba39e`;
  23 complete mastery records / 77,899 bytes, SHA-256
  `c9375f9c54b0e67ba301b495763d235ece03aaaa2fd12ac6b88aaaacaadc915e`.
- Notebook: 13 cells / seven code cells / 19 assertions; clean stored outputs;
  NumPy 2.4.4, SciPy 1.17.1, and Matplotlib 3.10.9. Conservative maximum
  energy drift `1.943e-15`, damped maximum step `-4.019e-14`, and maximum
  dissipation-balance error `1.559e-05`; all assertions passed.
- Reader: 16 payload files / 2,025,454 bytes excluding the 1,670-byte manifest;
  408 chapter and 455 mastery MathML nodes; 12 local dependencies; nine
  resolved figures, three localized notes, and zero missing local dependency,
  duplicate ID, broken fragment, raw mastery TeX, token shape, or U+FFFD.
- Figure 3.4 is an Indonesian adaptation of the retained frozen source bitmap;
  the final 1,024×1,024 asset is 131,859 bytes with SHA-256
  `76172508b59ddce827f57d8e76d7c89c49dc9b56294a7ef32c6287e4228fe975`.
  Figure 3.1 is constrained to its 300 px intrinsic width in the reader.
- Reader manifest SHA-256
  `1957c32aab44de6589f8c5509da0393848f845c56deb15bd48234577893d7be5`.
  Deterministic double build: 17 files including manifest, byte-identical;
  canonical tree SHA-256
  `427eabd4cd6a5f4e40c7df02c713f6c0f29d47949807ab39a64da2036bcd71c1`.
- Regression: the generalized builder reproduced Part 2 byte-for-byte and
  rebuilt Chapter 1 and Chapter 2 deterministically after adding visible
  `requirements.lock` downloads. Their new trees are respectively
  `6cfa3acae2b7ef23e0265eee6c7ce7b9d59a4266f61a31300510ccc7363a1e67`
  and `568dc4dcc92fb005702a40106fde0821e61ec30341a662f72d17bc252240137e`.
- A browser pass on superseded Chapter 3 bytes found a centered 768 px desktop
  article, zero horizontal overflow, nine loaded local figures, zero missing
  alt text, and no duplicate IDs. Its two findings were then resolved by
  localizing Figure 3.4's English labels and constraining Figure 3.1 to its
  300 px intrinsic width. One bounded final-byte retry failed because the
  in-app browser was unavailable, so the final index is not claimed as visually
  certified. Final-byte structural/locality checks pass; mobile layout,
  keyboard focus, computed contrast, and external-link reachability remain
  explicitly unestablished. No audio or live widget exists.

## Admitted build — O005-LEGA-V101-CH04 — 2026-08-21

- Builder: `scripts/build_unit_reader.py --unit O005-LEGA-V101-CH04`, Pandoc
  3.9.0.2, native MathML for chapter and mastery mathematics.
- QA: `scripts/qa_unit.py --unit O005-LEGA-V101-CH04 --execute-notebook
  --deterministic-build`, exit 0.
- Structural replay: 143 source / 143 target elements, 22 / 22 links, 245
  ordered source TeX occurrences mapped to 258 declared target occurrences,
  and four / four source problems with stable IDs. The 13 additional target
  formulas and every changed source formula are declared in the QA mapping and
  correction ledger.
- Backend: 196 paired segments / 140,847 bytes, SHA-256
  `c89f5eed3bcca294e546447010551abcc2087e1c31b7d3d98ae7f55498c4a295`;
  four complete mastery records / 18,558 bytes, SHA-256
  `799c9ad13c683b2575c7192c95e81dc3144d88061aef57ea173c918a687e9395`.
- Notebook: 20 cells / seven code cells, unique deterministic cell IDs, clean
  stored outputs, NumPy 2.4.4 and Matplotlib 3.10.9. Every assertion passed.
  The notebook checks free-flight range, the corrected gyroscopic integration
  constant, square-stone collision and turning depth, critical-speed domains,
  and jump-length decay. It explicitly distinguishes equation/implementation
  validation from unavailable experimental validation.
- Figure 4.1 is an accessible code-native Indonesian SVG redraw, 3,664 bytes,
  SHA-256
  `bbeb5d0ec62ce85cb1ea336ada8cde15fc55d545373601c2cde963a9af0ddce0`;
  its frozen source and transformation receipt remain bound. Figure 4.2 is a
  byte-identical 9,016-byte source asset, SHA-256
  `e38c1e539565bfab8a128d8269d36b4983d9710b8affe5cc94a29060bed04dc6`.
- Reader: nine payload files / 447,163 bytes excluding the 929-byte manifest;
  258 chapter and 119 mastery MathML nodes; five local dependencies; two
  loaded figures; four localized notes; zero missing dependency, duplicate ID,
  broken internal fragment, token shape, local path, or U+FFFD.
- Reader manifest SHA-256
  `0e9dff17d5f5d9625c16f5e7d62e5d0c84af75757a717e31ce53840e88eaab85`.
  Deterministic double build: ten files including manifest, byte-identical;
  canonical tree SHA-256
  `15f5b87b32ff5afdeaf2dd29cdd80c2f3f8c90b04a2d2ffc079c1ca671d6f1ef`.
- Regression: Chapters 1–3 and Part 2 retained their previously admitted
  deterministic trees after the generic multi-column-array rendering repair.
- Browser visual QA: at 1280×900 the 1,152 px main shell was centered with no
  document overflow; at 390×844 the main shell and chapter were 357.5 px wide
  and centered, with document scroll width equal to client width. Both figures
  loaded with nonzero natural dimensions, their Indonesian captions and
  long-description links were visible, and no console error occurred. Wide
  MathML is contained in keyboard-scrollable formula spans. External-link
  reachability was not tested; no audio or live widget exists.
