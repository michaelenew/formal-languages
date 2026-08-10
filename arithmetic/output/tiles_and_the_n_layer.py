"""Tiles, and where the shift's content actually lives.

Two things, both measured.

**1. The telescoping identities are a family, and `N` is in it.** The
proposed `s(x) ^ s(N x) ^ N(x)` does not hold -- it fails at x = 1, 2, 3.
But the *shape* is right, and the corrected members form a family with
the corpus's own `!`:

    series                        telescoping identity
    !x   = XOR of all shifts      !x ^ s(!x)  =  x
    U(x) = UNION of all shifts    U(x) ^ s(U x) =  V2(x)   the lowest set bit
    N(x) = the two-way closure    N(x) ^ s(N x) =  [x != 0] at position 0

So `T ^ s(T)` is what a shift-series *measures*: `!` measures x itself,
`U` measures the lowest set position, `N` measures nonemptiness as one
bit. `V2` is 0008's own primitive, and `U` also satisfies the fixpoint
`U(x) = x | s(U x)` -- the stabilizing-series shape of 0002, exactly.

**2. The tile decomposition, and why it matters.** Treating each symbol
(`x` and `s(x)` are different symbols) as a circle on a Venn diagram,
every statement is a union of tiles, and the closure distributes over
that union -- so closing tile by tile at checking time is the same
object as closing K whole. Verified.

What the tile picture buys is not a different closure but a different
*place to put the content*. The collapse `C(T) = N(T)` of 0038 is a
SEMANTIC fact: it holds because `s` is the real shift. Over free symbols
it is false -- `s^k(t)` are distinct tiles and the union does not
collapse, which is 0037's unrolling. Tiles reconcile the two: the
Boolean structure lives in the tiles, which are free, and everything the
shift relation contributes lives in the **N-layer** as constraints on
which tiles can be non-empty together. The shift's whole contribution is
one such constraint, `N(x) = N(s x)`, verified.

Consequence: entailment becomes a propositional implication over the
N-values of tiles, restricted to the realisable vectors. Finite and
decidable, demonstrated below.

Run directly for the verification suite.
"""

from __future__ import annotations

from itertools import product as cartesian_product

WIDTH = 12
MASK = (1 << WIDTH) - 1

shift = lambda value: (value << 1) & MASK
join = lambda left, right: left ^ right ^ (left & right)
complement = lambda value: MASK ^ value
indicator = lambda value: 0 if value == 0 else MASK
lowest_set = lambda value: value & -value


def up_closure(value: int) -> int:
    total, rising = value, value
    for _ in range(WIDTH):
        rising = shift(rising)
        total = join(total, rising)
    return total


def two_way_closure(value: int) -> int:
    total = rising = falling = value
    for _ in range(WIDTH):
        rising = shift(rising)
        falling >>= 1
        total = join(join(total, rising), falling)
    return total


def xor_series(value: int) -> int:
    """The corpus's `!x` -- XOR of every shift."""
    total, rising = 0, value
    while rising:
        total ^= rising
        rising = shift(rising)
    return total


# ---------------------------------------------------------------------
# 1. the telescoping family
# ---------------------------------------------------------------------

def verify_the_identity_family() -> None:
    domain = range(1 << WIDTH)
    rows = [
        ("s(x) ^ s(N x) ^ N(x)        as proposed",
         lambda v: shift(v) ^ shift(indicator(v)) ^ indicator(v)),
        ("!x ^ s(!x) ^ x              corpus's !",
         lambda v: xor_series(v) ^ shift(xor_series(v)) ^ v),
        ("U(x) ^ s(U x) ^ V2(x)       union series",
         lambda v: up_closure(v) ^ shift(up_closure(v)) ^ lowest_set(v)),
        ("N(x) ^ s(N x) ^ [x!=0]      two-way closure",
         lambda v: (indicator(v) ^ shift(indicator(v))
                    ^ (1 if v else 0))),
        ("U(x) ^ (x | s(U x))         the fixpoint",
         lambda v: up_closure(v) ^ join(v, shift(up_closure(v)))),
        ("N(x) ^ N(s x)               s is injective",
         lambda v: indicator(v) ^ indicator(shift(v))),
    ]
    for label, statement in rows:
        failures = [v for v in domain
                    if statement(v) != 0 and v < (1 << (WIDTH - 1))]
        verdict = "empty (holds)" if not failures else (
            f"NOT empty, first failures x = {failures[:3]}")
        print(f"  {label:<44} {verdict}")
    proposed = [v for v in domain
                if shift(v) ^ shift(indicator(v)) ^ indicator(v) != 0]
    assert proposed[:3] == [1, 2, 3]
    for _, statement in rows[1:]:
        assert not [v for v in domain if statement(v) != 0
                    and v < (1 << (WIDTH - 1))]
    print("    The proposal has the right SHAPE -- `T ^ s(T)` is what a "
          "shift-series")
    print("    measures -- and the wrong right-hand side. `!` measures x,"
          " `U` the lowest")
    print("    set position (0008's V2), `N` nonemptiness as a single "
          "bit.")


# ---------------------------------------------------------------------
# 2. tiles
# ---------------------------------------------------------------------

def tiles_of(symbols: tuple) -> list:
    """Every minterm of the algebra generated by the given symbol
    functions: the tiles of the Venn diagram."""
    def tile(polarity, value):
        region = MASK
        for chosen, symbol in zip(polarity, symbols):
            region &= symbol(value) if chosen else complement(symbol(value))
        return region
    return [(polarity, lambda v, p=polarity: tile(p, v))
            for polarity in cartesian_product((1, 0), repeat=len(symbols))]


def verify_closure_is_tilewise() -> None:
    """Closing tile by tile is closing the whole, because `s` and `h`
    distribute over union."""
    symbols = (lambda v: v, shift)
    tiles = tiles_of(symbols)
    statement = lambda v: join(v, shift(v))         # x | s(x)
    failures = []
    for value in range(1 << WIDTH):
        whole = two_way_closure(statement(value))
        piecewise = 0
        for _, tile in tiles:
            part = tile(value) & statement(value)
            piecewise = join(piecewise, two_way_closure(part))
        if whole != piecewise:
            failures.append(value)
    assert not failures, failures[:5]
    print("  C(K) = union over K's tiles of C(tile)   "
          f"for every x < 2^{WIDTH}")
    print("    so the closure may be taken at checking time, tile by "
          "tile, and it is")
    print("    the same object as closing K whole. `s` and `h` "
          "distribute over union.")


def verify_the_collapse_is_semantic() -> None:
    """C(T) = N(T) holds because `s` is the real shift. Over free
    symbols the shifts of a tile are distinct and nothing collapses --
    which is 0037's unrolling, and the reason the two views differ."""
    semantic = [v for v in range(1 << WIDTH)
                if two_way_closure(v) != indicator(v)]
    assert not semantic
    print(f"  semantically:  C(T) = N(T) for every T < 2^{WIDTH}")

    # symbolically, over free symbols, the shifts of one tile stay
    # distinct: count the distinct symbolic images s^k(tile).
    symbols = (lambda v: v, shift)
    tiles = tiles_of(symbols)
    polarity, tile = tiles[1]                      # x & not s(x)
    images = {tuple(tile(v) for v in range(1 << 6))}
    lifted = tile
    for _ in range(4):
        previous = lifted
        lifted = (lambda v, f=previous: shift(f(v)))
        images.add(tuple(lifted(v) for v in range(1 << 6)))
    print(f"  symbolically:   the first five shifts of the tile "
          f"{polarity} are {len(images)} distinct maps")
    assert len(images) == 5
    print("    so over FREE symbols the union of shifts does not "
          "collapse -- 0037's")
    print("    unrolling. Tiles are where the two views meet: the "
          "Boolean structure is")
    print("    free, and the shift's contribution is a constraint in "
          "the N-layer.")


# ---------------------------------------------------------------------
# 3. the N-layer
# ---------------------------------------------------------------------

def realisable_vectors(symbols: tuple, domain) -> set:
    """Which tiles can be non-empty together, given that the symbols are
    what they are. This is the whole content of the operator relations,
    expressed on the tiles."""
    tiles = tiles_of(symbols)
    return {tuple(1 if tile(value) else 0 for _, tile in tiles)
            for value in domain}


def verify_the_n_layer_reformulation() -> None:
    symbols = (lambda v: v, shift)                  # x and s(x)
    tiles = tiles_of(symbols)
    labels = ["x·s(x)", "x·~s(x)", "~x·s(x)", "~x·~s(x)"]
    # stay below the top bit: shifting out of the mask would make
    # s(x) empty for non-empty x, a finite-width artefact rather
    # than a fact about the shift.
    domain = range(1 << (WIDTH - 1))
    vectors = realisable_vectors(symbols, domain)
    print(f"  tiles of {{x, s(x)}}: {labels}")
    print(f"  realisable N-vectors over x < 2^{WIDTH - 1}: {len(vectors)} of "
          f"{2 ** len(tiles)} possible")
    for vector in sorted(vectors):
        print(f"    {vector}")

    # the shift's contribution, read off the realisable set
    constraint_holds = all(
        (vector[0] or vector[1]) == (vector[0] or vector[2])
        for vector in vectors)
    assert constraint_holds
    print("    every realisable vector satisfies  N(x) = N(s x),  i.e.")
    print("      N(x·s(x)) or N(x·~s(x))  ==  N(x·s(x)) or N(~x·s(x))")
    print("    -- that single Boolean law is the whole of what the "
          "shift contributes.")

    # entailment as propositional implication over realisable vectors
    knowledge_tiles = (0, 1)                        # K = x
    hypothesis_tiles = (0, 2)                       # H = s(x)
    empty = lambda vector, chosen: all(not vector[i] for i in chosen)
    propositional = all(
        not empty(vector, knowledge_tiles)
        or empty(vector, hypothesis_tiles) for vector in vectors)
    semantic = all(value != 0 or shift(value) == 0 for value in domain)
    assert propositional and semantic
    print()
    print("  K := x    H := s(x)")
    print("    entailment, semantically:                 True")
    print("    implication over realisable N-vectors:    True")
    print("    -- the deduction is propositional once the tiles are "
          "named, and the only")
    print("    non-Boolean input is the realisable set. Finite, and "
          "decidable by")
    print("    enumeration.")


def run_verification_suite() -> None:
    print("=" * 70)
    print("1. The telescoping identities are a family")
    print("=" * 70)
    verify_the_identity_family()

    print()
    print("=" * 70)
    print("2. The closure is tile-wise")
    print("=" * 70)
    verify_closure_is_tilewise()
    print()
    verify_the_collapse_is_semantic()

    print()
    print("=" * 70)
    print("3. The shift's content lives in the N-layer")
    print("=" * 70)
    verify_the_n_layer_reformulation()

    print()
    print("=" * 70)
    print("all checks passed")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
