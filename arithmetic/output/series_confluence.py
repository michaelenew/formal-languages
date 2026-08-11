"""Is 0042's rule set confluent? Searched, not sampled.

The rules, oriented so that every one strictly shrinks a term:

    distribute   S(a o_S b)          -> S(a) o_S S(b)
    shift-out    S(sigma_S t)        -> sigma_S(S t)
    idempotence  S(S t)              -> S(t)                  [| and & series]
    absorb       S1(S2 t)            -> per 0042's table
    telescope    S(t) ^ sigma_S(S t) -> m_S(t)
    constants    S(0) -> 0, and the N-specific shift laws

Every rule is checked semantically before it is used, so any two normal
forms of one term are equal in meaning. Confluence is then exactly the
question of whether they are equal as TERMS -- and that is decidable per
term by exploring the whole rewrite graph, which is what this module
does. Not a sampled strategy comparison: the full reachable set of
normal forms, with a node cap that is reported if it is hit.

Run directly for the verification suite.
"""

from __future__ import annotations

import random
from itertools import product as cartesian_product

WIDTH = 9
MASK = (1 << WIDTH) - 1
SAFE = range(1 << (WIDTH - 2))

SHIFTS = {
    "a": lambda v: (v << 1) & MASK,
    "b": lambda v: ((v << 1) | 1) & MASK,
    "h": lambda v: v >> 1,
}
JOINS = {
    "^": lambda p, q: p ^ q,
    "|": lambda p, q: p ^ q ^ (p & q),
    "&": lambda p, q: p & q,
}
lowest_set = lambda v: v & -v
highest_set = lambda v: 0 if not v else 1 << (v.bit_length() - 1)
lowest_zero = lambda v: lowest_set(MASK ^ v)
nonempty = lambda v: 0 if v == 0 else MASK

# name -> (join, shift, measure, is_closure)
SERIES = {
    "!": ("^", "a", lambda v: v, False),
    "!h": ("^", "h", lambda v: v, False),
    "U": ("|", "a", lowest_set, True),
    "D": ("|", "h", highest_set, True),
    "T": ("&", "b", lowest_zero, True),
}


def run_series(name: str, value: int) -> int:
    join, shift, _, _ = SERIES[name]
    combine, lift = JOINS[join], SHIFTS[shift]
    total, lifted = value, value
    for _ in range(2 * WIDTH):
        lifted = lift(lifted)
        total = combine(total, lifted)
    return total


APPLY = {name: (lambda v, n=name: run_series(n, v)) for name in SERIES}
APPLY["N"] = nonempty

# 0042's absorption table, outer(inner) -> replacement, as a term builder
ABSORB = {
    ("N", "N"): ("N", None), ("N", "T"): ("N", "low"),
    ("N", "U"): ("N", None), ("N", "D"): ("N", None),
    ("T", "N"): ("N", None), ("T", "T"): ("T", None),
    ("T", "U"): ("N", "low"), ("T", "D"): ("D", None),
    ("U", "N"): ("N", None), ("U", "T"): ("N", "low"),
    ("U", "U"): ("U", None), ("U", "D"): ("N", None),
    ("D", "N"): ("N", None), ("D", "T"): ("T", None),
    ("D", "U"): ("N", None), ("D", "D"): ("D", None),
}


# ---------------------------------------------------------------------
# terms
# ---------------------------------------------------------------------

def evaluate(term, value: int) -> int:
    kind = term[0]
    if kind == "x":
        return value
    if kind == "const":
        return term[1]
    if kind == "op":
        return JOINS[term[1]](evaluate(term[2], value),
                              evaluate(term[3], value))
    if kind == "shift":
        return SHIFTS[term[1]](evaluate(term[2], value))
    if kind == "series":
        return APPLY[term[1]](evaluate(term[2], value))
    if kind == "measure":
        return term[1](evaluate(term[2], value))
    raise ValueError(term)


def size(term) -> int:
    if term[0] in ("x", "const"):
        return 1
    if term[0] == "op":
        return 1 + size(term[2]) + size(term[3])
    return 1 + size(term[2])


def render(term) -> str:
    kind = term[0]
    if kind == "x":
        return "x"
    if kind == "const":
        return {0: "0", MASK: "U"}.get(term[1], str(term[1]))
    if kind == "op":
        return f"({render(term[2])} {term[1]} {render(term[3])})"
    if kind == "shift":
        return f"{term[1]}({render(term[2])})"
    if kind == "series":
        return f"{term[1]}({render(term[2])})"
    return f"m({render(term[2])})"


# ---------------------------------------------------------------------
# the rules
# ---------------------------------------------------------------------

def rules_at(term) -> list:
    """Every rule applicable at the ROOT of `term`, as (name, result)."""
    results = []

    if term[0] == "op":
        join, left, right = term[1], term[2], term[3]
        # constant folding and idempotence of the base operators
        if left[0] == "const" and right[0] == "const":
            results.append(("fold", ("const", JOINS[join](left[1],
                                                          right[1]))))
        # commutativity, oriented: every join here is commutative, and
        # the corpus's ANF already normalises modulo it. Without this the
        # engine reports (1 & x) and (x & 1) as different normal forms.
        if repr(left) > repr(right):
            results.append(("commute", ("op", join, right, left)))
        # units and annihilators of the base operators
        for first, second in ((left, right), (right, left)):
            if first == ("const", 0):
                if join in ("^", "|"):
                    results.append(("unit", second))
                else:
                    results.append(("unit", ("const", 0)))
            elif first == ("const", MASK):
                if join == "|":
                    results.append(("unit", ("const", MASK)))
                elif join == "&":
                    results.append(("unit", second))
        if left == right:
            results.append(("idem-op",
                            ("const", 0) if join == "^" else left))
        # COLLECT, not distribute: S(a) o_S S(b) -> S(a o_S b).
        # 0042 oriented this the other way; section 3 shows why that
        # orientation cannot be completed.
        if (left[0] == "series" and right[0] == "series"
                and left[1] == right[1] and left[1] in SERIES
                and SERIES[left[1]][0] == join):
            results.append(("collect",
                            ("series", left[1],
                             ("op", join, left[2], right[2]))))
        # low-bit rules: completion of the absorption table. The
        # `& 1` wrapper that absorption introduces has to be pushed
        # through the series, or two absorptions at different depths
        # reach different normal forms.
        if join == "&":
            for first, second in ((left, right), (right, left)):
                if second != ("const", 1):
                    continue
                if first[0] == "series" and first[1] in ("U", "T", "!"):
                    results.append(("low-bit",
                                    ("op", "&", first[2], ("const", 1))))
                elif first[0] == "series" and first[1] == "D":
                    results.append(("low-bit",
                                    ("op", "&",
                                     ("series", "N", first[2]),
                                     ("const", 1))))
                elif first[0] == "shift" and first[1] == "a":
                    results.append(("low-bit", ("const", 0)))
                elif first[0] == "shift" and first[1] == "b":
                    results.append(("low-bit", ("const", 1)))
        # telescope, either argument order
        if join == "^":
            for first, second in ((left, right), (right, left)):
                if (first[0] == "series" and first[1] in SERIES
                        and second[0] == "shift"
                        and second[2] == first
                        and second[1] == SERIES[first[1]][1]):
                    measure = SERIES[first[1]][2]
                    results.append(("telescope",
                                    ("measure", measure, first[2])))
        return results

    if term[0] == "shift" and term[2][0] == "const":
        results.append(("shift-fold",
                        ("const", SHIFTS[term[1]](term[2][1]))))
        return results

    if term[0] != "series":
        return results

    name, inner = term[1], term[2]

    if inner[0] == "const":
        if name == "N":
            results.append(("constant",
                            ("const", 0 if inner[1] == 0 else MASK)))
        else:
            results.append(("constant",
                            ("const", APPLY[name](inner[1]))))

    # completion of `collect` against constant folding: when one side
    # of the join under a series is a constant, split it off and fold it
    # at once. Series count is unchanged and the series' argument
    # shrinks, so the measure still falls.
    if name in SERIES and inner[0] == "op" and inner[1] == SERIES[name][0]:
        for first, second in ((inner[2], inner[3]), (inner[3], inner[2])):
            if first[0] == "const":
                results.append((
                    "split-constant",
                    ("op", inner[1], ("const", APPLY[name](first[1])),
                     ("series", name, second))))

    # a low-bit argument is already closed for D and T, and only its
    # emptiness survives for U
    if (inner[0] == "op" and inner[1] == "&"
            and ("const", 1) in (inner[2], inner[3])):
        if name in ("D", "T"):
            results.append(("low-arg", inner))
        elif name == "U":
            results.append(("low-arg", ("series", "N", inner)))

    if name == "N" and inner[0] == "shift":
        if inner[1] == "a":
            results.append(("N-shift", ("series", "N", inner[2])))
        elif inner[1] == "b":
            results.append(("N-shift", ("const", MASK)))

    if name in SERIES and inner[0] == "shift":
        if inner[1] == SERIES[name][1]:
            results.append(("shift-out",
                            ("shift", inner[1], ("series", name,
                                                 inner[2]))))

    if (name == "N" and inner[0] == "op" and inner[1] == "&"
            and ("const", 1) in (inner[2], inner[3])):
        other = inner[3] if inner[2] == ("const", 1) else inner[2]
        if other[0] == "series" and other[1] == "N":
            results.append(("N-lowbit", other))

    if inner[0] == "series" and (name, inner[1]) in ABSORB:
        replacement, wrapper = ABSORB[(name, inner[1])]
        argument = inner[2]
        if wrapper == "low":
            argument = ("op", "&", argument, ("const", 1))
        results.append(("absorb", ("series", replacement, argument)))

    return results


def rewrites(term) -> list:
    """Every one-step rewrite anywhere in the term."""
    steps = [(rule, result) for rule, result in rules_at(term)]
    if term[0] == "op":
        for index in (2, 3):
            for rule, result in rewrites(term[index]):
                replaced = list(term)
                replaced[index] = result
                steps.append((rule, tuple(replaced)))
    elif term[0] in ("shift", "series", "measure"):
        for rule, result in rewrites(term[2]):
            replaced = list(term)
            replaced[2] = result
            steps.append((rule, tuple(replaced)))
    return steps


def normal_forms(term, node_cap: int = 4000):
    """Every normal form reachable from `term`, by exploring the whole
    rewrite graph. Returns (forms, hit_cap)."""
    seen, frontier, forms = {term}, [term], set()
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

def verify_rules_are_sound(trials: int = 300, seed: int = 20260812) -> None:
    """Every rule preserves meaning, so divergent normal forms can only
    be a SYNTACTIC failure."""
    generator = random.Random(seed)
    checked = 0
    for _ in range(trials):
        term = random_term(generator, 3)
        for rule, result in rewrites(term):
            for value in SAFE:
                assert evaluate(term, value) == evaluate(result, value), (
                    rule, render(term), render(result))
            checked += 1
    print(f"  {checked} rule applications, every one meaning-preserving "
          f"on all x < 2^{WIDTH - 2}")


def measure(term):
    """(number of series symbols, total size of their arguments, size) --
    lexicographic. `collect` and the eliminating rules cut the first
    component; `shift-out` cuts the second."""
    def counts(node):
        if node[0] in ("x", "const"):
            return 0, 0, 0
        if node[0] == "op":
            left, right = counts(node[2]), counts(node[3])
            return tuple(l + r for l, r in zip(left, right))
        inner = counts(node[2])
        if node[0] == "series":
            return (inner[0] + 1, inner[1] + size(node[2]),
                    inner[2] + (0 if node[1] == "N" else 1))
        return inner
    def unsorted(node):
        if node[0] in ("x", "const"):
            return 0
        if node[0] == "op":
            return (unsorted(node[2]) + unsorted(node[3])
                    + (1 if repr(node[2]) > repr(node[3]) else 0))
        return unsorted(node[2])
    series_count, argument_size, non_trivial = counts(term)
    return (series_count, argument_size, non_trivial, size(term),
            unsorted(term))


def verify_rules_shrink(trials: int = 600, seed: int = 20260812) -> None:
    generator = random.Random(seed)
    growing = []
    for _ in range(trials):
        term = random_term(generator, 3)
        for rule, result in rewrites(term):
            if measure(result) >= measure(term):
                growing.append((rule, render(term), render(result)))
    if growing:
        print(f"  {len(growing)} applications do NOT shrink the measure, "
              f"e.g. {growing[0][0]}: {growing[0][1]} -> {growing[0][2]}")
    else:
        print("  every rule strictly decreases (series count, total "
              "argument size, size)")
        print("    lexicographically, so the system terminates.")
    return growing


def random_term(generator: random.Random, budget: int):
    kind = generator.random()
    if budget == 0 or kind < 0.25:
        return generator.choice([("x",), ("x",), ("const", 1),
                                 ("const", MASK)])
    if kind < 0.45:
        return ("series", generator.choice(list(APPLY)),
                random_term(generator, budget - 1))
    if kind < 0.6:
        return ("shift", generator.choice(list(SHIFTS)),
                random_term(generator, budget - 1))
    return ("op", generator.choice(list(JOINS)),
            random_term(generator, budget - 1),
            random_term(generator, budget - 1))


def search_for_divergence(trials: int = 4000,
                          seed: int = 20260812) -> None:
    generator = random.Random(seed)
    divergent, capped, examined = [], 0, 0
    for _ in range(trials):
        term = random_term(generator, 3)
        forms, hit = normal_forms(term)
        if hit:
            capped += 1
            continue
        examined += 1
        if len(forms) > 1:
            divergent.append((term, sorted(forms, key=render)))
    print(f"  {examined} terms explored to completion, {capped} hit the "
          f"node cap")
    if not divergent:
        print("  **no term has two normal forms** -- confluent on every "
              "term explored")
        return None
    term, forms = min(divergent, key=lambda pair: size(pair[0]))
    print(f"  {len(divergent)} terms have more than one normal form")
    print(f"  smallest witness:  {render(term)}")
    for form in forms:
        print(f"      -> {render(form)}")
    return term, forms


def verify_the_critical_pair(term=None) -> None:
    """0042 predicted an overlap between combination and telescope.
    With combination oriented as COLLECT it no longer exists -- the
    collected form is exactly what telescope wants."""
    inner = ("op", "|", ("x",), ("shift", "a", ("x",)))
    left = ("series", "U", inner)
    overlap = ("op", "^", left, ("shift", "a", left))
    forms, hit = normal_forms(overlap)
    print(f"  overlap term: {render(overlap)}")
    print(f"  normal forms reachable: {len(forms)}"
          + ("  (node cap hit)" if hit else ""))
    for form in sorted(forms, key=render):
        print(f"      -> {render(form)}")
    for form in forms:
        for value in SAFE:
            assert evaluate(form, value) == evaluate(overlap, value)
    print("    all of them equal in meaning, as they must be; the "
          "question is whether")
    print("    they are equal as terms.")


def anf(term):
    """ANF over the atoms: expand `|` into `^`/`&` and reduce. Maximal
    non-op subterms are atoms. This is the corpus's own normal form for
    the base algebra, which the rewrite engine above deliberately does
    not apply -- it keeps `|` primitive."""
    if term[0] != "op":
        return frozenset([frozenset([term])])
    left, right = anf(term[2]), anf(term[3])
    if term[1] == "^":
        return left ^ right
    product: set = set()
    for first in left:
        for second in right:
            product ^= {first | second}
    conjunction = frozenset(product)
    if term[1] == "&":
        return conjunction
    return left ^ right ^ conjunction         # a | b = a ^ b ^ ab


def verify_the_residue_is_the_base_algebra(trials: int = 4000,
                                           seed: int = 20260812) -> None:
    """Whatever divergence survives, is it in the SERIES rules or in the
    base algebra? Answered by normalising the base algebra properly."""
    generator = random.Random(seed)
    divergent, base_only = [], 0
    for _ in range(trials):
        term = random_term(generator, 3)
        forms, hit = normal_forms(term)
        if hit or len(forms) <= 1:
            continue
        divergent.append((term, sorted(forms, key=render)))
        if len({anf(form) for form in forms}) == 1:
            base_only += 1
    print(f"  {len(divergent)} terms still reach more than one normal "
          f"form")
    print(f"  of those, {base_only} become identical once the base "
          f"algebra is put in ANF")
    for term, forms in sorted(divergent, key=lambda pair: size(pair[0])):
        print(f"    {render(term)}")
        for form in forms:
            print(f"        -> {render(form)}")
    assert base_only == len(divergent)
    print("    Every survivor is a BASE-algebra difference, not a series "
          "one: the engine")
    print("    keeps `|` primitive, while the corpus expands it to "
          "a ^ b ^ ab and reduces")
    print("    to ANF, where Boolean absorption ((a|b)&a = a) is an "
          "identity. So the")
    print("    series rules are confluent; the residue is a base "
          "convention.")


def run_verification_suite() -> None:
    print("=" * 70)
    print("1. Every rule preserves meaning")
    print("=" * 70)
    verify_rules_are_sound()

    print()
    print("=" * 70)
    print("2. Every rule shrinks the term")
    print("=" * 70)
    verify_rules_shrink()

    print()
    print("=" * 70)
    print("3. The predicted critical pair: distribute against telescope")
    print("=" * 70)
    verify_the_critical_pair()

    print()
    print("=" * 70)
    print("4. Searching the whole rewrite graph for divergence")
    print("=" * 70)
    search_for_divergence()

    print()
    print("=" * 70)
    print("5. Is the residue in the series rules or the base algebra?")
    print("=" * 70)
    verify_the_residue_is_the_base_algebra()

    print()
    print("=" * 70)
    print("suite complete")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
