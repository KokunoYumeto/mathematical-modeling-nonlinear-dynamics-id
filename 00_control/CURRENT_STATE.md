# Current State — O005/C120

Updated: 2026-08-23 Europe/Berlin

## Current status override — 2026-08-23

The complete 26-unit reader is finished, QA-verified, and preserved in
canonical Zenodo record `22070943` / DOI `10.5281/zenodo.22070943`. The
historical progress paragraphs below are retained as provenance; this override
supersedes their earlier "three bridge modules remain" wording. The current
closure is 3,448 source segments + 657 bridge segments = 4,105 total, with
141 mastery records, 26 notebooks, and 12 projects. Figshare remains an
external account blocker and GitHub remains suspended; neither changes the
completed reader or its public Zenodo preservation.

## Status

Lega Pressbooks v1.01 is selected and admitted. Source selection is closed.
The official PDF and EPUB are frozen locally, and the coordinator's complete
22-record semantic snapshot and 45-asset manifest have been copied verbatim
into this lane. All 22 source-derived semantic records—front matter, all five
visible part introductions, Chapters 1–14, and both back-matter records—are
translated, built, reviewed, and verified. Chapter 14,
Pressbooks record 555, is admitted as `O005-LEGA-V101-CH14`, *Proyek
Pemodelan*, with all twelve independent open project packets. The
source-derived translation is therefore closed. Original bridge C1 is now
complete and verified; three declared bridge modules remain before the edition
is complete.

The complete Chapter 14 boundary and sanitized Zenodo preservation receipt are
sealed in local commit `555062f9ef9942c2c3167a15e59e81b5f87ab0ea`
(132 files / 1,323,634 bytes). Its reproducible inventory SHA-256 is
`73cc49bba0c35598002408d0b30ece20fe7bcfc98d8221ae54afe400c1ba73a6`,
computed from UTF-8, no-BOM, LF-terminated, headerless, ordinal-path-sorted
`path<TAB>bytes<TAB>sha256` rows. Its parent is the complete Chapter 13 commit
`a8f3357043a5483efcacca76cf886ad75269a58d`, whose parent is the Chapter 12 and
Chapter 13-authority commit `d3363f6b3612b3beef9b235f9b6c134fa0593fc1`.
The last remote attempt, against the previous pending head, was at
`2026-08-22T18:16:05+02:00` and returned GitHub's explicit HTTP 403
account-suspended response. The Chapter 14 commit was deliberately not retried:
The user reports that the suspension followed VPN use and that a support ticket
is open. The exact chain remains push-ready and must be sent unchanged only
after the user reports restored access. Zenodo is the active versioned
preservation surface while the GitHub lineage is temporarily unavailable.

## Frozen Chapter 10 authority

- Record 194, slug `pattern-formation`, modified
  `2026-03-19T20:11:05Z`; the empty record-level license override inherits the
  book's CC BY-NC-SA 4.0 license.
- Canonical record: 49,768 bytes, SHA-256
  `fbabaa5ed87f7b1e1a2a851555b2e0b7b37d3398a6450b67ffb73efcdb614f06`;
  raw content: 19,476 bytes, SHA-256
  `b1daf70ba354c270332d0e0f849c73e165aa84769be71eb15a7594159bfa2367`;
  rendered content: 28,202 bytes, SHA-256
  `ff79a728a7d61bcd33717cdb540dc4f09cc03d6de25d223ac53458ed6bd91108`.
- Exact raw census: 98 physical lines, 116 opening/void elements, 24 `href`
  attributes, 77 TeX slots, three captions, thirteen footnotes, six numbered
  problems, and three source images.
- Frozen figures: 120,120-byte pattern collage
  (`ed55c4ad09e5b4f1746dabf66aa87509538bcf76bcbc442650a4925ea47006ba`),
  59,364-byte Swift–Hohenberg pattern image
  (`f92c04b397d388f84a31737b72dfbfdf89a14df4210e7cbf3c41fcf2f8b8958a`),
  and 8,974-byte growth-rate image
  (`a49ff56eba92cc8f74400b6925443a63a4bcdbe95afd477c51f386f038abf32c`).
- The only named executable surface is the unavailable proprietary MATLAB GUI
  `Patterns`; no code, data, URL, or binary is bundled. Problems 4–6 rely on
  the cited Klausmeier paper, so the independent companion must supply an
  explicitly cited, self-contained equation/scaling card without importing
  proprietary code.

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

## Admitted Chapter 9 boundary

- Pressbooks chapter 196, *Diffusion*; modified
  `2026-03-19T20:10:36Z`. Canonical record: 65,160 bytes, SHA-256
  `e53b35acf85334d2df48124211843b08b7ca1e9e9ca8c91465f215dfbb219c2a`;
  raw source: 27,486 bytes, SHA-256
  `84fe10d60eaacdb18efb97d52035e3f6e923012c7041e7b3d037b866e90af442`.
- Scope: 172 raw lines, 166 ordered opening/void elements, 27 hrefs, 213 TeX
  occurrences, three figures, five footnotes, and seven problems. All three
  frozen rasters match the authority manifest byte-for-byte.
- Complete natural id-ID target: 29,698 bytes, SHA-256
  `0b4633d88a3aed144738429bccc466f1d3f472714bbeb57e0ddb338cdab329e4`.
  Exact replay preserves 166 / 166 ordered elements, 27 / 27 links, 213
  source TeX occurrences mapped to 214 declared target occurrences, three /
  three figures, five / five footnotes, and seven / seven stable problems.
  Corrections O005-CORR-0087–0106 bind every mathematical, bibliographic,
  markup, and accessibility intervention.
- Seven-record mastery layer: 28,465 bytes, SHA-256
  `9b5beba72aae6132d7bce4a72ca36041caee499b27cd93806b96694804c1b1fc`;
  every record has a hint, final-answer check, and worked solution or explicit
  rubric. Independent review corrected four residual English uses of *front*.
- Independent open diffusion notebook: 23,561 bytes, SHA-256
  `bbc57501bb83e4195e1c65ad30bd235c67aa1342028aa6a323207ec66101ec97`;
  10 cells / four code cells / 73 assertion sites. Fresh locked execution under
  Python 3.13.9, NumPy 2.4.4, SciPy 1.17.1, and Matplotlib 3.10.9 passed all
  123 dynamic assertion evaluations. Independent recomputation confirmed the
  random-walk mean-square-displacement law, Fisher–KPP eigenvalues, the
  oscillatory sign-changing profile for c=1, the critical nonnegative profile
  for c=2, and the slow-tail rate for c=3.
- Modular segment layer: 228 records / 145,487 bytes, SHA-256
  `fb0b37030cf91b8eef4c1d0d751d3f8d190dabdc74b14222db79dda55002081f`.
  The builder losslessly normalizes the frozen source's one crossing footnote
  span and one one-word bibliography anchor before pairing; the target and
  final reader retain balanced, descriptive markup.
- Reader package: ten payload files / 724,082 bytes excluding its 1,071-byte
  manifest; manifest SHA-256
  `f7b3bdf67c22956f80e6e94d6a968aca4932e450615e3ffb4fba4d6e9b3836d3`.
  It renders 214 chapter and 189 mastery MathML nodes and resolves all six
  local dependencies. Repeated builds were byte-identical across eleven files,
  canonical tree SHA-256
  `8a9a1e68ec70673f2d14a5622d26088a64ca38452ec153f3622b9482488ab7cc`.
- Independent translation review found two final issues and both were repaired:
  the modern Fisher disclaimer now unambiguously refers to the chapter author,
  and the Müller DOI exposes the complete cited title. Browser QA at 1280×900
  and 390×844 found centered 768 / 357.5 px articles, zero page overflow,
  three loaded responsive figures, 38 unique IDs, no broken fragment, complete
  footnotes, and an empty fresh-load warning/error log. The Problem 7 target
  landed at 79.86 px below the 70.60 px sticky navigation. External-link
  reachability was not tested; no audio/live widget exists.
- Published production commit:
  `cbfde5f97e1d79cddbd2fb729a028adf13d5994b` on `origin/main`. Remote-head
  equality passed. Anonymous immutable-commit readback covered all 35 changed
  files / 1,548,116 bytes with zero byte-count or SHA-256 mismatches; the
  ordered inventory SHA-256 is
  `f3a45caf82be33b8c5d0c9af4c86b2d4eb4c977d441036ec01b63a6f7e1ec12f`.

## Admitted Chapter 10 boundary

- Pressbooks chapter 194, *Pattern Formation*, modified
  `2026-03-19T20:11:05Z`; canonical/raw/rendered hashes remain bound by the
  frozen authority. The 98-line target is 20,027 bytes, SHA-256
  `0c951f1e8dd251be396e437660a6a610bfe28a2b6aeb4f18cd45882f38df18f3`.
- Exact replay preserves 116 / 116 ordered elements, 24 / 24 links, 77 source
  TeX occurrences mapped to 78 declared target occurrences, three / three
  figures, thirteen / thirteen footnotes, and six / six stable problems.
  Backend: 149 paired segments / 96,796 bytes, SHA-256
  `6adc788295e1edd7399946d386708c9520633424e4fade643b6f7492f3af14da`.
- Six-record mastery: 25,321 bytes, SHA-256
  `3130aaa0d8efd70f2fc90c4c0568268579cbe05634b8a3abbc29d90b158fb257`;
  independent review found all six hints, checks, and worked solutions complete
  after the exact Soal 2 uniqueness cases and Soal 5 physical units were made
  explicit. It renders 203 MathML nodes.
- Independent open notebook: ten cells / four code cells, 36,507 bytes,
  SHA-256
  `95a6aadcb565f6b78542065520e6bc5ee775387dd21b1a31b3de2b5cfc0dab50`.
  Two clean executions under the locked Python/NumPy/SciPy/Matplotlib stack
  were deterministic and passed the Swift–Hohenberg branch, finite-box,
  spectral, time-refinement, Klausmeier scaling, equilibrium, Jacobian, and
  dispersion assertions without external-file or network access.
- Figure 10.1 is an independently authored accessible 800×560 SVG, 3,946
  bytes, SHA-256
  `6d416bd0125b06047b352be7b645f58bc1304161290e9177fd16e3c535d6b779`;
  its standalone provenance receipt is 984 bytes, SHA-256
  `d376a0b6bf31a8dd27abe12d2b40669a5533e61baee096e672aeb6f605adcc54`.
- Reader: eleven payload files / 403,280 bytes excluding its 1,177-byte
  manifest; manifest SHA-256
  `10086b57c048bc55eafaf431ae7a0e1c88f100542b02d03e965b16330a6ffcf7`.
  Repeated clean builds were byte-identical across twelve files, canonical tree
  SHA-256 `0785c71e3c71ab7021f515c1f489b9c4c5a1ea8f3a9b57b899f3cef531446bde`.
  Desktop/mobile browser QA found centered 768 / 357.5 px articles, zero page
  overflow, three loaded responsive figures, 28 unique IDs, 22 intact fragment
  links, thirteen notes, and an empty warning/error log; the Problem 6 target
  landed at 80.13 px below the 70.60 px sticky navigation.
- Published in production commit
  `0302eef818b06dafa372b2ab5cd5ff784b6eb184` on `origin/main`; remote-head
  equality and anonymous immutable-commit byte readback passed.

## Admitted Part 5 introduction boundary

- Pressbooks part 409, *Appendices*, modified `2024-07-04T01:20:04Z`;
  canonical record 1,664 bytes, SHA-256
  `ccc3b6a575bf84e7ae94d3b3f5320e59279b088bede008e0e99bb423821a05c8`;
  raw source 510 bytes, SHA-256
  `657289c8fa8b8aeb613fff2d842330b3b769024a17c9609abc0fefab547419c0`.
- Complete two-paragraph natural id-ID target *Lampiran*: 492 bytes, SHA-256
  `00fb30fb29d5cbedc669ed8aea8931a455f90e426e51b7ca4191094f33221d65`.
  Independent review found no omission, addition, or changed Chapter 11–14
  reference. Backend: two paired segments / 1,843 bytes, SHA-256
  `70d92d69ccb1e53fb1a1a1ad22a6c41d0c036a5bb652e3af52de0193856a97dd`.
- Reader: four payload files / 10,006 bytes excluding its 397-byte manifest;
  manifest SHA-256
  `66ba9c2060abefc13a1bb12406ce978fc3d7dcf49b917916928521aa59f6b1f3`.
  Five-file deterministic tree SHA-256
  `4478e3e6a68aa854c5dbfaaf9011b3326b34bc15e59ea792300dff72f2a8bd17`.
  Desktop/mobile inspection found centered 768 / 357.5 px articles, two exact
  paragraphs, zero overflow, three unique IDs, two intact fragment links, and
  no browser warning/error. Mastery, notebook, asset, problem, formula, and
  footnote surfaces are correctly absent.
- Published with Chapter 10 and the frozen Chapter 11 authority in production
  commit `0302eef818b06dafa372b2ab5cd5ff784b6eb184`. Anonymous readback covered all
  61 changed files / 1,366,211 bytes with zero byte-count or SHA-256 mismatch;
  ordered inventory SHA-256
  `c8c095a643dae69fc354c031b30812ef799fb5c874b1a73fb0fe84c0f57821dc`.

## Admitted Chapter 11 boundary

- Pressbooks chapter 410, slug `linear-algebra`, *Refresher: Linear Algebra*,
  modified `2026-03-19T20:11:37Z`; canonical/raw/rendered identities remain
  bound by the frozen authority and no component asset is referenced.
- Complete natural id-ID target *Penyegaran: Aljabar Linear*: 14,293 bytes,
  SHA-256
  `f62354eb267c5788bd0ea8a70d6b7de64f8059c1656eedbffa40898da4c9606d`.
  Exact replay preserves 127 / 127 ordered elements, zero / zero links,
  165 / 165 TeX occurrences, both source equation anchors, and seven / seven
  stable problems across all 166 physical source-order lines.
- Thirteen explicit source corrections, `O005-CORR-0118` through
  `O005-CORR-0130`, repair the vector-space criterion, scalar-field
  qualifications, transpose and cofactor notation, invertibility quantifier,
  generalized-eigenvector definition, algebraic multiplicity statements,
  eigenspace decomposition, localized TeX text, and Problem 7 column arrays.
  Frozen English bytes remain immutable.
- Backend: 142 paired segments / 84,119 bytes, SHA-256
  `0ee5d83a3cd0f9096019e0d7ced962ff8f44b4938a49caea207293dc7dcee289`.
  Seven independently authored mastery records: 22,086 bytes, SHA-256
  `76acebcc58ce8f81d35b933a08e47a5a0eee5a717caa168975ada561f091f56e`;
  all seven exact calculations and proofs passed independent recomputation and
  review. No notebook or asset is applicable.
- Reader: five payload files / 300,247 bytes excluding its 509-byte manifest;
  manifest SHA-256
  `4c2f860ed701af4682ebd7202c9f5a01b6daba8a0e4d8015f97ca450d54c0153`.
  Repeated builds were byte-identical across six files, canonical tree SHA-256
  `4711a2d39c2ce08eb9f7f760ca7b0346451d60496583e09fa72213150ff14da1`.
- Independent translation review and independent mastery review both passed.
  Browser QA found a centered 1,152 px shell and 768 px article at 1280×900;
  at 390×844 the 357.5 px shell/article filled the usable 375 px client width
  and remained centered. Page scroll width equaled client width. All 31
  overwide formula nodes had bounded horizontal-scroll hosts; all 20 reader
  IDs and ten fragment links were intact; 21 disclosures rendered; the final
  problem target cleared the sticky navigation by 35.97 px; and the final
  local page emitted no warning or error. External-link reachability was
  inapplicable, and no audio or live widget exists.
- Published in production commit
  `8ff7758f0afdf66881a7a0552581e1c1668a6860` on `origin/main`. Remote-head
  equality passed, and anonymous immutable-commit readback matched all 32
  changed files / 866,260 bytes with zero mismatch; ordered inventory SHA-256
  `121edbad5bde443b6d01f41c24ed66f3e6d223db21722bdd472f9266801959a8`.

## Admitted Chapter 12 boundary

- Pressbooks chapter 413, slug `appendix-vector-calculus`, *Refresher: Vector
  Calculus*, modified `2026-03-19T19:53:52Z`; the empty record-level license
  override inherits CC BY-NC-SA 4.0 and no component asset is referenced.
- Canonical record: 31,922 bytes, SHA-256
  `fa1364a307b033035bce94975db0667edf3b8d208e73b4e07882b090cafab377`;
  raw content: 14,175 bytes, SHA-256
  `165e0b7a0b489dd9be7ae396ac9a3c0430c89599c23a444fcaadffb2a07a3ccc`;
  rendered content: 15,354 bytes, SHA-256
  `1e6590dd97823f1dc009947eee63585b1e2afcda8dee91b66587e9cded4e0303`.
- Exact frozen census: 112 physical lines, 85 ordered elements, 161 TeX
  occurrences, and zero links, assets, footnotes, or problems.
- Complete natural id-ID target *Penyegaran: Kalkulus Vektor*: 15,288 bytes,
  SHA-256
  `6e0e2d720732726d88e3479d399ee25a4b012a750a4626c2219de9e54baa8f8b`.
  Exact replay preserves 85 / 85 ordered elements and maps 161 source TeX
  occurrences to 165 declared target occurrences. Corrections
  `O005-CORR-0131` through `O005-CORR-0140` bind the four replacements and
  four additive definitions without altering the frozen source.
- Backend: 121 paired segments / 78,475 bytes, SHA-256
  `be1a4ec04a0739dde654f507b7ef9bbf906398b4ae1dcf6c9f03572a15cec34d`;
  unit record: 1,105 bytes, SHA-256
  `044e1b32e3fc16e2418b7ab86015798fdf67b12d51afe7ae6706754876612940`.
- Reader: four payload files / 181,451 bytes excluding its 399-byte manifest;
  manifest SHA-256
  `80eb6c5692d0d01c2fa85de079c32ba9056442455cbd3ed7f3495fb627f67085`.
  Repeated builds were byte-identical across five files, canonical QA tree
  SHA-256 `50d3befe18450e4ab83f1ca57e87703af285429c3957d8cd007f5711704b3fce`.
- Independent translation and mathematics audits passed. The bounded regression
  rebuilt every earlier completed unit successfully. Browser QA found centered
  768 px desktop and 357.5 px mobile articles, zero page overflow, 165 labeled
  MathML nodes, three unique IDs, two intact fragment links, and an unobscured
  `#isi` target. Problems, mastery, notebook, links, assets, images, and
  footnotes are correctly absent.

## Frozen Chapter 13 authority

- Pressbooks chapter 445, slug `appendix-ordinary-differential-equations`,
  *Refresher: Ordinary Differential Equations*, modified
  `2026-03-19T20:12:31Z`; the empty record-level license override inherits
  CC BY-NC-SA 4.0.
- Canonical record: 136,353 bytes, SHA-256
  `4c1d86fe406cb145189312bc82c7c1572632335b2cab0eb29ee6fbfa1fa9a37c`;
  raw content: 59,328 bytes, SHA-256
  `4ef96c2d76484ba271a9e94c524d755806064a97eb051944a958f8e664b6b005`;
  rendered content: 70,793 bytes, SHA-256
  `2aa5153cf1262aecc298ebceffbaa2f447adb3f0701e39c9a7d50e562e280b6a`;
  authority manifest: 2,535 bytes, SHA-256
  `aabc41570d241c58c0c5e195a1db7ab04d5acdfc3039689914777783199b4861`.
- Exact frozen census: 581 physical lines, 456 ordered elements, 524 balanced
  TeX expressions, 39 fragment-only links with no missing target, eight figures
  with eight descriptions, eleven numbered problems, and eleven corresponding
  source answer groups.
- Eight valid primary PNG assets total 284,549 bytes. Their exact paths, EPUB
  members, dimensions, byte counts, and SHA-256 identities are bound in
  `authority/units/O005-LEGA-V101-CH13/AUTHORITY_MANIFEST.json`. The frozen
  rendered witness retains remote responsive `srcset` alternatives; production
  must ship the eight local primary assets and remove remote runtime dependency.

## Admitted Chapter 13 boundary

- Complete natural id-ID target *Penyegaran: Persamaan Diferensial Biasa*:
  61,373 bytes, SHA-256
  `90e45dbcb0e3c95a5f9ca07a1533886c4bee99b71530fe18f7b245a128bcc46b`.
  Exact replay preserves 456 / 456 ordered elements and 39 / 39 links, and maps
  524 source TeX occurrences to 528 declared target occurrences. Corrections
  `O005-CORR-0141`–`0153` bind every mathematical intervention.
- Backend: 546 paired segments / 329,930 bytes, SHA-256
  `d824d63da00be5f49f1d45f0cc6465c80b7e09efb2c106cb546b580a0120acbb`;
  unit record: 3,211 bytes, SHA-256
  `7fd24929fe42d8f6f9961d81a1ec0da876eca0db68d52469c42c2bf2cf050fc1`.
  Eleven independently authored mastery records are 34,275 bytes, SHA-256
  `67965dd1d7e64e66de99b060f1c6be4ee526cd5bd66ffae6a8e2b0be94ff115a`.
- Reader: thirteen payload files / 1,169,623 bytes excluding its 1,385-byte
  manifest; manifest SHA-256
  `995e0f24de41317590468911dbd729f04484b9441baf4954e58af5dd400f78c3`.
  Repeated builds were byte-identical across fourteen files, canonical QA tree
  SHA-256 `78ead87f005d1b4d48fa2a731a1c9287b332e7c288ee14fa2fc84c967e46af4d`.
- Independent translation and mathematical/mastery audits passed after their
  three findings were repaired. Every earlier completed unit, CH01–CH12 and
  PT02–PT05, passed fresh deterministic regression; all ten applicable
  notebooks executed successfully. Browser QA against final bytes found
  centered 768 / 357.5 px articles, zero page overflow, eight loaded local
  figures, 778 labeled MathML nodes, 68 unique IDs, 53 intact fragment links,
  33 working disclosures, and no warning or error.

## Frozen Chapter 14 authority

- Pressbooks chapter 555, slug `examples-of-project-topics`, authoritative
  display title *Modeling Projects*, modified `2026-03-24T21:46:02Z`; the
  empty record-level license override inherits CC BY-NC-SA 4.0.
- Canonical record: 38,887 bytes, SHA-256
  `cb9e10a0a6df089194f2bb90bc335d641230cce00dc47c90b6d1802dd6769013`;
  raw content: 18,737 bytes, SHA-256
  `337ce752f17b70d3677216b114792685a84acded115dfdc06213bb469dd5761a`;
  rendered content: 18,394 bytes, SHA-256
  `3487086799c2562006c975c587dcd61f573f80e0b8f71caa6129dc242c57d0f9`;
  authority manifest: 663 bytes, SHA-256
  `e680688dce94d1ac0e19b43aae3cb9a16bc37c061a352e74dcc6ccc6a7b4ef5e`.
- Frozen EPUB chapter witness: 19,070 bytes, SHA-256
  `e2eb8b494af8fc00d62dc9cbfc73de8f76cf475b9929ff4c570aa838edc41784`;
  its chapter heading and TOC also say *Modeling Projects*. The Indonesian
  display title is therefore *Proyek Pemodelan*; the legacy slug is retained
  only as source identity.
- Exact raw topology: 240 physical lines; one introductory text node; twelve
  project blocks, twelve shaded textboxes, 36 headings, 24 lists, 95 list
  items, 16 unique external links, 52 strong elements, and 17 emphasized
  elements. There are zero exercises, formulas, footnotes, internal anchors,
  figures, descriptions, or semantic media assets.
- Corrections `O005-CORR-0154`–`0160` bind six high-confidence grammar/cross-
  reference repairs and one heading-alignment normalization. The 16 linked
  papers/resources remain external citations and are not redistributed or
  relicensed by this edition.

## Admitted Chapter 14 boundary

- Complete natural id-ID target *Proyek Pemodelan*: 19,110 bytes, SHA-256
  `9a08e5a663685a52c4551a560ee68ea4f4dad9675b3aea04702dfa8416d719b4`.
  Exact replay preserves 252 / 252 ordered elements, 16 / 16 links, all twelve
  project boxes and 95 list items; the unit has no source formula, exercise,
  image, footnote, or internal anchor.
- Backend: 247 paired segments / 135,384 bytes, SHA-256
  `8074b66de970f9381056a7c5c71d9bff2806337813606b7a68bf244305d7ad7f`;
  project catalog: 26,966 bytes, SHA-256
  `9107863aee7cc9013b024e10d0091e227fdd3135b8913f5e103cc1157ce92e56`;
  unit record: 4,492 bytes, SHA-256
  `e11be3dcf3907d84e6fffc9c9a78c7195ca32b517920e3c62a3c2f99d7d5028a`.
- The deterministic generator is 47,402 bytes, SHA-256
  `62eeb904b4c06800f64758454e7a8db78ab89ae4dfb2ff2220e877ca5194f2c5`.
  It produces twelve packet directories / 72 files / 156,596 bytes and twelve
  safe deterministic ZIPs / 72,815 bytes. Repeated generation is byte-identical.
- All twelve output-clean notebooks, 120 cells / 48 code cells, execute with
  the pinned CPython 3.13.9, NumPy 2.4.4, SciPy 1.17.1, and Matplotlib 3.10.9
  stack. Independent audit repaired Project 6 to use dynamically recomputed
  local periodic neighborhoods, verified it over the fixed plus 20 alternate
  seeds, normalized remaining reader-facing terminology, and closed with no
  residual finding.
- Reader: seventeen payload files / 268,890 bytes excluding its 1,878-byte
  manifest; manifest SHA-256
  `1be6f14f57da0ed950fd484c0c7e07291d981e4f4b76b2c8f3be49520507b597`.
  Repeated clean builds are byte-identical across eighteen files, canonical QA
  tree SHA-256
  `da7aa599e38559f33553872f7e1663de6d555ebc478b6b598dc7aa1d4bf6c347`.
- All seventeen earlier units passed deterministic regression; all ten
  applicable earlier notebooks executed. Final browser QA found centered
  desktop/mobile articles and packet panels, zero page overflow, seventeen
  unique IDs, complete fragments, twelve visible downloads, correct sticky-nav
  clearance, and no warning or error.

## Reader-first Zenodo preservation — Chapter 14 progress boundary

- Published record: <https://zenodo.org/records/22061640>; version DOI
  `10.5281/zenodo.22061640`; concept DOI `10.5281/zenodo.22059939`; version
  `v1.01-id-progress-CH14-reader-20260822`.
- Metadata is explicitly in progress, names Joceline Lega as creator, uses
  `ind`, open access, and `cc-by-nc-sa-4.0`, preserves the official source as
  `isDerivedFrom`, and states the change/non-endorsement boundary. TTP occurs
  exactly once as an `Other` contributor and nowhere in the title or
  description. The public description also identifies the production model
  exactly as `OpenAI Codex gpt-5.6-sol, Ultra.` without displacing the creator
  or human-contributor credits.
- The five-file, 48,468,743-byte release begins with a 297-page tagged PDF
  reader, followed by one 387-member compact resumable source ZIP, license,
  release manifest, and checksums. Ordered local/public inventory SHA-256 is
  `444ff63bc66e3c2bff051f8a439c766f315a75e452a60e0286974728708928ff`.
- All five artifacts were downloaded anonymously from the public record and
  matched local filename, byte count, and SHA-256. The PDF readback retained
  297 pages, `/Lang id`, tagged structure, and twenty bookmarks; the ZIP passed
  full CRC and member-count verification.
  The credential-free receipt is
  `00_control/ZENODO_PUBLICATION_RECEIPT_CH14_20260822.json`.

## Figshare metadata preservation — Chapter 14 progress boundary

- The account's complete seven-license list does not contain CC BY-NC-SA 4.0.
  No release byte was therefore uploaded under a false substitute license.
- A fileless CC0 metadata/link item was published as article `33314769`, DOI
  `10.6084/m9.figshare.33314769.v2`, at
  <https://figshare.com/articles/online_resource/Pengantar_Pemodelan_Matematika_Edisi_Bahasa_Indonesia_metadata_/33314769/2>.
  Its description states that CC0 applies only to the metadata, the linked work
  remains CC BY-NC-SA 4.0, and this is an incomplete CH14 checkpoint.
- Anonymous readback found the exact title, Joceline Lega plus the account
  owner as authors, two relevant categories, eight status/subject/license
  keywords, the Zenodo version/concept and official-source references, zero
  files, and zero standalone TTP occurrences. The rendered public page exposes
  no file-download surface. Its metadata contains the exact model identification
  `OpenAI Codex gpt-5.6-sol, Ultra.` and preserves the source and human credits.
- The item is publicly present in project `280296` and in the 21-item
  collection version `10.6084/m9.figshare.c.8668413.v37`. Both DOI redirects
  resolve to the expected immutable version pages. Sanitized receipt:
  `00_control/FIGSHARE_PUBLICATION_RECEIPT_CH14_20260822.json`. The collection
  description explicitly permits truthful link-only records when its platform
  cannot represent the work's exact license.

## Indonesian field-terminology QA — 2026-08-22

- A genuine Indonesian mathematical-modeling witness was frozen from
  arXiv:2001.05854v1: Natanael Karjanto's 94-page bilingual upload contains the
  complete original 47-page Indonesian thesis and downloadable TeX.
- The 144,585-byte official source archive has SHA-256
  `520cd160b47664dda32e57df87a6eb028348154e4d7a7494d230e8e517891d53`;
  the 91,655-byte, 2,076-line Indonesian TeX has SHA-256
  `03f7e68801badc84255df3323078ae00eee7ecff8a9f118cba064ce5d46ff2f2`.
- Direct TeX comparison justified normalization to `syarat batas`, `sistem
  dinamik`, and `matriks Jacobi`; added evidence-backed glossary entries for
  governing equations, boundary-value problems, numerical methods, initial
  guesses, numerical error, convergence, and dispersion relations; retained
  modern `konvergensi` rather than the witness's single dated
  `kekonvergenan`; and documented rather than collapsed the equilibrium/fixed
  point and initial-condition distinctions.
- CH01, CH02, CH04, CH05, CH06, CH07, CH10, and CH13 were regenerated. All
  eight passed structural, backend-binding, local-dependency, and repeated
  byte-identical build QA. No formula, ID, link, problem, or executable code
  topology changed. Full evidence is in
  `00_control/TERMINOLOGY_QA_INDONESIAN_FIELD_SOURCE_20260822.md`.

## Published-checkpoint consistency closure — 2026-08-22

- Historical Zenodo/Figshare QA sections are explicitly marked superseded and
  no longer point to live receipts for later versions.
- The current public builder protects the published CH14 directory and version
  label against mutation, requires a fresh no-overwrite destination, and adds
  the terminology decision plus its bounded witness manifest/license notice to
  future resumable packages. An isolated five-file smoke build passed privacy,
  390-member ZIP closure/CRC, and protected-output refusal checks.
- The exact model identification is one raw README line. Current private
  controls use only the role label `the user`; verbatim historical directives
  and source-author credits remain untouched.

## Complete source-record closure — 2026-08-22

- Front-matter record 22 is admitted as `O005-LEGA-V101-FM01`, *Prakata*.
  The target is 5,633 bytes, SHA-256
  `27f12221c462101e7008cbdd409e7b7fd1bcf99f7aea8d458b2e87efa80c1f56`;
  its seven paired segments are 13,835 bytes, SHA-256
  `9e60af834465dfe1ea7d9e6631288fd963addcc437cbedc42f342d5b3b0a5090`.
  Exact paragraph replay includes the two required signature breaks. The
  five-file deterministic reader tree is
  `ef0e77cf6c674f6b9a88b89fa8a357120a4249681be8c9e312a6b421e1d5c14c`.
- Part 1 record 23 is admitted as `O005-LEGA-V101-PT01`, *Pendahuluan*. The
  target is 738 bytes, SHA-256
  `2922e6de1e5b9287f29283add8cb04be9f469cc67c51b3d42e8b7e365312bcff`;
  its three paired segments have SHA-256
  `64d41bf505e30ee886ccb0abade535554d7322b9b3da4e1f6c8ec81a84126361`.
  The deterministic reader tree is
  `d9029d36333e9a7596cef6aa44dac77e867b55a199c3af6232deaf67d0a14b0d`.
- Back-matter record 767 is admitted as `O005-LEGA-V101-BM01`, *Pernyataan
  Aksesibilitas*. The target is 3,683 bytes, SHA-256
  `e36f9bbc8b4f2506dae31527290aa1e15a4960ab4051bd56b04d0d69a8659ff5`;
  its 28 paired segments have SHA-256
  `230dddbb10c82c99e5782a6010cf72ff3a647a75b3d8ebb02c6f0fa869f289c9`.
  Six links and the reciprocal local footnote targets replay exactly, with no
  broken or duplicate identifier. The deterministic reader tree is
  `733d363f6c1af06623ca4a33bf78be6b2748d5b1e81b2af92f8e7ff3e43ca17c`.
- Back-matter record 771 is admitted as `O005-LEGA-V101-BM02`, *Riwayat
  Versi*. The target is 1,703 bytes, SHA-256
  `7aa3fad37ec153d70335b66eaf81aced827f398d305fd2830af27c84ffc577b3`;
  its ten paired segments have SHA-256
  `1415789dc7e8bb89e6ea88b308235b7be70f2177c1fdd35424ed8f4927f92761`.
  Reader replay has exactly two prose paragraphs, one table, three rows, three
  scoped column headers, and zero empty generated paragraphs. The deterministic
  reader tree is
  `ab0c3fbb16e2a6e9a4a9e7d47211ccd480946407faec337c7d0bb022563439f7`.
- Final browser regression at 1,440 px and 390 px found every one of these four
  articles centered (768 px desktop; 357.507 px mobile), with zero document or
  element overflow and zero runtime console entries. The glossary now contains
  275 unique stable term IDs through `O005-TERM-0275`.
- A final independent fidelity pass then sharpened three bounded renderings:
  spatial extent is `terbentang secara spasial`, successive refinement is
  `secara berulang`, and postgraduate mentors are no longer narrowed to
  postdoctoral mentors. FM01 and PT01 were rebuilt and repeated browser QA
  retained the same centered, overflow-free geometry.
- The source closure is sealed in local commits
  `2574d58777412210f6394b2920508765c1f1dd7f` (58 files / 541,894 bytes,
  changed-path inventory SHA-256
  `b350fc8e44acead9803e417e9d5fbf6681373f7be1031dd24ac78c91b8194d54`)
  and `cc404bd113f5e7af294205c4ad32f59cc0edabba` (20 files / 253,900 bytes,
  changed-path inventory SHA-256
  `7624a19694ea44dba5e02e48656bab04782626c7bf5e15a1b146b2c94098f30d`).
  Neither commit was sent to the suspended GitHub account.

## Admitted original bridge C1 boundary

- `O005-BRIDGE-C1`, *Alur Kerja Python/Jupyter yang Reprodusibel*, is a new
  independent supplement, not source-book content. Its canonical content is
  16,946 bytes, SHA-256
  `c8593b80996e6f7bd368a4a2e198472198163fc17ee408b98ccbd7e58c99e4eb`.
- The seven-record mastery layer is 12,528 bytes, SHA-256
  `8757a13a2c799fe2f13aa697fb4596d4ab623c06688733cb16df39fc151fb27a`.
  The output-clean 14-cell notebook is 14,436 bytes, SHA-256
  `c266a0e332b6d709007344e1d401b8af324744d6ed524e7afa793ba5a01bee02`;
  its complete pinned environment lock is SHA-256
  `5c6816d5c2e5993961f8a21ddce68f7f1ecbb4a48eff04fb345dc8e4ce2a8c68`.
- The stable modular layer has 152 segment records, SHA-256
  `dfd2cb1f671ab3f672e27d7435d92c84b562b30131c14cca00863040749a20b0`,
  bound to the immutable semantic-ID ledger SHA-256
  `8cf00bb705b542fe1f300076824b23a05af3b58188cef6a92fde76ed1521ebbd`.
- Canonical and changed-seed notebooks each passed in a separate fresh kernel
  with one PNG. Two isolated 14-file builds matched each other and every
  canonical byte; final deterministic tree SHA-256 is
  `c169dd1fc53b2b99f3c4a9876553b52403d7b7308669ed7918ce2129b7819d46`.
- Desktop/mobile browser QA proves centered 768 px / 357.507 px articles, zero
  horizontal overflow, valid captions, clean preformatted code, zero empty
  paragraphs or raw TeX, and zero console warnings. The shared renderer repair
  is part of the admitted boundary.
- C1 preserves the exact source-book credit, CC BY-NC-SA 4.0 boundary,
  non-endorsement, and production identification `OpenAI Codex gpt-5.6-sol,
  Ultra.` It imports no proprietary code, external data, or third-party art.

## Next action

Integrate and verify `O005-BRIDGE-C2`, the complete natural id-ID local-
bifurcation unit now present in the source tree, by generalizing the strict
bridge schemas/build/QA without weakening cross-record or fresh-kernel gates.
Then continue in order through C3 chaos and C4 model validation and
uncertainty. At the next substantial verified reader boundary,
use Zenodo's new-version action on concept DOI `10.5281/zenodo.22059939`, update
Figshare article `33314769`, and republish collection `8668413`. Do not retry
GitHub until the user reports that account access is restored.

## Complete bridge and release boundary — 2026-08-23

- Original bridges C1–C4 are structurally and computationally complete. Their
  657 stable segments comprise C1 152, C2 115, C3 117, and C4 273; each unit
  has seven mastery records and one open notebook. All strict schemas, static
  checks, fresh-kernel executions, perturbed branches, full PNG decoding, and
  deterministic staged-build regressions pass.
- The Indonesian terminology boundary contains 321 unique glossary IDs. The
  exact arXiv:2001.05854v1 source archive and Indonesian TeX still hash to
  `520cd160b47664dda32e57df87a6eb028348154e4d7a7494d230e8e517891d53`
  and `03f7e68801badc84255df3323078ae00eee7ecff8a9f118cba064ce5d46ff2f2`.
- A first complete 26-unit PDF build produced 355 tagged A4 pages, 28 outline
  entries, Indonesian language metadata, and all 141 mastery records. Visual
  QA rejected those bytes because several bridge mastery expressions rendered
  as linear ASCII rather than MathML. A bounded explicit-TeX typography repair
  and full bridge regression are in progress; rebuild the PDF afterward.
- Zenodo new-version draft `22063401` is reserved under concept record
  `22059939`, DOI `10.5281/zenodo.22063401`. It has no uploaded files and must
  remain unpublished until the corrected PDF, build receipt, six-file release
  package, and visual/privacy gates pass. GitHub remains paused.

Exact next action: finish the C1–C4 mastery typography regression; rebuild and
visually inspect the complete PDF; update README/control evidence with final
hashes; create the immutable complete release package; upload and publish draft
`22063401`; anonymously download and hash every public file; then update the
existing fileless Figshare article and Indonesian collection.

## Final complete reader boundary after responsive-table repair — 2026-08-23

- The stale typography-blocked state above is superseded by this verified
  boundary. C1–C4 all pass full normal/optimized static QA, fresh-kernel and
  perturbed notebook checks, PNG decoding, deterministic staged builds, and
  responsive browser QA. The final bridge trees are C1
  `56c7a055e8fa75630e2545b1e7d7b96c889925aea16534ab0d5ebcac4e9a14d6`, C2
  `1ee130ed30b9e6aa23524218030b6ddd787a2771d99a696117218b5538ec6b96`, C3
  `3f68874df2b3b164d71eee6066f039ce46bd7ce9400d63805c55e805ce68ea3b`, and
  C4 `9b1df796f9319ab1603bf9115e2c14e3e4b379e02512f32df11cbc0c875e77f0`.
- The shared CSS repair makes all 14 bridge tables keyboard/touch-scrollable
  within the viewport. C2, C3, and C4 at 390 px retain a 357.507 px centered
  article and document scroll width 375 px; all images load and IDs are unique.
- The rebuilt complete PDF is 43,463,488 bytes, SHA-256
  `f62218d51c97bd86f94ac80c6fe179a2b535be5cd8f8bcf2f402764421597cf3`, 355
  tagged A4 pages, `/Lang id`, 28 outline entries, no forms/JavaScript/
  suspects. Its build receipt is 18,978 bytes, SHA-256
  `e979ef2ac745b45ba50a15f43ab71864fc2e21c02151b7fa13592b0716ef9619`.
- Selected-page visual QA, including bridge tables, formulas, figures, project
  pages, and the closing note, passes with no clipping, overlap, raw ASCII
  formula, or broken image. The PDF has not yet been uploaded to Zenodo.
- Exact next action is now packaging to the new immutable directory, then
  publishing and anonymously verifying Zenodo draft `22063401`, updating the
  existing Figshare article/collection, and recording sanitized receipts.

## Historical published complete-reader boundary — 2026-08-23 (superseded)

- The immutable six-file release package is complete at
  `release/zenodo/reader-first-complete-20260823`. It contains the 355-page
  reader PDF, compact resumable source, build receipt, license, release
  manifest, and checksums. Total payload is 54,569,698 bytes and remains below
  the preservation cap. The PDF SHA-256 is
  `f62218d51c97bd86f94ac80c6fe179a2b535be5cd8f8bcf2f402764421597cf3`.
- Zenodo record `22063401`, DOI
  `10.5281/zenodo.22063401`, is published as the next version of concept
  `10.5281/zenodo.22059939`. The public record has the exact clean title,
  Joceline Lega attribution, CC BY-NC-SA 4.0 rights, Indonesian language,
  source and concept lineage, and the PDF as default preview. The exact model
  identification occurs once in the description; the project label is absent
  from title and description. The sanitized receipt is
  `00_control/ZENODO_PUBLICATION_RECEIPT_COMPLETE_20260823.json` (SHA-256
  `c5a65735105c7c350def98bb571f6ec0e021999e1e65f3335af2e0b1c482ec04`).
- Anonymous streaming readback of all six public files matched every local
  byte count and SHA-256. The six identities are recorded in that receipt;
  no credential material was persisted.
- Figshare was checked without creating a duplicate or uploading under a
  substitute license. The supplied token now returns HTTP 403
  `InactiveAccount`; the existing article page reports removed, the public
  project has no matching content, and collection version 43 has no content.
  The prior verified v2 receipt is preserved, and the current blocker is
  recorded in `00_control/FIGSHARE_PUBLICATION_RECEIPT_COMPLETE_20260823.json`
  (SHA-256
  `13b91dcad3828ffb4110119d5ecaadaef32351d46edd15933da48897cb355f46`).
  When the account is restored, update article `33314769` to the complete
  Zenodo DOI, publish one metadata-only version, add it additively to
  collection `8668413`, and anonymously verify the public item.
- GitHub remains deliberately untouched while the external suspension is
  active. No further authentication retry is useful until restoration is
  reported.

## Canonical corrected complete-reader boundary — 2026-08-23

- A bounded audit parsed all 26 packaged `backend/segments/*.jsonl` files:
  3,448 source records plus 657 bridge records, 4,105 total. The earlier
  complete release controls and Zenodo description under-counted source
  records by exactly 48 (FM01, PT01, BM01, and BM02); the reader content and
  unit closure were already complete.
- The hardened release builder now derives these counts from the exact JSONL
  closure. Canonical immutable package:
  `release/zenodo/reader-first-complete-20260823-r5`, six files,
  54,570,837 bytes. Its manifest SHA-256 is
  `6767a2fb8e50f0cd4ed00e23de046948878cd2ceb513f7358c646bcc8234ce51` and
  its checksum-file SHA-256 is
  `dfd12f1352030df83c69de7b97565809bb0bae851cab77796347c43e90ea3cc2`.
- Canonical Zenodo record `22070943`, DOI
  `10.5281/zenodo.22070943`, is published under concept
  `10.5281/zenodo.22059939`; it supersedes the intermediate corrected
  versions without changing the 355-page PDF bytes. Anonymous downloads of
  all six final files match local sizes and SHA-256 values. Its embedded
  public README/QA use only the stable concept DOI, preventing stale
  self-references in later versions.
- Sanitized receipt:
  `00_control/ZENODO_PUBLICATION_RECEIPT_CANONICAL_20260823.json`, SHA-256
  `6cb1962c5e14668c2be86284b78e182b4f8951a1f5d9baafcd937ae25906cab9`.
  Current cursor SHA-256 is
  `d0259a2b6cb7af8cae3f31b12f211ac8057bb35e40d872eba560bbca050e2dd3` and
  recovery-pointer SHA-256 is
  `d0a5f3ad7eba01c6bfe4371938932a0ea9d21847ba8686ed9cbe1365c47a60a5`.
  Figshare remains blocked by the recorded HTTP 403 `InactiveAccount`; its
  follow-up now points to canonical Zenodo DOI `22070943`. GitHub remains
  paused. The current Figshare blocker receipt SHA-256 is
  `264aa276dc374d1e5031799aaeba242c9288c4306895b2370e0d5d8df0aee35a`.
