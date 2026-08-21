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
- Reader: eight payload files / 217,390 bytes excluding
  `PACKAGE_MANIFEST.tsv`; 14 chapter MathML nodes and 46 mastery MathML nodes;
  no missing local dependency, duplicate ID, broken
  fragment, local profile path, personal-name leak, token shape, or U+FFFD.
- Reader manifest: 820 bytes, SHA-256
  `1ba10f670dab0b4cf78b30ef17e25984f21e486ac95f98db50d5f3d899d96cb9`.
- Deterministic double build: nine files including manifest, byte-identical;
  canonical tree SHA-256
  `29ceb15656b43f45da8b801ccefab60b20a9d4f3d00a55a73dcbdb941770d082`.
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
- fourteen protected TeX occurrences preserved exactly;
- one figure resolved locally with meaningful Indonesian alternative and long
  description;
- eleven scholarly/context links preserved;
- seven source exercises mapped to seven stable problem IDs;
- seven hints, seven checks/final answers, and seven solutions/rubrics;
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
- Reader: eight payload files / 358,661 bytes excluding
  `PACKAGE_MANIFEST.tsv`; 92 chapter MathML nodes, 155 mastery MathML nodes,
  and three local dependency classes; no missing local dependency, duplicate
  ID, broken fragment, raw mastery TeX, local profile path, personal-name leak,
  token shape, or U+FFFD.
- Reader manifest: 822 bytes, SHA-256
  `5296b09661d64f4c33aaaa4736404f0d87eb5ea4bc51e5e8660719607da2dace`.
- Deterministic double build: nine files including manifest, byte-identical;
  canonical tree SHA-256
  `b0f14a66e0a4e3ed39c79e39daa3ee3b46a6b5af75bb1856247caf4aca0c05b2`.
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
