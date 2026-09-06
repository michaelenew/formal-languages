# formal-languages

Exploration of formal languages with **semantic convexity**: syntaxes whose
sentences reduce, by a knowably terminating no-cleverness algorithm, to
TRUE (the empty set, 0) exactly when they are semantically true, and
otherwise remain unreduced (undecided). The judgment is deliberately
one-sided — true / undecided, never false.

## Workstreams

- `clue/` — the original workstream: bridging binary truth statements with
  set theory ({XOR, AND, 1} over sets, empty set = TRUE), the KH ^ H
  deduction test, applied to the game Clue. A dated journal of notes and
  code (later dates = more recent; `older/` predates the dating scheme).
  Recent entry points: `2026-06-21 AI exploration.md` (best single summary
  of the framework and the arithmetic push),
  `2026-01-01 Semantic convexity, syntax vs semantics, and universal
  algebra.md` (term-rewriting background), `2026-02-02 +1 operation.md`.
- `arithmetic/` — extending the convex framework with arithmetic
  (first target: addition, now done for ground terms), toward deciding
  infinite-Clue-style games. See `arithmetic/SUMMARY.md`;
  `exploration/0004` maps its notation to the clue/ corpus.
- `elementary/` — Odrzywołek's one-operator basis for elementary
  functions (`eml(x,y) = exp(x) − ln(y)`, constant 1): why it works (a
  packaging lemma: abelian group + bijection), the family of other such
  bases, the eigen-frame reading (exp-generators are eigenvectors of
  differentiation, log-generators its Jordan chains), and integration on
  EML trees as Risch — convex relative to the constant field, where
  Schanuel's conjecture enters. See `elementary/SUMMARY.md`.

New workstream folders carry a `SUMMARY.md` (exact current state),
`exploration/` (numbered working files, later = more recent), and
`output/` (material artifacts: proofs, verified code).
