# Mayday Mystery: executed investigation checkpoint

2026-10-21 UTC. **The mystery is not solved.** This checkpoint establishes an auditable partial corpus, independently checks several consequential cross-document references, and rejects overbroad interpretations. All original repository evidence is retained on the research branch.

## Evidence recovered and coverage

The complete pinned repository tree contains **234 files**: 107 archive advertisement images, 26 dated researcher scans, one researcher preview, 44 research crops, 38 art assets, three research PDFs and 15 other artifacts. Those 133 dated scan files span **108 filename dates**, not 133 distinct advertisements. The archive mirror describes itself as a February 2020 collection of renamed and sometimes GIF-to-JPEG-converted scans. The researcher collection describes library scanning and links higher-resolution Internet Archive derivatives.

**197 source files were recovered locally and verified against remote Git blob identifiers**, including 102 of 107 archive images and one of 26 researcher scans. All **103 accessible scans** received OCR. Another 43 research crops were processed: 146 unique image extractions in total. Remaining material is remotely inventoried, not falsely marked as downloaded. [Inventory](reports/inventory.csv), [coverage comparison](reports/coverage.json), [source assessment](SOURCES.md).

No identical Git blobs occur among the 234 source file entries, and no identical SHA-256 files occur among the 197 local copies. That is not proof of distinct advertisements. Visual inspection confirmed that the two 2015 files show the same advertisement design with different crops/renditions and an obstructing WEEKEND overlay in the newspaper scan. June 2005's `_2` file is an enlargement of the circle in `_1`. A visually similar June/August 2004 pair was rejected as a duplicate: layout resemblance produced a false positive. The 2001 same-date pair remains a page-relationship review item. Global perceptual hashes missed the confirmed crop relationship, illustrating why automatic deduplication must stay conservative. [Reviewed decisions](curated_evidence.json).

SR/CL's public finding aid lists 128 recovered records at 127 dates through 2026; most full scans are withheld in that edition. Comparing those dates with all repository filenames produces **26 unmatched SR/CL dates**: 22 after 2019 and four earlier date conflicts (1992-09-01, 1993-05-01, 1997-12-03 and 2010-12-01). The repository has nearby labels 1992-09-02, 1993-05-03, 1997-12-01 and 2010-12-08. These require issue verification, not four automatic missing-ad claims. Seven repository labels are absent from SR/CL's date set. The wiki introduces additional disagreements, including 2018-04-25 versus the mirror/SR/CL's May 1 label. This comparison is a coverage lead, not an independently authenticated census of publication.

## Independently checked primary connections

The clearest result is a durable date-and-level reference system:

| Source advertisement | Reviewed connection | Evidence |
|---|---|---|
| 1984-09-13 | Explicitly directs readers forward to 1985-03-15 for Khartoum and later coordinates | E5 |
| 1989-09-27 | Applies the Third Level via Owsley and quadrigae to 1989-05-01 | E1 |
| 1998-12-02 | Labels a diagram Second Level and points to 1989-05-01 | E2 |
| 1998-12-02 | Points to the Fourth Level of 1988-01-20 | E6 |
| 2000-09-20 | Requests date and hour from the 1983-11-22 schedule | E4 |
| 2006-05-01 | Explicitly refers to 5/1/89, Fourth Level | E3 |
| 2005-06-22 | A circle separately labels 5/1/89 and 6/25/05, with source-limb and fold terminology | E11 |

See [reviewed assertions and image regions](curated_evidence.json); each source path links to a preserved scan in the repository. E1–E7 reproduce leads already reported by [SR/CL](https://srcl.net/corpus). E11 was independently noticed here; no first-discovery claim is made. These links establish textual dependence across decades. They do not establish a key, the truth of narrated actions, or that coordinates identify actual gatherings.

The priority May 1989 image has a prominent Cromwell portrait, mathematical margins and panels, musical notation and a bottom narrative invoking Winthrop, Schrödinger and Confessio Augustana. Crucially, the same page is addressed through Levels 2, 3 and 4 by different later documents. A one-document-to-one-level legend is therefore untenable. The November 1983 scan distinguishes coordinate, schedule, worldview and doctrinal fields. September 2000 explicitly reuses its schedule phrase while combining a GPS-error graph, a speech-recognition flowchart, literary/scriptural allusions and a represented financial narrative. Treating all these marks as interchangeable symbols would destroy useful layout distinctions.

## Hypotheses actually tested

[Executed tests](reports/hypothesis_tests.json) and [ranked assessment](HYPOTHESES.md) distinguish several claims:

- **Multilevel cross-document addressing survives.** Starting with the September 1989 callback, December 1998 and May 2006 independently exhibit other levels of the same target page. This is retrospective replication of a prior lead, not blind validation or decoded plaintext.
- **A universal four-level system fails in its strongest form.** January 1988 visibly prints a fifth Level. That sequence does not call itself quadrigae, leaving a narrower classical four-sense interpretation unresolved.
- **The May 1989 Julian Day does not equal its newspaper date.** Standard conversion of 2,447,703.5 yields **1989-06-26 00:00**, 56 days after May 1. This rejects a simple publication-date restatement; it does not establish what the later date means.
- **A recurring confessional/political canon survives descriptive testing.** Later 2006 and 2015 scans return to Cromwell, Luther and Calvin. A simple exploratory permutation control finds six OCR documents with all three names versus a null mean of 0.214. Selection bias, OCR omissions and the crude null prevent treating its small empirical tail probability as a discovery of hidden meaning.
- **September 2000 is not self-contained.** Its explicit dependence on the 1983 schedule contradicts that hypothesis. A real-world organization remains possible but unverified; fictional or artistic organization explains these instructions too.

No globally applicable decryption, authenticated author identity, or verified real-world operation emerged. The best-supported description is an evolving project using repeated historical/religious vocabulary and explicit cross-publication instructions. Cipher, ideological, artistic and organizational explanations remain partly overlapping.

## Machine-readable research and reproducibility

The local [SQLite corpus](corpus.sqlite) contains 103 scan extraction records and **17,478 OCR word records** with source coordinates, confidence and review flags. FTS5 supplies text search. Structured outputs include 222 date-reference candidates, 35 repeated five-word phrases appearing on at least three filename dates, entity relationships, number/symbol candidates, visual duplicate candidates and the pre-existing VUE map (128 nodes, 77 links). Candidate counts are not reviewed fact counts.

Every accessible scan has raw text, TSV, hOCR and JSON derived files keyed by source SHA-256. OCR uses only the installed English model and preserves engine uncertainty. Fourteen timeouts in the first pass were resolved by limiting Tesseract's thread use; the continuation also caught four scans recovered after the first inventory. Foreign scripts, rotated margins, mathematics and music are not reliably transcribed. Four selected translations are stored separately; no claim of complete translation or semantic extraction is made. The graph is represented by queryable SQLite mention/reference tables plus reviewed JSON assertions; prior map links remain labeled as prior research.

Five tests passed, checking date validation, reference ambiguity, perceptual versus byte identity, recovered scan integrity, and complete OCR coverage of accessible scans. Instructions are in [RUNBOOK.md](RUNBOOK.md). No paid inference or configured AI keys were used.

The accessible `dates.pdf` and `dates.xlsx` were also extracted as native text and worksheet values. Their historical scan notes report missing bound-library issues in late April/early May 2004 and identify May 2001 as pages 6 and 7. These remain prior researcher notes rather than fresh verification of library holdings. A portable [JSONL text view](reports/transcripts.jsonl) accompanies the checkpoint; full word-coordinate extractions and SQLite are available in the workspace and can be reproduced with the pipeline.

## Limits and continuation

The initial milestone is **incomplete**. Thirty repository scan files (25 researcher scans and five archive images) remain unrecovered, along with seven other files. Workspace HTTPS failed at the inherited proxy; a subsequent request for additional network permission stalled until interrupted. GitHub's connected Contents interface returned empty content above 1 MB, while binary blob interfaces rejected text decoding. Public web tools could inspect secondary indexes and one SR/CL image, but .org requests failed and Internet Archive/Wayback requests were inaccessible through that tool. Those failures are environment/tool limits, not proof that the public archives are unavailable generally. No access controls were bypassed.

Next work should recover high-resolution scans and 22 later dated positions, reconcile publication dates, review Greek/Hebrew and mathematical regions, and define a narrowly specified decoder with genuinely unseen holdouts. The June 2005 circle and the May 1989 geometrical panels are a concrete comparison target. [Prioritized continuation](NEXT_STEPS.md), [journal](JOURNAL.md).
