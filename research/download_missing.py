#!/usr/bin/env python3
"""Recover missing snapshot files at <=1 request/second. Never overwrite a file.

Requires ordinary HTTPS connectivity. Does not bypass access restrictions. Git LFS
pointers are preserved as pointers; their external targets are not silently fetched.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
from pipeline import ROOT, RESEARCH, REF

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--limit',type=int,default=40);a=ap.parse_args()
    tree=json.loads((RESEARCH/'provenance/repository_tree.json').read_text())
    log=RESEARCH/'provenance/http_retrievals.jsonl'; attempted=0
    for f in tree['tree']:
        p=ROOT/f['path']
        if f['type']!='blob' or p.exists(): continue
        if attempted>=a.limit: break
        attempted+=1
        url=f'https://raw.githubusercontent.com/DiogoTM/maydaymystery/{REF}/'+quote(f['path'],safe='/')
        record=dict(url=url,path=f['path'],retrieved_utc=datetime.now(timezone.utc).isoformat(),git_blob_expected=f['sha'])
        stop=False
        try:
            with urlopen(Request(url,headers={'User-Agent':'MaydayResearch/0.1 (public archival research; max 1 request/second)'}),timeout=30) as response:
                b=response.read(32*1024*1024+1)
                if len(b)>32*1024*1024: raise ValueError('File exceeds 32 MiB retrieval cap')
                git=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
                if git!=f['sha'] or len(b)!=f['size']: raise ValueError('Snapshot byte count or Git blob hash mismatch')
                p.parent.mkdir(parents=True,exist_ok=True)
                with p.open('xb') as out: out.write(b)
                record.update(status='verified',sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
        except HTTPError as e:
            record.update(status='http_error',code=e.code);stop=e.code in (401,403,429)
        except (URLError,OSError,ValueError) as e:
            record.update(status='error',error=str(e));stop=True
        with log.open('a') as out: out.write(json.dumps(record)+'\n')
        print(f['path'],record['status'])
        if stop: break
        time.sleep(1)

if __name__=='__main__': main()
