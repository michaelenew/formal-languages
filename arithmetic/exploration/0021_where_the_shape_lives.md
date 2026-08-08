# 0021 — The shape of the claim has a home, and it is algebraic

The claim as refined: not "no exponential speedups" (conceded — PPSZ,
0020), but **"you cannot remove enough to reach polynomial time"**, and
more generally the *shape*: you cannot do materially better than the
ring's own canonicalisation.

The first half is settled as far as it can be here: restricted to this
framework it is exactly P ≠ NP, since finite entailment is
coNP-complete (0018). Nothing further is extractable from that
formulation.

The second half — the *shape* — is the interesting part, and it has a
precise home. **It is a question in algebraic complexity, not Boolean
complexity**, and that matters because the two have different open
problems, different barriers, and different amounts of partial
progress.

## Why algebraic

This framework is not merely analogous to a polynomial ring — it *is*
one: GF(2)[x₁…xₙ]/(xᵢ² − xᵢ), with expand-and-cancel as normalisation.
So "the ring's procedure is optimal" is natively a statement about
algebraic proof systems, where the relevant objects are:

- **Polynomial Calculus** — expand-and-cancel exactly (add
  polynomials, multiply by a variable). Its lower bounds are proven
  *through degree*: a degree lower bound yields a size lower bound
  (Impagliazzo–Pudlák–Sgall, size ≥ 2^Ω((d−d₀)²/n)). This is the
  working technical form of "you cannot avoid the expansion", and it
  is a real, functioning method — not a conjecture.
- **The Ideal Proof System** (Grochow–Pitassi) — the strong algebraic
  system, where a refutation is an algebraic *circuit*. The headline
  theorem: **superpolynomial IPS lower bounds imply VP ≠ VNP.**

So the shape, pushed to its natural conclusion, lands on **Valiant's
conjecture** rather than on Cook–Levin. That is a genuinely different
target: partial results exist for restricted circuit classes
(multilinear formulas — Raz; depth-3 over finite fields —
Grigoriev–Karpinski; the depth-4 programme), and the barriers are not
the same ones (relativisation, natural proofs, algebrization) that
block P vs NP.

**The caution that keeps this honest**: "the ring's canonicalisation"
must be specified. As *Polynomial Calculus* it is provably not optimal
(0020 §4: the pigeonhole principle has polynomial-size Frege proofs
and requires exponential-size PC proofs). As *IPS* it is extremely
strong — it p-simulates Extended Frege — so optimality there is a much
larger claim, and proving it would settle Valiant. The intuition is
therefore right in proportion to how strong a ring procedure it means.

## Where this framework's own problem sits

Measured (`representation_tradeoff.py` §5). Mini-Clue's **a priori**
knowledge — before any event, just the deal structure, 24 consistent
deals:

| | |
|---|---|
| consistent deals | 24 |
| ANF terms | **27,648** |
| ANF degree | **15** of 18 variables |
| canonical automaton | **17** states |

This refutes nothing — one family says nothing about a worst case,
which is the whole point of 0020's correction. It is a *locator*, and
a sharp one: Clue's constraints are hand **sizes**, i.e. threshold
functions, which are near-maximal degree in the ring. Degree is
exactly the quantity through which PC lower bounds are proved. So the
theory predicts the measurement — the ring form is at its worst on
precisely the constraints this problem is made of, and 24 deals cost
27,648 ring terms against 17 automaton states.

The honest reading: the "ring canonicalisation is near-optimal"
intuition is most defensible in general and least defensible *here*.
For this toy problem the ring form is the wrong representation by
three orders of magnitude at the very first knowledge state, for a
reason that is measurable and theoretically predicted.

## What would actually move the needle

If the shape is worth pursuing rather than shaking:

1. **Degree lower bounds are the tractable form.** They are provable
   by combinatorial arguments, they imply size bounds, and they are
   how every PC lower bound in the literature is obtained. A degree
   lower bound for Clue-shaped constraint systems would be a real
   result, self-contained, and would formalise "you cannot avoid the
   expansion" for exactly the systems this workstream cares about.
2. **The IPS route is the ambitious one** and terminates at Valiant.
   Worth knowing as the ceiling; not worth aiming at directly.
3. Anything phrased as "no algorithm whatsoever" for the Boolean
   decision problem is P ≠ NP and should be recognised as such
   immediately rather than pursued.
