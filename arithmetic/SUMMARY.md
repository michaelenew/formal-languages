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
- **Addition, in three verified equivalent forms**: (1) carry recursion
  (x, y) ↦ (x^y, a(x&y)), ≤ popcount(x)+popcount(y) steps by a strictly
  decreasing measure (Prop 5); (2) unit-step Kleene least fixpoint
  (Prop 6); (3) the corpus's doubling-limit / Kogge–Stone form
  (clue/2026-06-21 AI exploration.md), now with its XOR-for-OR
  disjointness invariants asserted per step and a ~log₂(width) bound.
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

**Reconciled with the recovered clue/ corpus (0004):** notation map
(a = n0/inc, b = n1, T = $/[&n1]); T and succ were independently rederived
identically to `clue/2026-02-02 +1 operation.md` — what this workstream
adds there is the plateau-soundness proof and a-priori bounds. Of the
corpus's "Looking for" list: general addition closed (three forms);
×-by-constant closed and safely below the ceiling; general × redirected
(ground computation fine, sentence-level convexity impossible); the
n0/n1/!/x degrees-of-freedom question identified as the same problem as
symbolic addition — both are the symbolic-convexity gap, with canonical
minimal automata as the shared candidate fix. One stale corpus identity
flagged (`2025-06-28 Refocusing.md`'s one-step add formula).

## Files

- `exploration/0001_framing_and_prior_art.md` — the framework (corrected
  against the corpus), convexity defined, prior-art anchors and the exact
  ceiling.
- `exploration/0002_addition_construction.md` — constructions and proofs.
- `exploration/0003_verification_log.md` — what was checked and how.
- `exploration/0004_reconciliation_with_clue_corpus.md` — notation map,
  status of the corpus's open asks, corrections made.
- `exploration/0005_zero_law_or_guarded_convexity_scope.md` — the OR
  without ×, guarded convexity, and the V_ω/well-ordering scope result.
- `output/bitset_arithmetic.py` — verified implementation; termination
  measures asserted per-step. Run directly for the suite.

**Redirections adopted (0005):** the logical OR needs only the zero law
(X ⊗ Y = ∅ iff either is ∅), which needs no arithmetic — it lives in a
statement layer above the expression algebra, a distributive lattice of
emptiness-assertions with CNF/DNF canonical forms; componentwise zero
rules alone are provably insufficient under disjunctive knowledge (Clue
refutations), the lattice laws do the work. Undecidability of × becomes a
*guard line*, not a wall: **guarded convexity** = soundness everywhere +
completeness on a syntactically marked core, with × readmitted sound-only
(two conservativity lemmas owed). Scope settled: the encoding is the
Ackermann bijection with V_ω (hereditary ∈ = BIT, which is
arithmetic-strength — top-level-only access is what stays under the
ceiling), and a small observation shows any convex semantics is countable
and canonically well-ordered — arbitrary/non-well-orderable sets are out
of scope for every convex framework, by theorem rather than by choice of
axioms.

## Next steps, in order of leverage

1. **Symbolic addition via canonical automata — the first prize.** Ground
   terms are solved; free variables are not (the carry recursion has no
   ground popcount to bound it symbolically). Candidate canonical form:
   minimal synchronous DFA of the denoted automatic relation
   (Myhill–Nerode canonicity as the arithmetic analogue of ANF
   uniqueness). Concrete first milestone: compile terms over
   {^, &, a, b, add, free variables} to minimal DFAs, and show
   sentence-truth = the automaton for the KH ^ H term reducing to the
   empty/universal automaton. Known caveat for the ω-extension: minimal
   Büchi automata are not unique; the ω-side canonical object is a real
   design decision (0005 §3).
2. **Statement layer {∪, ⊗}** (0005 §1): formalize the distributive
   lattice of emptiness-assertions, discharge the proof obligation
   (entailment of monotone formulas over the expression-layer atom poset,
   decidable relative to layer below), and encode a real Clue refutation.
   Nonemptiness = size ≥ 1 keeps refutations additive.
3. **Guarded convexity** (0005 §2): prove the two conservativity lemmas;
   then × re-enters sound-only without fear.
4. **The closure principle** (0002): convexity preserved under bounded
   stabilizing series, as a theorem with exact side conditions rather
   than per-instance.
5. **Reconnect to Clue** (corpus in `clue/`): finite Clue's "player holds
   exactly n cards" via binary counters built from `add`
   (polynomial-size, vs exponential pure-ANF cardinality —
   `clue/code/2025-08-16_figuring_out_plus.py` already computes these
   majority/sum-bit forms by brute force).
