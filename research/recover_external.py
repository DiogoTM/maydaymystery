#!/usr/bin/env python3
"""Reproduce public IA website backup recovery. Downloads ~463 MB once; no live-site crawl."""
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path,PurePosixPath
from urllib.request import Request,urlopen
import py7zr
from pipeline import RESEARCH,REPORTS,dump

EXPECTED='2cc938d3bfd8eb751f9d5047a9dc7ef9d5aee8a9266ec5a0a1ec4302efdc6309'
URL='https://archive.org/download/MayDayMystery/backups/MayDayMirror_2020-02-28.7z'

def main():
    out=RESEARCH/'external';out.mkdir(exist_ok=True);archive=out/'MayDayMirror_2020-02-28.7z'
    if not archive.exists():
        partial=out/'MayDayMirror_2020-02-28.partial';n=0
        with urlopen(Request(URL,headers={'User-Agent':'MaydayResearch/0.2'}),timeout=30) as response,partial.open('wb') as f:
            while True:
                b=response.read(1024*1024)
                if not b:break
                n+=len(b)
                if n>600*1024*1024:raise ValueError('600 MiB retrieval cap')
                f.write(b)
        if hashlib.sha256(partial.read_bytes()).hexdigest()!=EXPECTED:raise ValueError('Archive hash mismatch; not extracted')
        partial.rename(archive)
        dump(RESEARCH/'provenance/ia_mirror_retrieval.json',dict(url=URL,retrieved_utc=datetime.now(timezone.utc).isoformat(),sha256=EXPECTED,bytes=n))
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==EXPECTED
    dest=out/'website_backup'
    with py7zr.SevenZipFile(archive) as z:
        members=z.list()
        assert sum(f.uncompressed or 0 for f in members)<1024**3
        for f in members:
            path=PurePosixPath(f.filename)
            assert not path.is_absolute() and '..' not in path.parts
        # Never overwrite extracted original files. A partially extracted directory
        # must be repaired into a separate destination, then compared manually.
        if not dest.exists():z.extractall(dest)
    rows=[dict(path=str(p.relative_to(RESEARCH)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),container_sha256=EXPECTED) for p in sorted(dest.rglob('*')) if p.is_file()]
    dump(REPORTS/'website_backup_inventory.json',rows);print('Inventoried',len(rows),'preserved files')

if __name__=='__main__':main()
