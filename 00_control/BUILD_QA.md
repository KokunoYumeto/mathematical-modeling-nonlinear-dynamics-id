# Build and QA Log — O005/C120

## Admitted build — O005-LEGA-V101-CH01 — 2026-08-21

- Builder: `scripts/build_ch01_reader.py`, Pandoc 3.9.0.2, native MathML.
- QA: `scripts/qa_ch01.py --execute-notebook --deterministic-build`, exit 0.
- Structural replay: 120 source / 120 target elements; ordered tags exact;
  attributes exact after only the localized image source/alt and seven stable
  problem IDs; 14 hrefs and 14 protected TeX expressions exact and ordered.
- Backend: 125 paired translation segments and seven complete mastery records;
  every segment text hash and every unit component hash replayed.
- Notebook: 12 cells / seven code cells; clean stored outputs; fixed seed
  `20260821`; NumPy 2.4.4, SciPy 1.17.1, Matplotlib 3.10.9; every cell and all
  numerical, parameter-recovery, model-selection, and reproducibility
  assertions passed under the existing Miniconda environment.
- Reader: eight payload files / 189,708 bytes excluding
  `PACKAGE_MANIFEST.tsv`; no missing local dependency, duplicate ID, broken
  fragment, local profile path, personal-name leak, token shape, or U+FFFD.
- Reader manifest: 820 bytes, SHA-256
  `124a67a728f9d6b1d6425c1199b9545c6804d5b06f6d0dff6acb425458fe39d4`.
- Deterministic double build: nine files including manifest, byte-identical;
  canonical tree SHA-256
  `175ae18c0e8b2a0d41a75887ebb271127691ca8324f655129d49fe0528d6edad`.
- Browser visual QA: at 1280×720 the main shell was 1,152 px and centered,
  article 768 px and centered, with zero horizontal overflow; at 390×844 the
  article was 357.5 px wide with zero overflow. Header, notice, objectives,
  figure, native MathML, and disclosure styling were inspected in dark mode.
- External scholarly/news link reachability was not tested. No audio or live
  widget exists in this unit; none was exercised.

## Standing unit gates

Required Chapter 1 gates:

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
