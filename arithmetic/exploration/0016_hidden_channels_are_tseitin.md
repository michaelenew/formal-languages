# 0016 — Hidden channels are Tseitin variables: the price of not naming the carry

Two results, both machine-checked in `output/succinctness.py`.

## 1. Hidden channels were always available — with one asymmetry

The corpus's original framing already admits hidden channels, with no
new operator: **invent a symbol, constrain it in terms of the others**.
On the knowledge side that *is* existential quantification, for an
exact reason. For a hypothesis H not mentioning the invented symbol C,

    ∀C ( K(C) → H )   ≡   ( ∃C K(C) ) → H

so leaving C free in K and quantifying it are the same statement.
Verified: the nonemptiness witness with its channel left free and with
it projected give identical verdicts.

**But the interchange fails on the hypothesis side.** There the
implication runs the other way:

    K → ∃C H(C)   is NOT   ∀C ( K → H(C) )

A free C in H demands that *every* candidate be a witness. Verified:
with the witness in the hypothesis, the projected form is entailed and
the free form is not — sound but incomplete. So:

> **Nonemptiness facts can be *learned* for free. Nonemptiness
> *questions* need a real quantifier.**

That is the whole cost of staying inside the original framing: K may
carry invented symbols freely, and hypotheses must either avoid them
or the language must gain an explicit ∃.

## 2. Not naming the carry cost exactly an exponential

Measured in the corpus's own canonical form (XOR of ANDs, the unique
multilinear normal form), with no hidden symbols permitted:

| statement | terms, no hidden symbols | with hidden symbols |
|---|---|---|
| "at least one of n cards" | **2ⁿ − 1** (exact) | 3 constraints, 1 channel |
| "at least two of n cards" | **2ⁿ⁻¹ − 1** (exact) | O(1) constraints, 1 channel |
| carry into bit i | **2ⁱ − 1** (exact) | 1 channel per bit, local |

All three exact formulas, verified n ≤ 12 / i ≤ 7. So the intuition
that "in that framing, worst-case sentence length is exponential" is
**correct and exact** — and it is *repaired*, not merely mitigated, by
inventing symbols. This is the classical **Tseitin transformation**:
auxiliary variables convert an exponential normal form into a linear
conjunction of local constraints. Without them the normal form must
name every interaction explicitly; with them each interaction gets a
name and a local law.

The two cases where the saving is exponential are precisely the two
places the corpus got stuck: **refutation events** (nonemptiness) and
**addition** (the carry). Naming the carry was not a convenience — it
was the difference between 2ⁱ terms and i constraints.

## 3. Consequently the 0015 construction is polynomial

0015's open question conflated definition size with evaluation cost.
Counting the flip-elimination construction for a target automaton with
s states over k channels: s + 2 hidden channels, O(s²) partition
atoms, O(s·2ᵏ·k) transition atoms — at fixed arity, **O(s²) atoms and
O(s) hidden channels, polynomial**.

What is exponential is *evaluating* it: each hidden channel is
projected away by a subset construction, and determinising a guessed
run is exponential in general. The distinction is worth holding onto:

> Writing the knowledge down stays small. Deciding with it is what can
> cost — and that cost is canonicalisation, not expression.

This also re-reads the whole workstream's cost profile. The K-workflow
(0007, 0010) keeps K canonical at every step, paying the
determinisation cost eagerly and getting O(states × deck) surveys in
return. A framing that kept K as a *positive formula with hidden
channels* would stay small but defer every question. That trade —
canonical-and-expensive versus positive-and-deferred — is the real
design axis, and both ends are now available.

## Open

- Is the exponential evaluation cost intrinsic, or does the *specific*
  shape of these run-encoding definitions admit cheaper
  determinisation? (Generic NFA→DFA is exponential, but these are
  highly structured: the hidden tracks are a one-hot partition.)
- Minimality of the positive signature {&, ^, <<, 0, 1} (from 0015).
