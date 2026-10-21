#!/usr/bin/env python3
"""Additional script-specific region OCR; never replaces full-page raw OCR."""
import os,json,subprocess,tempfile
from PIL import Image
from pipeline import ROOT,RESEARCH,REPORTS,dump,sha

def main():
    specs=[('1989_greek','texts/My Scans/1989-05-01_page24.jpg',[.29,.742,.70,.767],'grc+eng',6),
           ('1989_hebrew','texts/My Scans/1989-05-01_page24.jpg',[.32,.728,.69,.747],'heb',6),
           ('1983_doctrine','texts/maydaymystery.org/1983-11-22.jpg',[.12,.75,.85,.84],'grc',6),
           ('1989_bottom','texts/My Scans/1989-05-01_page24.jpg',[.02,.78,.97,1],'eng+lat+deu',3)]
    results=[]
    for name,path,region,lang,psm in specs:
        source=ROOT/path
        with Image.open(source) as im:
            w,h=im.size;box=[round(region[0]*w),round(region[1]*h),round(region[2]*w),round(region[3]*h)]
            crop=im.crop(box).convert('RGB');s=max(1,min(3,2200/max(crop.size)));crop=crop.resize((round(crop.width*s),round(crop.height*s)))
            with tempfile.NamedTemporaryFile(suffix='.png') as f:
                crop.save(f.name);r=subprocess.run(['tesseract',f.name,'stdout','--tessdata-dir',str(RESEARCH/'tools/tessdata'),'-l',lang,'--psm',str(psm)],capture_output=True,text=True,timeout=60,env={**os.environ,'OMP_THREAD_LIMIT':'1'})
        results.append(dict(id=name,source=path,source_sha256=sha(source),source_bbox=box,languages=lang,psm=psm,tool='tesseract',text=r.stdout,stderr=r.stderr,returncode=r.returncode,status='additional_machine_unreviewed_not_canonical'))
    dump(REPORTS/'multilingual_regions.json',results);print([(x['id'],x['returncode']) for x in results])

if __name__=='__main__':main()
