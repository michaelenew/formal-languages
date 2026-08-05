# 0009 — Guarded multiplication, measured

The next prize after addition. Full z = x·y is provably outside the
canonical layer (not automatic, 0006), so the question is what guarded
form survives with convexity intact, and at what cost. Answer: the
**width-guarded family** lives entirely inside the automata layer,
built by wiring from the existing basis with nothing new added to the
logic, fully convex, with a measured cost curve. Implementation and
suite: `output/guarded_multiplication.py`.

## Two inequivalent meanings of "guarded" — pick the right one

- **Domain restriction** (built here): mult_k denotes the relation
  {(x, y, z) : z = x·y ∧ y < 2^k}. The automaton is *complete* about
  every tuple inside the guard and *rejects* every tuple outside —
  there is no unknown region, so semantic convexity is fully preserved.
  The price: using mult_k asserts y < 2^k into K (the guard must be
  known, not hoped).
- **Sound-partial rules** (0005 §2's guarded convexity): × as
  rewrite rules sound everywhere, complete only on a marked core;
  outside, statements sit at "unknown". Needed only when no bound on
  the factors is known. Carries the two unproven conservativity
  lemmas.

In a bounded game the guard is free knowledge (hand sizes, deck size
are bounded a priori), so **bounded games get real multiplication with
full convexity and zero new machinery**. The sound-partial tier is
only forced by genuinely unbounded factors.

## Construction (pure wiring, one new named move)

Schoolbook multiplication, one row per guard bit:

    y < 2^k        :=  y & (2^k − 1) = y        (finite mask)
    row i          :=  (y_i = 1 ∧ t_i = aⁱ(x)) ∨ (y_i = 0 ∧ t_i = 0)
    mult_k         :=  guard ∧ rows ∧ z = t_0 + … + t_{k−1},
                       all t_i hidden

The ∨ is the *union move*: derivable from share + flip as
¬(¬A ∩ ¬B), now a named DFA method (`unioned_with`). No new primitive
— the basis of 0008 stands; disjunction of relations was always in the
wiring-closure because flip is.

## Measured laws

**Constant multiplication is exactly linear: z = c·x costs c + 1
canonical states**, verified for c ∈ {3, 5, 7, 11, 13, 21, 43}
(4, 6, 8, 12, 14, 22, 44 states). The upper bound is the carry
argument: the running carry in computing c·x is always < c, so carry
value + dead state suffice. Minimality (no two carries collapse) is
observed at every tested c, not separately proved.

**The wall is exponential in guard width, quadratic in guard bound:**

| guard | bound B | canonical states | ratio |
|---|---|---|---|
| mult_1 | y < 2 | 4 | — |
| mult_2 | y < 4 | 13 | 3.25 |
| mult_3 | y < 8 | 51 | 3.92 |
| mult_4 | y < 16 | 207 | 4.06 |

The ratio tends to 4 per guard bit: states ≈ Θ(4^k) = Θ(B²) for guard
y < B. Heuristic accounting (not proved): checking bit j of z needs a
window of the last k bits of x (2^k = B combinations) times a running
carry of magnitude < B — window × carry ≈ B². Exhaustively verified
complete inside the guard and rejecting outside it for k ≤ 3 (all
x < 64, all guarded y, plus boundary cases at y = 2^k).

The framing that matters: the wall is exponential *in bits* but only
**quadratic in the magnitude of the bound** — for game-sized bounds
(a deck of 21, hands of 6) guarded multiplication is a few hundred
states, entirely tractable. Non-automaticity of full × shows up
empirically as this curve refusing to level off.

## Where this leaves the unbounded case

Two live paths, in preference order:

1. **Level crossing** (the research edge, and the exponentiation
   path): on power-of-two operands, multiplication is *addition of
   exponents* — trivial one level up the corpus's {x} = 2^x map. A
   two-level system (value-level automata + exponent-level automata,
   with the level map as the only crossing) would make pow2-guarded ×
   and genuine exponentiation statements convex per level; the
   crossing itself is the BIT-strength map (0005 §3), which is exactly
   where completeness must stop. Unexplored; this is where "another
   extension may be necessary" becomes true.
2. **Sound-partial ×** (0005 §2): mechanical to add (ground products
   always reduce; symbolic laws as sound rules), but the two
   conservativity lemmas must be proved first so the guard line is
   honest.

## Status of the prize

Guarded multiplication in the domain-restriction sense is **done and
convex** for bounded factors — which covers every multiplicative need
a bounded game can pose. The unbounded case is now a sharply posed
choice between the two paths above rather than an open-ended search.
