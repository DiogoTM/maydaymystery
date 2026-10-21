#!/usr/bin/env python3
"""Exact, falsifiable checks on a reviewed transcription; never repair source entries."""
import itertools
import json
import unicodedata

import sympy as S

from pipeline import RESEARCH, REPORTS, dump


def structure(basis):
    """Find exact structure constants, or report brackets outside the linear span."""
    n = len(basis)
    width = basis[0].rows ** 2
    columns = S.Matrix.hstack(*(m.reshape(width, 1) for m in basis))
    if columns.rank() != n:
        raise ValueError('Coefficient matrices are not independent')
    outside = []
    adjoints = []
    for i, a in enumerate(basis):
        coordinates = []
        for j, b in enumerate(basis):
            try:
                v, _ = columns.gauss_jordan_solve((a*b-b*a).reshape(width, 1))
            except ValueError:
                outside.append([i, j])
                v = S.zeros(n, 1)
            coordinates.append(v)
        adjoints.append(S.Matrix.hstack(*coordinates))
    return outside, adjoints


def levenshtein(a, b):
    row = list(range(len(b)+1))
    for i, ac in enumerate(a, 1):
        new = [i]
        for j, bc in enumerate(b, 1):
            new.append(min(new[-1]+1, row[j]+1, row[j-1]+(ac != bc)))
        row = new
    return row[-1]


def plain_greek(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower())
                   if unicodedata.category(c) != 'Mn')


def main():
    source = json.loads((RESEARCH/'matrix_1989.json').read_text())
    names = source['parameters']
    symbols = S.symbols(' '.join(names))
    lookup = dict(zip(names, symbols))
    matrix = S.Matrix([[S.sympify(v, locals=lookup) for v in row]
                       for row in source['matrix']])
    basis = [matrix.diff(p) for p in symbols]
    outside, adjoints = structure(basis)
    assert not outside, 'Exact transcription failed closure; do not silently repair it'
    killing = S.Matrix(8, 8, lambda i, j: S.trace(adjoints[i]*adjoints[j]))

    # An explicit isomorphism is stronger than a classification inferred from size.
    a, ap, b, bp, c, cp, s, t = symbols
    small = S.Matrix([[-s+t/3, a, b], [ap, s+t/3, cp], [bp, c, -2*t/3]])
    small_basis = [small.diff(p) for p in symbols]
    small_outside, small_adjoints = structure(small_basis)
    assert not small_outside
    same_brackets = all(x == y for x, y in zip(adjoints, small_adjoints))
    # Columns express the small-basis adjoint coordinates in the scanned basis.
    e = S.eye(8)
    P = S.Matrix.hstack(e[:, 0], -e[:, 3], e[:, 7], -e[:, 6],
                        -e[:, 5], e[:, 4], e[:, 1]+e[:, 2],
                        (e[:, 1]-e[:, 2])/3)
    intertwines = all(bi*P == P*ai for bi, ai in zip(basis, small_adjoints))
    assert same_brackets and intertwines and P.det() != 0
    damaged = [m.copy() for m in basis]
    damaged[0][0, 1] += 1  # One controlled transcription error, not evidence repair.
    damaged_outside, _ = structure(damaged)
    numeric = matrix.subs(dict(zip(symbols, range(1, 9))))
    result = dict(
        id='H9', hypothesis='The May 1989 symbolic matrix realizes an adjoint Lie algebra.',
        protocol=source['prospective_test'], source=source['source'], region=source['region'],
        basis_rank=8, independent_commutators=28, outside_span=outside,
        killing_form=[[str(v) for v in row] for row in killing.tolist()],
        killing_rank=killing.rank(), killing_determinant=str(killing.det()),
        explicit_3_by_3_model=[[str(v) for v in row] for row in small.tolist()],
        all_64_ordered_brackets_identical_to_3_by_3_model=same_brackets,
        change_of_basis=[[str(v) for v in row] for row in P.tolist()],
        change_of_basis_determinant=str(P.det()),
        all_eight_intertwining_identities_verified=intertwines,
        interpretation='Exactly equivalent to the adjoint action of traceless 3x3 matrices: sl(3) over the chosen characteristic-zero field.',
        control=dict(description='Increase the alpha coefficient of entry (1,2) by one.',
                     ordered_brackets_outside_span=len(damaged_outside)),
        hermitian_counterexample=dict(parameters=dict(zip(names, range(1,9))),
                                      equals_own_conjugate_transpose=numeric == numeric.conjugate().T),
        result='supported_exactly_for_the_transcribed_entries',
        novelty='Independent derivation; no matching identification found in the searched archived page text or repository PDF extraction. Priority is not established.',
        limitations=['Transcription is provisional and not independently double-entered.',
                     'Primes were treated as independent parameters. No real form, such as su(3), is specified by this check.',
                     'Protocol was locked before the first bracket computation, but this is within-document validation, not a blind cross-document test.',
                     'No numerical parameter assignment, hour, minute, plaintext, or Romberg input series follows.'])
    dump(REPORTS/'matrix_algebra_test.json', result)

    printed, ordinary = plain_greek('φάγῃ'), plain_greek('φραγῇ')
    alphabet = 'αβγδεζηθικλμνξοπρστυφχψω'
    alternatives = sorted({printed[:i]+ch+printed[i:]
                           for i in range(len(printed)+1) for ch in alphabet})
    distances = {levenshtein(printed, v) for v in alternatives}
    assert distances == {1} and ordinary in alternatives
    dump(REPORTS/'edit_distance_test.json', dict(
        id='H10', hypothesis='The Levenshtein distance alone uniquely determines the missing Greek letter and position.',
        motivating_source='texts/My Scans/2008-04-02_page14.jpg',
        target='texts/My Scans/1989-05-01_page24.jpg',
        printed=printed, scriptural_comparison=ordinary,
        normalization='NFD, remove combining marks, lowercase; no letter substitution.',
        levenshtein_distance=levenshtein(printed, ordinary),
        hamming_distance=None, hamming_reason='Unequal lengths under standard Hamming distance.',
        control='Enumerate every single insertion from 24 ordinary Greek letters at every position.',
        equally_distant_distinct_candidates=len(alternatives),
        result='uniqueness_rejected_without_additional_constraints',
        limitations=['A mathematical ambiguity check, not a blind decipherment experiment.',
                     'Alternatives are strings, not necessarily grammatical words.',
                     'Romans 3:19 supplies an external linguistic constraint; scalar distance does not supply it.',
                     'The 2008 notice does not explicitly designate this Greek word as the Levenshtein operand.']))
    print(json.dumps(dict(matrix_closure=True, sl3_adjoint_equivalence=intertwines,
                          killing_rank=killing.rank(), damaged_brackets=len(damaged_outside),
                          equally_distant_greek_insertions=len(alternatives))))


if __name__ == '__main__':
    main()
