# Investigation status

2026-10-21 UTC. Active investigation; initial milestone not yet complete.

- Reviewed PR #1 (open, head efba92b36c7515aa945bd974f1d83f63e2cca9f0); retained its audit script locally without merging.
- Captured complete, untruncated repository tree at 2bc34341b92f4c8989779b4bb744833912bfdc50: 234 file entries, 18 directories.
- Recovered repository text including the VUE research map. Recovering sub-1 MB binary files through GitHub connector with Git blob SHA-1 verification.
- Workspace clone and HTTP retrieval fail because proxy:8080 refuses connections. GitHub connector returns empty content for files over 1 MB; binary blob endpoints reject UTF-8 decoding. Larger scans remain remotely inventoried, not locally verified.
- Public web tools can inspect historical indexes. SR/CL states 128 records at 127 dated positions and publishes only one complete advertisement in its current edition. Other pages withheld there are not assumed publicly available.
- No configured AI credentials were reported; no paid inference has been used.

## Executed checkpoint

- 197 of 234 source files locally recovered and verified against remote Git blob identifiers; SHA-256 recorded.
- 103 accessible scans: 102 archive images and one researcher scan, representing 100 filename dates. All have successful raw OCR, word boxes and uncertainty records. Another 43 research crops processed.
- SQLite FTS5 corpus built: 103 scan records, 17,478 OCR words, 222 date-reference candidates, 35 recurrent five-word phrases. Prior VUE map exported separately: 128 nodes, 77 links.
- Reviewed primary images confirm three different level callbacks to May 1989 and the September 2000 callback to November 1983. These reproduce prior SR/CL findings; no decryption is claimed.
- Three visual pair decisions recorded, including a confirmed 2015 variant and June 2005 detail enlargement; a June/August 2004 false duplicate rejected.
- Five hypothesis checks executed, including retrospective holdouts and an exploratory permutation control. Five implementation/integrity tests passed.
- REPORT.md, HYPOTHESES.md, SOURCES.md, NEXT_STEPS.md and RUNBOOK.md now provide a reviewable checkpoint.
- Initial milestone remains incomplete: 30 repository scans and seven other files unavailable through current retrieval methods; later public evidence still requires recovery. Detailed blockers and workarounds are in REPORT.md and NEXT_STEPS.md.

See JOURNAL.md and provenance/ for retrieval evidence. No merge into the default branch has been performed.
