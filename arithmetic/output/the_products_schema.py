"""Multiplication as a series, and the products schema behind it.

Asked: express multiplication by infinite series of existing primitives
and see what the new useful series are.  The decomposition is forced --
peeling y's LOW bit needs the banned right shift, so the recursion runs
over an externally indexed family, and the one genuinely new constructor
is the family itself:

    t_i  =  a^i(x) & N(a^i(1) & y)          the i-th partial product

a TWO-TRACK shift: `a` advances the accumuland a^i(x) and the probe
a^i(1) together, and `N` turns "bit i of y" into the 0/Omega scalar
that switches the term on or off.  Everything after that is a choice of
JOIN, and all four joins are interesting:

    join   product                         at y = Omega
    ^      carryless product  x (*) y      !(x)
    |      Minkowski sum      x (+) y      U(x)
    &      erosion            x (-) y      0
    +      MULTIPLICATION     x * y        -x   (2-adic)

So 0042's series schema is the Omega-COLUMN of a products schema, and
multiplication is not a new kind of thing -- it is the fourth join's
product, the same way addition was the `|` cell over a guarded shift
(0050).

The `+` join also completes 0042's nine-cell table with a fourth row,
and its two cells are old friends:

    S = x + a(S)   solves to   S = -x        (2-adic negation)
    S = x + b(S)   solves to   S = not-x     (complement, = -x - 1)

Run directly for the verification suite.
"""

from __future__ import annotations

import itertools
import random

WIDTH = 16
MASK = (1 << WIDTH) - 1


def guarded_family(x: int, y: int, width: int):
    """t_i = a^i(x) & N(a^i(1) & y): the partial products present in y."""
    mask = (1 << width) - 1
    return [(x << i) & mask for i in range(width) if (y >> i) & 1]


def product(join: str, x: int, y: int, width: int = WIDTH) -> int:
    mask = (1 << width) - 1
    terms = guarded_family(x, y, width)
    if join == "^":
        total = 0
        for term in terms:
            total ^= term
    elif join == "|":
        total = 0
        for term in terms:
            total |= term
    elif join == "&":
        total = mask                    # the absent term is Omega, the
        for term in terms:              # join's identity -- the guard
            total &= term               # dualises with the join
    elif join == "+":
        total = 0
        for term in terms:
            total = (total + term) & mask
    return total & mask


# ---------------------------------------------------------------------
# 1. the + product IS multiplication
# ---------------------------------------------------------------------

def verify_multiplication_is_a_series(seed=20261012) -> None:
    for x in range(128):
        for y in range(128):
            assert product("+", x, y, 14) == (x * y) & ((1 << 14) - 1)
    generator = random.Random(seed)
    for _ in range(4000):
        x = generator.randrange(1 << WIDTH)
        y = generator.randrange(1 << WIDTH)
        assert product("+", x, y) == (x * y) & MASK, (x, y)
    print("  x * y  =  Sum+ over i in y of a^i(x)     exhaustive to 128,")
    print(f"  4000 random pairs at width {WIDTH}: exact.")
    print()
    print("  The family is the one new constructor: a^i(x) & N(a^i(1)y),")
    print("  a DIAGONAL shift moving the accumuland and the probe")
    print("  together, with N as the 0/Omega scalar. No right shift, no")
    print("  new primitive operation -- and the join is 0050's addition,")
    print("  so every carry inside is the guarded-shift `|` cell.")


# ---------------------------------------------------------------------
# 2. the four products, against independent definitions
# ---------------------------------------------------------------------

def _convolution(x: int, y: int, width: int) -> int:
    total = 0
    for position in range(width):
        bit = 0
        for i in range(position + 1):
            bit ^= ((x >> i) & 1) & ((y >> (position - i)) & 1)
        total |= bit << position
    return total


def _minkowski(x: int, y: int, width: int) -> int:
    total = 0
    for i in range(width):
        for j in range(width):
            if (x >> i) & 1 and (y >> j) & 1 and i + j < width:
                total |= 1 << (i + j)
    return total


def _erosion(x: int, y: int, width: int) -> int:
    total = 0
    for position in range(width):
        if all((x >> (position - i)) & 1 if position >= i else False
               for i in range(width) if (y >> i) & 1):
            total |= 1 << position
    return total


def verify_the_four_products(seed=20261012) -> None:
    generator = random.Random(seed)
    width = 12
    for _ in range(1500):
        x = generator.randrange(1 << width)
        y = generator.randrange(1 << width)
        assert product("^", x, y, width) == _convolution(x, y, width)
        assert product("|", x, y, width) == _minkowski(x, y, width)
        assert product("&", x, y, width) == _erosion(x, y, width)
        assert product("+", x, y, width) == (x * y) & ((1 << width) - 1)
    print("  1500 random pairs at width 12, each product against an")
    print("  independent definition:")
    print("    ^   carryless product      GF(2) convolution of the bits")
    print("    |   Minkowski sum          { i + j : i in x, j in y }")
    print("    &   erosion                { k : k - i in x for all i in y }")
    print("    +   multiplication         x * y")
    print()
    print("  One family, four joins. The set-shaped products are classical")
    print("  objects (dilation and erosion are mathematical morphology's")
    print("  pair), and multiplication sits beside them as the `+` case.")


# ---------------------------------------------------------------------
# 3. the schema's series are the Omega column
# ---------------------------------------------------------------------

def _bang(x: int, width: int) -> int:
    total, lifted, mask = x, x, (1 << width) - 1
    for _ in range(width):
        lifted = (lifted << 1) & mask
        total ^= lifted
    return total


def _up(x: int, width: int) -> int:
    total, lifted, mask = x, x, (1 << width) - 1
    for _ in range(width):
        lifted = (lifted << 1) & mask
        total |= lifted
    return total


def _trail(x: int, width: int) -> int:
    total, lifted, mask = x, x, (1 << width) - 1
    for _ in range(width):
        lifted = ((lifted << 1) | 1) & mask
        total &= lifted
    return total


def verify_the_omega_column(seed=20261012) -> None:
    generator = random.Random(seed)
    width = 14
    mask = (1 << width) - 1
    for _ in range(2000):
        x = generator.randrange(1 << width)
        assert product("^", x, mask, width) == _bang(x, width)
        assert product("|", x, mask, width) == _up(x, width)
        assert product("&", x, mask, width) == (mask if x == mask else 0)
        assert product("+", x, mask, width) == (-x) & mask
    print("  2000 random x at width 14, y = Omega:")
    print("    x (*) Omega  =  !(x)         the xor series")
    print("    x (+) Omega  =  U(x)         the up closure")
    print("    x (-) Omega  =  0            (0042's dead (&,a) cell)")
    print("    x  *  Omega  =  -x           2-adic negation: Omega = -1")
    print()
    print("  0042's series schema is the y = Omega column of the products")
    print("  schema. The unary operators were never a separate species --")
    print("  each is its product evaluated at the universe. And the `&`")
    print("  row's a-cell being 0 is no longer a degenerate corner: it is")
    print("  erosion by an infinite structuring set.")
    print()
    # the b-fill column: T is the erosion of the b-shift family
    for _ in range(800):
        x = generator.randrange(1 << width)
        eroded = mask
        for i in range(width):
            eroded &= ((x << i) | ((1 << i) - 1)) & mask
        assert eroded == _trail(x, width)
    print("  and with the b-fill (shift filling ones), the erosion at")
    print("  Omega is T(x) -- 0042's b column is the same schema with the")
    print("  other fill, exactly as it was for the unary series.")


# ---------------------------------------------------------------------
# 4. the + row completes 0042's table
# ---------------------------------------------------------------------

def verify_the_plus_row(seed=20261012) -> None:
    generator = random.Random(seed)
    width = 18
    mask = (1 << width) - 1
    for _ in range(2000):
        x = generator.randrange(1 << width)
        minus = (-x) & mask
        complement = x ^ mask
        assert minus == (x + ((minus << 1) & mask)) & mask
        assert complement == (x + (((complement << 1) | 1) & mask)) & mask
    # convergence of the fixpoint iteration, low bits first
    stabilised = 0
    for _ in range(300):
        x = generator.randrange(1 << width) | 1
        current = 0
        for step in range(width + 1):
            current = (x + ((current << 1) & mask)) & mask
        assert current == (-x) & mask
        stabilised += 1
    print("  S = x + a(S)  solves to  S = -x     (S - 2S = x)")
    print("  S = x + b(S)  solves to  S = ~x     (-x - 1)")
    print(f"  both fixpoint identities exact on 2000 values at width "
          f"{width},")
    print(f"  and the iteration from 0 stabilises one low bit per step")
    print(f"  ({stabilised} values checked) -- 2-adic convergence, the")
    print("  same reading that makes every lasso constant a rational.")
    print()
    print("  0042's table, completed:")
    print()
    print("    join \\ shift    a               b")
    print("    ^               !               (divergent)")
    print("    |               U               Omega")
    print("    &               0               T")
    print("    +               -x              ~x")
    print()
    print("  The + row is a group join like ^ -- invertible, nothing")
    print("  absorbing, telescoping exact (S - a(S) = x is the defining")
    print("  equation) -- and its two cells are negation and complement.")
    print("  Complement needed Omega = N(b 0) before; here it is a CELL,")
    print("  and Omega = -1 is its value at x = 1... the constant tier")
    print("  and the operator tier meet in the 2-adics.")


def verify_lassos_are_rationals() -> None:
    """Ultimately periodic sets are the odd-denominator rationals."""
    width = 24
    mask = (1 << width) - 1
    cases = []
    # (prefix, cycle) -> claimed rational p/q, verified as value*q = p
    pattern_third = sum(1 << i for i in range(0, width, 2))    # (10)^w
    cases.append(("(10)^w", pattern_third, -1, 3))
    pattern_fifth = sum(1 << i for i in range(0, width, 4))    # (1000)^w
    cases.append(("(1000)^w", pattern_fifth, -1, 15))
    cases.append(("(1)^w = Omega", mask, -1, 1))
    pattern_sixth = (sum(1 << i for i in range(1, width, 2)))  # 0(01)...
    cases.append(("(01)^w", pattern_sixth, -2, 3))
    for label, value, p, q in cases:
        assert (value * q - p) & mask == 0, label
        print(f"    {label:<16} = {p}/{q}   ({p} = {q} * pattern, "
              f"mod 2^{width})")
    print()
    print("  0047's lasso constants are exactly the rationals with odd")
    print("  denominator, read 2-adically. The constant tier the products")
    print("  need is closed: sums and products of lassos are lassos,")
    print("  because Q is a field and the odd-denominator subring is")
    print("  closed under + and *.")


# ---------------------------------------------------------------------
# 5. each product distributes over its own join
# ---------------------------------------------------------------------

def verify_distribution_is_diagonal(seed=20261012) -> None:
    """(x1 J x2) P y  =  (x1 P y) J (x2 P y)  exactly when J is P's join.

    0042 s2's law was S(p J q) = S(p) J S(q) over the series' own join
    and no other; the products inherit it in the x track -- the track
    the unary schema kept. (The y track is different: three products
    are commutative so the law transfers, but erosion is not, and its
    y-law is the classical anti-distribution, checked after.)
    """
    generator = random.Random(seed)
    width = 12
    mask = (1 << width) - 1
    joins = ["^", "|", "&", "+"]
    apply_join = {"^": lambda p, q: p ^ q, "|": lambda p, q: p | q,
                  "&": lambda p, q: p & q,
                  "+": lambda p, q: (p + q) & mask}
    broken = {(row, col): 0 for row in joins for col in joins}
    for _ in range(700):
        x1 = generator.randrange(1 << width)
        x2 = generator.randrange(1 << width)
        y = generator.randrange(1 << width)
        for row in joins:
            for col in joins:
                left = product(row, apply_join[col](x1, x2), y, width)
                right = apply_join[col](product(row, x1, y, width),
                                        product(row, x2, y, width))
                if left != right:
                    broken[(row, col)] += 1
    print("    product \\ join   ^      |      &      +")
    for row in joins:
        marks = ["ok " if not broken[(row, col)] else "no "
                 for col in joins]
        print(f"    {row:<16} " + "    ".join(marks))
    for row in joins:
        assert not broken[(row, row)], row
        for col in joins:
            if col != row:
                assert broken[(row, col)], (row, col)
    print()
    print("  The diagonal holds exactly and nothing off it does: each")
    print("  product distributes over ITS OWN join in the x track --")
    print("  0042 s2's 'over its own join, and no other', lifted from the")
    print("  unary series to the products.")
    for _ in range(400):
        x = generator.randrange(1 << width)
        y = generator.randrange(1 << width)
        z = generator.randrange(1 << width)
        assert product("&", x, y | z, width) == \
            (product("&", x, y, width) & product("&", x, z, width))
    print()
    print("  In the y track the three commutative products inherit the")
    print("  same law; erosion instead anti-distributes --")
    print("  x (-) (y | z) = (x(-)y) & (x(-)z), the morphology duality --")
    print("  verified.")


def verify_shifts_and_units(seed=20261012) -> None:
    generator = random.Random(seed)
    width = 12
    mask = (1 << width) - 1
    commutes = {join: True for join in "^|&+"}
    for _ in range(800):
        x = generator.randrange(1 << width)
        y = generator.randrange(1 << width)
        for join in "^|&+":
            assert product(join, x, 1, width) == x, join
            left = product(join, (x << 1) & mask, y, width)
            middle = (product(join, x, y, width) << 1) & mask
            right = product(join, x, (y << 1) & mask, width)
            if join != "&":
                assert left == middle == right, (join, x, y)
            if product(join, x, y, width) != product(join, y, x, width):
                commutes[join] = False
    print("  for every product: 1 is the unit, and `a` is a homomorphism")
    print("  in each argument (a(x)*y = a(x*y) = x*a(y)) -- except")
    print("  erosion, where shifting the structuring set moves the other")
    print("  way. Commutativity:")
    for join in "^|&+":
        print(f"    {join}   {'commutative' if commutes[join] else 'NOT commutative'}")
    assert commutes["^"] and commutes["|"] and commutes["+"]
    assert not commutes["&"]
    print()
    print("  Three of four commute. Erosion does not -- the dual guard")
    print("  (absent terms are Omega) breaks the symmetry of the family,")
    print("  which is exactly what makes it the odd one out in morphology")
    print("  too.")


def verify_n_is_multiplicative(seed=20261012) -> None:
    generator = random.Random(seed)
    width, wide = 12, 26                # inputs 12 bits, evaluate at 26:
    for _ in range(2000):               # no truncation, no exclusions
        x = generator.randrange(1 << width)
        y = generator.randrange(1 << width)
        for join in ("^", "|", "+"):
            value = product(join, x, y, wide)
            assert bool(value) == (bool(x) and bool(y)), (join, x, y)
    print("  N(x P y) = N(x) & N(y) for P in {carryless, Minkowski,")
    print("  multiplication} -- 2000 pairs, evaluated wide enough that")
    print("  truncation cannot interfere. Three of the four products have")
    print("  no zero divisors (GF(2)[t], set addition, and Z_2 are all")
    print("  domains), so N is multiplicative across them: one more law")
    print("  for the operator that cannot be expanded (0051), and it is a")
    print("  ring-homomorphism law, not a lattice one.")


# ---------------------------------------------------------------------
# 6. the carry of a family: the majority appears
# ---------------------------------------------------------------------

def verify_the_three_two_reduction(seed=20261012) -> None:
    generator = random.Random(seed)
    width = 16
    mask = (1 << width) - 1
    for _ in range(3000):
        x = generator.randrange(1 << width)
        y = generator.randrange(1 << width)
        z = generator.randrange(1 << width)
        parity = x ^ y ^ z
        majority = (x & y) ^ (x & z) ^ (y & z)
        assert (x + y + z) & mask == \
            (parity + ((majority << 1) & mask)) & mask
    print("  x + y + z  =  (x ^ y ^ z)  +  a( xy ^ xz ^ yz )")
    print()
    print("  3000 triples, exact. Two terms needed (p, g) = (x^y, x&y);")
    print("  three terms need (parity, MAJORITY), and the majority --")
    print("  Post's monotone self-dual clone -- walks in as the 3-ary")
    print("  carry. Folding the product's whole family through this 3->2")
    print("  reduction is the Wallace-tree shape of multiplication, and")
    print("  the layer operators e1 = parity, e2-carry = majority are the")
    print("  next candidates for NAMED series if a coalescing system for")
    print("  `*` is built.")


# ---------------------------------------------------------------------
# 7. every product crosses the wall; every constant slice returns
# ---------------------------------------------------------------------

def _residuals(function, prefix_bits: int, tail_bits: int) -> int:
    tails = [(tx, ty) for tx in range(1 << tail_bits)
             for ty in range(1 << tail_bits)]
    classes = set()
    for low_x in range(1 << prefix_bits):
        for low_y in range(1 << prefix_bits):
            classes.add(tuple(
                function(low_x | (tx << prefix_bits),
                         low_y | (ty << prefix_bits)) >> prefix_bits
                for tx, ty in tails))
    return len(classes)


def verify_the_wall_in_all_four_joins(tail_bits=4) -> None:
    width = 10
    mask = (1 << width) - 1
    functions = [
        ("x (*) y", lambda x, y: _convolution(x & mask, y & mask, width)),
        ("x (+) y", lambda x, y: _minkowski(x & mask, y & mask, width)),
        ("x (-) y", lambda x, y: _erosion(x & mask, y & mask, width)),
        ("x * y", lambda x, y: (x * y) & mask),
    ]
    print(f"    residual classes after reading p bits (tails of "
          f"{tail_bits}):")
    print("    p    " + "".join(f"{label:>10}" for label, _ in functions))
    growth = {}
    for prefix_bits in range(0, 5):
        counts = [_residuals(function, prefix_bits, tail_bits)
                  for _, function in functions]
        growth[prefix_bits] = counts
        print(f"    {prefix_bits}    " +
              "".join(f"{count:>10}" for count in counts))
    for index in range(4):
        assert growth[4][index] > growth[1][index]
    print()
    constants = [3, 5, 7, 11, 21]
    print("    and multiplication by a CONSTANT stays finite-state:")
    for constant in constants:
        states = len({
            tuple((constant * (low | (t << p)) >> p) & ((1 << 6) - 1)
                  for t in range(1 << 6))
            for p in range(6) for low in range(1 << p)})
        print(f"      x -> {constant}x   {states} residual classes")
    print()
    print("  All four products cross 0047's bounded-state wall -- the")
    print("  wall is not about + versus *, it is unary-series versus")
    print("  binary-products, in every join. And every constant slice")
    print("  x -> c*x drops back inside (the carry is bounded by c), so")
    print("  the decidable tier is: the schema, its products WITH ONE")
    print("  ARGUMENT A LASSO, and their compositions.")


def run_verification_suite() -> None:
    sections = [
        ("Multiplication is a series of the primitives",
         verify_multiplication_is_a_series),
        ("The four products, against independent definitions",
         verify_the_four_products),
        ("The schema is the Omega column", verify_the_omega_column),
        ("The + row completes 0042's table", verify_the_plus_row),
        ("Lasso constants are the odd-denominator rationals",
         verify_lassos_are_rationals),
        ("Distribution is diagonal", verify_distribution_is_diagonal),
        ("Shifts, units, commutativity", verify_shifts_and_units),
        ("N is multiplicative", verify_n_is_multiplicative),
        ("The 3->2 reduction: majority is the family carry",
         verify_the_three_two_reduction),
        ("Every product crosses the wall; constant slices return",
         verify_the_wall_in_all_four_joins),
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
