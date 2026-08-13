"""Two trades at the schema wall: hide the state, or bound it.

The Parikh observation: a Parikh automaton's counters are write-only
during the run and read once at the end -- and that is exactly how the
counted tier (0034-0036, `CountedAutomaton`'s machine-enforced hiding
guard) holds unbounded state without losing decidability.  In channel
syntax the criterion is a scan:

    a channel is DANGEROUS iff it is unbounded AND some definition
    body reads it.  Unbounded + write-only  = counted tier (Parikh /
    Presburger).  Bounded + read-back = finite state.  Unbounded +
    read-back = Minsky territory.

Multiplication's carry schema is read-back by definition -- the carry
re-enters the datapath at every position -- so the two ways to trade:

  HIDE:   keep the state exact, forbid reading it until the end.
          The wall relocates from state SIZE to state FEEDBACK.
  BOUND:  keep reading, truncate the state to k bits, and accept an
          approximation.  The wall becomes an error rate.

This module measures the BOUND trade exactly:

  s2  `&` is the unique 0-state columnwise approximant of `x*y` that
      is ever exact anywhere: bit 0 forces f = AND on all four inputs.
      Its full per-bit agreement curve is measured, against all 16
      columnwise functions.
  s3  the diagonal identity: the i=j layer of the partial-product
      array is spread(x&y) -- the Frobenius of the 0-state member, so
      W1's missing name is also the shape of the best cheap guess.
  s4  the exact state cost of the p-th family member: minimal Mealy
      states of x*y mod 2^p, computed by residual classes.
  s5  the family, with its tail corrected by measurement: guaranteed
      prefix p at s4's price, and above the horizon the best tail is
      0, not & -- the diagonal anticorrelates with the carry-heavy
      mid-range.

Run directly for the verification suite.
"""

from __future__ import annotations

import itertools
import random


# ---------------------------------------------------------------------
# 1. the read-back criterion, demonstrated at its corners
# ---------------------------------------------------------------------

def verify_the_readback_criterion() -> None:
    """Write-only unbounded state is harmless; read-back is the wall.

    popcount equality needs an unbounded counter, but no step ever
    branches on it -- accumulate, compare at the end. The carry needs
    ONE bit, but every step reads it. The danger is the feedback loop,
    not the size of the memory.
    """
    width = 12
    generator = random.Random(20261103)
    for _ in range(2000):
        x = generator.randrange(1 << width)
        y = generator.randrange(1 << width)
        counter = 0                       # unbounded, write-only
        for i in range(width):
            counter += ((x >> i) & 1) - ((y >> i) & 1)
        assert (counter == 0) == (bin(x).count("1") == bin(y).count("1"))
        carry = 0                         # bounded, read every step
        total = 0
        for i in range(width):
            bit_x, bit_y = (x >> i) & 1, (y >> i) & 1
            total |= (bit_x ^ bit_y ^ carry) << i
            carry = (bit_x & bit_y) | (bit_x & carry) | (bit_y & carry)
        assert total == (x + y) % (1 << width)
    print("  popcount(x) = popcount(y): an UNBOUNDED counter, never read")
    print("  during the run -- write-only, compared once at the end. The")
    print("  counted tier's shape (0034-0036: CountedAutomaton's hiding")
    print("  guard is exactly this, machine-enforced).")
    print()
    print("  x + y: a 1-BIT carry, read at every step -- feedback.")
    print()
    print("  The classical anchors calibrate the triangle:")
    print("    unbounded, write-only   Parikh: emptiness decidable,")
    print("                            acceptance semilinear (Presburger)")
    print("    bounded, read-back      finite state: fully decidable")
    print("    unbounded, read-back    two counters with zero-tests are")
    print("                            Turing-complete (Minsky)")
    print()
    print("  So the syntactic scan of 0054 refines: a channel is")
    print("  dangerous iff it is unbounded AND some definition body")
    print("  reads it. Multiplication's schema is read-back by its own")
    print("  definition -- the carry re-enters the datapath -- which is")
    print("  WHY it is the wall, and why counting never was.")


# ---------------------------------------------------------------------
# 2. the 0-state approximants: & is forced, and measured best
# ---------------------------------------------------------------------

def columnwise(function_index: int, x: int, y: int, width: int) -> int:
    total = 0
    for i in range(width):
        column = (((x >> i) & 1) << 1) | ((y >> i) & 1)
        if (function_index >> column) & 1:
            total |= 1 << i
    return total


FUNCTION_NAMES = {0: "0", 1: "~(x|y)", 2: "y&~x", 3: "~x", 4: "x&~y",
                  5: "~y", 6: "x^y", 7: "~(x&y)", 8: "x&y", 9: "~(x^y)",
                  10: "y", 11: "x|~y", 12: "x", 13: "~y|x... ", 14: "x|y",
                  15: "Ω"}


def verify_and_is_the_zero_state_member(width=8) -> None:
    size = 1 << width
    agree = {index: [0] * width for index in range(16)}
    for x in range(size):
        for y in range(size):
            product = (x * y) & (size - 1)
            for index in range(16):
                guess = columnwise(index, x, y, width)
                match = ~(product ^ guess)
                for i in range(width):
                    agree[index][i] += (match >> i) & 1
    total_pairs = size * size
    print(f"    per-bit agreement with x*y, exhaustive {width}-bit inputs:")
    print(f"    {'f':<9}" + "".join(f"  bit{i}" for i in range(5))
          + "   mean")
    ranked = sorted(range(16), key=lambda i: -sum(agree[i]))
    for index in ranked[:5]:
        rates = [agree[index][i] / total_pairs for i in range(width)]
        name = FUNCTION_NAMES.get(index, str(index))
        print(f"    {name:<9}" + "".join(f"  {r:.2f}" for r in rates[:5])
              + f"   {sum(rates)/width:.3f}")
    best = ranked[0]
    assert best == 8, FUNCTION_NAMES.get(best)
    assert agree[8][0] == total_pairs
    for index in range(16):
        if index != 8:
            assert agree[index][0] < total_pairs
    print()
    print("  `&` (f = 8) is exact at bit 0 -- and it is FORCED: bit 0 of")
    print("  x*y is x0·y0, so a columnwise f that is always right at bit 0")
    print("  must equal AND on all four inputs. It is also the best in")
    print("  mean agreement over all bits, not just guaranteed prefix:")
    print("  the conjecture holds in both senses, uniquely.")


# ---------------------------------------------------------------------
# 3. the diagonal identity: & is the Frobenius-compressed diagonal
# ---------------------------------------------------------------------

def spread(value: int, width: int) -> int:
    total = 0
    for i in range(width):
        if (value >> i) & 1:
            total |= 1 << (2 * i)
    return total


def verify_the_diagonal_identity(width=8) -> None:
    size = 1 << width
    for x in range(size):
        for y in range(size):
            diagonal = sum(((x >> i) & 1) * ((y >> i) & 1) * (1 << (2 * i))
                           for i in range(width))
            assert diagonal == spread(x & y, width)
    print("  the i = j layer of the partial-product array is")
    print()
    print("      Σ x_i·y_i·4^i  =  spread(x & y)  =  F(x & y)")
    print()
    print("  -- the Frobenius of the 0-state member. `&` is the best")
    print("  0-bit guess BECAUSE it is the diagonal: below bit 1 there")
    print("  are no cross terms (first at bit 1) and no carries (first")
    print("  at bit 2), so the diagonal is all there is, and the")
    print("  operator 0053 could not name (W1) is also the shape of the")
    print("  cheapest approximation.")


# ---------------------------------------------------------------------
# 4. the exact state cost of the p-th member
# ---------------------------------------------------------------------

def minimal_states_mod(precision: int) -> int:
    """Minimal Mealy states of (x, y) -> x*y mod 2^p, read LSB-first.

    A state is a residual: the map from all future input tails to all
    future output bits. Outputs above p-1 are 0, so a horizon of p
    suffices and the count is exact.
    """
    horizon = precision + 1
    tails = [(tx, ty) for tx in range(1 << horizon)
             for ty in range(1 << horizon)]
    mask = (1 << precision) - 1
    signatures = set()
    for length in range(precision + 2):
        for low_x in range(1 << length):
            for low_y in range(1 << length):
                signature = tuple(
                    (((low_x | (tx << length)) *
                      (low_y | (ty << length))) & mask) >> length
                    for tx, ty in tails)
                signatures.add(signature)
        if length > precision:
            break
    return len(signatures)


def verify_the_state_cost(limit=4) -> None:
    print("    p (exact low bits)   minimal Mealy states   log2")
    costs = []
    for precision in range(1, limit + 1):
        count = minimal_states_mod(precision)
        costs.append(count)
        from math import log2
        print(f"    {precision:>18}   {count:>20}   {log2(count):>5.1f}")
    assert all(second > first for first, second in zip(costs, costs[1:]))
    print()
    print("  The family's price list, exact -- and CHEAPER than expected:")
    print("  0054's bound says the full product needs 2p state bits for p")
    print("  bits of precision, but the truncated task (don't-care above")
    print("  the horizon) collapses residuals to ~1.2 bits of state per")
    print("  guaranteed bit at these sizes. Approximation buys a real")
    print("  discount on the wall's price, not just a cutoff.")


# ---------------------------------------------------------------------
# 5. the family A_p: exact below the horizon, & above
# ---------------------------------------------------------------------

def verify_the_family(width=8) -> None:
    """Two tails above the exact horizon, measured against each other.

    The conjecture guessed `& above the horizon`. Measurement says the
    better tail is 0: above bit 1 the cross terms dominate and the
    diagonal hurts more than it helps -- even the constant 0 agrees
    with x*y's high bits more often than & does. So `&` is optimal
    exactly where the conjecture put it, as the POSITION-UNIFORM
    (1-state) member; the p-th member is the plain mod-2^p multiplier,
    at s4's price.
    """
    size = 1 << width
    print(f"    {'p':>3} {'guaranteed':>11} {'mean, 0-tail':>13} "
          f"{'mean, &-tail':>13}")
    for precision in (0, 1, 2, 4, 6):
        mask = (1 << precision) - 1
        agree_zero = agree_and = 0
        guaranteed = width
        for x in range(size):
            for y in range(size):
                product = (x * y) & (size - 1)
                zero_tail = product & mask
                and_tail = zero_tail | ((x & y) & ~mask & (size - 1))
                agree_zero += bin(~(product ^ zero_tail)
                                  & (size - 1)).count("1")
                agree_and += bin(~(product ^ and_tail)
                                 & (size - 1)).count("1")
                for candidate in (zero_tail, and_tail):
                    difference = product ^ candidate
                    if difference:
                        low = (difference & -difference).bit_length() - 1
                        guaranteed = min(guaranteed, low)
        total_bits = size * size * width
        print(f"    {precision:>3} {guaranteed:>11} "
              f"{agree_zero / total_bits:>13.3f} "
              f"{agree_and / total_bits:>13.3f}")
    print()
    print("  Guaranteed prefix tracks p exactly (both tails). In mean")
    print("  agreement the 0-tail wins from p >= 2: the &-tail's diagonal")
    print("  bits are anticorrelated with the carry-heavy mid-range. The")
    print("  corrected family:")
    print("    1 state        &            1 bit guaranteed, best uniform")
    print("    s4's price     x*y mod 2^p  p bits guaranteed, best tail 0")
    print("  The conjecture's shape survives -- one member per carry")
    print("  length, & at the bottom -- with the tail corrected by the")
    print("  measurement.")


def run_verification_suite() -> None:
    sections = [
        ("The read-back criterion", verify_the_readback_criterion),
        ("`&` is the 0-state member, forced and measured",
         verify_and_is_the_zero_state_member),
        ("The diagonal identity", verify_the_diagonal_identity),
        ("The exact state cost of the p-th member",
         verify_the_state_cost),
        ("The family A_p", verify_the_family),
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
