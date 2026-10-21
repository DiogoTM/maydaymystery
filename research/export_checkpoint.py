#!/usr/bin/env python3
"""Export native artifacts and portable text view without rewriting evidence."""
import json
from pipeline import ROOT, RESEARCH, REPORTS, dump

def main():
    out=[]
    try:
        import fitz
        p=ROOT/'dates.pdf'
        if p.exists():
            with fitz.open(p) as d:
                out.append(dict(source=p.name,status='native_text_unreviewed',pages=[dict(page=i+1,text=page.get_text(),blocks=page.get_text('blocks')) for i,page in enumerate(d)]))
    except ImportError: out.append(dict(source='dates.pdf',status='missing_optional_PyMuPDF'))
    try:
        import openpyxl
        p=ROOT/'dates.xlsx'
        if p.exists():
            w=openpyxl.load_workbook(p,read_only=True,data_only=False)
            out.append(dict(source=p.name,status='spreadsheet_values_unreviewed',sheets={s.title:[list(row) for row in s.iter_rows(values_only=True)] for s in w}));w.close()
    except ImportError: out.append(dict(source='dates.xlsx',status='missing_optional_openpyxl'))
    # Datetimes become ISO strings; original workbook remains the source.
    (REPORTS/'artifact_extractions.json').write_text(json.dumps(out,default=str,ensure_ascii=False,indent=2)+'\n')
    rows=json.loads((REPORTS/'inventory.json').read_text());docs=[]
    for r in rows:
        if not r['local'] or r['collection'] not in ('archive_scan','researcher_scan'):continue
        p=RESEARCH/'corpus'/(r['sha256']+'.json')
        if not p.exists():continue
        d=json.loads(p.read_text())
        docs.append(dict(source_path=r['path'],source_url=r['source_url'],source_sha256=r['sha256'],
            filename_date=r['filename_date'],publication_date=r['publication_date'],status='machine_unreviewed',
            language_model='eng',text=d['text'],word_count=len(d['words']),
            uncertain_word_count=sum(w['uncertain'] for w in d['words']),coordinate_extraction='corpus/'+r['sha256']+'.json'))
    (REPORTS/'transcripts.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in docs))

if __name__=='__main__':main()
