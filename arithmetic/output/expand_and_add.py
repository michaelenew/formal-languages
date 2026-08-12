"""Expand-and-cancel as the canonical form, and addition in the frame.

Two things, and the first makes the second sayable.

**Expansion, not collection.** 0043 chose `collect` -- `S(a) ∘ S(b) ->
S(a ∘ b)` -- as the combining rule, and that choice was made before
there was a canonical form to judge it against. The other orientation is
0042 §2's fixpoint law run FORWARD,

    S(t)  ->  t  ∘  σ_S(S t)

with ANF's symmetric difference left to do the cancelling. It subsumes
two rules at once:

    telescope    !(t) ^ a(!t)  ->  (t ^ a(!t)) ^ a(!t)  ->  t
    collect      both sides expand to the same sum

and it does subsume telescoping. It does NOT subsume `collect`, which
is 0042 §2's *second* universal law (distribution) and independent of
the fixpoint -- measured in §2. That is worth knowing: the two rules
0044 ordered against each other are not two halves of one thing.

**Addition.** With expansion available the carry is a sentence:

    p = x ^ y                 g = x & y
    C = g | (p & a(C))                       the carry set
    x + y = p ^ a(C)

`C = g | (p & a(C))` is 0042's fixpoint shape `S = base ∘ σ(S)` with the
shift `a` replaced by `σ_p(z) = p & a(z)`. So addition is a cell of the
schema over a **guarded shift**, and the schema's own two shifts are the
two constant cases of one affine family

    σ_{p,q}(z) = (p & a(z)) ^ q      a = σ_{Ω,0}    b = σ_{Ω,1}

Run directly for the verification suite.
"""

from __future__ import annotations

import functools
import random

import sentence_canonical_form as S
from sentence_canonical_form import (OMEGA, ONE, X, Y, ZERO, atom, conj,
                                     equal, render, shift_a, xor)

WIDTH = 24
MASK = (1 << WIDTH) - 1


# ---------------------------------------------------------------------
# 1. expansion
# ---------------------------------------------------------------------

MEASURE_EXPANSION = {
    # each measure is its own telescoping, solved for the measure
    "lowset": lambda p: xor(p, conj(p, shift_a(S._raw_atom("U", p)))),
    "lowzero": lambda p: conj(xor(p, OMEGA),
                              S.shift_b(S._raw_atom("T", p))),
}


def expand_once(poly):
    """Unfold every series atom by the fixpoint law, at every depth.

    The measures unfold too -- `lowset(t) = t & ¬a(U t)` and
    `lowzero(t) = ¬t & b(T t)` -- because they are what telescoping
    produces, so leaving them opaque would stop expansion one step short
    of the identity it is meant to reach.
    """
    result = ZERO
    for atoms in poly:
        piece = OMEGA
        for element in atoms:
            piece = conj(piece, _expand_atom(element))
        result = xor(result, piece)
    return result


def _expand_atom(element):
    kind, *rest = element
    if kind in S.LEAF:
        return frozenset([frozenset([element])])
    inner = rest[0]                 # arguments are NOT expanded: an
    # occurrence inside `a(...)` must stay put, or the two copies in a
    # telescoping pair unfold to different depths and stop cancelling
    if kind in S.SERIES:
        join, shift = S.SERIES[kind]
        return S.apply_join(join, inner,
                            S.apply_shift(shift, S._raw_atom(kind, inner)))
    if kind in MEASURE_EXPANSION:
        return MEASURE_EXPANSION[kind](inner)
    if kind == "a":
        return S.shift_a(inner)
    return S._raw_atom(kind, inner)


def _reduced(poly):
    forms, capped = S.normal_forms(poly)
    if capped or len(forms) != 1:
        return None
    return next(iter(forms))


def canonical(poly, depth: int = 2):
    """Reduce, expand, reduce -- `depth` times.

    The local rules (settle, low-bit, confine, unit, absorb, shift-out,
    contain) still run: expansion replaces `collect` and `telescope`, not
    the prefix analysis. Cancellation is ANF's, not a rule.
    """
    current = _reduced(poly)
    for _ in range(depth):
        if current is None:
            return None
        current = _reduced(expand_once(current))
    return current


def without_collect_and_telescope():
    """Turn off the two rules expansion is meant to replace."""
    S._collect = lambda poly, depth: []
    S._telescope = lambda poly: []
    S.rewrites.cache_clear()


def verify_expansion_subsumes_the_two_rules() -> None:
    """Telescoping and collection, done by unfolding and cancelling."""
    t = X
    cases = [
        ("telescope, ^", xor(atom("!", t), shift_a(atom("!", t))), t),
        ("telescope, |", xor(atom("U", t), shift_a(atom("U", t))),
         atom("lowset", t)),
        ("telescope, &", xor(atom("T", t), S.shift_b(atom("T", t))),
         atom("lowzero", t)),
        ("collect, ^", xor(atom("!", X), atom("!", Y)),
         atom("!", xor(X, Y))),
        ("collect, &", conj(atom("T", X), atom("T", Y)),
         atom("T", conj(X, Y))),
        ("collect, |", S.disj(atom("U", X), atom("U", Y)),
         atom("U", S.disj(X, Y))),
    ]
    for label, left, right in cases:
        assert equal(left, right), label
        reached = None
        for depth in range(1, 5):
            if canonical(left, depth) == canonical(right, depth):
                reached = depth
                break
        mark = f"depth {reached}" if reached else "NOT reached by depth 4"
        print(f"    {label:<16} {render(left):<34} {mark}")
    print()
    print("  All three telescopings fall out at ONE unfolding: expand")
    print("  `S(t)` to `t ∘ σ(S t)` and the partner annihilates under XOR.")
    print("  So `telescope` is not a rule, it is the fixpoint law plus")
    print("  ANF -- provided the MEASURES unfold too, since they are what")
    print("  telescoping produces.")
    print()
    print("  `collect` is NOT reached, at any depth, and that is the point.")
    print("  Expanding `!(x) ^ !(y)` gives `x ^ y ^ a(!x) ^ a(!y)` and")
    print("  expanding `!(x^y)` gives `x ^ y ^ a(!(x^y))`; the difference")
    print("  is the same question one shift up, forever. `collect` is")
    print("  0042 §2's SECOND law, distribution, and it is independent of")
    print("  the fixpoint. 0044 ordered the two against each other as if")
    print("  they were rivals; they are not the same fact at all.")


def verify_expansion_closes_the_residue(trials=700, seed=20260915,
                                        depth=2) -> None:
    """0048 §5, with expansion instead of collection."""
    without_collect_and_telescope()
    generator = random.Random(seed)
    pool = []
    for index in range(trials):
        builder = S.random_poly if index % 2 else S.structured_poly
        poly = builder(generator, 3)
        form = canonical(poly, depth)
        if form is not None:
            pool.append((poly, form))
    groups = {}
    for poly, form in pool:
        groups.setdefault(S._fingerprint(poly), []).append((poly, form))
    unidentified, unsound = [], 0
    import itertools
    for members in groups.values():
        for first, second in itertools.combinations(members[:5], 2):
            try:
                same = equal(first[0], second[0])
            except RuntimeError:
                continue
            if same and first[1] != second[1]:
                unidentified.append((render(first[1]), render(second[1])))
    seen = {}
    for poly, form in pool:
        seen.setdefault(form, []).append(poly)
    for form, members in seen.items():
        for first, second in itertools.combinations(members[:4], 2):
            try:
                if not equal(first, second):
                    unsound += 1
            except RuntimeError:
                continue
    print(f"  {len(pool)} terms canonicalised by expand-and-cancel "
          f"(depth {depth})")
    print(f"  {unsound} pairs share a form without being equal "
          f"(should be 0)")
    print(f"  {len(unidentified)} pairs are equal with different forms "
          f"-- 0048 measured 19 with collect+telescope")
    for first, second in sorted(unidentified,
                                key=lambda pr: len(pr[0]) + len(pr[1]))[:6]:
        print(f"    {first}   vs   {second}")
    assert not unsound
    return unidentified


def verify_expansion_costs_what_the_join_costs() -> None:
    """What k terms of a series cost in ANF, by join."""
    print(f"    {'join':<6} " + " ".join(f"{'k=%d' % k:>6}"
                                         for k in range(1, 7)))
    for join, label in (("^", "^"), ("|", "|"), ("&", "&")):
        sizes = []
        for count in range(1, 7):
            total = None
            for index in range(count):
                piece = X
                for _ in range(index):
                    piece = shift_a(piece)
                total = piece if total is None else S.apply_join(join, total,
                                                                 piece)
            sizes.append(len(total))
        print(f"    {label:<6} " + " ".join(f"{n:>6}" for n in sizes))
    print()
    print("  `^` costs k monomials, `&` costs one (a single monomial with")
    print("  k factors), and `|` costs 2^k - 1. So the partial sums of the")
    print("  `|` cell are the expensive ones, and its closed form `U` is")
    print("  the only thing standing between the sentence and an")
    print("  exponential -- 0049 §5 again, now as the price of expanding")
    print("  rather than the price of failing to recognise.")


# ---------------------------------------------------------------------
# 3. addition in the sentence frame
# ---------------------------------------------------------------------

def carry(x: int, y: int, width: int = WIDTH) -> int:
    """The carry set, by iterating its own fixpoint to closure."""
    mask = (1 << width) - 1
    propagate, generate = (x ^ y) & mask, (x & y) & mask
    current = 0
    for _ in range(width + 2):
        current = (generate | (propagate & ((current << 1) & mask))) & mask
    return current


def verify_addition_is_a_fixpoint(trials=4000, seed=20260929) -> None:
    """`x + y = (x^y) ^ a(C)` with `C = (x&y) | ((x^y) & a(C))`."""
    generator = random.Random(seed)
    mask = (1 << (WIDTH - 2)) - 1
    for _ in range(trials):
        x = generator.randrange(mask)
        y = generator.randrange(mask)
        c = carry(x, y)
        assert (x ^ y) ^ ((c << 1) & ((1 << WIDTH) - 1)) == x + y, (x, y)
        assert c == ((x & y) | ((x ^ y) & ((c << 1) &
                                           ((1 << WIDTH) - 1)))), (x, y)
    print(f"  {trials} random pairs at width {WIDTH}:")
    print()
    print("      p = x ^ y                 g = x & y")
    print("      C = g | (p & a(C))                     the carry set")
    print("      x + y = p ^ a(C)")
    print()
    print("  both the closed form and the fixpoint equation hold exactly.")
    print("  Nothing here is new machinery -- `^`, `&`, `|`, `a` only.")


def verify_the_carry_is_a_guarded_cell(trials=3000, seed=20260929) -> None:
    """`C = g | σ_p(C)` for the guarded shift `σ_p(z) = p & a(z)`.

    That is 0042 §1's schema shape with the shift no longer fixed. The
    schema's own two shifts are the constant cases of one affine family.
    """
    generator = random.Random(seed)
    mask = (1 << (WIDTH - 2)) - 1
    for _ in range(trials):
        x = generator.randrange(mask)
        y = generator.randrange(mask)
        propagate, generate = x ^ y, x & y
        full = (1 << WIDTH) - 1
        unfolded, term = 0, generate               # ⋁_k σ_p^k(g)
        for _ in range(WIDTH + 2):
            unfolded |= term
            term = propagate & ((term << 1) & full)
        assert unfolded == carry(x, y), (x, y)
    print(f"  {trials} pairs: the carry is the `|` cell over the guarded")
    print("  shift, unfolded --")
    print()
    print("      C  =  ⋁_k σ_p^k(g)      σ_p(z) = p & a(z)")
    print()
    print("  and the schema's two shifts are the constant cases of")
    print()
    print("      σ_{p,q}(z) = (p & a(z)) ^ q       a = σ_{Ω,0}   b = σ_{Ω,1}")
    print()
    print("  So `U` is the p=Ω member of the same family the carry lives")
    print("  in, and `T` is the p=Ω, q=1 member with the join changed.")


def verify_succ_is_the_y_equals_one_case(width=16) -> None:
    """`C = T(x)` when `y = 1`, which is the corpus's `succ`."""
    def trailing(value):
        total, lifted = value, value
        for _ in range(width + 2):
            lifted = ((lifted << 1) | 1) & ((1 << width) - 1)
            total &= lifted
        return total
    for value in range(1 << (width - 2)):
        assert carry(value, 1, width) == trailing(value), value
        assert (value ^ 1) ^ ((trailing(value) << 1) &
                              ((1 << width) - 1)) == value + 1, value
    print(f"  every x < {1 << (width - 2)}:  C(x, 1) = T(x)")
    print()
    print("  so  x + 1  =  (x ^ 1) ^ a(T x)  =  x ^ b(T x)")
    print()
    print("  which is the corpus's `succ`, recovered as the y=1 case. The")
    print("  trailing-ones mask was never a special construction -- it is")
    print("  the carry set of adding one, and 0041's `T`/`succ` circle is")
    print("  that identity read in both directions.")


def verify_which_universal_laws_the_guarded_cell_keeps(trials=2000,
                                                       seed=20260929) -> None:
    """0042 §2's three laws, asked of the carry."""
    generator = random.Random(seed)
    mask = (1 << (WIDTH - 2)) - 1
    full = (1 << WIDTH) - 1
    broken = {"fixpoint": 0, "distribution": 0, "telescoping": 0}
    for _ in range(trials):
        x = generator.randrange(mask)
        y = generator.randrange(mask)
        propagate, generate = x ^ y, x & y
        current = carry(x, y)
        if current != (generate | (propagate & ((current << 1) & full))):
            broken["fixpoint"] += 1
        # distribution over the BASE, holding the guard fixed
        other = generator.randrange(mask)
        left = _guarded(propagate, generate | other)
        if left != (_guarded(propagate, generate)
                    | _guarded(propagate, other)):
            broken["distribution"] += 1
        # telescoping: C ^ sigma_p(C) -- what does cancellation return?
        shifted = propagate & ((current << 1) & full)
        if (current ^ shifted) != (generate & ~shifted & full):
            broken["telescoping"] += 1
    for law, count in broken.items():
        print(f"    {law:<14} {'holds' if not count else f'fails ({count})'}")
    print()
    print("  Fixpoint by definition. **Distribution survives** -- over the")
    print("  base, with the guard held fixed -- so the carry has 0042 §2's")
    print("  combination law and `collect` applies to it unchanged.")
    print("  **Telescoping survives, with measure `g & ¬σ_p(C)`** -- the")
    print("  part of the generate set the propagation did not already")
    print("  cover. For the plain `|` cell (p = Ω, g = t) that is")
    print("  `t & ¬a(U t)`, which is `lowset(t)`: the schema's measure is")
    print("  the p = Ω case of the carry's.")
    print("  So the guarded cell is a full member of the schema, not a")
    print("  degenerate one -- which is why addition was reachable all")
    print("  along and only the shift had to be widened.")


def _guarded(propagate, base, width=WIDTH):
    full = (1 << width) - 1
    current = 0
    for _ in range(width + 2):
        current = (base | (propagate & ((current << 1) & full))) & full
    return current


def verify_containment_is_just_a_statement() -> None:
    """`A ⊑ B` IS the sentence `A ^ AB` -- A is empty where it misses B.

    0048 and 0049 treated containment as a relation needing its own
    derivation system. It does not: it is a statement of the language,
    and a canonical form that sends true statements to 0 handles it with
    no order theory at all. Including the case 0049 §6 called the wall.
    """
    cases = [
        ("T(t) ⊑ t", atom("T", X), X),
        ("T(t) ⊑ b(T t)", atom("T", X), S.shift_b(atom("T", X))),
        ("t ⊑ U(t)", X, atom("U", X)),
        ("!(t) ⊑ U(t)", atom("!", X), atom("U", X)),
        ("a(!t) ⊑ U(t)", shift_a(atom("!", X)), atom("U", X)),
        ("lowset(t) ⊑ t", atom("lowset", X), X),
    ]
    for label, small, big in cases:
        statement = xor(small, conj(small, big))
        assert equal(statement, ZERO), label
        reached = next((d for d in range(4)
                        if canonical(statement, d) == ZERO), None)
        mark = ("-> 0 at depth %d" % reached if reached is not None
                else "NOT reduced")
        print(f"    {label:<18} {render(statement):<28} {mark}")
    print()
    print("  `T(t) ^ T(t)·b(T t)` needs one unfolding and then goes to 0.")
    print("  That is exactly the identity 0049 §6 could not turn into a")
    print("  rule -- because it tried to make containment a factor-drop")
    print("  between two atoms, when the statement is a polynomial and")
    print("  expansion is what opens it.")


def run_verification_suite() -> None:
    sections = [
        ("Expansion does telescoping, and does not do collection",
         verify_expansion_subsumes_the_two_rules),
        ("What a series costs, per join",
         verify_expansion_costs_what_the_join_costs),
        ("Addition is a fixpoint", verify_addition_is_a_fixpoint),
        ("The carry is a guarded cell of the schema",
         verify_the_carry_is_a_guarded_cell),
        ("succ is the y = 1 case", verify_succ_is_the_y_equals_one_case),
        ("Which universal laws the guarded cell keeps",
         verify_which_universal_laws_the_guarded_cell_keeps),
        ("Containment is just a statement",
         verify_containment_is_just_a_statement),
    ]
    without_collect_and_telescope()
    for index, (title, check) in enumerate(sections, start=1):
        print("=" * 70)
        print(f"{index}. {title}")
        print("=" * 70)
        check()
        print()
    print("=" * 70)
    print("7. Expand-and-cancel as the canonical form")
    print("=" * 70)
    verify_expansion_closes_the_residue()
    print()
    print("=" * 70)
    print("suite complete")
    print("=" * 70)


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    run_verification_suite()
