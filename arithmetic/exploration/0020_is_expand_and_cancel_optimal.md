# 0020 — Is expand-and-cancel worst-case optimal?

The refined claim: *worst case*, no algorithm can eliminate a
superpolynomial number of expand-and-cancel steps. Not "on some
family" — for every conceivable input.

First, a retraction. 0019 (c) claimed this was refuted by the
"at least one of n" family, where a 2-state automaton beats a
2ⁿ−1-term ANF. **That argument does not touch a worst-case claim** —
it exhibits one family where another method wins, which is the same
move as a sort that is O(1) on already-sorted input. The correct
comparison is worst-case time against worst-case time, and 0019 (c)
is corrected accordingly.

Under that correct comparison the claim splits into three, with three
different statuses.

## Setting the baseline

Expand-and-cancel on a sentence over n variables produces the ANF,
which can have 2ⁿ−1 terms (the single clause x₁ ∨ … ∨ xₙ, measured in
`representation_tradeoff.py`). Computed sensibly the cost is Θ̃(2ⁿ).
So the baseline being defended is **2ⁿ**.

Translation into the sentence form is indeed cheap, as claimed —
`A | B → A ^ B ^ A&B`, `¬A → 1 ^ A`, linear — so the whole cost sits
in canonicalisation, and comparing algorithms to expand-and-cancel is
a fair fight.

## 1. Bounded clause width: the claim is FALSE, unconditionally

For 3-CNF there are worst-case algorithms beating 2ⁿ by an exponential
factor. PPSZ (Paturi–Pudlák–Saks–Zane), as improved by Hertli, decides
3-SAT in **O(1.308ⁿ)** worst case. Against the 2ⁿ baseline that is a
saving of (2/1.308)ⁿ ≈ 1.53ⁿ — superpolynomial, on worst-case inputs,
not on a favourable subclass. *(Cited, standard; not reproved here.)*

So as literally stated — no algorithm eliminates a superpolynomial
number of steps in the worst case — the claim is false, and this is
proven rather than conjectural.

## 2. Unbounded width: the claim is exactly SETH

For CNF-SAT with unbounded clause width, no algorithm is known that
beats 2ⁿ by an exponential factor, and the **Strong Exponential Time
Hypothesis** conjectures that none exists: no (2−ε)ⁿ algorithm for any
ε > 0. SETH is widely believed and unproven.

So for the general sentence framing, the claim is neither established
nor refuted — it *is* SETH, wearing this framework's notation.

## 3. "No polynomial algorithm": exactly P ≠ NP

The weakest and most robust reading — the exponential cannot be
removed altogether — is equivalent to P ≠ NP in this setting. Finite
entailment here is coNP-complete (0018), so a polynomial algorithm
would put coNP in P and collapse the hierarchy. Believed, unproven.

## 4. As a proof system, the claim is half-proven and half-refuted

There is a fourth reading, and it is the one where real theorems live.
Expand-and-cancel over GF(2) is not an ad-hoc procedure — it is
essentially the **Polynomial Calculus** proof system (Clegg–Edmonds–
Impagliazzo), whose derivation rules are exactly "add two polynomials"
and "multiply by a variable", over GF(2) with x² = x. Recognising it
by that name imports both directions of the question:

**Proven in favour.** Polynomial Calculus over GF(2) has
**unconditional** exponential size lower bounds — random 3-CNF
(Ben-Sasson–Impagliazzo), the pigeonhole principle (Razborov's degree
bound with Impagliazzo–Pudlák–Sgall's size-from-degree). So the
intuition that expand-and-cancel is exponentially expensive is *not*
conjectural for this method; it is a theorem. No conditional
assumption is needed.

**Proven against.** The same literature shows PC is not the strongest
system. The pigeonhole principle has *polynomial-size Frege proofs*
(Buss) while requiring exponential-size PC proofs — so a different
certificate system is superpolynomially more efficient on a family
where PC provably cannot be. Conversely PC over GF(2) refutes Tseitin
formulas in polynomial size (they are GF(2) linear systems, so
Gaussian elimination applies) where Resolution requires exponential
size (Urquhart), and PC over GF(2) is itself exponential on counting-
mod-3 principles that are easy over GF(3). Expand-and-cancel is
**incomparable** to its neighbours, not dominant.

**The caveat that keeps this from settling reading 2 or 3.** Proof
size is not algorithm time: a system can have short proofs that are
hard to find. So the Frege separation does not hand over a faster
*algorithm*, and the algorithmic question stays exactly where
readings 1–3 left it. Worth noting also that whether *any* optimal
proof system exists is itself a known open problem
(Krajíček–Pudlák).

## What this means for the framework

The suspicion is not a suspicion about *this framework*. It is P vs NP
(and SETH) wearing the framework's clothes. That is worth stating
plainly, because it settles the framework's standing: expand-and-cancel
is not a naive method waiting to be replaced by a clever one — it is
within a conjectured-optimal factor for unbounded width, and provably
beatable only by exponential-factor refinements (PPSZ-style) that do
not touch the exponential itself.

## The inversion worth noticing

There is exactly one place in this workstream where an *unconditional*
lower bound exists: the symbolic layer, where deciding sentences is
non-elementary (Meyer, Stockmeyer, for WS1S — 0017). There the
automaton method is provably essentially optimal.

And expand-and-cancel does not run there at all. It is a finite,
ground, propositional method; the symbolic layer has unboundedly many
positions and no finite ANF.

So the intuition "expand-and-cancel is optimal" is best supported
exactly where expand-and-cancel is not the algorithm, and remains
conjectural exactly where it is. That is not an argument against the
intuition — it is a map of where its proof would have to come from:
any unconditional proof of the claim for the propositional fragment
would settle P vs NP.

## Status summary

| reading | verdict |
|---|---|
| no superpolynomial saving, bounded width | **false** — PPSZ at 1.308ⁿ vs 2ⁿ |
| no (2−ε)ⁿ saving, unbounded width | **= SETH**, open, believed |
| no polynomial algorithm | **= P ≠ NP**, open, believed |
| expand-and-cancel is exponentially costly | **true, unconditional** — Polynomial Calculus lower bounds |
| expand-and-cancel is the *best* certificate system | **false, unconditional** — Frege beats it on the pigeonhole principle |
| symbolic layer, automaton method optimal | **true**, unconditional (non-elementary) |

So the intuition is right about the *cost* of expand-and-cancel —
provably, not conjecturally — and wrong about its *optimality*, also
provably, but only in the certificate-size sense. The algorithmic
version of optimality is P ≠ NP and SETH, which is where the question
has to be left.
