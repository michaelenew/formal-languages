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
- `exploration/0008_composition_and_basis.md` — the three-move wiring
  calculus and the {^, &, a} basis theorem for the layer.
- `exploration/0009_guarded_multiplication.md` — width-guarded × inside
  the layer; the measured cost curves; the unbounded-case fork.
- `exploration/0010_finite_clue_solved.md` — the finite game solved:
  the solver, the one-sweep deduction extraction, full-size numbers.
- `exploration/0011_thresholds_and_order.md` — at-least-k counting and
  unbounded order are inside the layer; the boundary located exactly.
- `exploration/0012_basis_showcase_and_and_independence.md` — the
  formula surface (wiring-closure = first-order definability) and the
  proof that & is independent.
- `exploration/0013_closure_hierarchy_post_structure.md` — the three
  closure levels, the Pol–Inv connection to the corpus's Post notes,
  and the minimal basis {&, <<} (framing corrected by 0014).
- `exploration/0014_presentation_not_cost.md` — the operator/logic
  split is bookkeeping; the presentation-independent content is the
  obstruction table.
- `exploration/0015_flip_is_not_irreducible.md` — negation traded for
  ^ in full generality; the run-in-hidden-channels construction; what
  it means for the original framing.
- `exploration/0016_hidden_channels_are_tseitin.md` — hidden channels
  are free on the knowledge side (and why not on the hypothesis
  side); the exact exponential cost of not naming the carry.
- `exploration/0017_inference_cost_is_intrinsic.md` — compactness
  buys no cheaper inference; the decision problem is non-elementary;
  where the blow-up is paid in each framing.
- `exploration/0018_clue_inference_complexity.md` — "what's in the
  envelope" is coNP-complete; canonical K is an OBDD in card order;
  the two framings differ only in amortisation.
- `exploration/0019_naturalness_and_representation_power.md` — the
  algebra is forced, not chosen (narrowing 0014); sentences
  poly-simulate automata and are sometimes exponentially smaller;
  canonical + compact + polynomial needs P = NP.
- `exploration/0020_is_expand_and_cancel_optimal.md` — the four
  readings of worst-case optimality and their four statuses;
  expand-and-cancel as Polynomial Calculus.
- `exploration/0021_where_the_shape_lives.md` — the optimality shape
  is an algebraic-complexity question (IPS → VP ≠ VNP; degree lower
  bounds as the tractable form), and where Clue itself sits.
- `exploration/0022_stress_test_the_optimality_suspicion.md` — the
  suspicion steelmanned and broken: true of the canonicalisation
  task, false of inference; no eigenbasis, an uncertainty principle.
- `output/guarded_multiplication.py` — the guarded family and constant
  multiplication, with the measurement suite. Run directly.
- `output/clue_solver.py` — the mechanical solver for finite Clue-like
  games; suite plays compact and full-size Clue to verified
  accusations. Run directly.
- `output/basis_showcase.py` — **start here**: a four-part executable
  tour of the basis, the derivations, the independence arguments, and
  the catalog of canonical sizes. Run directly.
- `output/closure_hierarchy.py` — the three closure levels with every
  checkable claim checked; the minimal basis and its necessity
  arguments. Run directly.
- `output/flip_elimination.py` — rebuilds any automatic relation with
  share and hide only, negation physically disabled. Run directly
  (~4 min).
- `output/succinctness.py` — the quantifier asymmetry, and the exact
  measured cost of forbidding hidden symbols. Run directly.
- `output/representation_tradeoff.py` — why the algebra is forced, and
  sentence-versus-automaton size measured both directions. Run
  directly.
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

**Composition calculus and a basis (0008):** composition of automata has
exactly three moves — share a channel (product/conjunction), hide a
channel (projection/∃), flip (complement) — with "output feeds input" as
the share-then-hide special case. Machine-checked derivations: b = a ^ 1;
T's graph is quantifier-free definable from {^, &, a, 1} (relation
definability and term composability come apart — the locality barrier
governs only the latter); **addition is derivable with exactly one
hidden, uniquely-determined carry wire**; V₂ (lowest set bit) likewise.
Hence, modulo Büchi–Bruyère ((ℕ, +, V₂)-definable = 2-automatic), **the
wiring-closure of {^, &, a} with constants is the entire canonical
layer**. Independence of a from {^, &, constants} proved by
bit-permutation invariance; **independence of & proved in 0012** (the
module GF(2)[t] is stable, but & yields addition hence the numeric
order, i.e. the strict order property).

**The Post-style structure, and the minimal basis (0013).** The basis
question turned out to be *level-dependent*, and all three levels are
now settled — the corpus's own Post notes supplied the engine (their
"f satisfies t iff t satisfies f" is the commutation relation behind
the Pol–Inv Galois connection):

| closure | invariant | is ^ needed? |
|---|---|---|
| term (composition) | monotonicity, Post's M | yes |
| pp (∧, ∃, =) | polymorphisms (Geiger/BKKR) | yes — and ∪ too |
| first-order (+ ¬) | invariance; stability | **no** |

Negation collapses the basis: the finite-subset lattice defines its
own relative complements by subset-extremality, so ^ is derivable
from {&, constants} alone. In this presentation the minimal signature
is {&, <<} + constants, both generators provably necessary — & is the
escape from stability (order, arithmetic, nonlinearity), << the escape
from permutation invariance (position structure, the register).

**But the operator/logic split is presentation, not cost (0014).**
Flip trades for exactly one relation: put relative complement in the
signature and XOR follows with no negation at all (verified). In the
WS1S presentation of the same layer, *both* generators live inside the
logic (intersection becomes ∧ on membership, the shift becomes the
successor). So "minimal basis" is presentation-relative. What is
presentation-independent is the **obstruction table** — any
presentation's ingredients must together break monotonicity (else no
XOR), intersection-closure (else no XOR or ∪), permutation invariance
(else no bit positions), and stability (else no order or arithmetic).
Who breaks them is convention; that they must be broken is not. The
three levels are a budget split, not a discount. *Also corrected in
0014: the Pol–Inv converse (Geiger/BKKR) is a finite-domain theorem
and is not claimed for this infinite domain; only the preservation
lemma, valid everywhere, is used.*

**Flip is not irreducible — negation is worth exactly one relation
(0015).** Every automatic relation is rebuilt using conjunction and
existential projection ALONE — no negation, enforced by disabling
`DFA.complemented` during the construction — over the fixed signature
{&, ^, <<, 0, 1}, by carrying the target automaton's run in hidden
state tracks bounded by a hidden finite horizon (the horizon is what
keeps every track a finite set; relative complement inside it,
`HL ^ (HL & v)`, is where ^ earns its keep). Verified on targets
obtained by complementation (x ≠ 0, x odd, x not a power of two,
x > y). So: pp-closure{&, <<, constants} ⊊ everything, but
pp-closure{&, ^, <<, 0, 1} = everything = FO-closure{&, <<,
constants}. **^ in the signature and flip in the logic are
interchangeable**, which reverses 0013's reading symmetrically — the
corpus carrying ^ as an operator was paying for negation up front,
not being redundant. Consequence for the original framing:
emptiness-assertions **plus hidden channels** are exactly
DFA-equivalent; what the framing lacked was never negation but ∃
(nonemptiness needs one hidden channel: ∃q, q an all-ones prefix
missing x with the position above it in x).

**Hidden channels are Tseitin variables (0016).** They need no new
operator: inventing a symbol and constraining it *is* existential
quantification on the knowledge side, because ∀C(K(C) → H) ≡
(∃C K(C)) → H for H not mentioning C — verified. The interchange
**fails on the hypothesis side** (K → ∃C H(C) is not ∀C(K → H(C))),
so nonemptiness facts can be *learned* for free but nonemptiness
*questions* need a real quantifier. Measured cost of forbidding
hidden symbols, in the corpus's own XOR-of-ANDs normal form and exact:
"at least one of n" = 2ⁿ−1 terms, "at least two of n" = 2ⁿ⁻¹−1, carry
into bit i = 2ⁱ−1 — versus O(1) constraints and one channel each. The
two exponential cases are exactly the corpus's two sticking points,
refutations and addition. Correction to 0015: its construction's
*definitions* are polynomial (O(s) channels, O(s²) atoms); only
*evaluating* them is exponential (projection determinises). Writing
knowledge down stays small; deciding with it is what costs.

**The algebra is forced; the sentence form is never beaten on size
(0019).** Narrowing 0014: what is bookkeeping is the *signature/logic
line*, not the algebra. By Stone, {^, &} are the ring operations a
Boolean algebra already carries; in any idempotent commutative ring
2x = 0, so the **cancel** step is forced rather than chosen; and
convexity needs a ring at all, since cancellation needs additive
inverses that {AND, OR, NOT} lacks. The "eigenbasis" intuition is
exactly right in the form: ANF monomials are a linear basis of the
GF(2) function space and expand-and-cancel is coordinate computation
in it. On representation power, measured both directions: "at least
one of n" is 2ⁿ−1 expression terms but 2 automaton states, while
parity(X & (Y<<w)) is w terms but 2^(w+1) states — so ANF and automata
are **incomparable**. With hidden symbols the comparison becomes
one-sided: automaton → sentence is always polynomial (0015) and
sentence → automaton is sometimes exponential, so **the sentence form
poly-simulates the automaton and is sometimes exponentially smaller;
the automaton never wins on size**, only on amortisation. The "nothing beats
expand-and-cancel" claim is treated properly in 0020 (0019's
subclass-based refutation of it is withdrawn).

**Is expand-and-cancel worst-case optimal? Four readings (0020).**
Compared worst-case against worst-case, with the baseline Θ̃(2ⁿ)
(x₁∨…∨xₙ has 2ⁿ−1 ANF terms) and translation into the sentence form
genuinely cheap: (1) **bounded width — false, unconditionally**: PPSZ
decides 3-SAT in O(1.308ⁿ), a superpolynomial saving over 2ⁿ on
worst-case inputs; (2) **unbounded width — exactly SETH**, open and
believed; (3) **no polynomial algorithm — exactly P ≠ NP**, open and
believed (finite entailment here is coNP-complete); (4) **as a proof
system** expand-and-cancel is Polynomial Calculus over GF(2), where
its exponential cost is *proven unconditionally* (random 3-CNF,
pigeonhole) but its optimality is *disproven* (pigeonhole has
polynomial-size Frege proofs; PC is incomparable to its neighbours) —
though proof size is not algorithm time, so this does not settle (2)
or (3). Net: the intuition is provably right about expand-and-cancel's
*cost* and provably wrong about its *optimality as a certificate
system*; the algorithmic version is P ≠ NP and SETH wearing this
framework's clothes. Notable inversion: the one place an
unconditional lower bound exists — the symbolic layer, non-elementary
— is exactly where expand-and-cancel does not run at all, and where
the automaton method is provably essentially optimal.

**The optimality *shape* is an algebraic-complexity question (0021).**
This framework is natively a polynomial ring, so "the ring's procedure
is optimal" belongs to algebraic proof complexity, not Boolean: as
Polynomial Calculus its lower bounds are proved *through degree*
(size ≥ 2^Ω((d−d₀)²/n), Impagliazzo–Pudlák–Sgall) — a working method,
not a conjecture; as the Ideal Proof System, superpolynomial lower
bounds would imply **VP ≠ VNP** (Grochow–Pitassi), so the shape
terminates at Valiant rather than Cook–Levin, with different barriers
and real partial progress on restricted classes. Measured locator:
mini-Clue's *a priori* knowledge (24 consistent deals, before any
event) is **27,648 ANF terms at degree 15 of 18 variables** against
**17 automaton states** — no refutation of any worst-case claim, but
it places the toy problem in the ring form's worst regime, and for a
predicted reason: hand sizes are threshold functions, which are
near-maximal degree, and degree is exactly what PC bounds go through.
Tractable next step if the shape is pursued: a **degree lower bound
for Clue-shaped constraint systems**.

**The suspicion, stress-tested to a verdict (0022).** Steelman: for
the *canonicalisation task* the tie between representation length and
cost is a theorem — ANF size is semantic, so every ring-form-producing
algorithm pays it, unconditionally; within the ring proof system the
expansion is provably unavoidable (PC lower bounds); and the basis is
forced (Stone). The irreparable breaks: (B1) sound-and-complete
inference need not visit the ring form — at n = 48, where the ring
form of "at least one of n" has ~2.8×10¹⁴ terms by the semantic bound,
the automaton decided both entailment directions in 25 ms with 22 and
50 states; (B2) the basis-swap repair dies symmetrically (windowed
parity: w ring terms vs provably minimal 2^(w+1) states); (B3) no
basis can ever be crowned — every canonical form system has
exponential statements (counting), and different systems have
different hard families; (B4) canonicalisation *overshoots* inference
by a class gap — the top ANF coefficient equals the parity of the
model count (verified), so producing the ring form solves
Parity-P-complete parity-SAT while inference is only coNP
(Valiant–Vazirani, Toda); (B5) what survives is basis-free (P ≠ NP /
SETH) and thus not about the ring. Clue-native witness: divisibility
by 3 is 3 automaton states at every width versus (2^(n+1)+1)/3 ring
terms at degree n−1, measured to width 14. Replacement intuition:
**no eigenbasis — an uncertainty principle** between the Reed–Muller
(Möbius) transform and the sequential/positional factorisation;
hardness is concentration-relative, instance difficulty is
concentration in the best basis, and basis-free difficulty is the
complexity conjectures. The pursuable descendant: PC degree lower
bounds for Clue-shaped systems, and characterising which statements
are concentrated in which basis.

**And a canonical sentence form exists but cannot be cheap (0019 d).**
The algebra does canonicalise — `<<` distributes over `^` and `&`, and
`&` over `^`, so ANF is a genuine canonical form (verified). Cost is
the obstacle, and 3-SAT settles it twice over: 3-CNF over disjoint
triples has exactly 7^m ANF terms from 3m literals (7, 49, 343, 2401,
16807 verified) while being *trivially satisfiable*, so canonicalising
can be strictly harder than deciding; and the ANF of a formula is zero
exactly when it is unsatisfiable, so canonicalising is coNP-hard, and
any polynomial-time canonical form would give **P = NP**. Hence
**canonical + compact + polynomial is unavailable**: ANF and the
minimal automaton are canonical but not compact, sentences with hidden
symbols are compact but not canonical. The intuition to invert:
canonicalising does not *remove* 3-SAT's difficulty, it is *where the
difficulty lives* — the hardness of SAT is exactly the cost of the
change of basis. The eigenbasis analogy holds to the end: **the basis
that diagonalises everything is also the basis that is expensive to
reach.**

**Clue inference itself is coNP-complete (0018).** Deciding "is this
card in the envelope" from Clue-style knowledge is coNP-complete —
membership by exhibiting a consistent deal, hardness by reduction from
Hitting Set with *consistent* knowledge (the unseen refutation, "holds
at least one of these three", is a hitting-set constraint in disguise;
unit facts are easy). So exponential in the worst case *unless P = NP*
— not unconditionally proven. **For a fixed deck, canonical K is
exactly an OBDD in card order**, which gives: build-once/query-cheap
(why the whole-grid survey is one sweep), order-sensitivity (measured:
265–301 states for identical knowledge under shuffled card orders, all
agreeing on 9106 deals; optimal ordering is NP-hard), and a
self-contained worst-case argument — every update is polynomial in
|K|, so K staying polynomial would put a coNP-hard problem in P.
Both framings sit in the same class; they differ only in
**amortisation** (sentence: a fresh decision per query; automaton:
canonicalise per event, then all 84 grid cells from one sweep).
Empirically Clue never reaches the blow-up: adversarial hitting-set
knowledge (14 cards, 10 refutations) stayed under 95 states.

**Compactness buys no cheaper inference (0017).** The exponential
moves rather than vanishing: a formula with O(k) atoms (compose
"triple it" k times) canonicalises to exactly 3ᵏ+1 states — measured.
And that is the optimistic case: deciding sentences of this layer *is*
the WS1S decision problem, which is **non-elementary** (Meyer,
Stockmeyer); even its additive fragment needs doubly exponential time
(Fischer–Rabin). So the automaton procedure is essentially optimal,
not wasteful. The cost splits as: formula → canonical automaton,
non-elementary; automaton ⊗ automaton → verdict, polynomial — which is
exactly why the K-workflow is fast (canonicalise once per event on a
small alternation-free formula, then answer every question by cheap
containment). **Correction to 0015 recorded there:** over {^, &, 1}
alone every expression is *bitwise*, and bitwise relations are already
closed under conjunction *and* projection, so hidden channels buy
nothing without the shift; credit for nonemptiness is joint (∃ *and*
the shift).

**Guarded multiplication, measured (0009):** the width-guarded family
mult_k = {z = x·y ∧ y < 2^k} lives entirely inside the canonical layer —
built by wiring (schoolbook rows via the union move ¬(¬A ∩ ¬B), now a
DFA method), complete inside the guard, rejecting outside it, so
convexity is fully preserved and **bounded games get real multiplication
for free** (the guard is knowledge a bounded game already has). Measured
laws: z = c·x costs exactly c + 1 canonical states (carry argument for
the upper bound; minimality observed); the guard curve is 4, 13, 51, 207
states for k = 1..4 — ratio → 4 per guard bit, i.e. Θ(B²) in the guard
bound B: exponential in bits, only quadratic in magnitude. Unbounded ×
is a sharp two-path choice: level crossing (exponent encoding over the
{x} = 2^x map — also the exponentiation path) or sound-partial rules
(pending the two conservativity lemmas).

**Finite Clue-like games: SOLVED (0010).** `output/clue_solver.py` is a
generic mechanical solver on the canonical layer — real mechanics
including the unseen refutation ("holds at least one": a nonemptiness
fact, impossible in the original expression algebra, one flip on the
automata layer), passes, seen refutations, own hand. "The most you can
deduce" is computed as one forward/backward sweep of canonical K: every
card×hand cell's three-valued verdict (KNOWN IN / KNOWN OUT / unknown,
provably matching semantics) plus the exact consistent-deal count, with
no enumeration. Full-size 21-card Clue solves in ~5 s over 8 rounds; K
peaked at 145 states while tracking 110,880 consistent deals (~760:1
description compression) and shrank monotonically to 29. Every round
validated: true deal never excluded, every KNOWN verdict true, counts
monotone, sweep ≡ entailment on spot checks. Assumption noted: the
refuter's card-choice policy is treated as uninformative. The original
problem statement is met for the bounded case; this is the scaffold for
extensions.

**Thresholds and order (0011):** two conjectured limits refuted by
construction. Fixed-threshold counting is regular via clamped counters
(|h| ≥ k costs k+1 states with *no bound on the set*; nonemptiness is
the k = 1 case; machine-checked equal to the flip of the union of
below-threshold counts). Order x ≤ y is automatic with 2 canonical
states and no bounds, and its wiring derivation (∃ gap: x + gap = y)
collapses to the identical canonical form. The true boundary: coupling
an unbounded set channel to its own cardinality channel, and comparing
two unbounded cardinalities — unbounded (unclampable) counting, nothing
else. Threshold clue events added to the solver.

## Next steps, in order of leverage

1. **The level-crossing extension** (0009's path 1): a two-level system
   — value-level automata and exponent-level automata joined only by
   the {x} = 2^x map — to make unbounded pow2-multiplication and
   genuine exponentiation statements convex per level. This is the
   remaining half of the × prize (bounded factors are done) and the
   whole of the exponentiation prize. Alternative if it stalls:
   sound-partial × after proving the two conservativity lemmas of
   0005 §2.
2. **Prove the Post-style completeness criterion** (0013/0014): the
   two known proper fragments — permutation-invariant {&, constants}
   and stable {<<, constants} — are not yet proved *maximal*. Proving
   it would give "a set of ingredients generates the layer iff it
   breaks stability and breaks permutation invariance", the exact
   analogue of Post's criterion, and stated obstruction-first it is
   presentation-independent. (The companion question from 0014 —
   whether flip is always tradeable — is now answered yes, 0015.)
   The size question is answered in 0016: definitions are polynomial,
   evaluation is what costs. Follow-ons: is {&, ^, <<, 0, 1} a
   *minimal* positive signature, and is the exponential
   determinisation of run-encoded definitions intrinsic, given that
   their hidden tracks are a one-hot partition?
3. **The closure principle** (0002): convexity preserved under bounded
   stabilizing series, as a theorem — now with the sharper conjectured
   form: series with finite-state transition structure land in the
   automatic fragment (0006's "automata are the closed forms"), and
   0008's addition-as-one-hidden-wire as the worked exemplar.
4. **ω-extension** for the infinite game: S1S/Büchi territory; the
   canonical object needs a design decision (minimal Büchi automata not
   unique).
5. **Variable-size counting**: 0007's sizes are constant-k (one witness
   per card). "Hands of equal unknown size" needs Presburger-style
   counting over the automatic layer; also investigate the observed
   monotone shrinkage of K's canonical size under knowledge updates.
