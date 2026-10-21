#!/usr/bin/env python3
"""Reproduce conservative coverage comparison and explicit hypothesis checks."""
from collections import Counter
from datetime import datetime, timedelta
import json
from pathlib import Path
import random
import re
import sqlite3
from pipeline import ROOT, RESEARCH, REPORTS, dump, csv_write

def coverage():
    web=json.loads((RESEARCH/'provenance/web_initial.json').read_text())
    text='\n'.join(c.get('text','') for c in web['content'])
    srcl=sorted(set(re.findall(r'L\d+:\s+\d+\.\s+.*?(\d{4}-\d{2}-\d{2}):',text)))
    assert len(srcl)==127, 'Finding aid extraction incomplete; do not publish false gaps'
    rows=json.loads((REPORTS/'inventory.json').read_text())
    scans=[r for r in rows if r['collection'] in ('archive_scan','researcher_scan')]
    labels={r['filename_date'] for r in scans}; local={r['filename_date'] for r in scans if r['local']}
    out=[]
    for d in sorted(set(srcl)|labels):
        paths=[r['path'] for r in scans if r['filename_date']==d]
        out.append(dict(date=d,srcl_position=d in srcl,repository_filename=d in labels,local_scan=d in local,
                        status='matching_label' if d in srcl and d in labels else 'unmatched_date_requires_reconciliation',paths=paths))
    dump(REPORTS/'coverage.json',dict(source='https://srcl.net/corpus',source_snapshot='research/provenance/web_initial.json',
         srcl_positions=len(srcl),repository_scan_date_labels=len(labels),
         srcl_dates_without_repository_label=sorted(set(srcl)-labels),
         repository_labels_absent_from_srcl=sorted(labels-set(srcl)),
         caveat='Not a list of proven missing advertisements: thematic and publication dates can differ. SR/CL records are independently claimed, most scans withheld. No automatic fuzzy-date merging.',positions=out))
    csv_write(REPORTS/'chronology.csv',out,['date','srcl_position','repository_filename','local_scan','status','paths'])

def tests():
    evidence=json.loads((RESEARCH/'curated_evidence.json').read_text()); a={x['id']:x for x in evidence['assertions']}
    for x in a.values():
        assert (ROOT/x['source']).exists(), x['source']
    results=[]
    # Explicitly retrospective tests: selected after reading finding aid, not blind validation.
    levels={a[e]['level'] for e in ['E1','E2','E3']}
    results.append(dict(id='H1',hypothesis='Later advertisements deliberately address different interpretive levels of a shared earlier document.',
        mechanism='Document date plus level forms a compound reference address.',construction=['E1'],held_out_from_construction=['E2','E3'],
        prediction='Later notices independently return to 1989-05-01 using different level numbers.',observed=sorted(levels),
        result='supported_as_reference_structure',confidence='high for printed references; low for any proposed decoding algorithm',
        alternative='A literary or artistic narrative can use the same structure without an executable cipher.',
        limitation='Retrospective replication of SR/CL leads; holdout is from construction only, not an unseen or preregistered test.'))
    results.append(dict(id='H2',hypothesis='Every printed Level belongs to one universal system of exactly four classical senses.',
        mechanism='Literal, allegorical, moral and anagogical levels apply uniformly.',construction=['E1','E2','E3'],held_out_from_construction=['E7'],
        prediction='A numbered Level sequence has no fifth member.',observed=a['E7']['levels'],result='rejected_in_universal_form',
        confidence='high against the universal claim; unresolved for a narrower quadrigae-only mapping',
        contradiction='E7 visibly enumerates a fifth Level but does not call that list quadrigae. Classical senses are not assigned by E1–E3.',
        limitation='Does not reject all fourfold readings.'))
    jd=a['E8']['value']; converted=datetime(1970,1,1)+timedelta(days=jd-2440587.5)
    results.append(dict(id='H3',hypothesis='The Julian Day labeled The day in May 1989 merely restates the publication date.',
        mechanism='Standard astronomical Julian Day to civil date conversion.',construction=['E8'],prediction='1989-05-01',
        observed=converted.isoformat(),day_offset=(converted.date()-datetime(1989,5,1).date()).days,
        result='rejected_under_standard_JD_convention',confidence='high for arithmetic',
        alternative='Future event date, another time convention, deliberate displacement, or error.',
        limitation='Single-document falsification; no held-out JD series available. Does not identify what 26 June means.'))
    results.append(dict(id='H4',hypothesis='The corpus sustains a Protestant political and historical canon across decades.',
        mechanism='Recurring named referents anchor an evolving narrative or ideological vocabulary.',construction=['E8'],
        construction_observation='1989 image prominently labels Cromwell and names Confessio Augustana.',
        held_out_from_construction=['E9','E10'],prediction='Later notices return to Cromwell and related Reformation figures.',
        observed={'2006':a['E9']['entities'],'2015':a['E10']['entities']},result='supported_as_recurring_vocabulary',
        confidence='high for named recurrence; low for real-world organizational or author identity claims',
        contradiction='Scientific, financial, musical and multilingual content exceeds a simple religious-message explanation.',
        limitation='An abbreviated G.A. in 2015 is left unresolved. Selected examples are retrospective and cannot estimate population prevalence.'))
    results.append(dict(id='H5',hypothesis='September 2000 is self-contained and its date references are incidental.',
        construction=['E4'],held_out_from_construction=[],prediction='No explicit instruction depends on a distant advertisement.',
        observed='E4 explicitly directs DATE AND HOUR to the 1983-11-22 schedule, approximately 17 years earlier.',
        result='rejected_for_self_containment',confidence='high for textual dependence',
        limitation='The instruction does not prove a physical meeting occurred, nor resolve the time formula.'))
    # Noise control for selected canon: compare within-document co-occurrence with independently
    # shuffled mention columns, preserving marginal frequency. Exploratory, OCR-sensitive.
    con=sqlite3.connect(RESEARCH/'corpus.sqlite')
    docs=con.execute('SELECT id,date_label FROM documents ORDER BY date_label,id').fetchall()
    # One document per filename date; avoid inflation from known scan variants.
    selected={}
    for k,d in docs: selected.setdefault(d,k)
    ids=list(selected.values()); names=['Martin Luther','John Calvin','Oliver Cromwell']
    columns=[]
    for n in names:
        hits={x[0] for x in con.execute('SELECT DISTINCT document_id FROM mentions WHERE entity=?',(n,))}
        columns.append([int(k in hits) for k in ids])
    observed=sum(all(v) for v in zip(*columns)); rng=random.Random(20261021); exceed=0; n=10000
    vals=[]
    for _ in range(n):
        shuffled=[rng.sample(c,len(c)) for c in columns]; value=sum(all(v) for v in zip(*shuffled)); vals.append(value); exceed+=value>=observed
    dump(REPORTS/'hypothesis_tests.json',dict(tests=results,control=dict(
        label='Exploratory co-occurrence permutation; not proof of meaning',entities=names,
        documents=len(ids),observed_three_way_cooccurrences=observed,permutations=n,seed=20261021,
        null='Independent uniform column permutations preserve per-name document frequencies.',
        expected_null=sum(vals)/n,empirical_p=(exceed+1)/(n+1),
        caveats=['Entity selection was informed by prior research; not a confirmatory p-value.',
                 'OCR omissions and shared page formats can bias counts.',
                 'Uniform permutation ignores time trends and document lengths.',
                 'Co-occurrence supports editorial grouping, not cipher correctness or historical truth.'])) )
    con.close()

if __name__=='__main__': coverage(); tests()
