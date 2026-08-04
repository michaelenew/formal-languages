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
  without ×, guarded convexity, and the V_ω/well-ordering scope result
  (statement-layer path subsequently declined by design; see 0006).
- `exploration/0006_canonical_symbolic_addition.md` — the symbolic layer:
  canonical automata, results, and the sharp fragment boundary.
- `output/bitset_arithmetic.py` — ground-term implementation; termination
  measures asserted per-step. Run directly for the suite.
- `exploration/0007_clue_k_workflow_findings.md` — the K workflow run on
  mini-Clue with hand sizes; findings.
- `output/canonical_automata.py` — the symbolic canonical-form engine
  (compile / minimize / universality / entailment). Run directly for the
  suite.
- `output/clue_k_workflow.py` — mini-Clue end-to-end on the automata
  layer, brute-force cross-validated. Run directly.

**Scope and guard results (0005):** the encoding is the Ackermann
bijection with V_ω (hereditary ∈ = BIT, which is arithmetic-strength —
top-level-only access is what stays under the ceiling), and a small
observation shows any convex semantics is countable and canonically
well-ordered — arbitrary/non-well-orderable sets are out of scope for
every convex framework, by theorem rather than by choice of axioms.
**Guarded convexity** (soundness everywhere, completeness on a
syntactically marked core; two conservativity lemmas owed) remains the
frame under which a closed × can coexist with the decidable core. The
statement-layer ⊗ analyzed in 0005 §1 was **declined by design**: operator
economy — each operator interacts with every other and convexity must
survive all interactions — and a closed multiplication is preferred as the
OR-carrier since it also grounds exponentiation. 0005 records why the
zero law itself is arithmetically cheap; the open design problem is giving
it a *closed* home.

**Symbolic addition — the first prize, claimed (0006):** statements over
{^, &, a, b, T, add} with free variables compile to **canonical minimal
synchronous DFAs** (Myhill–Nerode uniqueness = the arithmetic ANF;
a-priori size bounds composable from the term = knowable termination;
truth = universality; entailment = containment; judgment one-sided).
Machine-checked in `output/canonical_automata.py`: the series successor
x ^ b(T(x)) and add(x, 1) reduce to the *identical* 3-state canonical
automaton; commutativity/associativity/unit and the corpus's carry-save
identity come out universal; strict entailment (y = 2x ⊨ ∃w. y = w+w, not
conversely) works via projection; ×-by-constant stays in the fragment
(z = 3x: 4 states). Conceptual core: the canonical automaton is the
closed form of the stabilizing series — state across positions is what
the locality barrier (Prop 4) says bounded windows cannot do. Sharp edge
of the fragment: automatic relations (Büchi arithmetic ⊃ Presburger);
z = x·y and y = 2^x are provably outside, so closed × / exponentiation
need a guarded tier or a genuinely new canonical object.

**The K workflow, run on the toy problem (0007):** mini-Clue (6 cards,
2 players + envelope, hand sizes 2/1/3) solved end-to-end with K as one
canonical automaton — update by intersection, deduction by containment —
cross-validated exactly against brute force at every stage (262,144 deals
× 4 stages, zero disagreements). Cardinality proved definable inside the
term language with no new primitive: pow2(y) := ∃w. add(w,1) = y ∧
y & w = 0, and |h| = k via k disjoint pow2 witnesses; |E| = 3 was
*derived*, never asserted. The one-sided trichotomy shows up concretely
(mustard-in-A unknown, its converse unknown, mustard-not-in-E known).
Observed but unproven: canonical size shrank monotonically with knowledge
(17 → 16 → 13 → 8 states).

## Next steps, in order of leverage

1. **Closed × / exponentiation under guard**: sharply posed by 0006 —
   both are provably non-automatic, so their complete home must be a
   guarded tier (prove the two conservativity lemmas of 0005 §2) or a new
   canonical object. Exponentiation is the corpus's {x} = 2^x level-shift
   map; any progress here is progress on the level dimension flagged in
   the 2026-06-21 note.
2. **The closure principle** (0002): convexity preserved under bounded
   stabilizing series, as a theorem — now with the sharper conjectured
   form: series with finite-state transition structure land in the
   automatic fragment (0006's "automata are the closed forms").
3. **ω-extension** for the infinite game: S1S/Büchi territory; the
   canonical object needs a design decision (minimal Büchi automata not
   unique).
4. **Variable-size counting**: 0007's sizes are constant-k (one witness
   per card). "Hands of equal unknown size" needs Presburger-style
   counting over the automatic layer; also investigate the observed
   monotone shrinkage of K's canonical size under knowledge updates.
