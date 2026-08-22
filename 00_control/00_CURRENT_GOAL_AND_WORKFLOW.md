# O005/C120 — Durable Goal and Workflow

Status: active production. This file and the other files in `00_control` are the
authoritative recovery surface for this lane. Chat history and compaction
summaries are not required to resume.

## Goal

Produce the complete natural Bahasa Indonesia reader of Joceline Lega's
*Introduction to Mathematical Modeling*, University of Arizona Pressbooks
v1.01 (March 2026), together with an accessible deterministic reader, a
locale-neutral machine backend, lawful provenance, open Python replacements,
and complete mastery support. Translation is the dominant activity. QA proves
bounded outputs but must not become a substitute for production.

Preserve the exact official PDF and EPUB, the public Pressbooks REST
`content.raw` closure, stable record IDs and hierarchy, TeX, shortcodes,
footnotes, links, figures and long descriptions, assets, rights, and source
hashes. Apply CC BY-NC-SA 4.0 attribution, NonCommercial, ShareAlike, change
notice, and non-endorsement. Maintain component-level rights. Redraw Figure
4.1, replace Figure 10.1, and create a new cover, CSS, fonts, and accessibility
statement; never represent the Pressbooks theme as part of the independently
reproducible source closure.

Chapter boundaries `O005-LEGA-V101-CH01` through `CH06` (records 25, 27, 38,
39, 48, and 53) and the visible Part 2 and Part 3 introductions (records 28 and
40) are translated, built, independently rereviewed where applicable, and
deterministically verified. Their complete topology, identifiers, protected
mathematics, links, figures, 64 stable problem IDs and mastery records, six
open Python notebooks, and 1,582 paired segments are bound in the current
state, cursor, and QA log. The immediate boundary is Chapter 7, Pressbooks
record 57, *Epidemiology*, as `O005-LEGA-V101-CH07`; preserve its frozen
123-line raw source, 126 opening elements, 29 links, 150 TeX occurrences, three
figures, one footnote, and five problems, then complete its
mastery/computation closure without returning to source selection.

Continue in exact frozen TOC order through all front/back matter and
fourteen chapters: 54,932 source words, 113 exercises, twelve projects, eleven
lawful source final answers, textboxes, formulas, citations, assets, and
descriptions. Add four original bridge modules: reproducible Python/Jupyter;
saddle-node/transcritical/pitchfork/Hopf bifurcations; period doubling,
Lyapunov exponents, Lorenz dynamics, Poincare sections and return maps; and
calibration, identifiability, sensitivity, residual/holdout diagnostics, model
comparison, uncertainty, and failure analysis. Deliver twenty-six notebooks,
twelve self-contained open/synthetic-data project packets, and complete
113-item hint/check/solution closure. Import no proprietary MATLAB, PPLANE,
Excel, Maple, or Mathematica code.

## Backend contract

Every resource, edition, unit, segment, concept, term, problem, hint, answer,
solution, project, asset, code file, dataset, right, correction, QA event, and
artifact receives a stable locale-neutral ID. Preserve ordered hierarchy,
prerequisite and concept edges, source/target hashes, segment mappings,
multilingual hooks, and deterministic schema-versioned JSON/CSV exports. IDs
must remain invariant across later languages.

## Boundary workflow

1. Read `RECOVERY_POINTER.json`, `CURRENT_STATE.md`, `TRANSLATION_CURSOR.json`,
   `DECISION_LOG.md`, `TERMINOLOGY.csv`, `RIGHTS_AND_PROVENANCE.md`, and the
   current unit manifest.
2. Verify only the exact authority files named by the cursor. Never run a broad
   workspace scan.
3. Translate the next complete source-order unit naturally into id-ID while
   preserving protected mathematics, IDs, links, assets, and topology.
4. Add only the open computation and mastery material required by the declared
   unit boundary, with distinct provenance.
5. Build deterministically and run structure, math, link, asset, language,
   accessibility, notebook, numerical, privacy, rights, and clean-rebuild QA.
6. Record hashes, tool versions, caveats, corrections, cursor, and next action.
7. Commit and push only the narrow verified lane files at a significant
   boundary under standing authorization; never stage unrelated paths.

## Invariants

- One existing task and one O005 lane; do not create another task or touch a
  sibling lane.
- No upstream contact during production. After the complete corpus, at most
  one separately authorized, concise, deduplicated, high-confidence issue may
  be sent, signed exactly `Codex, on instructions of the user.`
- Public DOI/reader publication occurs only at a substantial verified corpus
  boundary. Ordinary verified production is committed and pushed as it grows.
