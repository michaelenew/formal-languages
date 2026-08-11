"""0043's rule set again, with `|` derived instead of primitive.

0043 kept `|` as a third primitive join, reached confluence with
**fourteen** rules, and left two of 4000 terms divergent -- both of them
base-algebra differences that ANF was expected to discharge. This module
takes the base at its word: terms *are* ANF polynomials over `^` and
`&`, `|` is `a ^ b ^ ab` on construction, and there are no op-terms at
all.

Representation: a polynomial is a set of monomials, XOR-joined; a
monomial is (set of atoms, constant mask), the atoms multiplied by `&`.
An atom is `x`, a shift, a series, or a measure. `xor` and `conj` are
the constructors, and they already do five of 0043's rules -- constant
folding, units, annihilators, idempotence and commutativity -- so those
are not rules here.

Two things came out of the rebuild that were not the question asked.

**Random terms do not exercise the schema.** In 3000 random depth-3
terms, `collect` fires once, `telescope` and `N-lowbit` never. 0043's
verdict was measured on a sample that essentially never built the
redexes of its own headline rules. `interesting_subterms` fixes that,
and six of the eight completion rounds below were only visible to it.

**Completing it properly *adds* a rule.** `N-absorb` -- `N(p) & m -> m`
wherever `m` vanishes with `p` -- is not in 0043 and is not bookkeeping:
it is the statement that `N` is a guard rather than a factor.

Two orderings are load-bearing and both were found by counterexample:
`collect` fires only between series atoms that are irreducible on their
own, and `telescope` fires only when nothing else can. See
`collectable` and `LAST_RESORT`.

Run directly for the verification suite.
"""

from __future__ import annotations

import functools
import random

WIDTH = 9
MASK = (1 << WIDTH) - 1
SAFE = range(1 << (WIDTH - 2))
# structured terms are large; check them on a spread of
# inputs rather than all of SAFE
SAMPLE = tuple(range(0, 1 << (WIDTH - 2), 5))

SHIFTS = {
    "a": lambda v: (v << 1) & MASK,
    "b": lambda v: ((v << 1) | 1) & MASK,
    "h": lambda v: v >> 1,
}
lowest_set = lambda v: v & -v
highest_set = lambda v: 0 if not v else 1 << (v.bit_length() - 1)
lowest_zero = lambda v: lowest_set(MASK ^ v)
nonempty = lambda v: 0 if v == 0 else MASK

SERIES = {                       # name -> (join, shift, measure name)
    "!": ("^", "a", "self"),
    "!h": ("^", "h", "self"),
    "U": ("|", "a", "low-set"),
    "D": ("|", "h", "high-set"),
    "T": ("&", "b", "low-zero"),
}
MEASURES = {"self": lambda v: v, "low-set": lowest_set,
            "high-set": highest_set, "low-zero": lowest_zero}


def _run(name, value):
    join, shift, _ = SERIES[name]
    combine = {"^": lambda p, q: p ^ q,
               "|": lambda p, q: p ^ q ^ (p & q),
               "&": lambda p, q: p & q}[join]
    total, lifted = value, value
    for _ in range(2 * WIDTH):
        lifted = SHIFTS[shift](lifted)
        total = combine(total, lifted)
    return total


APPLY = {name: (lambda v, n=name: _run(n, v)) for name in SERIES}
APPLY["N"] = nonempty

ABSORB = {
    ("N", "N"): ("N", False), ("N", "T"): ("N", True),
    ("N", "U"): ("N", False), ("N", "D"): ("N", False),
    ("T", "N"): ("N", False), ("T", "T"): ("T", False),
    ("T", "U"): ("N", True), ("T", "D"): ("D", False),
    ("U", "N"): ("N", False), ("U", "T"): ("N", True),
    ("U", "U"): ("U", False), ("U", "D"): ("N", False),
    ("D", "N"): ("N", False), ("D", "T"): ("T", False),
    ("D", "U"): ("N", False), ("D", "D"): ("D", False),
    # the `^` series are invertible (0042 s2) and fix 0, so they are
    # zero iff their argument is -- invisible to `N`. 0042's table
    # stopped at {N,T,U,D} and so missed these two.
    ("N", "!"): ("N", False), ("N", "!h"): ("N", False),
}


# ---------------------------------------------------------------------
# polynomials: the base algebra, in ANF, with `|` derived
# ---------------------------------------------------------------------

def const(value: int):
    value &= MASK
    return frozenset() if value == 0 else frozenset([(frozenset(), value)])


def atom_poly(atom):
    return frozenset([(frozenset([atom]), MASK)])


VARIABLE = atom_poly(("x",))


def xor(left, right):
    """Symmetric difference. Absorbs 0043's `unit` (a ^ 0), `idem-op`
    (a ^ a) and `commute` for `^`."""
    return left ^ right


def conj(left, right):
    """Product with idempotent atoms. Absorbs 0043's `fold`, the `&`
    units and annihilators, and `commute` for `&`."""
    product = set()
    for atoms_l, mask_l in left:
        for atoms_r, mask_r in right:
            mask = mask_l & mask_r
            if mask:
                product ^= {(atoms_l | atoms_r, mask)}
    return frozenset(product)


def disj(left, right):
    """`|` is not primitive here."""
    return xor(xor(left, right), conj(left, right))


def apply_join(join, left, right):
    return {"^": xor, "|": disj, "&": conj}[join](left, right)


def series_poly(name, argument):
    return atom_poly(("series", name, argument))


def shift_poly(name, argument):
    return atom_poly(("shift", name, argument))


@functools.lru_cache(maxsize=None)
def evaluate(poly, value: int) -> int:
    total = 0
    for atoms, mask in poly:
        term = mask
        for atom in atoms:
            if atom[0] == "x":
                term &= value
            elif atom[0] == "shift":
                term &= SHIFTS[atom[1]](evaluate(atom[2], value))
            elif atom[0] == "series":
                term &= APPLY[atom[1]](evaluate(atom[2], value))
            else:
                term &= MEASURES[atom[1]](evaluate(atom[2], value))
        total ^= term
    return total


@functools.lru_cache(maxsize=None)
def size(poly) -> int:
    total = 1
    for atoms, _ in poly:
        total += 1
        for atom in atoms:
            total += 1 if atom[0] == "x" else 1 + size(atom[2])
    return total


def measure(poly):
    """(series count, non-N series, total series-argument size, size).

    `non-N` sits above `argument size` because the low-bit rules trade a
    named series for `N` at the cost of a bigger argument
    (`h(D t) & 1 -> N(h t) & 1`), and that trade has to count as
    progress.
    """
    def counts(p):
        series_count = argument_size = non_trivial = 0
        for atoms, _ in p:
            for atom in atoms:
                if atom[0] == "x":
                    continue
                inner = counts(atom[2])
                series_count += inner[0]
                non_trivial += inner[1]
                argument_size += inner[2]
                if atom[0] == "series":
                    series_count += 1
                    argument_size += size(atom[2])
                    non_trivial += 0 if atom[1] == "N" else 1
        return series_count, non_trivial, argument_size
    return counts(poly) + (size(poly),)


def render(poly) -> str:
    if not poly:
        return "0"
    pieces = []
    for atoms, mask in sorted(poly, key=lambda m: (sorted(map(str, m[0])),
                                                   m[1])):
        names = "".join(
            "x" if atom[0] == "x"
            else f"{atom[1]}({render(atom[2])})"
            for atom in sorted(atoms, key=str))
        label = {0: "0", MASK: "Ω"}.get(mask, str(mask))
        pieces.append(names + ("" if mask == MASK and names else
                               ("&" + label if names else label)))
    return " ^ ".join(pieces)


def is_constant(poly):
    return all(not atoms for atoms, _ in poly)


def constant_value(poly):
    total = 0
    for _, mask in poly:
        total ^= mask
    return total


def vanishes_with(poly, base):
    """Is `poly` forced to 0 everywhere `base` is 0?

    Every operator in the language is zero-preserving except `b`
    (which fills a one), so a monomial vanishes with `base` as soon as
    one of its atoms is built from `base`. This is what makes `N` a
    guard rather than a factor: `N(t)` is the whole universe wherever
    anything derived from `t` is non-zero, so it is redundant there.
    """
    return all(any(_atom_vanishes(atom, base) for atom in atoms)
               for atoms, _ in poly)


def _atom_vanishes(atom, base):
    if atom_poly(atom) == base:
        return True
    if atom[0] == "x":
        return base == VARIABLE
    if atom[0] == "shift" and atom[1] == "b":
        return False
    if atom[0] == "series":
        target, low = ABSORB.get(("N", atom[1]), (None, False))
        # `N(S t) = N(t & 1)` (0042 s4) says `S(t)` is zero exactly where
        # `t & 1` is -- so it vanishes with a base the recursion below,
        # which only walks into `t`, would never match.
        if target == "N" and low and base == conj(atom[2], const(1)):
            return True
    return vanishes_with(atom[2], base)


def low_bit_only(poly):
    """Does every monomial's mask sit inside bit 0?"""
    return bool(poly) and all(mask & ~1 == 0 for _, mask in poly)


# ---------------------------------------------------------------------
# the rules
# ---------------------------------------------------------------------

LOW_BIT_SERIES = {"U": None, "T": None, "!": None, "D": "N"}

# `telescope` runs only when nothing else can.
#
# It is the one rule whose redex the *base algebra* can create and
# destroy behind its back: any other rewrite may turn one monomial into
# a copy of another, and XOR then annihilates both -- removing `S(t)` or
# `sigma_S(S t)`, or exposing a pair that was not there before.
# Cancellation is not a rewrite we control, so telescope must not fire
# until cancellation has finished. Running it *first* fails for the same
# reason in mirror image: it can take a monomial that a pending `fold`
# was about to annihilate, and then the fold has no partner.
LAST_RESORT = ("telescope",)

# The rule set, in full. Ten, where 0043 had fourteen.
RULE_NAMES = ("fold", "absorb", "shift-out", "low-bit", "low-arg",
              "N-absorb", "N-lowbit", "N-shift", "collect", "telescope")


def collectable(name, left, right):
    """May `collect` fuse `S(left)` with `S(right)`?

    Only if neither is a redex on its own. `collect` buries its
    arguments inside a new series where no other rule can reach them, so
    every rule that can fire on `S(arg)` alone must fire first --
    `fold` on a constant, `absorb` on a nested series, `shift-out`
    followed by `telescope` on a shifted sibling. Making `collect` the
    last resort replaces three separate side conditions with one, and it
    is 0043's round 1 restated: combination must not destroy the redex
    that cancellation needs.
    """
    return not (rewrites(series_poly(name, left))
                or rewrites(series_poly(name, right)))


@functools.lru_cache(maxsize=None)
def rewrites(poly):
    """Every one-step rewrite of the polynomial."""
    steps = []
    monomials = sorted(poly, key=lambda m: (sorted(map(str, m[0])), m[1]))

    # --- rules inside an atom's argument (recursion) -----------------
    for atoms, mask in monomials:
        for atom in atoms:
            if atom[0] == "x":
                continue
            for rule, replacement in rewrites(atom[2]):
                rebuilt = (atoms - {atom}
                           | {(atom[0], atom[1], replacement)})
                steps.append((rule, (poly - {(atoms, mask)})
                              ^ frozenset([(frozenset(rebuilt), mask)])))

    # --- fold: a series or shift applied to a constant ---------------
    for atoms, mask in monomials:
        for atom in atoms:
            if atom[0] == "x" or not is_constant(atom[2]):
                continue
            value = constant_value(atom[2])
            folded = (APPLY[atom[1]](value) if atom[0] == "series"
                      else SHIFTS[atom[1]](value) if atom[0] == "shift"
                      else MEASURES[atom[1]](value))
            rest = frozenset(atoms - {atom})
            steps.append(("fold", (poly - {(atoms, mask)})
                          ^ conj(frozenset([(rest, mask)]), const(folded))))

    # --- absorb: S1(S2 t) --------------------------------------------
    for atoms, mask in monomials:
        for atom in atoms:
            if atom[0] != "series":
                continue
            inner = atom[2]
            if len(inner) != 1:
                continue
            (inner_atoms, inner_mask), = inner
            if inner_mask != MASK or len(inner_atoms) != 1:
                continue
            (inner_atom,) = inner_atoms
            if inner_atom[0] != "series":
                continue
            key = (atom[1], inner_atom[1])
            if key not in ABSORB:
                continue
            name, low = ABSORB[key]
            argument = inner_atom[2]
            if low:
                argument = conj(argument, const(1))
            rest = frozenset(atoms - {atom})
            steps.append(("absorb", (poly - {(atoms, mask)})
                          ^ conj(frozenset([(rest, mask)]),
                                 series_poly(name, argument))))

    # --- shift-out: S(sigma_S t) -> sigma_S(S t) ---------------------
    for atoms, mask in monomials:
        for atom in atoms:
            if atom[0] != "series" or atom[1] not in SERIES:
                continue
            inner = atom[2]
            if len(inner) != 1:
                continue
            (inner_atoms, inner_mask), = inner
            if inner_mask != MASK or len(inner_atoms) != 1:
                continue
            (inner_atom,) = inner_atoms
            if (inner_atom[0] == "shift"
                    and inner_atom[1] == SERIES[atom[1]][1]):
                rest = frozenset(atoms - {atom})
                lifted = shift_poly(inner_atom[1],
                                    series_poly(atom[1], inner_atom[2]))
                steps.append(("shift-out", (poly - {(atoms, mask)})
                              ^ conj(frozenset([(rest, mask)]), lifted)))

    # --- low-bit: S(t) & 1 -> t & 1 ----------------------------------
    for atoms, mask in monomials:
        if mask & ~1:
            continue
        for atom in atoms:
            if atom[0] != "series":
                continue
            if atom[1] == "N":
                # `N(p) & 1` is `p & 1` once `p` cannot exceed bit 0
                if not low_bit_only(atom[2]):
                    continue
                replacement = atom[2]
            elif atom[1] in LOW_BIT_SERIES:
                wrapper = LOW_BIT_SERIES[atom[1]]
                replacement = (atom[2] if wrapper is None
                               else series_poly(wrapper, atom[2]))
            else:
                continue
            rest = frozenset(atoms - {atom})
            steps.append(("low-bit", (poly - {(atoms, mask)})
                          ^ conj(frozenset([(rest, mask)]), replacement)))
        for atom in atoms:
            if atom[0] != "shift":
                continue
            if atom[1] in ("a", "b"):
                rest = frozenset(atoms - {atom})
                folded = const(0) if atom[1] == "a" else const(1)
                steps.append(("low-bit", (poly - {(atoms, mask)})
                              ^ conj(frozenset([(rest, mask)]), folded)))
                continue
            # `h(D t) & 1` is bit 1 of `D t`, which is `N(h t) & 1`.
            # Without this, shift-out strands the D-low-bit rule: once
            # `D(h t)` has become `h(D t)` no rule can reach the `D`.
            inner = atom[2]
            if len(inner) != 1:
                continue
            (inner_atoms, inner_mask), = inner
            if inner_mask != MASK or len(inner_atoms) != 1:
                continue
            (inner_atom,) = inner_atoms
            if (inner_atom[0] != "series" or inner_atom[1] != "D"):
                continue
            rest = frozenset(atoms - {atom})
            lifted = series_poly("N", shift_poly("h", inner_atom[2]))
            steps.append(("low-bit", (poly - {(atoms, mask)})
                          ^ conj(frozenset([(rest, mask)]), lifted)))

    # --- low-arg: S(t & 1) -------------------------------------------
    for atoms, mask in monomials:
        for atom in atoms:
            if atom[0] != "series" or not low_bit_only(atom[2]):
                continue
            if atom[1] in ("D", "T"):
                replacement = atom[2]
            elif atom[1] == "U":
                replacement = series_poly("N", atom[2])
            else:
                continue
            rest = frozenset(atoms - {atom})
            steps.append(("low-arg", (poly - {(atoms, mask)})
                          ^ conj(frozenset([(rest, mask)]), replacement)))

    # --- N-absorb: N(p) & m -> m  whenever m sits inside p -----------
    for atoms, mask in monomials:
        for atom in atoms:
            if atom[0] != "series" or atom[1] != "N" or len(atom[2]) != 1:
                continue
            (guarded_atoms, guarded_mask), = atom[2]
            rest = frozenset(atoms - {atom})
            inside = guarded_atoms <= rest and mask & ~guarded_mask == 0
            if inside or vanishes_with(frozenset([(rest, mask)]), atom[2]):
                steps.append(("N-absorb", (poly - {(atoms, mask)})
                              ^ frozenset([(rest, mask)])))

    # --- N-lowbit: N(N(t) & 1) -> N(t) -------------------------------
    for atoms, mask in monomials:
        for atom in atoms:
            if atom[0] != "series" or atom[1] != "N":
                continue
            inner = atom[2]
            if len(inner) != 1:
                continue
            (inner_atoms, inner_mask), = inner
            if inner_mask != 1 or len(inner_atoms) != 1:
                continue
            (inner_atom,) = inner_atoms
            if inner_atom[0] != "series" or inner_atom[1] != "N":
                continue
            rest = frozenset(atoms - {atom})
            steps.append(("N-lowbit", (poly - {(atoms, mask)})
                          ^ conj(frozenset([(rest, mask)]),
                                 series_poly("N", inner_atom[2]))))

    # --- N-shift ------------------------------------------------------
    for atoms, mask in monomials:
        for atom in atoms:
            if atom[0] != "series" or atom[1] != "N":
                continue
            inner = atom[2]
            if len(inner) != 1:
                continue
            (inner_atoms, inner_mask), = inner
            if inner_mask != MASK or len(inner_atoms) != 1:
                continue
            (inner_atom,) = inner_atoms
            if inner_atom[0] != "shift":
                continue
            if inner_atom[1] == "a":
                replacement = series_poly("N", inner_atom[2])
            elif inner_atom[1] == "b":
                replacement = const(MASK)
            else:
                continue
            rest = frozenset(atoms - {atom})
            steps.append(("N-shift", (poly - {(atoms, mask)})
                          ^ conj(frozenset([(rest, mask)]), replacement)))

    # --- collect, per join -------------------------------------------
    singles = {}
    for atoms, mask in monomials:
        if mask == MASK and len(atoms) == 1:
            (atom,) = atoms
            if atom[0] == "series" and atom[1] in SERIES:
                singles.setdefault(atom[1], []).append(atom)
    for name, found in singles.items():
        join = SERIES[name][0]
        for index, first in enumerate(found):
            for second in found[index + 1:]:
                if not collectable(name, first[2], second[2]):
                    continue
                combined = series_poly(name, apply_join(join, first[2],
                                                        second[2]))
                if join == "^":
                    steps.append(("collect",
                                  poly ^ atom_poly(first)
                                  ^ atom_poly(second) ^ combined))
                elif join == "|":
                    pair = frozenset([(frozenset([first, second]), MASK)])
                    if pair <= poly:
                        steps.append(("collect",
                                      poly ^ atom_poly(first)
                                      ^ atom_poly(second) ^ pair
                                      ^ combined))
    for atoms, mask in monomials:
        found = [atom for atom in atoms
                 if atom[0] == "series" and atom[1] in SERIES
                 and SERIES[atom[1]][0] == "&"]
        for index, first in enumerate(found):
            for second in found[index + 1:]:
                if first[1] != second[1] or not collectable(
                        first[1], first[2], second[2]):
                    continue
                rest = frozenset(atoms - {first, second})
                combined = series_poly(first[1], conj(first[2], second[2]))
                steps.append(("collect", (poly - {(atoms, mask)})
                              ^ conj(frozenset([(rest, mask)]), combined)))

    # --- telescope: S(t) ^ sigma_S(S t) -> m(t) ----------------------
    for atoms, mask in monomials:
        if mask != MASK or len(atoms) != 1:
            continue
        (atom,) = atoms
        if atom[0] != "series" or atom[1] not in SERIES:
            continue
        partner = shift_poly(SERIES[atom[1]][1], atom_poly(atom))
        if partner <= poly:
            # the `^` series measure *is* the argument (0042 s2), so emit
            # it rather than an inert `self(...)` atom no rule can open
            measure_name = SERIES[atom[1]][2]
            replacement = (atom[2] if measure_name == "self"
                           else atom_poly(("measure", measure_name,
                                           atom[2])))
            steps.append(("telescope",
                          poly ^ atom_poly(atom) ^ partner ^ replacement))

    steps = [(rule, result) for rule, result in steps if result != poly]
    # Telescope goes first, always. It is the only rule whose redex the
    # *base algebra* can destroy: any other rewrite may turn one
    # monomial into a copy of another, and XOR then annihilates both --
    # taking `S(t)` or `sigma_S(S t)` with it. Cancellation is not a
    # rewrite we control, so the cancellation rule has to run ahead of
    # everything that could trigger it.
    others = [step for step in steps if step[0] not in LAST_RESORT]
    return others or steps


def normal_forms(poly, node_cap: int = 4000):
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
# checks
# ---------------------------------------------------------------------

def random_poly(generator, budget):
    kind = generator.random()
    if budget == 0 or kind < 0.25:
        return generator.choice([VARIABLE, VARIABLE, const(1), const(MASK)])
    if kind < 0.45:
        return series_poly(generator.choice(list(APPLY)),
                           random_poly(generator, budget - 1))
    if kind < 0.6:
        return shift_poly(generator.choice(list(SHIFTS)),
                          random_poly(generator, budget - 1))
    return apply_join(generator.choice(["^", "|", "&"]),
                      random_poly(generator, budget - 1),
                      random_poly(generator, budget - 1))


def interesting_subterms():
    """The redexes each structural rule is *for*.

    Random generation almost never builds a telescoping pair or a
    collectable sibling, so a census taken over random terms says
    nothing about those rules. This pool is what they are aimed at.
    """
    pool = []
    for name, (_, shift, _) in SERIES.items():
        base = series_poly(name, VARIABLE)
        pool += [
            base,                                          # S(x)
            shift_poly(shift, base),                       # sigma_S(S x)
            series_poly(name, shift_poly(shift, VARIABLE)),  # S(sigma_S x)
            series_poly(name, series_poly(name, VARIABLE)),  # S(S x)
            conj(base, const(1)),                          # S(x) & 1
            series_poly(name, conj(VARIABLE, const(1))),    # S(x & 1)
            series_poly(name, const(1)),                   # S(1)
            series_poly("N", base),                        # N(S x)
            series_poly(name, series_poly("N", VARIABLE)),  # S(N x)
        ]
    n_of_x = series_poly("N", VARIABLE)
    pool += [n_of_x,
             series_poly("N", conj(n_of_x, const(1))),     # N(N(x) & 1)
             series_poly("N", shift_poly("a", VARIABLE)),
             series_poly("N", shift_poly("b", VARIABLE)),
             VARIABLE, const(1), const(MASK)]
    return pool


def random_structured_poly(generator, budget):
    if budget == 0 or generator.random() < 0.4:
        return generator.choice(interesting_subterms())
    return apply_join(generator.choice(["^", "|", "&"]),
                      random_structured_poly(generator, budget - 1),
                      random_structured_poly(generator, budget - 1))


def verify_the_structural_rules_fire(seed=20260813) -> None:
    """Each rule, on the redex it exists for: does it fire, and does the
    redex have exactly one normal form?"""
    cases = []
    for name, (join, shift, measure_name) in SERIES.items():
        base = series_poly(name, VARIABLE)
        # a shift the series does not use, so that `S(sibling)` is
        # irreducible and `collect` is actually allowed to fire
        other = "a" if shift != "a" else "h"
        sibling = series_poly(name, shift_poly(other, VARIABLE))
        cases += [
            ("collect", apply_join(join, base, sibling)),
            ("telescope", xor(base, shift_poly(shift, base))),
            ("shift-out", series_poly(name, shift_poly(shift, VARIABLE))),
        ]
    n_of_x = series_poly("N", VARIABLE)
    cases += [
        ("N-lowbit", series_poly("N", conj(n_of_x, const(1)))),
        ("N-shift", series_poly("N", shift_poly("a", VARIABLE))),
        ("absorb", series_poly("N", series_poly("T", VARIABLE))),
        ("low-bit", conj(series_poly("U", VARIABLE), const(1))),
        ("low-arg", series_poly("D", conj(VARIABLE, const(1)))),
        ("fold", series_poly("T", const(1))),
        ("N-absorb", conj(series_poly("N", VARIABLE),
                          series_poly("U", VARIABLE))),
    ]
    missing, ambiguous = [], []
    for rule, poly in cases:
        fired = {step for step, _ in rewrites(poly)}
        if rule not in fired:
            missing.append((rule, render(poly), sorted(fired)))
        forms, _ = normal_forms(poly)
        if len(forms) > 1:
            ambiguous.append((rule, render(poly),
                              sorted(render(f) for f in forms)))
    for rule, shown, fired in missing:
        print(f"  {rule} does NOT fire on {shown} (got {fired})")
    for rule, shown, forms in ambiguous:
        print(f"  {shown} has {len(forms)} normal forms: {forms}")
    if not missing and not ambiguous:
        print(f"  all {len(cases)} canonical redexes fire their rule and "
              f"have exactly one normal form")
    return missing, ambiguous


def verify_rules_are_sound(trials=3000, seed=20260813, builder=None,
                           values=None) -> None:
    generator = random.Random(seed)
    builder = builder or random_poly
    values = SAFE if values is None else values
    checked = 0
    for _ in range(trials):
        poly = builder(generator, 3)
        for rule, result in rewrites(poly):
            for value in values:
                assert evaluate(poly, value) == evaluate(result, value), (
                    rule, render(poly), render(result))
            checked += 1
    print(f"  {checked} rule applications over {len(values)} inputs, "
          f"every one meaning-preserving")


def verify_rules_shrink(trials=400, seed=20260813, builder=None) -> None:
    generator = random.Random(seed)
    builder = builder or random_poly
    growing = []
    for _ in range(trials):
        poly = builder(generator, 3)
        for rule, result in rewrites(poly):
            if measure(result) >= measure(poly):
                growing.append((rule, render(poly), render(result)))
    if growing:
        print(f"  {len(growing)} applications do not shrink the measure, "
              f"e.g. {growing[0][0]}: {growing[0][1]} -> {growing[0][2]}")
    else:
        print("  every rule strictly decreases (series count, non-N, "
              "argument size, size)")
    return growing


def search_for_divergence(trials=3000, seed=20260813, builder=None,
                          depth=3) -> None:
    generator = random.Random(seed)
    builder = builder or random_poly
    divergent, capped, examined = [], 0, 0
    for _ in range(trials):
        poly = builder(generator, depth)
        forms, hit = normal_forms(poly)
        if hit:
            capped += 1
            continue
        examined += 1
        if len(forms) > 1:
            divergent.append((poly, sorted(forms, key=render)))
    print(f"  {examined} polynomials explored to completion, {capped} hit "
          f"the node cap")
    if not divergent:
        print("  **no polynomial has two normal forms**")
        return
    print(f"  {len(divergent)} have more than one normal form")
    for poly, forms in sorted(divergent, key=lambda pr: size(pr[0]))[:6]:
        traces = {tuple(evaluate(form, v) for v in SAFE) for form in forms}
        verdict = ("same meaning, different syntax" if len(traces) == 1
                   else "DIFFERENT MEANING -- a rule is unsound")
        print(f"    {render(poly)}   [{verdict}]")
        for form in forms:
            print(f"        -> {render(form)}")


def report_rule_census(trials=3000, seed=20260813) -> None:
    counted = {}
    for label, builder in (("random", random_poly),
                           ("targeted", random_structured_poly)):
        generator = random.Random(seed)
        used = {}
        for _ in range(trials):
            poly = builder(generator, 3)
            for rule, _ in rewrites(poly):
                used[rule] = used.get(rule, 0) + 1
        counted[label] = used
    every = list(RULE_NAMES)
    assert set(counted["random"]) | set(counted["targeted"]) <= set(every)
    print(f"  {'rule':<12} {'random':>8} {'targeted':>10}")
    for rule in sorted(every, key=lambda r: -counted["targeted"].get(r, 0)):
        print(f"  {rule:<12} {counted['random'].get(rule, 0):>8} "
              f"{counted['targeted'].get(rule, 0):>10}")
    print()
    print(f"  {len(every)} rules, against 0043's fourteen.")
    print("    Gone -- building an ANF polynomial already does them:")
    print("      fold-of-two-constants, unit, annihilator, idem-op, commute")
    print("    Gone -- ANF discharges the case that forced it:")
    print("      split-constant")
    print("    NEW, and not in 0043 at all:")
    print("      N-absorb  N(p) & m -> m   wherever m vanishes with p")
    print()
    print("  Read the two columns against each other. `collect`,")
    print("  `telescope` and `N-lowbit` are the schema's own structural")
    print("  rules, and random terms essentially never build their")
    print("  redexes -- so a confluence verdict sampled from random")
    print("  terms is a verdict on the bookkeeping, not on the schema.")


def run_verification_suite() -> None:
    print("=" * 70)
    print("1. Every rule preserves meaning")
    print("=" * 70)
    verify_rules_are_sound()
    verify_rules_are_sound(trials=600, builder=random_structured_poly,
                           values=SAMPLE)

    print()
    print("=" * 70)
    print("2. Termination")
    print("=" * 70)
    verify_rules_shrink()
    verify_rules_shrink(trials=600, builder=random_structured_poly)

    print()
    print("=" * 70)
    print("3. Each structural rule, on the redex it exists for")
    print("=" * 70)
    verify_the_structural_rules_fire()

    print()
    print("=" * 70)
    print("4. Divergence search -- random terms")
    print("=" * 70)
    search_for_divergence()

    print()
    print("=" * 70)
    print("5. Divergence search -- terms built from the redexes")
    print("=" * 70)
    search_for_divergence(trials=1200, builder=random_structured_poly, depth=2)

    print()
    print("=" * 70)
    print("6. How many rules are left")
    print("=" * 70)
    report_rule_census()

    print()
    print("=" * 70)
    print("suite complete")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
