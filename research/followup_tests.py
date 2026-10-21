#!/usr/bin/env python3
"""Exploratory tests and explicit historical attribution, separate from initial hypotheses."""
import json,random,sqlite3
from pipeline import RESEARCH,REPORTS,dump

def valid_books(books,pairs):
    return [b for b in books if all(c<=len(b['chapters']) and v<=len(b['chapters'][c-1]) for c,v in pairs)]

def main():
    books=json.loads((RESEARCH/'external/references/kjv.json').read_text(encoding='utf-8-sig'))
    pairs=[(23,24),(4,19),(19,46),(22,37)]
    matches=valid_books(books,pairs)
    assert len(books)==66
    # The dataset uses Portuguese book labels with English KJV text; canonical
    # position 42 is Luke (Lucas), not a name inferred from language heuristics.
    luke=books[41];assert luke['abbrev']=='lc'
    rng=random.Random(19890501);trials=10000;any_match=0;unique=0
    for _ in range(trials):
        random_pairs=[(c,rng.randrange(1,60)) for c,v in pairs]
        hits=valid_books(books,random_pairs);any_match+=bool(hits);unique+=len(hits)==1
    result=dict(id='H7',hypothesis='The four hour pairs in May 1989 could be Bible chapter-and-verse addresses.',
        source='texts/My Scans/1989-05-01_page24.jpg',region=[.18,.78,.96,.82],pairs=pairs,
        prediction='One canonical book admits all four pairs without changing their order or values.',
        matches=[dict(dataset_name=b['name'],abbrev=b['abbrev'],canonical_position=books.index(b)+1) for b in matches],
        interpretation='Luke is the only compatible book in this 66-book chapter/verse table.',
        selected_texts=[dict(reference=f'Luke {c}:{v}',text=luke['chapters'][c-1][v-1]) for c,v in pairs],
        control=dict(seed=19890501,trials=trials,method='Fix chapter numbers; draw each verse number uniformly from 1..59 (angle minutes excluding zero).',
                     any_compatible_book_fraction=any_match/trials,unique_compatible_book_fraction=unique/trials),
        result='structurally_compatible_candidate_not_a_decoding',
        limitations=['Bible interpretation selected after seeing corpus themes; no correction for trying other representations.',
                    'The control is exploratory and does not model the original author or all alternative encodings.',
                    'No specified procedure turns the verses into a clock time.',
                    'This test covers one document and supplies no blind holdout success.',
                    'Book labels in the public dataset are Portuguese; verse content is English KJV.'],
        provenance='research/provenance/reference_retrievals.json')
    dump(REPORTS/'hour_pair_test.json',result)
    dump(REPORTS/'followup_hypotheses.json',[
        dict(id='H6',hypothesis='The May 1989 missing-rho Greek wording is a reproducible designed perturbation, rather than merely an OCR omission.',
             construction='May 1989 Greek line visibly reads φάγῃ (may eat), differing from Romans 3:19 φραγῇ (may be stopped).',
             held_out_from_construction='May 1990 diagram, explicitly labeled scordatura: ADW, 5/1/89',
             prediction='A later primary notice explicitly calls out the altered 1989 reading.',
             observed='1990 main node prints the stopped-mouth wording; adjacent scordatura trapezoid points to 5/1/89 and repeats the eating form.',
             result='supported_for_this_annotated_text_change',confidence='high for printed contrast; unresolved for a general decoding algorithm',
             prior_art='Archived 1990 reader comments already discuss this difference; independently reproduced, not a new discovery.',
             sources=['texts/My Scans/1989-05-01_page24.jpg','texts/maydaymystery.org/1990-05-01.jpg'],
             limit='Retrospective, not blinded. Rho insertion is not claimed to decode any other region.'),
        dict(id='H8',hypothesis='The June 2005 formula is compatible with a known physical construction rather than requiring invented numerical arithmetic.',
             source='texts/maydaymystery.org/2005-06-22_1.jpg',formula='mu = theta_star / (Delta_t * sin(phi))',
             prediction='A pre-2005 microlensing source independently gives the same algebraic relation.',
             observed='Albrow et al., The Relative Lens-Source Proper Motion in MACHO 98-SMC-1: equation (2), p.2, t_star=Delta_t sin(phi); equation (3), p.4, mu=theta_star/t_star.',
             supporting_reference='https://www.astronomy.ohio-state.edu/gaudi.1/ms98001.pdf',
             result='physical_formula_reproduced_exact_visual_source_unidentified',confidence='high for algebraic equivalence; low for author intent',
             limit='The date annotations and chessboard are not explained; Gaudi/Petters Folds was inspected but not established as the diagram source.')])
    print(json.dumps(dict(compatible_books=[b['name'] for b in matches],control=result['control'])))

if __name__=='__main__':main()
