#!/usr/bin/env python3
"""Index frozen public website evidence separately from primary scan OCR."""
from collections import Counter
from datetime import date
from html.parser import HTMLParser
import hashlib,json,re,sqlite3
from pathlib import Path
from urllib.parse import urljoin
from pipeline import RESEARCH,REPORTS,dump,csv_write

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.parts=[];self.links=[];self.images=[];self.skip=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('script','style'):self.skip+=1
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='img' and a.get('src'):self.images.append(a['src'])
        if tag in ('br','p','pre','li','hr','h1','h2','h3','tr'):self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.skip=max(0,self.skip-1)
        if tag in ('p','pre','li','h1','h2','h3','tr'):self.parts.append('\n')
    def handle_data(self,data):
        if not self.skip:self.parts.append(data)
    def text(self):return re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+','\n\n',''.join(self.parts)).strip()

MONTHS={'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
def page_date(name):
    m=re.fullmatch(r'(\d{2})-(jan\w*|feb\w*|mar\w*|apr\w*|may|jun\w*|jul\w*|aug\w*|sep\w*|oct\w*|nov\w*|dec\w*)(\d{1,2})\.html',name,re.I)
    if not m:return None
    y=int(m[1]);y+=1900 if y>=70 else 2000
    try:return date(y,MONTHS[m[2][:3].lower()],int(m[3])).isoformat()
    except ValueError:return None

def main():
    root=RESEARCH/'external/website_backup';rows=[];leads=[]
    for p in sorted(root.rglob('*.html')):
        raw=p.read_bytes();s=raw.decode('utf8',errors='replace');parser=Page();parser.feed(s)
        match=re.search(r'Mirrored from ([^\s]+)',s)
        fallback=str(p).split('/maydaymirror/')[-1]
        url=('http://'+match[1]) if match and not match[1].startswith('http') else (match[1] if match else 'http://'+fallback)
        d=page_date(p.name);text=parser.text()
        kind='advertisement_context_mixed_with_reader_comments' if d else 'correspondence_or_research_page_unclassified'
        if p.name.startswith('friend'):kind='attributed_correspondence_with_possible_editorial_comment'
        row=dict(id=hashlib.sha256(raw).hexdigest(),path=str(p.relative_to(RESEARCH)),original_url=url,
            container_date='2020-02-28',date_label=d,date_status='filename_label_only',kind=kind,text=text,
            encoding_replacements=s.count('\ufffd'),images=[urljoin(url,x) for x in parser.images],
            local_image_paths=[str((p.parent/x).resolve().relative_to(RESEARCH)) if (p.parent/x).resolve().is_relative_to(RESEARCH) else None for x in parser.images],
            links=[urljoin(url,x) for x in parser.links if not x.startswith('javascript:')])
        rows.append(row)
        for m in re.finditer(r'quadrigae|scordatur\w*|first level is always|phase shifts',text,re.I):
            leads.append(dict(path=row['path'],original_url=url,offset=m.start(),context=text[max(0,m.start()-220):m.end()+400],
                              status='source_statement_or_reader_comment_not_authenticated',kind=kind))
    (REPORTS/'website_pages.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    dump(REPORTS/'website_method_leads.json',leads)
    dated=[{k:r[k] for k in ('path','id','original_url','date_label','kind','images','local_image_paths')} for r in rows if r['date_label']]
    dump(REPORTS/'website_ad_context_index.json',dated)
    con=sqlite3.connect(RESEARCH/'corpus.sqlite')
    con.executescript('DROP TABLE IF EXISTS web_pages;DROP TABLE IF EXISTS web_search;CREATE TABLE web_pages(id TEXT,path TEXT,original_url TEXT,date_label TEXT,kind TEXT,text TEXT);CREATE VIRTUAL TABLE web_search USING fts5(id UNINDEXED,text);')
    for r in rows:
        con.execute('INSERT INTO web_pages VALUES(?,?,?,?,?,?)',tuple(r[k] for k in ('id','path','original_url','date_label','kind','text')))
        con.execute('INSERT INTO web_search VALUES(?,?)',(r['id'],r['text']))
    con.commit();con.close()
    summary=dict(html_pages=len(rows),unique_page_hashes=len({r['id'] for r in rows}),dated_ad_context_pages=len(dated),
                 date_labels=len({r['date_label'] for r in dated}),kinds=dict(Counter(r['kind'] for r in rows)),
                 pages_with_decode_replacements=sum(r['encoding_replacements']>0 for r in rows),method_leads=len(leads),
                 limitation='Page text mixes prior researchers, attributed correspondence, and editorial commentary; it is never substituted for primary scan text. Sender identities unauthenticated.')
    dump(REPORTS/'website_summary.json',summary);print(json.dumps(summary))

if __name__=='__main__':main()
