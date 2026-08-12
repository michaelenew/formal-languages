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
- `exploration/0023_eigenbases_of_the_problem.md` — the QM upgrade
  made literal: bases as operator eigenbases (verified), the
  worst-case width split, and what forces the DFA.
- `output/eigenbasis_structure.py` — restrictions diagonal in ANF,
  translations diagonal in Walsh, noncommutation witness, the
  concentration table, the worst-case table. Run directly.
- `exploration/0024_eigenbasis_classification.md` — the classification
  closes: three measurements per coordinate, the decision-diagram
  taxonomy, polarity frames, the Donoho–Stark theorem.
- `output/eigenbasis_classification.py` — the one-coordinate
  enumeration, unipotence of translations, polarity reconstruction and
  the cure of the refutation event, the tight uncertainty inequality.
  Run directly.
- `exploration/0025_anf_automaton_one_way_street.md` — no uncertainty
  inequality exists for the ANF × automaton pair; the crossing law and
  the one-way simulation that replace it.
- `output/anf_automaton_tradeoff.py` — the four cells, the crossing
  law verified tight, frame sensitivity explained. Run directly.
- `exploration/0026_taxonomy_relation_graph.md` — all ten frame pairs
  classified; the automaton is the universal sink.
- `output/taxonomy_relation_graph.py` — the three new ordered laws
  (path, span, degree), the free pairs, the sink property. Run
  directly.
- `exploration/0027_sink_refuted_and_exact_ceilings.md` — the sink
  conjecture refuted (sharing is the sink-maker) and all three
  ordered-edge ceilings made exact.
- `output/sink_uniqueness_and_ceilings.py` — the FDD frame, the
  flat→shared flow, the killing separation, and the three exact laws
  with isolated collapse modes. Run directly.
- `exploration/0028_zeta_conjugacy_and_the_flow_map.md` — the Davio
  laws, the zeta conjugacy of the shared frames, the transported
  literature witness, the flow matrix, the finite frame conjecture.
- `output/frame_flow_map.py` — fiber/survivor laws exact, ζ verified
  an involution, the one-hot multiplexer measured, the flow matrix
  with witnesses, the one-coordinate enumeration. Run directly.
- `output/frame_grid_figure.py` / `output/frame_flow_grid.png` — the
  full 7×7 eigen-frame flow grid rendered (verdict + law + witness
  per cell; symmetry-derived cells starred; no unmeasured cells left
  after 0029).
- `exploration/0029_matrix_completed.md` — the up-zeta law, the
  shared-frame triad, the cross-polarity cells, and the Walsh→OBDD
  cell resolved per-frame at subexponential rate.
- `output/matrix_completion.py` — the negFDD frame, the trio law
  verified exact, the triad measured, the binary-address multiplexer
  measurements. Run directly.
- `exploration/0030_subclass_escapes_and_frame_completeness.md` — the
  subclass escape map, the one-coordinate completeness theorem (with
  the machine-caught hybrid correction), the cure exhibits, the
  proof-sketch audit.
- `output/subclass_escapes.py` — the operator-monoid enumeration,
  the affine and multiplication cures (*BMD implemented), the
  subclass × frame measurements. Run directly.
- `output/subclass_map_figure.py` / `output/subclass_escape_map.png`
  — the subclass × frame map rendered (homes, escapes, canonical
  algorithms; falsifier rows added after 0031).
- `exploration/0031_decision_counting_split.md` — the impossibility:
  portfolio optimality refuted for decision (median-closed and Horn
  witnesses); the program re-scoped to deduction-with-counting.
- `output/polymorphism_frames.py` — the two tractable-class families,
  their polynomial deciders cross-checked, every frame measured at
  three sizes, the verdict. Run directly.
- `exploration/0032_rank_floor_unconditional_bound.md` — the rank
  floor theorem (one number floors the whole taxonomy), its honest
  looseness on parity families, and the unconditional exponential
  worst case for the fixed-basis portfolio (affine witness).
- `output/rank_floor.py` — the floor verified against every measured
  frame, the looseness table, the affine rank measurements across
  orders. Run directly.
- `exploration/0033_field_inverse_witness.md` — both live edges
  landed on the field-inverse witness; the parity conjecture reduced
  to a one-way street; the completed picture and final ledger.
- `output/live_edges.py` — the squeeze theorem, the self-validating
  GF(2^n) construction, the full-rank-under-GL measurements, the
  matrix-tree cross-checks, the determinant's two faces. Run
  directly.
- `exploration/0034_set_construction_and_the_counted_tier.md` — the
  set-construction operator located: the game that forces it, the
  unconditional wall, and the counted tier that carries it.
- `exploration/0035_counted_tier_in_sentence_form.md` — the same tier
  in the corpus's own sentence form; supersedes 0034 §5's presentation
  of the boundary.
- `exploration/0036_canonicity_under_the_measure.md` — three senses of
  canonical form; no canonical form unguarded; the intended Pareto
  impossibility for the tier fails; canonical up to GL(d, ℤ).
- `exploration/0037_pointwise_and_the_containment_test.md` — why
  `KH ^ H` stops collapsing at `<<`: the test loses completeness, not
  the rule set. Corrects 0035 §1's Presburger restriction.
- `output/pointwise_and_the_containment_test.py` — pointwise
  completeness of the containment test, the shift residual computed
  non-empty, the s-closure repair, and the width-proportional depth.
  Run directly.
- `exploration/0038_the_nonemptiness_primitive.md` — the infinite
  closure's closed form is the nonemptiness indicator `N`; three rules,
  terminating; the test becomes exact.
- `output/nonemptiness_primitive.py` — the closed form verified, the
  test exact in both directions, the s-graded ANF engine and the
  two-step derivation, the termination measure. Run directly.
- `exploration/0039_tiles_and_the_n_layer.md` — the telescoping
  identities as a family; the closure is tile-wise; the shift's whole
  content is one Boolean law in the N-layer.
- `output/tiles_and_the_n_layer.py` — the identity family measured, the
  tile-wise closure, the semantic/symbolic split, and the realisable
  N-vectors. Run directly.
- `exploration/0040_tiles_are_windows.md` — the tiles are the windows
  of the bit string, the single N-law is far from sufficient, and the
  realisable set is the de Bruijn walk-sets: the N-layer IS the
  automaton.
- `output/tiles_are_windows.py` — tiles-are-windows verified, the law's
  insufficiency counted, and the de Bruijn characterisation checked
  exact. Run directly.
- `exploration/0041_canonicalising_T.md` — T is `succ` under
  complement and `U` under De Morgan; its tiles are ones-padded
  windows, so it inherits 0040's canonical form.
- `output/canonicalising_T.py` — the elementary form, the
  complement-conjugacy bridge, both fixpoints and both telescopings,
  the dependence measurement, and T's tiles. Run directly.
- `exploration/0042_the_series_schema.md` — the nine cells of the
  series schema, the three universal laws, what the join decides, and
  the closing composition table for {N, T, U, D}.
- `output/the_series_schema.py` — the cells enumerated and identified,
  the laws verified per cell, `N = U | D`, and the composition table.
  Run directly.
- `exploration/0043_series_confluence.md` — confluence completed in
  nine rounds; `collect` is the orientation that works; the residue is
  the `|`-as-primitive convention.
- `output/series_confluence.py` — the rewrite engine, the soundness and
  termination checks, the critical pair, and the exhaustive divergence
  search. Run directly.
- `exploration/0044_confluence_without_the_union_primitive.md` — the
  ANF rebuild: six of 0043's rules discharged by the constructors,
  `N-absorb` added, `collect`'s three side conditions unified, and the
  finding that random terms never exercise the schema's own rules.
- `output/series_confluence_anf.py` — the same engine over ANF
  polynomials with `|` derived; the targeted redex pool, the
  per-redex uniqueness check, both divergence searches, and the
  two-column rule census. Run directly.
- `exploration/0045_removing_the_right_shift.md` — `ker h = ker (&(Ω^1))`,
  the `a^d` elimination, the `h` column being exactly the two cells the
  corpus never had, `N` as the language's one downward channel, and the
  termination measure reverting.
- `output/removing_the_right_shift.py` — the kernel comparison, the
  elimination procedure verified as an exact scaling, the schema
  without `h`, the LSB-causality table, and 0044's suite re-run with
  `h` removed. Run directly.
- `exploration/0046_the_primitive_basis.md` — eight primitive
  operations, the split between algebra signature and rewrite
  signature, and every operator worked on a bitstring with its
  expansion beside it.
- `output/the_primitive_basis.py` — constants as a/b chains, the
  smaller `{1, a, ^}` basis, `Ω = N(b 0)`, the measures as
  telescopings and as each other's complement, and the worked
  examples. Run directly.
- `exploration/0047_the_guarded_canonical_form.md` — the truth guard
  collapsing onto the word problem, bounded state as the invariant that
  decides, `N` as the guard, the (guard, minimal machine) canonical
  form, the two defects measured in the 0044/0045 rule set, lasso
  constants, and the wall at unbounded state.
- `output/guarded_canonical_form.py` — the term-to-Mealy-machine
  compiler, the reachability decision procedure with guard
  consistency, minimal-machine canonicalisation, the six missing laws,
  the ANF constant-folding correction, the lasso table, the
  head-to-head against the rewrite engine, and the `x^y` / `x+y` /
  `x*y` residual counts. Run directly.
- `exploration/0048_canonicity_in_sentence_form.md` — the mask deleted,
  `a` pushed to the leaves, the prefix analysis and its three rules, the
  join deciding which rule each schema cell needs, and containment as
  the threshold an ANF engine cannot cross.
- `output/sentence_canonical_form.py` — mask-free ANF over the 0046
  basis, `known_prefix` and `support_bound`, the eleven rules, the
  prefix-depth measurement, the residue classifier, and the rule
  census. Uses 0047's decision procedure only as an oracle. Run
  directly.
- `exploration/0049_closing_containment.md` — containment closed by the
  fixpoint law and the `^`-closed down-set, the 84% measurement, joins
  costing 2^n−1 when unnamed, and the wall relocated to ANF's rule
  shape.
- `output/containment_closure.py` — the monotonicity census, the
  down-set closure check, the derived containment relation with its
  soundness check, the boundary search and classification, the
  join-cost table, and the rule-shape demonstration. Run directly.
- `exploration/0050_expand_and_add.md` — the fixpoint law run forward
  as the canonical form, containment as the statement `A ^ AB`, and
  addition as the `|` cell over a guarded shift.
- `output/expand_and_add.py` — expansion with the measures unfolded,
  the telescope/collect separation, the per-join cost table, the carry
  fixpoint and its unfolding, `succ` as the y=1 case, and the three
  universal laws for the guarded cell. Run directly.
- `exploration/0051_termination_and_confluence.md` — the multiplicative
  reduction order, the L-divergence and `!(x&1)` certificates, the
  infinite path, the no-normal-form theorem, the two completion rules,
  and the stuck-truth demonstration.
- `output/termination_and_confluence.py` — the interpretation and its
  lemma grid, the exhaustive divergence scan, the locality checks, the
  peak census before/after repair, N-fold and annihilate, and the
  stuck-truth certificate. Run directly.
- `exploration/0052_the_products_schema.md` — multiplication as the
  `+`-join of the guarded diagonal family, the four products, the
  unary schema as the Ω-column, the `+` row of 0042's table, lassos as
  odd-denominator rationals, and the wall re-measured in all four
  joins.
- `output/the_products_schema.py` — the guarded family and the four
  products against independent definitions, the Ω-column and b-fill
  checks, the `+`-row fixpoints, the rational lassos, diagonal
  distribution, N-multiplicativity, the 3→2 majority reduction, and
  the residual tables. Run directly.
- `output/canonicity_under_the_measure.py` — the bit-length measure
  table, the failed Pareto construction with the language's Nerode
  index, and the unimodular register basis change with its singular
  counterexample. Run directly.
- `output/counted_sentence_form.py` — the three measure laws, the
  section from the count sort, the worked pair as sentences with the
  sort error raised where it is written, and the orthogonal growth of
  the two levels under union. Run directly.
- `output/level_crossing.py` — the interdefinability of `{.}` and
  `|.|`, the corpus level-map correction, the unbounded Myhill-Nerode
  index of the balance rule, and `CountedAutomaton` (deterministic
  Parikh automaton) with Boolean closure, entailment, canonical form
  and the machine-enforced hiding guard. Run directly.
- `output/infinite_clue.py` — Infinite Clue defined and solved on the
  counted tier, the clamp diagonal, and cross-validation against brute
  force. Run directly.
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

**The eigenbasis picture, corrected and made literal (0023).** The
uncertainty observation strengthens the eigenbasis analogy rather than
defeating it: as in QM, there are multiple eigenbases, one per
operator family, and their noncommutation is the uncertainty. Verified:
the ring/ANF basis is the common eigenbasis of the RESTRICTION
operators f(x) ↦ f(x&m) (eigenvalues 0/1); the Walsh/character basis
— living over the counting layer's ℤ lift — is the common eigenbasis
of the TRANSLATIONS f(x) ↦ f(x^a) (eigenvalues ±1, phases); the
automaton is definitionally the canonical quotient of the SHIFT action
(states = Brzozowski derivatives); restriction and translation do not
commute (witnessed), so no common eigenbasis exists and concentration
trades (measured table: every statement small somewhere, no basis
small everywhere). **What forces the DFA**: the same theorem that
forced << — the two forced decompositions sit exactly over the two
proven-necessary generators ({&,^} ring → ANF via Stone; << → minimal
automaton via Myhill–Nerode, a machine-free quotient definition), with
initial-algebra/final-coalgebra duality as the structural seat and
reading order as the automaton family's frame freedom (like coordinate
choice for the position basis). Worst-case re-arm of 0022's critique:
for 3-CNF, deciding (O(1.308ⁿ), PPSZ) provably beats canonicalising
(≥ 7^(n/3) ≈ 1.913ⁿ, exact family) — worst case against worst case,
both unconditional — while for unbounded width the "may as well
canonicalise" claim is plausible under SETH: the truth is
width-split. Eigen-frame criterion: canonical = eigen; CNF/3SAT/Sudoku
lack uniqueness, hence are non-eigen frames of the same problem.
Open: classify maximal commuting observable families over the
generators (= classify eigenbases); which are convexity-compatible;
quantitative uncertainty inequalities between basis concentrations.

**The classification closes, and it already has a name (0024).** One
coordinate is exhaustively enumerable: GF(2)² has exactly three bases
— {1,x} (eigenbasis of substitute-to-0; positive Davio), {1,1^x}
(substitute-to-1; negative Davio), {x,1^x} (multiply; Shannon) — and
no fourth; translations are unipotent over GF(2) ((T_a+I)² = 0,
verified), so the Walsh basis exists only over the counting layer's ℤ
lift — the lift is forced, like complex numbers for spin. Products
over coordinates + the sharing (quotient) move + order + lift generate
exactly the **Kronecker decision-diagram taxonomy** of logic synthesis
(PPRM/FPRM/OBDD/FDD/KFDD/*BMD): the automaton is Shannon-plus-sharing,
ANF is Davio-flat, and the measured ANF-vs-automaton incomparability
is an instance of the known OBDD/FDD exponential separations. All
frames are canonical with terminating transforms, so **every frame is
convex — convexity is a property of the taxonomy, not of a member**;
best-frame search is itself NP-hard (known, both for order and
polarity). Frames move blind spots without removing them: polarity is
the translation orbit of ANF (FPRM(p) = ANF of f(x^p), verified), and
it cures the refutation event exactly — 2ⁿ−1 terms at polarity 0,
2^(n−|p|)+1 in between, **2 terms** at full complement — while parity
stays ~n terms at every polarity; and by counting, almost every
statement is exponential in every frame simultaneously. First exact
uncertainty theorem in hand: Donoho–Stark for the minterm × Walsh
pair, support(f)·support(Walsh f) ≥ 2ⁿ, verified and tight exactly on
subspace indicators (the coherent states). Open next: explicit
everywhere-spread statements, and whether the affine (GL(n,2)) orbit
adds genuinely new concentration classes.

**ANF × automaton: a one-way street, not an uncertainty pair (0025).**
No Donoho–Stark analogue exists, with a structural diagnosis: the
bases are not mutually unbiased — an ANF basis vector (single
monomial) has an O(n) automaton, so tiny-in-both is possible (parity:
A·B = 300 against 2¹² = 4096) and every product bound dies. All four
joint cells are inhabited, the (BIG, BIG) cell by an explicit
direct-sum witness measured at two sizes. What replaces uncertainty is
the **crossing law**: for XOR-of-monomial statements and any order,
distinct subfunctions at a cut ≤ 2^(straddle+1) (straddle = monomials
with variables on both sides), proved in three lines, verified on 300
random instances at every cut, and **tight** (ratio 1.00 achieved).
Corollary: log₂(automaton) ≤ A + log₂(n+1) + 1 — **ANF-concentration
forces automaton-concentration; the converse fails exponentially**
(at-least-one). The crossing law also explains frame sensitivity
quantitatively (same statement: straddle 6 vs 2 across frames,
automaton 259 vs 70 tracking 2^straddle) — frame optimisation IS
crossing minimisation. Geometry of the frame space: it contains both
**conjugate pairs** (minterm × Walsh, exact product uncertainty, tight
coherent states) and **ordered pairs** (ANF → automaton, one-way
simulation at a combinatorial rate) — QM's homogeneous picture does
not carry over; the frame space is directed in places. Practical
corollary: the K-workflow's automaton frame is safe against
ring-sparse knowledge (upstream law) while the reverse choice would
not have been safe against counting-shaped knowledge — which is
exactly Clue's diet. Open: when the 2^straddle ceiling collapses;
all-frames crossing hardness for a natural Clue statement.

**The relation graph, completed — the automaton is the universal sink
(0026).** All ten pairs among {ANF, dualANF, minterm, Walsh, automaton}
classified. One conjugate pair (minterm × Walsh, the Donoho–Stark
axis). Six ordered edges, all pointing at the automaton or at the ring
frames from Walsh: ANF → automaton and dualANF → automaton (2^crossing,
0025 + complement symmetry — model count, Walsh support and automaton
size are verified invariant under full complement, transferring every
ANF edge to dualANF); **minterm → automaton at LINEAR rate**
((n+1)(μ+1): one subfunction per model prefix per cut plus the zero
subfunction — the cheapest edge in the graph); **Walsh → automaton at
rate 2^d** where d = dim⟨Walsh support⟩ (the statement factors through
a d-dimensional linear map; the automaton carries d running parities);
**Walsh → ANF/dualANF at quasipolynomial rate n^{log σ}** via
deg₂(f) ≤ log₂ σ — verified exhaustively over all 65,536 functions of
4 variables (0/1-transform convention; the law lives on the zero
coefficient where signed and plain spectra differ), with the
n-dependence genuine (AND of two (n/2)-parities: σ = 4 fixed, ANF
(n/2)² growing). Three free pairs: ANF × dualANF, ANF × minterm,
dualANF × minterm — four cells measured, no law either way. Headline:
**concentration in every frame flows to the automaton — linearly from
the semantic frame, 2^crossing from the ring frames, 2^span from the
spectral frame — and the automaton forces nothing back** (at-least-one
at 25 states defeats ANF, minterm and Walsh simultaneously; the full
monomial defeats dualANF and Walsh). The DFA's seat gets its final
answer: not a peer across from sentences but downstream of everything —
the unique frame with no exponential blind spot against any neighbour,
which is why the K-workflow was robust against every statement family
this thread produced. Residual geometry: a directed flow with one
conjugate axis across it and a free triangle among
{ANF, dualANF, minterm}. ~~Conjectured: the automaton is the unique
sink of the full taxonomy~~ — **refuted and improved in 0027**.

**The sink conjecture refuted; sink-ness belongs to the sharing move
(0027 A).** The taxonomy contains ANF's own shared form — the FDD
(positive Davio with sharing) — and measurement settles it: the flat
frames' extremal witnesses flow to the FDD just as to the automaton
(all linear: 25, 13, 25, 35), and the two shared frames separate in
the killing direction — windowed parity separated: FDD 68→85→104
(linear) vs automaton 259→515→1027 (doubling per pair). So a taxonomy
member does not flow to the automaton: conjecture false. The reverse
hunt (automaton-small, FDD-big) came up empty on every counting family
tried — a prediction that majority's Davio closure would explode was
wrong by measurement (FDD tracks the automaton, 71 vs 71 at n=14);
both-direction exponential BDD/FDD separations are cited to the
decision-diagram literature as the one unreproduced gap. Improved
statement: **flat frames flow to shared frames; shared frames are
mutually incomparable; the sink property belongs to the sharing move
(the quotient / Myhill–Nerode / node-merging), not to the Shannon
choice or any fixed frame** — 0026's automaton was unique only because
its frame set contained a single shared frame. Above the shared
frontier, sink-ness survives only as a parameter portfolio, and
best-parameter search is NP-hard.

**The ceilings made exact (0027 B).** All three ordered-edge laws
upgraded from inequalities to equalities — each per-cut state count is
exactly an image size of the upstream description under the cut:
crossing law exact (subfunctions = distinct selected-right-part
symmetric differences ⊕ completed parity; equality at every cut of 200
random statements; ceiling 2^s achieved under shattering + independent
rights, and each dependence — a right-part collision, a shared left
variable — collapses it by exactly a factor of two); path law exact
(states = distinct model **suffix-sets** + zero-subfunction; the
first distinct-prefixes attempt was corrected by the machine; collapse
= suffix-set coincidence or clustering, 21 vs 91 states for clustered
vs spread models); span law collapse = the inner function's
translation stabiliser (generic g reaches 2^d = 8, parity-g pins every
cut at 2). Unified closure: **concentration flows flat → shared at a
rate set exactly by the upstream description's algebraic independence
across each cut**; the collapse mechanisms are completely enumerated.
Open (both closed in 0028): the Davio-side analogues of the four
laws, and the unreproduced reverse BDD/FDD witness.

**The zeta conjugacy, the transported witness, and the flow map
(0028).** The Davio-side analogues, done first as directed, closed
everything at once. **Fiber law, exact**: FDD width at a cut =
distinct entries of the ANF's left-fiber vector (fiber(D) = XOR of
right parts of monomials with left part exactly D) — equality at
every cut of 200 random statements. Corollaries: **ANF → FDD is
LINEAR** ((n+1)(terms+1)) and **minterm → FDD is exponential with
exact ceiling 2^μ** (the survivor law; one-hot-prefix models reach
it: 8 models force FDD width 256 while the OBDD sits at 71). The
flat→shared square is a perfect mirror: each flat frame flows
linearly into its own shared form, exponentially into the other's.
Deeper: 0027's exact crossing law is the same fiber vector aggregated
over down-sets — i.e. **OBDD width = distinct entries of ζv, FDD
width = distinct entries of v, and over GF(2) ζ is an involution**
(verified entrywise): the two shared frames are **ζ-conjugate cut by
cut**, so every separation witness maps to a witness in the opposite
direction. That turned the literature verification into a
computation: ζ(windowed parity's fiber vector) = the fiber vector of
the **one-hot multiplexer**, and measurement confirms OBDD linear /
FDD ≥ 2^k (59/196, 76/389, 95/774 at k = 6,7,8, mirror of wp's
253/59, 509/76, 1021/95 — with OBDD(mux) = FDD(wp) exactly, the
involution visible in raw sizes). **Both directions of the cited
BDD/FDD separation are now machine facts**; 0027's hunt failed
because the ζ-image of a parity-accumulator is a selector, not a
counter. The **flow matrix** over {ANF, minterm, Walsh, OBDD, FDD}
(dual folded by complement symmetry) is complete except one open
cell (Walsh → OBDD tightness): shared frames are pure sinks and
mutually incomparable, flat frames drain linearly into their own
sharing, Walsh is quasipolynomial upstream of the Davio side
(degree law ∘ fiber law), minterm × Walsh stays the conjugate axis.
**Finite frame conjecture**: eigen-frames = diagonalisers of
commuting families generated by the finitely many logic primitives
(^ → translations, & → restrictions, << → shift/sharing, flip →
complement); one coordinate is exhaustively 3 bases over GF(2) plus
finitely many over the ℤ lift, so — conjecturally — at most fourteen
kinds up to the classified parameters (order/polarity/GL(n,2)), six
of them this thread's frames. Complexity-flow reading: C_minterm ⊆
C_OBDD and C_ANF ⊆ C_FDD (P preserved along own-sharing edges),
C_Walsh ⊆ quasipoly C_FDD, shared classes incomparable, all other
moves have witnessed P → E escapes — and the two shared frames split
the sentence basis {^, &} between them (OBDD: all connectives cheap,
parity-knowledge expensive to receive; FDD: ring frame received
linearly, conjunction worst-case exponential). Clue-shaped K is
OBDD-side polynomial, Tseitin-shaped K is FDD-side polynomial, and a
K needing both has no home frame — where 0018's coNP-hardness lives.

**The matrix completed (0029).** The five remaining cells all fell to
the same machinery. **Up-zeta law, exact**: negative Davio's moves
(substitute-at-1 keeps every monomial; derivative keeps only monomials
containing the variable) make the negFDD's cut widths the distinct
entries of ζ↑v — the up-set sums of the same fiber vector — so **the
three shared frames read one vector three ways** (FDD: v, OBDD: ζ↓v,
negFDD: ζ↑v; both zetas involutions; address complement reverses the
lattice and exchanges them). Corollary, the **anti-fiber ceiling**
negFDD ≤ 2^t per cut, mirror of 2^straddle. The **triad** {windowed
parity, one-hot mux, co-one-hot mux} = {v-on-singletons, its ζ↓
image, its ζ↑ image} gives each shared frame exactly one killer,
measured at k = 8: (1021, 95, 103), (95, 774, 103), (95, 102, 1021)
— pairwise incomparability of all three shared frames in both
directions. Cross-polarity cells: ANF → negFDD E (co-singleton
selector: 8 terms force width 256 = 2^t, anti-fiber ceiling reached);
dualANF → FDD E (its complement, measured); FDD ↔ negFDD E both ways
(co-mux / mux). The **Walsh → OBDD cell resolved per-frame**: the
binary-address multiplexer has order-free Walsh support 4^k + 1 =
Θ(n²) and full dimension d = n, is linear in address-first order but
≥ 2^(n−k) in data-first order (σ = 257 vs OBDD 131,349 at n = 20) —
so the cell is E within a fixed frame, and the escape is *exactly
subexponential*: span law + the cited dimension bound d = O(√σ log σ)
(Sanyal) cap it at 2^O(√σ log σ), which the multiplexer meets at
2^Θ(√σ). The only non-full-exponential escape in the matrix. **No
unmeasured cells remain**; the residual opens are refinements: the
best-frame Walsh → OBDD variant (the witness is order-curable), the
ℤ-lift shared kinds (presumably a moment analogue of the zetas), and
the non-product refutation surface of the finiteness conjecture.

**The subclass escape map, and frame completeness (0030).** The
matrix refined to the object the program actually needs — which
*subclasses* escape which frame moves — plus the completeness
evidence. **Completeness at one coordinate is now a machine theorem
with a machine-caught correction**: over GF(2) all 16 operators
enumerate to the three known eigenbases; over the counting lift the
projective closure of the primitive-generated monoid has 11 elements
and my "only four eigenbases" claim was false (cross-layer composites
force hybrids like {x, 1−2x}); the repaired, stronger statement —
**the eigenvector pool is finite and closed** ({1, x, 1−x, 1−2x}) —
holds, giving ≤ 6 lift kinds (4 pure + 2 hybrids = the literature's
HDD rows), with three isolated relative-completeness assumptions
(product structure, primitive inventory, sharing-as-quotient) as the
refutation surface. **The cure exhibits make the extended parameters
mandatory**: a random affine system (d = n/2 parities) escapes all
seven frames at 2^(n/2) simultaneously yet is poly-decidable — cured
to 33 states by the GL(n,2) parameter (Gaussian elimination = that
parameter's canonical algorithm); multiplication's middle bit grows
exponentially in every bit-level frame measured while the word-level
*BMD (implemented) is linear 28→34→40 (word arithmetic = the moment
lift's canonical algorithm). Had the list been closed at seven,
"escapes all frames ⇒ hard" would be refuted by these families; each
lands in a conjectured kind instead. **The subclass × frame map**
(measured, rendered): counting/symmetric → home = all three shared
frames (sharing cures counting); sparse-model → minterm + OBDD;
parity-spread → the ring side; selector → OBDD + negFDD + dual ANF
(24 terms, the co-singleton structure); affine → GL-OBDD only; word
arithmetic → *BMD only; generic → no home by counting but not
succinct, hence not an instance. Every classical poly algorithm
family met so far (DP, enumeration, cancellation, branching, Gauss,
word arithmetic) IS some frame's canonicalisation — no known
frameless poly algorithm for this class. **The proof-sketch audit**:
Step 1 (finitely many frames) machine-supported relative to the
three assumptions; Step 2 (portfolio optimality) is the load-bearing
open step = the optimal-proof-system question (Krajíček–Pudlák);
Step 3 (strict union) is a theorem at representation level but its
witnesses are non-succinct — for succinct inputs it *is* the
conclusion; Step 4 follows from 2 + succinct-3. The proven CSP
dichotomy (Bulatov/Zhuk) is the exact shape of the target, proved
through polymorphisms (0013's Pol–Inv), pointing at the
polymorphism ↔ frame correspondence as Step 2's bridge.

**The decision/counting split — where the program stops, and what
survives (0031).** The polymorphism test was run and it settled the
load-bearing step. Two succinct families — independent sets of a
cycle-plus-matching graph (median-closed, machine-checked; full
deduction grid by implication closure, cross-checked against brute
force) and a bipartite implication system (definite Horn,
min-closed; grid by unit propagation) — have **no frame home**:
every frame of the taxonomy grows by more than 2× per size step on
both (measured at n = 12/16/20, asserted; e.g. independent sets at
n = 20: minterm 5620, ANF 133508, Walsh 1000171, OBDD 384, FDD 3162,
negFDD 869), parameter probes fail (best random order 101, best
random GL map 304, moment 152, vs natural 66 at n = 12), every-order
OBDD hardness is the expander cutwidth theorem (cited), and DNNF-
and-below hardness is cited to the compilation-map literature — the
escape is not curable by any known canonical class, linear or not.
Yet both families' full deduction grids are polynomial via
formula-side closure that compiles nothing. **Portfolio optimality
is therefore FALSE for the decision task** — 0020's B1 break
upgraded to a structural fact witnessed by two-thirds of the
tractable Boolean CSP world; the P ≠ NP route through decision
complexity is blocked, and this is the impossibility the pace was
set to find. **What survives is exact**: the boundary is the
counting line. Counting independent sets of cubic graphs is
#P-complete (Greenhill), and any frame compilation yields model
counts for free — so no frame could be small there without
collapsing #P; the all-frames blow-up sits precisely on a real
hardness boundary. The frame theory stands as a theory of
DEDUCTION-WITH-COUNTING (the Clue solver's actual task since 0010:
verdicts plus exact deal counts), with the surviving conjecture
sharply posed: **a subclass has a polynomial frame home iff its
model-counting problem is polynomial.** Immediate tests: spanning
trees (matrix-tree: counting poly — does a frame home exist?),
planar perfect matchings (FKT), and the refutation direction (a
frame-homed family with hard counting would kill it instantly).

**The rank floor, and the unconditional worst case for the
fixed-basis portfolio (0032).** The requested theorem — no
worst-case subexponential eigen-representation algorithm on the
parity (counting) side — delivered in its achievable form. **Rank
floor theorem**: at any cut, every frame of the taxonomy has size ≥
rank_GF(2) of the communication matrix (flat kinds: Kronecker basis
elements are rank-1 across every cut; shared kinds: level families
span the row space by the fiber laws' invertible transforms; lift
kinds: rank_ℚ ≥ rank_GF(2)) — one number floors every kind,
polarity, order, sharing and lift; verified at every cut of 100
random statements against seven frames plus the moment diagram; pure
linear algebra, no complexity assumptions. **Honest looseness**
(first plan failed by measurement, recorded): GF(2) cut rank is the
parity-communication measure — windowed parity rank 8 vs width 256,
IS family rank 23 vs widths 384–3162 — so 0031's families stay
certified per-frame, not by rank. **The floor bites on the affine
family**: disjoint-coset rows make rank = distinct-row count ≈
2^(n/2−c) at balanced cuts in every order probed (minima 8→16→128
at n = 12/16/20), giving the **unconditional theorem: every
fixed-basis frame — any kind, polarity, order, sharing, lift — is
2^Ω(n) on the random affine family; the fixed-basis portfolio has no
subexponential worst case for counting.** Sharpened: the family's
count is easy (2^(n−d)) and only its GL member is small (33 states)
— the parameter groups are load-bearing, exactly as the parity
conjecture requires. **The remaining wall, named**: the
full-portfolio (GL-inclusive) unconditional bound needs cut rank
exponential under every linear change of variables — matrix-rigidity
territory, open. Final ledger of the founding suspicion: counting
task/fixed bases — TRUE unconditionally; counting task/full
portfolio — open at the rigidity wall, empirically supported;
decision task — FALSE (0031).

**The field-inverse witness: both live edges, one function (0033).**
The rigidity hunt and the parity conjecture's positive test landed
on the same witness. **Squeeze theorem**: cut rank ≤ ANF sparsity in
every basis (monomials are rank-1 across every cut; spot-checked
under GL probes) — so GL-robust witnesses must be everywhere-dense,
necessary but not sufficient (the IS family is everywhere-dense yet
rank 23). Two candidates failed by measurement first: the GF(2)
determinant statement turned out **ring-homed** (ANF exactly k!
Leibniz monomials, 6 and 24 asserted, zero cancellation; FDD 99 at
n = 16 — subexponential), and toy expander spanning trees are
order-curable (2836 → 318 under the frontier-sorted order). **The
field inverse delivers**: low bit of x^(−1) in GF(2^n) (AES S-box
core; self-validating exp/log field construction) has mid-cut rank
essentially FULL — 62–64 of 64 at n = 12, 127–128 of 128 at n = 14 —
in the natural basis and under every random GL(n,2) probe, doubling
per two variables. By the rank floor, every frame of the taxonomy in
every probed basis is ≈ 2^(n/2) on this succinct poly-time family:
the maximal possible empirical witness for the full-portfolio bound,
with all-of-GL certification pinned at the rigidity wall. **And the
same witness refutes the parity converse by measurement**: the
inverse is a bijection, so its statement's model count is
closed-form (2^(n−1), verified) — polynomial counting by pure
algebraic structure, no frame home. Parity is a one-way street:
frame-homed ⊊ counting-tractable. Matrix-tree implemented (Bareiss)
and cross-checked against brute force as the general counting-side
escape engine; the determinant's two faces noted (tame as a
statement, untameable as an algorithm — representations capture what
it says, not what it can do). **Completed picture**: frame homes =
width-style dynamic programming on both tasks; every known escape is
linear algebra over the value structure (Gauss/closure on decision;
bijectivity/matrix-tree/FKT on counting); the eigenframe theory is
the complete complexity theory of representations for this logic,
with its outside mapped and named, and the remaining mathematics
beyond it is the rigidity wall itself.

**Set construction located, and the counted tier that carries it
(0034).** The corpus's expected `{x} = 2^x` operator is the size
operator: `y = 2^x iff |y| = 1 and |y-1| = x` (verified both
directions). **Why the finite game never needed it**: boundedness is a
complete escape — a known deck makes every hand size a constant, and a
constant size is 0011's clamped counter. **The game that forces it**:
*Infinite Clue* — categories by `i mod 3`, one envelope card per
category, two balanced hands, the dealt cards an initial segment `[0,N)`
whose length is not announced, and a spectator who learns only passes
and refutations. Every axiom is automatic (2, 3, 9 states; `card+3` per
move) except `|H1| = |H2|`, whose Myhill-Nerode index is the running
count difference and grows without bound (measured `1,3,5,7,9,11,13`),
so by Büchi-Bruyère it is not expressible in the layer in any
presentation. **No clamp substitutes**: the best regular
over-approximation at clamp `k` decides the game at scale `k` and loses
it at scale `k+1` (measured diagonal), because the game's deduction is a
bootstrap between the balance rule and the initial-segment rule that
advances a counter each round. Measured payoff: five grid cells decided
only with balance, cross-validated against brute force at three deck
bounds, zero disagreements. **The wall, unconditional**: `{p} & X != 0`
is Ackermann's BIT, and `(N, BIT)` is `(V_omega, in)`, bi-interpretable
with `(N,+,x)` — so layer + `{.}` is undecidable and no convex syntax
can carry it, strictly below 0001's ceiling (one binary relation, no
arithmetic operator). **The guard is a sort discipline — restated in sentence form
in 0035, which supersedes the presentation here**: two sorts, each with
its own equality and its own zero. The set sort is the corpus's
idempotent ring, equality `^`, a sentence asserts a term is the empty
set, truth checker "the track reads all zeros". The count sort is ℤ, so
equality is `−` not `^`, a sentence asserts a form is zero, truth
checker "the register reads zero" — the same checker quantified over
registers instead of positions. The only bridge is the measure, with
three verified laws (the first two the corpus's own): `|A^B| + 2|A&B| =
|A|+|B|`, `A&B = 0 ⟺ |A^B| = |A|+|B|`, and `|A<<1| = |A|`. So `|.|` is a
measure, not a ring map, and it cannot see `<<` at all — which is the
one-line form of "the measure is the complete invariant of position
permutation". Both sorts are ℕ, and **undecidability is exactly the
identification of the two copies**: `2^|x|` (a set from a count) is
decidable, `2^x` (a set from a value) is BIT. Not forbidden, contrary to
the obvious guesses: a *section* (`T(A) ^ A` vanishes on `2^k − 1`, the
corpus's own canonical set of size k, so "the set of size c" is
writable for c a count), constants (`|y| − 1` is legal — naming points
is not naming the map), or hiding. **The boundary is on statements, not operators.** `<<` is
**unary**, so `x << 3` is a finite composition and never leaves; the
construct that leaves is *iterating a unary operator a variable number
of times* — 0002's situation, answered there by the stabilizing series.
Two features of the iteration decide: what it is iterated by, and what
it must carry across a cut. `w ^ (x<<3)` (constant / nothing) is layer;
`y ^ (1 << |x|)` (count / a count) is in the tier at 3 control states
and 3 registers; `z ^ (x << |b|)` (count / a **set**, the bits to place)
is **outside both**; `y ^ (1 << x)` (value) closes to BIT. Same operator
in all four; only the statements differ. Membership test,
model-robust: a deterministic Parikh automaton with |Q| states and d
registers moving by ≤1 per column has ≤ |Q|(k+1)^d configurations after
k columns, so superpolynomial residual growth rules out every such
automaton whatever registers it picks. Measured residuals `1,3,5,7,9` /
`1,4,6,8,10` / `1,6,18,50`, and for the third an exact `2^k` lower bound
by pairwise separation — shifting an arbitrary set by a count needs the
shifted bits *buffered*, and a register counts, it does not buffer.
`1 << |x|` escapes only because the shifted thing is the constant 1, so
the sentence pins `y` by shape and offset and never replays bits.
Anything passing the sort check is a *candidate*; being in the tier also
requires that what must be remembered across a cut is a count and not a
set. **Two lines, not to be run together**: in-the-tier / outside is a
width question about one statement, decided by the residual test;
decidable / Gödel is a closure question about a class. A statement can
be narrow and still generate an undecidable theory — `y = 2^x` truncated
to width w has a polynomial minimal automaton (5, 8, 11, 15, 20, 25, 31,
38 at w = 2..9). **Correction to 0034 §5c**: it paired each primitive
with "its" eigen-frame and slotted `|.|` in as a fourth; that table was
not the taxonomy and is withdrawn. The eigen-frames are classified per
coordinate (three GF(2) bases plus ≤6 lift kinds) times the parameters,
`<<` names no frame (the automaton is Shannon *plus sharing*, and 0027
put sink-ness in the sharing move), and the register is outside the
taxonomy's scope rather than a frame it missed — the taxonomy classifies
representations of a fixed-n function, and a register only means
something over unbounded words, so 0028's finite-frame conjecture is
untouched. What survives and is checked: popcount is the complete
invariant of the S_n position action, `<<` is what 0013/0014 named as
the escape from that invariance, and 0030 already homed
counting/symmetric subclasses in the shared frames. **Why combining levels does not collapse**: union multiplies the
control automata and concatenates the registers, and the two grow
orthogonally — measured, a set sentence moves the control column and
never the register column, a count form over existing measures moves
neither, and measuring a new term costs one register plus the wire
pinning it. Collapse would need a register to name a position; no
sentence has such a term, so no union of sentences does. In
eigen-frame terms the counting level is not new: `&` diagonalises
restrictions, `^` translations, `<<` the shift, and `|.|` is the
complete invariant of `S_n` permuting bit positions (orbits = popcount
levels, verified) — the very invariance 0013/0014's obstruction table
named `<<` as the escape from. A deterministic Parikh automaton factors
a statement into an order-sensitive finite part (control state) and an
order-invariant unbounded part (counters), and `{.} = 2^x` is exactly
the map that turns a value into a position, identifying the two
coordinates the factorisation keeps apart. Scale says it in one line: a
counter is bounded by the word length, a value is exponential in it. The
primitive table is measured — every layer primitive is 1–2 live states
with no counter, `c = |x|` is 1 state with one counter (the counting
level adds a register, not states), and `y = 2^x` has no automaton at
either level (Nerode classes `5,8,11,15,20,25,31,38` at widths 2–9);
balance fails the layer by needing count-against-count, which a counter
supplies, while the level map fails it by needing position-against-value,
which nothing below full arithmetic supplies. This restates 0011's
boundary ("coupling an unbounded set channel to its own cardinality
channel") in its own terms. **The tier**: `CountedAutomaton`, a deterministic Parikh
automaton over the layer's bit columns; counters are monoid
homomorphisms of the word hence padding-invariant; closed under `and`,
`or` and **complement** (free because deterministic — the
nondeterministic Parikh class has undecidable universality); entailment
decidable; canonical form = the Nerode quotient of the configuration
space, presentation-independent on the 0006 test (two unrelated
presentations of balance, identical signatures). **The exclusion**: you
may not count what you freely hide, enforced by measurement with a
witness word, and *allowed* when the hidden channel is functionally
determined (0008's uniquely-determined wire, now carrying a counter).
The exclusion mirrors 0016's knowledge/hypothesis asymmetry exactly and
inverts the layer's economics — in the layer hiding was cheap and
negation was traded; at the counted tier negation is free and hiding is
the dangerous move. Infinite Clue lands inside the guard because a Clue
player counts the hands, and the hands are the named channels.
**Canonicity, settled in three senses (0036).** *Some computable
canonical form*: fails unguarded (a canonical form reached by
terminating reduction IS a decision procedure, and the unguarded theory
is undecidable — so none exists, unconditionally), holds for the tier
(decidable equivalence plus an r.e. class gives "least equivalent
representation", which the layer also has and which therefore
distinguishes nothing). The rewrite-side diagnosis, separate and weaker:
layer operators move bit-length by at most one, `{.}` moves it from L to
2^L, so no measure certifying the layer's termination certifies its own.
*Determined by the semantics*: the intended impossibility for the tier —
a Pareto frontier between control states and registers — **does not
exist**. `popcount ≡ 0 mod m` has presentations at (m states, 0
registers) and (1 state, 1 register) with neither dominating, but the
language is regular with Nerode index exactly m, so the second is simply
not minimal; every buildable trade concerns a regular sub-part that the
minimal automaton absorbs, and on the non-regular part the resources do
not trade. What is true instead: **the register content is free exactly
up to GL(d, ℤ)** — the two presentations of balance have register
vectors related by [[1,0],[1,1]], det 1 (verified), while a singular
matrix collapses a balanced and an unbalanced pair onto one vector. The
register map is the abelian part of the transition monoid, so a change
of register basis is an invertible integer matrix; **GL(d, ℤ) is the
count sort's GL(n,2)**, and 0030 already showed that parameter
mandatory. Structural reading: the layer's canonical form is
coordinate-free because a finite residual set has no coordinates; the
measure makes the residual set infinite, and an infinite state space
must be coordinatised to be written down. **The measure costs
coordinate-freedom, not canonicity.**

**Why `H ^ HK` stops collapsing at `<<`, and the rule that repairs it
(0037).** The corpus's test is complete for `{^, &, 1}` for a real
reason: every one of those operators is **pointwise**, so a failure of
containment squeezes into a one-point universe where entailment and
containment are the same condition (machine-checked on 400 random
terms). `<<` carries position p to p+1, the squeeze dies, and with
`K := x ^ 2`, `H := s(x) ^ 4` the residual `H ^ HK` does not reduce to 0.
**The repair is one rule, and it acts on statements rather than terms**:
*from K infer s(K)*, sound because `s` carries the empty set to itself.
It closes the example on contact — `s(x ^ 2)` pushes down to `s(x) ^ 4`,
which IS `H`, so `H ^ H·s(K)` is 0 with no new term machinery. The
knowledge in force is K's **s-closure** `K | s(K) | ss(K) | …`, and the
depth needed is the **shift-depth of the hypothesis**, read off H — so
the search is bounded a priori, which is the corpus's own termination
requirement. The closure is an infinite union, and a finite
representation of an infinite union closed under the shift is an
automaton: this is the sentence-side derivation of 0006's "the automaton
is the closed form of the stabilizing series" and of 0023's "what forces
the DFA". The templating instinct was right; what gets injected is the
*shifted knowledge*, not the residual. **Sound but not complete, and the
gap is the inverse**: on 2424 random satisfiable K/H pairs neither test
was ever unsound, the upward closure missed 67 true entailments, and all
67 are *downward* inferences (from `s(x) = 4` infer `x = 2`) needing the
injectivity of `s`. The mirror rule *from K infer K >> 1* — the corpus's
own `h`, here a closure rule rather than a term-former — closes every
miss in the sample. **Closing at ingest is a protocol, not a query-time trick**: the closure
distributes over `|` (`C(A|B) = C(A)|C(B)`, verified — `s` and `h` are
ring homomorphisms and `|` is built from `^` and `&`), so recording each
increment as `I' := C(I)` and updating `K := K | I'` gives exactly the
same object as closing K at query time; K never has to be reopened.
Chaining comes free — `A ^ B` is always inside `A | B`, so equalities
compose with no transitivity rule (`x = 2`, `y = s(x)` ⊢ `y = 4`,
verified). **Which operators admit such a rule**: `f` must carry the
empty set to itself *and* be `^`-linear, so that `f(u)^f(v) = f(u^v)`
turns congruence into a rule about whole statements. Measured, only the
two shifts qualify; `+`, `T` and `|.|` all fail — and **the failure of
`+` is exactly the carry**, 0002's founding wall. **The price**: `+`
needs no rule of its own after all, since the shift closure reaches
`+`-entailments given enough depth, but the depth required is
**proportional to the width** — one extra level of closure per extra bit,
measured at four widths (6/8/10/12). So the closed K is an *unrolling*
that grows with the problem, which is the cleanest statement of what the
automaton is for: 0006 called the automaton the closed form of the
stabilizing series, and here the series is `K | s(K) | s²(K) | …`, the
unrolling is width-proportional, and the automaton is what makes it
finite. The two frames are not rivals — one is the closed form of the
other. **And the measure gets no such rule**: `|.|` preserves the empty
set but fails linearity, so there is nothing to close under; `s` is a
linear bijection of statements and stays inside the sentence algebra
while `|.|` leaves the sort — the sentence-side form of the
two-copies-of-ℕ line, and why `<<` needs only a closure rule while the
measure needed a register. Completeness in general is unproven.

**The infinite closure has a closed form, and it is one symbol (0038).**
0037's unrolling does not have to be expanded in the original
primitives. Reading a statement as a set of positions, the up-closure is
every position at or above min(T) and the down-closure every position at
or below max(T), so for non-empty T the two-way closure is **every
position**: `C(T) = 0` if T is empty and the universe otherwise —
verified for every `T < 2^10`. **The infinite union is the nonemptiness
indicator `N`.** It is the primitive the workstream already named:
0015/0016 concluded from the automaton side that what the framing lacked
was the existential, nonemptiness, and here the same object arrives from
the sentence side as the closed form of the shift closure. **It costs
nothing** — 0011's "at least k" at k = 1 is 2 states, so N is already
inside the layer and convexity is untouched. **The test becomes exact**:
`H ^ H·N(K)` collapses exactly when K entails H, 0 unsound and 0
incomplete on 3438 random satisfiable pairs — which also supplies the
soundness check 0037 never ran at its width-proportional depths.
**Rules**: `N(0) -> 0`, `N(1) -> 1`, `N(N a) -> N a`,
`N(a|b) -> N(a)|N(b)`, `N(s a) -> N(a)` (s injective), and the
cancellation `a & N(b) -> a` whenever `N(a)` and `N(b)` share a normal
form — the side condition decided by putting the term in **s-graded ANF**
and dividing out the largest power of `s`. 0037's worked example
collapses in two steps, every intermediate checked semantically.
**Termination** by term size counting shift degree, which the division
rule consumes (200/200 strictly smaller, never larger) — a bound readable
off the term, which the unrolling could not offer. **This corrects
0037's headline**: it is not true that the sentence frame must unroll
while the automaton is the finite form; N is the finite form on the
sentence side. The two are two closed forms of the same series, and
**Tiles, and where the shift's content lives (0039).** The telescoping
identities are a family: `!x ^ s(!x) = x`, `U(x) ^ s(U x) = V₂(x)` (the
lowest set bit, 0008's own primitive), and `N(x) ^ s(N x) = [x ≠ 0]` as
one bit at position 0 — so **`T ^ s(T)` is what a shift-series
measures**. (The proposed `s(x) ^ s(N x) ^ N(x)` is not empty; it fails
at x = 1, 2, 3. Right shape, wrong right-hand side.) `U` also satisfies
the fixpoint `U(x) = x | s(U x)`, the stabilizing-series shape of 0002
exactly. **The closure is tile-wise**: treating `x` and `s(x)` as
different circles on a Venn diagram, `C(K) = ⋃ over K's tiles of
C(tile)`, verified — so it can be taken at checking time rather than at
ingest, and the two are the same computation at different moments.
**What tiles buy is a relocation of the content.** Semantically
`C(T) = N(T)`; symbolically over free symbols it is false (the first
five shifts of the tile `x·~s(x)` are five distinct maps) — that gap is
0037's unrolling. Tiles reconcile them: **the Boolean structure lives in
the tiles, which are free, and everything the shift contributes lives in
the N-layer** as a constraint on which tiles can be non-empty together.
For `{x, s(x)}` only 5 of 16 non-emptiness vectors are realisable, and
every one satisfies `N(x·s(x)) ∨ N(x·~s(x)) == N(x·s(x)) ∨ N(~x·s(x))`,
i.e. `N(x) = N(s x)` — **that single Boolean law is the whole of what
the shift contributes**. Consequently entailment becomes a propositional
implication over the realisable non-emptiness vectors: finite and
decidable by enumeration, a different shape from both the rewrite
closure (0037) and the new term-former (0038), and the same two-layer
split the counted tier has (0035) with a Boolean upper layer instead of
an arithmetic one. Open: the realisable set for larger symbol sets and
whether it is always generated by `N(sᵏx) = N(sᵏ⁺¹x)`; whether the pair
(tile support, realisable set) is canonical, given that tiles are 2ⁿ in
the symbol count; and the N-laws of the other operators — `N(h x) ≠
N(x)` since `h` kills a lone low bit, while `|.|` fails 0037's linearity
criterion yet satisfies `N(|a|) = N(a)` exactly, so that criterion does
not govern this layer.

**The tiles are windows, and the N-layer is the automaton (0040).**
0039's first open question, chased and settled negatively. Over the
symbols `{x, s(x), …, s^(n-1)(x)}` the tile of polarity p is non-empty
**exactly when p occurs as a length-n window of x's bit string**
(verified n = 2, 3, 4) — because bit i of `s^k(x)` is bit i−k of x, so
fixing every polarity at a position fixes the window ending there. A
tile is therefore not an arbitrary Venn region but the assertion that a
bit pattern appears somewhere in x. Consequently the single law
`N(s^k x) = N(s^(k+1) x)` is **sound but nowhere near sufficient**:
realisable vectors number 3, 11, 57 at n = 2, 3, 4 against 12, 220,
64596 satisfying the law (of 2^(2^n) = 16, 256, 65536). What does
characterise the realisable set is the **de Bruijn condition** —
consecutive windows overlap in n−1 symbols, so the occurring windows are
exactly the vertices of a sliding-window walk (free bits while reading
x, then forced zeros above its top bit), and realisable = walk-vertex-
sets exactly at every n measured. **So the tiles are de Bruijn states,
the realisable set is the set of runs, and "which tiles are non-empty"
is "which states the run visits".** The tile decomposition does not
replace the automaton frame — it reconstructs it, at the same 2^n cost,
from the sentence side. That also settles 0039's second question: the
pair (tile support, realisable set) is canonical exactly insofar as the
automaton is, because it *is* the automaton's run structure. And it
revises 0038: the two frames are not independent closed forms of one
series but one object, with 0019's incomparability being about how
compactly a statement is *written* in each, not about what they are.
**The chain, end to end**: the containment test is complete exactly on
the pointwise fragment (0037); `<<` is not pointwise so knowledge must
be closed under it, and the closure is an infinite union (0037) whose
closed form is `N` (0038); the closure distributes over tiles, and over
shift-generated symbols the tiles are the windows of the bit string
(0039, 0040) — so the closed knowledge is the run structure of the
sliding-window automaton, and the sentence frame reaches the automaton
by its own road. Open: whether "tiles are windows" survives other
operators (`{x, x+1}` and `{x, T(x)}` are the immediate experiments, and
would say whether it is a fact about the shift or about the framework);
whether the counted tier's register is the **Parikh image of the same
run** — counts of visits rather than sets of visited states, which would
not be a coincidence since the tier's decision procedure is Parikh's
theorem; and the growth of the realisable set (3, 11, 57).

**T re-expressed: it is not a new series, it is `U` in a mirror
(0041).** Two reconstructions of the corpus's `$`/`T`. **With addition,
a finite term**: `T(x) = x & neg(x+1)`, no series at all — but it closes
a circle with the successor, which the corpus defines as
`succ(x) = x ^ b(T x)`, so **T and succ are interdefinable, each a
two-symbol term in the other, and neither is prior**. **With the
up-closure, no new operator at all**: one bridge identity
`neg(b(y)) = s(neg y)` (b and a are complement-conjugate) makes De
Morgan turn the intersection series into 0039's union series, giving
`T(x) = neg(U(neg x))` — verified. So `$` and `U` are **one operator
seen through complement**, and T inherits U's whole algebra: fixpoints
`U(x) = x | s(U x)` and `T(x) = x & b(T x)`, and telescopings
`U(x) ^ s(U x) =` the lowest **set** bit and `T(x) ^ b(T x) =` the
lowest **zero** bit — the latter being 0039's telescoping family gaining
its T member, and the piece canonicalisation most wants. **No finite
shift-term reaches T**: bit 6 of T(x) depends on x's bits 0..6, every
bit at or below it, while a term of shift-depth d reaches only i−d..i —
0002's locality argument on the term side, which also says the two
reconstructions are the only shapes available. **Canonicalisation
payoff**: T's own tiles over `{x, b(x), …}` are the length-n windows of
x with **ones** padding the bottom instead of zeros (verified n = 2, 3,
4), since b fills with ones where a fills with zeros — so **T inherits
0040 unchanged**, its tiles are de Bruijn states, its realisable set is
the runs, and there is no separate canonicalisation problem for T. Net:
the corpus's operator list is redundant in a specific way — `$` is the
union-series dualised and `!` is the third member of the same
telescoping family. Open: whether the whole family is **one
construction parameterised by the join** (`!` joins with `^`, `U` with
`|`, `T` with `&`; telescopings x, lowest set bit, lowest zero bit),
which would collapse the series zoo to a single schema; whether the
T/succ circle can be broken over `{^, &, <<, N}` with neither series nor
addition, `N` being the candidate unavailable when 0002 ran the locality
argument; and whether 0040's window reading survives a non-shift symbol,
since `b` is still a shift.

**The series zoo is one schema, with its own rewrite rules (0042).**
Every series in the corpus has the shape `S(x) = x ∘ σ(x) ∘ σ²(x) ∘ …`
for a join `∘ ∈ {^, |, &}` and a shift `σ ∈ {a, b, h}`. Nine cells,
enumerated: `(^,a) = !`, `(^,h) = !ʰ` suffix parity, `(|,a) = U`,
`(|,h) = D` down-closure, `(&,b) = T`; `(^,b)` diverges, and `(|,b)`,
`(&,a)`, `(&,h)` are constants. **Five non-trivial cells, and they are
exactly the operators the corpus carries separately** — one construction
with two parameters, not five primitives. **Three universal laws**,
verified for every survivor and serving as the expansion, combination
and cancellation rules: fixpoint `S(x) = x ∘ σ(S x)`, distribution
`S(a ∘ b) = S(a) ∘ S(b)` over its OWN join and no other, and telescoping
`S(x) ^ σ(S x) = the measure`. **Two further properties split by join,
exclusively**: `^` measures x, is invertible, never idempotent (`x =
S(x) ^ σ(S x)` IS its telescoping); `|` measures the extremal element
and `&` the extremal gap, both idempotent and neither invertible. Filled
in: `!`/`!ʰ` measure x, `U` the lowest set bit, `D` the highest set bit,
`T` the lowest **zero** bit. **`N` is not a cell** — `N(x) = U(x) | D(x)`,
verified — which is why it behaves unlike the rest and why its rules had
to be found separately in 0038: combining two cells destroys the
telescoping, since no single extremum survives. **The composition table
for `{N, T, U, D}` closes**: every composite collapses to something
already named, so the set is closed under composition — the property a
terminating rewrite system wants. `N` absorbs on either side, `T` and `D`
absorb each other, and exactly two entries move information rather than
deleting it: `N(T x) -> N(x & 1)` and `T(U x) -> N(x & 1)`, both saying
that `T(x)` is empty exactly when x's low bit is clear. **The resulting
system** is expansion / combination / cancellation / idempotence (`|`
and `&` only) / absorption, and every rule either reduces the number of
series symbols or replaces a series by a measure, so a depth-counting
measure decreases. **Confluence is the honest remaining gap** — the same
one 0038 §6 left open, but the rule set is now finite, uniform and
derived from the schema rather than assembled case by case, so
critical-pair analysis is feasible. Also open: whether losing the
telescoping is generic for joins of cells or special to `N`; and whether
the `h`-side members `!ʰ` and `D`, which fall out of the schema but are
absent from the corpus's operator list, are useful or merely formal.

**Confluence: completed, and the residue located (0043).** 0042 left it
unchecked; checked here by exploring the WHOLE rewrite graph of each
term, so more than one normal form is a proof of divergence rather than
evidence of it (every rule is verified meaning-preserving first, so a
divergence can only be syntactic). **The starting state was worse than
0042 claimed**: 28 divergent terms of 4000, and the size measure did not
certify termination — `distribute` grows terms. **Nine completion
rounds**, each round's smallest witness forcing exactly one missing or
misoriented rule. **Round 1 is load-bearing**: 0042 oriented combination
as *distribute*, and that orientation cannot be completed because it
destroys the very redex telescoping needs; oriented as **collect**
(`S(a) ∘ S(b) → S(a ∘ b)`) the predicted critical pair vanishes outright
— the collected form is exactly what telescope matches — and a genuine
termination measure appears, `(series count, argument size, non-N series,
size, unsortedness)` lexicographic, verified strictly decreasing on every
application. The other eight rounds add constant folding, units and
annihilators, low-bit rules, a constant-splitting rule, and an oriented
commutativity, taking the rule set from five to fourteen. **Result: 2
divergent terms of 4000 remain, and both become identical once the base
algebra is put in ANF** — the engine keeps `|` primitive while the corpus
expands `a | b = a ^ b ^ ab`, where Boolean absorption is an identity
(`1 & (1 ^ x ^ 1x) = 1`). So **the series rules are confluent; the
residue is a base-algebra convention the engine imposed and the corpus
does not have**. Honest limits: exhaustive graph search over 4000 random
single-variable terms at depth 3, not a critical-pair proof over all
terms; the rule set grew from five to fourteen and minimality is
unexamined; multi-variable terms may open pairs this search cannot see.
Open: rebuild on an ANF base (§3 suggests it discharges the residue and
probably absorbs several bookkeeping rules); a Knuth–Bendix proof, now
feasible with a working termination order; and the two-symbol extension.

**Rebuilt on an ANF base: ten rules, and the sampling was wrong (0044).**
0043's rebuild, done. Terms *are* ANF polynomials over `^` and `&` with
`|` built as `a ^ b ^ ab`, so the constructors are total functions into
normal form and **six of 0043's fourteen rules cease to exist** —
constant folding, units, annihilators, idempotence, commutativity, and
`split-constant` (which only existed to expose a constant through `|`).
0043 §3's guess held: both of its surviving divergent terms are
identities here. **But the rebuild also showed 0043's verdict was
under-tested.** In 3000 random depth-3 terms the census reads `collect`
0, `telescope` 0, `N-lowbit` 0 — random terms essentially never build
the redexes of the schema's three *structural* rules, so 0043's
confluence was measured on the bookkeeping. Against a targeted pool
built from those redexes (`interesting_subterms`), the same rules fire
623/46/1, and **six of eight further completion rounds are visible only
to it** — including one that was not a confluence failure at all: a
**rule was unsound**, my port having folded `N-lowbit` into `low-arg` as
`N(t&1) → t&1`, which confuses a bit with the whole universe. Three
rounds collapse into one general side condition — **`collect` fires only
between series atoms that are irreducible alone**, since combination
buries its arguments where nothing can reach them; this is 0043's round
1 stated in general. Two orderings are forced by the base algebra rather
than by rule orientation: **`telescope` is a last resort** (XOR
cancellation creates and destroys its redex behind the rule set's back —
running it first fails in mirror image, stealing a monomial a pending
`fold` would have annihilated), and **`low-bit` must reach through
`shift-out`** via `h(D t) & 1 → N(h t) & 1`, which trades a named series
for `N` at the cost of a bigger argument and so reorders the termination
measure to `(series count, non-N series, argument size, size)`. One
genuinely **new** rule, not in 0043 and not bookkeeping: **`N-absorb`,
`N(p) & m → m` wherever `m` vanishes with `p`** — the statement that `N`
is a *guard, not a factor*, since `N(p)` is the whole universe exactly
where anything derived from `p` is non-zero. Also new to 0042 §4's
table: `N(! t) = N(t)` and `N(!ʰ t) = N(t)`, the `^` series being
invertible and fixing 0. **Result: ten rules, no divergence in either
pool** — 2996 random and 1137 structured terms explored to completion,
all 22 canonical redexes firing their rule with exactly one normal form,
soundness over 2615 + 6410 applications, termination strictly decreasing
throughout. Honest limits: still graph search rather than a
critical-pair proof; 63 of 1200 structured terms hit the node cap;
still single-variable; and confluence now leans on two *strategy*
conditions rather than orientation alone — ordinary priority rewriting,
unique normal form, but a weaker object than unordered confluence. Open:
whether `N-absorb` is a law of the schema rather than a repair (it reads
like `N`'s analogue of distribution, and would belong in 0042 §2);
whether `telescope`'s ordering can be removed by a representation in
which cancellation is itself a rewrite; and two symbols, now with a
targeted pool to generate from.

**The right shift is `&` in disguise, and it comes out (0045).**
Objection to 0044 §9: `h` has no business being primitive, because `&`
was the only operator that could erase information and Post's lattice
gives a two-valued logic one information-losing direction, not two. The
objection holds on every count. **`a(h(v)) = (Ω^1) v`** for every `v`,
and — the statement that settles it, since an operator's information
loss *is* the partition it induces — **`ker h = ker (&(Ω^1))`**, the
same 2048 classes. `h` destroys the low bit, by masking, and nothing
else. The **general elimination**: `a` is an algebra homomorphism, so it
pushes to the leaves and cancels at an `h`; for a base-algebra term of
`h`-depth `d`, **`a^d(E)` is `h`-free and equals `E << d` exactly** —
stronger than the zero-equivalence asked for, and `E = 0 ⟺ a^d(E) = 0`
follows. Verified on 1849 terms carrying an `h`. **What the series
column costs is exactly the two cells the corpus never had**: dropping
`h` from 0042 §1's table deletes `{!ʰ, D}`, which is precisely the pair
0042 §6.3 flagged as absent from the corpus's operator list, leaving
`{!, U, T} + N` — the corpus's own series. **`N` is the language's one
downward channel**: measured, every `h`-free operator is LSB-causal
(output bit *i* depends only on input bits ≤ *i*) and `N` is not, so
nothing over `{x, ^, &, a, b, !, U, T, constants}` computes it — which
is no obstacle, since `N` is already primitive, and is the sharper
statement of what `h` was for. **The rewrite system stays confluent**
with `SHIFTS = {a,b}`, `SERIES = {!,U,T}`: nothing had to be added, the
ten rule names are unchanged, and the tables inside shrink from 47 to
**32 rule instances** (`absorb` 18→10, `collect`/`telescope` 5→3 each).
One rule disappears outright, `h(D t) & 1 → N(h t) & 1` — and **that was
the rule that forced 0044 §5's measure reorder**, so 0043's ordering
`(series count, argument size, non-N, size)` is verified sufficient
again. Honest cost: 0042 §3's `N = U | D` stops being a sentence of the
language; `N` keeps its rules and its behaviour, loses its derivation.
Limits: the `a^d` procedure covers `h` in the base algebra only — it
does not push through a series argument (`a` does not commute with `T`),
which §3 makes moot by deleting the `h`-series rather than translating
them; the causality test is exhaustive at width 10 for the listed
operators, not a proof over all expressions. Open: whether `N` has a
telescoping after all, now that `N = U | D` is unavailable as its
explanation; whether `{^, &, a, constants} + N` is minimal (`b(t) =
a(t) ^ 1`, so `b` is not primitive), which is 0013/0014's Post-style
completeness question applied to what remains.

**The guarded canonical form exists, and the wall is somewhere else
(0047).** Target: a form sound and complete for *true* statements
(terms denoting ∅), sloppy about which nonempty set a false one
denotes, so undecidability gets pushed out of the true class. **First,
the guard buys nothing on the decision side**: `E1 = E2` iff
`E1 ^ E2 = 0`, and `^` is in the signature, so recognising exactly the
true statements *is* deciding the word problem. Only the *output* can
be weakened — a zero test owes no normal form to the nonzero terms.
**The invariant that decides is not LSB-causality (0045 §4) but bounded
state**: every operator but `N` is a one- or two-state Mealy step read
LSB upward (`!` carries a parity bit, `U` a seen bit, `T`/`lowzero` an
alive bit, `a` a delay), so an `N`-free term is a finite transducer and
"identically 0" is reachability — verified against the interpreter on
24000 runs over 4000 two-variable terms. **`N` is exactly the guard**:
fix each `N` subterm to 0 or Ω, carry one emission flag per `N`
argument plus the root, close each configuration under a tail of zeros,
and accept a guard only when the settled flags match it. 2^k sweeps for
k distinct `N` subterms; against brute force on 1500 terms, every
refutation carries a witnessing input and no term called empty is
nonzero at width 11. 0038's and 0042's hand-found `N` rules all fall
out of the guard, with no rule for `N` at all. **The canonical form is
(guard, minimal Mealy machine) per consistent guard, and the statement
holds iff every entry is the zero machine** — 600 terms, never
disagreeing with the decision procedure. So the answer to the question
as asked is *positive*: at the 0046 signature nothing is undecidable.
**What the exercise actually found is two defects in 0043–0046.**
(1) **Width-bound**: 30 of 836 normal forms do not mean what the term
meant, because `fold` evaluates constants inside a fixed width —
`a(Ω) → 510`, `!(Ω) → 341` at width 9, when unboundedly `a(Ω) = Ω ^ 1`
is *cofinite*. Those rewrites are sound at width 9 and at no other.
(2) **Incomplete**: 3 of 836 terms are identically empty without
normalising to `0`, and 92 pairs mean the same at every width with
different normal forms; six named true laws are missed six times over
(`b(x) = a(x)^1`, `T(a x) = 0`, `U(b x) = Ω`, `N(x&1) = !(x&1)`,
`a(Ω^x)·b(x) = 0`, `7 = 1 ^ 6`). **Correction to 0044**: its census
listed `fold-of-two-constants` among the rules "gone — building an ANF
polynomial already does them". It is not gone; ANF folds constants only
when the masks are *equal*, where cancellation does it, so
`xor(const 1, const 6)` is two monomials with no rewrites. **The repair
is a new kind of constant, not a new operation**: the constants are not
closed under the signature (`U` of any nonzero finite set is cofinite,
`!(Ω)` alternates forever), every closed term is a machine with no
input hence a **lasso**, and the rewrite system's constants must be
ultimately periodic `(prefix)(cycle)^ω` rather than integers — 0046
§2's algebra/rewrite signature split arriving a second time. **The wall
is bounded state**, measured by residual counts: `x ^ y` needs one
state, `x + y` needs two (**so addition is free** — a finite-state
operator the corpus never had), `x * y` is LSB-causal yet its count
multiplies by four per bit read (1, 4, 16, 64, 256, 1024, 4096). Limits:
the decision procedure is verified, not proved; brute force bounds the
"empty at every width" direction at one width only; the head-to-head is
single-variable because the engine is; the rewrite system has **not**
been rebuilt over lasso constants. Open: rebuild `fold` over lassos;
find which identities are unreachable by *any* finite rule set over
this signature (the sharp form of "canonicity leaves the term
language"); take addition into the counted tier of 0034–0036; and
whether the guard count `k` can be reduced the way the machine merges
states.

**Canonicity in sentence form: the mask goes, containment is left
(0048).** Two objections to 0047: `7` vs `1 ^ 6` was never a gap in the
algebra — constants are not primitive (0046 §1) and that pair exists
only because the engine carried an **integer mask** on every monomial —
and the machine speaks to procedure where a sentence speaks to
structure. Both hold. **Mask-free ANF**: a monomial is a set of atoms
and the EMPTY monomial is `Ω` (the multiplicative unit, since
`Ω & t = t`); a polynomial is a set of monomials and the empty one is
`0`; atoms are `x`, `1`, and the unary operators. No integer appears.
The load-bearing construction is that **`a` pushes to the leaves** — it
is a homomorphism for *both* joins, since bit *i* of either side reads
bit *i−1* of each argument — which makes **`a(Ω) = Ω ^ 1` a fact of
construction rather than a constant evaluated at some width, and that
is 0047 §5's entire width-bound family repaired**. Of 0047's seven
laws, **four are then free** (`b(x) = a(x)^1`, `a(Ω) = Ω^1`, `7 = 1^6`,
`a(Ω^x)·b(x) = 0`); the three that survive are all about the argument's
low bits. **One syntactic analysis covers them**: `known_prefix(P, d)`,
the 0047 machine table run over `{0, 1, unknown}` (checked on 288000
bit-positions), feeding `settle`, `low-bit` and `confine` — where
`settle` reads the prefix of an *argument* and `low-bit` reads bit 0 of
a monomial's *factors*, the same analysis at opposite ends. **`settle`
never fires above the argument's own shift depth** (measured: positions
0–3 over 3000 terms, `a`-depth 2), which is what "bounded state" looks
like in a sentence — the term carries its own bound. **Which KIND of
rule a schema cell needs is read off its join alone**: `^` makes the
two-element algebra a *group*, so nothing absorbs and no prefix ever
settles `!` (or its identity measure) — only cancellation, i.e.
telescope; `|` saturates at Ω and `&` annihilates at 0, and both settle.
0042 gave one schema for the operators; this is one for their rules.
**Eleven rules** (`settle`, `low-bit`, `confine`, `unit`, `absorb`,
`shift-out`, `N-see-through`, `N-absorb`, `contain`, `collect`,
`telescope`) against 0043's fourteen and 0044's ten, all 2284 sampled
applications meaning-preserving. `fold` is gone — no constant domain —
leaving only `unit`, a closed width-free table on `0` and `Ω`;
`low-arg` became `confine`; `N-shift` split into `settle` (the `b`
case) and `N-see-through` (the `a` case), which are different facts;
and `telescope` had to be generalised to fire under a common factor.
**The threshold is containment.** The schema carries an order,
`T(t) ⊆ t ⊆ U(t) ⊆ N(t)`, with **`U(t)` the top of everything the
schema builds from `t`** (measured over `t`, `!(t)`, `T(t)`, `U(t)`,
`lowset(t)` and every `a`-shift; the exceptions are the predicted ones —
`lowzero(t) ⊆ U(t^Ω)` is the dual, `N(t)` is above everything). Adding
`contain` cuts unidentified pairs 36 → 19, **and the 19 survivors are
also containments**, needing `A ⊆ B` with `B` compound (`T(t) ⊆ b(T t)`,
`N(t&1) ⊆ U(t)`). So: **every gap that survives the mask-free
representation is a containment, and containment is what an ANF engine
cannot see on principle** — `⊆` reads `A & B = A`, ANF is built on `^`,
`^` makes the algebra a group, and a group admits no compatible order.
That is 0045's Post argument from the other side: there only the
ordering direction loses information, here only the ordering direction
is invisible to the canonical form. Limits: the rule set is **not**
complete and 0044's divergence search has not been re-run over this
representation, so confluence does not carry over; `contain` implements
a deliberately conservative atom-against-atom fragment of `⊆`, which is
what the 19 survivors measure; single variable; the machine is used
only as an oracle. Two mid-build claims corrected against measurement:
that the representation absorbs `low-bit` (it absorbs only the shift
half — `S(t)&1 = t&1` is a real rule), and that `lowset`/`lowzero`
never settle (they do, at the same bit their series does; only `!` never
does). Open: give containment a representation — a normal form keeping
monomials in a `⊆`-antichain would absorb `contain` the way ANF absorbs
commutativity; prove `U(t)` is the top of the orbit; re-run the
divergence search; and whether `!(Ω)`, which has no finite name over
`{1, a, ^, &}`, deserves a symbol.

**Containment closes; the wall is ANF's rule shape (0049).** 0048 called
containment a wall. Premature — it repeated the mistake this workstream
already got past once, and the fix is the corpus's own method: write the
infinite series and name its closed form. **The infinite expression was
already written down**: 0042 §2's *first* universal law is the fixpoint
`S(t) = t ∘ σ(S t)`, whose unfoldings
`T(t) = t & bt & … & b^k(T t)` and `U(t) = t | at | … | a^k(U t)` are
each a containment statement about the closed form — `T(t) ⊑ b^k(T t)`,
`a^k(U t) ⊑ U(t)`, at every k. 0048 implemented telescoping and
`collect` and **never implemented the fixpoint**, which is why
containment looked external. **No new primitive is introduced.** **The
name is the down-set** `↓S = {A : A ⊑ S}`, which is closed under all
three joins — `^` included, because a down-set is a *subgroup* as well
as a sublattice (1800 checks, none escape). That is how containment
crosses `!`, which is measured **not monotone** (`1 ⊑ 3` but
`!(1) = Ω ⋢ !(3) = 1`; `a`, `U`, `T`, `N` are monotone, `!` and both
measures are not — 0045's Post split, third appearance): every partial
sum `⊕_{k<n} a^k(t)` is in `↓U(t)`, which is `^`-closed, so the closed
form `!(t)` is too. Hence **`U(t)` is the top of the subalgebra
generated by the orbit `{a^k(t)}`** — 0048 §6's measured claim, now
derived. All eleven containments 0048 needed follow from the fixpoint
law plus the down-set; of 144 derived containments checked against
0047's decision procedure, **none is false**. **Closure measured: 952
true containments among 2500 random pairs, 804 derived (84%)**; of the
148 escapes, 118 are reached once both sides are normalised (not
containment gaps), 7 are `N`-guarded, and **the 23 structural ones all
have the upper bound as a XOR-sum that is secretly a union or a
complement** (`a(x) ⊑ Ω ^ 1`, `1x ⊑ a(x) ^ x ^ a(x)x = x | a(x)`) —
adding the two clauses that recover those took the relation 68% → 84%.
**So the boundary is which joins have names.** ANF stores `P | Q` as
`P ^ Q ^ PQ`, so an unnamed n-fold union costs **2^n − 1 monomials**
(measured: 1, 3, 7, 15, 31, 63, 127) with the join erased, while a named
one is **one atom** — `U(x) = x | a(U x)` folds the whole orbit. 0019(d)
already floors the recovery search: canonicalising is coNP-hard, so no
rule set recovers hidden joins in polynomial time unless P = NP.
**But the decisive measurement is that installing the relation into
0048's rewrite system moves the residue 19 → 19.** `contain` has one
shape — drop a factor from a monomial — needing `A ⊑ B` between two
*atoms* in a product. The containment that matters is against the
*polynomial* `b(T t) = a(T t) ^ 1`: `T(t) ⊑ b(T t)` is derived and true,
`T(t) ⊑ a(T t)` is false, so the factor-drop is simply wrong and the
real law `T(t)·a(T t) = T(t) ^ t&1` relates two two-monomial
polynomials. Nothing in an ANF term is a "product of A and B" any more —
the product was expanded on construction, exactly as `|` was. **ANF is a
normal form for one of the three joins; the other two survive only as
expansions a rule must re-find by search.** That is the wall: not
expressive power, not containment, but that the representation making
`^` free makes `&` and `|` invisible. Limits: 84% is reach over one
generator at depth 3, single variable, and the relation is deliberately
a sound derivation system rather than a decision procedure; soundness is
machine-checked against a verified-not-proved oracle; §6 diagnoses the
rule shape and does not supply the repair. Open: a representation
normalising the *meet* — monomials as a `⊑`-antichain, now that a usable
`⊑` exists — so `contain` is absorbed by construction the way ANF
absorbs commutativity; which joins are worth names and whether that
family is finite (`N = U | D` is the only named join of two different
cells); and whether 84% is a plateau or whether a complete
join-recovery procedure exists at exponential cost — which would put
this boundary exactly on 0019(d)'s and make the obstacle complexity
rather than expressiveness.

**Expand instead of collect; addition is a guarded cell (0050).** Two
corrections and one construction. **Containment is not a relation
needing a derivation system — it is a statement, `A ^ AB`** ("A is empty
where it misses B"), and a canonical form that sends true statements to
0 handles it with no order theory. 0048 and 0049 both built machinery
that was not needed. **Expansion, not collection**: 0043 picked
`collect` before there was a canonical form to judge it against; running
0042 §2's fixpoint law FORWARD (`S(t) -> t ∘ σ_S(S t)`) and letting ANF
cancel gives **all three telescopings at one unfolding** — `!(t)^a(!t)`,
`U(t)^a(U t)`, `T(t)^b(T t)`. Two things had to be right: the
**measures must unfold too** (`lowset(t) = t & ¬a(U t)`,
`lowzero(t) = ¬t & b(T t)`, both verified), and expansion must be
**top-level only**, since an occurrence inside `a(…)` that unfolds to a
different depth stops cancelling. **`collect` is NOT subsumed at any
depth** — expanding `!(x)^!(y)` and `!(x^y)` leaves the same question
one shift up forever — because it is 0042 §2's *second* law,
distribution, independent of the fixpoint; 0044 ordered the two against
each other as rivals and they are not the same fact. As a **sentence test** —
the corpus's own criterion, "does `A ^ B` reduce to 0", not "do two
terms share a normal form" — with both rules deleted: **82 true
statements, 80 reduce to 0**, and the 2 that do not are `T(T x)·T(b x)`
shapes needing `collect`. So deleting `collect` costs 2 of 82 and
nothing else is missing. **Three corrections to an earlier draft, all
defects in the procedure and none in the algebra**: expansion as a
uniform pass is the wrong operation (telescoping needs the shifted copy
held FIXED while the bare one unfolds; stranded terms like
`a(x) & lowset(x)` need an unfolding UNDER the shift; no single pass
does both, so expansion must be a **positional rewrite**); `a` is a
homomorphism so expansion must push through it, and leaving `a(U t)`
opaque stranded `a(x) & lowset(x) = 0`; and a **capped search is not a
failed search** — every rule preserves meaning, so reaching 0 on one
path is a proof, and discarding capped results hid the rest. An earlier
draft's "15 unidentified pairs" measured those three bugs, not the
sentence form. **Every containment 0049 needed goes to 0**, including
`T(t) ^ T(t)a(T t) ^ T(t)1` at depth 1, which is exactly the identity
**0049 §6 called the wall**; it was a wall only because `contain` was
written as a factor-drop between two atoms when the statement is a
polynomial. So 0049's conclusion is corrected: the obstacle was the
rule shape, not ANF's blindness to order. **Cost by join** (monomials in
k terms of a series): `&` is 1, `^` is k, `|` is 2^k−1 — the same number
0049 §5 found, now as the price of expanding rather than of failing to
recognise. **Addition**: `p = x^y`, `g = x&y`, **`C = g | (p & a(C))`**,
**`x + y = p ^ a(C)`** — verified exactly on 4000 pairs at width 24,
using nothing but `^`, `&`, `|`, `a`. That is 0042 §1's schema shape
with the shift widened: `C = ⋁_k σ_p^k(g)` for `σ_p(z) = p & a(z)`, so
**addition is the `|` cell over a guarded shift**, and the schema's own
two shifts are the constant cases of one affine family
`σ_{p,q}(z) = (p & a(z)) ^ q` with `a = σ_{Ω,0}`, `b = σ_{Ω,1}`. `U` is
the p=Ω member of the family the carry already lives in. **`succ` is the
y=1 case**: `C(x,1) = T(x)` for every x < 2^14, so
`x+1 = (x^1) ^ a(T x) = x ^ b(T x)` — the trailing-ones mask is the
carry set of adding one, and 0041's "neither T nor succ is prior" is
that identity read both ways. **All three universal laws survive for the
guarded cell** (fixpoint by definition; distribution over the base with
the guard fixed, so `collect` applies unchanged; telescoping with
measure `g & ¬σ_p(C)`, which at p=Ω, g=t is `lowset(t)`) — so it is a
full member of the schema, not a degenerate one. Limits: 15-vs-19 is
sampled, neither system complete; **termination is not established** for
expand-and-cancel — it is a canonicalisation procedure with a depth
parameter, not a terminating rewrite system; addition is verified
numerically and by unfolding, not proved, and only for the `|` cell; the
affine family is stated from three data points. Open: redo 0042's
nine-cell table over affine shifts (does guarding fix the divergent
`(^, b)` cell?); terminate the expansion; and multiplication — 0047 §7
put the wall at unbounded state and located it at `x·y`, which with a
guarded shift is a sum of `2^i`-shifted copies guarded by y's bits, the
same shape one level up, so whether that is a second widening or where
the family genuinely stops is the sharp question and is where this
workstream's boundary should now be tested.

**Expand-and-cancel: not terminating, not confluent — both theorems
(0051).** Asked for hard proof, computationally verified; both
properties FAIL, each with a finite machine-checked certificate, and
each failure is structural. **The inner loop terminates, by a real
reduction order**: counting measures provably cannot work (`shift-out`'s
b-case rewrites one atom into the two-monomial `a(S t) ^ 1`, duplicating
every sibling — 0043/0044/0048's measured terminations sampled around
this), but a **multiplicative interpretation** — monomial = product of
atom weights, `w(S(P)) = 2K^(W(P)+1)`, `w(N(P)) = K^(W(P)+1)`, K = 2048
— absorbs duplication natively; every rule reduces to a "K^linear beats
linear" root inequality, checked exactly for n ≤ 600, audited on 3272
computable applications. **The inner loop is NOT confluent**: L
terminates, so complete normal-form sets are computable exactly, and
`1x | U(1x)` reaches both `N(1x)` and `N(1x) ^ 1x ^ N(1x)·1x`, both
irreducible — 40 of 2918 scanned terms diverge; by Newman, local
confluence fails. Two corrections to 0048 fell out: its harness
**silently skipped divergent terms** (`if capped or len(forms) != 1:
continue`), and the scan caught a divergent pair that was not
semantically equal, exposing an **unsound rule 0048 shipped**:
`T(lowzero t) → lowzero(t&1)` — the true law is `lowzero(t) & 1`, mask
OUTSIDE, which the absorb table cannot express; wrong at `t = Ω`; entry
removed, neighbours re-audited sound. **Expansion does not terminate**:
the reduction graph of `!(x)` is a SINGLE INFINITE PATH (`X_k = ⊕a^i(x)
^ a^k(!x)`, checked to k = 40: no local redex, exactly one expansion,
sizes strictly increase) — no strategy escapes because there is never a
choice. **Worse, weak normalization fails**: series-free N-free terms
are d-local (bit i depends on window `[i−d, i]`, d = a-depth; 7.6M
window checks), no series or measure is d-local for any d (witnesses at
every d ≤ 8), and N-guards do not help (on `x_r = 1<<r` the flags are
eventually constant, so a flat-plus-guards term is local on a tail of
the family, and U separates inside a shared window). Every normal form
is flat-plus-guards, so **`U(x)` has no normal form at all** —
non-termination is 0002 Prop 4's "the series is necessary" promoted to
the whole rewrite system. **Expand-and-cancel is NOT confluent**:
`!(x&1) → N(x&1)` by confine, and `→* x&1 ^ a(N(x&1))` by
expand-then-reduce — both irreducible, distinct, equal at every width.
Diagnosis exact: `N` is the one operator with no fixpoint law (0042 §3),
so expansion cannot chase what confine mints; **the failure of
confluence IS the failure of N to have an expansion, made local** —
0047's "N is the guard", in sentence form: N is where determinism dies.
**Knuth–Bendix on the wreckage** surfaced two missing rules, not
guessed: `N-fold` (`C·p ^ C·a(N p) → C·N(p)`, p confined to bit 0 —
N's fixpoint on the one domain where it has one, a contraction where an
expansion was impossible) and `annihilate` (a monomial with finite
support bound and all-zero known prefix is 0 — expansion of measures on
constants mints `a(a(1))·a(1)` and nothing else removed it). Both sound,
both fit the order; census 46/471 unjoined → 23/477, the certificate
and the stuck-truth example heal; completion NOT run to closure, so the
repaired system's confluence is a conjecture — the theorem is the
negative one. **Consequence**: reaching 0 on any path is a proof, but a
true statement can also reduce to a stuck nonzero term (`!(1x) ^ N(1x)`
→ 0 by confine, →* `N(1x) ^ a(N(1x)) ^ 1x` irreducible by
expand-first), so "normalize and read off" is impossible and "search
for 0" is forced — 0050's `decides` retro-justified from first
principles. Open: run completion to closure; test confluence of the
N-free fragment (every certificate ingredient needs an N-minting rule);
whether 0047's per-guard emission flag can be internalized as a bounded
family of N-folds; weight-aware search priority.

**Multiplication is a series, and it brings a products schema (0052).**
Asked: express multiplication by infinite series of existing primitives
and find the new useful series. The decomposition is forced (peeling
y's low bit needs the banned right shift), and it is **one new
constructor**: the guarded diagonal family `t_i = a^i(x) & N(a^i(1)y)`
— a two-track shift advancing accumuland and probe together, with `N`
as the 0/Ω scalar. Then **`x·y = Σ⁺_i t_i`** (exact, exhaustive to
128×128 and 4000 wide pairs), with Σ⁺ the 0050 carry, so every carry
inside is the guarded-shift `|` cell; multiplication by a constant
needs no `N` (guards evaluate; `x·a(y) = a(x·y)`, `x·b(y) = a(x·y)+x`).
**Folding the SAME family with each join gives four products**, each
verified against an independent definition: `^` → carryless product
(GF(2) convolution), `|` → Minkowski sum `{i+j}`, `&` → erosion (guard
dualises: absent terms are Ω), `+` → multiplication — dilation/erosion
are mathematical morphology's pair, and `·` sits beside them as the
fourth join. **0042's unary schema is the y = Ω column**: `x⊗Ω = !(x)`,
`x⊞Ω = U(x)`, `x⊖Ω = 0` (the "dead" cell is erosion by an infinite
structuring set), `x·Ω = −x` — and the b-fill erosion at Ω is `T(x)`.
**The `+` join completes 0042's nine-cell table with a fourth row**
whose fixpoints solve algebraically: `S = x + a(S) ⟹ S = −x`
(negation), `S = x + b(S) ⟹ S = ¬x` (complement) — a group join like
`^`, telescoping exact, and complement becomes a CELL where it
previously needed `Ω = N(b 0)`. Since `Ω = −1`, the tiers meet in the
2-adics: **lassos are the odd-denominator rationals** (`(10)^ω = −1/3`,
`(01)^ω = −2/3`, verified as `q·pattern ≡ p mod 2^24`), so the constant
tier is closed under all four products. **The laws lift**: distribution
is diagonal in the x track (4×4 table measured — each product over its
own join and no other, 0042 §2 verbatim; erosion anti-distributes in y,
the morphology duality); `1` is every product's unit; `a` is a
homomorphism in each argument; `⊗`, `⊞`, `·` commute and `⊖` does not;
and **`N` is multiplicative** — `N(x P y) = N(x)&N(y)` for the three
domain products, a ring-homomorphism law for the operator 0051 proved
cannot be expanded. **The majority walks in as the family's carry**:
`x+y+z = (x^y^z) + a(xy ^ xz ^ yz)` — Post's monotone self-dual clone
as the 3-ary carry, the Wallace-tree layer; the candidate named series
for a coalescing `·`-system are `⊗` (the linear layer) and the
majority layers. **The wall re-measured**: all four products cross
bounded state at the same measured rate (4^p residuals at these
parameters), so the wall is unary-series vs binary-products in every
join, not `+` vs `·`; and every constant slice returns inside —
`x → c·x` has exactly `c` residual classes for odd c. The decidable
tier in product language: the schema, its products with one argument a
lasso, and their compositions. Limits: numeric verification at widths
10–26 plus exact algebra; no asymptotic claim on the residual tie; no
rewrite system built — deliberately, per 0050/0051's coalesce-not-
expand lesson. Open: the coalescing system for `·` (symbols: `⊗` and
the majority layers; first laws: diagonal distribution and
N-multiplicativity); the b-fill product row (borrows/subtraction);
guarded products toward division and the counted tier; and the 2-adic
reading (`subsets of ℕ = ℤ₂, statements = zero tests`) as an
organizing principle for the corpus.



Open:

completeness of `{N, ^, &, s, h, constants}` (yes on the sample, now for
a structural reason); confluence, which is unchecked and which a
canonical form also needs; the law for `N(h a)` (`h` kills a lone low
bit, so `N(h a) != N(a)`); and `N(|a|) = N(a)`, the one law relating the
two levels inside the sentence algebra, which may give the counted tier
the sentence-side handle 0037 said it lacked. **Correction recorded**: an
earlier version of 0037 concluded no rule set could repair the test; it
reached that by reasoning about values of x where K is not empty, which
the framing excludes — asserting K *is* the definition of the context.
**Correction to 0035 §1**: the count level's equality is `^` after all
(counts are numbers, `a ^ b = 0` iff `a = b`), and the acceptance
predicate need not be Presburger — if it is Büchi-arithmetic definable,
i.e. the count level carries the layer's own signature, the tier stays
decidable and Boolean-closed, since the achievable register vectors are
semilinear hence Büchi-definable. So **the count level is a second copy
of the layer's language, and the discipline is about *level*, not about
which operators are available**.

Remaining open, now sharper:
prove the GL(d, ℤ) statement in general (only the instance is checked);
finite presentability of the Nerode quotient off the window; and whether
the canonical form is reachable by rewriting rather than by
construction-then-minimisation.

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

1. **Close the counted tier's canonicity** (0034 §8): show the Nerode
   congruence on configurations is Presburger-definable and decidable
   via the product automaton's semilinear Parikh-indexed reachability.
   That converts the tier from *decidable* to *convex* in this
   workstream's sense, and it is the last step between 0034 and the
   framework's own standard.
2. **The level-crossing extension, upward** (0009's path 1): 0034 uses
   the {x} = 2^x map only downward (sets counted into numbers), where
   counters are the abelian shadow of the coarse level. Genuine
   exponentiation statements need the coarse level to be a second
   *automaton* rather than a counter vector — a pair of automata joined
   by the level map, with 0034 §5's scale rule as the interface
   discipline. This is the remaining half of the × prize (bounded
   factors are done) and the whole of the exponentiation prize.
   Alternative if it stalls: sound-partial × after proving the two
   conservativity lemmas of 0005 §2.
3. **Prove the Post-style completeness criterion** (0013/0014): the
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
4. **The closure principle** (0002): convexity preserved under bounded
   stabilizing series, as a theorem — now with the sharper conjectured
   form: series with finite-state transition structure land in the
   automatic fragment (0006's "automata are the closed forms"), and
   0008's addition-as-one-hidden-wire as the worked exemplar.
5. **ω-extension** for the infinite game: S1S/Büchi territory; the
   canonical object needs a design decision (minimal Büchi automata not
   unique). After 0034 this is the only remaining piece of "infinite
   Clue" untouched — unbounded decks are handled, genuinely infinite
   plays are not.
6. **Variable-size counting**: closed for equal-unknown-size hands by
   0034's counted tier (Presburger on counters over the automatic
   layer, which is what "hands of equal unknown size" needed). Still
   open from 0007: the observed monotone shrinkage of K's canonical
   size under knowledge updates.
7. **Where the counted tier sits in the frame taxonomy** (0026–0033):
   its state space is infinite and semilinear rather than a product
   over coordinates, so it is the first natural object outside the
   product structure over which 0028's finite-frame conjecture was
   stated. Whether it refutes or merely extends that conjecture is
   open.
