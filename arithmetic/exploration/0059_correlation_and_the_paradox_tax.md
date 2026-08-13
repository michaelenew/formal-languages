# 0059 — Correlation buys back all but one bit, and the last bit is phase

0058 left the door open: forced entropy was computed over product
distributions, and correlated distributions were flagged as "exactly
where a quantum state would differ from a classical mixture." This
exploration answers the question, informed by the information-theory
corpus in `stat-tracker` (the probability/trust separation; influence
∝ √information). The answer is exact and has more structure than a
yes or no. Code: `output/correlation_and_entropy.py`.

**The ledger:**

```
product distributions       k bits    (0058)
correlated (classical)      1 bit     (this file — the floor)
amplitudes (quantum)        0 bits    (this file — the buy-back completes)
```

---

## 1. The stationary polytope and the 1-bit floor

The joint generalization of 0058's "distributional solution" (fixed
point of the induced map on Bernoulli parameters) is a joint
distribution fixed under pushforward by the revision map T. This is
revision-theory semantics (Gupta–Belnap) with probability on top, and
it reduces to 0058's notion on product distributions — verified: the
liar's product fixed point is the fair coin, the triangle's is
all-1/2.

For negation systems T permutes the atoms, so (one line, verified)
**stationary distributions are exactly the mixtures of
orbit-uniforms**, and with disjoint supports the entropy is exact:

```
H  =  H(mixture weights) + Σ w_o · log₂|orbit o|
min H over stationary  =  log₂(smallest orbit of T)
```

For the odd k-cycle: no atom is fixed (that *is* the paradox), but
the two constants {00…0, 11…1} always form a 2-orbit. So

> **forced entropy (correlated) = 1 bit, for every odd k** — against
> k bits for the product solution. Correlation buys back k−1 of the
> k bits. Verified k = 3, 5, 7 by orbit census; even cycles have
> fixed atoms and floor 0, matching the cycle-parity law.

Two structural facts sharpen this:

- **0058's product solution is the maximum-entropy stationary point**
  (the uniform, k bits). The product computation found the top of the
  polytope and mistook it for the price.
- **The residual bit is phase, not value.** The floor distribution
  puts all mass on the two constants — atoms that violate *every*
  edge. T fixes no atom, so the world must oscillate with period 2;
  the unbuyable coin is the phase of that clock, not uncertainty
  about which constraint holds.

## 2. One coin, many liars — and the graded tax

The floor is log₂(shortest revision period), and that makes the tax
**per-world, not per-paradox**:

- **m independent liars cost 1 bit total** (all orbits of the global
  complement have size 2). Each marginal is still a forced fair coin
  — verified — but one shared coin drives them all; mutual
  information carries the other m−1 bits. A liar plus the Specker
  triangle: still 1 bit.
- **The expensive paradox exists, and the carry channel is its
  agent.** The self-increment paradox `n := n + 1` (carry-coupled) is
  one revision cycle through all 2^w states: unique stationary
  distribution = uniform, **tax = w bits = the whole state**,
  verified w = 2..5. The w → ∞ limit is the 2-adic odometer, uniquely
  ergodic with Haar measure — every bit an independent fair coin,
  correlation buys nothing at all. Strip the carry (`n := n ^ 1`) and
  the tax collapses to 1 bit. The channel that walls off
  multiplication (0053/0054) is also what makes a paradox expensive:
  it couples the bits into one long clock.

So paradoxes are graded by their revision period: the liar is the
cheapest possible (period 2), the odometer the most expensive
(period = state count), and the grading is the same "how far does
information travel" quantity as everywhere else in this corpus.

## 3. Truth vs certainty: the product point is Pareto-dominated

Along the triangle's stationary polytope (weight w on the 2-orbit),
expected satisfied-context fraction is (1−w)·2/3 and entropy is
H(w) + w + (1−w)·log₂6. First draft conjectured both monotone; the
audit corrected it, and the correction is the finding:

```
w        E[satisfied]   entropy
0.00     0.667          2.585      6-orbit uniform
0.25     0.500          3.000   <- 0058's product solution (the PEAK)
1.00     0.000          1.000      the floor
```

Satisfaction is monotone in w; **entropy peaks at exactly the
uniform**. So the product solution is Pareto-dominated: shifting all
weight to the 6-orbit gains truth (1/2 → 2/3) *and* sheds entropy
(3 → 2.585 bits). **Correlation is not a trade against the product
baseline — it is a strict improvement in both coordinates.** The real
frontier runs from (truth 2/3, 2.585 bits) to (truth 0, 1 bit):
past the dominated region certainty is bought with truth, and truth
is capped at 2/3 — one minus the contextual fraction of 0058 §1 — at
any price.

## 4. The contextwise reading: nothing global to buy

Keep pointwise truth per context (each edge supported on its
anticorrelated pairs) and demand only marginal consistency: the
consistency chain forces every parameter to 1/2 — **the empirical
model is unique** (perfect anticorrelation per edge, every marginal a
fair coin, 1 bit per context) — and **no global joint reproduces it**
(every atom violates some edge; verified). This is the
Abramsky–Brandenburger strong-contextuality reading: here correlation
cannot buy entropy because there is no global object to spend it on.
The model sits at the no-signaling extreme; the literature reports
the triangle's anticorrelated model as beyond quantum realization
(Liang–Spekkens–Wiseman) — cited, not verified here.

## 5. The amplitude buy-back

Quantize the revision map: T becomes a permutation unitary U, a
solution is a U-invariant state. No basis state is invariant (the
paradox, again), but every finite permutation has an orthonormal
eigenbasis, so **pure invariant states always exist**: the cat state
(|00…0⟩ + |11…1⟩)/√2 for the triangle and the liars, the eight
character states for the w=3 odometer — all verified invariant, all
**entropy zero**, and all with computational-basis statistics exactly
equal to the classical floor distribution.

The classical residue log₂(min period) is *phase* entropy (§1), and
amplitudes are precisely the objects that internalize phase. The
buy-back completes at the square root of probability. Probabilities
cannot hold a paradox below 1 bit; square roots of probabilities hold
it at zero — and pay in measurement uncertainty: the state is
complete, the readout is not. That is 0055's "Heisenberg feel"
resolved to a mechanism: **incompleteness at the probability level =
uncertainty at the measurement level of a complete amplitude-level
state.**

## 6. The stat-tracker bridge

The `stat-tracker` corpus separated probability from trust because an
unknown distribution cannot carry both the process and the confidence
in the process, and found the conserved influence budget lives at
√information ("information is an energy, influence is an amplitude" —
sensitivities compose linearly, informations quadratically). Two
precise contact points, stated at their actual strength:

1. **The paradox re-opens the trust axis even with known
   distributions.** The constraints fix the within-orbit shape
   exactly (uniform — zero free parameters) and say *nothing* about
   the mixture weight w: the stationary polytope is a coordinate the
   definitions cannot see. Probability lives within orbits; the
   between-orbit weight is a confidence-like degree of freedom with
   zero evidence behind it — a hard-edged instance of "the
   distribution cannot carry both." This is where the user's
   forward-pointing case (distribution shape inter-correlated rather
   than a priori static — covariance a function of prior covariance)
   would land: as a dynamics *on the polytope coordinate itself*,
   which is exactly the regime where the trust calculus becomes
   load-bearing. Flagged as open, not developed.
2. **The √ is the same √.** Influence ∝ √nats is the
   amplitude/energy split; the Fisher–Rao geometry that makes it
   exact is the √p embedding of distributions; and §5's buy-back
   happens at that level. The coordinate stat-tracker was forced to
   invent (trust, composing linearly where information composes
   quadratically) is the classical shadow of the coordinate that
   dissolves the paradox tax (amplitude, holding phase where
   probability cannot). Stated as a structural correspondence, not a
   theorem.

## 7. Honest limits

- The stationarity lemma (stationary ⟺ constant on orbits) is a
  one-line proof for permutations; orbit censuses are exhaustive at
  the stated widths. Entropy formulas are exact (disjoint supports).
- "Tax = log₂(shortest revision period)" is proved for permutation
  revision maps. Non-invertible revision maps (bodies with `&`
  absorbing information) have attractors rather than orbit
  decompositions; the floor statement there is unexamined.
- The unique-ergodicity/Haar claim for the infinite odometer is
  standard ergodic theory, cited not re-proved; finite widths are
  verified.
- §5's quantization (permutation unitary, invariant state) is *a*
  natural quantization, not the unique one; the invariant pure states
  inherit reading (B)'s abandonment of pointwise truth (the cat state
  measures onto constraint-violating atoms).
- The Liang–Spekkens–Wiseman non-realizability of the triangle model
  is literature, unverified here.

## 8. Open

1. **Non-invertible revision maps.** Bodies with `&` make T lossy;
   stationary distributions concentrate on the eventual image. Does
   the tax formula become log₂(shortest cycle *in the core*), and can
   absorption make a paradox cheaper than its cycle structure
   suggests?
2. **The polytope as a dynamical arena.** The user's inter-correlated
   distribution shape: put a law on w (e.g. wₜ₊₁ a function of the
   current mixture's covariance) and ask which meta-laws have unique
   stationary meta-distributions — the trust calculus (σ(Λ),
   influence ∝ √nats, row-min robustness) is the natural instrument
   set there.
3. **Amplitude semantics for the frame.** §5 quantized one definition
   at a time. A compositional amplitude semantics (channels as
   unitaries, conjunction as tensor-then-project) would say whether
   the frame's *statements* — not just its paradoxes — admit
   zero-entropy consistent states, and where projection (the
   non-unitary step) reintroduces the tax.
4. **The odometer as the maximal paradox.** Tax = whole state is an
   extreme point; is there a matching theorem that `n := n + 1` is
   the *unique* (up to conjugacy) single-channel paradox with full
   period, tying it to the carry cocycle's non-degeneracy?
