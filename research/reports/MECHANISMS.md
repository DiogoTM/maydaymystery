# May 1989: an exact mathematical identification

2026-10-21 UTC. **The reviewed 8×8 matrix is exactly equivalent to the adjoint action of traceless 3×3 matrices, sl(3).** This is a structural identification, conditional on the transcription. It supplies neither parameter values nor a decoded time.

## Evidence and calculation

The source is [the May 1, 1989 newspaper scan](../../texts/My%20Scans/1989-05-01_page24.jpg), normalized region `[.67,.687,.935,.765]`, beside CROMWELL. The lower-resolution [archive rendition](../../texts/maydaymystery.org/1989-05-01.jpg) was also visually compared. [The transcription](../matrix_1989.json) preserves all 64 entries, mapping α, α′, β, β′, γ, γ′, σ, τ to independent symbols `a, ap, b, bp, c, cp, s, t`. No entry was changed after the first calculation. A second independent transcriber is still needed.

Before computing brackets, the protocol recorded predictions of eight-dimensional commutator closure and a nondegenerate Killing form. Both passed exactly over rational coefficients. All 28 independent brackets close; the Killing form has rank 8 and determinant −2,239,488. These properties motivated checking a specific model rather than assigning a name from dimensions alone.

For a traceless 3×3 matrix

```text
X = [ -s+t/3    a        b    ]
    [   ap     s+t/3     cp   ]
    [   bp       c     -2*t/3 ]
```

form its adjoint action `Y → XY − YX`, in the ordered coefficient basis `(a, ap, b, bp, c, cp, s, t)`. All 64 ordered structure brackets agree with those of the scanned coefficient matrices. More strongly, let `e1,…,e8` be the scanned coordinate vectors. The change-of-basis matrix with columns

```text
P = (e1, -e4, e8, -e7, -e6, e5, e2+e3, (e2-e3)/3)
```

has determinant 2/3. For each of the eight coefficients, the code verifies `M_i P = P ad(X_i)` exactly. Consequently the entire transcribed matrix satisfies `M = P ad(X) P⁻¹`. This explicit equivalence establishes the identification without relying on a classification guess. It does not establish a compact real form such as su(3); the meaning of primes and any parameter restrictions remain unspecified.

A controlled single-entry error in the α coefficient produces ten ordered brackets outside the span. The check therefore detects at least that transcription error. This is a sensitivity example, not a statistical false-positive estimate. The generic matrix is also not Hermitian under the independent-parameter model: a recorded real numerical substitution provides a counterexample to the archived reader's tentative Hermitian suggestion. Special parameter constraints or a different inner product require separate examination.

Run `python research/mechanism_tests.py`. [Exact results and P](matrix_algebra_test.json) accompany the transcription. Tests also check the bracket solver against known sl(2) relations and a nonclosed span. The protocol preceded the initial bracket calculation; this is within-document verification, not a blind prediction on a new advertisement.

## What later documents actually request

April 2, 2008 explicitly attaches Levenshtein distance to **May 1989, Level II**, and separately addresses **May 1990, Level III**. Both scan renditions were inspected. Researcher OCR returns Level I in one extraction; the visible source says II. Raw OCR remains unchanged. The collage visibly reuses portions of the older page, including the geometric globe, CROMWELL label and bottom numbered material. This supports layout-aware reuse, without establishing the operations on that collage.

May 1, 2009 requests an hour and minute from **“5/1/89, matrix”**, naming Romberg–Beleznay and a supposed Bradwardine modification. The archived reader comment reverses the year to 1998; the newspaper image resolves the reading as 1989. [Reviewed relations E13–E16](../curated_evidence.json) are searchable in SQLite.

Romberg–Beleznay is a real scientific lead: Kertész's 1986 paper applies modified Romberg extrapolation to finite-size transfer-matrix results, as confirmed by the [author's publication list](https://www.phy.bme.hu/~kertesz/pub2.html) and [institutional record](https://research.ceu.edu/en/publications/extrapolation-of-transfer-matrix-data-for-percolation-and-lattice/). This does **not** say that an arbitrary matrix is already the required input series. Full-paper retrievals failed with HTTP 503/timeouts; the publisher route was restricted. The complete modified recurrence has not been implemented here. Neither the reviewed matrix nor the 2009 sentence specifies numerical parameter values, finite-size ordering or the Bradwardine modification. [Retrieval record and bibliography](../provenance/romberg_reference.json).

## Edit-distance ambiguity and source criticism

Removing Greek accents for a separate comparison, `φαγη` and `φραγη` have Levenshtein distance 1. Standard Hamming distance is undefined for this unequal-length pair. Enumerating all single insertions from 24 Greek letters yields **116 distinct strings**, each at the same distance. Distance alone therefore cannot select rho and its position. Romans 3:19 provides a linguistic constraint; the scalar metric does not. The 2008 notice does not explicitly identify this word as its operand. This rejects only the proposed uniqueness from distance alone. [Executable result](edit_distance_test.json).

The 2007 archived page explicitly warns that the margin comments on its linked huge PDF are a reader's annotations. Any typography or geometry study must exclude those annotations from claims about the author's design. The warning is evidence about that rendition, not a blanket assertion about every handwritten feature in the archive. Source: historical backup, `texts/07-may1.html`.

## Attribution and next discriminating work

The Greek contrast was already identified by earlier readers; the May 1989 time conversion was already in Piggott. The sl(3) equivalence was independently derived in this pass. Searches of the recovered page text for adjoint/sl(3)/special-linear terms and the repository PDF extraction found no matching identification; this limited check cannot establish historical priority. Other archived pages discuss SU(3) and Lie algebras, so those broad themes are not new findings.

The next useful steps are independent transcription review, locating the matrix's printed mathematical source, and defining a numerical input sequence before attempting extrapolation. A successful decoding claim would still need an independently checkable output and an out-of-sample prediction. The exact algebra narrows the source search; it does not solve the mystery.
