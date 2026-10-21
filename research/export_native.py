#!/usr/bin/env python3
"""Preserve native text/values for supplemental PDFs, workbooks and text files."""
import gzip,hashlib,json
from pathlib import Path
import fitz,xlrd
from pipeline import ROOT,RESEARCH,REPORTS,ocr_one,sha,dump

def main():
    base=RESEARCH/'external/website_backup'
    sources=[ROOT/'dates.pdf',ROOT/'megamap.pdf',ROOT/'misc/exdat_notes_Charlie_Piggott.pdf']
    sources+=sorted(p for p in base.rglob('*') if p.suffix.lower() in ('.pdf','.xls','.txt','.wpd','.doc') and '/hts-cache/' not in str(p))
    results=[]
    for p in sources:
        if not p.is_file():continue
        row=dict(path=str(p.relative_to(ROOT)),sha256=sha(p),bytes=p.stat().st_size,status='native_extraction_unreviewed')
        if p.suffix.lower()=='.pdf':
            pages=[]
            with fitz.open(p) as doc:
                for i,pg in enumerate(doc):
                    page=dict(page=i+1,text=pg.get_text(),blocks=pg.get_text('blocks'),coordinate_units='PDF points',page_bounds=list(pg.rect))
                    if len(page['text'].strip())<30 and p!=ROOT/'megamap.pdf':
                        dest=RESEARCH/'derived_pdf_pages'/(row['sha256']+f'_page{i+1}.png');dest.parent.mkdir(exist_ok=True)
                        if not dest.exists():pg.get_pixmap(matrix=fitz.Matrix(2,2)).save(dest)
                        key=sha(dest);page.update(rendered_source=str(dest.relative_to(ROOT)),render_scale=2,ocr_sha256=key,
                                                 ocr_status=ocr_one(dict(path=str(dest.relative_to(ROOT)),sha256=key)))
                    elif not page['text'].strip():page['status']='image_only_research_map_native_VUE_available'
                    pages.append(page)
            row['pages']=pages
        elif p.suffix.lower()=='.xls':
            w=xlrd.open_workbook(p);row['sheets']={s.name:[s.row_values(i) for i in range(s.nrows)] for s in w.sheets()}
        elif p.suffix.lower()=='.txt':
            row['text']=p.read_text(errors='replace');row['encoding_warning']='UTF-8 replacement decoding; retain original bytes'
        else:row['status']='empty_source' if not p.stat().st_size else 'legacy_binary_conversion_pending'
        results.append(row)
    data=json.dumps(results,ensure_ascii=False,indent=2,default=str).encode()
    with (REPORTS/'native_artifacts.json.gz').open('wb') as out:
        with gzip.GzipFile(fileobj=out,mode='wb',mtime=0) as gz:gz.write(data)
    dump(REPORTS/'native_artifacts_summary.json',dict(files=len(results),legacy_pending=[r['path'] for r in results if r['status']=='legacy_binary_conversion_pending'],
         pages_ocr=sum('ocr_sha256' in p for r in results for p in r.get('pages',[]))))
    print('Native artifacts',len(results))

if __name__=='__main__':main()
