"""The Post-style structure of this layer: three closure levels, three
different answers to "is XOR necessary?".

Post's theorem classifies Boolean functions under COMPOSITION, and its
engine (as the corpus's `older/Posts Functional Completeness
Theorem.md` sets out) is preservation: if every elementary function
has property X, so does every composition, so a generating set must
break every X. Universal algebra generalizes the engine -- the
corpus's own "f satisfies t if and only if t satisfies f, by
symmetry" is exactly the commutation relation behind the Pol-Inv
Galois connection (Geiger; Bodnarchuk-Kaluznin-Kotov-Romov).

Applying that engine here shows the basis question has three answers
depending on which closure is meant:

    LEVEL          closure operations        preservation invariant
    ------------------------------------------------------------------
    term           composition (nesting)     monotonicity (Post's M)
    pp             conjunction, exists, =    polymorphisms (Geiger)
    first-order    ... and negation          invariance / stability

    LEVEL          is ^ derivable from {&, <<, constants}?
    ------------------------------------------------------------------
    term           NO   -- &, <<, constants are all monotone; ^ is not
    pp             NO   -- and not even union: intersection is a
                            polymorphism of every base relation but of
                            neither the ^-graph nor the union-graph
    first-order    YES  -- relative complement is definable by
                            subset-extremality, so ^ comes free

So negation is exactly what collapses the basis, and the minimal
first-order basis of the whole canonical layer is

    { &, << } + constants

with both generators provably necessary. The corpus's XOR is
indispensable at the term level (where its work is real) and
redundant at the wiring level (where equality and negation are
primitives of the logic itself).

Run this file directly; every claim below that can be checked, is.
"""

from __future__ import annotations

import os
import sys
from itertools import product as cartesian_product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_automata import (
    DFA, Term, Variable, Constant, statement_of_less_or_equal)

x: Term = Variable('x')
y: Term = Variable('y')
z: Term = Variable('z')
u: Term = Variable('u')


# ---------------------------------------------------------------------
# Level 1 -- term closure: the corpus's Post argument, in this setting
# ---------------------------------------------------------------------

def is_monotone_binary(operation, sample_width: int) -> bool:
    """Is the operation monotone with respect to subset order?"""
    universe = range(1 << sample_width)
    for left, right in cartesian_product(universe, repeat=2):
        if left & right != left:      # keep only left subset of right
            continue
        for other in universe:
            if (operation(left, other) & operation(right, other)
                    != operation(left, other)):
                return False
            if (operation(other, left) & operation(other, right)
                    != operation(other, left)):
                return False
    return True


def show_term_level() -> None:
    print("=" * 70)
    print("LEVEL 1  TERM CLOSURE -- Post's argument, applied here")
    print("=" * 70)
    print("""
Post's engine: a property closed under composition, held by every
generator, is held by everything they generate. Monotonicity with
respect to subset order is such a property.""")
    intersection_monotone = is_monotone_binary(
        lambda left, right: left & right, 4)
    shift_monotone = is_monotone_binary(
        lambda left, right: left << 1, 4)
    constant_monotone = is_monotone_binary(
        lambda left, right: 5, 4)
    exclusive_or_monotone = is_monotone_binary(
        lambda left, right: left ^ right, 4)
    print(f"    &  monotone: {intersection_monotone}")
    print(f"    << monotone: {shift_monotone}")
    print(f"    constants monotone: {constant_monotone}")
    print(f"    ^  monotone: {exclusive_or_monotone}"
          f"   <-- witness: grow the left input from the empty set to"
          f" {{0}}, holding the right input at {{0}}: the output"
          f" SHRINKS from {{0}} to the empty set")
    assert (0 ^ 1) == 1 and (1 ^ 1) == 0     # growing shrank it
    assert (intersection_monotone and shift_monotone
            and constant_monotone and not exclusive_or_monotone)
    print("""
    => ^ is NOT a composition of {&, <<, constants}.  This is exactly
       the corpus's Post-class reasoning, and it is why the original
       operator set needed XOR: at the term level its work is real.
""")


# ---------------------------------------------------------------------
# Level 2 -- pp closure: polymorphisms (the Galois connection)
# ---------------------------------------------------------------------

def is_preserved_by_intersection(relation_test, arity: int,
                                 sample_width: int) -> bool:
    """Is the relation closed under coordinatewise intersection?
    That is: is intersection a polymorphism of the relation?"""
    universe = range(1 << sample_width)
    tuples = [candidate for candidate in
              cartesian_product(universe, repeat=arity)
              if relation_test(*candidate)]
    tuple_set = set(tuples)
    for first in tuples:
        for second in tuples:
            meet = tuple(left & right
                         for left, right in zip(first, second))
            if meet not in tuple_set:
                return False
    return True


def show_pp_level() -> None:
    print("=" * 70)
    print("LEVEL 2  pp CLOSURE -- polymorphisms")
    print("=" * 70)
    print("""
Drop negation, keep conjunction, existential quantification and
equality: positive primitive (pp) definability. The preservation
lemma is elementary --

    if every base relation is closed under coordinatewise F, then so
    is every pp-definable relation

    (conjunction: intersections of F-closed sets are F-closed;
     existential: if (a,w1) and (b,w2) are in an F-closed R, then
     (F(a,b), F(w1,w2)) is too, so the projection is F-closed)

-- and Geiger / Bodnarchuk-Kaluznin-Kotov-Romov supply the converse,
making polymorphisms a complete invariant for pp-definability. This
is the general form of the corpus's own symmetry observation, "f
satisfies t if and only if t satisfies f".

Taking F = intersection:""")
    checks = [
        ("graph of &   (z = x & y)",
         lambda a, b, c: c == (a & b), 3, True),
        ("graph of <<  (z = x << 1)",
         lambda a, b: b == (a << 1), 2, True),
        ("constant     (x = 5)",
         lambda a: a == 5, 1, True),
        ("graph of ^   (z = x ^ y)",
         lambda a, b, c: c == (a ^ b), 3, False),
        ("graph of |   (z = x | y)",
         lambda a, b, c: c == (a | b), 3, False),
    ]
    for label, relation_test, arity, expected in checks:
        preserved = is_preserved_by_intersection(relation_test, arity, 3)
        assert preserved == expected, label
        verdict = "closed" if preserved else "NOT closed"
        print(f"    {label:<28} {verdict}")
    print("""
    witness for ^:  ({0},{0},0) and ({0},0,{0}) are both in the graph,
                    their coordinatewise meet is ({0},0,0), and
                    {0} ^ 0 = {0}, not 0.

    => neither ^ NOR union is pp-definable from {&, <<, constants}.
       Note union is monotone, so this is strictly sharper than
       level 1: pp closure sees more than composition does.
""")


# ---------------------------------------------------------------------
# Level 3 -- first-order closure: negation collapses the basis
# ---------------------------------------------------------------------

def subset_statement(left: Term, right: Term) -> DFA:
    return (left & right).equals(left)


def for_all(statement: DFA, variable_name: str) -> DFA:
    """Universal quantification, as flip-hide-flip."""
    return (~((~statement).exists(variable_name))).minimized()


def union_from_intersection(left: Term, right: Term,
                            result: Term) -> DFA:
    """result = left union right, as the subset-least upper bound --
    written with & and constants only."""
    return (subset_statement(left, result)
            & subset_statement(right, result)
            & for_all(~(subset_statement(left, u)
                        & subset_statement(right, u))
                      | subset_statement(result, u), 'u')).minimized()


def difference_from_intersection(left: Term, right: Term,
                                 result: Term) -> DFA:
    """result = left minus right, as the subset-greatest part of left
    disjoint from right -- written with & and constants only."""
    return (subset_statement(result, left)
            & (result & right).equals(0)
            & for_all(~(subset_statement(u, left)
                        & (u & right).equals(0))
                      | subset_statement(u, result), 'u')).minimized()


def exclusive_or_from_intersection() -> DFA:
    """z = x ^ y  ==  (x minus y) union (y minus x), from & alone."""
    left_part, right_part = Variable('LeftPart'), Variable('RightPart')
    return (difference_from_intersection(x, y, left_part)
            & difference_from_intersection(y, x, right_part)
            & union_from_intersection(left_part, right_part, z)
            ).exists('LeftPart', 'RightPart')


def show_first_order_level() -> None:
    print("=" * 70)
    print("LEVEL 3  FIRST-ORDER CLOSURE -- negation collapses the basis")
    print("=" * 70)
    print("""
Add negation (the flip move) and universal quantification comes with
it. The finite-subset lattice then defines its own relative
complements by subset-extremality, and XOR follows -- using & and
constants only, no shift, no XOR:

    z = x union y      z is a superset of both, and a subset of every
                       common superset
    z = x minus y      z sits inside x, misses y, and contains every
                       such set
    z = x ^ y          the union of the two differences
""")
    derived_union = union_from_intersection(x, y, z)
    assert derived_union.describes_same_relation_as((x | y).equals(z))
    derived_difference = difference_from_intersection(x, y, z)
    assert derived_difference.describes_same_relation_as(
        (x ^ (x & y)).equals(z))
    derived_exclusive_or = exclusive_or_from_intersection()
    assert derived_exclusive_or.describes_same_relation_as(
        (x ^ y).equals(z))
    print(f"    union      derived from {{&, constants}}: verified "
          f"({derived_union.state_count} states)")
    print(f"    difference derived from {{&, constants}}: verified "
          f"({derived_difference.state_count} states)")
    print(f"    XOR        derived from {{&, constants}}: verified "
          f"({derived_exclusive_or.state_count} states)")
    print("""
    => ^ is redundant at the first-order level. The minimal basis of
       the whole canonical layer is  { &, << } + constants.
""")


# ---------------------------------------------------------------------
# Necessity of the two survivors
# ---------------------------------------------------------------------

def show_necessity() -> None:
    print("=" * 70)
    print("NECESSITY -- neither survivor can be dropped")
    print("=" * 70)
    print("""
(a) << is necessary.  Any formula uses finitely many constants; let pi
    permute bit positions above all of them. Bitwise operations
    commute with pi, so the &-graph and those constants are
    pi-invariant, and first-order definitions built from invariant
    relations are invariant. The shift's graph is not invariant:""")
    low_power, high_power = 1 << 5, 1 << 6
    assert 2 * low_power == high_power and 2 * high_power != low_power
    print(f"      (2^5, 2^6) is in the shift graph; its image under "
          f"swapping positions 5 and 6, (2^6, 2^5), is not.")
    print("""      => << is not first-order definable from {&, constants}.

(b) & is necessary.  (finite sets, <<, constants) is a reduct of the
    module GF(2)[t] over itself (0012), and reducts of stable
    structures are stable. But with & present the numeric order is
    definable -- & gives ^ (level 3), ^ with << gives addition, and
    addition gives x <= y as exists gap: x + gap == y -- and an
    infinite linear order is the strict order property, which no
    stable structure has.""")
    order_statement = statement_of_less_or_equal(x, y)
    for left_value, right_value in ((3, 7), (7, 3), (0, 0), (1 << 40,
                                                             1 << 41)):
        assert order_statement.accepts_assignment(
            {'x': left_value, 'y': right_value}) == (
            left_value <= right_value)
    print(f"      x <= y, definable once & is present: "
          f"{order_statement.state_count} canonical states, verified")
    print("""      => & is not first-order definable from {<<, constants}.
""")


def show_summary_table() -> None:
    print("=" * 70)
    print("THE STRUCTURE")
    print("=" * 70)
    print("""
    closure       invariant that governs it        ^ needed?
    ------------------------------------------------------------
    term          monotonicity (Post class M)      yes
    pp            polymorphisms (Geiger, BKKR)     yes, and | too
    first-order   invariance; stability            no

    minimal first-order basis of the canonical layer:
        {  &,  <<  }  + constants          both provably necessary

    What each generator contributes, isolated by its own invariant:
        &   breaks stability   -> order, arithmetic, all nonlinearity
        <<  breaks permutation invariance -> position structure, the
            register, everything sequential

    Read the other way: {&, constants} alone is the permutation
    invariant fragment -- pure set algebra, no arithmetic;
    {<<, constants} alone is stable -- linear, orderless. Each
    generator is exactly the escape from one of those two worlds.
""")


def run_hierarchy() -> None:
    show_term_level()
    show_pp_level()
    show_first_order_level()
    show_necessity()
    show_summary_table()
    print("all closure-hierarchy checks passed")


if __name__ == "__main__":
    run_hierarchy()
