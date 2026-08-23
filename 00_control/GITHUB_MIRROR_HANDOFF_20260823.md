# O005/C120 — Frozen GitHub Mirror Handoff

Status: **complete and publicly verified**. Frozen at
`2026-08-23T21:15:44.7620801+02:00`.

This is the sole root-consumable handoff for the completed GitHub mirror of
Joceline Lega, *Introduction to Mathematical Modeling*, University of Arizona
Pressbooks v1.01 — independent Bahasa Indonesia edition. It records publication
only. No translated text, backend record, notebook, project packet, Zenodo
record, author contact, or upstream issue was changed or created at this
boundary.

## Public surfaces

- Repository: <https://github.com/KokunoYumeto/mathematical-modeling-nonlinear-dynamics-id>
- Frozen release:
  <https://github.com/KokunoYumeto/mathematical-modeling-nonlinear-dynamics-id/releases/tag/v1.01-id-complete-reader-20260823-r5>
- Reader: <https://kokunoyumeto.github.io/mathematical-modeling-nonlinear-dynamics-id/>
- Existing canonical Zenodo DOI, unchanged: <https://doi.org/10.5281/zenodo.22070943>

The public repository was fast-forwarded from
`b468fae819730380d960f3b33df84aa8dcd8e826` to the verified frozen reader head
`75f35bce216a0c6c223d3bcc3938a40403028a08`; the remote had no divergent
commit. Release tag `v1.01-id-complete-reader-20260823-r5` is a lightweight tag
whose public target is exactly that frozen head.

The Pages-only wrapper is commit
`934822e79264a3747610691f08ce204b364eb978`. It adds only
`.github/workflows/pages.yml`, `site/index.html`, `site/site.css`, and two README
links. It copies the already-built 26 readers, exact complete PDF, and license;
it does not rebuild or modify the edition. GitHub Actions run
<https://github.com/KokunoYumeto/mathematical-modeling-nonlinear-dynamics-id/actions/runs/32660511697>
completed successfully: both `build` and `deploy` passed.

## Frozen release assets

All six assets were streamed through unauthenticated public download URLs and
matched the exact local r5 byte counts and SHA-256 values.

| File | Bytes | SHA-256 |
|---|---:|---|
| `01_Pengantar_Pemodelan_Matematika_Edisi_Bahasa_Indonesia_Lengkap.pdf` | 43,463,488 | `f62218d51c97bd86f94ac80c6fe179a2b535be5cd8f8bcf2f402764421597cf3` |
| `02_O005_LEGA_v1.01_id_complete-reader-20260823-r5_compact_source.zip` | 11,083,138 | `0350d0dc9530c877c3ebcbb84d3cfe7f73654eaeb59bfad46f4ddf61d9446d72` |
| `03_O005_LEGA_v1.01_id_complete_pdf_build_receipt.json` | 18,978 | `e979ef2ac745b45ba50a15f43ab71864fc2e21c02151b7fa13592b0716ef9619` |
| `LICENSE.md` | 1,229 | `df09d1b94e42fd7ef903d8ab50070e363b8c3c456b414773ca5e4a0010d74a53` |
| `RELEASE_MANIFEST.json` | 3,449 | `6767a2fb8e50f0cd4ed00e23de046948878cd2ceb513f7358c646bcc8234ce51` |
| `CHECKSUMS.sha256` | 555 | `dfd12f1352030df83c69de7b97565809bb0bae851cab77796347c43e90ea3cc2` |

Aggregate release payload: six files / **54,570,837 bytes**. GitHub's recorded
asset digests agree with every SHA-256 above. The release is published, not a
draft or prerelease, and targets the frozen reader head rather than the later
Pages wrapper.

## Anonymous branch and Pages readback

The unauthenticated GitHub commits API resolved public `main` to Pages commit
`934822e79264a3747610691f08ce204b364eb978` at verification time. Seven raw
public branch witnesses matched local bytes and hashes: the Pages workflow,
landing HTML, landing CSS, README, translation cursor, canonical Zenodo
receipt, and the 43,463,488-byte PDF. The public PDF SHA-256 is the exact frozen
value above.

Every Pages byte was then downloaded without credentials and compared locally:

- 249 files from all 26 `build/reader` trees;
- landing `index.html`, `site.css`, `LICENSE.md`, and complete PDF;
- 253 files / **56,411,468 bytes** total;
- **253/253 byte-and-SHA-256 matches**, zero missing or mismatched files.

The public landing page has `lang="id-ID"`, one main landmark, 26 unit links,
no replacement glyph, and no horizontal overflow at desktop or a 390 px mobile
viewport. The first public unit opens as `Prakata`, retains `lang="id-ID"`,
loads with zero missing images or console warnings, and has no horizontal
overflow. The landing page links to the exact PDF, frozen GitHub release,
source repository, official Pressbooks source, CC BY-NC-SA 4.0 license, and
canonical Zenodo DOI.

## Terminal state

The assigned per-corpus GitHub mirror requirement is complete. Do not create a
second repository or release, retag r5, rewrite the translated corpus, mutate
the Zenodo lineage, contact the author, or open an upstream issue from this
handoff. Any future change is a new, separately verified version; r5 remains
the frozen snapshot identified above.
