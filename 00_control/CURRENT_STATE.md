# Current State — O005/C120

Updated: 2026-08-22 Europe/Berlin

## Status

Lega Pressbooks v1.01 is selected and admitted. Source selection is closed.
The official PDF and EPUB are frozen locally, and the coordinator's complete
22-record semantic snapshot and 45-asset manifest have been copied verbatim
into this lane. Chapters 1–8 and the visible Part 2–4 introductions are
translated, built, and verified. Production now moves to Chapter 9,
Pressbooks record 196, *Diffusion*, as `O005-LEGA-V101-CH09`; its exact
authority record and three-asset closure are frozen. The next visible source
item is Chapter 10, record 194, *Pattern Formation*.

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
- Reader package: eight payload files / 217,520 bytes, excluding the manifest;
  manifest SHA-256
  `8c94a298617a14de7af3bda5e7b07831c6cc1cd2b050529fa339eb818cd72942`.
- Exact structure replay: 120/120 elements, 14/14 links, 14/14 TeX
  expressions, seven/seven problems; no unexplained drift.
- Notebook: all seven code cells executed with the pinned environment; all
  deterministic numerical/model-selection assertions passed.
- The generic reader renders 14 chapter and 46 mastery MathML nodes. Repeated
  clean builds were byte-identical across nine files, canonical tree SHA-256
  `3dcbcf930f3b21eaa55f1277bccbd00ae60b6b910af3509260b3438cdc5b4dd1`.
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
- Reader package: eight payload files / 358,791 bytes, excluding the manifest;
  manifest SHA-256
  `5189b7f1280718e3773f0abe8d895f5cc10c574c08986c9a5500ccbd936fde50`.
- Exact structure replay: 103/103 elements, 10/10 links, 92/92 protected
  TeX expressions, and seven/seven problems; no unexplained drift.
- Notebook: all seven code cells and 23 assertions passed with fixed seed
  `20260821`; the baseline produced a 15-seat median width and measured speed
  20 seats/second with regression R-squared 1.0.
- Repeated clean builds were byte-identical across nine files, canonical tree
  SHA-256 `5cb3fd2ed90f1841e8dd8da0e93613b6d1ba8fb442c79cc49a8ff4c508dfa9b4`.
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
- Reader package: four payload files / 11,218 bytes, excluding the manifest;
  manifest SHA-256
  `e9a1ddbe2b77d428782ade23a239b9216ea3f8383290f4ddcf1fb505b5301c2b`.
- Exact replay: zero/zero source-target elements, links, formulas, and
  problems; three/three paragraph boundaries and segment hashes exact.
- Repeated clean builds were byte-identical across five files, canonical tree
  SHA-256 `32b5dcf0c5dd9a8b73b3518c6e2bb7383942130b5787228b650e16cfe02b75d9`.
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
- Reader package: 16 payload files / 2,025,462 bytes, excluding the 1,670-byte
  manifest; manifest SHA-256
  `c062741f4df7d28ed1b57ac16390e3f2754dec627ed39f760b82a47a7ca29d87`.
- Exact structure replay: 423/423 elements, 62/62 links, 404 source TeX
  occurrences mapped to 407 declared target occurrences, and 23/23 stable
  problems; no unexplained drift.
- Notebook: 13 cells / seven code cells / 19 assertions. NumPy 2.4.4,
  SciPy 1.17.1, and Matplotlib 3.10.9 executed successfully; conservative
  energy drift was `1.943e-15`, the damped energy never increased, and the
  dissipation-balance error was `1.559e-05`.
- Reader renders 408 chapter MathML nodes and 455 mastery MathML nodes, resolves
  all nine figures and the notebook/lock locally, and exposes all three
  footnotes as Indonesian notes. Repeated clean builds were byte-identical
  across 17 files, canonical tree SHA-256
  `f485e128318733f43fe967c165d30d3045219a161a776976c729663a57c152b2`.
  Final-byte structural, locality, responsive-CSS, and accessibility checks
  pass; bounded browser evidence and its explicit limits are in `BUILD_QA.md`.

## Admitted Chapter 4 boundary

- Source record: Pressbooks chapter 39, *Stone-Skipping*; target title
  *Pemantulan Batu di Permukaan Air*; modified `2026-03-19T21:51:57Z`.
- Canonical record: 71,697 bytes, SHA-256
  `a1a31a51f76e7b4f74b8ed302b112acaad6bd87b0b9b5cb134676c5205b03e55`;
  raw source fragment: 31,497 bytes, SHA-256
  `21b06c068a09c580d89f6a7bf71b770535f2fd9446fc1d42921e5aaaa9babbbf`.
- Scope: 4,492 source words, 143 elements, 22 links, 245 protected TeX
  occurrences, four problems, four footnotes, and two figures.
- Complete natural id-ID fragment: 32,476 bytes, SHA-256
  `4d19140e14d182466a049ce376ce3168b6d6230adcec80fd136d24c0cc05010b`.
- Accessible independent Figure 4.1 SVG redraw: 3,664 bytes, SHA-256
  `bbeb5d0ec62ce85cb1ea336ada8cde15fc55d545373601c2cde963a9af0ddce0`;
  Figure 4.2 retains the frozen 9,016-byte source asset, SHA-256
  `e38c1e539565bfab8a128d8269d36b4983d9710b8affe5cc94a29060bed04dc6`.
- Four-record mastery layer: 18,558 bytes, SHA-256
  `799c9ad13c683b2575c7192c95e81dc3144d88061aef57ea173c918a687e9395`.
- Independent open stone-skipping notebook: 23,390 bytes, SHA-256
  `49e68c250f6c4e9d6b612b11be86ed8030ce1aa483081cafb08c6ca535418b5e`;
  pinned environment lock: 262 bytes, SHA-256
  `a6a514bccd39c4c2b817b4faf284ef7f1adb9e31593649a76fa6ca3239af6f9e`.
- Modular segment layer: 196 records / 140,847 bytes, SHA-256
  `c89f5eed3bcca294e546447010551abcc2087e1c31b7d3d98ae7f55498c4a295`.
- Exact replay: 143/143 elements, 22/22 links, 245 source TeX occurrences
  mapped to 258 declared target occurrences, and four/four stable problems.
  All mathematical interventions are enumerated as O005-CORR-0018 through
  O005-CORR-0024 in `SOURCE_CORRECTIONS.csv`.
- Notebook: 20 cells / seven code cells, all assertions passing under NumPy
  2.4.4 and Matplotlib 3.10.9. It checks the free-flight, gyroscopic,
  collision-depth, critical-speed, and jump-decay equations, while explicitly
  making no experimental-validation claim.
- Reader package: nine payload files / 447,218 bytes excluding its manifest;
  manifest SHA-256
  `830384e8d193c40911d3bc520e7d2bf18fc60b8608f7893349832a0dd6e0f363`.
  It renders 258 chapter and 119 mastery MathML nodes and resolves all local
  dependencies. Repeated clean builds were byte-identical across ten files,
  canonical tree SHA-256
  `12309752f9ba8f8c79918bc528cd884e1a99e28bf181a3b5a5bd37de2ef6cd52`.
- Browser QA: at 1280×900 the 1,152 px main shell was centered; at 390×844
  the chapter was 357.5 px wide and centered. Document scroll width equaled
  client width at both sizes; both figures loaded at natural resolution,
  long-description links were present, and the browser reported no console
  error. Wide MathML remains locally horizontally scrollable by design.
- Published production commit:
  `184f3df2ece1d6b44b2f0fd852ca86c3511ae642` on `origin/main`. Remote-head
  equality passed. GitHub raw-byte readback matched the local hashes for the
  target content, reader index, package manifest, notebook, and Figure 4.1 SVG.

## Admitted Part 3 introduction boundary

- Source record: visible Pressbooks part 40, *Population Dynamics and
  Epidemiology*; target title *Dinamika Populasi dan Epidemiologi*; modified
  `2024-06-29T02:57:20Z`.
- Canonical record: 5,758 bytes, SHA-256
  `e0c7435af2c60d11f80eef9924934c335c93100cd86de57170820560797f9576`;
  raw source: 2,478 bytes, SHA-256
  `7ef1dfd5305cebe47e0108b408648a9df618000ba0b3bbe467683e2dc4f4ebd1`.
- Complete natural id-ID fragment: four paragraphs / 2,532 bytes, SHA-256
  `8d40cff6e34bcae42c9ad743d743877ab95c0266fab235b9bfcdfdf9adc87933`;
  the source's single emphasis element and paragraph order are exact.
- Modular segment layer: four records / 6,687 bytes, SHA-256
  `9698e525582f2e412e0e87185cb597ef722d7bb59ed2381e66d5d5b61d31c21b`.
- Reader package: four payload files / 17,018 bytes excluding the manifest;
  manifest SHA-256
  `4c3b585cdcb549809f7caac6648fc515b2f234778504fdecee9e1f820eb04995`.
  Repeated clean builds were byte-identical across five files, canonical tree
  SHA-256
  `660a59f9b8c219334ba2dcbd8823e5264ff84cc286af18ad09f8d6cb4c4035e0`.
- Browser QA: the desktop article was 768 px and centered in a 1,152 px main
  shell at 1280×900; the mobile article was 357.5 px and centered at 390×844.
  Document scroll width equaled client width, all four paragraphs rendered,
  and no console error occurred. This part contains no formula, problem,
  asset, mastery, notebook, audio, or live-widget surface.
- Published production commit:
  `493a70632d4d71d3cb7a0729ba7a169a1b3900e9` on `origin/main`. Remote-head
  equality and GitHub raw-byte readback of content, reader, and manifest passed.

## Admitted Chapter 5 boundary

- Source record: Pressbooks chapter 48, *Single-Species Models*; target title
  *Model Populasi Satu Spesies*; modified `2026-03-27T02:27:32Z`.
- Canonical record: 119,420 bytes, SHA-256
  `7f276a994f78af2af02d5bdd39b9566a50f5e3b09b25351c70cdff50736c66be`;
  raw source fragment: 51,685 bytes, SHA-256
  `476153ddf275a4c6d9f52e4268be21c009da3ba5a4e0b5b15fefc73c32d828f2`.
- Complete natural id-ID fragment: 54,818 bytes, SHA-256
  `8a8a205b1dfac9778c3e8549c036559dae88aff1e5262e9513cc5646d72bff7e`.
- Exact replay: 326 source/target lines, 364 ordered elements, 50 links, 389
  source TeX occurrences mapped to 403 declared target occurrences, seven
  figures, seven descriptions and footnotes, and 17 stable problems. Every
  mathematical or typographic intervention is enumerated as O005-CORR-0025
  through O005-CORR-0045.
- Seventeen-record mastery layer: 59,424 bytes, SHA-256
  `d85cda9304f74e5f5d3ff874b37044e18068a9446bf6a3cd4682831bc8c45cc6`;
  17 hints/checks and 12 worked solutions plus five qualitative rubrics.
- Independent open single-species notebook: 19,847 bytes, SHA-256
  `b7a19523b1fedc344a1cda20cca0a8cfb8a46588f05ff7f59417fa59cfd9c7cd`;
  16 cells / seven code cells / 40 assertions. The official 100-row Census
  packet is 8,148 bytes, SHA-256
  `f59dbd91b2bf975df7b7fb4af6de52dc3c68a705632e83d60410d98781206f09`.
- Three figures have self-contained Indonesian-label SVG adaptations; four
  reader figures retain the source raster. All seven display at native size,
  centered, without avoidable enlargement.
- Modular segment layer: 473 records / 292,942 bytes, SHA-256
  `32732105bb934be792de3749e7ede0cf2cdd617126fab6efeddd9468d096dd9f`.
- Reader package: 16 payload files / 968,497 bytes excluding its manifest;
  manifest SHA-256
  `de862361118699c3c398145bf2424d43a6f39610ad3c409c484aad19c506c30d`.
  Repeated clean builds were byte-identical across 17 files, canonical tree
  SHA-256 `16ec1089ec9abccc946cf5970a7d9a51e45855cce4036cea2f05b15329f1fc5e`.
- Browser QA: desktop main shell 1,152 px and chapter 768 px, both centered;
  mobile shell/chapter 357.5 px at 390×844. Navigation wraps on mobile,
  document overflow is zero, seven figures load at native dimensions, all 67
  IDs are unique, all fragment links resolve, and a fresh load has no browser
  warning or error. Wide MathML remains locally scrollable by design.
- Published production commit:
  `400908debd1bc013b0fef5d6d7e20996523fc099` on `origin/main`. Remote-head
  equality passed. Eleven public GitHub raw-byte comparisons matched the local
  byte counts and SHA-256 hashes, covering chapter source, reader, manifest,
  notebook, Census data, localized SVG, mastery, unit metadata, shared CSS,
  and representative earlier-reader reflow outputs.

## Admitted Chapter 6 boundary

- Source record: Pressbooks chapter 53, *Two-Species Models*; target title
  *Model Populasi Dua Spesies*; modified `2026-03-27T02:30:16Z`.
- Canonical record: 63,377 bytes, SHA-256
  `cdcc1c12fc5c0245ffbb94c6cfdc706570f50540bb6719d78e1391f282b114de`;
  raw source fragment: 27,114 bytes, SHA-256
  `d9e372db30a8afbae16bdc43f03fa486035c87deb5f8db774ae2e671d6594938`.
- Complete natural id-ID fragment: 29,882 bytes, SHA-256
  `67e09680f3a67626a2a6761dd4376202985d87a06bdea72dbbd59978b9b08564`.
- Exact replay: 182 / 182 source-target lines, 185 / 185 ordered elements,
  31 / 31 links, 227 source TeX occurrences mapped to 237 declared target
  occurrences, four / four figures, three / three footnotes, and six / six
  stable problems. Every intervention is enumerated as O005-CORR-0046–0063.
- Six-record mastery layer: 24,865 bytes, SHA-256
  `898e4b224ca73073a20a8fb87021d305d00be53f43729eb10d9717cc39dba1b4`;
  six hints/checks and five worked solutions plus one qualitative rubric.
- Independent open two-species notebook: 23,030 bytes, SHA-256
  `2bb805326ad45bfb90a914dbd2eb12b5a579e63d0cb60cdce8f4f6c8928eb33a`;
  14 cells / six code cells / 49 assertions. Locked execution passed under
  Python 3.13.9, NumPy 2.4.4, SciPy 1.17.1, and Matplotlib 3.10.9.
- Four source figures are retained byte-for-byte. Modular segment layer: 211
  records / 137,097 bytes, SHA-256
  `f6e18702e5d7c5ed521a487b5439d888f942b052fda194cbc16217feacc0eecf`.
- Reader package: 11 payload files / 1,460,989 bytes excluding its manifest;
  manifest SHA-256
  `7a5b5b3d80871ba4f1411fd693a2cb351befa7bab8c0cda11c55999585605b44`.
  A final deterministic double build was byte-identical across 12 files,
  canonical tree SHA-256
  `f18df68aa2462a496b8cca2eb3c85ddb9e7a421924819cdeff9c1316a635c1cc`.
- Browser QA: at 1280×900 the main shell was 1,152 px and the chapter 768 px,
  exactly centered; at 390×844 the chapter was 357.5 px and centered. Page
  overflow was zero, all four images loaded without enlargement, all 34 IDs
  were unique, every fragment resolved, and a fresh load had no console warning
  or error. Figure-return links land below the sticky navigation.
- Published production commit:
  `b6155217be51f0bbe6acd67ba1cbafacbe657260` on `origin/main`. Remote-head
  equality passed. Eleven anonymous immutable-commit GitHub raw-byte
  comparisons matched local byte counts and SHA-256 hashes for the target,
  reader, manifest, notebook, source figure, mastery, unit/segment backend,
  shared CSS, Chapter 7 authority, and representative Chapter 5 reflow.

## Admitted Chapter 7 boundary

- Source record: Pressbooks chapter 57, *Epidemiology*; target title
  *Epidemiologi*; modified `2026-03-19T20:23:36Z`.
- Canonical record: 48,627 bytes, SHA-256
  `dcf828ca5ce0c58ced8eb5203dfd1b5a949bd6af3b9c000017a6dd133bb58d2f`;
  raw source: 20,928 bytes, SHA-256
  `027493e86a470e8573d48833b41e4bc365910b255bd7324f1d7ae3272d17c38c`.
- Complete natural id-ID fragment: 22,380 bytes, SHA-256
  `a7ea1f78c96dbdc24694bd376413e8d675e96899849f4ff2887c3c7a825918c1`.
- Exact replay: 123 / 123 source-target lines, 126 / 126 ordered elements,
  29 / 29 links, 150 source TeX occurrences mapped to 160 declared target
  occurrences, three / three figures, one / one footnote, and five / five
  stable problems. Every intervention is enumerated as O005-CORR-0064–0080.
- Five-record mastery layer: 19,470 bytes, SHA-256
  `d4e6d41a84fd2615af02e599df9ebcca1fd40a7b47152159ac501a5064785eed`;
  each problem has a hint, answer check, and worked solution or explicit
  reference closure.
- Independent epidemiology notebook: 23,599 bytes, SHA-256
  `92a9cf27d48d5e7766881592095f1232cc4d2357ee5d0a46bdb871591afafce4`;
  14 cells / six code cells / 42 assertions. Locked execution passed under
  Python 3.13.9, NumPy 2.4.4, SciPy 1.17.1, and Matplotlib 3.10.9.
- Three frozen source phase portraits are retained byte-for-byte. Modular
  segment layer: 162 records / 106,058 bytes, SHA-256
  `57e00551fd14bc85e072def42da47c12ad7ade11a3445578a16a303d96903e7f`.
- Reader package: ten payload files / 1,188,206 bytes excluding its manifest;
  manifest SHA-256
  `3db70ad91f0c0e1d5ffbe4ce0aed504f8fca516f03da216629fa4a15576feed1`.
  A final deterministic double build was byte-identical across 11 files,
  canonical tree SHA-256
  `c5a308a88ba224e05416d4dc5d59219d3dcafa57a5623dbd16e253d5c3822011`.
- Browser QA: at 1280×900 the main shell was 1,152 px and the article 768 px,
  exactly centered; at 390×844 the shell/article was 357.5 px and centered.
  Document overflow was zero, all three 1,024 px rasters loaded responsively,
  their transparent canvases rendered white so black equations and axes stayed
  legible, all 30 IDs were unique, all 34 fragment links resolved, the Figure
  7.3 return target landed below the sticky navigation, and browser logs were
  empty. External-link reachability was not tested; no audio/live widget exists.
- Published production commit:
  `ade2b69bdc07a1ca665de50494b969b221559c0b` on `origin/main`. Remote-head
  equality passed. Anonymous immutable-commit readback covered all 58 changed
  files / 2,573,920 bytes; every filename, byte count, and SHA-256 matched the
  committed local artifact.

## Admitted Part 4 introduction boundary

- Pressbooks part 58, *Chemical Reactions and Spatial Effects*; modified
  `2026-03-17T22:14:18Z`. Canonical record: 6,589 bytes, SHA-256
  `75d370fb729c39ba436eb1a91f5876291ef4c0487235b968d8a0a0002481f232`;
  raw source: 2,907 bytes, SHA-256
  `959b11175f0a5a913275f40058ae06a81e757ceab01aa54dbd63712d7d95d320`.
- Scope: seven raw lines, six ordered opening elements, eleven TeX occurrences,
  and no link, asset, footnote, figure, problem, mastery, or notebook surface.
  Direct UTF-8 inspection proves the raw source's disputed spacing before
  “reaction-diffusion” is valid U+00A0, with zero U+FFFD; it is not a defect.
- Complete natural id-ID fragment: four paragraphs / 3,109 bytes, SHA-256
  `79c8943cf558b0d1fe485b0765ef8def9c970703d5f80a7f18c04c66c8f60a25`.
  Independent review found no semantic omission or addition; all six emphasis
  nodes and all eleven formulas preserve their exact order and payload.
- Modular segment layer: four records / 7,692 bytes, SHA-256
  `41d626f76bac4b0087399f82bc9a4b52b0de0322e9147001ddfc5aa6b09a3b88`.
- Reader package: four payload files / 21,506 bytes excluding its 397-byte
  manifest; manifest SHA-256
  `9e58ce41950ccea4c052c223888b27eed3c933deaacf90c4c1f39cc8e1992790`.
  Repeated builds were byte-identical across five files, canonical tree
  SHA-256 `04ea86d82fadf03fe68f476b7284e8b320987ad7a2c908254f520d3fba48284e`.
- Browser QA: desktop main/article widths were 1,152 / 768 px and centered at
  1280×900; mobile shell/article width was 357.5 px and centered at 390×844.
  Document overflow was zero, four paragraphs and eleven MathML nodes rendered,
  all three IDs were unique, both fragment links resolved, and logs were empty.
- Published production commit:
  `a21eeb7bb5f092042ab0e726a263788dca0ce14a` on `origin/main`. Remote-head
  equality passed. Anonymous immutable-commit readback covered all 27 changed
  files / 793,229 bytes with zero byte-count or SHA-256 mismatches.

## Admitted Chapter 8 boundary

- Pressbooks chapter 62, *Chemical Reactions*; modified
  `2026-03-24T21:29:34Z`. Canonical record: 60,372 bytes, SHA-256
  `1c9f5f1ec75756f23720a3ef5d278302de0957347a59dde6f8021d3a970d7656`;
  raw source: 25,702 bytes, SHA-256
  `d822c7b12a1f859ad3218ab7c6dc5f80f47e0e6f9115ef82544cdb08393e6830`.
- Scope: 216 raw lines, 179 ordered elements, 28 hrefs, 186 TeX occurrences,
  three figures, six footnotes, and thirteen problems. The three primary source
  rasters are frozen byte-for-byte; exact hashes are in the unit authority.
- Complete natural id-ID target: 26,145 bytes, SHA-256
  `49a6be865bf34fac62b832b7d2338982595c48e1ff5c1e0389e626b197659e0a`.
  Exact replay preserves 179 / 179 elements, 28 / 28 links, 186 / 186 TeX
  occurrences, three / three figures, six / six footnotes, and thirteen /
  thirteen stable problems across 217 paired segments. The internally
  consistent source anchor `Orgonator` remains intact.
- Complete thirteen-record mastery layer: 49,712 bytes, SHA-256
  `f244ce8bc66e7fd8bb5fb62af32a95bbff0093741148c528a6b5514d1a12c0fa`;
  twelve records have worked solutions and one has an explicit qualitative
  rubric. Independent review repaired one provenance leak, removed an
  inaccurate SymPy dependency claim, and qualified the hyperbolic-cycle return
  criterion.
- Independent open chemical-reactions notebook: 33,424 bytes, SHA-256
  `8cbc3faa8d63683d15ac4498d2c7249763622789988df9e5684250fef1f74a5b`;
  16 cells / seven code cells / 99 static assertion sites. Fresh locked
  execution under Python 3.13.9, NumPy 2.4.4, SciPy 1.17.1, and Matplotlib
  3.10.9 reached 226 successful dynamic assertion evaluations and independently
  verified conservation laws, Brusselator/Oregonator bifurcation diagnostics,
  Poincare returns, and the Lotka–Volterra invariant.
- Reader package: ten payload files / 972,822 bytes excluding its 1,058-byte
  manifest; manifest SHA-256
  `1302a06298f3434e5e9f1b503fa602c05ce46b201e4e724f7a4c3fcaeb276275`.
  It renders 186 chapter and 321 mastery MathML nodes and resolves six local
  dependencies. Repeated builds were byte-identical across eleven files,
  canonical tree SHA-256
  `313c59b2b4dcafd7a5b4336ad8b9f8105afb8eb0641e478350fc43f41fa0591f`.
- Browser QA: desktop main/article widths were 1,152 / 768 px and centered at
  1280×900; mobile shell/article width was 357.5 px and centered at 390×844.
  Document overflow was zero, all three 1,024 px rasters loaded responsively on
  opaque white canvases, all 45 IDs were unique, every fragment resolved, all
  39 disclosure widgets rendered, and the Problem 13 target landed at 80.08 px
  below the 45.05 px sticky navigation. External-link reachability was not
  tested; no audio/live widget exists. The final warning/error console log was
  empty.
- Published production commit:
  `a3a1e1412a45b199b4b8e5dd22da352486991037` on `origin/main`. Remote-head
  equality passed. Anonymous immutable-commit readback covered all 43 changed
  files / 2,369,575 bytes with zero byte-count or SHA-256 mismatches; the
  ordered inventory SHA-256 is
  `a1b5285726f9fa6325432afe7363de65b2e9f621d678619d44418e4c5e561c77`.

## Frozen Chapter 9 boundary

- Pressbooks chapter 196, *Diffusion*; modified
  `2026-03-19T20:10:36Z`. Canonical record: 65,160 bytes, SHA-256
  `e53b35acf85334d2df48124211843b08b7ca1e9e9ca8c91465f215dfbb219c2a`;
  raw source: 27,486 bytes, SHA-256
  `84fe10d60eaacdb18efb97d52035e3f6e923012c7041e7b3d037b866e90af442`.
- Scope: 172 raw lines, 166 ordered opening/void elements, 27 hrefs, 213 TeX
  occurrences, three figures, five footnotes, and seven problems. All three
  frozen rasters match the authority manifest byte-for-byte.
- The bounded primary-byte audit identifies explicit algebraic, probabilistic,
  traveling-wave, flux, markup, figure-description, and bibliographic repairs
  for the correction ledger. The open companion is one deterministic
  NumPy/SciPy/Matplotlib notebook covering a two-dimensional random walk and
  Fisher–KPP phase portraits at c=1, 2, and 3. Next source item: Chapter 10
  record 194, *Pattern Formation*.

## Next action

Complete Chapter 9 record 196, *Diffusion*, in source order as
`O005-LEGA-V101-CH09`, preserving 172 raw lines, 166 ordered opening/void
elements, 27 hrefs, 213 TeX occurrences, three source figures, five footnotes,
and seven stable problems. Add complete mastery and one independently authored
random-walk/Fisher–KPP notebook, ledger every correction, then build, execute,
inspect, and publish the verified boundary without a confirmation pause.
