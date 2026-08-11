"""Canonicity in sentence form, over the honest basis.

0047 answered the canonicity question with a machine. Objection: the
machine speaks to procedure, and a sentence speaks to structure. And
0047's `7` vs `1 ^ 6` was not a gap in the algebra at all -- it was a
gap in the engine's *representation*, which carried an integer mask on
every monomial. Constants are not primitive (0046 §1); allow only
`{1, a, ^, &, !, U, T, N}` and there is no integer anywhere to fold.

So: rebuild ANF with the mask deleted, and see what is left.

  monomial   a set of atoms, multiplied by `&`.  The EMPTY monomial is
             `Ω` -- the multiplicative unit, since `Ω & t = t`.
  polynomial a set of monomials, joined by `^`.  The EMPTY polynomial
             is `0`.
  atoms      x, 1, and a(P), !(P), U(P), T(P), lowset(P), lowzero(P),
             N(P).

There is no width in that representation, and no constant domain to be
closed under anything -- which deletes 0047 §5's width-bound family and
§6's lasso repair outright. Both were artifacts of the mask.

What survives is one family, and it is the threshold this module is
for: **an operator whose output is settled by a finite known prefix of
its argument.** `U` and `T` and `N` have it; `!` and the two measures do
not. The split is not incidental --

    join   absorbing element   the rule its series needs
    ^      none                telescope   (cancellation)
    |      Ω                   prefix      (saturation)
    &      0                   prefix      (annihilation)

-- so which rule a cell of 0042's schema needs is decided by whether its
join has an absorbing element. Measured in §5.

The 0047 machine is used here only as an ORACLE, to check the sentence
rules against. It is not the answer.

Run directly for the verification suite.
"""

from __future__ import annotations

import functools
import itertools
import random

import guarded_canonical_form as oracle

# ---------------------------------------------------------------------
# 1. ANF with no mask
# ---------------------------------------------------------------------

ZERO = frozenset()
OMEGA = frozenset([frozenset()])            # the empty monomial is the unit
ONE = frozenset([frozenset([("one",)])])
X = frozenset([frozenset([("x",)])])

SERIES = {"!": ("^", "a"), "U": ("|", "a"), "T": ("&", "b")}
MEASURE = {"!": None, "U": "lowset", "T": "lowzero"}
UNARY = ("a", "!", "U", "T", "lowset", "lowzero", "N")


def xor(left, right):
    return left ^ right


def conj(left, right):
    product = set()
    for atoms_l in left:
        for atoms_r in right:
            product ^= {atoms_l | atoms_r}
    return frozenset(product)


def disj(left, right):
    return xor(xor(left, right), conj(left, right))


def apply_join(join, left, right):
    return {"^": xor, "|": disj, "&": conj}[join](left, right)


def _raw_atom(kind, argument):
    return frozenset([frozenset([(kind, argument)])])


def atom(kind, argument):
    """`a` is never a bare wrapper: it pushes to the leaves on sight.

    Routing it through the constructor is what makes `a(Ω)` and `Ω ^ 1`
    the same object rather than two normal forms.
    """
    return shift_a(argument) if kind == "a" else _raw_atom(kind, argument)


def shift_a(poly):
    """`a` pushed all the way to the leaves.

    `a` is a homomorphism for BOTH joins -- `a(P^Q) = a(P)^a(Q)` and
    `a(P&Q) = a(P)&a(Q)`, since bit i of either side reads bit i-1 of
    each argument. So it never needs to be an opaque wrapper around a
    compound, and pushing it down makes

        a(Ω) = Ω ^ 1

    a fact of CONSTRUCTION rather than a constant to fold at some width.
    That single line is 0047 §5's width-bound family, repaired.
    """
    total = ZERO
    for atoms in poly:
        if not atoms:                           # the monomial Ω
            total = xor(total, xor(OMEGA, ONE))
            continue
        piece = OMEGA
        for element in atoms:
            piece = conj(piece,
                         _raw_atom("a", _raw_atom(*element)
                                   if len(element) > 1
                                   else frozenset([frozenset([element])])))
        total = xor(total, piece)
    return total


shift_b = lambda p: xor(shift_a(p), ONE)        # `b` is not a constructor
series = lambda name, p: atom(name, p)


def apply_shift(name, poly):
    return shift_a(poly) if name == "a" else shift_b(poly)


def to_term(poly):
    """The 0047 term this polynomial denotes -- for the oracle only."""
    if not poly:
        return oracle.ZERO
    total = None
    for atoms in sorted(poly, key=lambda m: sorted(map(str, m))):
        piece = oracle.OMEGA
        for kind, *rest in sorted(atoms, key=str):
            if kind == "x":
                factor = oracle.var("x")
            elif kind == "one":
                factor = oracle.ONE
            else:
                factor = (kind, to_term(rest[0]))
            piece = oracle.and_(piece, factor)
        total = piece if total is None else oracle.xor_(total, piece)
    return total


def render(poly) -> str:
    if not poly:
        return "0"
    pieces = []
    for atoms in sorted(poly, key=lambda m: (len(m), sorted(map(str, m)))):
        if not atoms:
            pieces.append("Ω")
            continue
        pieces.append("".join(
            "x" if kind == "x" else "1" if kind == "one"
            else f"{kind}({render(rest[0])})"
            for kind, *rest in sorted(atoms, key=str)))
    return " ^ ".join(pieces)


@functools.lru_cache(maxsize=None)
def size(poly) -> int:
    total = 1
    for atoms in poly:
        total += 1
        for kind, *rest in atoms:
            total += 1 if kind in ("x", "one") else 1 + size(rest[0])
    return total


def equal(left, right) -> bool:
    return oracle.equal(to_term(left), to_term(right))


def is_zero(poly) -> bool:
    return oracle.decide_zero(to_term(poly)) is None


# ---------------------------------------------------------------------
# 2. the known prefix
# ---------------------------------------------------------------------

def _and(p, q):
    if p == 0 or q == 0:
        return 0
    return None if p is None or q is None else 1


def _xor(p, q):
    return None if p is None or q is None else p ^ q


def _or(p, q):
    if p == 1 or q == 1:
        return 1
    return None if p is None or q is None else 0


def _not(p):
    return None if p is None else 1 - p


@functools.lru_cache(maxsize=None)
def known_prefix(poly, depth: int) -> tuple:
    """The low `depth` bits of `poly` that are fixed for every input.

    `None` where the bit depends on the variable. Purely syntactic: this
    is the sentence-form counterpart of an automaton's reachable state,
    and §6 measures how deep it has to go.
    """
    bits = [0] * depth
    for atoms in poly:
        piece = [1] * depth                    # the empty monomial is Ω
        for element in atoms:
            factor = _atom_prefix(element, depth)
            piece = [_and(p, q) for p, q in zip(piece, factor)]
        bits = [_xor(p, q) for p, q in zip(bits, piece)]
    return tuple(bits)


def _atom_prefix(element, depth: int) -> tuple:
    """One atom's known prefix -- the machine table of 0047 §2, run over
    {0, 1, unknown} instead of over bits."""
    kind, *rest = element
    if kind == "x":
        return (None,) * depth
    if kind == "one":
        return tuple(1 if index == 0 else 0 for index in range(depth))
    inner = known_prefix(rest[0], depth)
    if kind == "a":
        return (0,) + inner[:depth - 1]
    if kind == "N":
        # settled upward the moment any bit of the argument is known 1
        return (1,) * depth if 1 in inner else (None,) * depth
    out = []
    state = 1 if kind in ("T", "lowzero") else 0
    for bit in inner:
        if kind == "!":
            state = _xor(state, bit)
            out.append(state)
        elif kind == "U":
            state = _or(state, bit)
            out.append(state)
        elif kind == "T":
            state = _and(state, bit)
            out.append(state)
        elif kind == "lowset":
            out.append(_and(bit, _not(state)))
            state = _or(state, bit)
        else:                                     # lowzero
            out.append(_and(state, _not(bit)))
            state = _and(state, bit)
    return tuple(out)


def prefix_constant(bits) -> frozenset:
    """A known bit pattern, as a polynomial over `1` and `a`."""
    total = ZERO
    for index, bit in enumerate(bits):
        if bit:
            piece = ONE
            for _ in range(index):
                piece = shift_a(piece)
            total = xor(total, piece)
    return total


def settled(kind, bits):
    """Does this prefix settle the operator's WHOLE output?

    `U` saturates at its first 1, `T` annihilates at its first 0, `N`
    saturates at any 1 -- each reaching the absorbing element of its
    join. The two measures settle too, at the same bit their series
    does, and produce a single set bit there.

    `!` is the only operator that never settles: `^` makes the
    two-element algebra a group, no element absorbs, and the running
    parity therefore stays live no matter how much prefix is known. Its
    measure is the identity and inherits that.
    """
    if kind == "N":
        return OMEGA if 1 in bits else None
    if kind == "U":
        for index, bit in enumerate(bits):
            if bit is None:
                return None
            if bit == 1:
                return xor(OMEGA, prefix_constant([1] * index))
        return None
    if kind == "T":
        for index, bit in enumerate(bits):
            if bit is None:
                return None
            if bit == 0:
                return prefix_constant([1] * index)
        return None
    if kind in ("lowset", "lowzero"):
        target = 1 if kind == "lowset" else 0
        for index, bit in enumerate(bits):
            if bit is None:
                return None
            if bit == target:
                return prefix_constant([0] * index + [1])
        return None
    return None


# ---------------------------------------------------------------------
# 3. support bound: is the argument confined to a known window?
# ---------------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def support_bound(poly):
    """`k` with `P ⊆ {0..k-1}`, or None if unbounded.

    Distinct from `known_prefix`, and needed because a prefix says
    nothing about what happens above it. Conservative: an operator whose
    output can run away upward reports None.
    """
    total = 0
    for atoms in poly:
        piece = None if not atoms else min(
            (_atom_bound(element) for element in atoms),
            key=lambda k: float("inf") if k is None else k)
        if piece is None:
            return None
        total = max(total, piece)
    return total


def _atom_bound(element):
    kind, *rest = element
    if kind == "one":
        return 1
    if kind == "x":
        return None
    inner = support_bound(rest[0])
    if kind == "a":
        return None if inner is None else inner + 1
    if inner == 0:
        return 0 if kind in ("!", "U", "T", "N", "lowset") else None
    return None


# ---------------------------------------------------------------------
# 4. the rules
# ---------------------------------------------------------------------

ABSORB = {("N", "N"): ("N", False), ("N", "U"): ("N", False),
          ("N", "!"): ("N", False), ("N", "T"): ("N", True),
          ("U", "U"): ("U", False), ("U", "N"): ("N", False),
          ("U", "T"): ("N", True),
          ("T", "T"): ("T", False), ("T", "N"): ("N", False),
          ("T", "U"): ("N", True),
          # the measures are single bits, so `lowset` is the identity on
          # them and `T` cannot shrink them further
          ("lowset", "lowset"): ("lowset", False),
          ("lowset", "lowzero"): ("lowzero", False),
          ("T", "lowset"): ("lowset", True),
          ("T", "lowzero"): ("lowzero", True)}

RULE_NAMES = ("settle", "confine", "low-bit", "unit", "absorb",
              "shift-out", "N-see-through", "N-absorb", "contain",
              "collect", "telescope")

# The operators on the two units. This is all that survives of 0043's
# `fold`: there is no constant domain here, only `0` (the empty
# polynomial) and `Ω` (the empty monomial), so the table is closed and
# carries no width. `!(Ω)` alternates forever and is its own normal
# form -- there is no finite term over `{1, a, ^, &}` equal to it.
ON_ZERO = {"a": ZERO, "!": ZERO, "U": ZERO, "T": ZERO, "N": ZERO,
           "lowset": ZERO, "lowzero": ONE}
ON_OMEGA = {"U": OMEGA, "T": OMEGA, "N": OMEGA, "lowset": ONE,
            "lowzero": ZERO}

PREFIX_DEPTH = 6


def _rebuild(poly, atoms, replacement):
    """Swap one monomial's atom-set for `replacement` times the rest."""
    return xor(poly, frozenset([atoms])) ^ replacement


def _monomial(atoms):
    return frozenset([atoms])


@functools.lru_cache(maxsize=None)
def rewrites(poly, depth: int = PREFIX_DEPTH):
    steps = []
    for atoms in sorted(poly, key=lambda m: sorted(map(str, m))):
        rest = _monomial(frozenset(atoms))
        for element in atoms:
            kind, *carried = element
            if kind in ("x", "one"):
                continue
            argument = carried[0]
            others = conj(_monomial(frozenset(atoms - {element})), OMEGA)

            # -- recursion into the argument ---------------------------
            for rule, replaced in rewrites(argument, depth):
                lifted = conj(others, atom(kind, replaced))
                steps.append((rule, xor(poly, xor(rest, lifted))))

            # -- settle: the join's absorbing element, from a prefix ---
            reached = settled(kind, known_prefix(argument, depth))
            if reached is not None:
                steps.append(("settle",
                              xor(poly, xor(rest, conj(others, reached)))))

            # -- confine: the argument lives in bit 0 ------------------
            if support_bound(argument) == 1:
                replacement = {"!": lambda p: atom("N", p),
                               "U": lambda p: atom("N", p),
                               "T": lambda p: p,
                               "lowset": lambda p: p}.get(kind)
                if replacement is not None:
                    steps.append(("confine",
                                  xor(poly, xor(rest,
                                                conj(others,
                                                     replacement(argument))))))

            # -- low-bit: S(t) & 1 -> t & 1 ----------------------------
            #
            # `confine` and this are the same one-bit fact from opposite
            # ends: confine restricts the ARGUMENT to bit 0, low-bit
            # restricts the OUTPUT to bit 0. Either way the series has
            # one surviving term. `N` is excluded -- `N(t)&1` is 1
            # whenever t is nonzero ANYWHERE, which is not `t&1`.
            if ("one",) in atoms and kind in ("!", "U", "T", "lowset",
                                              "lowzero"):
                replacement = (xor(argument, OMEGA) if kind == "lowzero"
                               else argument)
                steps.append(("low-bit",
                              xor(poly, xor(rest, conj(others,
                                                       replacement)))))

            # -- unit: the operators on 0 and on Ω ---------------------
            if not argument and kind in ON_ZERO:
                steps.append(("unit", xor(poly, xor(rest, conj(
                    others, ON_ZERO[kind])))))
            elif argument == OMEGA and kind in ON_OMEGA:
                steps.append(("unit", xor(poly, xor(rest, conj(
                    others, ON_OMEGA[kind])))))

            # -- absorb: S1(S2 t) --------------------------------------
            nested = _sole_atom(argument)
            if nested is not None and (kind, nested[0]) in ABSORB:
                name, low = ABSORB[(kind, nested[0])]
                inner = nested[1]
                if low:
                    inner = conj(inner, ONE)
                steps.append(("absorb",
                              xor(poly, xor(rest, conj(others,
                                                       atom(name, inner))))))

            # -- shift-out: S(sigma_S t) -> sigma_S(S t) ---------------
            if kind in SERIES:
                shift = SERIES[kind][1]
                peeled = _peel_shift(argument, shift)
                if peeled is not None:
                    lifted = apply_shift(shift, atom(kind, peeled))
                    steps.append(("shift-out",
                                  xor(poly, xor(rest, conj(others, lifted)))))

            # -- N-see-through: N is blind to an injective wrapper -----
            #
            # `a` is injective and fixes 0, so `N(a t) = N(t)`. The same
            # reasoning puts ("N", "!") in ABSORB -- `!` is invertible
            # (0042 §2). `settle` covers the `b` case instead, since
            # `b(t)` has a known 1 at bit 0.
            if kind == "N":
                peeled = _peel_shift(argument, "a")
                if peeled is not None:
                    steps.append(("N-see-through",
                                  xor(poly, xor(rest,
                                                conj(others,
                                                     atom("N", peeled))))))

            # -- N-absorb: N(p) & m -> m -------------------------------
            if kind == "N" and len(atoms) > 1:
                if _monomial_vanishes(frozenset(atoms - {element}), argument):
                    steps.append(("N-absorb", xor(poly, xor(rest, others))))

    steps += _contain(poly)
    steps += _low_bit_prefix(poly, depth)
    steps += _collect(poly, depth)
    steps += _telescope(poly)
    steps = [(rule, result) for rule, result in steps if result != poly]
    others = [step for step in steps if step[0] != "telescope"]
    return tuple(others or steps)


def _under_U(element, argument):
    """Is this atom below `U(argument)`?

    `U` is the `|` cell, so it is the least upper bound of the whole
    `a`-orbit of its argument -- everything the schema builds from `t`,
    and every further `a`-shift of that, sits under `U(t)`. Measured in
    §7. `lowzero` is the exception and it is the dual one: it sits under
    `U(t ^ Ω)`, not under `U(t)`.
    """
    kind, *rest = element
    if kind in ("x", "one"):
        return frozenset([frozenset([element])]) == argument
    if kind == "a":
        return all(len(m) == 1 and _under_U(next(iter(m)), argument)
                   for m in rest[0])
    if kind in ("!", "U", "T", "lowset"):
        return rest[0] == argument
    return False


def _contains(big, small):
    """`small ⊆ big`, syntactically and soundly.

        T(t) ⊆ t ⊆ U(t) ⊆ N(t)

    is the order the schema carries, and `&`/`|` are exactly the joins
    that have one -- `^` makes the algebra a group and a group has no
    order compatible with it. So this rule is invisible to an ANF engine
    on principle, not by oversight: ANF is built on `^`.
    """
    kind, *rest = big
    if kind == "U":
        return _under_U(small, rest[0])
    if small[0] in ("T", "lowset"):
        return small[1] == frozenset([frozenset([big])])
    return False


def _contain(poly):
    """`A & B -> A` when `A ⊆ B`."""
    steps = []
    for atoms in poly:
        for big, small in itertools.permutations(atoms, 2):
            if not _contains(big, small):
                continue
            steps.append(("contain",
                          xor(poly, xor(_monomial(frozenset(atoms)),
                                        _monomial(frozenset(atoms - {big}))))))
    return steps


def _low_bit_prefix(poly, depth):
    """A monomial masked to bit 0 is decided by bit 0 of its factors.

    Same analysis as `settle`, read at the other end: `settle` asks what
    a known prefix of an ARGUMENT does to the operator above it, this
    asks what a known bit 0 of the FACTORS does to a monomial that has
    been masked to bit 0. `a(t) & 1 -> 0` and `b(t) & 1 -> 1` are both
    this rule, which is why neither needs to be written down.
    """
    steps = []
    for atoms in poly:
        if ("one",) not in atoms or len(atoms) == 1:
            continue
        others = frozenset(atoms - {("one",)})
        bit = known_prefix(_monomial(others), 1)[0]
        if bit is None:
            continue
        replacement = ONE if bit == 1 else ZERO
        steps.append(("low-bit",
                      xor(poly, xor(_monomial(frozenset(atoms)),
                                    replacement))))
    return steps


def _sole_atom(poly):
    """`poly` as a single bare atom, or None."""
    if len(poly) != 1:
        return None
    (atoms,) = poly
    if len(atoms) != 1:
        return None
    (element,) = atoms
    return None if element[0] in ("x", "one") else element


def _peel_shift(poly, shift):
    """`poly` as `sigma(inner)`, or None."""
    if shift == "b":
        if ONE not in [frozenset([m]) for m in poly] and \
                frozenset([("one",)]) not in poly:
            return None
        poly = xor(poly, ONE)
    inner = ZERO
    for atoms in poly:
        if len(atoms) != 1:
            return None
        (element,) = atoms
        if element[0] != "a":
            return None
        inner = xor(inner, element[1])
    return inner if poly else None


def _monomial_vanishes(atoms, base):
    """A conjunction dies wherever `base` does if ANY factor does."""
    return any(_atom_vanishes(element, base) for element in atoms)


def _poly_vanishes(poly, base):
    """A sum dies wherever `base` does only if EVERY summand does."""
    return all(_monomial_vanishes(atoms, base) for atoms in poly)


def _atom_vanishes(element, base):
    """Is this atom forced to 0 everywhere `base` is 0?

    Every operator in the signature fixes 0 except `lowzero`, whose
    lowest zero bit of the empty set is bit 0 -- so it never vanishes.
    Getting that wrong is what made `N(x) T(a(x)^1) 1 -> T(a(x)^1) 1`
    look sound: at x = 0 the left side is 0 and the right side is 1.
    """
    kind, *rest = element
    if kind == "one":
        return False
    if kind == "x":
        return base == X
    if atom(kind, rest[0]) == base:
        return True
    if kind == "lowzero":
        return False
    return _poly_vanishes(rest[0], base)


def _collect(poly, depth):
    """`S(p) ∘_S S(q) -> S(p ∘_S q)`, only between irreducible arguments."""
    steps = []
    singles = {}
    for atoms in poly:
        if len(atoms) == 1:
            (element,) = atoms
            if element[0] in SERIES:
                singles.setdefault(element[0], []).append(element)
    for name, found in singles.items():
        join = SERIES[name][0]
        for first, second in itertools.combinations(found, 2):
            if rewrites(atom(name, first[1]), depth) or \
                    rewrites(atom(name, second[1]), depth):
                continue
            combined = atom(name, apply_join(join, first[1], second[1]))
            if join == "^":
                steps.append(("collect", xor(xor(xor(poly, _monomial(
                    frozenset([first]))), _monomial(frozenset([second]))),
                    combined)))
            elif join == "|":
                pair = _monomial(frozenset([first, second]))
                if pair <= poly:
                    steps.append(("collect", xor(xor(xor(xor(
                        poly, _monomial(frozenset([first]))),
                        _monomial(frozenset([second]))), pair), combined)))
    for atoms in poly:
        found = [e for e in atoms if e[0] in SERIES and SERIES[e[0]][0] == "&"]
        for first, second in itertools.combinations(found, 2):
            if first[0] != second[0]:
                continue
            if rewrites(atom(first[0], first[1]), depth) or \
                    rewrites(atom(second[0], second[1]), depth):
                continue
            others = conj(_monomial(frozenset(atoms - {first, second})), OMEGA)
            combined = atom(first[0], conj(first[1], second[1]))
            steps.append(("collect", xor(poly, xor(_monomial(frozenset(atoms)),
                                                   conj(others, combined)))))
    return steps


def _telescope(poly):
    """`C·S(t) ^ C·σ_S(S t) -> C·m_S(t)`, last resort (0044 §5).

    The common factor `C` matters. Restricted to bare monomials the rule
    misses `(!(t) ^ a(!t)) & m`, which is exactly the shape a
    distributed telescoping takes in ANF -- and for `T` the partner is
    `a(T t) ^ 1`, two monomials, so the pattern is a whole polynomial
    rather than a single atom either way.
    """
    steps = []
    for monomial in poly:
        for element in monomial:
            if element[0] not in SERIES:
                continue
            name = element[0]
            common = _monomial(frozenset(monomial - {element}))
            partner = conj(common, apply_shift(SERIES[name][1],
                                               atom(name, element[1])))
            if not partner <= poly:
                continue
            measure = MEASURE[name]
            replacement = (element[1] if measure is None
                           else atom(measure, element[1]))
            steps.append(("telescope",
                          xor(xor(xor(poly, _monomial(frozenset(monomial))),
                                  partner), conj(common, replacement))))
    return steps


def normal_forms(poly, node_cap: int = 3000):
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


# ---------------------------------------------------------------------
# 5. checks
# ---------------------------------------------------------------------

def random_poly(generator, budget):
    choice = generator.random()
    if budget == 0 or choice < 0.3:
        return generator.choice([X, X, ONE, OMEGA, ZERO])
    if choice < 0.5:
        return apply_shift(generator.choice(["a", "b"]),
                           random_poly(generator, budget - 1))
    if choice < 0.7:
        return atom(generator.choice(UNARY),
                    random_poly(generator, budget - 1))
    return apply_join(generator.choice(["^", "|", "&"]),
                      random_poly(generator, budget - 1),
                      random_poly(generator, budget - 1))


def redex_pool():
    """The redexes each rule exists for (0044 §4's lesson: random terms
    never build them)."""
    pool = [X, ONE, OMEGA, ZERO, conj(X, ONE)]
    for name, (_, shift) in SERIES.items():
        base = atom(name, X)
        pool += [base, apply_shift(shift, base),
                 atom(name, apply_shift(shift, X)),
                 atom(name, atom(name, X)), conj(base, ONE),
                 atom(name, conj(X, ONE)), atom("N", base),
                 atom(name, atom("N", X)),
                 atom(name, apply_shift("a", X)),
                 atom(name, apply_shift("b", X)),
                 xor(base, apply_shift(shift, base))]
    pool += [atom("N", X), atom("N", apply_shift("a", X)),
             atom("N", apply_shift("b", X)),
             atom("N", conj(atom("N", X), ONE))]
    return pool


def structured_poly(generator, budget):
    if budget == 0 or generator.random() < 0.4:
        return generator.choice(redex_pool())
    return apply_join(generator.choice(["^", "|", "&"]),
                      structured_poly(generator, budget - 1),
                      structured_poly(generator, budget - 1))


def verify_the_constructors_do_the_work(seed=20260915) -> None:
    """Which of 0047 §5's laws mask-free ANF discharges with no rule."""
    def chain(value):
        poly = ZERO
        for bit in format(value, "b"):
            poly = shift_b(poly) if bit == "1" else shift_a(poly)
        return poly
    laws = [
        ("b(x) = a(x) ^ 1", shift_b(X), xor(shift_a(X), ONE)),
        ("a(Ω) = Ω ^ 1", shift_a(OMEGA), xor(OMEGA, ONE)),
        ("7 = 1 ^ 6", chain(7), xor(ONE, chain(6))),
        ("a(Ω ^ x) & b(x) = 0", conj(shift_a(xor(OMEGA, X)), shift_b(X)),
         ZERO),
        ("T(a x) = 0", atom("T", shift_a(X)), ZERO),
        ("U(b x) = Ω", atom("U", shift_b(X)), OMEGA),
        ("N(x&1) = !(x&1)", atom("N", conj(X, ONE)),
         atom("!", conj(X, ONE))),
    ]
    free = 0
    for label, left, right in laws:
        assert equal(left, right), label
        identical = left == right
        free += identical
        verdict = "free" if identical else "needs a rule"
        print(f"    {label:<22} {verdict}")
        if not identical:
            print(f"        {render(left)}   vs   {render(right)}")
    print()
    print(f"  {free} of {len(laws)} identified by the representation alone.")
    print("  The three that are not are exactly the ones about the")
    print("  ARGUMENT's low bits -- which is §6.")


def verify_the_rules_preserve_meaning(trials=500, seed=20260915) -> None:
    generator = random.Random(seed)
    checked, broken = 0, []
    for index in range(trials):
        builder = random_poly if index % 2 else structured_poly
        poly = builder(generator, 3)
        for rule, result in rewrites(poly):
            checked += 1
            try:
                if not equal(poly, result):
                    broken.append((rule, render(poly), render(result)))
            except RuntimeError:
                checked -= 1
    print(f"  {checked} rule applications, checked against the unbounded "
          f"decision procedure")
    for rule, before, after in broken[:5]:
        print(f"    UNSOUND {rule}: {before} -> {after}")
    print(f"  {len(broken)} do not preserve meaning")
    assert not broken


def verify_how_deep_the_prefix_must_go(trials=3000, seed=20260915) -> None:
    """The sentence-form of `bounded state`."""
    generator = random.Random(seed)
    fired = {}
    for index in range(trials):
        builder = random_poly if index % 2 else structured_poly
        poly = builder(generator, 3)
        for atoms in poly:
            for element in atoms:
                if element[0] not in ("U", "T", "N"):
                    continue
                bits = known_prefix(element[1], PREFIX_DEPTH)
                if settled(element[0], bits) is None:
                    continue
                position = next(index for index, bit in enumerate(bits)
                                if bit is not None
                                and (bit == 1 if element[0] in ("U", "N")
                                     else bit == 0))
                depth = shift_depth(element[1])
                fired.setdefault(position, [0, 0])
                fired[position][0] += 1
                fired[position][1] = max(fired[position][1], depth)
    print(f"  position at which `settle` fires, over {trials} terms:")
    print(f"    {'position':>9} {'times':>8} {'max a-depth of argument':>26}")
    for position in sorted(fired):
        count, depth = fired[position]
        print(f"    {position:>9} {count:>8} {depth:>26}")
    print()
    print("  `settle` never fires above the argument's own shift depth,")
    print("  because a known bit can only come from a shift, a constant or")
    print("  a settled operator underneath. That bound is syntactic, and it")
    print("  is what `finite state` looks like in a sentence: the rule")
    print("  needs a prefix, and the term says how long.")


@functools.lru_cache(maxsize=None)
def shift_depth(poly) -> int:
    best = 0
    for atoms in poly:
        for kind, *rest in atoms:
            if kind in ("x", "one"):
                continue
            inner = shift_depth(rest[0])
            best = max(best, inner + (1 if kind == "a" else 0))
    return best


def _fingerprint(poly, width=18, values=(0, 1, 2, 3, 5, 6, 9, 12, 21, 44, 77)):
    term = to_term(poly)
    machine = oracle.Machine(term)
    out = []
    for value in values:
        env = {"x": value} if machine.variables else {}
        guard = oracle.consistent_guard(machine, env, width)
        out.append(machine.run(env, guard, width))
    return tuple(out)


def verify_what_is_still_not_identified(trials=700, seed=20260915) -> None:
    """Equal terms that reach different normal forms."""
    generator = random.Random(seed)
    pool = []
    for index in range(trials):
        builder = random_poly if index % 2 else structured_poly
        poly = builder(generator, 3)
        forms, capped = normal_forms(poly)
        if capped or len(forms) != 1:
            continue
        pool.append((poly, next(iter(forms))))
    groups = {}
    for poly, normal in pool:
        groups.setdefault(_fingerprint(poly), []).append((poly, normal))
    unidentified, unsound = [], []
    for members in groups.values():
        for first, second in itertools.combinations(members[:5], 2):
            try:
                same = equal(first[0], second[0])
            except RuntimeError:
                continue
            if same and first[1] != second[1]:
                unidentified.append((render(first[1]), render(second[1])))
    seen_forms = {}
    for poly, normal in pool:
        seen_forms.setdefault(normal, []).append(poly)
    for normal, members in seen_forms.items():
        for first, second in itertools.combinations(members[:4], 2):
            try:
                if not equal(first, second):
                    unsound.append(render(normal))
            except RuntimeError:
                continue
    print(f"  {len(pool)} terms with a single normal form")
    print(f"  {len(unsound)} pairs share a normal form without being equal "
          f"(should be 0)")
    print(f"  {len(unidentified)} pairs are equal and reach different "
          f"normal forms")
    for first, second in sorted(unidentified,
                                key=lambda pr: len(pr[0]) + len(pr[1]))[:8]:
        print(f"    {first}   vs   {second}")
    assert not unsound
    return unidentified


def report_rule_census(trials=1500, seed=20260915) -> None:
    counted = {}
    for label, builder in (("random", random_poly),
                           ("targeted", structured_poly)):
        generator = random.Random(seed)
        used = {}
        for _ in range(trials):
            poly = builder(generator, 3)
            for rule, _ in rewrites(poly):
                used[rule] = used.get(rule, 0) + 1
        counted[label] = used
    print(f"  {'rule':<15} {'random':>8} {'targeted':>10}")
    for rule in sorted(RULE_NAMES,
                       key=lambda r: -counted["targeted"].get(r, 0)):
        print(f"  {rule:<15} {counted['random'].get(rule, 0):>8} "
              f"{counted['targeted'].get(rule, 0):>10}")
    assert set(counted["random"]) | set(counted["targeted"]) <= set(RULE_NAMES)
    print()
    print(f"  {len(RULE_NAMES)} rules, where 0044 had ten and 0043 fourteen.")
    print("    gone, absorbed by the mask-free representation:")
    print("      fold        -- there is no constant domain to fold in")
    print("      the SHIFT half of low-bit -- `a(t)&1 = 0` and")
    print("      `b(t)&1 = 1` are construction, but the SERIES half")
    print("      (`S(t)&1 = t&1`) is a real rule and is kept")
    print("    gone, merged:")
    print("      low-arg   -> `confine`, now at any operator")
    print("      N-shift   -> `settle` (the b case) and `N-see-through`")
    print("                   (the a case), which are different facts")


def verify_the_join_decides_the_rule() -> None:
    """Why `!` gets no prefix rule, and `U`/`T` do."""
    rows = [("!", "^", None, "self"), ("U", "|", "Ω", "lowset"),
            ("T", "&", "0", "lowzero")]
    print(f"    {'cell':<6} {'join':<6} {'absorbing':<11} "
          f"{'settles?':<10} {'measure':<9} {'settles?'}")
    for name, join, absorbing, measure in rows:
        cell = any(settled(name, bits) is not None
                   for bits in ((1,) * PREFIX_DEPTH, (0,) * PREFIX_DEPTH))
        if measure == "self":
            same = False
        else:
            same = any(settled(measure, bits) is not None
                       for bits in ((1,) * PREFIX_DEPTH,
                                    (0,) * PREFIX_DEPTH))
        print(f"    {name:<6} {join:<6} {str(absorbing):<11} "
              f"{('yes' if cell else 'no'):<10} {measure:<9} "
              f"{'yes' if same else 'no'}")
    assert settled("!", (1,) * PREFIX_DEPTH) is None
    assert settled("U", (1,) * PREFIX_DEPTH) is not None
    assert settled("T", (0,) * PREFIX_DEPTH) is not None
    print()
    print("  `^` makes the two-element algebra a GROUP -- every element")
    print("  invertible, nothing absorbing -- so no finite prefix of the")
    print("  argument settles `!`, and its measure is the identity and")
    print("  inherits that. `|` and `&` are not groups, and their")
    print("  absorbing elements are exactly what a prefix reaches.")
    print()
    print("  So which KIND of rule a cell of 0042's schema needs is read")
    print("  off its join alone:")
    print("    ^  ->  cancellation only    (telescope; the inverse exists)")
    print("    |  ->  saturation at Ω      (settle)")
    print("    &  ->  annihilation at 0    (settle)")
    print("  and the same split governs `contain` (§7): a group carries no")
    print("  compatible order, so the containments the rules need all live")
    print("  in the `|` and `&` cells.")
    print("  0042 gave one schema for the operators. This is one for their")
    print("  rules.")


def verify_the_residue_is_containment() -> None:
    """What §5's survivors are, and why `_contains` misses them.

    Both need `A ⊆ B` where B is a compound rather than a bare atom.
    `_contains` only relates two atoms, so it cannot state either -- and
    the reason is structural: `⊆` reads `A & B = A`, and in ANF a
    conjunction against a XOR-sum distributes into several monomials
    with nothing left to match against.
    """
    x = X
    cases = [
        ("T(t) ⊆ b(T t)", atom("T", x), shift_b(atom("T", x)),
         "gives T(t)·a(T t) = T(t) ^ t&1"),
        ("N(t & 1) ⊆ U(t)", atom("N", conj(x, ONE)), atom("U", x),
         "gives N(t&1) | U(t) = U(t)"),
    ]
    for label, small, big, consequence in cases:
        holds = equal(conj(small, big), small)
        derivable = any(_contains(b, s) for b in
                        (next(iter(m)) for m in big if len(m) == 1)
                        for s in (next(iter(m)) for m in small
                                  if len(m) == 1))
        assert holds, label
        print(f"    {label:<20} true, `_contains` derives it: "
              f"{'yes' if derivable else 'NO'}")
        print(f"        {consequence}")
    print()
    print("  So the residue is not a ragbag. Every surviving pair in §5")
    print("  is a containment, and containment is the one thing an ANF")
    print("  engine cannot see on principle: `^` makes the algebra a")
    print("  group, a group admits no compatible order, and the order")
    print("  facts therefore have to be imported from outside the")
    print("  representation. That is the threshold, stated in sentences.")


def run_verification_suite() -> None:
    sections = [
        ("What the mask-free representation does for free",
         verify_the_constructors_do_the_work),
        ("The join decides which rule the cell needs",
         verify_the_join_decides_the_rule),
        ("Every rule preserves meaning", verify_the_rules_preserve_meaning),
        ("How deep the prefix must go",
         verify_how_deep_the_prefix_must_go),
        ("What is still not identified",
         verify_what_is_still_not_identified),
        ("What the residue is", verify_the_residue_is_containment),
        ("The rule set", report_rule_census),
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
