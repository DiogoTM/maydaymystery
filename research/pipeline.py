#!/usr/bin/env python3
"""Read-only evidence processing. Derived output stays in research/.

python research/pipeline.py inventory|ocr|analyze|all
python research/pipeline.py query 'quadriga*'
Dates parsed from filenames are labels, never verified publication dates.
"""
import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import date
import hashlib
import io
import itertools
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / 'research'
REPORTS = RESEARCH / 'reports'
CORPUS = RESEARCH / 'corpus'
DB = RESEARCH / 'corpus.sqlite'
REF = '2bc34341b92f4c8989779b4bb744833912bfdc50'
DATE = re.compile(r'(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)')
IMAGE = {'.jpg', '.jpeg', '.png', '.tif', '.tiff'}
ALIASES = {
 'Martin Luther': r'\bLuther\b', 'John Calvin': r'\bCalvin\b',
 'Oliver Cromwell': r'\bCromwell\b', 'Gustavus Adolphus': r'\bGustav(?:us|e)\w*\s+Adolph\w*',
 'John Winthrop': r'\bWinthrop\b', 'Orphanage': r'\bOrphanage\b',
 'Owsley': r'\bOwsley\b', 'Hannibal': r'\bHannibal\b',
 'Kitchener': r'\bKitchener\b', 'Khartoum': r'\bKhartoum\b',
 'Constantine': r'\bConstantine\b', 'Heidegger': r'\bHeidegger\b',
 'Arbella': r'\bArbella\b', 'quadrigae': r'\bquadriga\w*',
 'Leitmotiv': r'\bLeitmotiv\b', 'SR/CL': r'\bSR\s*[/|]\s*CL\b',
 'Bible': r'\b(?:Revelation|Ephesians|Romans|Corinthians|Deuteronomy|Isaiah|Matthew)\b',
}

def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf8')

def csv_write(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf8') as f:
        w=csv.DictWriter(f, fields, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def label_date(path):
    m=DATE.search(Path(path).name)
    if not m: return None
    try: return date.fromisoformat(m[1]).isoformat()
    except ValueError: return None

def collection(path):
    if path.startswith('texts/maydaymystery.org/') and Path(path).suffix.lower() in IMAGE: return 'archive_scan'
    if path.startswith('texts/My Scans/') and Path(path).suffix.lower() in IMAGE: return 'researcher_scan' if label_date(path) else 'preview'
    if path.startswith('megamap_files/'): return 'research_crop'
    if path.startswith('art/'): return 'art'
    if Path(path).suffix.lower()=='.pdf': return 'research_pdf'
    return 'research_artifact'

def image_hash(path):
    from PIL import Image, ImageOps
    import numpy as np
    from scipy.fft import dctn
    with Image.open(path) as im:
        im=ImageOps.exif_transpose(im).convert('L'); size=im.size
        a=np.asarray(im.resize((32,32)), dtype=float)
        d=dctn(a,norm='ortho')[:8,:8].ravel()
        bits=d>np.median(d[1:]); bits[0]=False
        ph=sum(int(v)<<i for i,v in enumerate(bits))
        a=np.asarray(im.resize((9,8)),dtype=int)
        dh=sum(int(v)<<i for i,v in enumerate((a[:,1:]>a[:,:-1]).ravel()))
        return size, f'{ph:016x}', f'{dh:016x}'

def inventory():
    tree=json.loads((RESEARCH/'provenance/repository_tree.json').read_text())
    assert tree['truncated'] is False, 'Refuse incomplete tree'
    rows=[]
    for f in tree['tree']:
        if f['type']!='blob': continue
        p=ROOT/f['path']; present=p.is_file()
        row=dict(path=f['path'],collection=collection(f['path']),filename_date=label_date(f['path']),
                 publication_date=None,date_status='filename_only' if label_date(f['path']) else 'undated',
                 remote_git_blob=f['sha'],remote_bytes=f.get('size'),local=present,
                 source_url=f'https://github.com/DiogoTM/maydaymystery/blob/{REF}/'+f['path'].replace(' ','%20'),
                 retrieved_utc='2026-10-21' if present else None,sha256=None,git_verified=False)
        if present:
            b=p.read_bytes(); row['sha256']=sha(p); row['local_bytes']=len(b)
            row['git_verified']=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['sha']
            if p.suffix.lower() in IMAGE:
                try:
                    size,ph,dh=image_hash(p); row.update(width=size[0],height=size[1],phash=ph,dhash=dh)
                except Exception as e: row['image_error']=str(e)
        rows.append(row)
    dump(REPORTS/'inventory.json',rows)
    csv_write(REPORTS/'inventory.csv',rows,list(dict.fromkeys(k for r in rows for k in r)))
    by_hash=defaultdict(list); by_git=defaultdict(list); by_date=defaultdict(list)
    for r in rows:
        by_git[r['remote_git_blob']].append(r['path'])
        if r['sha256']: by_hash[r['sha256']].append(r['path'])
        if r['filename_date'] and r['collection'] in ('archive_scan','researcher_scan'):
            by_date[r['filename_date']].append(r['path'])
    scans=[r for r in rows if r['collection'] in ('archive_scan','researcher_scan')]
    pairs=[]
    for a,b in itertools.combinations([r for r in scans if r.get('phash')],2):
        h=(int(a['phash'],16)^int(b['phash'],16)).bit_count()
        dh=(int(a['dhash'],16)^int(b['dhash'],16)).bit_count()
        if h<=12 or a['filename_date']==b['filename_date']:
            pairs.append(dict(a=a['path'],b=b['path'],phash_distance=h,dhash_distance=dh,
                              status='candidate_requires_visual_review',same_date=a['filename_date']==b['filename_date']))
    dump(REPORTS/'perceptual_candidates.json',sorted(pairs,key=lambda x:x['phash_distance']))
    summary=dict(remote_files=len(rows),remote_bytes=sum(r['remote_bytes'] for r in rows),
        local_files=sum(r['local'] for r in rows),verified_files=sum(r['git_verified'] for r in rows),
        collections=dict(Counter(r['collection'] for r in rows)),
        accessible_scans=sum(r['local'] for r in scans),remote_scan_files=len(scans),
        scan_filename_dates=len(by_date),sha256_duplicate_groups=[v for v in by_hash.values() if len(v)>1],
        remote_git_duplicate_groups=[v for v in by_git.values() if len(v)>1],
        same_date_groups={k:v for k,v in by_date.items() if len(v)>1},
        missing_local=[r['path'] for r in rows if not r['local']],
        limitations=['Remote Git blob identifiers are not local SHA-256 verification.',
        'Date labels are not proof of publication date or distinct advertisements.',
        'Perceptual hashes produce candidates, not automatic duplicate decisions.',
        'No crops or layouts are removed from the source collection.'])
    dump(REPORTS/'inventory_summary.json',summary)
    print(json.dumps({k:summary[k] for k in ['remote_files','local_files','verified_files','accessible_scans','remote_scan_files','scan_filename_dates']}))

def ocr_one(row):
    from PIL import Image, ImageOps
    p=ROOT/row['path']; key=row['sha256']; out=CORPUS/key
    marker=out.with_suffix('.json')
    if marker.exists(): return 'cached'
    out.parent.mkdir(parents=True,exist_ok=True)
    # Derived resizing only. OCR coordinates are rescaled back to source pixels.
    with Image.open(p) as im:
        im=ImageOps.exif_transpose(im).convert('RGB'); width,height=im.size
        scale=min(1,3600/max(im.size)); im=im.resize((round(width*scale),round(height*scale)))
        target=out.with_suffix('.png'); im.save(target)
    try:
        proc=subprocess.run(['tesseract',str(target),str(out),'-l','eng','--psm','3','txt','tsv','hocr'],
                            capture_output=True,text=True,timeout=60,
                            env={**os.environ,'OMP_THREAD_LIMIT':'1'})
        if proc.returncode: raise RuntimeError(proc.stderr)
        words=[]
        with out.with_suffix('.tsv').open() as f:
            for w in csv.DictReader(f,delimiter='\t'):
                if not (w.get('text') or '').strip(): continue
                conf=float(w['conf'])
                words.append(dict(text=w['text'],confidence=conf,
                    bbox=[round(int(w[k])/scale) for k in ('left','top','width','height')],
                    page=int(w['page_num']),block=int(w['block_num']),paragraph=int(w['par_num']),line=int(w['line_num']),
                    uncertain=conf<70))
        data=dict(source_path=row['path'],source_sha256=key,source_dimensions=[width,height],
                  tool='tesseract',language_models=['eng'],psm=3,scale=scale,
                  coordinates='source pixels: x,y,width,height; EXIF-oriented',
                  extraction_status='machine_unreviewed',words=words,
                  warnings=['English model only; non-Latin scripts, mathematics and symbols are unreliable.',
                            'TSV confidence is engine confidence, not probability of correct reading.',
                            'Layout grouping is engine-generated; reading order requires review.'],
                  text=out.with_suffix('.txt').read_text(),stderr=proc.stderr)
        dump(marker,data)
        out.with_suffix('.error.json').unlink(missing_ok=True)
        return 'processed'
    except Exception as e:
        dump(out.with_suffix('.error.json'),dict(path=row['path'],error=str(e))); return 'error'
    finally: target.unlink(missing_ok=True)

def ocr():
    rows=json.loads((REPORTS/'inventory.json').read_text())
    rows=[r for r in rows if r['local'] and r['collection'] in ('archive_scan','researcher_scan','research_crop')]
    unique={r['sha256']:r for r in rows}
    with ThreadPoolExecutor(max_workers=3) as pool:
        results=list(pool.map(ocr_one,unique.values()))
    dump(REPORTS/'ocr_run.json',dict(results=Counter(results),requested=len(rows),unique_sources=len(unique)))
    print(dict(Counter(results)))

def references(text):
    """Ambiguous short dates retained as candidates with context, not asserted edges."""
    found=[]
    for m in re.finditer(r'(?<![\d/])(\d{1,2})\s*/\s*(\d{1,2})\s*/\s*(\d{2}|\d{4})(?!\d)',text):
        mo,da,yr=map(int,m.groups()); yr=yr+1900 if yr<81 else yr+1900 if yr<100 else yr
        # No century inference beyond the historical 1981-1999 range.
        if len(m[3])==2 and int(m[3])<81:
            found.append(dict(raw=m[0],target_date=None,start=m.start(),status='ambiguous_century',context=text[max(0,m.start()-90):m.end()+90]));continue
        try: target=date(yr,mo,da).isoformat()
        except ValueError: continue
        context=text[max(0,m.start()-90):m.end()+90]
        found.append(dict(raw=m[0],target_date=target,start=m.start(),context=context,status='date_candidate',
                          explicit_adw=bool(re.search(r'\b(?:A\.?\s*D\.?\s*W\.?|Wildcat)\b',context,re.I))))
    return found

def map_extract():
    raw=(ROOT/'megamap.vue').read_text(); raw=raw[raw.index('<?xml'):]
    root=ET.fromstring(raw); xsi='{http://www.w3.org/2001/XMLSchema-instance}type'
    nodes=[]; edges=[]
    for c in root.iter('child'):
        node=dict(id=c.get('ID'),label=c.get('label'),type=c.get(xsi),x=c.get('x'),y=c.get('y'),
                  notes=c.findtext('notes'),resources=[r.get('spec') for r in c.findall('resource')])
        if c.get(xsi)=='link':
            node.update(source=c.findtext('ID1'),target=c.findtext('ID2')); edges.append(node)
        else: nodes.append(node)
    dump(REPORTS/'prior_megamap.json',dict(provenance='megamap.vue; prior researcher assertions, not independently confirmed',nodes=nodes,edges=edges))
    return nodes,edges

def analyze():
    rows=json.loads((REPORTS/'inventory.json').read_text()); scans=[r for r in rows if r['collection'] in ('archive_scan','researcher_scan')]
    con=sqlite3.connect(DB)
    con.executescript('''DROP TABLE IF EXISTS files; DROP TABLE IF EXISTS documents; DROP TABLE IF EXISTS words;
    DROP TABLE IF EXISTS mentions; DROP TABLE IF EXISTS reference_candidates; DROP TABLE IF EXISTS search;
    CREATE TABLE files(path TEXT PRIMARY KEY, collection TEXT, filename_date TEXT, publication_date TEXT, sha256 TEXT, local INTEGER, git_verified INTEGER, source_url TEXT);
    CREATE TABLE documents(id TEXT PRIMARY KEY, date_label TEXT, text TEXT, status TEXT);
    CREATE TABLE words(document_id TEXT, ordinal INTEGER, text TEXT, confidence REAL, x INTEGER, y INTEGER, width INTEGER, height INTEGER, block INTEGER, line INTEGER, uncertain INTEGER);
    CREATE TABLE mentions(document_id TEXT, entity TEXT, surface TEXT, offset INTEGER, bbox TEXT, status TEXT);
    CREATE TABLE reference_candidates(document_id TEXT, target_date TEXT, raw TEXT, context TEXT, status TEXT, explicit_adw INTEGER);
    CREATE VIRTUAL TABLE search USING fts5(document_id UNINDEXED,text, tokenize='unicode61');''')
    for r in rows:
        con.execute('INSERT INTO files VALUES(?,?,?,?,?,?,?,?)',tuple(r.get(k) for k in ('path','collection','filename_date','publication_date','sha256','local','git_verified','source_url')))
    texts={}; ents=defaultdict(set); refs=[]; nums=[]; review=[]
    for r in scans:
        if not r['local']: continue
        p=CORPUS/(r['sha256']+'.json')
        if not p.exists(): continue
        d=json.loads(p.read_text()); key=r['sha256']
        if key in texts: continue
        text=d['text']; texts[key]=dict(date=r['filename_date'],text=text,path=r['path'])
        con.execute('INSERT INTO documents VALUES(?,?,?,?)',(key,r['filename_date'],text,d['extraction_status']))
        con.execute('INSERT INTO search VALUES(?,?)',(key,text))
        for i,w in enumerate(d['words']):
            con.execute('INSERT INTO words VALUES(?,?,?,?,?,?,?,?,?,?,?)',(key,i,w['text'],w['confidence'],*w['bbox'],w['block'],w['line'],w['uncertain']))
        for entity,pattern in ALIASES.items():
            for m in re.finditer(pattern,text,re.I):
                ents[entity].add(key)
                boxes=[w['bbox'] for w in d['words'] if re.search(pattern,w['text'],re.I)]
                con.execute('INSERT INTO mentions VALUES(?,?,?,?,?,?)',(key,entity,m[0],m.start(),json.dumps(boxes),'machine_candidate'))
        for ref in references(text):
            ref.update(document_id=key,source_path=r['path'],source_date=r['filename_date']);refs.append(ref)
            con.execute('INSERT INTO reference_candidates VALUES(?,?,?,?,?,?)',(key,ref['target_date'],ref['raw'],ref['context'],ref['status'],ref.get('explicit_adw',False)))
        for w in d['words']:
            if re.search(r'\d|[∫Σ∞=°±√]',w['text']): nums.append(dict(document_id=key,source_path=r['path'],**w))
        uncertain=sum(w['uncertain'] for w in d['words'])
        review.append(dict(path=r['path'],sha256=key,words=len(d['words']),uncertain_words=uncertain,uncertain_fraction=round(uncertain/max(1,len(d['words'])),3)))
    con.commit(); con.close()
    dump(REPORTS/'reference_candidates.json',refs);dump(REPORTS/'numeric_symbol_candidates.json',nums)
    csv_write(REPORTS/'review_queue.csv',sorted(review,key=lambda r:-r['uncertain_fraction']),['path','sha256','words','uncertain_words','uncertain_fraction'])
    entity_rows=[dict(entity=e,documents=[dict(id=k,date=texts[k]['date'],path=texts[k]['path']) for k in sorted(ks)]) for e,ks in sorted(ents.items(),key=lambda p:-len(p[1]))]
    dump(REPORTS/'entity_relationships.json',entity_rows)
    # Count phrase recurrence once per labeled date to limit scan-variant inflation.
    phrases=defaultdict(dict)
    for k,d in texts.items():
        tokens=re.findall(r"[a-z]+(?:'[a-z]+)?",d['text'].lower())
        for gram in set(tuple(tokens[i:i+5]) for i in range(len(tokens)-4)):
            phrases[' '.join(gram)][d['date']]=d['path']
    repeated=[dict(phrase=p,date_count=len(ds),sources=ds) for p,ds in phrases.items() if len(ds)>=3]
    dump(REPORTS/'repeated_phrases.json',sorted(repeated,key=lambda x:(-x['date_count'],x['phrase'])))
    nodes,edges=map_extract()
    dump(REPORTS/'analysis_summary.json',dict(ocr_scan_documents=len(texts),reference_candidates=len(refs),
        entity_counts={e:len(ks) for e,ks in ents.items()},repeated_5grams=len(repeated),
        prior_map_nodes=len(nodes),prior_map_edges=len(edges),
        limitation='English OCR and finite alias dictionary; candidates require primary-image review. No claim of complete entity or cipher extraction.'))
    print(json.dumps(json.loads((REPORTS/'analysis_summary.json').read_text())))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['inventory','ocr','analyze','all','query']);ap.add_argument('query',nargs='?');a=ap.parse_args()
    REPORTS.mkdir(parents=True,exist_ok=True);CORPUS.mkdir(parents=True,exist_ok=True)
    if a.action=='query':
        with sqlite3.connect(DB) as con:
            for row in con.execute('SELECT f.filename_date,f.path,snippet(search,1,\'[\',\']\',\'…\',30) FROM search JOIN files f ON f.sha256=search.document_id WHERE search MATCH ?',(a.query,)): print(*row,sep=' | ')
        return
    for name in (['inventory','ocr','analyze'] if a.action=='all' else [a.action]): globals()[name]()

if __name__=='__main__': main()
