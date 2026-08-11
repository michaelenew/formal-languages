"""T re-expressed: it is not a new series, it is `U` in a mirror.

The corpus's `$`/`T` is the trailing-ones mask, defined as the
intersection series `x & b(x) & b(b(x)) & ...` with `b(y) = 2y + 1`.
Asked: re-express it in elementary terms and see whether other
primitives reconstruct it. Two reconstructions, and they say different
things.

**1. With addition, a finite term.**

    T(x) = x & neg(x + 1)

No series at all. But it is circular with the successor, which the
corpus defines the other way round as `succ(x) = x ^ b(T x)`, so
**T and succ are interdefinable and neither is prior** -- each is a
two-symbol term in the other.

**2. With the up-closure, no new operator at all.** The bridge is one
identity between the two shifts:

    neg(b(y)) = s(neg(y))            b and a are complement-conjugate

De Morgan then turns the intersection series into the union series:

    T(x) = neg(U(neg x))             U(x) = x | s(x) | s(s(x)) | ...

So `$` and the union-series of 0039 are **one operator seen through
complement**, and every law of one is a law of the other:

    U(x) = x | s(U x)                T(x) = x & b(T x)          fixpoints
    U(x) ^ s(U x) = lowest SET bit   T(x) ^ b(T x) = lowest ZERO bit

The second pair extends 0039's telescoping family with its `T` member,
which is what canonicalising `T` most directly needs: `T ^ b(T)` is what
the series measures, and it measures the lowest zero.

**3. And no finite term over the shift alone reaches it.** Bit `i` of
`T(x)` depends on bits `0..i` of `x` -- measured -- while a term of
shift-depth `d` reaches only `i-d..i`. So `T` needs either `+` or a
series, exactly as 0002's locality argument says.

**4. The canonicalisation payoff.** 0040 showed the tiles over
`{x, s(x), ...}` are the windows of `x`'s bit string. The same holds for
`T`'s own symbols `{x, b(x), ...}` -- they are the windows of `x` read
with **ones** padding the bottom instead of zeros, because `b` fills
with ones where `s` fills with zeros. So `T` inherits 0040's whole
analysis unchanged: tiles are de Bruijn states, the realisable set is
the runs, and the canonical object is the same automaton with one
convention flipped.

Run directly for the verification suite.
"""

from __future__ import annotations

from itertools import product as cartesian_product

WIDTH = 12
MASK = (1 << WIDTH) - 1
SAFE = range(1 << (WIDTH - 1))          # room for one shift, no truncation

shift = lambda value: (value << 1) & MASK               # a(x) = 2x
shift_one = lambda value: ((value << 1) | 1) & MASK     # b(x) = 2x+1
negate = lambda value: MASK ^ value
join = lambda left, right: left ^ right ^ (left & right)
successor = lambda value: (value + 1) & MASK
lowest_set = lambda value: value & -value
lowest_zero = lambda value: lowest_set(negate(value))


def trailing_ones(value: int) -> int:
    """The corpus's T / $ : x & b(x) & b(b(x)) & ..."""
    total, lifted = value, value
    for _ in range(WIDTH):
        lifted = shift_one(lifted)
        total &= lifted
    return total


def up_closure(value: int) -> int:
    """U : x | s(x) | s(s(x)) | ..."""
    total, lifted = value, value
    for _ in range(WIDTH):
        lifted = shift(lifted)
        total = join(total, lifted)
    return total


def _check(label: str, statement) -> None:
    failures = [value for value in SAFE if statement(value) != 0]
    assert not failures, (label, failures[:3])
    print(f"  {label:<48} holds")


# ---------------------------------------------------------------------
# 1. elementary, with addition
# ---------------------------------------------------------------------

def verify_the_elementary_form() -> None:
    _check("T(x) ^ (x & neg(x+1))              elementary",
           lambda v: trailing_ones(v) ^ (v & negate(successor(v))))
    _check("succ(x) ^ (x ^ b(T x))             corpus's succ",
           lambda v: successor(v) ^ (v ^ shift_one(trailing_ones(v))))
    print("    So T is a finite term once `+` is available, and succ is a "
          "finite term")
    print("    once T is. **T and succ are interdefinable and neither is "
          "prior** -- the")
    print("    corpus derives succ from T, and this derives T from succ, "
          "each in two")
    print("    symbols.")


# ---------------------------------------------------------------------
# 2. the duality: T is U in a mirror
# ---------------------------------------------------------------------

def verify_the_duality() -> None:
    _check("neg(b(y)) ^ s(neg y)               the bridge",
           lambda v: negate(shift_one(v)) ^ shift(negate(v)))
    _check("T(x) ^ neg(U(neg x))               T is U dualised",
           lambda v: trailing_ones(v) ^ negate(up_closure(negate(v))))
    print("    `b` and `a` are complement-conjugate, so De Morgan turns "
          "the intersection")
    print("    series into the union series. `$` and 0039's U are ONE "
          "operator.")
    print()
    _check("U(x) ^ (x | s(U x))                U's fixpoint",
           lambda v: up_closure(v) ^ join(v, shift(up_closure(v))))
    _check("T(x) ^ (x & b(T x))                T's fixpoint",
           lambda v: trailing_ones(v) ^ (v & shift_one(trailing_ones(v))))
    _check("U(x) ^ s(U x) ^ lowest-set-bit(x)  U telescopes",
           lambda v: (up_closure(v) ^ shift(up_closure(v))
                      ^ lowest_set(v)))
    _check("T(x) ^ b(T x) ^ lowest-zero-bit(x) T telescopes",
           lambda v: (trailing_ones(v) ^ shift_one(trailing_ones(v))
                      ^ lowest_zero(v)))
    print("    Every law of one is a law of the other. The last line is "
          "0039's")
    print("    telescoping family gaining its T member: `T ^ b(T)` is "
          "what the series")
    print("    measures, and it measures the lowest ZERO -- the mirror of "
          "U's lowest set.")


# ---------------------------------------------------------------------
# 3. no finite shift-term reaches T
# ---------------------------------------------------------------------

def verify_no_finite_shift_term(position: int = 6) -> None:
    depends = [source for source in range(WIDTH)
               if any((trailing_ones(v) >> position & 1)
                      != (trailing_ones(v ^ (1 << source)) >> position & 1)
                      for v in SAFE)]
    assert depends == list(range(position + 1)), depends
    print(f"  bit {position} of T(x) depends on x's bits {depends}")
    print("    -- every bit at or below it. A term of shift-depth d "
          "reaches only bits")
    print("    i-d .. i, so no finite term over {^, &, <<} matches T. It "
          "needs `+` or a")
    print("    series, which is 0002's locality argument arriving on the "
          "term side.")


# ---------------------------------------------------------------------
# 4. T's tiles are windows too, with ones padding
# ---------------------------------------------------------------------

def tile(polarity: tuple, value: int, lifter) -> int:
    region, lifted = MASK, value
    for chosen in polarity:
        region &= lifted if chosen else negate(lifted)
        lifted = lifter(lifted)
    return region


def windows(value: int, length: int, padding: int) -> set:
    def bit(position: int) -> int:
        if position < 0:
            return padding
        return (value >> position) & 1 if position < WIDTH else 0
    return {tuple(bit(index - offset) for offset in range(length))
            for index in range(WIDTH)}


def verify_T_tiles_are_windows() -> None:
    for length in (2, 3, 4):
        polarities = list(cartesian_product((0, 1), repeat=length))
        failures = [
            value for value in range(1 << (WIDTH - length))
            if {p for p in polarities if tile(p, value, shift_one)}
            != windows(value, length, padding=1)]
        assert not failures, (length, failures[:3])
        print(f"  n = {length}:  tiles over {{x, b(x), ...}} are the "
              f"length-{length} windows of x, ones-padded")
    print("    `b` fills with ones where `a` fills with zeros, so T's "
          "tiles are 0040's")
    print("    windows with the bottom padding flipped. T therefore "
          "inherits 0040 whole:")
    print("    tiles are de Bruijn states, the realisable set is the "
          "runs, and the")
    print("    canonical object is the same automaton with one "
          "convention changed.")


def run_verification_suite() -> None:
    print("=" * 70)
    print("1. T in elementary terms")
    print("=" * 70)
    verify_the_elementary_form()

    print()
    print("=" * 70)
    print("2. T is U in a mirror")
    print("=" * 70)
    verify_the_duality()

    print()
    print("=" * 70)
    print("3. No finite shift-term reaches T")
    print("=" * 70)
    verify_no_finite_shift_term()

    print()
    print("=" * 70)
    print("4. T's tiles are windows too")
    print("=" * 70)
    verify_T_tiles_are_windows()

    print()
    print("=" * 70)
    print("all checks passed")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
