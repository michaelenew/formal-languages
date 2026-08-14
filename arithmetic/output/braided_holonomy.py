"""Braided holonomy: where the frame's commutativity breaks.

Thread 4: every paradox so far had CYCLIC holonomy (one traversal
generates everything; 0060 proved a single causal channel can do
nothing else).  Two reference loops through a SHARED channel change
that: their monodromies need not commute, and three new phenomena
appear, all verified.

  s1  THE GROUP TAX.  With two loops of monodromies sigma, tau on a
      shared fiber, revision (pick a loop at random, apply it) is a
      doubly stochastic chain whose stationary space is exactly the
      mixtures of uniforms on the orbits of the GENERATED GROUP
      <sigma, tau> -- verified by exact elimination.  The tax
      formula generalizes verbatim:

          forced entropy = log2(smallest orbit of <sigma, tau>)

      e.g. sigma=(01), tau=(12) on a 3-value channel: <sigma,tau> =
      S3, transitive, tax = log2 3 = 1.585 bits.

  s2  ORDER BECOMES OBSERVABLE.  Auditing loop A then B differs
      from B then A by the commutator [sigma, tau]; for the S3 pair
      the commutator is a 3-cycle -- a deterministic, state-
      independent discrepancy.  For any abelian pair (all of
      0059-0063) the residue is the identity: parity was the ONLY
      path-memory.  Noncommuting loops remember the WORD, not just
      its length mod 2 -- the frame's first genuinely braided
      path-dependence, the permutation shadow of anyons.

  s3  BINARY CHANNELS CANNOT BRAID; A SHARED 2-BIT CHANNEL CAN.
      All monodromies of a 1-bit channel live in S2 (abelian), so
      braiding needs a fiber of >= 3 values: the minimal braided
      systems are two loops through one 2-bit channel (verified:
      swap and flip generate the dihedral group, tax 2 bits,
      nontrivial commutator).  Single causal channels are cyclic
      (0060); one shared multi-bit channel with two loops is where
      the frame's holonomy first fails to commute.

Run directly for the verification suite.
"""

from __future__ import annotations

import itertools
from fractions import Fraction
from math import log2


def compose(p, q):
    """(p after q) as tuples: apply q first."""
    return tuple(p[q[i]] for i in range(len(p)))


def generated_group(generators):
    frontier = {tuple(range(len(generators[0])))}
    group = set(frontier)
    while frontier:
        nxt = set()
        for g in frontier:
            for gen in generators:
                h = compose(gen, g)
                if h not in group:
                    group.add(h)
                    nxt.add(h)
        frontier = nxt
    return group


def orbits_of_group(group, n):
    seen, out = set(), []
    for start in range(n):
        if start in seen:
            continue
        orbit = {g[start] for g in group}
        seen |= orbit
        out.append(orbit)
    return out


def stationary_dimension_of_chain(generators, n):
    """Exact nullity of (P - I) for the uniform-choice chain."""
    m = len(generators)
    rows = []
    for s in range(n):
        row = [Fraction(0)] * n
        row[s] -= 1
        for gen in generators:
            for t in range(n):
                if gen[t] == s:
                    row[t] += Fraction(1, m)
        rows.append(row)
    rank = 0
    for col in range(n):
        piv = next((r for r in range(rank, n) if rows[r][col]), None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        lead = rows[rank]
        for r in range(n):
            if r != rank and rows[r][col]:
                f = rows[r][col] / lead[col]
                rows[r] = [x - f * y for x, y in zip(rows[r], lead)]
        rank += 1
    return n - rank


def verify_the_group_tax() -> None:
    cases = [
        ("sigma=(01), tau=(12) on 3", [(1, 0, 2), (0, 2, 1)], 3),
        ("swap, flip0 on 2 bits", [(0, 2, 1, 3), (1, 0, 3, 2)], 4),
        ("flip0, flip1 (abelian) on 2 bits",
         [(1, 0, 3, 2), (2, 3, 0, 1)], 4),
    ]
    print(f"    {'loops':<36} {'|group|':>8} {'orbits':>7} "
          f"{'tax (bits)':>11}")
    for name, gens, n in cases:
        group = generated_group(gens)
        orbs = orbits_of_group(group, n)
        assert stationary_dimension_of_chain(gens, n) == len(orbs)
        tax = log2(min(len(o) for o in orbs))
        print(f"    {name:<36} {len(group):>8} {len(orbs):>7} "
              f"{tax:>11.3f}")
    print()
    print("  Stationary beliefs of two-loop revision = mixtures of")
    print("  uniforms on the orbits of the GENERATED group (exact")
    print("  elimination agrees with the orbit count in every case),")
    print("  so the tax law generalizes verbatim: forced entropy =")
    print("  log2(smallest orbit of <sigma, tau>).  The S3 pair taxes")
    print("  log2 3 = 1.585 bits -- Haar on a nonabelian group's")
    print("  orbit, the first non-cyclic coin.")


def verify_order_observability() -> None:
    sigma, tau = (1, 0, 2), (0, 2, 1)
    ab = compose(tau, sigma)                     # audit A then B
    ba = compose(sigma, tau)                     # audit B then A
    assert ab != ba
    commutator = compose(compose(sigma, tau),
                         compose(sigma, tau))    # (st)^2 since s,t inv
    stst = compose(compose(sigma, tau), compose(sigma, tau))
    assert stst != tuple(range(3))               # [sigma,tau] = 3-cycle
    print(f"    A-then-B sends states to {ab}; B-then-A to {ba}:")
    print(f"    a deterministic, state-independent discrepancy; the")
    print(f"    commutator is the 3-cycle {stst}.")
    flip0, flip1 = (1, 0, 3, 2), (2, 3, 0, 1)
    assert compose(flip0, flip1) == compose(flip1, flip0)
    print(f"    the abelian pair's residue is the identity: in every")
    print(f"    system of 0059-0063 the only path-memory was parity.")
    print()
    print("  Noncommuting loops remember the WORD of the traversal,")
    print("  not just its length mod 2: path-dependence beyond parity")
    print("  -- the permutation shadow of braiding.  (True anyonic")
    print("  braiding adds phases on top: the amplitude level of this,")
    print("  as 0059 s5 was to the liar.)")


def verify_where_binary_fails() -> None:
    # every pair of permutations of a 2-element fiber commutes
    perms2 = list(itertools.permutations(range(2)))
    assert all(compose(p, q) == compose(q, p)
               for p in perms2 for q in perms2)
    # and a 3-element fiber already braids (s1); minimal in bits:
    # one shared 2-bit channel, loops acting as swap and flip
    swap, flip = (0, 2, 1, 3), (1, 0, 3, 2)
    assert compose(swap, flip) != compose(flip, swap)
    group = generated_group([swap, flip])
    assert len(group) == 8                        # dihedral D4
    print("    1-bit fibers: all monodromies commute (S2 is abelian) --")
    print("    no binary channel pair can braid.")
    print("    2-bit shared fiber: swap + flip generate D4 (order 8),")
    print("    noncommuting -- the minimal braided system is two loops")
    print("    through ONE shared 2-bit channel.")
    print()
    print("  0060 proved single causal channels are cyclic; this locates")
    print("  the exact door: braiding enters with the SECOND loop")
    print("  through a shared multi-valued channel, and not before.")


def run_verification_suite() -> None:
    sections = [
        ("The group tax", verify_the_group_tax),
        ("Order becomes observable", verify_order_observability),
        ("Where binary fails and braiding begins",
         verify_where_binary_fails),
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
