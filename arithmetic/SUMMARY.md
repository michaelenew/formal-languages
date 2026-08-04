# Arithmetic under semantic convexity — SUMMARY

**Goal.** Extend the convex {XOR, AND, 1} set-framework (from the Clue
workstream) with arithmetic, first target addition, so that an
infinite-Clue-style game is decidable by a no-cleverness terminating
reduction: every sentence reduces to TRUE (0, the empty set) or stays
unreduced (undecided).

## State of the art (this workstream)

**Done, proved, and machine-verified:**

- Numbers as bitsets (n = set of binary 1-positions; 0 = ∅), with base
  operators ^, &, a(x)=2x, b(x)=2x+1 and one new syntax construct: the
  **stabilizing series** — monotone chains in finite-subset lattices whose
  termination bound is read off the term (max element or popcount).
- Trailing-ones mask T(x) = x & b(x) & b(b(x)) & ⋯, with proof that the
  first plateau is the limit and an a-priori bound max(x)+1 (0002,
  Prop 2 / Lemmas 2b, 2c).
- Successor succ(x) = x ^ b(T(x)); iterating gives the constant-offset
  family n+1, n+2, … (Prop 3).
- **The series is necessary**: no finite composition of the base operators
  computes succ (locality argument, Prop 4). Carry propagation is exactly
  the unbounded influence finite terms cannot express.
- **Addition**: (x, y) ↦ (x^y, a(x&y)) iterated; terminates in ≤
  popcount(x)+popcount(y) steps by a strictly decreasing popcount measure
  (Prop 5). Equivalent carry-lookahead least-fixpoint form (Prop 6).
- Deduction test extends: "u+v = w" is the term add(u,v) ^ w, reducing to
  0 iff true; judgment stays one-sided.
- Candidate unifying principle (unproved in general, proved per-instance):
  *convexity is preserved under monotone stabilizing series with syntactic
  bounds.*

**Positioning against known theory (0001):** the propositional core is the
Zhegalkin algebra (unique ANF = the convexity of that fragment). The
decidability ceiling is sharp: Presburger (ℕ,+) is decidable, and with
Matiyasevich even the ∃-fragment of (ℕ,+,×) is undecidable — so no convex
syntax can carry full + and ×; the additive direction pursued here is
essentially maximal. Numbers-as-bitsets is the Büchi–Elgot WS1S encoding;
addition is a 2-state automatic relation. The infinite-game set-size
problem is diagnosed exactly: cardinality of arbitrary sets is non-regular
(equicardinality is not WS1S-definable), so sizes must enter as first-class
numbers with additive bookkeeping, not as an operator on raw sets.

## Files

- `exploration/0001_framing_and_prior_art.md` — framework reconstruction
  (flagged; original Clue files unreachable — see root README), convexity
  defined, prior-art anchors and the exact ceiling.
- `exploration/0002_addition_construction.md` — constructions and proofs.
- `exploration/0003_verification_log.md` — what was checked and how.
- `output/bitset_arithmetic.py` — verified implementation; termination
  measures asserted per-step. Run directly for the suite.

## Next steps, in order of leverage

1. **Symbolic convexity via canonical automata.** Ground terms are solved;
   free variables are not (the carry recursion has no ground popcount to
   bound it symbolically). Candidate canonical form: minimal synchronous
   DFA of the denoted automatic relation (Myhill–Nerode canonicity as the
   arithmetic analogue of ANF uniqueness). Concrete first milestone:
   compile terms over {^, &, a, b, add, free variables} to minimal DFAs,
   and show sentence-truth = the automaton for the H^HK term accepting
   everything/nothing (fix polarity when the Clue reading is confirmed).
2. **State and prove the closure principle** (convexity preserved under
   bounded stabilizing series) as a theorem about convex languages, not
   per-instance. Identify the exact side conditions (finite-subset lattice;
   what replaces it for ω-words in the infinite game).
3. **Reconnect to Clue.** Recover the original Clue files (unpushed nested
   repo). Then: finite Clue's "player holds exactly n cards" via binary
   counters built from `add` (polynomial-size, vs exponential pure-ANF
   cardinality constraints); infinite Clue iff the deal constraints phrase
   additively (they do for exact-size hands over indexed card families).
4. **Optional, bounded-risk:** map how far multiplication-by-constant and
   congruences (both Presburger-definable) reach before the ceiling — they
   are free expressiveness if step 1's automata carry them.
