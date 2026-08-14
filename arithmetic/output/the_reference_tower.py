"""The reference tower: gauge-fixing costs the tax, forever.

Thread 3: if the absolute sheet is gauge (0063), fixing the gauge
means adding a reference -- and the fourth-bucket question ("true but
inexpressibly so") becomes the statement that the reference itself
always re-opens a sheet.

  s1  GAUGE-FIXING WORKS AND COSTS EXACTLY THE TAX.  m liars plus
      one reference liar: every bit-relative-to-reference is an
      invariant, EXACT observable in every floor solution ("absolute
      in the reference gauge"), and the whole system's floor is
      still 1 bit -- the reference's own coin.  Gauge-fixing
      converts all m relative bits to definite values at the price
      of the tax, paid once per world.

  s2  THE TOWER NEVER CLOSES.  Adding more references never reaches
      0 bits: the floor is 1 bit for every m -- each new reference
      has no sheet of its own to stand on.  This is the frame's
      shape of iterated incompleteness: adding the axiom "the
      intended sheet is THIS one" produces a system with its own
      undecided sheet (PA -> PA+Con(PA) -> ...).

  s3  THE FOUR BUCKETS.  Toy theory = the hexagon (double cover of
      the triangle); models = its two global solutions; the
      language's observables = deck-invariant functions.  Every
      statement classifies by its truth across the two models:
          decided-true      true in both        (provable)
          decided-false     false in both       (refutable)
          independent       true in exactly one (the fourth bucket)
      and the deck transformation is a BIJECTION between the
      independent-true-in-A and independent-true-in-B classes:
      every independent statement has a dual, and a statement is
      decided IFF it is deck-invariant.  All 12 literals ("vertex i
      has value v") are independent; all parity statements are
      decided.  "True but inexpressibly so" = true on the intended
      sheet, where "intended" is not deck-invariant and therefore
      not a statement of the language.

  s4  GUARDED LOOPS CARRY NO HOLONOMY.  The odd-negation loop WITH
      a guard, n := NOT a(n), has a one-point core (a unique
      attracting solution) at every width -- depth kills holonomy.
      Paradox needs the loop to close at the SAME level: depth-0
      syntax (the liar) or the boundary at infinity (read-back, h).
      This is the user's "every finite cycle is even" made precise:
      finite guarded travel always descends, so it cannot come back
      odd; the boundary is where loops close.

Run directly for the verification suite.
"""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction
from math import log2

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from lossy_revision_and_the_carry import cycles_of


# ---------------------------------------------------------------------
# 1-2. gauge-fixing and the tower
# ---------------------------------------------------------------------

def liars_map(m: int) -> dict:
    return {n: tuple(1 - b for b in n)
            for n in itertools.product((0, 1), repeat=m)}


def verify_the_reference_gauge() -> None:
    print(f"    {'liars m':>8} {'+ references':>13} {'floor':>7} "
          f"{'relative bits exact':>20}")
    for m in (1, 2, 3, 4):
        for refs in (1, 2):
            T = liars_map(m + refs)
            orbits = cycles_of(T)
            assert all(len(o) == 2 for o in orbits)
            floor = log2(min(len(o) for o in orbits))
            assert floor == 1.0
            # in every floor solution every XOR-with-reference is exact
            for orbit in orbits:
                for i in range(m):
                    rel = {a[i] ^ a[m] for a in orbit}   # vs reference 0
                    assert len(rel) == 1
            print(f"    {m:>8} {refs:>13} {floor:>5.0f} b "
                  f"{'all ' + str(m) + ' of them':>20}")
    print()
    print("  Fixing the gauge works: relative-to-reference values are")
    print("  exact in every floor solution -- and costs exactly the")
    print("  1-bit tax, once per world, no matter how many liars it")
    print("  covers.  Adding MORE references never reduces the floor:")
    print("  the new reference has no sheet of its own to stand on.")
    print("  The tower never closes -- the frame's iterated")
    print("  incompleteness (fix the sheet by axiom; the fixed system")
    print("  has a fresh undecided sheet).")


# ---------------------------------------------------------------------
# 3. the four buckets
# ---------------------------------------------------------------------

def verify_the_four_buckets() -> None:
    k = 3
    cover = [v for v in itertools.product((0, 1), repeat=2 * k)
             if all(v[i] != v[(i + 1) % (2 * k)] for i in range(2 * k))]
    A, B = cover
    deck = lambda v: tuple(v[(i + k) % (2 * k)] for i in range(2 * k))
    assert deck(A) == B and deck(B) == A
    # statements = arbitrary properties; classify literals and parities
    literals = [(i, val) for i in range(2 * k) for val in (0, 1)]
    independent = decided = 0
    for i, val in literals:
        in_a, in_b = A[i] == val, B[i] == val
        assert in_a != in_b                       # every literal splits
        independent += 1
    # deck-duality: the dual literal is true in the other model
    for i, val in literals:
        j = (i + k) % (2 * k)
        assert (A[i] == val) == (B[j] == val)     # dual pair swaps
    parity_pairs = [(i, j) for i in range(2 * k)
                    for j in range(i + 1, 2 * k)]
    for i, j in parity_pairs:
        stmt_a = (A[i] ^ A[j])
        stmt_b = (B[i] ^ B[j])
        assert stmt_a == stmt_b                   # parities decided
        decided += 1
    print(f"    two models (the hexagon's two solutions), deck-swapped:")
    print(f"      all {independent} literals: independent "
          f"(true in exactly one model),")
    print(f"        and the deck maps each to its dual in the other")
    print(f"      all {decided} pairwise parities: decided "
          f"(same truth in both)")
    print()
    print("  A statement is DECIDED iff it is deck-invariant; the")
    print("  independent statements come in dual pairs swapped by the")
    print("  deck.  The fourth bucket -- 'true, but inexpressibly so'")
    print("  -- is truth on the intended sheet, where 'intended' is")
    print("  not deck-invariant and hence not a statement of the")
    print("  language.  Provable = true on every sheet; the Goedel")
    print("  sentence is a relative bit read as if it were absolute.")


# ---------------------------------------------------------------------
# 4. guarded loops carry no holonomy
# ---------------------------------------------------------------------

def verify_guards_kill_holonomy() -> None:
    print(f"    {'width':>6} {'core of  n := NOT a(n)':>24} "
          f"{'holonomy':>9}")
    for w in (4, 6, 8):
        mask = (1 << w) - 1
        T = {v: (~(2 * v)) & mask for v in range(1 << w)}
        cyc = cycles_of(T)
        assert len(cyc) == 1 and len(cyc[0]) == 1   # one-point core
        print(f"    {w:>6} {'single fixed point':>24} {'none':>9}")
    print()
    print("  An ODD-negation loop with a guard contracts to a unique")
    print("  solution: depth kills holonomy, at every width.  A loop")
    print("  only carries holonomy if it closes at the SAME level --")
    print("  depth-0 syntax (the liar's direct self-reference) or the")
    print("  boundary at infinity (read-back through h, 0054/0055).")
    print("  Finite guarded travel always descends: it cannot come")
    print("  back odd.  Goedel's diagonal sentence closes its loop")
    print("  through an unbounded proof-search -- through the boundary")
    print("  -- which is why the obstruction lives there and is a")
    print("  cliff (0057): holonomy is a class, not a quantity, and no")
    print("  finite stage carries a fraction of it.")


def run_verification_suite() -> None:
    sections = [
        ("Gauge-fixing works and costs exactly the tax; the tower "
         "never closes", verify_the_reference_gauge),
        ("The four buckets", verify_the_four_buckets),
        ("Guarded loops carry no holonomy", verify_guards_kill_holonomy),
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
