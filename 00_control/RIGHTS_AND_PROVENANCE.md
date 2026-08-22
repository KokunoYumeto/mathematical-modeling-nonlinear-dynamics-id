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

## Model provenance

OpenAI Codex gpt-5.6-sol, Ultra. was used for translation, technical
adaptation, and QA. This model-identification note supplements rather than
replaces the preserved credits for Joceline Lega, University of Arizona, and
recorded human contributors.

## Frozen witnesses

The exact PDF, EPUB, canonical REST records, semantic and asset manifests, and
coordinator audit are under `authority/`. Their hashes and counts are recorded
in `CURRENT_STATE.md`, the unit authority manifest, and the coordinator
snapshot manifests. Local coordination transcripts are deliberately excluded
from the public repository.

The separate terminology-QA witness under
`authority/terminology/arxiv-2001.05854v1/` is Natanael Karjanto's
arXiv:2001.05854v1 source package under CC BY-SA 4.0. It is preserved
unmodified, separately attributed, and used only as Indonesian field-usage
evidence. It is not relicensed as part of the CC BY-NC-SA 4.0 Lega adaptation.

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
Its raw source contains one valid U+00A0 nonbreaking space before the emphasized
term “reaction-diffusion” and zero U+FFFD characters. This is spacing, not a
source-text defect; the frozen authority remains byte-identical. The complete
four-paragraph Indonesian adaptation preserves the six emphasis nodes and
eleven formulas and adds no inapplicable mastery, notebook, asset, footnote,
figure, or problem component.

## Chapter 8 frozen component record

Chapter 8's admitted authority retains three primary Pressbooks rasters
byte-for-byte: the Brusselator phase portrait (169,478 bytes, SHA-256
`957ba0e2af31820eb0224add944508da2a1ab42135ea43450854880e38d8c9f4`),
Brusselator time series (129,573 bytes, SHA-256
`0244fe5655d13b710978c4ee42ed84556d4cbc5124d3a60fe7c3d4ca9e2c5e7c`),
and Oregonator phase portrait (140,277 bytes, SHA-256
`052645103df598f8feac0be17dfbf64f6525bf6d44f798f9bccfc10c269a548b`).
Their exact EPUB members and authority identities are recorded in the unit
manifest; no claim is made for the rendered `srcset` derivatives beyond the
three primary frozen images.

The source invokes PPLANE, MAPLE, and MATHEMATICA but supplies no program source
in the admitted closure. Chapter 8 production must independently implement the
printed Brusselator/Oregonator mathematics with open Python tools and must not
copy proprietary program code. Source-derived translation, figures, captions,
and descriptions remain within the CC BY-NC-SA 4.0 ShareAlike boundary; new
mastery and code components receive distinct provenance.

## Chapter 9 component record

Chapter 9 retains its three frozen Pressbooks rasters byte-for-byte: the random
walk figure and two Fisher–KPP phase-plane figures. Their exact EPUB members,
sizes, and hashes are bound by the unit authority and reader manifests. The
chapter-level record has no license override, so the translated prose,
captions, descriptions, and retained figures are distributed within the
book's CC BY-NC-SA 4.0 boundary; no broader component-rights claim is made.

The named MATLAB diffusion GUI and PPLANE surfaces supply no code in the
admitted closure. The random-walk/Fisher–KPP notebook is independently authored
from the printed mathematics with NumPy/SciPy/Matplotlib. No MATLAB, PPLANE, or
proprietary implementation was imported. Newly authored mastery records and
code are identified separately and distributed compatibly with ShareAlike.

## Chapter 10 component record

Chapter 10's authority preserves all three exact Pressbooks figure witnesses:
the 120,120-byte collage (SHA-256
`ed55c4ad09e5b4f1746dabf66aa87509538bcf76bcbc442650a4925ea47006ba`),
the 59,364-byte Swift–Hohenberg pattern raster (SHA-256
`f92c04b397d388f84a31737b72dfbfdf89a14df4210e7cbf3c41fcf2f8b8958a`),
and the 8,974-byte growth-rate raster (SHA-256
`a49ff56eba92cc8f74400b6925443a63a4bcdbe95afd477c51f386f038abf32c`).
The record provides no component-specific creator or license statement. The
reader therefore retains the latter two within the inherited CC BY-NC-SA 4.0
boundary at intrinsic size and makes no broader claim for them.

The mixed-photo Figure 10.1 collage remains an audit witness but is not shipped
as the reader figure. It is replaced by a self-contained 800×560 accessible SVG
created independently for this edition, with no source pixels reused and with
its own machine-readable provenance receipt shipped alongside the reader. The
source long description is adapted to describe that replacement accurately.

The proprietary MATLAB GUI `Patterns` is named but no URL, source, executable,
dataset, parameter set, grid, time step, or random seed is supplied. The open
pattern-formation notebook is a new independent implementation of the printed
Swift–Hohenberg mathematics and separately reconstructed Klausmeier checks; it
imports no MATLAB code and does not claim to reproduce either source figure
pixel-for-pixel. The cited Klausmeier article is not redistributed. Its
equations and scaling are supplied as mathematical facts with an exact DOI
citation so Problems 4–6 can be studied offline; all new hints, checks, worked
solutions, and code remain explicitly separate from source-provided content.

## Part 5 introduction and Chapters 11–12

Visible Part 5 record 409 is a source-derived two-paragraph prose unit with no
asset, problem, formula, footnote, notebook, or mastery component. Its natural
Indonesian translation and modular segment records remain within the inherited
CC BY-NC-SA 4.0 boundary with the standard change and non-endorsement notice.

Chapter 11 record 410 likewise references no component asset. Its frozen
canonical/raw/rendered bytes inherit the book license because the record-level
license override is empty. The complete translation and seven source-derived
exercise summaries remain in the CC BY-NC-SA 4.0 adaptation; the seven hints,
checks, and worked solutions are identified as newly authored support. The
thirteen mathematical/notation corrections are declared in the correction
ledger. No notebook or external artifact was attributed to the source or added
to this unit.

Chapter 12 record 413 has an empty record-level license override and references
no component asset, link, exercise, or computational surface. Its frozen
canonical/raw/rendered bytes therefore inherit the book's CC BY-NC-SA 4.0
license. The admitted Indonesian translation remains an adaptation under that
license; its corrections are separately ledgered, and no mastery, notebook, or
asset component was fabricated merely to populate an inapplicable backend
field.

Chapter 13 record 445 also has an empty record-level license override and thus
inherits CC BY-NC-SA 4.0. Its eight primary PNGs are preserved byte-for-byte in
the frozen authority and bound by exact EPUB member, path, size, dimension, and
SHA-256 identity; no broader component-rights claim is made. The rendered
Pressbooks witness retains remote responsive `srcset` variants that are not
part of the admitted primary-asset closure. The independent Indonesian reader
uses only the eight frozen local primary files, retains and translates all
eight figure descriptions, and removes remote image selection at runtime. The
eleven printed answer groups remain labeled source-derived; the eleven hints,
checks, and worked solutions are newly authored, distinctly provenanced, and
distributed compatibly with ShareAlike. No notebook or proprietary program
surface is attributed to or manufactured for this refresher chapter.

Chapter 14 record 555, *Modeling Projects*, has an empty record-level license
override and no embedded asset, formula, footnote, or source answer surface. Its
translated twelve-project directory remains an adaptation of the book under CC
BY-NC-SA 4.0. The linked research articles and supplemental resources are
citations only and are not redistributed or claimed under the book license.
Each executable project packet, notebook, synthetic/open dataset, check, and
rubric is independently authored for this edition, separately provenanced, and
must not import proprietary code or imply reproduction of an article result
unless the packet actually verifies that result from lawfully available data.
