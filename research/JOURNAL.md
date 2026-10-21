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
