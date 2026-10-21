# Reproduce or resume

Python 3.10+, Tesseract 5 (`eng` installed), SQLite FTS5 and `requirements.txt` packages are required. No API key or paid service is needed. The workspace now has a full Git checkout on the research branch; all 234 pinned source files match their original blobs.

Repository processing:

```bash
python -m pip install -r research/requirements.txt
python research/pipeline.py all
python research/register_variants.py
python research/investigate.py
python research/export_checkpoint.py
python research/graph_checkpoint.py
python -m unittest discover -s research -p 'test_*.py'
python research/pipeline.py query 'quadriga*'
```

The full inventory is pinned to the base source tree. Additional evidence has separate manifests; originals are never overwritten. Filename and reviewed publication dates occupy separate fields. Three OCR workers use one OpenMP thread each; successful raw extraction is cached by source SHA-256.

Public historical backup recovery (downloads 463 MB once, then verifies/cache-skips):

```bash
python research/recover_external.py
python research/external_pipeline.py
python research/ocr_website.py
python research/export_native.py
python research/recover_assets.py
python research/followup_tests.py
python research/ocr_regions.py
python research/graph_checkpoint.py
```

`recover_external.py` validates archive checksum, member paths and expansion size. It refuses to overwrite an extracted directory; repair a partial extraction into a separate destination and compare files. It does not crawl the live site. `recover_assets.py` retrieves hash-recorded scientific references and optional language models, refusing changed bytes. Stop on access/rate denials; the current live .org robots and Wayback 429 are documented limitations.

Important artifacts:

- `reports/inventory.csv/.json`: every repository file and local SHA-256/Git verification.
- `publication_dates.json`: reviewed headers and registered witnesses; original labels retained.
- `reports/geometric_variants.json`: shared-region candidates with coverage/inlier statistics; no automatic deletion or merging.
- `reports/coverage.json`, `chronology.csv`: conservative SR/CL date-label comparison, not a publication census.
- `corpus.sqlite`: repository files/documents/words/mentions/reference_candidates/search; web_pages/web_search; web_images/web_ocr_search; reviewed_evidence and separately typed prior_map_nodes/edges.
- `corpus/<SHA256>.json/.txt/.tsv/.hocr`: raw extraction with coordinates/uncertainty. Same-byte image aliases share extraction.
- `reports/transcripts.jsonl`: portable repository scan text.
- `reports/website_pages.jsonl.gz`, `website_image_transcripts.jsonl.gz`: portable historical text exports, with evidence-type warnings.
- `reports/website_backup_inventory.json`, `website_image_manifest.json`: website artifacts and image-to-source mappings.
- `reports/native_artifacts.json.gz`: extracted PDFs/workbooks/text, render associations and legacy-format limits.
- `curated_evidence.json`: reviewed short excerpts, approximate image regions, translations and variant decisions.
- `reports/hypothesis_tests.json`, `followup_hypotheses.json`, `hour_pair_test.json`: executed tests and limitations.

Example SQL:

```sql
SELECT f.filename_date, f.publication_date, f.path, m.entity
FROM mentions m JOIN files f ON f.sha256=m.document_id
WHERE m.entity='John Winthrop';
SELECT * FROM reviewed_evidence WHERE target_date='1989-05-01';
SELECT p.original_url, p.kind, snippet(web_search,1,'[',']','...',25)
FROM web_search JOIN web_pages p ON p.id=web_search.id
WHERE web_search MATCH 'scordatura';
```

Page text includes reader interpretations and attributed correspondence; it is not scan transcription. Date-like fractions can be false positives. Two-digit years below 81 remain century-ambiguous in the candidate extractor. The alias dictionary is finite, and language-model confidence is not correctness probability. Additional OCR settings require versioned extraction namespaces; reviewed readings must not replace raw output.

Large caches, language models, extracted originals and SQLite stay outside Git. The downloadable workspace checkpoint contains derived OCR/SQLite and manifests; raw public backups can be reproduced from their cited URLs. Compressed text exports are committed so the checkpoint remains inspectable without local OCR.
