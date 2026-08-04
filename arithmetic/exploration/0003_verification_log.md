# 0003 — Verification log

`output/bitset_arithmetic.py` implements 0002 and checks it. Design point:
the termination measures are **asserted inside the constructions** on every
step — a passing run verifies the convexity bounds themselves, not only the
arithmetic answers.

Run: `python3 arithmetic/output/bitset_arithmetic.py` (seeded, reproducible).

Results (2026-08-04, all passing):

| Claim | Check |
|---|---|
| Prop 2: T(x) = trailing-ones mask | exhaustive x < 2^14 vs closed-form oracle `(~x & (x+1)) − 1`; plateau stop within Lemma 2c bound asserted every call |
| Prop 3: succ(x) = x+1 | exhaustive x < 2^14, plus 500 random 256-bit |
| Prop 5: add = +, ≤ popcount(x)+popcount(y) steps | exhaustive 256×256, 500 random 512-bit; strict measure decrease asserted per step |
| Prop 6: lfp carry-lookahead = + | 500 random 512-bit; Kleene chain increase asserted per step |
| Doubling-limit form (clue/2026-06-21) = + | exhaustive 256×256 + 500 random 512-bit; both XOR-for-OR disjointness invariants and the ~log₂(width) step bound asserted per step |
| offset family n+1, n+2, n+3, n+7 | x < 1000 |
| Prop 4 witness | bit 96 of succ flips when only bit 0 of input flips |
| deduction test add(u,v) ^ w | reduces to 0 on a true instance, not on a false one |

Notes for the next agent:

- Empirically the carry recursion (Prop 5) runs far fewer steps than the
  popcount bound — the bound is loose but that is irrelevant to convexity;
  only its syntactic evidence matters.
- The assertions in `trailing_ones` and `add_lfp` also confirm Lemma 2b /
  Kleene plateau soundness on every input exercised: no false plateaus
  observed (and none possible, per the proofs).
- Nothing here is symbolic: all inputs are ground bitsets. The symbolic
  reduction (free variables → canonical automaton) is unimplemented — see
  SUMMARY next steps.
