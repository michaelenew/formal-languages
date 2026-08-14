"""The relational sheet: absolute parity is gauge, relative parity is
physical.

0062 showed one traversal of an odd definition cycle is the deck flip
(T^k = complement) and two traversals are the identity.  The user's
readings of that fact, verified here:

  s1  N MOVES PIN 1/2; 2N MOVES PIN NOTHING.  Stationarity under T
      implies invariance under T^k = complement, so every channel's
      marginal is EXACTLY 1/2 -- the forced coin comes entirely from
      the odd power.  Invariance under T^2k = identity is vacuous:
      any belief whatsoever is consistent with the even power.
      "Whatever I see now" survives 2N moves; 1/2 survives N.

  s2  OBSERVATION HAS A PARITY.  Reading channel j from channel i
      through the constraint chain complements once per hop: even
      paths read the value itself, odd paths its dual.  0-hop and
      2-hop observation are the same observation; 1-hop is the
      other one.  On the double cover this is the bipartition of
      the 2k-cycle: even paths stay on your sheet.

  s3  THE SHEET IS RELATIONAL.  Two liars, jointly: the traversal
      generates only the DIAGONAL flip (the individual flips are
      not powers of it), so the gauge group is "flip both sheets at
      once".  Consequences, verified exactly:
        - each liar's own value: marginal forced to 1/2 -- one full
          bit of compulsory noise; the absolute sheet is invisible
          even in principle (it is gauge);
        - the XOR of the two liars: INVARIANT under the dynamics,
          exact (entropy 0) in every floor solution -- the relative
          sheet is a bona fide observable, free of charge.
      The same holds for two triangles (agreement of their constant
      worlds is deck-invariant; either sheet alone is not).  This
      is the frame's version of "a 2*pi rotation of the universe is
      invisible; a 2*pi rotation of one arm of the interferometer
      is measurable."

  s4  "EXACTLY TWO" IS THE Z2 CASE.  The dual is a d-fold echo in
      general: two odometers jointly have deck group Z_2^w -- each
      absolute position is forced-uniform (w bits of noise), while
      the DIFFERENCE is invariant and exact.  Everything is its own
      dual when the holonomy is Z2; its own d-fold echo when the
      holonomy is Z_d.

Run directly for the verification suite.
"""

from __future__ import annotations

import itertools
import random
import sys
from fractions import Fraction
from math import log2

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from lossy_revision_and_the_carry import cycles_of


def negation_cycle_map(k: int) -> dict:
    return {n: tuple(1 - n[(i + 1) % k] for i in range(k))
            for n in itertools.product((0, 1), repeat=k)}


def push(T, pi):
    out = {}
    for a, m in pi.items():
        out[T[a]] = out.get(T[a], 0) + m
    return out


def random_stationary(T, rng):
    """A random rational mixture of orbit-uniforms."""
    orbits = cycles_of(T)
    weights = [Fraction(rng.randrange(1, 9)) for _ in orbits]
    total = sum(weights)
    pi = {}
    for orbit, w in zip(orbits, weights):
        for a in orbit:
            pi[a] = w / (total * len(orbit))
    return pi


# ---------------------------------------------------------------------
# 1. N moves pin 1/2; 2N moves pin nothing
# ---------------------------------------------------------------------

def verify_odd_power_pinning(seed=63001) -> None:
    rng = random.Random(seed)
    for k in (3, 5):
        T = negation_cycle_map(k)
        for _ in range(20):
            pi = random_stationary(T, rng)
            assert push(T, pi) == pi
            flipped = {tuple(1 - b for b in a): m for a, m in pi.items()}
            assert flipped == pi               # invariance under T^k = deck
            for i in range(k):                 # every marginal exactly 1/2
                marginal = sum(m for a, m in pi.items() if a[i] == 1)
                assert marginal == Fraction(1, 2), (k, i)
        # 2N moves pin nothing: T^2k = id, so ANY distribution is
        # invariant under the even power -- including a point mass.
        point = {a: (Fraction(1) if a == (0,) * k else Fraction(0))
                 for a in T}
        after = dict(point)
        for _ in range(2 * k):
            after = push(T, after)
        assert after == point
        print(f"    k={k}: every stationary belief is complement-"
              f"symmetric; all marginals exactly 1/2")
        print(f"         a point mass ('whatever I see now') survives"
              f" {2 * k} moves unchanged")
    print()
    print("  The forced coin is the odd power alone: consistency with")
    print("  ONE traversal (the deck flip) pins every channel at 1/2;")
    print("  consistency with TWO traversals pins nothing at all.")


# ---------------------------------------------------------------------
# 2. observation has a parity
# ---------------------------------------------------------------------

def verify_observation_parity() -> None:
    for k in (3, 5):
        cover = []
        for v in itertools.product((0, 1), repeat=2 * k):
            if all(v[i] != v[(i + 1) % (2 * k)] for i in range(2 * k)):
                cover.append(v)
        assert len(cover) == 2
        for v in cover:
            for i in range(2 * k):
                for hops in range(2 * k):
                    j = (i + hops) % (2 * k)
                    if hops % 2 == 0:
                        assert v[j] == v[i]        # even path: itself
                    else:
                        assert v[j] == 1 - v[i]    # odd path: the dual
        print(f"    k={k}: on the double cover, even paths read the")
        print(f"         value, odd paths its complement -- 0-hop and")
        print(f"         2-hop observation are the same observation")
    print()
    print("  Observation-through-constraints has only a parity: the")
    print("  bipartition of the cover.  What oscillates at successive")
    print("  encounters is the path parity, and it always oscillates")
    print("  between the same two values -- the value and its dual.")


# ---------------------------------------------------------------------
# 3. the sheet is relational
# ---------------------------------------------------------------------

def entropy(pi):
    return -sum(float(m) * log2(float(m)) for m in pi.values() if m)


def verify_the_relational_sheet() -> None:
    # two liars, jointly
    T = {(a, b): (1 - a, 1 - b) for a in (0, 1) for b in (0, 1)}
    # (a) the joint traversal generates only the diagonal flip
    powers = set()
    current = {k: k for k in T}
    for _ in range(4):
        current = {k: T[current[k]] for k in T}
        powers.add(tuple(sorted(current.items())))
    individual = {(a, b): (1 - a, b) for a, b in T}
    assert tuple(sorted(individual.items())) not in powers
    # (b) XOR is invariant under the dynamics
    for (a, b) in T:
        na, nb = T[(a, b)]
        assert (na ^ nb) == (a ^ b)
    # (c) the two floor solutions: XOR exact, marginals forced fair
    orbits = cycles_of(T)
    assert sorted(len(o) for o in orbits) == [2, 2]
    for orbit in orbits:
        pi = {s: Fraction(1, 2) for s in orbit}
        xor_values = {a ^ b for (a, b) in orbit}
        assert len(xor_values) == 1                # relative bit: EXACT
        for index in (0, 1):                       # absolute: forced fair
            marg = sum(m for s, m in pi.items() if s[index] == 1)
            assert marg == Fraction(1, 2)
        assert entropy(pi) == 1.0
    print("    two liars: gauge group = the diagonal flip only;")
    print("      each liar's value     marginal 1/2, forced (gauge)")
    print("      XOR of the two        invariant, exact in every floor")
    print("      total entropy         1 bit (the shared coin), not 2")
    # (d) two triangles: agreement of constant worlds is deck-invariant
    T3 = negation_cycle_map(3)
    joint = {(x, y): (T3[x], T3[y]) for x in T3 for y in T3}
    for (x, y) in joint:
        nx, ny = joint[(x, y)]
        assert (x == y) == (nx == ny)              # agreement invariant
    print("    two triangles: 'do their worlds agree' is invariant;")
    print("      'which world is mine' is not -- the sheet is a relation,")
    print("      not a property.")
    print()
    print("  The absolute sheet is gauge: no observable of the dynamics")
    print("  distinguishes it, and its marginal is compulsory noise.")
    print("  The RELATIVE sheet between two systems is a free, exact")
    print("  observable.  You cannot know which of the two dual worlds")
    print("  you are in -- and everyone agrees about every difference.")


# ---------------------------------------------------------------------
# 4. "exactly two" is the Z2 case: duals grade to d-fold echoes
# ---------------------------------------------------------------------

def verify_the_graded_echo(w=3) -> None:
    size = 1 << w
    T = {(a, b): ((a + 1) % size, (b + 1) % size)
         for a in range(size) for b in range(size)}
    for (a, b) in T:
        na, nb = T[(a, b)]
        assert (na - nb) % size == (a - b) % size  # difference invariant
    orbits = cycles_of(T)
    assert all(len(o) == size for o in orbits) and len(orbits) == size
    for orbit in orbits[:3]:
        pi = {s: Fraction(1, size) for s in orbit}
        diffs = {(a - b) % size for (a, b) in orbit}
        assert len(diffs) == 1                     # relative: exact
        for index in (0, 1):
            for value in range(size):
                m = sum(mm for s, mm in pi.items() if s[index] == value)
                assert m == Fraction(1, size)      # absolute: uniform
    print(f"    two odometers (w={w}): difference invariant and exact;")
    print(f"      each absolute position forced-uniform ({w} bits of")
    print(f"      noise); deck group Z_{size}, not Z_2.")
    print()
    print("  'Everything is its own dual' is the Z2 holonomy case.  In")
    print("  general everything is its own d-fold echo: d consistent")
    print("  unobservable positions of the rest of the world, with all")
    print("  DIFFERENCES exact and shared.  The dual pair is the")
    print("  physically dominant case because the cheapest paradox has")
    print("  period 2 -- but the tower above it is real (the odometer).")


def run_verification_suite() -> None:
    sections = [
        ("N moves pin 1/2; 2N moves pin nothing",
         verify_odd_power_pinning),
        ("Observation has a parity", verify_observation_parity),
        ("The sheet is relational", verify_the_relational_sheet),
        ("The graded echo", verify_the_graded_echo),
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
