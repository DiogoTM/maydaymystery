#!/usr/bin/env python3
"""Recover pinned scientific references and OCR models from recorded public URLs."""
import hashlib,json,time
from pathlib import Path
from urllib.request import Request,urlopen
from pipeline import RESEARCH

def main():
    records=json.loads((RESEARCH/'provenance/reference_retrievals.json').read_text())
    for r in json.loads((RESEARCH/'provenance/ocr_models.json').read_text()):
        if 'sha256' in r:records.append({**r,'path':'tools/tessdata/'+r['language']+'.traineddata'})
    for r in records:
        if 'sha256' not in r:continue
        p=(RESEARCH/r['path']).resolve();assert p.is_relative_to(RESEARCH)
        if p.exists():
            assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],str(p)
            continue
        with urlopen(Request(r['url'],headers={'User-Agent':'MaydayResearch/0.2'}),timeout=30) as response:b=response.read(32*1024*1024+1)
        assert len(b)<=32*1024*1024 and hashlib.sha256(b).hexdigest()==r['sha256'],'Asset differs from recorded version'
        p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f:f.write(b)
        print(r['path']);time.sleep(1)

if __name__=='__main__':main()
