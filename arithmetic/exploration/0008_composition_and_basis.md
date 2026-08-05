# 0008 — Wiring composition, and a basis for the canonical layer

Prompted by the question: can every primitive be expressed as a
composition of a small set of automata, with primitivity meaning
non-derivability — a basis for the logic? Answer: yes, sharply. The
composition calculus has exactly three moves, and modulo one cited
theorem the basis of the *entire* canonical layer is the corpus's
original operator pair plus a single shift: **{^, &, a} with
constants**. The generation half is machine-checked in the suite
(`canonical_automata.run_verification_suite`, "basis derivations").

## The composition calculus: three moves, not one

An automaton is a box with named ports (channels). There is no
input/output direction — a box is a *constraint* on whatever strips are
wired to its ports. Composition is wiring, and every construction in
the engine is one of:

1. **Share** (same name = same strip): boxes wired to a common channel
   run in lockstep — the product construction, states = pairs,
   bound |A|·|B|. This is conjunction, including fan-out of one strip
   into many boxes.
2. **Hide** (solder over an internal wire): a channel is removed and
   its bits become guesses — projection + subset construction, bound
   2^|A|. This is ∃.
3. **Flip** (complement): complete the box, exchange accept/reject.
   This is what turns the calculus into a judgment (entailment =
   share with a flipped box, then check emptiness).

The "output of one feeds the input of the next" picture is the special
case share-then-hide on an intermediate channel. The successor
x ^ b(T(x)) as a wiring diagram:

        x ────┬──────────────────────────┐
              │                          │
          ┌───▼───┐  m   ┌───────┐  u  ┌─▼──────┐
          │ T-box ├──────► b-box ├─────►  ⊕-box ├──── z
          └───────┘ (hid)└───────┘ (hid)└────────┘

    share: x fans out to T-box and ⊕-box; m joins T-box to b-box;
           u joins b-box to ⊕-box
    hide:  m and u are internal — projected away
    (the engine does exactly this; the pipeline never exceeds
     4 live channels because hiding is eager)

Two refinements of the pipeline picture that matter:

- **Constraint, not dataflow.** Pipelines are the function-shaped
  special case. The K workflow's partition constraint
  (A ^ B ^ E = FULL) has no direction at all, and entailment wires K to
  a flipped hypothesis — neither is "output feeds input". Dataflow is
  what wiring looks like when every box happens to be a function graph
  and every hidden wire has a unique solution.
- **Coalescing is minimization, not running.** Equivalent automata
  land on the identical form because states with indistinguishable
  futures are merged (Myhill–Nerode), not because the machine was run
  forward. Running far enough is how *ground* strips get judged;
  merging futures is how *symbolic* objects get canonicalized.

## Term-level independence vs wiring-level derivability

The basis question splits on which composition is allowed, and the two
answers are both already in this workstream:

- **Term composition** (function-style nesting only, no hiding):
  + and T are genuinely independent of {^, &, a, b} — that is exactly
  the locality barrier (0002 Prop 4): finite terms have bounded
  influence windows; carry propagation doesn't.
- **Wiring composition** (share + hide + flip): the hierarchy
  collapses. Machine-checked in the suite:
  - b(x) = a(x) ^ 1 — universal (no wiring even needed).
  - **T is derivable with no hidden wire at all**: z = T(x) iff
    z & b(z) = z (z is an all-ones prefix — the bit sequence is
    monotone decreasing) and z & x = z and (b(z) ^ z) & x = 0. The
    *graph* of T is quantifier-free definable from the base graphs
    even though T as a *function* is not term-composable — relation
    definability and term composability come apart, and the locality
    barrier only governs the latter.
  - **Addition is derivable with exactly one hidden wire**:
    z = x + y iff ∃C: C = a(xy ∨ ((x^y) & C)) and z = x ^ y ^ C.
    The hidden carry wire is *forced* (bit 0 of C is 0; bit i+1 is
    determined by bit i), so the ∃ is a definite description — the
    pipeline intuition survives intact.
  - V₂(x) (lowest set bit) is derivable with one hidden all-ones mask:
    z = b(m) ^ m with m ⊆ b(m), z ⊆ x, m & x = 0.

## The basis theorem (modulo one citation)

**Claim: the wiring-closure of {^, &, a} with constants is the entire
canonical layer (all base-2 automatic relations).**

- Generation: by the machine-checked derivations, the closure contains
  + and V₂. By Büchi–Bruyère (the relations first-order definable in
  (ℕ, +, V₂) are exactly the 2-recognizable relations), everything in
  the layer is a wiring of + and V₂. *(Cited, not reproved here.)*
- Containment: every base graph is automatic and the three wiring
  moves preserve automaticity — that is the engine's own closure
  argument (0006).

So the corpus's original triple {^, &, 1} needed exactly **one new
generator** — the shift a — to become a complete basis for everything
this layer can ever say. Addition, the first prize, is not a new
primitive after all at the wiring level; it is the unique solution of a
one-wire fixpoint over the original algebra. (This is the automata-side
restatement of the stabilizing-series story: the series *is* the
unique-solution equation, and the hidden wire is its limit.)

## Independence (the other half of "basis")

- **a is independent of {^, &, constants} — proved.** Bit-position
  permutations act on numbers by permuting binary digits. The graphs
  of ^ and & are invariant under every such permutation; constants are
  invariant under all permutations fixing positions below the
  constant's width; any relation wired from invariant relations is
  invariant (permutations induce automorphisms, and all three wiring
  moves commute with automorphisms). But a's graph is not: (2^{N+1},
  2^{N+2}) is in the graph and swapping two high positions takes it to
  (2^{N+2}, 2^{N+1}), which is not. So no wiring of {^, &, constants}
  yields a. ∎
- **Mutual independence of ^ and & within the basis — open.** Expected
  route for &: {^, a, constants} generate only GF(2)-affine structure,
  and by Baur–Monk quantifier elimination for modules every definable
  relation is a boolean combination of coset conditions, which the
  AND-graph should fail; not yet made rigorous (the pp-definable
  subgroup analysis needs care). The dual direction (^ from
  {&, a, constants}) is also open. Flagged as the workstream's current
  cleanest small theory problem.

## Consequences

- The framework's operator-economy instinct is vindicated in the
  strongest form: there is nothing to add. Every future operator
  (counting, orderings, congruences, ×-by-constant) is a wiring, not a
  primitive; the only genuine primitives are the original algebra plus
  one shift.
- Primitivity of full × / exponentiation now has an exact meaning:
  they are not in the wiring-closure of anything in this layer (0006's
  non-automaticity), so adding them is adding a genuinely new
  generator — and the price (0001 §2) is known.
- The term-level vs wiring-level split gives the corpus's "semantic
  minimality" question (2025-12-17) its resolution shape: symbols like
  n0(x), !x, T(x) that are semantically determined but term-irreducible
  are all *wiring-definable* from x — the degrees of freedom collapse
  exactly when hiding is admitted into the syntax.

## Addendum: state = hidden channel (the dictionary)

The carry appears in three costumes, and they are the same information:
the stabilizing series' *limit* (term level: the whole carry set,
computed by iteration until stable), the *hidden wire* (wiring level:
the same set characterized as the unique solution of the one-line
equation), and the *automaton state* (machine level: bit i of that
strip at moment i, never materialized whole). A run's state trace IS
the hidden strip read out in time; the series iteration IS the machine
execution unrolled.

The trade goes both directions: hiding a wire manufactures state (the
subset construction — states are "what is known about the hidden strip
so far", bound 2^n), and the basis theorem dissolves any state back
into hidden wires over {^, &, a}. The engineering reading is exact:
this layer is **sequential circuit theory** — ^ and & are combinational
gates (memoryless, per-column), the shift a is the register (the unit
delay, the only element carrying information between positions), hidden
channels are internal signals. "Any finite-state machine =
combinational logic + registers + internal wires" is the basis theorem;
"a is independent of {^, &}" is *you cannot build a register out of
gates* — the locality barrier in its third costume.

Consequence for syntax: the "one-line" formula language for this layer
exists — **systems of {^, &, a}-equations with ∃-bound hidden
channels** (the carry equation is addition's one-liner). The canonical
minimal machine is that language's *solved form*: wiring expressions
are to canonical automata exactly what {^, &, 1} expressions are to
ANF. Machines and formulas are not rival notations; the machine is the
normal form of the formula.

One correction worth recording against a natural misreading: the
entailment test is not transition-table containment. K: x = 2 entails
H: x even, but neither minimal table is a sub-table of the other — they
do not even share a shape. Containment is of *languages* (the
world-sets the tables describe), decided by walking the product of K
with flipped H and finding no accepting path. Canonical forms make
description-*equality* meaningful; containment always goes through the
joint walk.
