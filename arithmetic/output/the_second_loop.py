"""The second loop: double covers, holonomy, and the knot counter.

The user's three threads, made computational:

  s1  THE DOUBLE COVER.  The odd context cycle with "differ"
      constraints has no global section; its connected double cover
      (the 2k-cycle) has EXACTLY TWO, and the deck transformation
      (rotation by k) swaps them.  Going around twice trivializes
      the obstruction -- the Z2 holonomy dies on the double cover.

  s2  THE FRAME ALREADY UNROLLS IT.  For the odd k-cycle system the
      revision map satisfies T^k = complement and T^2k = identity:
      one traversal of the definitions is the deck flip, two
      traversals are the identity.  The 2k-orbit of mixed worlds IS
      the unrolled double traversal, and the constant worlds see
      pure deck action (no transport): the phase fiber.  The
      stationary solutions of 0059 live on the double cover; the
      +/- cat states of 0059 s5 are its two spinor sectors
      (deck-periodic and deck-antiperiodic).

  s3  THE HOLONOMY LEDGER.  The joint tax of several paradoxes is
      log2 of the ORDER OF THE JOINT TRAVERSAL -- lcm of the
      periods, not the product:
          m liars                 lcm(2,..,2) = 2      1 bit
          liar + triangle         lcm(2,2)    = 2      1 bit
          odometer(w) + liar      lcm(2^w,2)  = 2^w    w bits
          odometer(w1)+odometer(w2)  lcm      = 2^max  max bits
      The "one coin, many liars" of 0059 is the DIAGONAL deck
      group; the floor distribution is Haar measure on the cyclic
      group the traversal generates.  The coin is Haar on the deck.

  s4  THE KNOT COUNTER.  Walking a knot diagram from a crossing,
      +1 per over-pass and -1 per under-pass:
        - the full loop always scores 0 (every crossing is visited
          once over, once under -- the diagram is its own double
          cover, each chord has two endpoints);
        - the first-return score = (own visit) + the signed sum
          over crossings INTERLEAVED with the start (one visit
          inside the arc) -- chord-diagram interlacement, verified
          exhaustively over all diagrams with <= 5 crossings;
        - Gauss's planarity parity (every chord of a classical
          diagram interleaves an EVEN number of chords) forces the
          first-return score to be ODD -- never 0; +-1 in the
          balanced case;
        - Gauss-even diagrams with first-return score +-3 exist,
          so +-1 is the balanced case, not a law.

  s5  THE HALF WINDING.  The winding integral of the circle about
      points approaching a boundary point from alternating sides is
      2*pi, 0, 2*pi, 0, ...; at the boundary point itself the
      principal-value integral is EXACTLY pi.  Abel and Cesaro
      summation of the alternating sequence give 1/2 -- the
      regularized value of Grandi's series equals the on-curve
      winding.  The user's identification is exact (it is the
      Sokhotski-Plemelj half-residue).

Run directly for the verification suite.
"""

from __future__ import annotations

import cmath
import itertools
import sys
from fractions import Fraction
from math import gcd, log2, pi

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from lossy_revision_and_the_carry import cycles_of


def lcm(a, b):
    return a * b // gcd(a, b)


# ---------------------------------------------------------------------
# 1. the double cover of the context cycle
# ---------------------------------------------------------------------

def cycle_solutions(length: int) -> list:
    """Proper assignments of the length-cycle with 'differ' edges."""
    out = []
    for v in itertools.product((0, 1), repeat=length):
        if all(v[i] != v[(i + 1) % length] for i in range(length)):
            out.append(v)
    return out


def verify_the_double_cover() -> None:
    print(f"    {'cycle':>8} {'solutions':>10}   "
          f"{'double cover':>12} {'solutions':>10} {'deck swaps them':>16}")
    for k in (3, 5, 7):
        base = cycle_solutions(k)
        cover = cycle_solutions(2 * k)
        assert base == [] and len(cover) == 2, k
        a, b = cover
        rotated = tuple(a[(i + k) % (2 * k)] for i in range(2 * k))
        assert rotated == b                       # deck = rotation by k
        print(f"    {'C' + str(k):>8} {'none':>10}   "
              f"{'C' + str(2 * k):>12} {2:>10} {'yes':>16}")
    print()
    print("  The odd cycle has no global section; its connected double")
    print("  cover has exactly two, and the deck transformation")
    print("  (rotation by k = going around once more) exchanges them.")
    print("  The Z2 holonomy that makes the triangle contextual is")
    print("  trivial upstairs: going around twice IS consistent.")


# ---------------------------------------------------------------------
# 2. the frame already unrolls the double cover
# ---------------------------------------------------------------------

def negation_cycle_map(k: int) -> dict:
    return {n: tuple(1 - n[(i + 1) % k] for i in range(k))
            for n in itertools.product((0, 1), repeat=k)}


def verify_the_frame_unrolls_it() -> None:
    for k in (3, 5):
        T = negation_cycle_map(k)
        atoms = list(T)

        def power(p, n):
            for _ in range(p):
                n = T[n]
            return n
        for n in atoms:
            assert power(k, n) == tuple(1 - b for b in n)     # T^k = deck
            assert power(2 * k, n) == n                       # T^2k = id
        constants = {tuple([0] * k), tuple([1] * k)}
        for n in constants:
            assert T[n] == tuple(1 - b for b in n)   # pure deck, no move
        mixed = [c for c in cycles_of(T) if len(c) == 2 * k]
        assert len(mixed) == (2 ** k - 2) // (2 * k)
        print(f"    k={k}:  T^{k} = complement (the deck flip),  "
              f"T^{2 * k} = identity")
    print()
    print("  One traversal of the definitions is the deck flip; two")
    print("  traversals are the identity.  The 2k-orbits of mixed worlds")
    print("  are the unrolled double traversal -- the revision dynamics")
    print("  LIVES on the double cover -- and the constants see pure")
    print("  deck action with no transport: the phase fiber.  0059's")
    print("  stationary solutions are distributions on this cover, and")
    print("  the +/- cat states are its two sectors: deck-symmetric and")
    print("  deck-antisymmetric -- integer and half-integer 'spin'.")


# ---------------------------------------------------------------------
# 3. the holonomy ledger: joint tax = log2(order of joint traversal)
# ---------------------------------------------------------------------

def product_map(maps: list) -> dict:
    keys = list(itertools.product(*[list(m) for m in maps]))
    return {k: tuple(m[part] for m, part in zip(maps, k)) for k in keys}


def complement_map(m: int) -> dict:
    return {n: tuple(1 - b for b in n)
            for n in itertools.product((0, 1), repeat=m)}


def increment_map(w: int) -> dict:
    return {n: (n + 1) % (1 << w) for n in range(1 << w)}


def floor_bits(T: dict) -> float:
    return log2(min(len(c) for c in cycles_of(T)))


def haar_check(T: dict) -> bool:
    """The floor distribution is uniform on a smallest cycle and is
    stationary: Haar measure on a torsor of the cyclic group <T>."""
    smallest = min(cycles_of(T), key=len)
    u = {v: Fraction(1, len(smallest)) for v in smallest}
    pushed = {}
    for v, mass in u.items():
        pushed[T[v]] = pushed.get(T[v], 0) + mass
    return pushed == u


def verify_the_holonomy_ledger() -> None:
    systems = [
        ("liar x liar",
         product_map([complement_map(1), complement_map(1)]), (2, 2)),
        ("four liars", product_map([complement_map(1)] * 4), (2, 2, 2, 2)),
        ("liar x triangle",
         product_map([complement_map(1), negation_cycle_map(3)]), (2, 2)),
        ("odometer(3) x liar",
         product_map([increment_map(3), complement_map(1)]), (8, 2)),
        ("odometer(3) x odometer(2)",
         product_map([increment_map(3), increment_map(2)]), (8, 4)),
        ("odometer(4) x triangle",
         product_map([increment_map(4), negation_cycle_map(3)]), (16, 2)),
    ]
    print(f"    {'system':<28} {'clocks':>12} {'joint floor':>12}")
    for name, T, periods in systems:
        expected = 1
        for p_ in periods:
            expected = lcm(expected, p_)
        smallest = min(len(c) for c in cycles_of(T))
        assert smallest == expected, (name, smallest, expected)
        assert floor_bits(T) == log2(expected)
        assert haar_check(T), name
        shown = "lcm" + str(periods)
        print(f"    {name:<28} {shown:>12} {floor_bits(T):>9.2f} bits")
    print()
    print("  Each component paradox offers its shortest clock (the")
    print("  triangle offers its 2-loop of constants, period 2; the")
    print("  odometer only its full 2^w ring), and the JOINT tax is")
    print("  log2 of the lcm of the chosen clocks -- paradoxes")
    print("  synchronize on their shortest compatible clocks, so liars")
    print("  share one coin (the diagonal deck group), a triangle rides")
    print("  a liar for free, and two odometers cost max(w1, w2), never")
    print("  the sum.  In every case the floor distribution verifies as")
    print("  HAAR MEASURE on (a torsor of) the cyclic group the joint")
    print("  traversal generates: the forced coin is Haar on the deck")
    print("  group, and 0059's 'phase' is which sheet of the cover you")
    print("  are on.")


# ---------------------------------------------------------------------
# 4. the knot counter
# ---------------------------------------------------------------------
# A diagram is a Gauss code: a sequence of (crossing, 'O' or 'U')
# visiting each crossing exactly twice, once O and once U.

TREFOIL = [(1, 'O'), (2, 'U'), (3, 'O'), (1, 'U'), (2, 'O'), (3, 'U')]
FIGURE8 = [(1, 'O'), (2, 'U'), (3, 'O'), (4, 'U'),
           (2, 'O'), (1, 'U'), (4, 'O'), (3, 'U')]


def counter_scores(code):
    """(full-loop score, {crossing: first-return score}).  The walk
    starts AT a crossing's first visit (counted), and the first-return
    score is the running total upon arriving back at that crossing."""
    def sign(visit):
        return 1 if visit[1] == 'O' else -1
    total = sum(sign(v) for v in code)
    first_return = {}
    n = len(code)
    for start in range(n):
        crossing = code[start][0]
        score = sign(code[start])
        i = (start + 1) % n
        while code[i][0] != crossing:
            score += sign(code[i])
            i = (i + 1) % n
        if crossing not in first_return:
            first_return[crossing] = score
    return total, first_return


def interleaved(code, c1, c2):
    """Chords interleave iff exactly one visit of c2 lies between the
    two visits of c1."""
    pos = {}
    for i, (c, _) in enumerate(code):
        pos.setdefault(c, []).append(i)
    a, b = pos[c1]
    inside = sum(1 for p in pos[c2] if a < p < b)
    return inside == 1


def all_chord_diagrams(n):
    """All pairings of 2n points, with all O/U assignments."""
    def pairings(points):
        if not points:
            yield []
            return
        first = points[0]
        for j in range(1, len(points)):
            rest = points[1:j] + points[j + 1:]
            for sub in pairings(rest):
                yield [(first, points[j])] + sub
    for pairing in pairings(list(range(2 * n))):
        for over_first in itertools.product((0, 1), repeat=n):
            code = [None] * (2 * n)
            for idx, ((a, b), of) in enumerate(zip(pairing, over_first)):
                code[a] = (idx + 1, 'O' if of else 'U')
                code[b] = (idx + 1, 'U' if of else 'O')
            yield code


def verify_the_knot_counter() -> None:
    for name, code in (("trefoil", TREFOIL), ("figure-eight", FIGURE8)):
        total, first = counter_scores(code)
        assert total == 0
        print(f"    {name:<14} full loop: 0   first-return scores: "
              f"{sorted(first.values())}")
    # exhaustive identity + parity over all diagrams with <= 5 chords
    checked = gauss_even = 0
    odd_scores = True
    score_histogram = {}
    for n in (2, 3, 4, 5):
        for code in all_chord_diagrams(n):
            checked += 1
            total, first = counter_scores(code)
            assert total == 0                      # double-cover law
            # identity: score = own visit + signed interleaved visits
            pos = {}
            for i, (c, kind) in enumerate(code):
                pos.setdefault(c, []).append((i, kind))
            for c, score in first.items():
                (a, ka), (b, kb) = pos[c]
                expect = 1 if ka == 'O' else -1
                for c2, visits in pos.items():
                    if c2 == c:
                        continue
                    inside = [k for (i, k) in visits if a < i < b]
                    if len(inside) == 1:
                        expect += 1 if inside[0] == 'O' else -1
                assert score == expect, (code, c)
            if all(sum(interleaved(code, c1, c2)
                       for c2 in pos if c2 != c1) % 2 == 0
                   for c1 in pos):
                gauss_even += 1
                for s in first.values():
                    score_histogram[s] = score_histogram.get(s, 0) + 1
                    if s % 2 == 0:
                        odd_scores = False
    assert odd_scores
    print()
    print(f"    exhaustive over {checked} chord diagrams (n <= 5):")
    print(f"      full-loop score 0 in every diagram (each crossing is")
    print(f"      visited once over, once under: the diagram is its own")
    print(f"      double cover, and the second loop always cancels)")
    print(f"      first-return score = own visit + signed sum over")
    print(f"      INTERLEAVED chords -- the identity held everywhere")
    print(f"    over the {gauss_even} Gauss-even diagrams (planarity's")
    print(f"      necessary parity): score histogram "
          f"{dict(sorted(score_histogram.items()))}")
    print(f"      -- always ODD (Gauss evenness forces it), so never 0;")
    print(f"      +-1 is the balanced case, +-3 and beyond occur.")
    print()
    print("  The counter is chord-diagram INTERLACEMENT read through the")
    print("  over/under signs -- the raw combinatorial substrate of the")
    print("  finite-type (Vassiliev) invariants and of the Jones state")
    print("  sums.  Its oddness is Gauss's 1840s planarity parity, and")
    print("  its full-loop vanishing is the diagram's built-in double")
    print("  cover: every chord has two ends -- one loop to flip, two")
    print("  loops to cancel, the same Z2 as s1.")


# ---------------------------------------------------------------------
# 5. the half winding
# ---------------------------------------------------------------------

def winding(point, samples=200000, clip=0.0):
    """Total change of arg(z(t) - point) around the unit circle
    centered at i (bottom touching the origin), t in (clip, 2pi-clip)."""
    total = 0.0
    previous = None
    for s in range(samples + 1):
        t = clip + (2 * pi - 2 * clip) * s / samples
        z = 1j * (1 - cmath.exp(1j * t))
        if abs(z - point) < 1e-15:
            continue
        current = z - point
        if previous is not None:
            total += cmath.phase(current / previous)
        previous = current
    return total


def verify_the_half_winding() -> None:
    print("    winding of the circle about p_i = (-1)^i / 2^(i+1) "
          "(on the y-axis):")
    sequence = []
    for i in range(6):
        p = 1j * ((-1) ** i / 2 ** (i + 1))
        w = winding(p)
        sequence.append(round(w / (2 * pi)))
        expected = 2 * pi if i % 2 == 0 else 0.0
        assert abs(w - expected) < 1e-3, (i, w)
    print(f"      alternating, exactly as claimed: "
          f"{[s for s in sequence]} x 2*pi")
    on_curve = winding(0j, clip=1e-6)
    assert abs(on_curve - pi) < 1e-3, on_curve
    print(f"      at the limit point ON the curve (principal value): "
          f"{on_curve / pi:.6f} x pi")
    # Abel and Cesaro summation of the winding sequence 1,0,1,0,...
    abel = None
    for x in (0.9, 0.99, 0.999):
        abel = sum((-1) ** n * x ** n for n in range(10000))
    assert abs(abel - 0.5) < 1e-2
    partial = list(itertools.accumulate((-1) ** n for n in range(1000)))
    cesaro = sum(partial) / len(partial)
    assert abs(cesaro - 0.5) < 1e-2
    print(f"      Abel sum of 1-1+1-... = {abel:.4f},  "
          f"Cesaro = {cesaro:.4f}")
    print()
    print("  The regularized value of the alternating winding sequence")
    print("  (1/2, i.e. pi) EQUALS the principal-value winding at the")
    print("  boundary point.  The user's identification is exact: this")
    print("  is the Sokhotski-Plemelj half-residue -- the boundary value")
    print("  of a jump discontinuity is the average of the two sides,")
    print("  and Abel/Cesaro regularization computes exactly that")
    print("  average.  Grandi's 1/2 is not nonsense; it is the value ON")
    print("  the wall between inside and outside.")


def run_verification_suite() -> None:
    sections = [
        ("The double cover: two loops are consistent",
         verify_the_double_cover),
        ("The frame already unrolls it: T^k = deck flip",
         verify_the_frame_unrolls_it),
        ("The holonomy ledger: joint tax = log2 lcm(periods)",
         verify_the_holonomy_ledger),
        ("The knot counter: interlacement, Gauss parity, double cover",
         verify_the_knot_counter),
        ("The half winding: Grandi's 1/2 is the boundary value",
         verify_the_half_winding),
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
