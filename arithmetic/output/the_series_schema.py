"""The series zoo is one schema, and it carries its own rewrite rules.

`!`, `$`/`T`, and the closures of 0038-0041 all have the shape

    S(x)  =  x  o  sigma(x)  o  sigma^2(x)  o  ...

for a join `o` in {^, |, &} and a shift `sigma` in {a, b, h}, where
a(x) = 2x fills with zeros, b(x) = 2x+1 fills with ones, and h(x) = x>>1
drops the low bit. Nine cells. Most are trivial or divergent; the
survivors are exactly the operators the corpus has been carrying
separately.

Three laws are universal across the survivors, and they are the
expansion, combination and cancellation rules a convex system needs:

    fixpoint       S(x) = x o sigma(S x)
    distribution   S(a o b) = S(a) o S(b)          over ITS OWN join
    telescoping    S(x) ^ sigma(S x) = <what the series measures>

Two more properties split by JOIN, and they are exclusive:

    join  measures                 closure   invertible
    ^     x itself                 no        yes
    |     the extremal element     yes       no
    &     the extremal gap         yes       no

A `^` series can be undone -- `x = S(x) ^ sigma(S x)` IS its telescoping
identity -- and so is never idempotent. A `|` or `&` series keeps only
one extremum, so it is idempotent and cannot be undone.

`N` is not a cell -- it is `U | D`, the two `|` cells joined -- which is
why it behaves differently from the rest and why its rules (0038) had to
be found separately.

Section 4 tabulates how `N` and `T` compose, which is the decomposition
side of the rewrite system: most composites collapse, and the ones that
do not are the rules worth keeping.

Run directly for the verification suite.
"""

from __future__ import annotations

from itertools import product as cartesian_product

WIDTH = 10
MASK = (1 << WIDTH) - 1
SAFE = range(1 << (WIDTH - 2))

negate = lambda value: MASK ^ value
lowest_set = lambda value: value & -value
highest_set = lambda value: 0 if not value else 1 << (value.bit_length() - 1)
lowest_zero = lambda value: lowest_set(negate(value))

SHIFTS = {
    "a": lambda value: (value << 1) & MASK,          # fills with zeros
    "b": lambda value: ((value << 1) | 1) & MASK,    # fills with ones
    "h": lambda value: value >> 1,                   # drops the low bit
}
JOINS = {
    "^": lambda left, right: left ^ right,
    "|": lambda left, right: left ^ right ^ (left & right),
    "&": lambda left, right: left & right,
}


def series(join: str, shift: str, value: int):
    """S(x) = x o sigma(x) o ... , or None if it never settles."""
    combine, lift = JOINS[join], SHIFTS[shift]
    total, lifted = value, value
    history = []
    for _ in range(2 * WIDTH + 4):
        lifted = lift(lifted)
        total = combine(total, lifted)
        history.append(total)
    return total if len(set(history[-WIDTH:])) == 1 else None


# ---------------------------------------------------------------------
# 1. the nine cells
# ---------------------------------------------------------------------

CATALOGUE = [
    ("0", lambda v: 0),
    ("the universe", lambda v: MASK),
    ("x", lambda v: v),
    ("! (xor series)", lambda v: series("^", "a", v)),
    ("!h (suffix parity)", lambda v: series("^", "h", v)),
    ("U (up-closure)", lambda v: series("|", "a", v)),
    ("D (down-closure)", lambda v: series("|", "h", v)),
    ("T (trailing ones)", lambda v: series("&", "b", v)),
]


def identify(candidate) -> str:
    for name, known in CATALOGUE:
        if all(candidate(v) == known(v) for v in SAFE):
            return name
    return "-"


def verify_the_nine_cells() -> None:
    print("  join \\ shift        a (fill 0)          b (fill 1)"
          "          h (right)")
    survivors = []
    for join in ("^", "|", "&"):
        cells = []
        for shift in ("a", "b", "h"):
            if any(series(join, shift, v) is None for v in SAFE):
                cells.append("divergent")
                continue
            name = identify(lambda v, j=join, s=shift: series(j, s, v))
            cells.append(name)
            if name not in ("0", "the universe"):
                survivors.append((join, shift, name))
        print(f"      {join}        " + "".join(f"{c:<20}" for c in cells))
    print()
    print(f"    {len(survivors)} non-trivial cells: "
          + ", ".join(name for _, _, name in survivors))
    print("    -- and they are exactly the operators the corpus carries "
          "separately.")
    assert len(survivors) == 5
    return survivors


# ---------------------------------------------------------------------
# 2. the five laws
# ---------------------------------------------------------------------

MEASURES = {
    ("^", "a"): ("x", lambda v: v),
    ("^", "h"): ("x", lambda v: v),
    ("|", "a"): ("lowest set bit", lowest_set),
    ("|", "h"): ("highest set bit", highest_set),
    ("&", "b"): ("lowest zero bit", lowest_zero),
}


def verify_the_laws(survivors) -> None:
    print("  cell                       fixpoint  distributes  "
          "telescopes to        closure  invertible")
    for join, shift, name in survivors:
        combine, lift = JOINS[join], SHIFTS[shift]
        run = lambda v, j=join, s=shift: series(j, s, v)

        fixpoint = all(run(v) == combine(v, lift(run(v))) for v in SAFE)
        label, measure = MEASURES[(join, shift)]
        telescopes = all(run(v) ^ lift(run(v)) == measure(v) for v in SAFE)
        distributes = all(
            run(combine(a, b)) == combine(run(a), run(b))
            for a in range(0, 1 << (WIDTH - 4))
            for b in range(0, 1 << (WIDTH - 4)))
        idempotent = all(run(run(v)) == run(v) for v in SAFE)
        # invertible: x is recoverable from S(x) alone
        invertible = len({run(v) for v in SAFE}) == len(SAFE)

        assert fixpoint and telescopes and distributes, name
        assert idempotent == (join != "^"), name
        assert invertible == (join == "^"), name
        print(f"  {name:<26} yes       yes          {label:<20} "
              f"{'yes' if idempotent else 'no ':<8} "
              f"{'yes' if invertible else 'no'}")
    print()
    print("    Fixpoint, distribution and telescoping are universal. The "
          "last two columns")
    print("    split by JOIN, and they are exclusive:")
    print()
    print("      join  measures                       closure  invertible")
    print("      ^     x itself                       no       yes")
    print("      |     the extremal element           yes      no")
    print("      &     the extremal gap               yes      no")
    print()
    print("    A `^` series can be undone -- x = S(x) ^ sigma(S x) IS "
          "the telescoping")
    print("    identity -- and so is never idempotent. A `|` or `&` "
          "series keeps only one")
    print("    extremum, so it is idempotent and cannot be undone. Each "
          "distributes over")
    print("    its OWN join and no other, which is the rule that pushes "
          "it inward.")


# ---------------------------------------------------------------------
# 3. N is not a cell
# ---------------------------------------------------------------------

def nonempty(value: int) -> int:
    return 0 if value == 0 else MASK


def verify_N_is_the_join_of_two_cells() -> None:
    up = lambda v: series("|", "a", v)
    down = lambda v: series("|", "h", v)
    assert all(JOINS["|"](up(v), down(v)) == nonempty(v) for v in SAFE)
    print("  N(x) = U(x) | D(x)         verified")
    print("    so N is not a cell of the table -- it is two `|` cells "
          "joined, which is")
    print("    why it behaves unlike the others and why its rules (0038) "
          "had to be found")
    print("    separately. U and D each measure one extreme; joined, "
          "they lose both and")
    print("    keep only whether an extreme exists at all.")


# ---------------------------------------------------------------------
# 4. how N and T compose
# ---------------------------------------------------------------------

def verify_composition_table() -> None:
    up = lambda v: series("|", "a", v)
    down = lambda v: series("|", "h", v)
    trailing = lambda v: series("&", "b", v)
    low = lambda v: nonempty(v & 1)

    catalogue = [
        ("0", lambda v: 0),
        ("1 (universe)", lambda v: MASK),
        ("x", lambda v: v),
        ("N(x)", nonempty),
        ("N(x&1)", low),
        ("U(x)", up),
        ("D(x)", down),
        ("T(x)", trailing),
    ]

    def name(candidate):
        for label, known in catalogue:
            if all(candidate(v) == known(v) for v in SAFE):
                return label
        return "(new)"

    outer = [("N", nonempty), ("T", trailing), ("U", up), ("D", down)]
    print("       " + "".join(f"{label:>12}" for label, _ in outer))
    for inner_label, inner in outer:
        row = [name(lambda v, f=outer_f, g=inner: f(g(v)))
               for _, outer_f in outer]
        print(f"  x{inner_label:<4}" + "".join(f"{cell:>12}" for cell in row))
    print("    read: row is applied first, then the column."
          "  Every composite collapses.")
    print()
    print("    The two rules worth keeping, because they are the only "
          "ones that move")
    print("    information rather than deleting it:")
    print("      N(T x) -> N(x & 1)      T is empty exactly when x's low "
          "bit is clear")
    print("      T(U x) -> N(x & 1)      likewise, through the other "
          "closure")
    assert name(lambda v: nonempty(trailing(v))) == "N(x&1)"
    assert name(lambda v: trailing(up(v))) == "N(x&1)"
    assert name(lambda v: trailing(nonempty(v))) == "N(x)"
    assert name(lambda v: up(nonempty(v))) == "N(x)"


def run_verification_suite() -> None:
    print("=" * 70)
    print("1. The nine cells of the schema")
    print("=" * 70)
    survivors = verify_the_nine_cells()

    print()
    print("=" * 70)
    print("2. The laws, and what the join decides")
    print("=" * 70)
    verify_the_laws(survivors)

    print()
    print("=" * 70)
    print("3. N is not a cell")
    print("=" * 70)
    verify_N_is_the_join_of_two_cells()

    print()
    print("=" * 70)
    print("4. How N and T compose")
    print("=" * 70)
    verify_composition_table()

    print()
    print("=" * 70)
    print("all checks passed")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
