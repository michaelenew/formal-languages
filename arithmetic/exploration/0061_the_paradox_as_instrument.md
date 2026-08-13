# 0061 — The paradox as instrument: pricing the invisible coordinate

0059 §6 found the mixture weight w — how stationary mass splits across
the core's cycles — is a coordinate the definitions cannot see, and
conjectured this was the stat-tracker probability/trust separation
appearing without distribution uncertainty. This exploration makes
that exact, then transplants the stat-tracker laws (influence ∝
√nats; window ∝ 1/drift; the collapsed oracle gap) into the frame's
own channel. Everything before §4's linearization is exact rational
arithmetic; §4 is exact Gaussian linear algebra. No Monte Carlo
anywhere. Code: `output/mixture_weight_inference.py`.

---

## 1. Zero evidence from the theory: w is a pure trust coordinate

The stationarity residual of π_w = w·u₂ + (1−w)·u₆ is exactly zero
for every w (rational grid; the residual is linear in w). The theory
— definitions plus consistency — assigns identical standing to every
mixture: **zero nats about w, ever**. The solution's two components
separate exactly:

```
within orbits     pinned (uniform)  — zero free parameters
between orbits    free              — zero evidence from the theory
```

The distribution carries the process; w is a pure trust coordinate.
This is the stat-tracker separation — there forced by unknown noise
distributions, here forced by paradox with the distributions fully
known. The correspondence needed no constructed corollary of
distribution uncertainty because paradox manufactures the same split
by a different mechanism: it pins the shape and orphans the weight.

## 2. The instrument: the parity channel

Read one context (edge) of a sampled world. Exactly:

- 2-orbit component: 00, 11 each 1/2 — parity always 0
- 6-orbit component: 01, 10 each 1/3; 00, 11 each 1/6

Likelihood ratios agree within each parity class, so **the edge
parity is a sufficient statistic**, and the channel is

```
P(parity = 1)  =  p(w)  =  (1 − w) · 2/3
```

— 0059's truth/certainty curve reappearing as the *response curve of
the paradox used as a measurement device*. Forced entropy is not
forced ignorance: the compulsory coin has a w-dependent bias that
accumulates clean evidence by log-odds addition (trust = σ(Λ), e per
nat, imported convention).

## 3. The price of contextuality: η(1/2) = 1/2, closed form

Fisher information about w: context-bound reader (4/9)/(p(1−p));
orbit oracle 1/(w(1−w)). Efficiency η = ratio, exact:

| w | η | oracle advantage |
|---|---|---|
| 1/8 | 0.200 | 5.00× |
| 1/2 | **0.500 exactly** | 2.00× |
| 7/8 | 0.636 | 1.57× |

(advantage → 3/2 as w → 1; → ∞ as w → 0, where the oracle detects
the rare orbit for free). The gap is charged to **contextuality, not
estimator quality**: the three edge parities of one world are (0,0,0)
on the 2-orbit and two-ones on the 6-orbit — disjoint — so reading
all contexts of one world *simultaneously* is the oracle. The price
is for sequential context access, and it is closed form.

## 4. The drift transplant: √ laws and the fourth-root gap

Let w drift — the user's inter-correlated-shape regime — as a random
walk observed through the parity channel, linearized at the operating
point (R_eff = 1/I_ctx; the one approximation in this file, stated as
such). This is exactly the stat-tracker model, and its laws re-derive
in this channel by exact linear algebra:

- **influence of the lag-k read = K(1−K)^k** (impulse response of the
  converged filter, machine precision);
- **incremental nats of the lag-k read decay as (1−K)^2k** (exact
  Gaussian conditioning, rank-one removal: measured ratio 1.220
  against (1−K)⁻² = 1.2213, within 3% across lags including boundary
  effects);
- **influence ∝ √nats** — the energy/amplitude split, constant to 2%
  across lags: stat-tracker's result 5 holds verbatim in this
  channel;
- **memory 1/K ∝ 1/√q** (K/√q = 0.9512, 0.9950, 0.9995 at
  q = 10⁻², 10⁻⁴, 10⁻⁶): window ∝ 1/drift, their L* ∝ 1/ω law;
- **the fourth-root compression of the oracle gap.** At w = 1/2 the
  static information gap is 1/η = 2. Under drift, the Riccati fixed
  point P ≈ √(QR) turns it into a variance gap √2 (measured 1.4146
  at q = 10⁻⁶) and an SD gap 2^{1/4} ≈ 1.19. **A 2× information
  oracle is a 19% tracker.**

The last item is the frame's version of the stat-tracker result the
user flagged — the oracle's advantage cut to near zero without Monte
Carlo. The mechanism here is explicit: the tracking game compresses
any static information advantage through two square roots (Riccati,
then variance → SD), advantage^(1/4) overall, and what remains is
closed-form and charged to contextuality by §3. The two corpora
also now share the √ at three independent sites: influence/nats
(both), amplitude/probability (0059 §5's buy-back), and
Riccati/tracking (here) — in each case the linearly-composing object
lives at the square root of the additively-composing one.

## Honest limits

- §§1–3 are exact (rational arithmetic; sufficiency and disjointness
  verified structurally). The sampling model is "one fresh world per
  epoch, one context read per world" — reading the *same* world's
  edge repeatedly gives correlated reads and a different (easier)
  problem.
- §4 linearizes the Bernoulli parity channel to Gaussian at the
  operating point; the √-laws are verified for the linearized model.
  The stat-tracker corpus verified the same laws directly on its own
  exact model; what transfers here is the structure, with the
  Bernoulli-exact version unchecked (a Beta-Bernoulli filter would
  check it).
- The fourth-root law uses the small-q Riccati asymptotic; measured
  exactly at q = 10⁻⁶, 3% off at q = 10⁻².
- η compares one edge read against one orbit read; richer per-epoch
  observation menus (two edges, adaptive edge choice) sit between
  and are not priced here. By symmetry of the triangle, edge choice
  cannot matter for a single read, but adaptive multi-read menus are
  open.

## Open

1. **The Bernoulli-exact drift filter.** Replace the Gaussian
   surrogate with exact Bayes on the parity channel (finite-state
   approximation of the posterior over w) and re-measure the three
   √ laws; any deviation localizes what linearization hides.
2. **Contextuality as a channel-capacity statement.** §3 prices one
   scenario. A general statement — for any strongly contextual
   system, sequential-context Fisher / global-read Fisher ≤ some
   function of the contextual fraction — would make the "price of
   contextuality" a theorem about the frame rather than an instance.
   The Mermin–Peres square (0058) is the natural second data point.
3. **Trust dynamics on the polytope.** With the instrument priced,
   the user's covariance-of-covariance case is formulable: let w's
   drift law depend on the current mixture's own statistics and ask
   when the meta-system (world + tracker) has a unique stationary
   law — the trichotomy, one level up.
