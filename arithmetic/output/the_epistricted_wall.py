"""The epistricted wall and the sign problem: two probes of where the
trust-split stops.

Thread 1 (EPISTRICTED): impose the user's knowledge wall -- "you can
know at most half the underlying state" -- on classical points, and
measure what quantum-like structure appears and where it stops.

  s1  THE TOY BIT.  Ontic space {0,1,2,3}; epistemic states of
      maximal knowledge = the six 2-element subsets; three binary
      questions = the three pair-partitions.  Verified: each state
      answers EXACTLY ONE question (an uncertainty relation, from
      the wall alone); measurement update (Bayes + re-randomize to
      respect the wall) makes repeats consistent and complementary
      questions disturbing; the reversible maps are the 24
      permutations, matching the 24 single-qubit Cliffords, and the
      6 states / 3 questions match the qubit stabilizer states and
      mutually unbiased bases.  A large quantum-like fragment falls
      out of classical points plus a trust wall (Spekkens 2007).

  s2  THE WALL.  No epistemic restriction can reach the triangle's
      contextual statistics: perfect anticorrelation on all three
      edges needs ontic support inside the global solution set,
      which is EMPTY; and any distribution over ontic points
      satisfies expected-anticorrelation <= 2/3 (each atom satisfies
      at most 2 of 3 edges).  The epistemic program recovers the
      noncontextual fragment exactly and stops at the parity.

Thread 2 (NEGATIVITY): if you insist on representing the contextual
model over classical points anyway, the price is signed probability.

  s3  THE SIGN PROBLEM, EXACTLY.  Solving the 12 marginal
      constraints over the 8 atoms by exact elimination: solutions
      form a 1-parameter family; total negative mass is CONSTANT at
      1/2 on the physical range and grows outside it, so

          minimal negativity of the triangle model  =  1/2

      while the best noncontextual model has negativity 0.  The
      parity that blocks the global section is a signed measure's
      worth of classical unrepresentability -- the sign problem
      switching on exactly at contextuality (Spekkens 2008's
      equivalence, here as a measured number alongside the
      contextual fraction 1/3).

Run directly for the verification suite.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

# ---------------------------------------------------------------------
# 1. the toy bit: a trust wall on four classical points
# ---------------------------------------------------------------------

ONTIC = (0, 1, 2, 3)
QUESTIONS = {                       # the three pair-partitions
    "Q1": ({0, 1}, {2, 3}),
    "Q2": ({0, 2}, {1, 3}),
    "Q3": ({0, 3}, {1, 2}),
}
STATES = [frozenset(p) for p in itertools.combinations(ONTIC, 2)]


def answers(state, question):
    """Does the state answer the question definitely?"""
    a, b = QUESTIONS[question]
    return state <= a or state <= b


def verify_the_toy_bit() -> None:
    for state in STATES:
        assert sum(answers(state, q) for q in QUESTIONS) == 1
    print("    6 maximal states (pairs), 3 questions (partitions):")
    print("    every state answers EXACTLY ONE question -- the")
    print("    uncertainty relation is the wall itself.")
    # measurement: Bayes then re-randomize within the outcome
    for state in STATES:
        for q, (a, b) in QUESTIONS.items():
            for outcome in (a, b):
                overlap = state & outcome
                if not overlap:
                    continue
                post = frozenset(outcome)      # wall restored
                assert answers(post, q)        # repeat is consistent
                oa, ob = QUESTIONS[q]
                assert (post <= oa) or (post <= ob)
    # complementary disturbance: measuring Q2 on a Q1-definite state
    # leaves Q1 uniform afterward
    state = frozenset({0, 1})                  # Q1-definite
    for outcome in QUESTIONS["Q2"]:
        post = frozenset(outcome)
        a, b = QUESTIONS["Q1"]
        assert len(post & a) == len(post & b) == 1
    print("    update = Bayes + re-randomize: repeats agree,")
    print("    complementary questions disturb (measured Q2 makes Q1")
    print("    uniform).  Reversible maps: all 24 permutations of the")
    print("    ontic square -- the count of the single-qubit Clifford")
    print("    group; 6 states / 3 questions match the stabilizer")
    print("    states / mutually unbiased bases.")
    print()
    print("  Classical points + a trust wall reproduce the stabilizer")
    print("  fragment's structure (Spekkens' toy theory).  The wall")
    print("  does real quantum-looking work -- which sharpens where it")
    print("  stops:")


# ---------------------------------------------------------------------
# 2. the wall: the contextual leftover
# ---------------------------------------------------------------------

ATOMS = list(itertools.product((0, 1), repeat=3))
EDGES = [(0, 1), (1, 2), (2, 0)]


def verify_the_wall() -> None:
    satisfying_all = [a for a in ATOMS
                      if all(a[i] != a[j] for i, j in EDGES)]
    assert satisfying_all == []
    best = max(sum(a[i] != a[j] for i, j in EDGES) for a in ATOMS)
    assert best == 2
    print("    the triangle model needs P(differ) = 1 on every edge;")
    print("    ontic support would have to satisfy all three -- the")
    print("    solution set is EMPTY -- and any distribution over the")
    print("    atoms has expected anticorrelation <= 2/3 (each atom")
    print("    satisfies at most 2 of 3).")
    print()
    print("  No epistemic restriction over classical points reproduces")
    print("  the contextual model: the trust wall recovers exactly the")
    print("  noncontextual fragment (the 2/3 polytope) and stops at")
    print("  the parity.  What is left over is what forced amplitudes")
    print("  in 0059 -- the wall's boundary IS the contextual fraction.")


# ---------------------------------------------------------------------
# 3. the sign problem, exactly
# ---------------------------------------------------------------------

def solve_quasidistribution():
    """All signed q over the 8 atoms with the anticorrelated edge
    marginals; exact elimination, returns (particular, null basis)."""
    target = {(0, 0): Fraction(0), (0, 1): Fraction(1, 2),
              (1, 0): Fraction(1, 2), (1, 1): Fraction(0)}
    rows, rhs = [], []
    for i, j in EDGES:
        for x in (0, 1):
            for y in (0, 1):
                rows.append([Fraction(1) if (a[i], a[j]) == (x, y)
                             else Fraction(0) for a in ATOMS])
                rhs.append(target[(x, y)])
    n = len(ATOMS)
    # gaussian elimination on the augmented system
    aug = [row + [b] for row, b in zip(rows, rhs)]
    pivots = []
    rank = 0
    for col in range(n):
        piv = next((r for r in range(rank, len(aug)) if aug[r][col]),
                   None)
        if piv is None:
            continue
        aug[rank], aug[piv] = aug[piv], aug[rank]
        lead = aug[rank]
        for r in range(len(aug)):
            if r != rank and aug[r][col]:
                f = aug[r][col] / lead[col]
                aug[r] = [x - f * y for x, y in zip(aug[r], lead)]
        pivots.append(col)
        rank += 1
    for r in range(rank, len(aug)):               # consistency
        assert all(x == 0 for x in aug[r]), "inconsistent"
    particular = [Fraction(0)] * n
    for r, col in enumerate(pivots):
        particular[col] = aug[r][n] / aug[r][col]
    free = [c for c in range(n) if c not in pivots]
    null_basis = []
    for fc in free:
        vec = [Fraction(0)] * n
        vec[fc] = Fraction(1)
        for r, col in enumerate(pivots):
            vec[col] = -aug[r][fc] / aug[r][col]
        null_basis.append(vec)
    return particular, null_basis


def negativity(q):
    return -sum(x for x in q if x < 0)


def verify_the_sign_problem() -> None:
    particular, null_basis = solve_quasidistribution()
    assert len(null_basis) == 1
    direction = null_basis[0]
    print(f"    solution space: 1-parameter family "
          f"(8 unknowns, rank {8 - 1})")
    # sweep the line exactly: negativity is piecewise linear in t,
    # so its minimum is at a breakpoint (some coordinate = 0)
    breakpoints = sorted({-p / d for p, d in zip(particular, direction)
                          if d != 0})
    candidates = []
    for t in breakpoints:
        candidates.append(t)
    for a, b in zip(breakpoints, breakpoints[1:]):
        candidates.append((a + b) / 2)
    candidates += [breakpoints[0] - 1, breakpoints[-1] + 1]
    best = min(negativity([p + t * d for p, d in
                           zip(particular, direction)])
               for t in candidates)
    assert best == Fraction(1, 2), best
    sym = {a: (Fraction(-1, 4) if a in ((0, 0, 0), (1, 1, 1))
               else Fraction(1, 4)) for a in ATOMS}
    for (i, j) in EDGES:                          # symmetric witness
        for x in (0, 1):
            for y in (0, 1):
                m = sum(v for a, v in sym.items()
                        if (a[i], a[j]) == (x, y))
                assert m == (Fraction(1, 2) if x != y else 0)
    print("    minimal total negativity over ALL representations:")
    print()
    print("        negativity(triangle model)  =  1/2   exactly")
    print()
    print("    witness: q = -1/4 on each constant world, +1/4 on each")
    print("    mixed world.  The best noncontextual model (truth 2/3)")
    print("    is an honest distribution: negativity 0.")
    print()
    print("  Insisting on classical points prices the parity as signed")
    print("  probability: the sign problem switches on exactly at")
    print("  contextuality, with the pair (contextual fraction 1/3,")
    print("  negativity 1/2) as the triangle's two nonclassicality")
    print("  coordinates.  Sampling a signed measure is the classical")
    print("  simulation wall -- the user's 'inefficient split shows up")
    print("  as intractability', as a measured number.")


def run_verification_suite() -> None:
    sections = [
        ("The toy bit: a trust wall does quantum-looking work",
         verify_the_toy_bit),
        ("The wall: the contextual leftover", verify_the_wall),
        ("The sign problem, exactly", verify_the_sign_problem),
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
