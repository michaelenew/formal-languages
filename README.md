# formal-languages

Exploration of formal languages with **semantic convexity**: syntaxes whose
sentences reduce, by a knowably terminating no-cleverness algorithm, to
TRUE (the empty set, 0) exactly when they are semantically true, and
otherwise remain unreduced (undecided). The judgment is deliberately
one-sided — true / undecided, never false.

## Workstreams

- `Clue/` — the original workstream: bridging binary truth statements with
  set theory ({XOR, AND, 1} over sets, empty set = TRUE), the H ^ HK
  deduction test, applied to the game Clue.
  **⚠ Broken in this repository:** `Clue/` was committed as a bare gitlink
  (submodule pointer to commit `ebdc91a`) with no `.gitmodules`, and the
  inner repository was never pushed anywhere. Fresh clones see an empty
  directory. To repair: either push the inner repo and add a proper
  `.gitmodules` entry, or delete the inner `.git/` and commit the files
  directly into this repo.
- `arithmetic/` — extending the convex framework with arithmetic
  (first target: addition), toward deciding infinite-Clue-style games.
  See `arithmetic/SUMMARY.md`.

Each workstream folder carries a `SUMMARY.md` (exact current state),
`exploration/` (numbered working files, later = more recent), and
`output/` (material artifacts: proofs, verified code).
