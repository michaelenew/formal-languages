# 0005 — The zero-law OR without ×, guarded convexity, and scope

Responds to three redirections: (1) the logical OR only needs the zero
law, not full multiplication; (2) undecidability of × is only a blocker if
it interferes with deciding the zero question; (3) the construction is not
of arbitrary sets — well-ordering is in play. Each point survives scrutiny
and sharpens the program. Addition remains the first prize (its symbolic
form is untouched by everything below).

## 1. The zero law needs no arithmetic at all

The needed operator: `X ⊗ Y = ∅ iff X = ∅ or Y = ∅` — OR at the truth
level, since statements are expressions asserted empty. Point taken and
strengthened: not only is full × unnecessary, *any* arithmetic content is
unnecessary. Introduce ⊗ as a **free statement-level operator** pinned to
the zero law alone, living in a layer above the expression algebra:

- Expression layer: {^, &, shifts, add, …} — terms denoting sets.
- Statement layer: emptiness-assertions about expressions, combined by
  ∪ (assertion-AND: union empty iff both empty — the existing K-update)
  and ⊗ (assertion-OR: the zero law).

Semantically the statement layer is a **distributive lattice** of
emptiness-conditions: "A=∅ or (B=∅ and C=∅)" ≡ "(A=∅ or B=∅) and (A=∅ or
C=∅)", so ⊗ distributes over ∪ and vice versa. Canonical form: flatten to
CNF/DNF over emptiness-atoms, sort, dedupe — terminating, no cleverness
(exponential, like ANF; convexity never promised efficiency).

**The subtlety that rules out the cheap version.** The obvious rewrite
rules — `0 ⊗ Y → 0`, `X ⊗ 0 → 0` — are sound but *incomplete* precisely in
Clue's central situation: disjunctive knowledge. If K contains the fact
A ⊗ B (a refutation: "the shown card was one of these"), then K entails
A ⊗ B semantically, but neither A nor B individually reduces to 0, so
componentwise rules never fire. Completeness needs the lattice laws (case
analysis via distribution), not just the zero rules. With them, statement-
layer entailment reduces to: monotone-formula entailment over an atom
poset whose order is expression-layer containment (`ab ^ a → 0`) —
decidable relative to the expression layer, since only finitely many atoms
occur in K and H. *(Proof obligation, not yet discharged: the exact
reduction and its completeness — next after symbolic addition.)*

Why this was invisible before: the framework's beautiful trick — K as a
*single expression*, conjunction as ∪ — works because AND of emptiness
internalizes as an expression operator. OR of emptiness resists
internalizing: an expression `X ⊗ Y` satisfying the zero law needs each
element to witness nonemptiness of both operands, i.e. an injective
pairing of elements. In a *finite* universe this is available (Cartesian
product into a re-encoded universe), which is why the finite game never
forces the issue. In the positional encoding, pairing positions is
super-linear, and WS1S-definable position maps are only i ↦ i + c — so
the internalized ⊗ is unavailable exactly where the infinite game lives
*(argument sketch, not a completed proof — the completed version should
show no automatic relation realizes the zero law over infinite sets)*.
The statement layer is the honest home for OR either way: it needs no
pairing at all.

Where × does remain relevant: only if one wants *sizes to multiply*
(|X×Y| = |X||Y|). That is genuine arithmetic content beyond the zero law,
and it is priced accordingly (§2). Clue's disjunctive facts, meanwhile,
funnel back to the additive side: "refuter holds one of c1, c2, c3" is
size(hand ∩ {c1,c2,c3}) ≥ 1 — a counting fact. Nonemptiness assertions in
general are size-≥-1 assertions, which is why they resisted the emptiness-
only framework, and why addition is indeed the first prize.

## 2. Guarded convexity: undecidability as a scope line, not a wall

The second point, formalized. Split convexity's contract:

- **Soundness, everywhere**: whatever reduces to 0 is true. Any sound
  rewrite rules for any operator (including full ×) preserve this for
  free.
- **Completeness, on a marked core**: a syntactically recognizable
  sublanguage (the *guard*) on which "fails to reduce" provably means
  "not entailed".

Call a language **guarded-convex** if guard-membership is itself decidable
by inspection and the reduction is complete on guarded statements. Then
Gödel/Matiyasevich are not walls but the *location of the guard line*:
full × may exist in the language as a sound-only operator (all ground
uses decide fine — compute and compare), while the guard excludes exactly
the symbolic ×-statements whose completeness would contradict DPRM.

The cost, stated honestly: outside the guard, "unknown" weakens from "not
entailed by K" (the framework's signature exactness — the language knows
the limits of its knowledge) to "not derivable by these rules". The corpus
already rejected an extension on exactly these grounds
(`the_set_containing`, in the 2026-06-21 prompt's Limitations). Guarded
convexity is the disciplined version of that judgment call: the exactness
claim is *retained verbatim inside the guard* and *explicitly disclaimed
outside it*, and the guard line is visible in the syntax — the framework
still knows the limits of its knowledge, one level up.

Two conservativity obligations make this rigorous (both look provable,
neither yet proved):

- (a) Adding sound ×-rules must not break completeness for guarded
  statements — reductions of guarded terms never need ×-terms, so the
  rewrite relation restricted to the guard is unchanged. Plausible by
  construction if ×-rules only produce ×-terms from ×-terms.
- (b) K may contain unguarded facts; for guarded H, completeness then
  means: if every model of *all* of K satisfies H, H reduces. This is
  subtler (unguarded knowledge can entail guarded conclusions — e.g.
  x·y = 1 entails x = 1 over ℕ) and the honest contract is likely:
  completeness relative to the guarded fragment of K, with unguarded
  facts contributing only soundly. The gap between the two is exactly
  what the guard line disclaims.

With §1, the pressure on × largely evaporates: the OR was the need, the
OR is free, and × survives as an optional sound-only citizen for
multiplicative size reasoning.

## 3. Scope: this is V_ω, and convexity can never see arbitrary sets

Confirmed against the corpus: `SetNum.from_int` recurses into components,
and 0 = {}, 1 = {0}, 2 = {1}, 3 = {0,1} — this is the **Ackermann
bijection** between ℕ and V_ω, the hereditarily finite sets, with
membership = the BIT predicate (m ∈ n iff bit m of n). Three consequences:

- **The construction is not of arbitrary sets, and correctly so.** Its
  universe is exactly V_ω: well-founded, and canonically well-ordered by
  the numeric codes themselves. The instinct "at the very least it should
  be well ordered" is satisfied by construction, not by axiom.
- **Hereditary membership is at the ceiling.** ∈ across levels is BIT,
  and (ℕ, BIT) interprets full arithmetic — undecidable. The algebra's
  discipline of touching only *top-level* membership (elements as bit
  positions, via &, ^, shifts) is not a limitation to apologize for; it
  is what keeps the fragment below the ceiling. `{x} = 2^x` (the corpus's
  first extension, which broke convexity) is the exponential map between
  levels — the corpus discovered the cliff empirically.
- **No axiomatization without well-ordering is ever needed**, by a small
  observation worth recording:

  > **Convex semantics is well-orderable.** A semantically convex language
  > has countably many normal forms (finite strings), and the alpha-map
  > factors through them injectively on semantic classes; so the
  > represented universe is countable and inherits a canonical well-order
  > (lexicographic on normal forms). *Proof: immediate from the
  > definitions.*

  So non-well-orderable sets (the AC-sensitive zoo) are not merely out of
  scope for *this* construction — they are out of scope for *any*
  semantically convex framework. Choice-related pathology can never
  interfere; scope anxiety about "arbitrary sets" dissolves into a
  theorem.

The right ladder for the infinite game is therefore not upward in rank
(sets of sets — third-order, where decidability collapses) but sideways to
**infinite sets of naturals**: P(ℕ) at one level, which is exactly the
WS1S → S1S step (Büchi: MSO over ω is decidable). Caveat flagged now,
before it bites: minimal *Büchi* automata are not unique, so the ω-side
canonical form needs care (candidate canonical objects exist — syntactic
congruences, canonical FDFAs — but this is a real design decision, not a
free lunch as in the finite-word case).

## Consequences for the priority stack

1. **Symbolic addition via canonical automata** — unchanged first prize;
   nothing above touches it, and §1's statement layer sits cleanly on top
   of whatever the expression layer can decide.
2. **Statement layer {∪, ⊗} as a distributive lattice** with CNF/DNF
   canonical forms and atom-entailment from the expression layer — the
   corrected home of disjunctive Clue facts (refutations), replacing the
   search for closed-form ×. Discharge the §1 proof obligation.
3. **Guarded convexity** — write the two conservativity lemmas; then ×
   can be readmitted sound-only without fear.
4. Sizes: nonemptiness = size ≥ 1 keeps refutations on the additive side;
   the counting story stays Presburger-shaped (0001 §4).
