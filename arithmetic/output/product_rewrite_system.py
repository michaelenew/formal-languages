"""A coalescing rewrite system for the products, built to find its walls.

0052 expressed multiplication as the `+`-join of the guarded diagonal
family; 0050/0051 settled that the rewrite direction must COALESCE
(expansion is not even weakly normalizing).  This module builds that
system and pushes it until it breaks, on purpose.

Design, and what each choice absorbs:

  +  is sugar, not a symbol:  x + y  =  x ^ y ^ a(C(x, y))
     with ONE new binary series, the carry `C` -- and `C(t, 1) = T(t)`,
     so `succ` costs nothing.  Negation is sugar too:
     -P = P ^ Omega ^ 1 ^ a(T(P ^ Omega)).
  mul  atoms carry a MULTISET of factors, flattened and sorted at
     construction: associativity and commutativity of `*` are absorbed
     the way ANF absorbs them for `^` and `&` -- one level up.
  cmul (the carryless product, `*`'s linear layer) is BILINEAR over the
     representation's own join, so the constructor expands it monomial
     by monomial: distribution over `^` costs nothing.
  dil  (Minkowski) distributes over `|`, which the representation does
     not have: it stays opaque.  That asymmetry is the point -- each
     product is native exactly in its own join's normal form.

The rules are coalescing only.  The system terminates (audited), so
complete normal-form sets are exact and every completeness or
confluence failure below is a finite certificate.

Run directly for the verification suite.
"""

from __future__ import annotations

import functools
import itertools
import random

VARS = ("x", "y", "z")
LEAF = VARS + ("one",)
SERIES = ("!", "U", "T", "N", "lowset", "lowzero")

ZERO = frozenset()
OMEGA = frozenset([frozenset()])
ONE = frozenset([frozenset([("one",)])])
X = frozenset([frozenset([("x",)])])
Y = frozenset([frozenset([("y",)])])
Z = frozenset([frozenset([("z",)])])


# ---------------------------------------------------------------------
# constructors
# ---------------------------------------------------------------------

def xor(left, right):
    return left ^ right


def conj(left, right):
    out = set()
    for atoms_l in left:
        for atoms_r in right:
            out ^= {atoms_l | atoms_r}
    return frozenset(out)


def disj(left, right):
    return xor(xor(left, right), conj(left, right))


def _key(poly):
    return sorted(sorted(map(str, atoms)) for atoms in poly), str(poly)


def _wrap(atom):
    return frozenset([frozenset([atom])])


def shift_a(poly):
    total = ZERO
    for atoms in poly:
        if not atoms:
            total = xor(total, xor(OMEGA, ONE))
            continue
        piece = OMEGA
        for element in atoms:
            piece = conj(piece, _wrap(("a", _wrap(element))))
        total = xor(total, piece)
    return total


def shift_b(poly):
    return xor(shift_a(poly), ONE)


def series(name, poly):
    return _wrap(("S", name, poly))


def carry(left, right):
    first, second = sorted((left, right), key=_key)
    return _wrap(("C", first, second))


def add(left, right):
    """+ is sugar: one new symbol (the carry), nothing else."""
    return xor(xor(left, right), shift_a(carry(left, right)))


def neg(poly):
    """-P = P ^ a(U(P)): the two-monomial negation.

    Found by chasing the k-neg/u-compdual critical pair: the four-
    monomial form ~P + 1 = (P^Omega) ^ 1 ^ a(T(P^Omega)) collapses,
    because u-compdual turns T(P^Omega) into U(P)^Omega and the ANF
    cancels a(Omega) = Omega ^ 1 away. The sugar-level canonical form
    IS the joined form of that peak.
    """
    return xor(poly, shift_a(series("U", poly)))


def mul(*factors):
    """Multiset of factors: associativity + commutativity absorbed."""
    flat = []
    for factor in factors:
        inner = _sole_product(factor)
        if inner is not None:
            flat.extend(inner)
        else:
            flat.append(factor)
    flat.sort(key=_key)
    if not flat:
        return ONE
    if len(flat) == 1:
        return flat[0]
    return _wrap(("mul", tuple(flat)))


def _sole_product(poly):
    if len(poly) != 1:
        return None
    (atoms,) = poly
    if len(atoms) != 1:
        return None
    (element,) = atoms
    return element[1] if element[0] == "mul" else None


def cmul(left, right):
    """Bilinear over ^ at construction: the carryless product is native
    to the representation's own join, so distribution costs nothing."""
    total = ZERO
    for monomial_l in left:
        for monomial_r in right:
            first, second = sorted((monomial_l, monomial_r),
                                   key=lambda m: sorted(map(str, m)))
            total = xor(total, _wrap(("cmul", first, second)))
    return total


def dil(left, right):
    """Minkowski: distributes over `|`, which ANF does not have, so it
    stays opaque. The asymmetry with cmul is deliberate and measured."""
    first, second = sorted((left, right), key=_key)
    return _wrap(("dil", first, second))


# ---------------------------------------------------------------------
# evaluation (all operators are LSB-causal except N, so masked
# evaluation gives the exact low bits; soundness checks run at two
# widths and compare low bits)
# ---------------------------------------------------------------------

def evaluate(poly, env, width) -> int:
    mask = (1 << width) - 1
    total = 0
    for atoms in poly:
        piece = mask
        for element in atoms:
            piece &= _evaluate_atom(element, env, width)
        total ^= piece
    return total & mask


def _run_series(name, value, width):
    mask = (1 << width) - 1
    if name == "N":
        return mask if value else 0
    if name == "lowset":
        return value & -value & mask
    if name == "lowzero":
        flipped = mask ^ value
        return flipped & -flipped & mask
    total, lifted = value, value
    for _ in range(width + 1):
        if name == "!":
            lifted = (lifted << 1) & mask
            total ^= lifted
        elif name == "U":
            lifted = (lifted << 1) & mask
            total |= lifted
        else:                                    # T
            lifted = ((lifted << 1) | 1) & mask
            total &= lifted
    return total


def _evaluate_atom(element, env, width) -> int:
    mask = (1 << width) - 1
    kind = element[0]
    if kind in VARS:
        return env[kind] & mask
    if kind == "one":
        return 1
    if kind == "a":
        return (evaluate(element[1], env, width) << 1) & mask
    if kind == "S":
        return _run_series(element[1], evaluate(element[2], env, width),
                           width)
    if kind == "C":
        left = evaluate(element[1], env, width)
        right = evaluate(element[2], env, width)
        propagate, generate = left ^ right, left & right
        value = 0
        for _ in range(width + 2):
            value = (generate | (propagate & ((value << 1) & mask))) & mask
        return value
    if kind == "mul":
        value = 1
        for factor in element[1]:
            value = (value * evaluate(factor, env, width)) & mask
        return value
    if kind == "cmul":
        left = mask
        for part in element[1]:
            left &= _evaluate_atom(part, env, width)
        right = mask
        for part in element[2]:
            right &= _evaluate_atom(part, env, width)
        total = 0
        for i in range(width):
            if (right >> i) & 1:
                total ^= (left << i) & mask
        return total
    if kind == "dil":
        left = evaluate(element[1], env, width)
        right = evaluate(element[2], env, width)
        total = 0
        for i in range(width):
            if (right >> i) & 1:
                total |= (left << i) & mask
        return total
    raise ValueError(kind)


def equal_low_bits(left, right, seed=7, samples=40) -> bool:
    """L = R on the low bits, at two widths, small inputs.

    Every operator here is LSB-causal except N, so a masked run is
    exact on its low bits; small inputs keep N honest at these widths.
    """
    generator = random.Random(seed)
    for width, input_bits, margin in ((22, 6, 8), (30, 7, 8)):
        check = (1 << (width - margin)) - 1
        for _ in range(samples):
            env = {name: generator.randrange(1 << input_bits)
                   for name in VARS}
            if (evaluate(left, env, width) ^
                    evaluate(right, env, width)) & check:
                return False
    return True


# ---------------------------------------------------------------------
# the rules (coalescing only)
# ---------------------------------------------------------------------

RULE_NAMES = ("u-zero", "u-one", "u-omega", "u-shift-out", "N-see",
              "N-absorbN", "u-compdual", "k-fold", "k-low",
              "p-dist-fold",
              "p-zero", "p-unit", "p-shift", "p-omega", "p-const",
              "c-unit", "c-zero", "c-omega", "c-shift",
              "d-zero", "d-unit", "d-omega", "d-shift",
              "k-zero", "k-one", "k-same", "k-shift", "k-disjoint",
              "k-neg", "N-product")


def _pure_shift(poly):
    """`poly` as a(Q), or None.

    `a(Omega) = Omega ^ 1` by construction, so the pair {Omega, 1} in a
    polynomial is a shifted Omega and must be peeled as one -- missing
    that stranded `Omega ^ 1` in every shift rule.
    """
    if not poly:
        return None
    inner = ZERO
    rest = poly
    if frozenset() in poly and frozenset([("one",)]) in poly:
        inner = OMEGA
        rest = xor(poly, xor(OMEGA, ONE))
    if not rest and inner == ZERO:
        return None
    for atoms in rest:
        if len(atoms) != 1:
            return None
        (element,) = atoms
        if element[0] != "a":
            return None
        inner = xor(inner, element[1])
    return inner


def _constant_chain(poly):
    """Is `poly` a constant (built from `one` and `a` only)?"""
    for atoms in poly:
        for element in atoms:
            if element[0] == "one":
                continue
            if element[0] == "a" and _constant_chain(element[1]):
                continue
            return False
    return True


def _poly_level_rules(poly):
    """Rules whose left-hand sides span monomials.

    k-fold: the carry's own fixpoint, supplied mid-exploration and
    verified: C(x,y) = xy ^ x·a(C) ^ y·a(C) -- bit i of C is the
    MAJORITY of column i-1 of {x, y, C}, so the carry is the fixpoint
    of the majority step (0052 s6), and unlike the `g | p&aC` form this
    one lives in the representation's own join. Read as a coalescing
    rule it folds the three-monomial majority pattern into the atom:

        m·P·Q ^ m·P·a(C(P,Q)) ^ m·Q·a(C(P,Q))  ->  m·C(P,Q)

    k-low: the recurrence's base case, C(P,Q) & 1 = P&Q & 1.
    """
    steps = []
    for atoms in poly:
        for element in atoms:
            if element[0] != "a":
                continue
            inner = _sole_atom(element[1])
            if inner is None or inner[0] != "C":
                continue
            left_arg, right_arg = inner[1], inner[2]
            if len(left_arg) != 1 or len(right_arg) != 1:
                continue
            (left_mono,) = left_arg
            (right_mono,) = right_arg
            body = atoms - {element}
            for own, other in ((left_mono, right_mono),
                               (right_mono, left_mono)):
                if not own <= body:
                    continue
                context = frozenset(body - own)
                triple = [frozenset(context | own | other),
                          frozenset(context | own | {element}),
                          frozenset(context | other | {element})]
                if all(m in poly for m in triple):
                    replacement = frozenset([frozenset(
                        context | {inner})])
                    steps.append(("k-fold", xor(xor(
                        poly, frozenset(triple)), replacement)))
                break
        for element in atoms:
            if element[0] == "C" and ("one",) in atoms:
                masked = conj(conj(element[1], element[2]), ONE)
                rest = frozenset([frozenset(atoms - {element})])
                steps.append(("k-low", xor(xor(
                    poly, frozenset([atoms])), conj(rest, masked))))
    return steps


def _dist_fold(poly):
    """`m·xy ^ m·xz ^ m·a(C(xy, xz))  ->  m·x(y + z)`.

    Distribution over `+`, oriented as a COALESCING rule: read right to
    left the ring law loses atoms, so the fold direction is the
    terminating one -- the same lesson as k-fold and N-fold. The
    pattern spans three monomials because `+` is sugar; the common
    factor multiset is the two mul atoms' intersection.
    """
    steps = []
    for atoms in poly:
        for element in atoms:
            if element[0] != "a":
                continue
            inner = _sole_atom(element[1])
            if inner is None or inner[0] != "C":
                continue
            left_arg, right_arg = inner[1], inner[2]
            first = _sole_atom(left_arg)
            second = _sole_atom(right_arg)
            if first is None or second is None:
                continue
            if first[0] != "mul" or second[0] != "mul":
                continue
            shared = []
            spare_left = list(first[1])
            spare_right = list(second[1])
            for factor in list(spare_left):
                if factor in spare_right:
                    shared.append(factor)
                    spare_left.remove(factor)
                    spare_right.remove(factor)
            if not shared:
                continue
            residual_left = mul(*spare_left)
            residual_right = mul(*spare_right)
            context = frozenset(atoms - {element})
            mono_left = frozenset(context | next(iter(left_arg)))
            mono_right = frozenset(context | next(iter(right_arg)))
            triple = [frozenset(atoms), mono_left, mono_right]
            if not all(m in poly for m in triple):
                continue
            folded = mul(*(shared + [add(residual_left,
                                         residual_right)]))
            replacement = conj(frozenset([context]), folded)
            steps.append(("p-dist-fold",
                          xor(xor(poly, frozenset(triple)), replacement)))
    return steps


@functools.lru_cache(maxsize=None)
def rewrites(poly):
    steps = list(_poly_level_rules(poly))
    steps += _dist_fold(poly)
    for atoms in sorted(poly, key=lambda m: sorted(map(str, m))):
        context = frozenset([frozenset(atoms)])
        for element in atoms:
            others = conj(_wrap(("one",)), ZERO)  # placeholder, unused
            rest = conj(frozenset([frozenset(atoms - {element})]), OMEGA)

            def emit(rule, replacement):
                steps.append((rule, xor(poly, xor(context,
                                                  conj(rest, replacement)))))

            for inner_rule, inner_result in _atom_rewrites(element):
                emit(inner_rule, inner_result)
    return tuple(step for step in steps if step[1] != poly)


def _atom_rewrites(element):
    """All one-step coalescings of a single atom, as replacements."""
    out = []
    kind = element[0]

    # recursion into arguments
    def descend(build, *arguments):
        for index, argument in enumerate(arguments):
            for rule, replaced in rewrites(argument):
                fresh = list(arguments)
                fresh[index] = replaced
                out.append((rule, build(*fresh)))

    if kind == "a":
        descend(shift_a, element[1])
        return out

    if kind == "S":
        name = element[1]
        argument = element[2]
        descend(lambda p: series(name, p), argument)
        if argument == ZERO:
            out.append(("u-zero", ZERO if name != "lowzero" else ONE))
        shifted = _pure_shift(argument)
        if shifted is not None:
            if name in ("!", "U"):
                out.append(("u-shift-out",
                            shift_a(series(name, shifted))))
            elif name == "N":
                out.append(("N-see", series("N", shifted)))
        if argument == ONE:
            out.append(("u-one", ONE if name in ("T", "lowset")
                        else OMEGA))
        if argument == OMEGA and name in ("U", "T", "N"):
            out.append(("u-omega", OMEGA))       # !(Omega) has no name
        if name == "T" and frozenset() in argument:
            # T(Q ^ Omega) = U(Q) ^ Omega: the trailing ones of a
            # complement are the complement of the up-closure -- the
            # 0041/0046 duality, surfacing as the rule the additive
            # inverse needs (verified: T(~x) = ~U(x))
            out.append(("u-compdual",
                        xor(series("U", xor(argument, OMEGA)), OMEGA)))
        if name == "N":
            nested = _sole_atom(argument)
            if nested is not None and nested[0] == "S" \
                    and nested[1] == "N":
                out.append(("N-absorbN", series("N", nested[2])))
            if nested is not None and nested[0] in ("mul", "cmul", "dil",
                                                    "C"):
                out.append(("N-product", _n_of_product(nested)))
        return out

    if kind == "C":
        left, right = element[1], element[2]
        descend(carry, left, right)
        if left == ZERO:
            out.append(("k-zero", ZERO))
        elif right == ZERO:
            out.append(("k-zero", ZERO))
        if left == ONE:
            out.append(("k-one", series("T", right)))
        elif right == ONE:
            out.append(("k-one", series("T", left)))
        if left == right:
            out.append(("k-same", left))
        shifted_l, shifted_r = _pure_shift(left), _pure_shift(right)
        if shifted_l is not None and shifted_r is not None:
            out.append(("k-shift", shift_a(carry(shifted_l, shifted_r))))
        if conj(left, right) == ZERO:
            out.append(("k-disjoint", ZERO))
        # k-neg: the carry of a number and its negation is the
        # up-closure (verified: C(x, -x) = U(x)). neg is now the
        # two-monomial canonical form, so the match survives inner
        # rewriting -- the k-neg/u-compdual peak is closed by choosing
        # the joined form as the pattern.
        if right == neg(left):
            out.append(("k-neg", series("U", left)))
        elif left == neg(right):
            out.append(("k-neg", series("U", right)))
        return out

    if kind == "mul":
        factors = element[1]

        def rebuild(*fresh):
            return mul(*fresh)
        descend(rebuild, *factors)
        if any(factor == ZERO for factor in factors):
            out.append(("p-zero", ZERO))
        if any(factor == ONE for factor in factors):
            kept = [factor for factor in factors if factor != ONE]
            out.append(("p-unit", mul(*kept)))
        for index, factor in enumerate(factors):
            shifted = _pure_shift(factor)
            if shifted is not None:
                kept = list(factors)
                kept[index] = shifted
                out.append(("p-shift", shift_a(mul(*kept))))
                break
        for index, factor in enumerate(factors):
            if factor == OMEGA:
                kept = factors[:index] + factors[index + 1:]
                out.append(("p-omega", neg(mul(*kept))))
                break
        for index, factor in enumerate(factors):
            # constant with bit 0 KNOWN SET: peel the b-step. Bit 0 is
            # the PARITY of {1-monomial present, Omega present} -- the
            # first soundness audit caught the membership-only guard:
            # mul{Omega ^ 1, y} peeled as if bit 0 were set, but
            # Omega ^ 1 = -2 has bit 0 = 1 ^ 1 = 0.
            # FINITE constants only: a lasso like Omega has infinitely
            # many set bits, and peeling it regresses forever
            # (-x = x + 2(-x) + ...). The first census run showed
            # exactly that blow-up on mul{Omega, x}.
            bit_zero = (ONE <= factor) and frozenset() not in factor
            if factor != ONE and factor != ZERO and \
                    frozenset() not in factor and \
                    _constant_chain(factor) and bit_zero:
                kept = factors[:index] + factors[index + 1:]
                lower = mul(xor(factor, ONE), *kept)
                out.append(("p-const", add(mul(*kept), lower)))
                break
        return out

    if kind == "cmul":
        left, right = element[1], element[2]
        # arguments are monomials; recursion via their atom polys
        if not left or not right:
            pass
        if left == frozenset() or right == frozenset():
            pass
        left_poly = frozenset([left])
        right_poly = frozenset([right])
        descend(lambda p, q: cmul(p, q), left_poly, right_poly)
        if left == frozenset():                  # the monomial Omega
            out.append(("c-omega", series("!", right_poly)))
        elif right == frozenset():
            out.append(("c-omega", series("!", left_poly)))
        if left == frozenset([("one",)]):
            out.append(("c-unit", right_poly))
        elif right == frozenset([("one",)]):
            out.append(("c-unit", left_poly))
        for monomial, other in ((left, right_poly), (right, left_poly)):
            shifted = _pure_shift(frozenset([monomial]))
            if shifted is not None:
                out.append(("c-shift", shift_a(cmul(shifted, other))))
                break
        return out

    if kind == "dil":
        left, right = element[1], element[2]
        descend(dil, left, right)
        if left == ZERO or right == ZERO:
            out.append(("d-zero", ZERO))
        if left == ONE:
            out.append(("d-unit", right))
        elif right == ONE:
            out.append(("d-unit", left))
        if left == OMEGA:
            out.append(("d-omega", series("U", right)))
        elif right == OMEGA:
            out.append(("d-omega", series("U", left)))
        shifted_l, shifted_r = _pure_shift(left), _pure_shift(right)
        if shifted_l is not None:
            out.append(("d-shift", shift_a(dil(shifted_l, right))))
        elif shifted_r is not None:
            out.append(("d-shift", shift_a(dil(left, shifted_r))))
        return out

    return out


def _sole_atom(poly):
    if len(poly) != 1:
        return None
    (atoms,) = poly
    if len(atoms) != 1:
        return None
    (element,) = atoms
    return element


def _n_of_product(element):
    """N over the domain products is multiplicative (0052 s8)."""
    if element[0] == "mul":
        total = OMEGA
        for factor in element[1]:
            total = conj(total, series("N", factor))
        return total
    if element[0] == "cmul":
        return conj(series("N", frozenset([element[1]])),
                    series("N", frozenset([element[2]])))
    if element[0] == "dil":
        return conj(series("N", element[1]), series("N", element[2]))
    if element[0] == "C":
        return series("N", conj(element[1], element[2]))
    raise ValueError(element[0])


def normal_forms(poly, node_cap=6000):
    seen, frontier, forms = {poly}, [poly], set()
    while frontier:
        current = frontier.pop()
        steps = rewrites(current)
        if not steps:
            forms.add(current)
            continue
        for _, result in steps:
            if result not in seen:
                if len(seen) >= node_cap:
                    return forms, True
                seen.add(result)
                frontier.append(result)
    return forms, False


def reduces_to_zero(poly, node_cap=6000) -> bool:
    forms, _ = normal_forms(poly, node_cap)
    return ZERO in forms


# ---------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------

def render(poly) -> str:
    if not poly:
        return "0"
    pieces = []
    for atoms in sorted(poly, key=lambda m: (len(m), sorted(map(str, m)))):
        if not atoms:
            pieces.append("Ω")
            continue
        pieces.append("·".join(_render_atom(e)
                               for e in sorted(atoms, key=str)))
    return " ^ ".join(pieces)


def _render_atom(element) -> str:
    kind = element[0]
    if kind in VARS:
        return kind
    if kind == "one":
        return "1"
    if kind == "a":
        return f"a({render(element[1])})"
    if kind == "S":
        return f"{element[1]}({render(element[2])})"
    if kind == "C":
        return f"C({render(element[1])}, {render(element[2])})"
    if kind == "mul":
        return "mul{" + ", ".join(render(f) for f in element[1]) + "}"
    if kind == "cmul":
        return (f"({render(frozenset([element[1]]))} ⊗ "
                f"{render(frozenset([element[2]]))})")
    if kind == "dil":
        return f"({render(element[1])} ⊞ {render(element[2])})"
    return str(element)


@functools.lru_cache(maxsize=None)
def size(poly) -> int:
    total = 1
    for atoms in poly:
        total += 1
        for element in atoms:
            kind = element[0]
            if kind in LEAF:
                total += 1
            elif kind == "a":
                total += 1 + size(element[1])
            elif kind == "S":
                total += 1 + size(element[2])
            elif kind in ("C", "dil"):
                total += 1 + size(element[1]) + size(element[2])
            elif kind == "mul":
                total += 1 + sum(size(f) for f in element[1])
            elif kind == "cmul":
                total += 1 + size(frozenset([element[1]])) \
                    + size(frozenset([element[2]]))
    return total


# ---------------------------------------------------------------------
# term generators
# ---------------------------------------------------------------------

def random_term(generator, budget):
    choice = generator.random()
    leaves = [X, X, Y, ONE, OMEGA]
    if budget == 0 or choice < 0.3:
        return generator.choice(leaves)
    if choice < 0.45:
        return shift_a(random_term(generator, budget - 1))
    if choice < 0.6:
        name = generator.choice(["!", "U", "T", "N"])
        return series(name, random_term(generator, budget - 1))
    if choice < 0.72:
        kind = generator.choice(["mul", "cmul", "dil", "C"])
        left = random_term(generator, budget - 1)
        right = random_term(generator, budget - 1)
        if kind == "mul":
            return mul(left, right)
        if kind == "cmul":
            return cmul(left, right)
        if kind == "dil":
            return dil(left, right)
        return carry(left, right)
    op = generator.choice([xor, conj])
    return op(random_term(generator, budget - 1),
              random_term(generator, budget - 1))


def redex_pool():
    pool = [
        mul(X, ONE), mul(X, ZERO), mul(X, OMEGA), mul(shift_a(X), Y),
        mul(X, xor(ONE, shift_a(ONE))),               # x * 3
        mul(X, Y, Z), mul(X, X),
        cmul(X, ONE), cmul(X, OMEGA), cmul(shift_a(X), Y), cmul(X, X),
        dil(X, ONE), dil(X, OMEGA), dil(shift_a(X), Y), dil(X, ZERO),
        carry(X, ONE), carry(X, X), carry(shift_a(X), shift_a(Y)),
        carry(X, neg(X)), carry(conj(X, ONE), shift_a(Y)),
        series("N", mul(X, Y)), series("N", carry(X, Y)),
        series("N", cmul(X, Y)), series("N", dil(X, Y)),
        series("T", xor(X, OMEGA)),
        add(X, Y), add(X, ONE), add(X, neg(X)), neg(neg(X)),
        # the fold patterns: random terms never build these (0044's
        # sampling lesson), so they are seeded explicitly
        xor(xor(conj(X, Y), conj(X, shift_a(carry(X, Y)))),
            conj(Y, shift_a(carry(X, Y)))),
        add(mul(X, Y), mul(X, Z)),
        xor(mul(X, add(Y, Z)), add(mul(X, Y), mul(X, Z))),
        conj(carry(X, Y), ONE),
    ]
    return pool


def structured_term(generator, budget):
    if budget == 0 or generator.random() < 0.5:
        return generator.choice(redex_pool())
    op = generator.choice([xor, conj])
    return op(structured_term(generator, budget - 1),
              structured_term(generator, budget - 1))


# ---------------------------------------------------------------------
# 1. soundness
# ---------------------------------------------------------------------

def verify_every_rule_is_sound(trials=350, seed=20261020) -> None:
    generator = random.Random(seed)
    checked, per_rule, broken = 0, {}, []
    for index in range(trials):
        builder = random_term if index % 2 else structured_term
        term = builder(generator, 2)
        for rule, result in rewrites(term):
            checked += 1
            per_rule[rule] = per_rule.get(rule, 0) + 1
            if not equal_low_bits(term, result, seed=index):
                broken.append((rule, render(term), render(result)))
    print(f"  {checked} rule applications, checked at widths 22 and 30")
    print(f"  on the low bits (every operator is LSB-causal, so masked")
    print(f"  evaluation is exact there):")
    for rule in sorted(per_rule, key=per_rule.get, reverse=True):
        print(f"    {rule:<14} {per_rule[rule]:>5}")
    for rule, before, after in broken[:5]:
        print(f"    UNSOUND {rule}: {before}  ->  {after}")
    fired = set(per_rule)
    silent = [rule for rule in RULE_NAMES if rule not in fired]
    print(f"  rules that never fired on the pools: {silent or 'none'}")
    assert not broken
    return per_rule


# ---------------------------------------------------------------------
# 2. constant multiplication coalesces completely
# ---------------------------------------------------------------------

def constant_poly(value: int):
    total = ZERO
    piece = ONE
    for index in range(value.bit_length()):
        if (value >> index) & 1:
            total = xor(total, piece)
        piece = shift_a(piece)
    return total


def _mul_free(poly) -> bool:
    for atoms in poly:
        for element in atoms:
            kind = element[0]
            if kind == "mul":
                return False
            if kind == "a" and not _mul_free(element[1]):
                return False
            if kind == "S" and not _mul_free(element[2]):
                return False
            if kind in ("C", "dil") and not (
                    _mul_free(element[1]) and _mul_free(element[2])):
                return False
            if kind == "cmul" and not (
                    _mul_free(frozenset([element[1]]))
                    and _mul_free(frozenset([element[2]]))):
                return False
    return True


def verify_constant_multiplication_coalesces(seed=20261020) -> None:
    generator = random.Random(seed)
    print(f"    {'c':>3}  mul-free NF reached   evaluates to c·x")
    for value in (2, 3, 5, 6, 7, 11, 13):
        term = mul(X, constant_poly(value))
        forms, capped = normal_forms(term, node_cap=20000)
        free = [form for form in forms if _mul_free(form)]
        assert free, value
        witness = min(free, key=size)
        good = all(evaluate(witness, {"x": v, "y": 0, "z": 0}, 26)
                   == (value * v) & ((1 << 26) - 1)
                   for v in (0, 1, 5, 77, 500, 4093))
        assert good, value
        print(f"    {value:>3}  yes ({len(free)} of {len(forms)} NFs)"
              f"{' ':<9} exact")
    small = min((f for f in normal_forms(
        mul(X, constant_poly(3)), node_cap=20000)[0] if _mul_free(f)),
        key=size)
    print()
    print(f"    3x  -->*  {render(small)}")
    print()
    print("  Every constant multiplication leaves the mul layer entirely:")
    print("  p-const peels one b-step per set bit, p-shift moves the")
    print("  power out, and what remains is the {^, a, C, T} sentence of")
    print("  the addition tier. The peeling needs a KNOWN low bit, which")
    print("  a constant has and a variable does not -- multiplication by")
    print("  a variable cannot leave the layer this way, and that is a")
    print("  wall by design, not by accident.")


# ---------------------------------------------------------------------
# 3. the law table
# ---------------------------------------------------------------------

def verify_the_law_table() -> None:
    laws = [
        ("comm:   xy = yx", xor(mul(X, Y), mul(Y, X)), "construction"),
        ("assoc:  (xy)z = x(yz)",
         xor(mul(mul(X, Y), Z), mul(X, mul(Y, Z))), "construction"),
        ("unit:   x·1 = x", xor(mul(X, ONE), X), "rule"),
        ("zero:   x·0 = 0", mul(X, ZERO), "rule"),
        ("omega:  x·Ω = -x", xor(mul(X, OMEGA), neg(X)), "rule"),
        ("shift:  a(x)·y = a(xy)",
         xor(mul(shift_a(X), Y), shift_a(mul(X, Y))), "rule"),
        ("inverse: x + (-x) = 0", add(X, neg(X)), "completion (k-neg)"),
        ("succ:   x + 1 = x ^ b(T x)",
         xor(add(X, ONE), xor(xor(X, ONE), shift_a(series("T", X)))),
         "rule (k-one)"),
        ("carry-shift: C(ax,ay) = a(C(x,y))",
         xor(carry(shift_a(X), shift_a(Y)),
             shift_a(carry(X, Y))), "rule"),
        ("C-fixpoint: C = xy ^ x·aC ^ y·aC",
         xor(carry(X, Y),
             xor(xor(conj(X, Y),
                     conj(X, shift_a(carry(X, Y)))),
                 conj(Y, shift_a(carry(X, Y))))), "rule (k-fold)"),
        ("C-low: C(x,y)·1 = xy·1",
         xor(conj(carry(X, Y), ONE), conj(conj(X, Y), ONE)),
         "rule (k-low)"),
        ("N-mult: N(xy) = N(x)N(y)",
         xor(series("N", mul(X, Y)),
             conj(series("N", X), series("N", Y))), "rule"),
        ("cmul-Ω: x⊗Ω = !(x)",
         xor(cmul(X, OMEGA), series("!", X)), "rule"),
        ("dil-Ω:  x⊞Ω = U(x)",
         xor(dil(X, OMEGA), series("U", X)), "rule"),
        ("cmul-dist over ^", xor(cmul(xor(X, Y), Z),
                                 xor(cmul(X, Z), cmul(Y, Z))),
         "construction"),
        ("DIST:   x(y+z) = xy + xz",
         xor(mul(X, add(Y, Z)), add(mul(X, Y), mul(X, Z))),
         "rule (p-dist-fold)"),
        # ---- expected failures: the walls ----
        ("cmul-assoc: (x⊗y)⊗z = x⊗(y⊗z)",
         xor(cmul(cmul(X, Y), Z), cmul(X, cmul(Y, Z))), "?"),
        ("dil-dist over |: x⊞(y|z) = x⊞y | x⊞z",
         xor(dil(X, disj(Y, Z)),
             disj(dil(X, Y), dil(X, Z))), "?"),
        ("square: x·x vs x⊗x layer",
         xor(mul(X, X), mul(X, X)), "trivial"),
    ]
    reached, missed = [], []
    for label, statement, how in laws:
        assert equal_low_bits(statement, ZERO), label
        if reduces_to_zero(statement, node_cap=12000):
            reached.append((label, how))
        else:
            missed.append((label, how))
    print("  reduces to 0:")
    for label, how in reached:
        print(f"    {label:<38} [{how}]")
    print()
    print("  does NOT reduce to 0 -- the isolated walls:")
    for label, how in missed:
        print(f"    {label:<38}")
    return reached, missed


def verify_the_frobenius_gap() -> None:
    term = cmul(X, X)
    steps = rewrites(term)
    print(f"    x ⊗ x   rewrites available: {len(steps)}   (irreducible)")
    print()
    print("  x ⊗ x is the position-doubling map (the GF(2) Frobenius:")
    print("  squaring in GF(2)[[t]] doubles exponents). Nothing in the")
    print("  signature names it, no law reaches it, and it is the kernel")
    print("  of the squaring identity x² = (x⊗x) + carries. A coalescing")
    print("  system that wants squares needs this operator NAMED -- the")
    print("  same shape as 0046's two-signature split: the algebra can")
    print("  express it only as a stuck product.")
    assert not steps


# ---------------------------------------------------------------------
# 4. termination audit
# ---------------------------------------------------------------------

def _mul_loads(poly, out):
    for atoms in poly:
        for element in atoms:
            kind = element[0]
            if kind == "mul":
                out.append(sum(len(f) for f in element[1]))
                for factor in element[1]:
                    _mul_loads(factor, out)
            elif kind == "a":
                _mul_loads(element[1], out)
            elif kind == "S":
                _mul_loads(element[2], out)
            elif kind in ("C", "dil"):
                _mul_loads(element[1], out)
                _mul_loads(element[2], out)
            elif kind == "cmul":
                _mul_loads(frozenset([element[1]]), out)
                _mul_loads(frozenset([element[2]]), out)
    return out


def _atom_count(poly) -> int:
    total = 0
    for atoms in poly:
        for element in atoms:
            kind = element[0]
            if kind in LEAF:
                continue
            total += 1
            if kind == "a":
                total += _atom_count(element[1])
            elif kind == "S":
                total += _atom_count(element[2])
            elif kind in ("C", "dil"):
                total += _atom_count(element[1]) + _atom_count(element[2])
            elif kind == "mul":
                total += sum(_atom_count(f) for f in element[1])
            elif kind == "cmul":
                total += _atom_count(frozenset([element[1]])) \
                    + _atom_count(frozenset([element[2]]))
    return total


def _omega_factors(poly) -> int:
    total = 0
    for atoms in poly:
        for element in atoms:
            kind = element[0]
            if kind == "mul":
                total += sum(1 for f in element[1] if f == OMEGA)
                total += sum(_omega_factors(f) for f in element[1])
            elif kind == "a":
                total += _omega_factors(element[1])
            elif kind == "S":
                total += _omega_factors(element[2])
            elif kind in ("C", "dil"):
                total += _omega_factors(element[1])                     + _omega_factors(element[2])
            elif kind == "cmul":
                total += _omega_factors(frozenset([element[1]]))                     + _omega_factors(frozenset([element[2]]))
    return total


def _arg_load(poly) -> int:
    total = 0
    for atoms in poly:
        for element in atoms:
            kind = element[0]
            if kind in LEAF:
                continue
            if kind == "a":
                total += _arg_load(element[1])
            elif kind == "S":
                total += size(element[2]) + _arg_load(element[2])
            elif kind in ("C", "dil"):
                total += size(element[1]) + size(element[2])                     + _arg_load(element[1]) + _arg_load(element[2])
            elif kind == "mul":
                total += sum(size(f) + _arg_load(f) for f in element[1])
            elif kind == "cmul":
                for part in (frozenset([element[1]]),
                             frozenset([element[2]])):
                    total += size(part) + _arg_load(part)
    return total


def measure(poly):
    loads = tuple(sorted(_mul_loads(poly, []), reverse=True))
    return (_omega_factors(poly), loads, _atom_count(poly),
            _arg_load(poly), size(poly))


def _dm_less(after, before):
    """Dershowitz-Manna on multisets of naturals = lex on sorted-desc."""
    if after == before:
        return None
    length = max(len(after), len(before))
    pad_a = after + (-1,) * (length - len(after))
    pad_b = before + (-1,) * (length - len(before))
    return pad_a < pad_b


def audit_termination(trials=900, seed=20261020) -> None:
    generator = random.Random(seed)
    checked, violations = 0, []
    for index in range(trials):
        builder = random_term if index % 2 else structured_term
        term = builder(generator, 2)
        before = measure(term)
        for rule, result in rewrites(term):
            checked += 1
            after = measure(result)
            if after[0] < before[0]:
                ok = True
            elif after[0] > before[0]:
                ok = False
            else:
                loads_verdict = _dm_less(after[1], before[1])
                ok = (loads_verdict is True or
                      (loads_verdict is None and after[2:] < before[2:]))
            if not ok:
                violations.append((rule, render(term)[:60],
                                   before, after))
    print(f"  measure: (Omega-factor count, mul loads under")
    print(f"            Dershowitz-Manna, operator-atom count, argument")
    print(f"            load, size), lexicographic")
    print(f"  {checked} applications audited: {len(violations)} violations")
    seen_rules = {}
    for rule, shown, before, after in violations:
        seen_rules.setdefault(rule, []).append((shown, before, after))
    for rule, cases in seen_rules.items():
        shown, before, after = cases[0]
        print(f"    {rule}: {len(cases)} cases, e.g. {shown}")
        print(f"        {before[:2]} -> {after[:2]}")
    return violations


def audit_search_termination(trials=500, seed=20261020) -> None:
    generator = random.Random(seed)
    capped = 0
    for index in range(trials):
        builder = random_term if index % 2 else structured_term
        term = builder(generator, 2)
        _, hit = normal_forms(term, node_cap=4000)
        capped += hit
    print(f"  {trials} full normal-form searches: {capped} hit the node")
    print(f"  cap (graph too large to exhaust), the rest terminated with")
    print(f"  complete normal-form sets.")


# ---------------------------------------------------------------------
# 5. the peak census
# ---------------------------------------------------------------------

def survey_the_peaks(trials=140, seed=20261020) -> None:
    generator = random.Random(seed)
    joined, unjoined = 0, []
    for index in range(trials):
        builder = random_term if index % 2 else structured_term
        term = builder(generator, 2)
        steps = list(rewrites(term))[:5]
        for (rule_l, left), (rule_r, right) in \
                itertools.combinations(steps, 2):
            if left == right:
                continue
            forms_l, cap_l = normal_forms(left, node_cap=2500)
            forms_r, cap_r = normal_forms(right, node_cap=2500)
            if cap_l or cap_r:
                continue
            if forms_l & forms_r:
                joined += 1
            else:
                unjoined.append((rule_l, rule_r, term))
    print(f"  {joined + len(unjoined)} peaks with exhaustible reducts:")
    print(f"  {joined} share a normal form, {len(unjoined)} do not")
    kinds = {}
    for rule_l, rule_r, _ in unjoined:
        kinds[tuple(sorted((rule_l, rule_r)))] = \
            kinds.get(tuple(sorted((rule_l, rule_r))), 0) + 1
    for pair, count in sorted(kinds.items(), key=lambda kv: -kv[1])[:8]:
        print(f"    {pair[0]} vs {pair[1]}: {count}")
    return unjoined


def run_verification_suite() -> None:
    sections = [
        ("Every rule is sound", verify_every_rule_is_sound),
        ("Constant multiplication coalesces completely",
         verify_constant_multiplication_coalesces),
        ("The law table: what reduces to 0, and the walls",
         verify_the_law_table),
        ("The Frobenius gap", verify_the_frobenius_gap),
        ("Termination audit", audit_termination),
        ("Search termination", audit_search_termination),
        ("Peak census", survey_the_peaks),
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
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    run_verification_suite()
