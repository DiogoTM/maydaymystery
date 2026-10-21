# Source status update — full recovery

2026-10-21 UTC. The earlier network limitation below is resolved. All 234 repository files now match their remote blobs, and a full research-branch Git checkout is available. The original source tree remains unchanged.

New public evidence:

- IA metadata: `https://archive.org/metadata/MayDayMystery`, captured with timestamp and SHA-256 in `provenance/public_http_20261021.json`.
- Public 2020 website backup: `https://archive.org/download/MayDayMystery/backups/MayDayMirror_2020-02-28.7z`; 463,117,266 downloaded bytes, MD5/SHA-1 checked against metadata, SHA-256 `2cc938d3bfd8eb751f9d5047a9dc7ef9d5aee8a9266ec5a0a1ec4302efdc6309`. Provenance: `provenance/ia_mirror_retrieval.json`. Full inventory and compressed page/image text exports are in `reports/`.
- Live .org index redirected to Frontera's error endpoint; its robots response disallowed all crawling. No further live crawl performed. A non-www request was already in flight before the robots response was read.
- Wayback CDX read timed out; availability API returned 429. Stopped retrying; no post-2019 primary scans recovered.
- Scientific formula comparison: Albrow et al., *The Relative Lens-Source Proper Motion in MACHO 98-SMC-1*, equations (2) and (3), via the author's institutional PDF. Gaudi/Petters *Folds* was inspected but not identified as the circle's visual source. `provenance/reference_retrievals.json` records URLs, timestamps and hashes.
- Bible structural control: public `thiagobodruk/bible` English KJV JSON. It uses Portuguese book labels; canonical position 42, Lucas/lc, is Luke. Claim is limited to its 66-book table and is not a claim of author intent.
- Additional Tesseract models: seven public tessdata_fast files with recorded SHA-256 in `provenance/ocr_models.json`. Region OCR remains uncertain.

The recovered website contains 716 HTML pages and attributed letters, including `friend39.html`. They mix signatures, editorial material and reader interpretations. None authenticates an individual or organization. No private Discord archive was downloaded. Historical WordPerfect/DOC files and audio remain inventoried but not fully decoded/transcribed.

The material below preserves the first checkpoint's source assessment; its availability notes describe that earlier attempt.

---

# Sources and provenance

First checkpoint retrieval history, 2026-10-21 UTC. Publisher of the scans: The (Arizona) Daily Wildcat, University of Arizona. Repository authors state they obtained permission for online redistribution; this investigation has not independently authenticated that permission.

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


## Matrix follow-up sources and boundaries

- `texts/My Scans/1989-05-01_page24.jpg`, matrix region [.67,.687,.935,.765], manually transcribed in `matrix_1989.json`; lower-resolution archive image visually compared. Algebraic identification is computed, not a source quotation. Independent second transcriber pending.
- `texts/My Scans/2008-04-02_page14.jpg` and archive counterpart: reviewed Level II Levenshtein pointer to May 1989 and Level III pointer to May 1990. Raw OCR's I/II disagreement is retained.
- `texts/My Scans/2009-05-01_page8.jpg`: header and matrix instruction visually reviewed. Primary date pointer reads 5/1/89; the historical `09-may1.html` reader comment says 1998 and is treated as erroneous on this point.
- Historical backup `texts/07-may1.html`: publisher-of-the-archive warning identifies margin comments on the huge linked PDF as a reader's additions. Exclude those from authorial-layout assertions.
- Kertész (1986), Journal of Physics A 19, 599–601, DOI https://doi.org/10.1088/0305-4470/19/4/021. Institutional record https://research.ceu.edu/en/publications/extrapolation-of-transfer-matrix-data-for-percolation-and-lattice/ and author publication list https://www.phy.bme.hu/~kertesz/pub2.html establish bibliographic identity and finite-size extrapolation context. Full PDF not recovered; no full-paper hash or recurrence implementation claimed. Beleznay (1986), same volume, 551–562, DOI https://doi.org/10.1088/0305-4470/19/4/016, is the algorithm source to obtain. Failed retrievals and source URLs are in provenance/romberg_reference.json. The advertisement's supposed Bradwardine modification remains undefined.
