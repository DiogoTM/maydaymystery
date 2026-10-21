#!/usr/bin/env python3
"""Geometric feature comparison for same/near-date scans; no deletion or merging."""
from datetime import date
import itertools,json
import cv2
import numpy as np
from pipeline import ROOT,REPORTS,dump

def features(path):
    im=cv2.imread(str(ROOT/path),cv2.IMREAD_GRAYSCALE)
    s=min(1,1600/max(im.shape));im=cv2.resize(im,(round(im.shape[1]*s),round(im.shape[0]*s)))
    kp,desc=cv2.SIFT_create(nfeatures=2500).detectAndCompute(im,None)
    return kp,desc,im.shape

def compare(a,b,fa,fb):
    ka,da,sa=fa;kb,db,sb=fb
    row=dict(a=a,b=b,status='insufficient_features',good_matches=0,inliers=0)
    if da is None or db is None:return row
    pairs=cv2.BFMatcher().knnMatch(da,db,k=2)
    good=[m for ps in pairs if len(ps)==2 for m,n in [ps] if m.distance<.7*n.distance]
    row['good_matches']=len(good)
    if len(good)<8:return row
    x=np.float32([ka[m.queryIdx].pt for m in good]);y=np.float32([kb[m.trainIdx].pt for m in good])
    cv2.setRNGSeed(20261021)
    mat,mask=cv2.findHomography(x,y,cv2.RANSAC,4)
    if mat is None:return row
    ix=mask.ravel().astype(bool);n=int(ix.sum());row.update(inliers=n,inlier_fraction=round(n/len(good),3),status='shared_visual_region_candidate')
    for label,points,shape in [('a',x[ix],sa),('b',y[ix],sb)]:
        area=cv2.contourArea(cv2.convexHull(points)) if len(points)>=3 else 0
        row[label+'_feature_coverage']=round(area/(shape[0]*shape[1]),3)
    row['strong_registration']=n>=25 and n/len(good)>=.5 and max(row['a_feature_coverage'],row['b_feature_coverage'])>=.15
    row['warning']='Registration demonstrates shared pixels/features, not necessarily the same full advertisement; repeated portraits and logos are possible.'
    return row

def main():
    rows=json.loads((REPORTS/'inventory.json').read_text());scans=[r for r in rows if r['local'] and r['collection'] in ('archive_scan','researcher_scan')]
    pairs=[(a,b) for a,b in itertools.combinations(scans,2) if abs((date.fromisoformat(a['filename_date'])-date.fromisoformat(b['filename_date'])).days)<=5]
    paths={r['path'] for pair in pairs for r in pair}
    fs={path:features(path) for path in sorted(paths)};results=[]
    for a,b in pairs:results.append(compare(a['path'],b['path'],fs[a['path']],fs[b['path']]))
    dump(REPORTS/'geometric_variants.json',dict(method='SIFT ratio .7, RANSAC 4px, max side 1600; candidates within five labeled days',pairs=results))
    print(json.dumps([r for r in results if r.get('strong_registration')],indent=2))

if __name__=='__main__':main()
