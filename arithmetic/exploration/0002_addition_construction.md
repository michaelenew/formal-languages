# 0002 — Addition with semantic convexity, via stabilizing series

Everything here is built from the base algebra plus one new syntax-level
construct, and each construction carries a termination bound readable off
the term. All propositions are proved below and machine-checked in
`output/bitset_arithmetic.py`.

## Setting

A number is a finite set of naturals: n(S) = Σ_{i∈S} 2^i, with 0 = ∅.
Base operators on sets (= bitwise on numbers):

- `x ^ y` — symmetric difference (XOR)
- `x & y` — intersection (AND)
- `a(x) = 2x` — shift left filling 0: {i} ↦ {i+1}
- `b(x) = 2x+1` — shift left filling 1: S ↦ {0} ∪ {i+1 : i ∈ S}
- finite constants (note: the number universe has no top element, so there
  is no complement here — the algebra is negation-free, and 0001's ceiling
  results are unaffected)

**Lemma 1.** bᵏ(x) = 2ᵏx + (2ᵏ − 1); as a set, i ∈ bᵏ(x) iff i < k or
i−k ∈ x. *Proof: induction on k.*

## The stabilizing series construct

The one addition to the syntax: given a sequence of terms whose partial
combinations form a monotone chain in the lattice of subsets of a finite
set, the limit is a term of the language, because the chain stabilizes and
**both stopping rules are syntactic**:

- (i) an a-priori bound: max element (or popcount) of the inputs;
- (ii) first plateau — *when proved sound for the series at hand* (it is
  not sound for arbitrary monotone chains; Lemma 2b proves it for the
  series used here, and Kleene iteration gives it for free in Prop 6).

This is the convexity-preserving mechanism. Both uses below are instances.

## Trailing-ones mask

Define T(x) = x & b(x) & b(b(x)) & ⋯ (the series from the synopsis).

**Proposition 2.** i ∈ T(x) iff {0, …, i} ⊆ x. Hence T(x) is the maximal
trailing-ones segment: T(x) = 2ᵗ − 1 where t = max { t : {0,…,t−1} ⊆ x }.

*Proof.* By Lemma 1, i survives every intersect iff for all k: i < k or
i−k ∈ x. The conditions with k ≤ i say exactly {0,…,i} ⊆ x; those with
k > i are vacuous. ∎

**Lemma 2b (first plateau is the limit).** Let I_k = x & b(x) & ⋯ & bᵏ(x).
Then i ∈ I_k iff {max(0, i−k), …, i} ⊆ x, i.e. iff x contains a run of
length min(i, k)+1 ending at i. Split x into maximal runs. The run touching
0 contributes exactly T(x) to every I_k. A maximal run of length L *not*
touching 0 contributes exactly max(L − k, 0) survivors to I_k — strictly
one fewer per step until extinct. So |I_k| − |T(x)| = Σ_runs max(L_r − k, 0)
is strictly decreasing until it reaches 0, and therefore
I_{k+1} = I_k ⟺ I_k = T(x). First plateau is the limit. ∎

**Lemma 2c (a-priori bound).** All non-trailing survivors are extinct once
k exceeds the longest run, so I_k = T(x) for every k ≥ max(x) + 1. ∎

## Successor, and why the series is necessary

**Proposition 3.** succ(x) := x ^ b(T(x)) = x + 1.

*Proof.* If 0 ∉ x: T = ∅, b(∅) = {0}, and x ^ {0} adjoins the 0 bit. If x
has trailing ones {0,…,t−1} with t ∉ x: b(T) = {0,…,t}, and the XOR clears
the trailing ones and sets bit t — binary increment. ∎

Iterating gives the constant-offset family n+1, n+2, … (the synopsis's
family). The series is not a convenience but a necessity:

**Proposition 4 (locality barrier).** No finite composition of
{^, &, a, b, finite constants} computes succ.

*Proof.* Induction on term structure: for a finite term t of shift-depth d,
bit i of t(x) depends only on bits of x at positions in
{i−s : 0 ≤ s ≤ d} (constants: no dependence; ^, & are bitwise: union the
offset sets; a, b shift offsets by one; there are no right shifts). But bit
k of x+1 depends on bit 0 for every k: witness x = 2ᵏ−1 vs x = 2ᵏ−2, which
differ only in bit 0 yet differ in bit k of the successor. Take k > d. ∎

So the stabilizing series strictly extends the algebra's expressive power
while preserving convexity — carry propagation is exactly the unbounded-
influence phenomenon that finite terms cannot reach.

## Addition

**Proposition 5.** Define the step (x, y) ↦ (x ^ y, a(x & y)), iterated
until the second component is 0; the result is the first component, and it
equals x + y.

*Correctness:* x + y = (x ^ y) + 2(x & y) — per bit, sum-without-carry plus
carry shifted — so the invariant "sum of the pair" is preserved and the
final pair is (x+y, 0).

*Termination (the measure is the point):* popcount(x^y) + popcount(a(x&y))
= |x| + |y| − |x&y| < |x| + |y| whenever the carry x & y is nonempty. The
popcount sum strictly decreases, so the recursion terminates in at most
popcount(x) + popcount(y) steps — a bound read directly off the inputs. ∎

**Proposition 6 (carry-lookahead form, same mechanism as T).** With
g = x & y, p = x ^ y, the carry set is the least fixpoint of the monotone
F(C) = a(g ∨ (p & C)) (where u ∨ v := u ^ v ^ (u & v) stays in the
algebra), and x + y = p ^ lfp(F). The Kleene chain ∅ ⊆ F(∅) ⊆ F²(∅) ⊆ ⋯ is
increasing, stabilizes within max-bit-length + 1 steps, and its first
repeat *is* the least fixpoint (standard Kleene — plateau soundness is free
here). ∎

T(x) and lfp(F) are the same shape — a monotone stabilizing series with a
syntactic bound — in the decreasing and increasing directions respectively.
Tentative general principle, the candidate "single rigorous sentence" of
this workstream:

> **Semantic convexity is preserved under monotone stabilizing series with
> syntactic bounds.** *(Proved here only instance-by-instance; stating and
> proving it once, as a closure property of convex languages, is the next
> theory task. Note the finite-subset lattice is doing real work — over
> infinite subsets of ℕ chains need not stabilize, which is exactly where
> ω-automata will have to take over for the infinite game.)*

## The deduction test, extended to arithmetic

Equality is XOR: x = y iff x ^ y reduces to 0 — the H ^ HK shape survives
intact. The hypothesis "u + v = w" is the term add(u, v) ^ w, which reduces
to 0 iff the hypothesis is true, and the judgment stays one-sided
(true / did-not-reduce). For *ground* terms this is a complete convex
decision procedure for +-equations.

## What this does not yet give

Symbolic convexity: reducing add(x, y) ^ z with **free variables** to a
canonical object. The carry recursion does not terminate symbolically
(Prop 4's unbounded influence again, now with no concrete popcount to
bound it). Per 0001 §3, the candidate canonical form is the minimal DFA of
the corresponding automatic relation — addition is a 2-state synchronous
automaton — with Myhill–Nerode canonicity playing the role ANF uniqueness
plays propositionally. That is the next construction target.
