# Research journal

## 2026-10-21 UTC — recovery and source criticism

Reviewed PR #1 before starting. Its audit is useful but intentionally excludes undated files, previews, art, PDFs outside two scan folders, and all perceptual comparison. Retained the original script and will supplement it with a complete remote/local inventory.

Direct clone failed immediately with `Failed to connect to proxy port 8080`. A second request to maydaymystery.org failed the same way. Cloud runtime reports no configured secrets or outbound identities. Network policy file describes unrestricted HTTP; observed policy state is unknown, so this is a transport failure, not evidence of archive refusal. No proxy bypass was attempted.

GitHub connector successfully returned the full recursive tree and base64 for 1989-05-01.jpg. Decoded it locally. A >1 MB research scan returned empty base64. Both fetch and fetch_blob reject binary Git blobs; preserving this limitation explicitly.

Inspected repository README files, preparation scripts, scan-order requests, and VUE XML. Original collection is a renamed, GIF-to-JPEG-converted mirror dated 2020-02-19, not the original newspaper files. Researcher scans claim direct library provenance and link an Internet Archive collection with TIFF, PDF and OCR derivatives. Treat permission statements as repository authors' statements, not newly obtained permissions.

Browsed SR/CL corpus, maydaymystery.com index and SR/CL's published 1983-11-22 scan. The .org index returned 502/timeouts via web tools. Internet Archive and Wayback URLs were inaccessible through web tools. The wiki's 1989 and September 2000 links are redlink edit URLs, not surviving document pages.

Initial lead: disagreement between archive filename dates, physical-scan filenames and later indexes. Publication date, printed thematic date and filename must remain separate. SR/CL's quadrigae interpretation is a prior research lead to test; its claims must not be relabeled as new discoveries.

## 2026-10-21 UTC — completed local processing checkpoint

Recovered 197 source files. GitHub connector base64 recovery obtained 184 binary/pointer artifacts plus 13 text files. Fixed patch-wrapper newlines in text copies only when exact remote blob identity could be restored; preserved wrapper versions and restoration log. All 197 copies now match expected Git blob hashes. All 234 remote file entries have distinct blob identifiers. Local SHA-256 checks found no exact duplicates.

Initial OCR pass processed 128 of 142 images, with 14 timeouts. Limiting OpenMP to one thread resolved all 14; the retry also picked up four late-recovered scans. Final total is 146 successful image extractions (103 advertisement scans, 43 crops). SQLite holds 103 scan documents, 17,478 word boxes, 222 date candidates, 35 recurrent five-grams. Candidate references and aliases are explicitly not reviewed relationships.

Reviewed scans for November 1983, September 1984, January 1988, May/September 1989, December 1998, September 2000, May 2006, May 2015 and June/August 2004/June 2005 pair decisions. Replicated SR/CL's three level callbacks to the same May 1989 page and September 2000's explicit return to the 1983 schedule. Observed June 2005 circle labels 5/1/89 and 6/25/05; recorded as an independently observed lead, not a new discovery claim. January 1988 prints a fifth Level but does not name that sequence quadrigae.

Confirmed May 2015 pair as same advertisement design with different rendition/crop and a newspaper WEEKEND overlay. June 2005 `_2` is an enlarged detail of `_1`, not a second page. Rejected June/August 2004 perceptual candidate: similar layout, different notices. Perceptual hashing alone missed both confirmed same-design/detail relationships.

Converted 2,447,703.5 JD from May 1989 to 1989-06-26 00:00, 56 days after publication; no meaning assigned. Executed five hypothesis checks and a 10,000-permutation exploratory co-occurrence control. Six date-deduplicated OCR documents contain Luther/Calvin/Cromwell together versus null mean 0.214. Explicitly recorded selection bias, missing OCR and time/length confounding; not a cipher significance result.

Parsed all 127 SR/CL positions from the captured finding aid. Twenty-six lack exact repository filename labels: 22 later than 2019, four earlier date disagreements with nearby repository labels. Seven repository labels are absent from SR/CL. No automatic merging or missing-ad count inferred.

An additional-network-permission command stalled until interrupted by the user. Do not repeat that blocking flow. The user requested visibility; shared local artifact links and prepared REPORT.md and a reproducible checkpoint for a dedicated research branch. Five tests passed. The milestone remains incomplete because larger images, later evidence, complete multilingual extraction and a reproducible decoder remain unresolved.

Extracted native text/blocks from the one accessible PDF (`dates.pdf`) and worksheet values from `dates.xlsx` (one sheet, 58 rows). The workbook reports a historical library gap in late April/early May 2004; this is an earlier researcher's holdings note, not a newly checked absence. Exported 103 raw scan transcripts to JSONL with source hashes and OCR status. The original preparation converter deletes source GIF files when run; inspected it but did not execute it. All new tooling avoids that behavior.


## 2026-10-21 UTC — continuation after network access enabled

Direct HTTPS now succeeds. Recovered the remaining 37 source files with the existing read-only downloader, verifying all 234 repository blobs and all 133 scans. Full Git clone completed; attached its Git metadata to the recovered workspace after verifying matching originals. All 44 supplemental crops also processed. Repository scan OCR now has 30,766 words, 337 reference candidates and 164 repeated five-grams.

Retrieved IA metadata and a 463 MB public website backup. Verified metadata MD5/SHA-1 and independent SHA-256. Validated archive paths and total expansion before extracting. Inventoried 1,836 files (2,030 total members), 1,681 unique hashes and 34 duplicate groups. Parsed 716 HTML pages into a separate searchable layer, retaining raw bytes and noting 103 pages with encoding replacement characters. OCR processed all 887 unique valid Mayday-site image hashes (1,039 files); one alleged JPEG is actually captured HTML. Two image-only PDF pages were rendered and OCR-processed; other website PDFs and two spreadsheets were extracted natively. Legacy WordPerfect/DOC and audio remain conversion/transcription work.

Live .org index redirected to an error page and robots disallowed all crawling. Stopped live crawl. Wayback CDX timed out and the availability API returned 429; no retry after the rate denial. The public IA backup was an independent recovery path, not a means of accessing withheld SR/CL media.

Geometric registration tested 33 same/near-date pairs, with 29 strong shared-region results. Reviewed actual headers for April 27, 1988; April 29, 1994; May 1, 1989; May 1, 2007, plus September 20, 2000. Preserved publication/title distinctions and all filenames. Registered 1988/1994 archive versions to these witnesses; a third April/May pair remains a shared-image relationship with publication verification pending.

Recovered Piggott's 230-page notes. Page 32 already states midnight June 25/26, 1989 for the JD; archived comments also give it. Marked our calculation as replication. Read `friend39.html`: signed explanation says first level is literal and discusses phase shifts, Qabbalah, slices and scordatura. Sender identity is not authenticated. Website 1990 comments already discuss the Greek eating/stopped-mouth contrast. Independently inspected 1989 HD Greek and the 1990 diagram's explicit scordatura callback; recorded as a deliberate-contrast candidate supported in two primary images.

Tested four hour-pairs as Bible chapter/verse addresses. Luke alone fits the 66-book table, but the exploratory random-minute control yields a unique compatible book 31.6% of the time. No clock-time output follows; weak lead retained without decoding claim. Independently matched the June 2005 proper-motion formula algebraically to Albrow et al. equations (2),(3); exact circle artwork source remains unidentified. Retrieved seven OCR models and tried four selected script-specific regions; results remain imperfect. Eight tests pass.

Repository-based initial milestone is now reached. Wider archive recovery, publication-date reconciliation, multilingual review and a general decoder remain open. No original evidence was modified, default branch merged, private chat archive fetched, or paid inference used.


## 2026-10-21 UTC — exact matrix and distance follow-up

Reviewed April 2008 metric instructions in both scans: Levenshtein distance points to May 1989 Level II; a separate instruction addresses May 1990 Level III. Preserved the researcher OCR's erroneous Level I as raw output and recorded the reviewed reading separately. Reviewed May 2009 newspaper header and instruction: “5/1/89, matrix”, not the 1998 reversal in archived reader commentary. Bibliography confirms Romberg–Beleznay as a real modified extrapolation method. Full-paper attempts failed (503/timeouts/restricted publisher route); no access bypass or invented implementation.

Transcribed all 64 entries of May 1989's symbolic matrix, then recorded closure/nondegeneracy predictions before calculating brackets. All 28 independent commutators close in the eight-dimensional coefficient span; the Killing form has rank eight. Derived an explicit traceless 3×3 model and invertible P (determinant 2/3), verifying all eight intertwining identities exactly. This identifies the scanned matrix as adjoint sl(3), conditional on transcription and independent treatment of primes. No source entries were repaired. A controlled one-entry error produces ten ordered brackets outside the span. The generic independent-parameter matrix is not Hermitian, contrary to a tentative archived reader suggestion. Independent double-entry and printed-source identification remain pending. No matching adjoint/sl(3) identification found in searched historical page text/repository PDF extraction; priority is not claimed. Other archived pages already discuss SU(3)/Lie algebras.

The scalar Levenshtein distance for unaccented eating/stopped-mouth words is one, shared by all 116 distinct Greek single-insertion strings in the defined control. Distance alone cannot select the restoration. Neither this ambiguity check nor the exact algebra is a blind cross-document decoding success. No numerical input, supposed Bradwardine modification, time or plaintext emerged.

Recorded the 2007 historical page's explicit warning that linked-PDF margin notes are a reader's annotations. Added reviewed graph assertions E13–E16 and regenerated SQLite relations. Ten integrity/implementation tests pass, including known sl(2) bracket and nonclosed-span checks; all 234 original files remain hash-identical. See reports/MECHANISMS.md for the proof, source criticism and limitations.
