# Reproduce or resume

Python 3.10+, Tesseract 5 with `eng`, and packages from `requirements.txt` are sufficient. SQLite FTS5 must be enabled. No API keys or paid services are needed.

```bash
python -m pip install -r research/requirements.txt
python research/pipeline.py all
python research/investigate.py
python research/export_checkpoint.py
python research/audit_scans.py
python -m unittest discover -s research -p 'test_*.py'
python research/pipeline.py query 'quadriga*'
python research/pipeline.py query 'Winthrop'
```

The workspace currently holds a recovered file snapshot, not a complete Git checkout: direct clone was blocked. To resume elsewhere, clone the research branch normally. It retains the full upstream tree and PR #1's two files. The pipeline inventories against the pinned base tree; subsequent evidence should receive an additional provenance manifest rather than silently replacing that snapshot.

To recover source files missing from this workspace after HTTPS is functional:

```bash
python research/download_missing.py
python research/pipeline.py all
python research/investigate.py
```

The downloader uses one request per second, verifies expected size and Git blob identity, refuses overwrite, and stops on access/rate denials. OCR uses three subprocess workers with one OpenMP thread each and a per-image timeout. Successful SHA-keyed OCR is cached; raw originals are never rewritten by the pipeline. To improve a transcription, store an additional reviewed record instead of editing raw OCR. Different OCR settings require a separate extraction namespace or explicit versioning; the current cache is for this checkpoint's fixed settings.

Important outputs:

- `reports/inventory.csv`, `inventory.json`: every remote file, local retrieval status and verification.
- `reports/chronology.csv`, `coverage.json`: conservative date-label comparison with SR/CL's finding aid.
- `corpus.sqlite`: files, documents, words, mentions, reference_candidates, search.
- `corpus/<SHA256>.json/.txt/.tsv/.hocr`: unreviewed extraction and layout.
- `reports/transcripts.jsonl`: portable text view of 103 scans; `artifact_extractions.json`: native PDF/spreadsheet data.
- `curated_evidence.json`: reviewed short excerpts, approximate image regions, selected translations and variant decisions.
- `reports/hypothesis_tests.json`: executed mechanism tests and exploratory control.
- `reports/prior_megamap.json`: prior researcher map exported without converting it to established fact.

Example SQL:

```sql
SELECT f.filename_date, f.path, m.entity
FROM mentions m JOIN files f ON f.sha256=m.document_id
WHERE m.entity='John Winthrop';
SELECT * FROM reference_candidates WHERE target_date='1989-05-01';
```

`references()` intentionally flags two-digit years below 81 as ambiguous rather than assuming a century. Numbered Bible verses and arbitrary fractions can resemble dates; reference rows remain candidates. Entity extraction uses a finite alias dictionary and does not authenticate identities. Perceptual hashes are candidate generators: crops can have distant hashes, and common layouts can have close hashes.
