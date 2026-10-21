#!/usr/bin/env python3
"""OCR historical Mayday-site images; preserve separate provenance from repository scans."""
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,sqlite3
from pathlib import Path
from pipeline import ROOT,RESEARCH,REPORTS,CORPUS,ocr_one,dump

def safe_ocr(row):
    try:return ocr_one(row)
    except Exception as e:
        dump(CORPUS/(row['sha256']+'.error.json'),dict(path=row['path'],error=str(e)))
        return 'error'

def main():
    inv=json.loads((REPORTS/'website_backup_inventory.json').read_text());rows=[]
    for f in inv:
        if '/mayday/' not in f['path'] or Path(f['path']).suffix.lower() not in {'.jpg','.gif','.png','.tif','.tiff'}:continue
        rows.append(dict(path='research/'+f['path'],sha256=f['sha256'],collection='website_image_unclassified',
                         bytes=f['bytes'],original_url='http://'+f['path'].split('/maydaymirror/')[-1],
                         captured_html_placeholder=(RESEARCH/f['path']).read_bytes()[:40].lstrip().upper().startswith(b'<HTML>'),
                         role='advertisement_correspondence_or_attachment_requires_context_review'))
    unique={r['sha256']:r for r in rows if not r['captured_html_placeholder']};counts={}
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures={pool.submit(safe_ocr,r):r for r in unique.values()}
        for i,future in enumerate(as_completed(futures),1):
            status=future.result();counts[status]=counts.get(status,0)+1
            if i%50==0:print(i,'/',len(unique),counts,flush=True)
    con=sqlite3.connect(RESEARCH/'corpus.sqlite')
    con.executescript('DROP TABLE IF EXISTS web_images;DROP TABLE IF EXISTS web_ocr_search;CREATE TABLE web_images(path TEXT,original_url TEXT,sha256 TEXT,status TEXT,text TEXT);CREATE VIRTUAL TABLE web_ocr_search USING fts5(sha256 UNINDEXED,text);')
    for r in rows:
        p=CORPUS/(r['sha256']+'.json');d=json.loads(p.read_text()) if p.exists() else None
        status='captured_html_placeholder_not_an_image' if r['captured_html_placeholder'] else ('machine_unreviewed' if d else 'extraction_failed')
        con.execute('INSERT INTO web_images VALUES(?,?,?,?,?)',(r['path'],r['original_url'],r['sha256'],status,d['text'] if d else None))
    for key in unique:
        p=CORPUS/(key+'.json')
        if p.exists():con.execute('INSERT INTO web_ocr_search VALUES(?,?)',(key,json.loads(p.read_text())['text']))
    con.commit();con.close()
    dump(REPORTS/'website_image_manifest.json',rows)
    summary=dict(image_files=len(rows),unique_image_hashes=len(unique),run_results=counts,
        captured_html_placeholders=sum(r['captured_html_placeholder'] for r in rows),
        successful_unique_images=sum((CORPUS/(key+'.json')).exists() for key in unique),
        limitation='Single-frame English OCR of unclassified historical images, not verified transcriptions; GIF animation frames and foreign scripts require review.')
    dump(REPORTS/'website_ocr_summary.json',summary);print(summary,flush=True)

if __name__=='__main__':main()
