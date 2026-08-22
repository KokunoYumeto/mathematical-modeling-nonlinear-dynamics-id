# Rights and Provenance — O005/C120

## Spine

Joceline Lega, *Introduction to Mathematical Modeling*, University of Arizona
Pressbooks, version 1.01 (March 2026). Official source:
<https://opentextbooks.library.arizona.edu/mathematicalmodeling/>.

The book metadata and each frozen exported content record identify CC
BY-NC-SA 4.0 with no section-level override. The Indonesian adaptation must
retain attribution, identify modifications/translation, remain noncommercial,
use the same license, impose no additional restrictions, and avoid suggesting
endorsement by the author or University of Arizona.

## Frozen witnesses

The exact PDF, EPUB, canonical REST records, semantic and asset manifests, and
coordinator audit are under `authority/`. Their hashes and counts are recorded
in `CURRENT_STATE.md`, the unit authority manifest, and the coordinator
snapshot manifests. Local coordination transcripts are deliberately excluded
from the public repository.

## Component boundary

- Keep all source-derived translated prose and source-derived exercise text
  under CC BY-NC-SA 4.0.
- Mark hints, new answers, worked solutions, notebooks, tests, synthetic data,
  figures, CSS, and backend metadata as newly authored components while
  maintaining compatibility with the reader's ShareAlike distribution.
- Preserve all source citations and asset attribution. Record replacements and
  redraws explicitly; do not silently copy proprietary software or data.
- Figure 4.1 must be redrawn; Figure 10.1 must be replaced. Chapter 1 Figure
  1.1 remains source-derived and keeps its full accessible description.

## Chapter 2 component record

The Chapter 2 stadium-wave screenshot is source-derived and is copied
byte-for-byte from the frozen Pressbooks asset (80,026 bytes, SHA-256
`9abe8e17abd593811c14a1d6ea72b3ff727682ba58d000a87ece4056332769b6`).
Its Indonesian alternative text and surrounding explanation are adaptation
content under CC BY-NC-SA 4.0.

The source refers to `The_Wave.m` and a MATLAB GUI, but neither program is in
the admitted editable closure. No MATLAB or other proprietary source was
copied. The Chapter 2 NumPy/Matplotlib notebook is a new, independently written
implementation of the mathematical behavior described in the chapter. It
records every convention needed where the prose is underdetermined and remains
distributed compatibly with the reader's ShareAlike boundary.

The visible Part 2 introduction is a three-paragraph translation of frozen
Pressbooks part record 28 under the same CC BY-NC-SA 4.0 boundary. It has no
asset, formula, exercise, mastery, or computational component; none was
fabricated for the edition.

## Chapter 3 component record

Chapter 3 retains eight source figures byte-for-byte. Figure 3.4 has a separate
Indonesian adaptation in which only four explanatory English labels were
localized; the unmodified source bitmap remains beside it. The exact source
and target hashes, prompt, method, dimensions, change statement, and review are
recorded through the versioned `phase-portrait-construction-id*.provenance.json`
receipts. The final 1,024×1,024 adaptation is 131,859 bytes, SHA-256
`76172508b59ddce827f57d8e76d7c89c49dc9b56294a7ef32c6287e4228fe975`;
both closed-orbit labels state the exact interval `-1 < E < 1`. The source and
adapted figures remain within the reader's CC BY-NC-SA 4.0 boundary.

The source mentions Maple, MATLAB, PPLANE, and a proprietary phase-plane app,
but no program source was imported. The NumPy/SciPy/Matplotlib phase-plane
notebook is newly and independently written from the stated equations. It
implements equilibrium classification, conservative and damped integration,
energy and dissipation checks, and open plotting without claiming to port the
absent programs. Figure 3.2 is retained unchanged; because its embedded axis
label uses `dθ/dt` while the scaled prose uses `dθ/dτ`, the Indonesian text
states that source-figure notation explicitly.

## Chapter 4 and Part 3 component record

Chapter 4 retains Figure 4.2 byte-for-byte and supplies an independently drawn
accessible SVG for Figure 4.1. The redraw implements only the geometry,
notation, and physical relationships stated in the admitted chapter; it does
not copy unavailable drawing source. The open NumPy/Matplotlib notebook is an
independent implementation of the printed equations and explicitly makes no
experimental-validation claim. Its derivation corrections and assumptions are
enumerated in `SOURCE_CORRECTIONS.csv`. Both the translated chapter and its
adapted reader components are distributed within the book's CC BY-NC-SA 4.0
ShareAlike boundary.

The visible Part 3 introduction is a four-paragraph translation of frozen
Pressbooks part record 40 under the same CC BY-NC-SA 4.0 boundary. It has no
asset, formula, exercise, mastery, notebook, audio, or live-widget surface.

## Chapter 5 component record

Chapter 5 retains all seven frozen Pressbooks raster figures byte-for-byte.
Figures 5.1, 5.2, and 5.7 additionally have self-contained SVG adaptations in
which only the English graph labels were replaced by Indonesian labels; each
SVG embeds the exact frozen raster and has a provenance receipt binding source
and target hashes. The adaptations and translated long descriptions remain
within the reader's CC BY-NC-SA 4.0 boundary.

Problem 16's `popclockest.txt` is an exact 8,148-byte response from the official
U.S. Census Bureau URL cited by the source chapter, SHA-256
`f59dbd91b2bf975df7b7fb4af6de52dc3c68a705632e83d60410d98781206f09`.
It is redistributed solely as a separately attributed, hashed offline data
packet for reproducibility. The adjacent provenance JSON records the publisher,
URL, retrieval response, parser contract, scope caveats, and change status. No
broader rights claim is made for the Census website or any third-party material.

No MATLAB or Excel code was imported. The Chapter 5 NumPy/SciPy/Matplotlib
notebook is a new independent implementation of the mathematical models and
uses the local Census packet without network access at runtime. The original
hints, checks, and worked solutions/rubrics are labeled by provenance and are
distributed compatibly with the reader's ShareAlike boundary.

## Chapter 6 component record

Chapter 6 retains all four frozen Pressbooks raster figures byte-for-byte:
the damped and closed predator–prey phase portraits and the coexistence and
exclusion competition phase portraits. Their exact source paths, byte counts,
SHA-256 hashes, and EPUB-member identities are bound in the unit authority and
reader manifests. Indonesian captions, long descriptions, and mathematical
corrections are adaptation content under CC BY-NC-SA 4.0.

Two source links to the proprietary MathWorks Phase Plane App were replaced in
the translated exercise surface by one local, independently authored
NumPy/SciPy/Matplotlib notebook. No MathWorks application, source code, or
other proprietary implementation was copied. The notebook implements only the
printed model equations, explicit independently chosen numerical conventions,
and verification checks needed for the chapter's learning activity.

The primary Fussmann et al. *Science* article cited by Problem 6 was consulted
only to verify the meanings of the state variables and the published model
equations. No article text, figure, data, or supplemental file is redistributed.
The mastery record explicitly labels the simplifying closure `R = B` as new to
this edition rather than source-derived. All six newly authored hints, checks,
solutions/rubrics, and the notebook remain distributed compatibly with the
reader's ShareAlike boundary.

## Chapter 7 and Part 4 introduction component record

Chapter 7 retains all three frozen Pressbooks raster phase portraits
byte-for-byte: classic SIR (269,240 bytes, SHA-256
`6fb4ddda16dc32455db64ec8211e561260118f5a2994aa88b503a179d851c08b`),
stable disease-free endemic dynamics (307,592 bytes, SHA-256
`20862c9a7ae87d9d6cc5d3c00a5ea855ee7c7a786cd832e40b6aebf8acbb63af`),
and stable endemic dynamics (288,503 bytes, SHA-256
`e1b4360292dceb3d403cc54cc1b76cf1b45d80a9331acdad6a2f460d77eb9058`).
Indonesian captions, distinct alternative text, long descriptions, corrections,
and the white reader canvas are adaptation components under CC BY-NC-SA 4.0;
the white canvas changes presentation only and does not alter the source bytes.

No PPLANE, MATLAB, or other proprietary program code was imported. The
NumPy/SciPy/Matplotlib epidemiology notebook is a new independent
implementation of the displayed systems. Problem 5 does not determine a unique
MSEIR model; the notebook and mastery record therefore identify every added
transition assumption and label their passively immune newborn-fraction model
as a reference closure rather than source-authored fact. The cited journal
articles were used only to verify bibliographic/model claims; no article text,
figure, data, or supplemental file is redistributed.

Visible Part 4 record 58 is frozen as a source-derived CC BY-NC-SA 4.0 prose
unit with no component asset, problem, mastery, notebook, footnote, or figure.
Its raw and rendered source each contain one literal U+FFFD before
“reaction-diffusion”; the planned Indonesian translation must record the
transparent textual repair without altering the frozen authority witness.
