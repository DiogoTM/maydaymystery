# Mayday Mystery — investigation checkpoint

2026-10-21 UTC. **All repository scans are now recovered and processed. The mystery remains unsolved, and the full 1981–2026 archive remains incomplete.** This supersedes the [initial partial report](checkpoints/REPORT_initial_partial.md).

## Evidence recovered

The examined series begins in 1981; repository holdings reach 2019, while SR/CL's finding aid reports positions through 2026. The repository contains two scan collections and earlier research, including a concept map. Its archive collection describes a February 2020 mirror with renamed files and GIF-to-JPEG conversion. Researcher scans describe direct newspaper-library provenance. These provenance histories must remain distinct.

| Collection | Verified holdings and processing |
|---|---|
| Repository | All 234 original files, 294,608,810 bytes; Git blob verification and local SHA-256 |
| Repository advertisement scans | All 133 files: 107 archive and 26 researcher scans; 30,766 OCR word records with coordinates |
| Supplemental repository crops | All 44 processed |
| Public IA website backup | 2,030 members including 1,836 files; 1,681 unique file hashes and 34 exact-duplicate groups |
| Website HTML | 716 pages separately indexed, including 101 date-named ad-context pages at 99 filename dates |
| Historical website images | 1,039 valid image files, 887 unique image hashes; all 887 successfully OCR-processed |
| Misnamed image | One `.jpg` is captured HTML rather than an image; preserved and flagged |
| Other documents | Three repository PDFs inspected, including 230-page Piggott notes; five website PDFs and two XLS workbooks extracted; two image-only PDF pages also rasterized and OCR-processed |

The website backup's SHA-256 is `2cc938d3bfd8eb751f9d5047a9dc7ef9d5aee8a9266ec5a0a1ec4302efdc6309`; MD5/SHA-1 also matched IA metadata. Raw backup, extracted originals, full OCR coordinates and SQLite are preserved in the workspace; compressed text exports and manifests accompany the research branch. No original repository evidence was altered. [Repository inventory](reports/inventory.csv), [website inventory](reports/website_backup_inventory.json), [website OCR summary](reports/website_ocr_summary.json).

## Duplicate scans and publication dates

The 133 scan files cover **108 filename dates**, not 133 advertisements. No exact duplicate blobs occur among the 234 repository entries. Nevertheless, geometric comparison evaluated 33 same/near-date image pairs and found 29 strong shared-visual-region matches. These connect researcher/archive renditions, a color variant and a detail enlargement; they are not automatic proof of 29 redundant advertisements. Two May 2001 pages are different page images at one publication date. [Geometric results](reports/geometric_variants.json).

Readable newspaper headers independently establish two important distinctions:

- **May Day, 1988** is the advertisement title; its newspaper header says **Wednesday, April 27, 1988**, page 16. The May 1 archive image matches with 517 geometric inliers over most of its area.
- **May Day, 1994** appears under a **Friday, April 29, 1994** newspaper header, page 16. Its May 1 archive image matches with 390 inliers.

These are independently verified publication/title distinctions, not newly discovered ads. Both filenames remain unchanged. June 2005's second file is an enlarged circle detail; May 2015's two versions share the design but differ in crop/rendition and a newspaper WEEKEND overlay. A June/August 2004 perceptual candidate was rejected as a duplicate because the text differs. [Reviewed dates](publication_dates.json), [visual assertions](curated_evidence.json).

## Exact mathematical follow-up

**May 1989's 8×8 symbolic matrix has an exact adjoint sl(3) model**, conditional on the reviewed transcription. All 28 independent commutators close in an eight-dimensional span; an explicit invertible change of basis verifies equivalence to commutation by a traceless 3×3 matrix. No entries were repaired to obtain the result. This is an independently derived structural identification, with historical priority unestablished. It yields no plaintext or clock time. [Proof, controls and source readings](reports/MECHANISMS.md), [structured matrix](matrix_1989.json), [exact output](reports/matrix_algebra_test.json).

April 2008 explicitly links Levenshtein distance to May 1989, Level II. May 2009 explicitly requests hour/minute extrapolation from its matrix; the image resolves an archived reader's 1989/1998 reversal. Distance alone cannot recover the missing Greek rho: 116 distinct single-insertion strings share the same distance. Numerical input and the supposed Bradwardine modification remain unspecified. The archived 2007 margin-annotation warning also limits authorial-layout claims. These are additional reviewed relationships and mechanism checks, not a general decoder.

## Coverage and remaining access limits

SR/CL reports **128 recovered records at 127 dated positions**, retaining two records at 1990-12-05. Its edition releases one full ad while withholding most other full pages. Filename comparison yields 26 unmatched SR/CL dates: 22 after 2019 and four earlier discrepancies (1992-09-01, 1993-05-01, 1997-12-03, 2010-12-01). Nearby repository labels exist for those four. Seven repository labels are absent from SR/CL. These are reconciliation leads, not an authenticated count of missing advertisements. [Coverage ledger](reports/coverage.json).

The live `.org` index redirects to an error endpoint and its robots response disallows all crawling; live crawling stopped. The public IA backup was recovered through IA's service. Wayback CDX timed out; a subsequent availability API request returned 429, so retries stopped. The 22 post-2019 primary positions remain unrecovered here. No access restriction was bypassed. The wider archive therefore remains incomplete.

## Independently reproduced primary relationships

| Source | Explicit connection |
|---|---|
| September 13, 1984 | Announces March 15, 1985 for Khartoum and later coordinates |
| September 27, 1989 | Applies Third Level via Owsley and quadrigae to May 1, 1989 |
| December 2, 1998 | Addresses May 1989 at Second Level and January 1988 at Fourth Level |
| September 20, 2000 | Requests date/hour from November 22, 1983's Schedule |
| May 1, 2006 | Refers explicitly to May 1989's Fourth Level |
| May 1, 1990 | Labels an altered Greek reading from May 1989 as scordatura |

The first five reproduce SR/CL leads; earlier reader comments already discuss the scordatura comparison. Source images, approximate regions and attribution are in [curated evidence](curated_evidence.json). The recovered 2007 OCR supplies another Second Level callback, pending detailed region review. No decoded plaintext is claimed.

The priority May 1989 page combines Cromwell, physics/geometry, music and multilingual narrative. Several levels address the same artifact, ruling out a fixed one-document-to-one-level legend. November 1983 distinguishes coordinate, schedule, worldview and doctrine fields; September 2000 explicitly returns to its schedule. Preserving layout is therefore necessary.

The recovered `friend39.html`, signed THE ORPHANAGE, describes Level 1 as literal wording and discusses phase shifts, geometric placement, database slices and scordatura. It is **attributed correspondence with an unauthenticated sender**, not an authenticated key. This reproduces the correspondence lead already cited by SR/CL. Reader comments and editorial interpretations are separately typed, never substituted for primary text. [Source contexts](reports/website_method_leads.json).

## Tested hypotheses

Ten checks appear in [initial results](reports/hypothesis_tests.json), [follow-up results](reports/followup_hypotheses.json), the [hour-pair test](reports/hour_pair_test.json) and the [mechanism follow-up](reports/MECHANISMS.md). They include retrospective comparisons and within-document tests; none is a blind plaintext success.

1. **Multilevel reference addressing survives.** Later notices attach Levels 2, 3 and 4 to May 1989. Holdouts were selected from prior research: this is retrospective replication, not blind validation or a decoder.
2. **A universal four-level rule fails in its strongest form.** January 1988 prints a fifth Level. That sequence does not call itself quadrigae, leaving a narrower classical four-sense mapping unresolved.
3. **JD as publication-date restatement fails.** The printed 2,447,703.5 JD converts to June 26, 1989 00:00, 56 days after publication. Piggott p.32 and archived comments already record this result. The nearby Augsburg anniversary points toward June 25; its relationship to the JD remains unexplained.
4. **A recurring confessional/political canon survives descriptively.** Seven of 105 variant/page analysis groups contain Luther, Calvin and Cromwell together, versus a null mean of 0.3268 over 10,000 simple permutations. These groups are not an ad census. Selection bias, OCR omissions, time trends and text length prevent interpreting this as cipher significance.
5. **September 2000 self-containment fails.** The date/hour instruction explicitly depends on the 1983 notice. Actual meetings or operations do not follow from textual dependence.
6. **One Greek alteration is explicitly signaled.** May 1989's `φάγῃ` means may eat; the familiar Romans 3:19 `φραγῇ` means may be stopped/silenced. May 1990 points to the altered word under scordatura while displaying the ordinary wording nearby. This supports an intentional contrast in this example, not a universal rho-insertion cipher. Earlier reader comments noticed it first.
7. **Bible addresses for the four hour numbers remain weak.** Treating 23°24′, 4°19′, 19°46′ and 22°37′ as chapter/verse pairs leaves Luke as the only compatible book in a 66-book KJV table. However, 31.6% of simple random-minute trials also leave a unique compatible book; no procedure yields a clock time. This is a candidate representation, not a decoding success or discovery claim.
8. **June 2005's formula has a conventional physical interpretation.** The printed proper-motion relation follows from equations (2) and (3) of Albrow et al.'s pre-2005 microlensing paper. The exact circle source is unidentified; its date labels and chessboard are unexplained. [Scientific primary source](https://www.astronomy.ohio-state.edu/gaudi.1/ms98001.pdf).
9. **May 1989's matrix has an adjoint sl(3) structure.** Exact coefficient brackets and an explicit change of basis verify this, conditional on transcription. Prime symbols were modeled independently; no su(3) real form or numerical time is established.
10. **Edit distance alone does not select the Greek restoration.** The expected missing-rho restoration shares distance 1 with 115 other single-insertion strings in the tested alphabet. Linguistic constraints are required; the ad's intended operands are unresolved.

An evolving intellectual/artistic or ideological project with deliberate inter-document instructions remains the strongest descriptive fit. A multilevel cipher could be a component. A represented real organization remains possible, but sender identity, operations and transactions are not independently authenticated. No general key or blind plaintext prediction emerged. [Ranked hypotheses](HYPOTHESES.md).

## Reproducibility and limits

SQLite separates repository OCR, website OCR, website text, reviewed assertions and the prior VUE map (128 nodes, 77 links). Repository analysis contains 337 date-reference candidates and 164 recurrent five-word phrases; those are unreviewed candidate totals. Raw text, TSV, hOCR and JSON preserve source coordinates and uncertainty.

Additional Greek/Hebrew/Latin-region OCR was attempted with hash-recorded language models. It remains imperfect and does not replace reviewed image readings. Full-image OCR uses English; foreign scripts, mathematics, music, rotation and layout remain limitations. Legacy WordPerfect/DOC and audio files are inventoried but not fully converted or transcribed. Text decoding replacements occur in 103 HTML pages; original bytes remain intact. Spreadsheets and correspondence interpretations remain prior research rather than authenticated primary assertions.

**Ten implementation/integrity tests pass. No paid inference was used.** [Runbook](RUNBOOK.md), [journal](JOURNAL.md), [next steps](NEXT_STEPS.md).

The repository-based initial milestone is reached: every repository scan is inventoried and processed, variants and major relationships investigated, competing mechanisms tested, and a report/checkpoint produced. The wider archive, multilingual transcription and meaning of the mystery remain unresolved.
