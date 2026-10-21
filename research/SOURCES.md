# Sources and provenance

Retrieved/inspected 2026-10-21 UTC. Publisher of the scans: The (Arizona) Daily Wildcat, University of Arizona. Repository authors state they obtained permission for online redistribution; this investigation has not independently authenticated that permission.

| Source | Role and reliability | Preserved evidence / limitations |
|---|---|---|
| [Fork snapshot](https://github.com/DiogoTM/maydaymystery/tree/2bc34341b92f4c8989779b4bb744833912bfdc50) | Fixed repository evidence, inherited from upstream; artifact dates require checking | [Complete 252-entry tree](provenance/repository_tree.json), 234 files; local bytes checked against Git blob SHA-1 and SHA-256. |
| [PR #1](https://github.com/DiogoTM/maydaymystery/pull/1) | Prior contribution: 87 lines in two files, audit not previously run on binary images | [PR snapshot](provenance/pr1.json). Retained audit script; new checkpoint builds on its head without merging default branch. |
| [Upstream](https://github.com/nimaid/maydaymystery) | Prior researcher corpus, map and provenance statements | Read repository text, request lists, preparation scripts and VUE XML. The map has 128 nodes and 77 links, retained as prior assertions rather than verified deductions. |
| [Original archive](https://www.maydaymystery.org/mayday/texts/index.html) | Long-standing scan collection and correspondence source | Repository mirror says 2020-02-19; GIFs converted to JPEG and renamed. Web access returned 502/timeouts; direct workspace retrieval failed at proxy. Original remote scan URLs have not been reconstructed for every mirror file. |
| [Wiki index](https://www.maydaymystery.com/index.php?title=List_of_May_Day_Mystery_ads) | Secondary historical finding aid | Inspected public index. Several dates differ from mirror and SR/CL; 1989 and September 2000 pages were redlinks. Do not treat redlinks as recovered evidence. |
| [SR/CL corpus](https://srcl.net/corpus) | Recent critical edition and useful hypothesis source | Claims 128 recovered records at 127 dated positions, including two records at 1990-12-05. Current edition publishes one full ad and withholds others for rights review. [Snapshot](provenance/web_initial.json) includes all 127 dated entries. Its interpretations are explicitly prior research leads. |
| [SR/CL 1983 scan](https://srcl.net/assets/pages/1983-11-22.jpg) | Independently accessible visual witness | Inspected via web tool; not downloaded into the local collection, and no byte identity claimed. |
| [Internet Archive collection](https://archive.org/details/MayDayMystery) | Repository-linked high-resolution TIFF/PDF/OCR source | Direct network unavailable; public web tool reported inaccessible. No conclusion that archive items themselves are restricted or missing. |
| [Wayback Machine](https://web.archive.org/) | Potential historical recovery route | Attempted a snapshot URL for .org index; web tool could not retrieve it. No CDX results obtained. |

Public web retrieval records are tool-extracted text, not original HTML/WARC captures. Dates in filenames are catalog labels until supported by a newspaper header or a reliable issue record. Correspondence was not independently recovered or authenticated in this run. No private materials or secrets were accessed or published. No paid inference was used.

Binary connector recovery: [per-file ledger](provenance/connector_downloads.json). Thirteen local text transfers initially acquired one patch-wrapper newline; exact source bytes were restored only when their remote Git blob hash matched, with wrapper versions retained under `provenance/transfer_wrappers/` and [restoration log](provenance/text_restoration.json). All recovered source files now match their remote blob identifiers.
