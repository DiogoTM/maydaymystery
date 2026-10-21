# Mayday archive audit (initial phase)

This folder contains **our independent research tooling**, not a claim that the Mayday Mystery has been solved.

## Verified repository inventory (GitHub tree, 2026-10-20)

- `texts/maydaymystery.org/`: **107 JPG files**. Of these, 102 have an exact `YYYY-MM-DD.jpg` filename; five are supplementary page/colour variants.
- `texts/My Scans/`: **26 dated JPG scans**, plus one `preview.jpg` (not counted as a dated scan).
- These are counts of files, **not distinct advertisements**.
- The original archive runs from **1981 to 2019**; its lack of entries after 2019 does not mean nothing was published.
- The 1989-05-01 scan exists in both archive collections; these may be different resolutions or crops. Exact-byte duplication must be tested locally.

## Reproducible audit

Run from the repository root:

```bash
python3 research/audit_scans.py
```

The tool generates `research/reports/scan_inventory.csv` (source, date, SHA-256, bytes) and `research/reports/audit_summary.json` (file counts, candidate same-date variants, exact SHA-256 duplicates). No third-party packages, internet connection, or AI services are needed.

## Research safeguards

Do not infer that files with different hashes are necessarily different advertisements. Keep each original scan immutable; preserve provenance and citations. Any proposed interpretation must record primary evidence, counterexamples, and confidence. Do not auto-upload unpublished/private correspondence.

## Next phase

1. Run the audit and review the CSV.
2. Assemble an independently sourced dated publication ledger and produce a *grounded* missing-date report.
3. Transcribe originals with page regions and review uncertainty manually.
4. Extract cross-document references and test interpretations against held-out issues.
