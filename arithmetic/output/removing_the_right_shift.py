"""Is the right shift a second information destroyer? No -- it is `&`.

The objection: `&` was the only operator that could erase information,
and a second squasher would be a real addition to the language. Post's
lattice says a two-valued logic has one information-losing direction
(the order), so there should not be two.

`h` is not one. The whole content of `h` is

    a(h(t))  =  (Ω ^ 1) t

-- its information loss factors exactly through masking by a constant,
and what is left is the injective map `a`. §1 checks that, and checks
the kernels agree, which is the statement in the form that matters:
`h` identifies two values iff `& (Ω^1)` does.

§2 turns that into the general procedure. For any base-algebra term `E`
of `h`-depth `d`,

    a^d(E)   is h-free, and equals  E << d   exactly

so `E = 0` iff `a^d(E) = 0` -- not merely zero-equivalent but an exact
scaling, which is a stronger claim and an easier one to check.

§3 asks what the *series* column costs. Removing `h` deletes exactly
two cells of 0042 §1's table, `!ʰ` and `D`, and those are precisely the
two 0042 §6.3 flagged as absent from the corpus's operator list. §4
finds the one thing that genuinely needs a downward flow, and §5 re-runs
0044's confluence suite with `h` gone.

Run directly for the verification suite.
"""

from __future__ import annotations

import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import series_confluence_anf as anf              # noqa: E402

# a universe wide enough that nothing in §1-§2 ever reaches the top bit
WIDE = 20
WIDE_MASK = (1 << WIDE) - 1
INPUTS = range(1 << 8)


# ---------------------------------------------------------------------
# a small term language for the base algebra alone
# ---------------------------------------------------------------------
#   ("x",) | ("c", v) | ("a", t) | ("b", t) | ("h", t)
#         | ("^", t, u) | ("&", t, u)

def evaluate(term, value: int) -> int:
    kind = term[0]
    if kind == "x":
        return value
    if kind == "c":
        return term[1] & WIDE_MASK
    if kind == "a":
        return (evaluate(term[1], value) << 1) & WIDE_MASK
    if kind == "b":
        return ((evaluate(term[1], value) << 1) | 1) & WIDE_MASK
    if kind == "h":
        return evaluate(term[1], value) >> 1
    if kind == "^":
        return evaluate(term[1], value) ^ evaluate(term[2], value)
    return evaluate(term[1], value) & evaluate(term[2], value)


def render(term) -> str:
    kind = term[0]
    if kind == "x":
        return "x"
    if kind == "c":
        return {0: "0", WIDE_MASK: "Ω", WIDE_MASK ^ 1: "(Ω^1)"}.get(
            term[1], str(term[1]))
    if kind in ("a", "b", "h"):
        return f"{kind}({render(term[1])})"
    return f"({render(term[1])} {kind} {render(term[2])})"


def h_depth(term) -> int:
    if term[0] in ("x", "c"):
        return 0
    if term[0] in ("a", "b"):
        return h_depth(term[1])
    if term[0] == "h":
        return 1 + h_depth(term[1])
    return max(h_depth(term[1]), h_depth(term[2]))


def contains_h(term) -> bool:
    return h_depth(term) > 0


# ---------------------------------------------------------------------
# 1. h's information loss is `&`'s
# ---------------------------------------------------------------------

def verify_h_is_masking_in_disguise() -> None:
    """`a(h(v)) = (Ω^1) v`, and `h` and `& (Ω^1)` identify the same
    pairs. The second is the statement that matters: an operator's
    information loss *is* the partition it induces, and these two
    partitions are equal."""
    for value in range(1 << 12):
        assert ((value >> 1) << 1) == value & (WIDE_MASK ^ 1), value
    print("  a(h(v)) = (Ω^1) v          for every v")

    collisions_h, collisions_mask = {}, {}
    for value in range(1 << 12):
        collisions_h.setdefault(value >> 1, []).append(value)
        collisions_mask.setdefault(value & ~1, []).append(value)
    classes_h = {tuple(group) for group in collisions_h.values()}
    classes_mask = {tuple(group) for group in collisions_mask.values()}
    assert classes_h == classes_mask
    print(f"  ker h = ker (& (Ω^1))      {len(classes_h)} classes, identical")
    print("  so `h` is `& (Ω^1)` followed by the injective `a`-inverse:")
    print("  it destroys the low bit and nothing else. There is no second")
    print("  squasher -- Post's ordering direction is still the only one.")


# ---------------------------------------------------------------------
# 2. eliminating h from any base-algebra term
# ---------------------------------------------------------------------

def lift(term, depth: int):
    """`a^depth(term)`, written without `h`. Requires depth >= h_depth.

    `a` is an algebra homomorphism -- it commutes with `^` and `&` and
    scales constants -- so it pushes all the way to the leaves. At an
    `h` it cancels: `a(h(t)) = (Ω^1) t`, one shift spent, one `h` gone.
    """
    kind = term[0]
    if kind == "x":
        return _a_power(("x",), depth)
    if kind == "c":
        return ("c", (term[1] << depth) & WIDE_MASK)
    if kind == "a":
        return ("a", lift(term[1], depth))
    if kind == "b":
        # b(t) = a(t) ^ 1, and `a` distributes over both
        return ("^", ("a", lift(term[1], depth)),
                ("c", (1 << depth) & WIDE_MASK))
    if kind == "h":
        assert depth >= 1, "not enough shifts to cancel the h"
        return lift(("&", term[1], ("c", WIDE_MASK ^ 1)), depth - 1)
    return (kind, lift(term[1], depth), lift(term[2], depth))


def _a_power(term, depth: int):
    for _ in range(depth):
        term = ("a", term)
    return term


def eliminate(term):
    """The h-free companion of `term`: same value, scaled by 2^d."""
    return lift(term, h_depth(term))


def random_term(generator, budget):
    if budget == 0 or generator.random() < 0.3:
        return generator.choice([("x",), ("x",), ("c", 1),
                                 ("c", generator.randrange(1, 64))])
    kind = generator.choice(["a", "b", "h", "h", "^", "&"])
    if kind in ("a", "b", "h"):
        return (kind, random_term(generator, budget - 1))
    return (kind, random_term(generator, budget - 1),
            random_term(generator, budget - 1))


def verify_the_elimination(trials=4000, seed=20260814) -> None:
    generator = random.Random(seed)
    checked = deepest = 0
    for _ in range(trials):
        term = random_term(generator, 3)
        depth = h_depth(term)
        if not depth:
            continue
        free = eliminate(term)
        assert not contains_h(free), render(free)
        for value in INPUTS:
            assert evaluate(free, value) == evaluate(term, value) << depth, (
                render(term), render(free), value)
        checked += 1
        deepest = max(deepest, depth)
    print(f"  {checked} terms with an `h`, h-depth up to {deepest}")
    print(f"  a^d(E) is h-free and equals E << d exactly, on all "
          f"{len(INPUTS)} inputs")
    print("  so E = 0 iff a^d(E) = 0 -- zero-equivalence, by exact scaling")
    example = ("^", ("h", ("&", ("x",), ("c", 12))), ("a", ("x",)))
    print(f"  e.g.  {render(example)}")
    print(f"    ->  {render(eliminate(example))}")


# ---------------------------------------------------------------------
# 3. what the series column costs
# ---------------------------------------------------------------------

def the_schema_without_h() -> None:
    """0042 §1 was a 3x3 table. Drop the `h` column and see what is
    lost."""
    width, mask = 12, (1 << 12) - 1
    shifts = {"a": lambda v: (v << 1) & mask,
              "b": lambda v: ((v << 1) | 1) & mask,
              "h": lambda v: v >> 1}
    joins = {"^": lambda p, q: p ^ q,
             "|": lambda p, q: p | q,
             "&": lambda p, q: p & q}

    def cell(join, shift, value):
        total, lifted = value, value
        for _ in range(2 * width):
            lifted = shifts[shift](lifted)
            total = joins[join](total, lifted)
        return total

    named = {"!": ("^", "a"), "!ʰ": ("^", "h"), "U": ("|", "a"),
             "D": ("|", "h"), "T": ("&", "b")}
    print("  0042 §1's table, with the `h` column marked:")
    print(f"    {'join':<6}{'a':<12}{'b':<12}{'h  (dropped)':<14}")
    for join in ("^", "|", "&"):
        row = []
        for shift in ("a", "b", "h"):
            values = [cell(join, shift, v) for v in range(1 << 8)]
            label = next((n for n, key in named.items()
                          if key == (join, shift)), None)
            if label is None:
                label = "0" if not any(values) else (
                    "Ω" if all(v == mask for v in values) else "divergent")
            row.append(label)
        print(f"    {join:<6}{row[0]:<12}{row[1]:<12}{row[2]:<14}")
    print()
    print("  The `h` column is exactly {!ʰ, D} -- and 0042 §6.3 already")
    print("  recorded that those two 'fall out of the schema but do not")
    print("  appear in the corpus's operator list'. Dropping `h` deletes")
    print("  the two cells the corpus never had, and leaves {!, U, T}:")
    print("  the corpus's own series, exactly.")


# ---------------------------------------------------------------------
# 4. the one thing that needs a downward flow
# ---------------------------------------------------------------------

def verify_the_h_free_fragment_is_lsb_causal() -> None:
    """Every h-free operator has output bit i depending only on input
    bits <= i. That is what makes them all one-directional, and it is
    why nothing built from them can be `N`."""
    width, mask = 10, (1 << 10) - 1

    def series(join, shift, value):
        step = {"a": lambda v: (v << 1) & mask,
                "b": lambda v: ((v << 1) | 1) & mask}[shift]
        combine = {"^": lambda p, q: p ^ q, "|": lambda p, q: p | q,
                   "&": lambda p, q: p & q}[join]
        total, lifted = value, value
        for _ in range(2 * width):
            lifted = step(lifted)
            total = combine(total, lifted)
        return total

    operators = {
        "a": lambda v: (v << 1) & mask,
        "b": lambda v: ((v << 1) | 1) & mask,
        "!": lambda v: series("^", "a", v),
        "U": lambda v: series("|", "a", v),
        "T": lambda v: series("&", "b", v),
        "N": lambda v: 0 if v == 0 else mask,
        "h": lambda v: v >> 1,
    }

    def causal(operator):
        """Does flipping a bit above position i ever change output bit i?"""
        for value in range(1 << width):
            for high in range(width):
                flipped = value ^ (1 << high)
                below = (1 << high) - 1
                if operator(value) & below != operator(flipped) & below:
                    return False
        return True

    print(f"  {'operator':<10}{'LSB-causal':<14}")
    for name, operator in operators.items():
        print(f"  {name:<10}{str(causal(operator)):<14}")
    print()
    print("  The h-free operators are all LSB-causal: information moves")
    print("  up, never down. So no expression over {x, ^, &, a, b, !, U, T,")
    print("  constants} can compute `N`, whose bit 0 is the OR of every")
    print("  bit of x. `N` is the corpus's one downward-flowing operator,")
    print("  and it is already primitive (0038, and 0042 §3: `N` is not a")
    print("  cell of the schema). Removing `h` does not reach it.")
    print()
    print("  What is lost: 0042 §3's `N = U | D` is no longer a sentence")
    print("  of the language, since `D` is gone. `N` keeps its rules and")
    print("  its behaviour; it loses its derivation.")


# ---------------------------------------------------------------------
# 5. the rewrite system with h removed
# ---------------------------------------------------------------------

def rerun_confluence_without_h() -> None:
    anf.configure_without_h()
    print(f"  shifts {sorted(anf.SHIFTS)}   series "
          f"{sorted(anf.SERIES)} + N")
    print()
    anf.verify_rules_are_sound(trials=1500)
    anf.verify_rules_shrink(trials=400)
    anf.verify_rules_shrink(trials=400, builder=anf.random_structured_poly)
    anf.verify_the_structural_rules_fire()
    print()
    anf.search_for_divergence(trials=1500)
    anf.search_for_divergence(trials=700, builder=anf.random_structured_poly,
                              depth=2)
    print()
    anf.report_rule_census(trials=1500)


def verify_the_measure_can_revert() -> None:
    """0044 §5 had to reorder the termination measure because
    `h(D t) & 1 -> N(h t) & 1` trades a named series for a bigger
    argument. That rule needs `h` *and* `D`. With both gone, does
    0043's ordering come back?"""
    original = anf.measure

    def old_ordering(poly):
        count, non_n, arguments, total = original(poly)
        return count, arguments, non_n, total

    generator = random.Random(20260814)
    anf.measure = old_ordering
    growing = []
    for _ in range(600):
        for builder in (anf.random_poly, anf.random_structured_poly):
            poly = builder(generator, 3)
            for rule, result in anf.rewrites(poly):
                if old_ordering(result) >= old_ordering(poly):
                    growing.append((rule, anf.render(poly)))
    anf.measure = original
    if growing:
        print(f"  0043's ordering still fails: {len(growing)} applications, "
              f"e.g. {growing[0][0]} on {growing[0][1]}")
    else:
        print("  0043's ordering (series, argument size, non-N, size) is")
        print("  sufficient again -- the reorder 0044 §5 forced was paid for")
        print("  by `h(D t) & 1`, and that rule left with `h`.")


def run_verification_suite() -> None:
    for index, (title, check) in enumerate([
            ("`h` is `&` in disguise", verify_h_is_masking_in_disguise),
            ("Removing `h` from any base-algebra term",
             verify_the_elimination),
            ("What the series column costs", the_schema_without_h),
            ("The one operator that flows downward",
             verify_the_h_free_fragment_is_lsb_causal),
            ("The rewrite system with `h` removed",
             rerun_confluence_without_h),
            ("Can the termination measure revert?",
             verify_the_measure_can_revert)], start=1):
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
