# 0025 — ANF × automaton: not an uncertainty pair — a one-way street

0024 posed the ANF × automaton analogue of the Donoho–Stark
inequality as the next target. Answer: **no such inequality exists,
provably, and the relationship that replaces it is asymmetric** — a
one-way simulation law with an exact combinatorial mechanism. Machine
checks: `output/anf_automaton_tradeoff.py`. (Automaton size throughout
= quasi-reduced OBDD in a stated order = number of distinct Brzozowski
derivatives by prefix length, the leveled form of 0018's
identification.)

## 1. Why no uncertainty inequality can exist

The Donoho–Stark mechanism requires the two bases to be *mutually
unbiased*: every basis vector of one maximally spread in the other
(minterms have flat Walsh spectra — that is what made 0024's theorem
work). This pair lacks exactly that: **an ANF basis vector — a single
monomial — has an O(n) automaton.** Measured: x₁⋯x₁₂ has A = 1,
B = 25, product 25 against 2¹² = 4096; parity has A·B = 300. Tiny in
both bases is possible, so every product-type bound is dead on
arrival. This is a structural diagnosis, not a failed search.

## 2. The joint behaviour is completely unconstrained: four cells

| statement | (A, B) cell | measured |
|---|---|---|
| parity | (small, small) | A = 12, B = 25 |
| windowed parity, separated order | (small, BIG) | A = 5, B = 128 |
| at least one | (BIG, small) | A = 4095, B = 25 |
| at-least-one(k) ⊕ windowed(m) | (BIG, BIG) | A: 65 → 258, B: 35 → 63 as (k, m) grows |

The (BIG, BIG) witness is a direct sum on disjoint variables: A
doubles with each OR variable, B doubles with each pair — measured at
two sizes, exponential in both coordinates by construction. Every
cell inhabited; there is no law of the product.

## 3. The crossing law — the theorem that replaces uncertainty

For a statement written as a XOR of monomials, and any variable
order:

> **distinct subfunctions at cut L ≤ 2^(straddle(L) + 1)**

where straddle(L) counts the monomials with variables on both sides
of the cut. *Proof*: a subfunction is determined by which straddling
monomials' left parts the prefix has satisfied (a vector in
{0,1}^straddle) plus one bit for the parity of the monomials already
completed; monomials entirely to the right contribute identically to
every subfunction. ∎

Verified on 300 random sparse forms at every cut — and the bound is
**achieved with ratio 1.00**, i.e. tight, on random instances.
Corollary, since straddle ≤ term count A:

> **log₂(automaton size) ≤ A + log₂(n+1) + 1.**

So **ANF-concentration forces automaton-concentration**. The converse
fails by an exponential margin (at-least-one: A = 2ⁿ−1, B = 2n+1).
The street runs one way: the ring basis is *upstream* of the
automaton basis.

## 4. The crossing law explains frame sensitivity, quantitatively

The same windowed-parity statement (8 pairs, window 2) in two frames:

| frame | peak straddle | automaton |
|---|---|---|
| separated x…x y…y | 6 | 259 |
| interleaved x y x y … | 2 | 70 |

The frame changes nothing about the statement and everything about
the crossing, and the automaton tracks 2^straddle in both frames. So
the order-sensitivity observed since 0018 has its mechanism: **frame
optimisation is crossing minimisation** — a graph-layout problem,
which is why finding the best frame is hard (0024).

## 5. What this does to the geometry of the frame space

The taxonomy's pairs are not all alike. The frame space has (at
least) two kinds of relations between bases:

- **Conjugate pairs** — mutually unbiased, governed by an exact
  product uncertainty, with coherent states at the tradeoff's edge:
  minterm × Walsh (0024, tight on subspaces).
- **Ordered pairs** — one basis upstream of the other, governed by a
  one-way simulation law with a combinatorial rate (the crossing):
  ANF → automaton (here).

QM's homogeneous picture (every pair of maximal observables roughly
alike) does not carry over; this frame space is *directed* in places.
For the framework this is good news with a sharp edge: nothing sparse
in the ring is ever lost to the automaton side (up to the crossing
rate), so the K-workflow's choice of the automaton frame is safe
against ring-sparse knowledge — while the reverse choice would not
have been safe against counting-shaped knowledge (at-least-one,
thresholds: exactly Clue's diet, 0021).

## Open, sharpened again

- **Lower half of the sandwich**: subfunction count is also bounded
  below by the number of distinct straddling *combinations actually
  achieved* (the image of the left-cube in the span of right-parts).
  Characterising when the 2^straddle ceiling is met (as random
  instances do) versus collapses (structured overlaps) is the
  remaining quantitative question for this pair.
- **All-orders version**: the crossing law is per-frame; functions
  hard in *every* frame need straddle high in every order (known
  examples in the OBDD literature: hidden weighted bit). Whether a
  natural Clue-like statement is crossing-hard in every frame is
  open here.
- **The taxonomy's full relation graph**: which remaining pairs
  (dual-ANF, polarity frames, Walsh vs automaton) are conjugate,
  ordered, or neither — three checks of the same two kinds would
  complete the map.
