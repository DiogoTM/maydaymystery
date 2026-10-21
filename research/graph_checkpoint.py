#!/usr/bin/env python3
"""Expose reviewed evidence and prior map as separately typed SQLite relations."""
import json,sqlite3
from pipeline import RESEARCH,REPORTS,dump

def main():
    evidence=json.loads((RESEARCH/'curated_evidence.json').read_text());prior=json.loads((REPORTS/'prior_megamap.json').read_text())
    con=sqlite3.connect(RESEARCH/'corpus.sqlite')
    con.executescript('DROP TABLE IF EXISTS reviewed_evidence;DROP TABLE IF EXISTS prior_map_nodes;DROP TABLE IF EXISTS prior_map_edges;CREATE TABLE reviewed_evidence(id TEXT PRIMARY KEY,source_path TEXT,target_date TEXT,relation TEXT,details_json TEXT);CREATE TABLE prior_map_nodes(id TEXT,label TEXT,details_json TEXT);CREATE TABLE prior_map_edges(id TEXT,source TEXT,target TEXT,details_json TEXT);')
    for e in evidence['assertions']:con.execute('INSERT INTO reviewed_evidence VALUES(?,?,?,?,?)',(e['id'],e['source'],e.get('target_date'),e['relation'],json.dumps(e,ensure_ascii=False)))
    for e in prior['nodes']:con.execute('INSERT INTO prior_map_nodes VALUES(?,?,?)',(e['id'],e.get('label'),json.dumps(e)))
    for e in prior['edges']:con.execute('INSERT INTO prior_map_edges VALUES(?,?,?,?)',(e['id'],e.get('source'),e.get('target'),json.dumps(e)))
    con.commit();con.close()

if __name__=='__main__':main()
