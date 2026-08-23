# O005/C120 completion audit — 2026-08-23

This is a bounded post-publication audit of the immutable release directory,
the sealed controls, and anonymous public Zenodo bytes. It does not replace
the earlier unit QA receipts and does not inspect other lanes.

## Local release identity

Release directory:
`release/zenodo/reader-first-complete-20260823`

The six intended public files are present. The five entries in
`CHECKSUMS.sha256` all match their local SHA-256 values. The release manifest's
four payload artifacts also match its recorded byte counts and hashes:

- PDF: 43,463,488 bytes, SHA-256
  `f62218d51c97bd86f94ac80c6fe179a2b535be5cd8f8bcf2f402764421597cf3`.
- Compact source ZIP: 11,082,093 bytes, SHA-256
  `7a7516e9d9273f5981b68b1723e89f04d4b81d2fe15dffc4e76b00f85fdba9cd`.
- PDF build receipt: 18,978 bytes, SHA-256
  `e979ef2ac745b45ba50a15f43ab71864fc2e21c02151b7fa13592b0716ef9619`.
- `LICENSE.md`: 1,229 bytes, SHA-256
  `df09d1b94e42fd7ef903d8ab50070e363b8c3c456b414773ca5e4a0010d74a53`.
- `RELEASE_MANIFEST.json`: SHA-256
  `5f404ac07c0ec06e93a094d323f1e14d2873a515d8febee63141987322dbc59e`.
- `CHECKSUMS.sha256`: SHA-256
  `98700c3c8f1c983ec105371ab199dbfd3f87cc5b3896285933aaf6212487c12f`.

The ZIP has 468 members, 467 rows in `SOURCE_PACKAGE_MANIFEST.tsv`, no
duplicate or unsafe paths, and a successful CRC test. Every manifest row was
read from the ZIP and matched its recorded byte count and SHA-256; the one
additional member is the manifest itself. Its total uncompressed member size
is 16,842,538 bytes. A bounded credential-pattern scan found no authorization
header, token, or credential-file content in the package.

## Closure and reader checks

The package contains all 26 ordered units (22 source-derived and four
original bridges), 26 notebooks, 141 mastery records (113 source plus 28
bridge), and 12 project packets, as declared by the release manifest and PDF
build receipt. The PDF independently reopens as 355 pages with `/Lang id`, 28
outline entries, and no AcroForm; its metadata title contains U+2014 and no
U+FFFD. The current local output PDF is byte-identical to the immutable release
PDF. Earlier structural, deterministic, notebook, accessibility, responsive
browser, terminology, and selected-page visual evidence remains in the named
controls and receipts.

## Public readback

Unauthenticated `https://zenodo.org/api/records/22063401` returned state
`done`, submitted `true`, DOI `10.5281/zenodo.22063401`, and six files. Each
file was streamed anonymously; filename, advertised byte count, downloaded
byte count, and SHA-256 matched the local release. The public metadata has the
clean title, creator Joceline Lega, language `ind`, CC BY-NC-SA 4.0, source and
concept lineage, one TTP contributor entry, and one model-provenance sentence.
TTP is absent from the title and description, and the independent/non-
endorsement statement is present.

## Remaining external state

Figshare is not silently treated as complete: the supplied account is still
recorded as HTTP 403 `InactiveAccount`; the old article is removed and the
current project/collection have no content. No duplicate item or incompatible
license upload was made. The exact blocker and one-shot restoration procedure
are in `FIGSHARE_PUBLICATION_RECEIPT_COMPLETE_20260823.json`. GitHub remains
paused under the reported suspension. The complete-reader production and
Zenodo preservation gates pass; only that external Figshare metadata mirror
remains to be retried after account restoration.

Audit performed at 2026-08-23T18:55:49+02:00.

## Census correction and republished boundary — 2026-08-23

The audit's aggregate-count finding was confirmed directly from all 26
packaged segment JSONL files: 3,448 source + 657 bridge = 4,105 total. The
release builder was hardened to derive those numbers from the selected closure,
and a no-overwrite corrected package was built and verified:
`release/zenodo/reader-first-complete-20260823-r2`, six files,
54,570,671 bytes, ZIP 468 members / 467 manifest rows, CRC-valid, and every
manifest row hash-matching.

The corrected package was published as Zenodo record `22070758`, DOI
`10.5281/zenodo.22070758`, under the existing concept. Anonymous readback of
all six files matched local byte counts and SHA-256. The corrected receipt is
`ZENODO_PUBLICATION_RECEIPT_CORRECTED_20260823.json` with SHA-256
`e18c1d38d0f73beb1c88d54299db3bbe739e4baa04488c57b59508755dbbf6a0`.
Record `22063401` remains immutable historical lineage; its stale census is
explicitly superseded rather than silently rewritten.

## Final stable-documentation boundary — 2026-08-23

The r2/r3 packages were valid but their embedded public README/QA named a
prior version DOI. To prevent a self-reference cascade, the public package
documentation now uses only the stable Zenodo concept DOI. Final package r4 is
`release/zenodo/reader-first-complete-20260823-r4` (54,570,851 bytes); its
compact source ZIP is 11,083,152 bytes, SHA-256
`a08d96461b32be3a14dbe904a08b94fde4289037e3cef748541e12c40ad42195`, with
3,448 + 657 = 4,105 segment census. Zenodo record `22070888` / DOI
`10.5281/zenodo.22070888` is published and all six anonymous file readbacks
match. Final receipt SHA-256:
`b903720f32f314f791c222fe19a18eb42aceb4cd02677b2b3d4cda8833a0a8ee`.

## Canonical release boundary — 2026-08-23

The public package-gate and boundary prose was made release-agnostic, using
only the stable concept DOI so future version publication cannot leave a stale
self-reference. Canonical package r5 is
`release/zenodo/reader-first-complete-20260823-r5`, six files,
54,570,837 bytes; its compact source ZIP is 11,083,138 bytes, SHA-256
`0350d0dc9530c877c3ebcbb84d3cfe7f73654eaeb59bfad46f4ddf61d9446d72`.
Zenodo record `22070943` / DOI `10.5281/zenodo.22070943` is published; all six
anonymous readbacks match local bytes and hashes, and the embedded README/QA
contain no version-specific record ID. Canonical receipt SHA-256:
`6cb1962c5e14668c2be86284b78e182b4f8951a1f5d9baafcd937ae25906cab9`.

The final control recheck also normalized the cursor and recovery pointer to
the canonical DOI/status. Their current SHA-256 values are
`d0259a2b6cb7af8cae3f31b12f211ac8057bb35e40d872eba560bbca050e2dd3` and
`d0a5f3ad7eba01c6bfe4371938932a0ea9d21847ba8686ed9cbe1365c47a60a5`.

Final bounded recheck: r5 manifest, checksum file, 468-member/467-row ZIP,
and every ZIP row passed; anonymous record `22070943` passed six-file byte and
SHA-256 readback; metadata passed version, `ind`, CC BY-NC-SA 4.0, corrected
3,448/4,105 census, clean title/description, one organization contributor,
and one model-provenance occurrence. Concept `22059939/versions/latest`
resolves to record `22070943`.
