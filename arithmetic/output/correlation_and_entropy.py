"""Does correlation buy back the forced entropy?  (0058 s3's open door)

0058 measured forced entropy over PRODUCT distributions: the liar costs
1 bit, the odd k-cycle costs k bits.  The question green-lit here: can
CORRELATED distributions reduce the bill?  The joint generalization of
0058's "distributional solution" (fixed point of the induced map on
Bernoulli parameters) is a joint distribution fixed under pushforward
by the revision map T -- a stationary distribution of the definition's
own dynamics.  For negation systems T is a PERMUTATION of the atoms,
so the stationary set is exactly the mixtures of orbit-uniforms, and
everything is computable in closed form.

  s1  THE STATIONARY POLYTOPE.  Forced entropy over correlated
      distributions = log2(smallest orbit of T).  For the odd k-cycle:
      the constants {00..0, 11..1} form a 2-orbit, and no atom is
      fixed (that IS the paradox), so the floor is EXACTLY 1 BIT for
      every odd k.  Correlation buys back k-1 of the k bits; the last
      bit is unbuyable.  And the residual bit is not about VALUE but
      about PHASE: T has no fixed point, so the system must oscillate,
      and the coin is the phase of a period-2 clock.

  s2  ONE COIN, MANY LIARS -- AND THE EXPENSIVE PARADOX.  m
      independent liars jointly cost 1 bit total (each marginal is
      still a forced fair coin; correlation pays for all but one).
      The tax is per-WORLD, not per-paradox: it is log2 of the
      shortest revision period.  Negation paradoxes have period 2 --
      the cheapest possible.  The self-increment paradox n := n+1
      (carry-coupled) has revision period 2^w on w bits: its tax is
      the WHOLE STATE, and its unique stationary distribution is
      uniform (the w -> infinity limit is Haar measure on Z_2 -- the
      odometer is uniquely ergodic).  Strip the carry (n := n XOR 1)
      and the tax collapses back to 1 bit: the carry channel, the
      wall's agent everywhere else in this corpus, is also what makes
      a paradox expensive.

  s3  TRUTH VS CERTAINTY.  Along the triangle's stationary polytope,
      satisfaction falls monotonically toward the floor but entropy
      peaks at exactly the uniform -- 0058's product solution -- so
      the product solution is Pareto-DOMINATED: full weight on the
      6-orbit gains truth (1/2 -> 2/3) AND sheds entropy (3 -> 2.585
      bits) at once.  The true frontier runs from (truth 2/3, the
      noncontextual bound, log2 6 bits) to (truth 0, 1 bit); past the
      dominated region certainty is bought with truth, and truth is
      capped at 2/3 at any price.

  s4  THE CONTEXTWISE READING (no-signaling / sheaf).  Keep pointwise
      truth per context and demand only marginal consistency: the
      triangle has a UNIQUE empirical model -- perfect anticorrelation
      on every edge, all marginals 1/2 -- and no global joint exists.
      What correlation cannot buy in this reading is not entropy but
      the existence of a global state at all.

  s5  THE AMPLITUDE BUY-BACK.  Quantize the revision dynamics: T
      becomes a permutation UNITARY, and a solution is an invariant
      state.  No basis state is invariant (the paradox), but the cat
      state (|00..0> + |11..1>)/sqrt(2) IS -- a PURE stationary state,
      entropy zero, whose measurement statistics are exactly the
      classical floor distribution.  The classical tax log2(min
      period) is phase entropy, and amplitudes internalize phase.
      The buy-back completes exactly at the square root of
      probability -- the same level where the stat-tracker corpus
      found influence must live (influence ~ sqrt(information)).

Run directly for the verification suite.
"""

from __future__ import annotations

import cmath
import itertools
from fractions import Fraction
from math import log2


# ---------------------------------------------------------------------
# revision-map machinery
# ---------------------------------------------------------------------

def negation_cycle_map(k: int) -> dict:
    """T(n)_i = NOT n_{(i+1) mod k}: the odd/even negation cycle."""
    return {n: tuple(1 - n[(i + 1) % k] for i in range(k))
            for n in itertools.product((0, 1), repeat=k)}


def complement_map(m: int) -> dict:
    """m independent liars: global complement."""
    return {n: tuple(1 - b for b in n)
            for n in itertools.product((0, 1), repeat=m)}


def product_map(T1: dict, T2: dict) -> dict:
    return {(a, b): (T1[a], T2[b]) for a in T1 for b in T2}


def increment_map(w: int) -> dict:
    """The self-increment paradox n := n + 1 mod 2^w (the odometer):
    the carry channel couples every bit into one revision cycle."""
    return {n: (n + 1) % (1 << w) for n in range(1 << w)}


def xor_one_map(w: int) -> dict:
    """n := n XOR 1 -- the same '+1' with the carry channel stripped."""
    return {n: n ^ 1 for n in range(1 << w)}


def orbits(T: dict) -> list:
    """Orbit decomposition; verifies T is a permutation on the way."""
    assert sorted(T.values(), key=repr) == sorted(T.keys(), key=repr)
    seen, out = set(), []
    for start in T:
        if start in seen:
            continue
        orbit, current = [], start
        while current not in seen:
            seen.add(current)
            orbit.append(current)
            current = T[current]
        out.append(orbit)
    return out


# Stationarity lemma (one line, used throughout): the pushforward of
# pi by a permutation T is (T pi)(s) = pi(T^-1(s)), so pi is stationary
# iff pi(T^-1(s)) = pi(s) for every s, i.e. iff pi is CONSTANT ON
# ORBITS.  Stationary distributions = mixtures of orbit-uniforms;
# with disjoint supports the mixture entropy is exact:
#     H = H(weights) + sum_o w_o * log2 |orbit o|
# so  min H over stationary = log2(smallest orbit),
# and max H = log2(number of atoms) at the uniform (= 0058's product
# solution, when one exists at the uniform point).


def entropy_floor(T: dict) -> float:
    return log2(min(len(o) for o in orbits(T)))


def h2(w: float) -> float:
    if w in (0.0, 1.0):
        return 0.0
    return -w * log2(w) - (1 - w) * log2(1 - w)


# ---------------------------------------------------------------------
# 1. the stationary polytope and the 1-bit floor
# ---------------------------------------------------------------------

def verify_the_stationary_polytope() -> None:
    print(f"    {'cycle':>6} {'atoms':>6} {'orbit sizes':>22} "
          f"{'floor':>6} {'product':>8} {'bought':>7}")
    for k in (3, 5, 7, 4, 6):
        T = negation_cycle_map(k)
        orbs = orbits(T)
        sizes = sorted(len(o) for o in orbs)
        fixed = [o for o in orbs if len(o) == 1]
        floor = entropy_floor(T)
        if k % 2:
            assert not fixed, k                     # the paradox
            assert sizes[0] == 2, k                 # the constants
            constants = {tuple([0] * k), tuple([1] * k)}
            assert any(set(o) == constants for o in orbs), k
            assert floor == 1.0, k
        else:
            assert fixed, k                         # alternating atoms
            assert floor == 0.0, k
        shown = ",".join(str(s) for s in sizes[:6])
        if len(sizes) > 6:
            shown += ",..."
        print(f"    {k:>6} {1 << k:>6} {shown:>22} "
              f"{floor:>6.1f} {k:>8} {k - floor:>7.1f}")
        # 0058's product fixed point p_i = 1 - p_{i+1} forces all 1/2
        # for odd k; the uniform it names is the MAX-entropy stationary
        # point (log2 of the atom count = k bits).
    print()
    print("  Stationary distributions of the revision map T are exactly")
    print("  the mixtures of orbit-uniforms (T is a permutation), so the")
    print("  correlated forced entropy is log2(smallest orbit).  Odd")
    print("  cycles have no fixed atom -- that IS the paradox -- but the")
    print("  two constant strings form a 2-orbit, so the floor is")
    print()
    print("      forced entropy (correlated)  =  1 bit,  for every odd k")
    print()
    print("  against k bits for 0058's product solution (which is the")
    print("  MAXIMUM-entropy stationary point, the uniform).  Correlation")
    print("  buys back k-1 of the k bits.  The residual bit is PHASE,")
    print("  not value: T fixes no atom, so the world must oscillate,")
    print("  and the floor distribution -- the fair coin between 00..0")
    print("  and 11..1 -- is uncertainty about the phase of a period-2")
    print("  clock, not about which constraint holds (it puts all its")
    print("  mass on atoms that violate EVERY edge).")


# ---------------------------------------------------------------------
# 2. one coin many liars, and the graded tax
# ---------------------------------------------------------------------

def marginal(dist: dict, index: int) -> Fraction:
    return sum(p for atom, p in dist.items() if atom[index] == 1)


def verify_one_coin_many_liars() -> None:
    print("    independent liars, jointly:")
    print(f"    {'m':>3} {'orbit sizes':>12} {'joint floor':>12} "
          f"{'marginals':>10}")
    for m in (1, 2, 3, 4):
        T = complement_map(m)
        sizes = {len(o) for o in orbits(T)}
        assert sizes == {2}, m
        floor = entropy_floor(T)
        assert floor == 1.0, m
        # the floor distribution: fair coin on {00..0, 11..1}
        half = Fraction(1, 2)
        dist = {tuple([0] * m): half, tuple([1] * m): half}
        assert dist == {T[a]: p for a, p in dist.items()}  # stationary
        margs = {marginal(dist, i) for i in range(m)}
        assert margs == {half}, m                  # each coin still fair
        print(f"    {m:>3} {'all 2':>12} {'1 bit':>12} {'all 1/2':>10}")
    mixed = product_map(complement_map(1), negation_cycle_map(3))
    assert entropy_floor(mixed) == 1.0             # liar + triangle
    print()
    print("    liar + Specker triangle jointly:      floor = 1 bit")
    print()
    print("  m liars cost 1 bit TOTAL: every marginal is still a forced")
    print("  fair coin, but one shared coin drives them all (the floor")
    print("  distribution is perfectly correlated; mutual information")
    print("  carries the other m-1 bits).  The tax is per-world, not")
    print("  per-paradox: it is log2 of the shortest revision period.")
    print()
    print("    the graded tax (log2 of the shortest revision period):")
    print(f"    {'paradox':<28} {'width':>6} {'period':>8} {'tax':>10}")
    for w in (2, 3, 4, 5):
        T = increment_map(w)
        orbs = orbits(T)
        assert len(orbs) == 1 and len(orbs[0]) == 1 << w, w
        print(f"    {'n := n + 1  (with carry)':<28} {w:>6} "
              f"{1 << w:>8} {entropy_floor(T):>7.0f} bits")
    for w in (3, 5):
        T = xor_one_map(w)
        assert entropy_floor(T) == 1.0, w
        print(f"    {'n := n ^ 1  (carry stripped)':<28} {w:>6} "
              f"{2:>8} {1:>7.0f} bit")
    print()
    print("  The self-increment paradox is one revision cycle through")
    print("  ALL 2^w states: its unique stationary distribution is")
    print("  uniform, tax = w bits = everything, diverging with width")
    print("  (the w->infinity limit is the 2-adic odometer, uniquely")
    print("  ergodic with Haar measure: every bit an independent fair")
    print("  coin, and correlation can buy back nothing at all).  Strip")
    print("  the carry and the tax collapses to 1 bit.  The carry")
    print("  channel -- the wall's agent in 0053/0054 -- is also what")
    print("  makes a paradox expensive: it couples the bits into one")
    print("  long clock.")


# ---------------------------------------------------------------------
# 3. truth vs certainty along the stationary polytope
# ---------------------------------------------------------------------

def verify_the_truth_certainty_trade() -> None:
    k = 3
    edges = [(0, 1), (1, 2), (2, 0)]

    def satisfied(atom):
        return sum(atom[i] == 1 - atom[j] for i, j in edges)

    counts = {atom: satisfied(atom)
              for atom in itertools.product((0, 1), repeat=k)}
    constants = {tuple([0] * k), tuple([1] * k)}
    for atom, c in counts.items():
        assert c == (0 if atom in constants else 2), atom
    # stationary polytope: weight w on the 2-orbit (constants),
    # 1-w on the 6-orbit.  E[satisfied fraction] = (1-w) * 2/3,
    # H = h2(w) + w*log2(2) + (1-w)*log2(6), exact (disjoint supports).
    print("    every atom satisfies at most 2 of 3 contexts (constants: 0,")
    print("    all six others: exactly 2) -- the noncontextual bound 2/3.")
    print()
    print(f"    {'w on 2-orbit':>13} {'E[satisfied]':>13} "
          f"{'entropy bits':>13}")
    rows = []
    for numerator in (0, 1, 2, 3, 4):
        w = numerator / 4
        sat = (1 - w) * 2 / 3
        entropy = h2(w) + w * 1 + (1 - w) * log2(6)
        rows.append((w, sat, entropy))
        marker = "   <- 0058's product solution" if w == 0.25 else ""
        print(f"    {w:>13.2f} {sat:>13.3f} {entropy:>13.3f}{marker}")
    assert abs(rows[0][2] - log2(6)) < 1e-12 and rows[0][1] == 2 / 3
    assert rows[-1][2] == 1.0 and rows[-1][1] == 0.0
    assert abs(rows[1][2] - 3.0) < 1e-12          # uniform = 3 bits
    assert abs(rows[1][1] - 0.5) < 1e-12
    # satisfaction is monotone in w; entropy is NOT -- it peaks at the
    # uniform (w = 1/4, the product solution), which is therefore
    # Pareto-DOMINATED: w = 0 has more truth AND less entropy.
    assert all(a[1] > b[1] for a, b in zip(rows, rows[1:]))
    fine = [h2(w) + w + (1 - w) * log2(6)
            for w in (i / 256 for i in range(257))]
    peak = max(range(257), key=lambda i: fine[i])
    assert peak == 64 and abs(fine[peak] - 3.0) < 1e-12   # w = 1/4
    assert rows[0][1] > rows[1][1] and rows[0][2] < rows[1][2]
    print()
    print("  Satisfaction falls monotonically with w, but entropy does")
    print("  NOT: it peaks at exactly the uniform -- which is 0058's")
    print("  product solution.  So the product solution is Pareto-")
    print("  DOMINATED: shifting all weight to the 6-orbit (w = 0) gains")
    print("  truth (1/2 -> 2/3) AND sheds entropy (3 -> 2.585 bits) at")
    print("  once.  Correlation is not a trade against the product")
    print("  baseline; it is a strict improvement in both coordinates.")
    print("  The real frontier runs from (truth 2/3, 2.585 bits) at the")
    print("  6-orbit uniform down to (truth 0, 1 bit) at the floor: past")
    print("  the dominated region, certainty IS bought with truth, and")
    print("  truth is capped at 2/3 (1 - the contextual fraction of 0058")
    print("  s1) at any price.  Both walls stand; the product point just")
    print("  never sat on either.")


# ---------------------------------------------------------------------
# 4. the contextwise reading: unique model, no global state
# ---------------------------------------------------------------------

def verify_the_contextwise_reading() -> None:
    # Each edge (i,j) carries a distribution on (n_i, n_j) supported on
    # the anticorrelated pairs {01, 10}; write a_e = P(n_i=1, n_j=0).
    # Marginal consistency chains the three edges:
    a12 = Fraction(1, 2)  # derived below; start symbolic and check
    # edge12: P(n1=1) = a12,      P(n2=1) = 1 - a12
    # edge23: P(n2=1) = a23   =>  a23 = 1 - a12;  P(n3=1) = a12
    # edge31: P(n3=1) = a31   =>  a31 = a12;      P(n1=1) = 1 - a12
    # consistency on n1:  a12 = 1 - a12  =>  a12 = 1/2, uniquely.
    solutions = [a for a in (Fraction(n, 12) for n in range(13))
                 if a == 1 - a]
    assert solutions == [Fraction(1, 2)]
    a23, a31 = 1 - a12, a12
    for name, a in (("e12", a12), ("e23", a23), ("e31", a31)):
        assert a == Fraction(1, 2), name
    print("  Keep pointwise truth PER CONTEXT (each edge distribution")
    print("  supported on its anticorrelated pairs) and demand only that")
    print("  shared marginals agree.  The consistency chain forces every")
    print("  parameter to 1/2: the empirical model is UNIQUE -- perfect")
    print("  anticorrelation on each edge, every marginal a fair coin,")
    print("  1 bit per context.")
    # no global joint: its edge marginals would need support inside the
    # anticorrelated pairs for all three edges simultaneously -- i.e.
    # support inside the global solution set, which is empty.
    edges = [(0, 1), (1, 2), (2, 0)]
    violates_some = all(any(atom[i] != 1 - atom[j] for i, j in edges)
                        for atom in itertools.product((0, 1), repeat=3))
    assert violates_some
    print()
    print("  No global joint reproduces it: every atom violates some")
    print("  edge, so any joint puts mass on a violating pair of some")
    print("  context.  In this reading correlation cannot buy entropy")
    print("  because there is nothing global to buy -- the obstruction")
    print("  is the existence of a global state, full stop.  (This is")
    print("  the Abramsky-Brandenburger strong-contextuality reading;")
    print("  the model sits at the no-signaling extreme, reported in the")
    print("  literature as beyond quantum realization for the triangle.)")


# ---------------------------------------------------------------------
# 5. the amplitude buy-back
# ---------------------------------------------------------------------

def push_amplitudes(T: dict, psi: dict) -> dict:
    """U|n> = |T(n)>: amplitudes travel with the atoms."""
    out = {}
    for atom, amp in psi.items():
        out[T[atom]] = out.get(T[atom], 0) + amp
    return out


def proportional(psi: dict, phi: dict) -> bool:
    """Same ray: phi = c * psi with |c| = 1 (float tolerance)."""
    ratios = [phi.get(a, 0) / amp for a, amp in psi.items()
              if abs(amp) > 1e-12]
    c = ratios[0]
    return abs(abs(c) - 1) < 1e-9 and \
        all(abs(r - c) < 1e-9 for r in ratios) and \
        all(abs(phi.get(a, 0)) < 1e-9
            for a in phi if a not in psi)


def verify_the_amplitude_buy_back() -> None:
    root_half = 2 ** -0.5
    print(f"    {'system':<24} {'invariant basis state':>22} "
          f"{'invariant PURE state':>22}")
    for label, T, low, high in (
            ("Specker triangle", negation_cycle_map(3),
             (0, 0, 0), (1, 1, 1)),
            ("two liars", complement_map(2), (0, 0), (1, 1)),
    ):
        assert all(T[a] != a for a in T)           # no classical atom
        cat = {low: root_half, high: root_half}
        assert proportional(cat, push_amplitudes(T, cat))
        anti = {low: root_half, high: -root_half}  # eigenvalue -1
        assert proportional(anti, push_amplitudes(T, anti))
        stats = {a: abs(amp) ** 2 for a, amp in cat.items()}
        assert all(abs(p - 0.5) < 1e-12 for p in stats.values())
        print(f"    {label:<24} {'none':>22} "
              f"{'(|lo> + |hi>)/sqrt2':>22}")
    # the odometer: character states over the single 2^w-orbit
    w = 3
    T = increment_map(w)
    size = 1 << w
    for j in range(size):
        omega = cmath.exp(2j * cmath.pi * j / size)
        psi = {n: omega ** n / size ** 0.5 for n in range(size)}
        assert proportional(psi, push_amplitudes(T, psi)), j
    print(f"    {'odometer (w=3)':<24} {'none':>22} "
          f"{'all 8 character states':>22}")
    print()
    print("  Quantized, the revision map is a permutation unitary, and")
    print("  every finite permutation has an orthonormal eigenbasis: the")
    print("  paradox has PURE invariant states -- entropy ZERO -- whose")
    print("  computational-basis statistics reproduce the classical floor")
    print("  exactly (the cat state measures as the fair coin between")
    print("  00..0 and 11..1; the characters measure as the uniform).")
    print()
    print("  So the ledger closes:   product distributions   k bits")
    print("                          correlated (classical)  1 bit")
    print("                          amplitudes (quantum)    0 bits")
    print()
    print("  The classical residue log2(min period) is PHASE entropy,")
    print("  and amplitudes are exactly the objects that internalize")
    print("  phase.  The buy-back completes at the square root of")
    print("  probability -- the same level where the stat-tracker corpus")
    print("  found the conserved influence budget must live (influence ~")
    print("  sqrt(information): sensitivities compose like amplitudes,")
    print("  informations like variances).  Probabilities cannot hold a")
    print("  paradox below 1 bit; square roots of probabilities hold it")
    print("  at zero, and pay for it in measurement uncertainty: the")
    print("  state is complete, the readout is not.")


def run_verification_suite() -> None:
    sections = [
        ("The stationary polytope: correlation buys back all but 1 bit",
         verify_the_stationary_polytope),
        ("One coin, many liars -- and the graded tax",
         verify_one_coin_many_liars),
        ("Truth vs certainty along the polytope",
         verify_the_truth_certainty_trade),
        ("The contextwise reading: unique model, no global state",
         verify_the_contextwise_reading),
        ("The amplitude buy-back",
         verify_the_amplitude_buy_back),
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
