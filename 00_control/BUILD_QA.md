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

## Admitted build — O005-LEGA-V101-PT03 — 2026-08-21

- Builder: `scripts/build_unit_reader.py --unit O005-LEGA-V101-PT03`, Pandoc
  3.9.0.2; no mathematics conversion was applicable.
- QA: `scripts/qa_unit.py --unit O005-LEGA-V101-PT03
  --deterministic-build`, exit 0.
- Structural replay: four / four ordered paragraph units and one / one
  emphasis element; zero href, TeX, footnote, caption, or problem surface.
- Backend: four paired segments / 6,687 bytes, SHA-256
  `9698e525582f2e412e0e87185cb597ef722d7bb59ed2381e66d5d5b61d31c21b`;
  unit type `part`; mastery, notebook, and asset fields correctly absent.
- Reader: four payload files / 16,945 bytes excluding the 397-byte manifest;
  one local CSS dependency; zero missing dependency, duplicate ID, broken
  internal fragment, token shape, local path, or U+FFFD.
- Reader manifest SHA-256
  `c91ad40bb3914221338e29e4302a018297466cdb72cc021a81af18fe4d74ecc9`.
  Deterministic double build: five files including manifest, byte-identical;
  canonical tree SHA-256
  `778bad58be64f29210f7e7b507f539fdad5365689c609a94f57d3680acb68204`.
- Browser visual QA: desktop 1,152 px centered main shell and 768 px centered
  article at 1280×900; mobile 357.5 px centered shell/article at 390×844;
  document scroll width equaled client width at both sizes, all four
  paragraphs rendered, and no console error occurred. External source-link
  reachability was not tested. No audio, live widget, formula, mastery,
  notebook, or figure exists in this unit.

## Admitted build — O005-LEGA-V101-CH05 — 2026-08-21

- Builder: `scripts/build_unit_reader.py --unit O005-LEGA-V101-CH05`, Pandoc
  3.9.0.2, native MathML for chapter and mastery mathematics.
- QA: `scripts/qa_unit.py --unit O005-LEGA-V101-CH05 --execute-notebook
  --deterministic-build`, exit 0.
- Structural replay: 326 / 326 source-target lines, 364 / 364 ordered
  elements, 50 / 50 links, 389 source TeX occurrences mapped to 403 declared
  target occurrences, seven / seven figures, and 17 / 17 source problems with
  stable IDs. The declared corrections are O005-CORR-0025–0045.
- Backend: 473 paired segments / 292,942 bytes, SHA-256
  `32732105bb934be792de3749e7ede0cf2cdd617126fab6efeddd9468d096dd9f`;
  17 complete mastery records / 59,424 bytes, SHA-256
  `d85cda9304f74e5f5d3ff874b37044e18068a9446bf6a3cd4682831bc8c45cc6`.
- Notebook: 16 cells / seven code cells / 40 assertions, unique deterministic
  cell IDs, clean stored outputs, NumPy 2.4.4, SciPy 1.17.1, and Matplotlib
  3.10.9. Period-1/2/4/8 attractors, Lyapunov exponents, exact ODE checks,
  stage-projection spectral radius, LPA nonnegativity, and Census fits passed.
  The exact local 100-row Census packet and its provenance were hash-verified;
  execution performs no network fetch.
- Reader: 16 payload files / 968,497 bytes excluding the 1,670-byte manifest;
  403 chapter and 310 mastery MathML nodes; 12 local dependencies; seven
  loaded figures; seven localized notes; zero missing dependency, duplicate
  ID, broken internal fragment, raw mastery TeX, token shape, local path, or
  U+FFFD.
- Figures 5.1, 5.2, and 5.7 use separately provenanced self-contained SVG
  label adaptations. All seven reader figures render at their intrinsic width
  rather than being enlarged. Reader manifest SHA-256
  `de862361118699c3c398145bf2424d43a6f39610ad3c409c484aad19c506c30d`.
- Deterministic double build: 17 files including manifest, byte-identical;
  canonical tree SHA-256
  `16ec1089ec9abccc946cf5970a7d9a51e45855cce4036cea2f05b15329f1fc5e`.
- Browser visual QA against the final bytes: at 1280×720 the main shell was
  1,152 px and the chapter 768 px, both centered; at 390×844 the shell and
  chapter were 357.5 px and centered. Document scroll width equaled client
  width at both sizes. The six-link navigation wrapped to three mobile rows
  without horizontal scrolling, all seven images loaded at native dimensions,
  all 67 IDs were unique, and every local fragment resolved. A fresh local
  load contained no script and reported no browser warning or error. Wide
  MathML surfaces remain locally horizontally scrollable by design.
- External-link reachability was not tested. No audio or live widget exists in
  this unit; none was exercised.

## Reader-style reflow migration — all completed units — 2026-08-21

The final Chapter 5 browser pass established two additive shared-reader
repairs: do not enlarge source figures beyond their intrinsic width, and wrap
the navigation links on narrow screens instead of requiring a page-level
horizontal strip. The six earlier completed readers were rebuilt from the
same final `source/reader/reader.css` (4,706 bytes, SHA-256
`281dd35fe70a01f037ee5f30fb87dfd2a5167d912dba1dbf5832bc198fe17e1a`).
The builder also now writes unit-record JSON with explicit LF line endings;
all seven unit records were normalized so clean builds are not host-newline
dependent. No source translation, segment, mastery, notebook, or asset bytes
changed.

| Unit | Payload bytes | Package-manifest SHA-256 | Deterministic tree SHA-256 |
|---|---:|---|---|
| O005-LEGA-V101-CH01 | 217,520 | `8c94a298617a14de7af3bda5e7b07831c6cc1cd2b050529fa339eb818cd72942` | `3dcbcf930f3b21eaa55f1277bccbd00ae60b6b910af3509260b3438cdc5b4dd1` |
| O005-LEGA-V101-CH02 | 358,791 | `5189b7f1280718e3773f0abe8d895f5cc10c574c08986c9a5500ccbd936fde50` | `5cb3fd2ed90f1841e8dd8da0e93613b6d1ba8fb442c79cc49a8ff4c508dfa9b4` |
| O005-LEGA-V101-PT02 | 11,218 | `e9a1ddbe2b77d428782ade23a239b9216ea3f8383290f4ddcf1fb505b5301c2b` | `32b5dcf0c5dd9a8b73b3518c6e2bb7383942130b5787228b650e16cfe02b75d9` |
| O005-LEGA-V101-CH03 | 2,025,462 | `c062741f4df7d28ed1b57ac16390e3f2754dec627ed39f760b82a47a7ca29d87` | `f485e128318733f43fe967c165d30d3045219a161a776976c729663a57c152b2` |
| O005-LEGA-V101-CH04 | 447,218 | `830384e8d193c40911d3bc520e7d2bf18fc60b8608f7893349832a0dd6e0f363` | `12309752f9ba8f8c79918bc528cd884e1a99e28bf181a3b5a5bd37de2ef6cd52` |
| O005-LEGA-V101-PT03 | 17,018 | `4c3b585cdcb549809f7caac6648fc515b2f234778504fdecee9e1f820eb04995` | `660a59f9b8c219334ba2dcbd8823e5264ff84cc286af18ad09f8d6cb4c4035e0` |

Each unit's structure/backend/locality QA and deterministic two-build replay
passed after migration. A single bounded browser sweep then loaded all seven
completed units at 1280×720 and 390×844. Every desktop main shell was 1,152 px
and every article 768 px; every mobile shell/article was 357.5 px. All were
centered within 0.1 px, document overflow was zero, mobile navigation wrapped
without overflow, all 20 reader images loaded, no image was enlarged beyond
its intrinsic width, and the fresh sweep reported no script, warning, or
error. Notebook execution was not repeated because notebook bytes and
computation code were unchanged; Chapter 5's notebook was executed in the
immediately preceding full QA run.

## Public readback — Chapter 5 and reader reflow — 2026-08-21

- Production commit: `400908debd1bc013b0fef5d6d7e20996523fc099`.
- `git push origin main` advanced the public branch from `4d3267f` to
  `400908d`; `git ls-remote origin refs/heads/main` returned the exact local
  40-character commit.
- Eleven files were fetched as anonymous public raw bytes from the immutable
  commit URL and compared in memory with their committed local counterparts.
  Every byte count and SHA-256 matched: Chapter 5 source HTML; final reader
  HTML; package manifest; notebook; official Census packet; localized Figure
  5.1 SVG; mastery JSON; unit JSON; shared reader CSS; Chapter 3's copied CSS;
  and the Part 3 package manifest.
- Key public hashes: source HTML
  `8a8a205b1dfac9778c3e8549c036559dae88aff1e5262e9513cc5646d72bff7e`;
  reader HTML
  `3b5014740c73daf8db9f0a6eef66a9c8f9146c2eb0f8e970b1e010befbb67b30`;
  package manifest
  `de862361118699c3c398145bf2424d43a6f39610ad3c409c484aad19c506c30d`;
  notebook
  `b7a19523b1fedc344a1cda20cca0a8cfb8a46588f05ff7f59417fa59cfd9c7cd`;
  and Census packet
  `f59dbd91b2bf975df7b7fb4af6de52dc3c68a705632e83d60410d98781206f09`.

## Admitted build — O005-LEGA-V101-CH06 — 2026-08-22

- Builder: `scripts/build_unit_reader.py --unit O005-LEGA-V101-CH06`, Pandoc
  3.9.0.2, native MathML for chapter and mastery mathematics.
- Final QA: `scripts/qa_unit.py --unit O005-LEGA-V101-CH06
  --execute-notebook --deterministic-build`, exit 0 after the final shared-CSS
  anchor-offset change.
- Structural replay: 182 / 182 source-target lines, 185 / 185 ordered
  elements, 31 / 31 links, 227 source TeX occurrences mapped to 237 declared
  target occurrences, four / four figures, three / three footnotes, and six /
  six stable problems. The declared corrections are O005-CORR-0046–0063.
- Backend: 211 paired segments / 137,097 bytes, SHA-256
  `f6e18702e5d7c5ed521a487b5439d888f942b052fda194cbc16217feacc0eecf`;
  six complete mastery records / 24,865 bytes, SHA-256
  `898e4b224ca73073a20a8fb87021d305d00be53f43729eb10d9717cc39dba1b4`.
- Notebook: 14 cells / six code cells / 49 assertions, unique deterministic
  cell IDs, clean stored outputs, Python 3.13.9, NumPy 2.4.4, SciPy 1.17.1,
  and Matplotlib 3.10.9. The damped predator–prey convergence error was
  `9.360e-05`, the Lotka–Volterra invariant drift was `8.260e-14`, and every
  equilibrium, discriminant, stability, scaling, and exercise assertion
  passed.
- Reader: 11 payload files / 1,460,989 bytes excluding the 1,177-byte
  manifest; 237 chapter and 212 mastery MathML nodes; seven local
  dependencies; four loaded figures; three localized notes; zero missing
  dependency, duplicate ID, broken fragment, raw mastery TeX, token-shape,
  local-path, privacy, or U+FFFD failure. Both source MathWorks links resolve
  to the packaged open notebook download.
- Reader manifest SHA-256
  `7a5b5b3d80871ba4f1411fd693a2cb351befa7bab8c0cda11c55999585605b44`.
  Final deterministic double build: 12 files including manifest,
  byte-identical; canonical tree SHA-256
  `f18df68aa2462a496b8cca2eb3c85ddb9e7a421924819cdeff9c1316a635c1cc`.
- Browser visual QA against the final bytes: at 1280×900 the 1,152 px main
  shell and 768 px article were centered; at 390×844 the article was 357.5 px
  wide and centered. Document scroll width equaled client width at both sizes,
  all four 1,024 px source images loaded without enlargement, all 34 IDs were
  unique, every local fragment and notebook path resolved, the corrected
  Figure 6.4 return target landed below the sticky navigation, and a fresh
  load reported no console warning or error. External-link reachability was
  not tested. No audio or live widget exists in this unit.

## Anchor-offset propagation — all completed units — 2026-08-22

The Chapter 6 accessibility pass added `scroll-margin-top: 5rem` to identifier
targets so internal links remain visible below the sticky reader navigation.
The final shared stylesheet is 4,740 bytes, SHA-256
`855b0177868a8c3d32ceffee55adfa8f738f8b2116581ca460acaa3e734789ee`.
The same 34-byte deterministic stylesheet delta was copied into every earlier
completed reader and each package manifest was regenerated. Source prose,
segments, unit metadata, mastery, notebooks, data, and figures did not change.

| Unit | Payload bytes | Package-manifest SHA-256 | Current tree SHA-256 |
|---|---:|---|---|
| O005-LEGA-V101-CH01 | 217,554 | `b82e8dae5e73a781b6c40706941f7f80bb514896a82950c14949429f9b96d34b` | `2135e8df21f041d681495ea9a9a98143f8a7b62f4c92d85dcfe3edd5746ba067` |
| O005-LEGA-V101-CH02 | 358,825 | `4fe0544da0dde86f57949af81ef74911df6bebb624d521a80d3702be58f14ce6` | `492056a253392e7eca9705a1c868cee45a79aea0a2eb4031df46578ff5dcfd1f` |
| O005-LEGA-V101-PT02 | 11,252 | `a07846e34797e4c67bdc9c53684a3487ee00c587086df57f81d80a65ad4a5201` | `f3247eab331bf1fbb87d784c61e1ecfdb702e5bd47830b22924dace3d1601ee2` |
| O005-LEGA-V101-CH03 | 2,025,496 | `fc204f5ede1f1115a401dc7045eebd7534fb67fd8c8d5ebb11750a7fae1fbb59` | `1d94c1bb7616fdb1206a190a78cead3c7f4436705e77285dd1c30e1228d34ce0` |
| O005-LEGA-V101-CH04 | 447,252 | `c4a4885af7751e2bcfdac61e41ba9c57c5f61c21b4b2a311c9037490057a2854` | `4bcb8fea4e833ff0e0fff5a29416ab209a44149c073a082cfee6eeaacd03940b` |
| O005-LEGA-V101-PT03 | 17,052 | `1132d5446df024c6ff82986f94dcd82dc2b4e2c4f2c149b4d158a48e6423e6fa` | `7843ce0c7a21f0756d825b4eeae21c0c2a2cae25a3d1cfd1a082d30c4db6a4e3` |
| O005-LEGA-V101-CH05 | 968,531 | `6f925f90dbf7305b1d7f6819eb28708ba1bf12bde9cef9b0cedb97d9582b448e` | `fa35cf796e2a4cda18f8b2c0b9798266c70eabe487be8144461f3b4f872f8f0a` |
| O005-LEGA-V101-CH06 | 1,460,989 | `7a5b5b3d80871ba4f1411fd693a2cb351befa7bab8c0cda11c55999585605b44` | `f18df68aa2462a496b8cca2eb3c85ddb9e7a421924819cdeff9c1316a635c1cc` |

The structure/backend/locality QA command returned exit 0 for all seven
earlier units after propagation. Chapter 6 then passed a fresh complete
notebook-executing deterministic double build. Its desktop/mobile browser pass
validated the visible anchor behavior on the final stylesheet bytes.

## Public readback — Chapter 6 and anchor-offset propagation — 2026-08-22

- Production commit: `b6155217be51f0bbe6acd67ba1cbafacbe657260`.
- `git push origin main` advanced the public branch from `77154cb` to
  `b615521`; `git ls-remote origin refs/heads/main` returned the exact local
  40-character commit.
- Eleven files were fetched anonymously from the immutable GitHub raw URL and
  compared in memory with their committed local counterparts. Every byte count
  and SHA-256 matched: Chapter 6 source HTML; reader HTML; package manifest;
  notebook; a source figure; mastery JSON; unit JSON; segment JSONL; shared
  reader CSS; the frozen Chapter 7 authority manifest; and Chapter 5's updated
  package manifest.
- Key public hashes: source HTML
  `67e09680f3a67626a2a6761dd4376202985d87a06bdea72dbbd59978b9b08564`;
  reader HTML
  `af00599bb9b30e09795640c243274bada010481fadbb8ead284d32c12851473d`;
  package manifest
  `7a5b5b3d80871ba4f1411fd693a2cb351befa7bab8c0cda11c55999585605b44`;
  notebook
  `2bb805326ad45bfb90a914dbd2eb12b5a579e63d0cb60cdce8f4f6c8928eb33a`;
  and shared CSS
  `855b0177868a8c3d32ceffee55adfa8f738f8b2116581ca460acaa3e734789ee`.

## Admitted build — O005-LEGA-V101-CH07 — 2026-08-22

- Builder: `scripts/build_unit_reader.py --unit O005-LEGA-V101-CH07`, Pandoc
  3.9.0.2, native MathML for chapter and mastery mathematics.
- Final QA: `scripts/qa_unit.py --unit O005-LEGA-V101-CH07
  --execute-notebook --deterministic-build`, exit 0 after the white scientific-
  figure canvas repair.
- Structural replay: 123 / 123 source-target lines, 126 / 126 ordered
  elements, 29 / 29 links, 150 source TeX occurrences mapped to 160 declared
  target occurrences, three / three figures, one / one footnote, and five /
  five stable problems. Declared interventions are O005-CORR-0064–0080.
- Backend: 162 paired segments / 106,058 bytes, SHA-256
  `57e00551fd14bc85e072def42da47c12ad7ade11a3445578a16a303d96903e7f`;
  five complete mastery records / 19,470 bytes, SHA-256
  `d4e6d41a84fd2615af02e599df9ebcca1fd40a7b47152159ac501a5064785eed`.
- Notebook: 14 cells / six code cells / 42 assertions, unique deterministic
  cell IDs and clean stored outputs. Python 3.13.9, NumPy 2.4.4, SciPy 1.17.1,
  and Matplotlib 3.10.9 executed successfully with the Agg backend. Viral and
  endemic equilibria, local eigenvalues, classic-SIR invariants/final sizes,
  threshold cases, and the explicitly added MSEIR population-balance closure
  all passed.
- Reader: ten payload files / 1,188,206 bytes excluding the 1,035-byte
  manifest; 160 chapter and 151 mastery MathML nodes; six local dependencies;
  three loaded figures; one localized note; zero missing dependency, duplicate
  ID, broken fragment, raw mastery TeX, token-shape, local-path, privacy, or
  U+FFFD failure.
- Reader manifest SHA-256
  `3db70ad91f0c0e1d5ffbe4ce0aed504f8fca516f03da216629fa4a15576feed1`.
  Final deterministic double build: 11 files including manifest,
  byte-identical; canonical tree SHA-256
  `c5a308a88ba224e05416d4dc5d59219d3dcafa57a5623dbd16e253d5c3822011`.
- Browser visual QA against the final bytes: at 1280×900 the main shell was
  1,152 px and the article 768 px, both centered; at 390×844 the shell/article
  was 357.5 px and centered. Document scroll width equaled client width, all
  three 1,024 px rasters loaded responsively with an opaque white canvas, all
  30 IDs were unique, all 34 fragment links resolved, and the Figure 7.3 return
  target landed 79.97 px below the top against a 45.05 px sticky navigation.
  Browser logs were empty. External-link reachability was not tested; no audio
  or live widget exists.

## Scientific-figure canvas propagation — all completed units — 2026-08-22

Chapter 7 exposed a shared dark-theme defect: transparent source rasters with
black equations and axis labels inherited the reader's dark background, making
their margins unreadable. The generic figure-image rule now supplies a white
canvas. Final shared CSS is 4,760 bytes, SHA-256
`dbcefe88c42a8cf49df285682124fa86010c6621faf9b82ec7be5c324625a0a5`.
The exact 20-byte change was copied into every earlier completed reader and
each package manifest regenerated; source prose, mathematics, segments,
mastery, notebooks, data, and figures did not change.

| Unit | Payload bytes | Package-manifest SHA-256 | Current tree SHA-256 |
|---|---:|---|---|
| O005-LEGA-V101-CH01 | 217,574 | `57c36f76beb9103f37bf352b03618764297497f2ff242bdf1826c95f29962910` | `753ccc07a6b6d999868befe65c562684c076d3031cccc17fbdaf302d966de097` |
| O005-LEGA-V101-CH02 | 358,845 | `4326d84165451af8281e4ebbeaf9ae7f886d14b25160e05c6cebf68fcdedc81f` | `e57091cdc7cc973569b57c18ee77cae3b672987f0195e31d57ecda27e4b59b61` |
| O005-LEGA-V101-PT02 | 11,272 | `dabde43f8d08b87e180a678b13f352bc29cea8158c50139bd20ef83cadf11ee1` | `389c6f8f17e675a1a71d19f67634b2d7885d0e652f331f60f236b27ccfc7b851` |
| O005-LEGA-V101-CH03 | 2,025,516 | `aae42b82ed66defe9ca7c741f548d528f4809ac522d3998e66853de773eac071` | `52d03ce3523f45b181fb089e2519eae5f30817a71e636037093f7df9e2611739` |
| O005-LEGA-V101-CH04 | 447,272 | `d5f3d23ae55a2036227575e38a3b84cb575dd38f32ee497e3445dd88bdff8181` | `194e3f0bbb034087e21bd48ead7dfcd046c9e6072385b2d115957ba869fb9451` |
| O005-LEGA-V101-PT03 | 17,072 | `420acb90f6e882533916d201c95e6caf441463e190d44968293bac57ba4ff18b` | `29a20b059617c2f6184357c341ed595f9471e545bfa7fc0aa76f810a6823ebb6` |
| O005-LEGA-V101-CH05 | 968,551 | `ef76221c7c0f89c90f3d3dfb416f9c82e16a93886ea42f4e24a6b9beee313525` | `e931b31a5ed2d9adc634089fca4aa495b235c65fb88164461048a181069e7e0f` |
| O005-LEGA-V101-CH06 | 1,461,009 | `3b317bf8da9e47c46fab03537496df7db27fb0ae81beae787f696ffb4381fe2e` | `879007befcf0a2908dfce14bcea55c4d20904c1d07f9bb79ab57d4631bd505ef` |

Each earlier unit passed a deterministic, non-notebook-executing structure,
backend, locality, accessibility, and package regression after propagation.
Chapter 7 then passed the complete notebook-executing deterministic gate and
the bounded desktop/mobile browser inspection on the same final CSS bytes.

## Public readback — Chapter 7 and figure-canvas propagation — 2026-08-22

- Production commit: `ade2b69bdc07a1ca665de50494b969b221559c0b`.
- `git push origin main` advanced the public branch from `74af9fe` to
  `ade2b69`; `git ls-remote origin refs/heads/main` returned the exact local
  40-character commit.
- Every one of the 58 files changed by the production commit was fetched as
  anonymous bytes from its immutable GitHub raw URL and compared with the
  committed local counterpart: 2,573,920 local bytes, 2,573,920 public bytes,
  and zero byte-count or SHA-256 mismatches.
- The ordered `path<TAB>bytes<TAB>sha256` public inventory has SHA-256
  `8dde382d77db97cbde208752600293f63c574c866f52bd6088e0eb725d5a8606`.
  Coverage includes Chapter 7 source fragments/assets, target, segments,
  mastery, unit record, notebook/lock, complete reader package, pipeline and
  controls; all eight earlier stylesheet/manifest pairs; and the complete
  frozen Part 4 authority record.

## Admitted build — O005-LEGA-V101-PT04 — 2026-08-22

- Before translation, strict UTF-8 code-point enumeration corrected an audit
  error: the character before the emphasized source term “reaction-diffusion”
  is one valid U+00A0 nonbreaking space, not U+FFFD. Both frozen source forms
  contain zero U+FFFD. No invented source correction was applied.
- Builder: `scripts/build_unit_reader.py --unit O005-LEGA-V101-PT04`, Pandoc
  3.9.0.2, native MathML for all eleven formulas.
- QA: `scripts/qa_unit.py --unit O005-LEGA-V101-PT04
  --deterministic-build`, exit 0. Exact replay covers four / four paragraphs,
  six / six ordered emphasis elements, zero / zero links, eleven / eleven TeX
  occurrences, and zero problems/footnotes/assets.
- Independent translation review found natural, complete Indonesian with no
  semantic omission/addition and exact ordered TeX/emphasis preservation.
- Backend: four paired segments / 7,692 bytes, SHA-256
  `41d626f76bac4b0087399f82bc9a4b52b0de0322e9147001ddfc5aa6b09a3b88`;
  mastery and notebook fields are correctly absent rather than dummy records.
- Reader: four payload files / 21,506 bytes excluding the 397-byte manifest;
  eleven chapter MathML nodes and one local CSS dependency; zero missing
  dependency, duplicate ID, broken fragment, token-shape, local-path, privacy,
  or U+FFFD failure. Manifest SHA-256
  `9e58ce41950ccea4c052c223888b27eed3c933deaacf90c4c1f39cc8e1992790`.
- Deterministic double build: five files including manifest, byte-identical;
  canonical tree SHA-256
  `04ea86d82fadf03fe68f476b7284e8b320987ad7a2c908254f520d3fba48284e`.
- Browser visual QA against final bytes: at 1280×900 the 1,152 px main shell
  and 768 px article were centered; at 390×844 the shell/article was 357.5 px
  and centered. Document scroll width equaled client width, all four paragraphs,
  six emphasis spans, and eleven formulas rendered, all three IDs were unique,
  both local fragments resolved, and browser logs were empty. No audio, live
  widget, figure, or external-link reachability test was applicable.

## Public readback — Part 4 and Chapter 8 authority — 2026-08-22

- Production commit: `a21eeb7bb5f092042ab0e726a263788dca0ce14a`.
- `git push origin main` advanced the public branch from `baff434` to
  `a21eeb7`; remote-head equality passed.
- All 27 changed files were fetched anonymously from immutable GitHub raw URLs
  and compared with committed local counterparts: 793,229 local bytes, 793,229
  public bytes, zero byte-count mismatches, and zero SHA-256 mismatches.
- The ordered `path<TAB>bytes<TAB>sha256` public inventory has SHA-256
  `d52b0b8b21296e8899faa1d3efd633a7760e4f769df2d5c81c37656d13a089bb`.
  Coverage includes the complete Part 4 target/backend/reader, corrected
  code-point provenance, pipeline and cursor controls, and all seven Chapter 8
  authority files including its three source rasters.

## Admitted build — O005-LEGA-V101-CH08 — 2026-08-22

- Builder: `scripts/build_unit_reader.py --unit O005-LEGA-V101-CH08`, Pandoc
  3.9.0.2, native MathML for chapter and mastery mathematics.
- Final gate: `scripts/qa_unit.py --unit O005-LEGA-V101-CH08
  --execute-notebook --deterministic-build`, exit 0. Exact replay covers 179 /
  179 ordered elements, 28 / 28 links, 186 / 186 TeX occurrences, three /
  three figures, six / six footnotes, and thirteen / thirteen problems.
- Target: 26,145 bytes, SHA-256
  `49a6be865bf34fac62b832b7d2338982595c48e1ff5c1e0389e626b197659e0a`.
  Backend: 217 paired segments / 134,156 bytes, SHA-256
  `09725f630eb53b477329baf3a4d8c5a08605496e70fae0c113544bd81f146631`;
  thirteen mastery records / 49,712 bytes, SHA-256
  `f244ce8bc66e7fd8bb5fb62af32a95bbff0093741148c528a6b5514d1a12c0fa`.
- Independent notebook: 16 cells / seven code cells, 33,424 bytes, SHA-256
  `8cbc3faa8d63683d15ac4498d2c7249763622789988df9e5684250fef1f74a5b`.
  Fresh execution under Python 3.13.9, NumPy 2.4.4, SciPy 1.17.1, and
  Matplotlib 3.10.9 passed all 99 static assertion sites (226 successful
  dynamic evaluations) in 6.314 seconds. Independent recomputation confirmed
  the mass-action conservation basis, Brusselator Hopf and repeated-eigenvalue
  cases, Oregonator Hopf threshold and attracting cycle, Poincare returns, and
  distinct Lotka–Volterra invariants.
- Reader: ten payload files / 972,822 bytes excluding the 1,058-byte manifest;
  186 chapter and 321 mastery MathML nodes; six local dependencies; three
  loaded figures. Manifest SHA-256
  `1302a06298f3434e5e9f1b503fa602c05ce46b201e4e724f7a4c3fcaeb276275`.
  Deterministic double build: eleven files, byte-identical, canonical tree
  SHA-256 `313c59b2b4dcafd7a5b4336ad8b9f8105afb8eb0641e478350fc43f41fa0591f`.
- Independent mastery review found three issues and all were repaired before
  the final build: source/new-original attribution for Problem 8, an inaccurate
  SymPy dependency claim, and an overgeneralized hyperbolic return criterion.
  Independent notebook review found no remaining actionable issue.
- Browser visual QA against final bytes: at 1280×900 the main shell / article
  widths were 1,152 / 768 px and centered; at 390×844 the shell / article was
  357.5 px and centered. Scroll width equaled client width; all three 1,024 px
  rasters loaded responsively on opaque white canvases; all 45 IDs were unique;
  every local fragment resolved; 39 disclosures rendered; the Problem 13
  target landed at 80.08 px below the 45.05 px sticky navigation; and the final
  warning/error console log was empty. External-link reachability was not
  tested and no audio/live widget exists.
- Every earlier completed unit (CH01, CH02, PT02, CH03, CH04, PT03, CH05,
  CH06, CH07, and PT04) passed a fresh deterministic structure/backend/locality/
  accessibility/package regression after the Chapter 8 pipeline additions.

## Public readback — Chapter 8 and Chapter 9 authority — 2026-08-22

- Production commit: `a3a1e1412a45b199b4b8e5dd22da352486991037`.
- `git push origin main` advanced the public branch from `57e9565` to
  `a3a1e14`; `git ls-remote origin refs/heads/main` returned the exact local
  40-character commit.
- All 43 changed files were fetched anonymously from immutable GitHub raw URLs
  and compared with committed local counterparts: 2,369,575 local bytes,
  2,369,575 public bytes, zero byte-count mismatches, and zero SHA-256
  mismatches.
- The ordered `path<TAB>bytes<TAB>sha256` public inventory has SHA-256
  `a1b5285726f9fa6325432afe7363de65b2e9f621d678619d44418e4c5e561c77`.
  Coverage includes the complete Chapter 8 translation, assets, notebook,
  mastery/backend, reader package, correction/terminology records, pipeline,
  reader-facing status and recovery controls, plus the complete frozen Chapter
  9 authority record and its three source rasters.

## Admitted build — O005-LEGA-V101-CH09 — 2026-08-22

- Builder: `scripts/build_unit_reader.py --unit O005-LEGA-V101-CH09`, Pandoc
  3.9.0.2, native MathML for chapter and mastery mathematics. The builder
  losslessly normalizes the frozen source's one crossing footnote-span pair and
  one one-word bibliography anchor before rendering and segment pairing; the
  target authoring HTML itself is balanced and descriptive.
- Final gate: `scripts/qa_unit.py --unit O005-LEGA-V101-CH09
  --execute-notebook --deterministic-build`, exit 0. Exact replay covers 166 /
  166 ordered elements, 27 / 27 links, 213 source TeX occurrences mapped to
  214 target occurrences, three / three figures, five / five footnotes, and
  seven / seven stable problems.
- Target: 29,698 bytes, SHA-256
  `0b4633d88a3aed144738429bccc466f1d3f472714bbeb57e0ddb338cdab329e4`.
  Backend: 228 paired segments / 145,487 bytes, SHA-256
  `fb0b37030cf91b8eef4c1d0d751d3f8d190dabdc74b14222db79dda55002081f`;
  seven mastery records / 28,465 bytes, SHA-256
  `9b5beba72aae6132d7bce4a72ca36041caee499b27cd93806b96694804c1b1fc`.
- Independent open diffusion notebook: 10 cells / four code cells / 73 static
  assertion sites, 23,561 bytes, SHA-256
  `bbc57501bb83e4195e1c65ad30bd235c67aa1342028aa6a323207ec66101ec97`.
  Fresh locked execution passed 123 dynamic evaluations. Independent review
  found no executable, dependency, provenance, determinism, or numerical
  issue; alternate integrations reproduced the c=1 sign changes and the
  monotone nonnegative c=2 and c=3 profiles.
- Reader: ten payload files / 724,082 bytes excluding the 1,071-byte manifest;
  214 chapter and 189 mastery MathML nodes; six local dependencies; three
  loaded figures. Manifest SHA-256
  `f7b3bdf67c22956f80e6e94d6a968aca4932e450615e3ffb4fba4d6e9b3836d3`.
  Deterministic double build: eleven files, byte-identical, canonical tree
  SHA-256 `8a9a1e68ec70673f2d14a5622d26088a64ca38452ec153f3622b9482488ab7cc`.
- Independent translation review's two final findings were repaired: the
  Fisher publisher statement now identifies the agreeing party as the chapter
  author, and the Müller DOI anchor contains the complete article title.
  Independent mastery review's four residual English *front* terms were
  replaced with the controlled Indonesian *muka gelombang* terminology.
- Browser visual QA against final bytes: at 1280×900 the main shell / article
  widths were 1,152 / 768 px and centered; at 390×844 the shell/article was
  357.5 px and centered. Document scroll width equaled client width; the three
  figures loaded responsively at intrinsic 300×261, 3087×2329, and 3087×2288;
  all 38 IDs were unique; all 33 fragment links resolved; 21 mastery
  disclosures and five complete notes rendered; the Problem 7 target landed
  at 79.86 px below the 70.60 px sticky navigation; and a fresh load had no
  warning or error. External-link reachability was not tested and no
  audio/live widget exists.
- Every earlier completed unit (CH01, CH02, PT02, CH03, CH04, PT03, CH05,
  CH06, CH07, PT04, and CH08) passed a fresh structure/backend/locality/
  accessibility/package regression after the Chapter 9 pipeline additions.

## Public readback — Chapter 9 — 2026-08-22

- Production commit: `cbfde5f97e1d79cddbd2fb729a028adf13d5994b`.
- `git push origin main` advanced the public branch from `ae85a3f` to
  `cbfde5f`; `git ls-remote origin refs/heads/main` returned the exact local
  40-character production commit.
- Every one of the 35 files changed by the production commit was fetched as
  anonymous bytes from its immutable GitHub raw URL and compared with the
  committed local counterpart: 1,548,116 local bytes, 1,548,116 public bytes,
  zero byte-count mismatches, and zero SHA-256 mismatches.
- The ordered `path<TAB>bytes<TAB>sha256` public inventory has SHA-256
  `f3a45caf82be33b8c5d0c9af4c86b2d4eb4c977d441036ec01b63a6f7e1ec12f`.
  Coverage includes the complete Chapter 9 translation, source fragments,
  assets, notebook/lock, mastery/backend, reader package, pipeline, status,
  correction/terminology records, and recovery controls.

## Admitted build — O005-LEGA-V101-CH10 — 2026-08-22

- Final gate: `scripts/qa_unit.py --unit O005-LEGA-V101-CH10
  --execute-notebook --deterministic-build`, exit 0. Exact replay covers
  116 / 116 ordered elements, 24 / 24 links, 77 source TeX occurrences mapped
  to 78 declared target occurrences, three / three figures, thirteen / thirteen
  footnotes, and six / six stable problems.
- Target: 20,027 bytes, SHA-256
  `0c951f1e8dd251be396e437660a6a610bfe28a2b6aeb4f18cd45882f38df18f3`;
  backend: 149 segments / 96,796 bytes, SHA-256
  `6adc788295e1edd7399946d386708c9520633424e4fade643b6f7492f3af14da`;
  mastery: six records / 25,321 bytes, SHA-256
  `3130aaa0d8efd70f2fc90c4c0568268579cbe05634b8a3abbc29d90b158fb257`.
- Notebook: ten cells / four code cells, 36,507 bytes, SHA-256
  `95a6aadcb565f6b78542065520e6bc5ee775387dd21b1a31b3de2b5cfc0dab50`.
  Fresh execution under Python 3.13.9, NumPy 2.4.4, SciPy 1.17.1, and
  Matplotlib 3.10.9 passed; two independent clean executions produced stable
  stdout, numerical-array hashes, and three rendered-figure hashes.
- Reader: eleven payload files / 403,280 bytes excluding its 1,177-byte
  manifest; 78 chapter and 203 mastery MathML nodes; seven local dependencies.
  Manifest SHA-256
  `10086b57c048bc55eafaf431ae7a0e1c88f100542b02d03e965b16330a6ffcf7`.
  The twelve-file deterministic tree SHA-256 is
  `0785c71e3c71ab7021f515c1f489b9c4c5a1ea8f3a9b57b899f3cef531446bde`.
- Browser QA: desktop main/article widths 1,152 / 768 px; mobile 357.5 /
  357.5 px. Both are centered relative to the document client width; page
  overflow is zero. Three images loaded at responsive/intrinsic dimensions,
  all 28 IDs were unique, all 22 fragments resolved, thirteen notes rendered,
  and the Problem 6 anchor cleared the sticky navigation. Logs were empty.
  External-link reachability was not tested; no audio/live widget exists.

## Admitted build — O005-LEGA-V101-PT05 — 2026-08-22

- Final gate: `scripts/qa_unit.py --unit O005-LEGA-V101-PT05
  --deterministic-build`, exit 0. Exact replay covers two / two plain
  paragraphs and zero element, link, math, problem, footnote, or asset surface.
- Target: 492 bytes, SHA-256
  `00fb30fb29d5cbedc669ed8aea8931a455f90e426e51b7ca4191094f33221d65`;
  backend: two segments / 1,843 bytes, SHA-256
  `70d92d69ccb1e53fb1a1a1ad22a6c41d0c036a5bb652e3af52de0193856a97dd`.
- Reader: four payload files / 10,006 bytes excluding its 397-byte manifest;
  manifest SHA-256
  `66ba9c2060abefc13a1bb12406ce978fc3d7dcf49b917916928521aa59f6b1f3`.
  Repeated builds were byte-identical across five files, canonical tree
  SHA-256 `4478e3e6a68aa854c5dbfaaf9011b3326b34bc15e59ea792300dff72f2a8bd17`.
- Independent review found a complete natural two-paragraph translation with
  all Chapter 11–14 references intact. Browser QA found centered 768 px and
  357.5 px articles at 1280×900 and 390×844, zero overflow, three unique IDs,
  two intact fragment links, and empty logs. Mastery/notebook execution and
  external-link reachability were inapplicable; no audio/live widget exists.

## Public readback — Chapter 10, Part 5, and Chapter 11 authority — 2026-08-22

- Production commit: `0302eef818b06dafa372b2ab5cd5ff784b6eb184`.
- `git push origin main` advanced the public branch from `05c8f93` to
  `0302eef`; `git ls-remote origin refs/heads/main` returned the exact local
  40-character commit.
- Every one of the 61 files changed by the production commit was fetched as
  anonymous bytes from its immutable GitHub raw URL and compared with the
  committed local counterpart: 1,366,211 local bytes, 1,366,211 public bytes,
  zero byte-count mismatches, and zero SHA-256 mismatches.
- The ordered `path<TAB>bytes<TAB>sha256` inventory has SHA-256
  `c8c095a643dae69fc354c031b30812ef799fb5c874b1a73fb0fe84c0f57821dc`.
  Coverage includes the complete Chapter 10 authority/translation/assets/
  mastery/notebook/backend/reader, the complete Part 5 authority/translation/
  backend/reader, Chapter 11's frozen canonical/raw/rendered authority, and all
  changed pipeline and durable control files.
