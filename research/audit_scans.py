#!/usr/bin/env python3
"""Audit local Mayday image corpus. Standard library only; no uploads or network."""
from pathlib import Path
from collections import defaultdict
from hashlib import sha256
import argparse, csv, json, re

DATE = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2})")
EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".pdf"}

def sha(path):
    h=sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--output", type=Path, default=Path("research/reports"))
    args=p.parse_args()
    root=args.repo.resolve()
    out=(root/args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rows=[]
    for folder,group in [("texts/maydaymystery.org","original_archive"),("texts/My Scans","researcher_scans")]:
        d=root/folder
        if not d.exists(): continue
        for f in sorted(d.rglob("*")):
            if not f.is_file() or f.suffix.lower() not in EXTS: continue
            m=DATE.search(f.name)
            if not m: continue # excludes contact sheets and previews
            rows.append({"date":m.group("date"),"collection":group,"path":f.relative_to(root).as_posix(),"sha256":sha(f),"bytes":f.stat().st_size})
    by_date=defaultdict(list); by_hash=defaultdict(list)
    for row in rows:
        by_date[row["date"]].append(row["path"])
        by_hash[row["sha256"]].append(row["path"])
    with (out/"scan_inventory.csv").open("w",newline="",encoding="utf-8") as fh:
        w=csv.DictWriter(fh,fieldnames=["date","collection","path","sha256","bytes"])
        w.writeheader();w.writerows(rows)
    summary={
        "source":"local repository files; not a census of all published Mayday advertisements",
        "scan_file_count":len(rows),
        "distinct_dates":len(by_date),
        "original_archive_files":sum(r["collection"]=="original_archive" for r in rows),
        "researcher_scan_files":sum(r["collection"]=="researcher_scans" for r in rows),
        "sha256_exact_duplicate_groups":[v for v in by_hash.values() if len(v)>1],
        "dates_with_multiple_files":{k:v for k,v in sorted(by_date.items()) if len(v)>1},
        "years_covered":sorted({r["date"][:4] for r in rows}),
        "limitations":["Different scans of the same advertisement may have different hashes.","Missing years and dates cannot be established without a trusted independent publication ledger.","The script does not transcribe or interpret the images."]
    }
    (out/"audit_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k not in ("dates_with_multiple_files","sha256_exact_duplicate_groups")},indent=2))
if __name__=="__main__": main()

