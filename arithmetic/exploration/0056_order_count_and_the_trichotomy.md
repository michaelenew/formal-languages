# 0056 — The trichotomy verified, and complementarity binds the co-living

The two directions green-lit from 0055's discussion: verify the
liar/truth-teller/grounded trichotomy exhaustively, and make the
order/count complementarity quantitative. Both done; the second
*corrected the conjecture* in an instructive direction — the naive
product law fails, and the failure isolates what an uncertainty
principle in this frame actually binds. Code:
`output/order_count_complementarity.py`.

---

## Part A — the reference trichotomy, exhaustively

Solution counts of channel definitions against their reference
structure (width 7, per input, exhaustive over all candidate values;
`h`-definitions checked on interior positions — the excluded top
constraint *is* the missing boundary at infinity):

```
grounded:      n = x ^ a(n)                  [1]        always
grounded:      n = ~a(n) & x                 [1]        negation, guarded
truth-teller:  n = x | h(n)                  [2]        least = down-closure,
                                                        greatest = all-ones
truth-teller:  n = n                         [128]      every value
liar:          n = n ^ Ω                     [0]
liar:          n = ~n & Ω                    [0]
```

Three structural facts, verified:

1. **Negation under a guard is harmless** — the liar needs *both*
   ungroundedness and negation.
2. **The truth-teller's two solutions are the 0/Ω guard choice**: the
   free top bit is the boundary at infinity, its two values yield the
   least (down-closure) and greatest (all-ones) fixed points — 0047's
   case split, appearing as the solution set of a definition.
3. **The cycle-parity law**: two channels with depth-0
   cross-references have solutions by the *parity of negations around
   the loop* — `2^w / 2^w / 0` for zero, two, one negation
   (exhaustive). The paradox is a parity of `Ω`-flips around a
   reference cycle: checkable by scan, exactly the shape Abramsky
   et al. give quantum-contextual liar cycles.

**Census** (400 random one-channel bodies over `{x, 1, Ω, n, a(n),
h(n)}` with `^, &`): 351 grounded instances — solution count **always
exactly 1**, no exceptions. 849 ungrounded instances scatter: 12%
liars (0 solutions), 11% accidentally unique, 77% many. Uncertainty
about a channel's value enters exactly where groundedness leaves, and
only there.

## Part B — order/count complementarity, and what it actually binds

Setup: exact minimal Mealy automata by residual (signature) BFS,
horizons checked stable; joint costs are reachable pairs of minimized
components, which is exact (distinct pairs are behaviorally distinct).

Two order observables, one count observable:

```
transient   O_p = x·y mod 2^p          dies above bit p
persistent  P_p = (x mod 2^p)·y        multiplication by a learned
                                       constant; the carry never dies
count       C_m = popcount(x) mod m    persistent by nature
```

Individual prices: `O_p`: 2, 5, 12. `P_p`: 3, 12, 50. `C_m`: exactly m.

| pair | joint | additive (s+m−1) | product (s·m) |
|---|---|---|---|
| O₁+C₂ … O₂+C₄ | 3,4,5,6,7,8 | **exact match** | far below |
| O₃+C_m | 16,17,18 | 13,14,15 (near) | 24–48 |
| P₁+C_m | 5,7,9 | 4,5,6 | 6,9,12 |
| P₂+C_m | 19,26,33 | 13,14,15 | 24,36,48 |
| P₃+C_m | 79,108,137 | 51,52,53 | 100,150,200 |

**The conjectured product law fails for the transient pair — and the
failure is the finding.** `x·y mod 2^p` dies above bit p; the count
lives forever; observables that occupy *different epochs of the run
share their state across time*, and the joint cost collapses to
additive. A dying observable evades the uncertainty trade entirely.

**For co-living observables the trade is real.** The persistent
multiplier paired with the counter climbs to ~70% of the full product
(79/100, 108/150, 137/200) — most state pairs must be independently
maintained. So the corrected statement:

> **Complementarity binds simultaneous observation.** The budget
> inequality `log₂ states(order) + log₂ m ≲ log₂ S` holds between
> observables that stay alive together, with measured slack (~30%
> unreachable pairs at these sizes); it says nothing about observables
> separated in time. The unbounded limit is unchanged: both exact,
> with read-back, is the Minsky wall.

This is a more Heisenberg-like shape than the original conjecture, not
less: in QM too, the uncertainty relation constrains *simultaneous*
measurement, and sequential measurement of non-coexisting quantities
evades it. The frame reproduced that distinction from pure state
counting, without being told.

## Honest limits

- All exact counts are at small parameters (p ≤ 3, m ≤ 4, width ≤ 7
  exhaustive for Part A); horizons for the signature BFS are checked
  stable at H vs H+1 on the small cases, not proved sufficient in
  general.
- "~70% of product" is three data points; whether the reachable-pair
  deficit vanishes, converges, or oscillates as p and m grow is open.
- The census classifies groundedness syntactically but consistency
  only empirically; the cycle-parity law is verified for pure
  copy/negate cycles, not for arbitrary bodies around a cycle.
- Part A's "grounded ⟹ exactly 1" has the contraction proof behind it
  (0054); the census is the audit, not the argument.

## Open

1. **The deficit's fate.** Does the persistent pair's reachable-pair
   ratio tend to 1 (asymptotically perfect complementarity), to a
   constant < 1 (a fixed discount — the frame's analogue of a
   commutator norm), or does it depend on arithmetic relations between
   p and m (resonances)?
2. **A commutator object.** The transient/persistent split says the
   binding quantity is *co-living state*. A candidate formalization:
   for observables A, B, define the deficit
   δ(A,B) = 1 − reachable-pairs / product. δ = 0 for time-separated
   pairs; δ measures shared structure for co-living ones. Whether δ
   behaves like a commutator (bilinear-ish, vanishing iff "compatible")
   is checkable with the machinery already built.
3. **The trichotomy at the statement level.** Part A classifies
   *definitions*; a statement mixes several channels. The minimal
   number of ungrounded channels a statement needs (0054 §10.3's
   "N-ness measure") is now measurable with the census tooling.
4. **The liar as a resource.** Odd cycles have no solutions — but a
   sentence containing a liar disjunct is *never* empty, i.e.,
   provably false by scan. Whether liar-detection subsumes part of the
   annihilate/settle rule family (falsity by parity, no evaluation) is
   a cheap experiment.
