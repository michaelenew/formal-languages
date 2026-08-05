# 0004 — Reconciliation with the recovered clue/ corpus

The original workstream files landed on main (`clue/`, gitlink repaired).
This file maps the notation, checks the arithmetic constructions of
0002/0003 against the corpus, records which of the corpus's open asks are
now closed, and flags where a known impossibility redirects one of them.

## Notation map

| clue/ corpus | this workstream | meaning |
|---|---|---|
| `n0`, `inc`, `2·` | `a` | shift left fill 0: x ↦ 2x |
| `n1` | `b` | shift left fill 1: x ↦ 2x+1 |
| `$`, `[&n1]` | `T` | trailing-ones mask, the series x & (2x+1) & (4x+3) & ⋯ |
| `!`, `[^n0]` | — | x ^ 2x ^ 4x ^ ⋯ (prefix-parity; bit i = parity of bits ≤ i) |
| `h` | — | right shift, h(n0(x)) = h(n1(x)) = x |
| `1` | — | universe constant (Boolean layer); see caveat in 0002 §Setting |

(The corpus sometimes says "leading 1s" for `$` — its examples print
lsb-first via `reverse()`; in msb-standard order it is the trailing-ones
mask. Same operator.)

## Independent rederivations agree

Written before the corpus was recoverable, 0002 arrived at, verbatim
modulo notation:

- **T = $**: Prop 2's series is `[&n1]` from `2026-02-02 +1 operation.md`,
  including the per-index expansion x, x & n0(x), x & n0(x) & n0(n0(x)), …
  ("A re-expression of $"). What 0002 adds: the proof that the *first
  plateau is the limit* (Lemma 2b — sound stopping with no cleverness) and
  the a-priori bound max(x)+1 (Lemma 2c).
- **succ**: `x ^ n0($x) ^ 1` (corpus) = `x ^ b(T(x))` (Prop 3), since
  b(T) = n0(T) ^ 1 and the two pieces are disjoint. Same for the derived
  offset family x+2, x+3, … — the corpus's expansion via
  `n0([&n1](x ^ b))`, b ranging over [0, a−1], is the unrolled form.

Convergent rederivation is decent evidence the constructions are the
natural ones for this algebra.

## Addition: three equivalent forms, now all verified

1. **Ripple / carry recursion** (0002 Prop 5): (x,y) ↦ (x^y, a(x&y)).
   New here: the strictly-decreasing popcount measure, giving the ≤
   popcount(x)+popcount(y) syntactic step bound.
2. **Unit-step least fixpoint** (0002 Prop 6): Kleene chain of
   F(C) = a(g ∨ (p & C)); plateau soundness free from monotonicity.
3. **Doubling limit** (`2026-06-21 AI exploration.md`, the Kogge–Stone
   form): G_{s+1} = G_s ^ (P_s & Sh_s(G_s)), P_{s+1} = P_s & Sh_s(P_s),
   sum = x ^ y ^ a(lim G). Now implemented as `add_by_doubling_limit` in
   `output/bitset_arithmetic.py` with the two disjointness invariants
   *asserted per step* (G_s & P_s = 0 and G_s & (P_s & Sh_s(G_s)) = 0 —
   these are what let ^ stand in for ∨, keeping the form inside {^, &, a}
   with no derived union), plus the ~log₂(width) step bound. All checks
   pass (0003 updated).

Also confirmed against the corpus's identity list: the disjointness rule
(a & b = 0 ⇒ add = ^) is Prop 5's terminal case; the carry-save identity
add(x^y^z, n0(x&y ^ x&z ^ y&z)) = x+y+z is the majority-form generalization
of the same per-bit bookkeeping.

## Status of the corpus's "Looking for" list (2026-02-02)

- **Closed form for x + y**: closed — three forms above, with proofs and
  machine-checked termination measures.
- **Product with a-priori-known a**: closed in the corpus
  (`x·a = Σ Sh_i(x)` over set-bits i of a, a finite chain of `+`), and
  consistent with the ceiling: multiplication by *constants* is
  Presburger-definable, so it is free expressiveness.
- **Product of two arbitrary sets**: the ground-term recursion
  (shift-and-add over bits of one argument, using h) terminates fine. But
  the search for a "flat single-limit closed form" should be re-aimed, per
  0001 §2: even the ∃-fragment of (ℕ, +, ×) is undecidable (Matiyasevich),
  so **no convex rewrite system can decide sentence-truth over full + and
  ×**, whatever closed form × is given. A flat form may still exist and be
  worth having for *ground computation* — the impossibility bites only at
  the symbolic/sentence level. The honest target is: how much
  multiplicative structure survives below the ceiling (constants ✓,
  congruences ✓ — both Presburger; full × ✗). *Superseded in part by
  0005: the logical need that motivated × (the zero-law OR) requires no
  arithmetic at all, and × can be readmitted sound-only under guarded
  convexity.*
- **Symbolic correlation of x, n0(x), n1(x), !x** (the degrees-of-freedom
  question, also `2025-12-17 Focus.md`'s "semantic minimality"): the
  2026-06-21 session established each of n0(x), n1(x), !x is semantically
  *determined* by x (1 true dof), so the problem is purely syntactic —
  determined-but-irreducible symbols are exactly a failure of clause (3)
  of convexity at the symbolic level. This is the same gap 0002 §"What
  this does not yet give" identifies for symbolic add, and the same
  candidate fix applies: compile terms to canonical minimal automata
  (Myhill–Nerode), where x, n0(x), !x are all automatic relations over a
  shared track and their relationships reduce mechanically. `!` in
  particular is transparently automatic: bit i of !x is the running parity
  of x's bits up to i — a 2-state transducer. The dof question and the
  symbolic-addition question are one question; solving symbolic convexity
  once should close both.

## Corrections this pass made to the arithmetic/ files

- 0001's framework section was a reconstruction written blind; replaced
  with the corpus's actual formulation (object-level sets asserted empty;
  K := K U A; test KH ^ H; convexity = alpha-map + convergent rewrite).
  The retracted "exclusion set of worlds" reading also silently weakened
  §5 — corrected: intersection gives only the *if* direction of the OR
  law; the iff needs the product, which is where the ceiling sits.
- 0002 Prop 4 (locality barrier) extended to cover the corpus's h
  primitive: bounded windows instead of one-sided offsets; barrier stands.

## One caution for the corpus, kept from earlier notes

`2025-06-28 Refocusing.md` records "a + b := a xor b xor inc(a and b)" as
a closed form. That is one carry-save step, not addition: it is correct
iff (a^b) & 2(a&b) = 0, i.e. iff no second-order carry occurs.
Counterexample a = 3, b = 1: the formula gives 2 ^ inc(1) = 0, but
3 + 1 = 4. The later corpus files already treat carries properly (the
recursion/limit is exactly what repairs this); noting it here so the stale
identity doesn't get cited.
