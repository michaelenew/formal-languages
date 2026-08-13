"""The paradox as an instrument: inference on the mixture weight.

0059 s6 identified the mixture weight w -- how stationary mass splits
across the core's cycles -- as a coordinate the definitions cannot
see: a trust axis reopened inside a-priori-known distributions.  This
module makes the information theory of that coordinate exact, and
transplants the stat-tracker laws (influence ~ sqrt(nats); window ~
1/drift; the collapsed oracle gap) into this frame's own channel.

  s1  ZERO EVIDENCE FROM THE THEORY.  The stationarity residual of
      pi_w = w*u2 + (1-w)*u6 is exactly zero for every w: the
      definitions price the within-orbit shape completely and the
      between-orbit weight not at all.  Every nat about w must come
      from observing worlds, none from the theory.  Probability
      (within orbits) and trust (between orbits) separate exactly.

  s2  THE INSTRUMENT.  Read one context (edge) of a sampled world.
      The edge parity is a SUFFICIENT statistic (likelihood ratios
      match on 00/11 and on 01/10), and the channel is

          P(parity = 1)  =  (1 - w) * 2/3

      -- 0059's truth/certainty curve, reappearing as the response
      curve of the paradox used as a measurement device.  Forced
      entropy is not forced ignorance: the compulsory coin has a
      w-dependent bias that carries clean Fisher information.

  s3  THE PRICE OF CONTEXTUALITY.  An oracle reads the orbit
      directly (Fisher 1/w(1-w)); a context-bound reader gets
      (4/9)/(p(1-p)).  The efficiency

          eta(w) = (4/9) w(1-w) / (p(1-p)),   eta(1/2) = 1/2 exactly

      is closed form -- no Monte Carlo -- and the gap is charged to
      CONTEXTUALITY, not to estimator quality: reading all three
      edges of one world at once discriminates the orbits perfectly
      (parity patterns (0,0,0) vs two-ones are disjoint), so
      simultaneous context access IS the oracle.  Sequential context
      access pays a factor 1/eta = 2 at w = 1/2.

  s4  THE DRIFT TRANSPLANT.  Let w drift (the inter-correlated-shape
      regime): a random walk observed through the parity channel,
      linearized at the operating point.  This is exactly the
      stat-tracker model, and its laws re-derive in this channel by
      exact linear algebra:
        - influence of the lag-k read on the estimate = K(1-K)^k;
        - incremental nats of the lag-k read decay as (1-K)^(2k);
        - influence ~ sqrt(nats), the energy/amplitude split;
        - memory 1/K ~ 1/sqrt(q): window ~ 1/drift-rate;
        - the static oracle advantage 1/eta enters the tracking
          error SD at the FOURTH ROOT: sqrt from the Riccati fixed
          point (P ~ sqrt(QR)), sqrt again from variance -> SD.
          A 2x information gap is a 19% tracking penalty.  The
          drifting game compresses oracles; this is the frame's
          version of stat-tracker's collapsed oracle gap, with the
          residual charged to contextuality in closed form.

Run directly for the verification suite.
"""

from __future__ import annotations

from fractions import Fraction
from math import log, log2, sqrt


# ---------------------------------------------------------------------
# the triangle's stationary family, exactly
# ---------------------------------------------------------------------

ATOMS = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
EDGES = [(0, 1), (1, 2), (2, 0)]


def revision(n):
    return tuple(1 - n[(i + 1) % 3] for i in range(3))


def stationary_mixture(w: Fraction) -> dict:
    two = {(0, 0, 0), (1, 1, 1)}
    pi = {}
    for atom in ATOMS:
        if atom in two:
            pi[atom] = w / 2
        else:
            pi[atom] = (1 - w) / 6
    return pi


# ---------------------------------------------------------------------
# 1. zero evidence from the theory
# ---------------------------------------------------------------------

def verify_zero_evidence() -> None:
    for numerator in range(8):
        w = Fraction(numerator, 7)
        pi = stationary_mixture(w)
        pushed = {}
        for atom, mass in pi.items():
            pushed[revision(atom)] = pushed.get(revision(atom), 0) + mass
        assert pushed == pi, w                 # residual exactly zero
    print("  The stationarity residual of pi_w is exactly zero for")
    print("  every w (checked on a rational grid; the residual is")
    print("  linear in w, so two points would suffice).  The theory --")
    print("  the definitions plus consistency -- assigns identical")
    print("  standing to every mixture: ZERO nats about w, ever.")
    print()
    print("  So the solution's two components separate exactly:")
    print("    within orbits    pinned (uniform), zero free parameters")
    print("    between orbits   free, zero evidence from the theory")
    print("  The distribution carries the process; the weight w is a")
    print("  pure trust coordinate -- the stat-tracker separation,")
    print("  forced here by paradox rather than by unknown noise.")


# ---------------------------------------------------------------------
# 2. the instrument: the parity channel
# ---------------------------------------------------------------------

def edge_distribution(pi: dict, edge) -> dict:
    i, j = edge
    out = {}
    for atom, mass in pi.items():
        key = (atom[i], atom[j])
        out[key] = out.get(key, 0) + mass
    return {key: mass for key, mass in out.items() if mass}


def verify_the_instrument() -> None:
    u2 = edge_distribution(stationary_mixture(Fraction(1)), EDGES[0])
    u6 = edge_distribution(stationary_mixture(Fraction(0)), EDGES[0])
    assert u2 == {(0, 0): Fraction(1, 2), (1, 1): Fraction(1, 2)}
    assert u6 == {(0, 0): Fraction(1, 6), (0, 1): Fraction(1, 3),
                  (1, 0): Fraction(1, 3), (1, 1): Fraction(1, 6)}
    # parity sufficiency: likelihood ratios agree within parity class
    assert u2[(0, 0)] / u6[(0, 0)] == u2[(1, 1)] / u6[(1, 1)]
    assert u2.get((0, 1), 0) == u2.get((1, 0), 0) == 0
    print("  Edge readings of a sampled world, exactly:")
    print("    2-orbit component:  00, 11 each 1/2   (parity always 0)")
    print("    6-orbit component:  01, 10 each 1/3; 00, 11 each 1/6")
    print("  Likelihood ratios match within each parity class, so the")
    print("  PARITY of one edge is a sufficient statistic, and the")
    print("  channel is")
    print()
    print("      P(parity = 1)  =  p(w)  =  (1 - w) * 2/3")
    print()
    for numerator in (0, 2, 4, 6, 8):
        w = Fraction(numerator, 8)
        pi = stationary_mixture(w)
        parity = sum(mass for atom, mass in pi.items()
                     if atom[0] != atom[1])
        assert parity == (1 - w) * Fraction(2, 3), w
    print("  -- 0059's truth/certainty curve, reappearing as the")
    print("  response curve of the paradox used as an instrument.")
    print("  Forced entropy is not forced ignorance: the compulsory")
    print("  coin has a w-dependent bias, and reading it accumulates")
    print("  clean evidence (log-odds addition, e per nat).")


# ---------------------------------------------------------------------
# 3. the price of contextuality
# ---------------------------------------------------------------------

def verify_the_price_of_contextuality() -> None:
    # Fisher of a Bernoulli(p(w)) read: (dp/dw)^2 / (p(1-p)),
    # dp/dw = -2/3.  Oracle reads the orbit: Bernoulli(w), 1/(w(1-w)).
    print(f"    {'w':>6} {'I_context':>10} {'I_oracle':>10} "
          f"{'eta':>8} {'oracle advantage':>17}")
    for numerator in (1, 2, 3, 4, 5, 6, 7):
        w = Fraction(numerator, 8)
        p = (1 - w) * Fraction(2, 3)
        i_ctx = Fraction(4, 9) / (p * (1 - p))
        i_orc = 1 / (w * (1 - w))
        eta = i_ctx / i_orc
        if w == Fraction(1, 2):
            assert eta == Fraction(1, 2)       # exactly one half
        print(f"    {str(w):>6} {float(i_ctx):>10.3f} "
              f"{float(i_orc):>10.3f} {float(eta):>8.4f} "
              f"{float(1 / eta):>13.2f} x")
    # simultaneous access to all three contexts = the oracle:
    two_patterns, six_patterns = set(), set()
    for atom in ATOMS:
        pattern = tuple(int(atom[i] != atom[j]) for i, j in EDGES)
        if atom in {(0, 0, 0), (1, 1, 1)}:
            two_patterns.add(pattern)
        else:
            six_patterns.add(pattern)
    assert two_patterns == {(0, 0, 0)}
    assert all(sum(p) == 2 for p in six_patterns)
    assert not (two_patterns & six_patterns)
    print()
    print("  eta(1/2) = 1/2 EXACTLY: a context-bound reader pays a")
    print("  factor 2 in information against the orbit oracle at the")
    print("  balanced point (advantage -> 3/2 as w -> 1, -> infinity as")
    print("  w -> 0 where the oracle detects the rare orbit for free).")
    print("  And the gap is charged to CONTEXTUALITY, not estimator")
    print("  quality: the three edge parities of one world are (0,0,0)")
    print("  on the 2-orbit and two-ones on the 6-orbit -- disjoint --")
    print("  so reading all contexts of ONE world simultaneously is the")
    print("  oracle.  The price is for sequential context access, and")
    print("  it is closed form: no Monte Carlo anywhere in this table.")


# ---------------------------------------------------------------------
# 4. the drift transplant
# ---------------------------------------------------------------------

def riccati_fixed_point(Q: float, R: float) -> tuple:
    P = (-Q + sqrt(Q * Q + 4 * Q * R)) / 2    # P = ((P+Q)R)/(P+Q+R)
    K = (P + Q) / (P + Q + R)
    assert abs(P - ((P + Q) * R) / (P + Q + R)) < 1e-12
    return P, K


def kalman_impulse_weights(Q, R, P0, steps, lags):
    """Actual time-varying filter run to convergence; weight of the
    lag-k observation on the final estimate, by unit impulses."""
    weights = {}
    for k in lags:
        estimate, P = 0.0, P0
        for t in range(steps):
            P = P + Q
            gain = P / (P + R)
            y = 1.0 if t == steps - 1 - k else 0.0
            estimate = estimate + gain * (y - estimate)
            P = (1 - gain) * P
        weights[k] = estimate
    return weights


def posterior_variance(T, Q, R, P0, exclude=None):
    """Var(w_T | all y_1..y_T except y_exclude), exact Gaussian
    linear algebra (no simulation)."""
    times = [t for t in range(1, T + 1) if t != exclude]
    n = len(times)

    def cov_w(a, b):
        return P0 + Q * min(a, b)
    A = [[cov_w(a, b) + (R if a == b else 0.0) for b in times]
         for a in times]
    c = [cov_w(T, a) for a in times]
    # solve A z = c with partial pivoting
    z = c[:]
    M = [row[:] for row in A]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[pivot] = M[pivot], M[col]
        z[col], z[pivot] = z[pivot], z[col]
        for r in range(col + 1, n):
            f = M[r][col] / M[col][col]
            M[r] = [x - f * y for x, y in zip(M[r], M[col])]
            z[r] -= f * z[col]
    for col in range(n - 1, -1, -1):
        z[col] = (z[col] - sum(M[col][j] * z[j]
                               for j in range(col + 1, n))) / M[col][col]
    return cov_w(T, T) - sum(ci * zi for ci, zi in zip(c, z))


def verify_the_drift_transplant() -> None:
    Q, R, P0, T = 0.01, 1.0, 25.0, 40
    P, K = riccati_fixed_point(Q, R)
    lags = list(range(0, 16))
    weights = kalman_impulse_weights(Q, R, P0, 200, lags)
    assert abs(weights[0] - K) < 1e-9
    for k in range(0, 12):
        assert abs(weights[k + 1] / weights[k] - (1 - K)) < 1e-9, k
    print(f"    q = Q/R = {Q / R}: steady gain K = {K:.4f},"
          f" memory 1/K = {1 / K:.1f} steps")
    print(f"    influence of lag-k read = K(1-K)^k exactly"
          f" (impulse response, machine precision)")
    base = posterior_variance(T, Q, R, P0)
    nats = {}
    for k in range(3, 14):
        excluded = posterior_variance(T, Q, R, P0, exclude=T - k)
        nats[k] = 0.5 * log(excluded / base)
    target = 1 / (1 - K) ** 2
    print()
    print(f"    incremental nats of the lag-k read (exact Gaussian")
    print(f"    conditioning), ratio per lag vs (1-K)^-2"
          f" = {target:.4f}:")
    print(f"    {'k':>4} {'nats':>12} {'ratio':>8}")
    for k in range(4, 12):
        ratio = nats[k] / nats[k + 1]
        flag = abs(ratio / target - 1)
        assert flag < 0.03, (k, ratio)
        print(f"    {k:>4} {nats[k]:>12.3e} {ratio:>8.4f}")
    for k in range(4, 12):                     # influence ~ sqrt(nats)
        left = weights[k] / weights[k + 1]
        right = sqrt(nats[k] / nats[k + 1])
        assert abs(left / right - 1) < 0.02, k
    print()
    print("    influence_k / sqrt(nats_k) constant across lags (2%):")
    print("    the energy/amplitude split, re-derived in this channel.")
    print()
    print("    memory ~ 1/sqrt(q)  (window ~ 1/drift):")
    print(f"    {'q':>10} {'K':>10} {'K/sqrt(q)':>10}")
    for q in (1e-2, 1e-4, 1e-6):
        _, gain = riccati_fixed_point(q, 1.0)
        print(f"    {q:>10.0e} {gain:>10.4g} {gain / sqrt(q):>10.4f}")
    _, tiny = riccati_fixed_point(1e-8, 1.0)
    assert abs(tiny / sqrt(1e-8) - 1) < 0.01
    print()
    # the fourth-root compression of the oracle gap
    print("    the oracle gap under drift (operating point w = 1/2:")
    print("    R_context = 1/I_ctx = 1/2, R_oracle = 1/I_orc = 1/4):")
    print(f"    {'q':>10} {'P_ctx/P_orc':>12} {'SD ratio':>10}")
    for q_scale in (1e-2, 1e-4, 1e-6):
        # same state drift Q for both readers; only R differs
        p_ctx, _ = riccati_fixed_point(q_scale, 0.5)
        p_orc, _ = riccati_fixed_point(q_scale, 0.25)
        var_ratio = p_ctx / p_orc
        print(f"    {q_scale:>10.0e} {var_ratio:>12.4f} "
              f"{sqrt(var_ratio):>10.4f}")
    p_ctx, _ = riccati_fixed_point(1e-8, 0.5)
    p_orc, _ = riccati_fixed_point(1e-8, 0.25)
    assert abs(p_ctx / p_orc - sqrt(2)) < 0.01
    print()
    print("  P ~ sqrt(QR) at small q, so the STATIC information gap")
    print("  1/eta = 2 becomes a variance gap sqrt(2) and an SD gap")
    print("  2^(1/4) = 1.19: the oracle's advantage enters the tracking")
    print("  error at the FOURTH ROOT.  A 2x information oracle is a")
    print("  19% tracker.  This is the frame's version of the")
    print("  stat-tracker result that cut the oracle's advantage to")
    print("  near zero without Monte Carlo: the drifting game")
    print("  compresses oracles by two square roots (Riccati, then")
    print("  variance -> SD), and what remains is closed form, priced")
    print("  in s3, and charged to contextuality.")


def run_verification_suite() -> None:
    sections = [
        ("Zero evidence from the theory: w is a pure trust coordinate",
         verify_zero_evidence),
        ("The instrument: the parity channel p(w) = 2(1-w)/3",
         verify_the_instrument),
        ("The price of contextuality: eta(1/2) = 1/2, closed form",
         verify_the_price_of_contextuality),
        ("The drift transplant: sqrt laws and the fourth-root gap",
         verify_the_drift_transplant),
    ]
    for index, (title, check) in enumerate(sections, start=1):
        print("=" * 70)
        print(f"{index}. {title}")
        print("=" * 70)
        check()
        print()
    print("=" * 70)
    print("suite complete")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
