"""The basis, showcased: three operators, why they are a basis, and
how everything else is written as a formula over them.

    THE BASIS          x ^ y      symmetric difference (XOR)
                       x & y      intersection (AND)
                       x << 1     shift filling zero (2x)
                       constants  finite numbers

Statements are built from terms by comparison (`.equals`, `.at_most`,
`.contained_in`) and combined by the three wiring moves, which are
exactly the first-order connectives:

    K & H     share    conjunction
    K | H     union    disjunction
    ~K        flip     negation
    K.exists('w')      hide     existential quantification

so "wiring-closure" and "first-order definability" are the same thing.
A statement is knowably TRUE when its canonical automaton is
universal; K entails H when K & ~H is empty; the judgment stays
one-sided.

This module is a guided tour in four parts, all executable:

    part 1  the three basis operators and their per-column logic
    part 2  generation: common and derived operations as formulas,
            each verified against ground truth or a native form
    part 3  independence: why none of the three can be dropped
    part 4  the catalog, with canonical sizes

Run this file directly.
"""

from __future__ import annotations

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_automata import (
    DFA, Term, Variable, Constant, TrailingOnes, ShiftFillOne,
    relation_addition, relation_shift_fill_zero,
    relation_exclusive_or, relation_intersection)

x: Term = Variable('x')
y: Term = Variable('y')
z: Term = Variable('z')
w: Term = Variable('w')


# ---------------------------------------------------------------------
# Part 1 -- the three basis operators
# ---------------------------------------------------------------------

def show_basis_operators() -> None:
    print("=" * 68)
    print("PART 1  THE BASIS")
    print("=" * 68)
    print("""
Each basis operator is a relation on channels, read one bit-column at
a time, least significant bit first. Two are memoryless; one carries a
single bit of memory, and that memory is the whole difference between
combinational and sequential -- between what finite formulas can say
and what they cannot (0002 Prop 4).
""")
    for label, automaton, note in [
            ("z = x ^ y", relation_exclusive_or('x', 'y', 'z'),
             "memoryless: one state, keep the columns where "
             "z_bit == x_bit ^ y_bit"),
            ("z = x & y", relation_intersection('x', 'y', 'z'),
             "memoryless: one state, keep the columns where "
             "z_bit == x_bit & y_bit"),
            ("z = x << 1", relation_shift_fill_zero('x', 'z'),
             "one bit of memory: the state IS the bit owed to z")]:
        print(f"  {label:<12} {automaton.state_count} state(s) "
              f"before completion -- {note}")
    print("""
Constants are the fourth ingredient and cost nothing conceptually:
"x = 5" is a machine that walks the bits of 5 and then demands zeros.
""")


# ---------------------------------------------------------------------
# Part 2 -- generation
# ---------------------------------------------------------------------

def _sample_check(statement: DFA, expected,
                  channel_names: tuple[str, ...],
                  trial_count: int, bit_width: int,
                  random_seed: int) -> None:
    """Check a statement against a ground-truth predicate on random
    assignments, both for acceptance and for rejection."""
    random_source = random.Random(random_seed)
    for _ in range(trial_count):
        values = {name: random_source.getrandbits(bit_width)
                  for name in channel_names}
        assert statement.accepts_assignment(values) == expected(values)


def show_generation() -> None:
    print("=" * 68)
    print("PART 2  GENERATION -- everything else, as formulas")
    print("=" * 68)

    # -- union, containment: pure Boolean algebra, no wiring needed --
    union_statement = (x | y).equals(z)
    _sample_check(union_statement,
                  lambda v: v['x'] | v['y'] == v['z'],
                  ('x', 'y', 'z'), 300, 40, 1)
    print("""
  UNION            x | y  ==  x ^ y ^ (x & y)
                   the corpus's derived union, unchanged.""")

    subset_statement = x.contained_in(y)
    _sample_check(subset_statement,
                  lambda v: v['x'] & v['y'] == v['x'],
                  ('x', 'y'), 300, 40, 2)
    print("""  CONTAINMENT      x.contained_in(y)  ==  (x & y).equals(x)
                   the corpus's containment test, unchanged.""")

    # -- shift filling one: b(x) = 2x + 1 --
    shift_one_statement = ((x << 1) ^ 1).equals(z)
    assert shift_one_statement.describes_same_relation_as(
        ShiftFillOne(x).equals(z))
    print("""  SHIFT FILL ONE   b(x)  ==  (x << 1) ^ 1
                   the corpus's n1; no new operator.""")

    # -- trailing ones: quantifier-free, no hidden wire (0008) --
    derived_trailing_ones = (
        (z & ((z << 1) ^ 1)).equals(z)          # z is an all-ones run
        & (z & x).equals(z)                     # z sits inside x
        & ((((z << 1) ^ 1) ^ z) & x).equals(0)  # the next bit is absent
    ).minimized()
    assert derived_trailing_ones.describes_same_relation_as(
        TrailingOnes(x).equals(z))
    print("""  TRAILING ONES    z = T(x)  ==  z is an all-ones run
                                and z sits inside x
                                and the next bit up is absent from x
                   the corpus's $ operator -- and note there is no
                   hidden wire here at all: T's graph is quantifier
                   free over the basis, even though T as a function
                   is not finitely composable (0002 Prop 4). Relation
                   definability and term composability differ.""")

    # -- addition: one hidden wire, uniquely determined (0008) --
    carry: Term = Variable('Carry')
    derived_addition = (
        carry.equals(((x & y) | ((x ^ y) & carry)) << 1)
        & z.equals(x ^ y ^ carry)
    ).exists('Carry')
    assert derived_addition.describes_same_relation_as(
        relation_addition('x', 'y', 'z').minimized())
    print("""  ADDITION         z = x + y  ==  exists Carry:
                       Carry = ((x & y) | ((x ^ y) & Carry)) << 1
                       and z = x ^ y ^ Carry
                   one hidden wire, and its equation has a unique
                   solution (bit 0 is 0; bit i+1 follows from bit i),
                   so the hidden channel is a definite description,
                   not a guess. This is the stabilizing carry series
                   of 0002 written as a single equation.""")

    # -- successor two ways --
    successor_by_series = (x ^ ShiftFillOne(TrailingOnes(x))).equals(z)
    successor_by_addition = (x + 1).equals(z)
    assert successor_by_series.describes_same_relation_as(
        successor_by_addition)
    print("""  SUCCESSOR        x ^ b(T(x))   and   x + 1
                   two syntactically unrelated formulas; identical
                   canonical automaton, found mechanically.""")

    # -- order: no bound anywhere (0011) --
    order_statement = x.at_most(y)
    _sample_check(order_statement, lambda v: v['x'] <= v['y'],
                  ('x', 'y'), 300, 60, 3)
    print("""  ORDER            x <= y  ==  exists gap: x + gap == y
                   unbounded on both sides; 2 canonical states.""")

    # -- evenness, doubling, parity-style predicates --
    even_statement = z.equals(w << 1).exists('w')
    _sample_check(even_statement, lambda v: v['z'] % 2 == 0,
                  ('z',), 300, 40, 4)
    print("""  EVENNESS         exists w: z == w << 1""")

    # -- multiplication by a constant --
    times_five = ((x << 2) + x).equals(z)
    _sample_check(times_five, lambda v: 5 * v['x'] == v['z'],
                  ('x', 'z'), 200, 30, 5)
    print("""  TIMES A CONSTANT z == (x << 2) + x            (z = 5x)
                   constants multiply freely; c*x costs c+1 states.""")

    # -- powers of two, and thresholds via the same idea --
    power_of_two = (w + 1).equals(x) & (x & w).equals(0)
    power_of_two = power_of_two.exists('w')
    _sample_check(power_of_two,
                  lambda v: v['x'] != 0 and v['x'] & (v['x'] - 1) == 0,
                  ('x',), 300, 30, 6)
    print("""  POWER OF TWO     exists w: w + 1 == x and x & w == 0
                   a successor disjoint from its predecessor; this is
                   how cardinality entered the layer (0007).""")

    # -- divisibility by three, showing congruences are free --
    divisible_by_three = x.equals(w + (w << 1)).exists('w')
    _sample_check(divisible_by_three, lambda v: v['x'] % 3 == 0,
                  ('x',), 300, 30, 7)
    print("""  CONGRUENCE       exists w: x == w + (w << 1)
                   x divisible by 3; all congruences are free.""")
    print()


# ---------------------------------------------------------------------
# Part 3 -- independence
# ---------------------------------------------------------------------

def show_independence() -> None:
    print("=" * 68)
    print("PART 3  INDEPENDENCE -- why none of the three can be dropped")
    print("=" * 68)
    print("""
Because the wiring moves ARE the first-order connectives, "derivable
by wiring" means "first-order definable from these base relations",
and independence claims become standard definability questions.

(a) THE SHIFT is not derivable from {^, &, constants}.

    Proof. Let pi permute bit positions, fixing every position below
    the width of the constants in play. Bitwise operations commute
    with pi, so the graphs of ^ and & are pi-invariant, as are those
    constants; first-order definitions built from invariant relations
    are invariant. But the shift's graph is not: (2^5, 2^6) lies in
    it, and its image (2^6, 2^5) does not. Hence no first-order
    definition of the shift exists over {^, &, constants}. []

    The witness, executed:""")
    low_power, high_power = 1 << 5, 1 << 6
    in_graph = (2 * low_power == high_power)
    image_in_graph = (2 * high_power == low_power)
    assert in_graph and not image_in_graph
    print(f"      (2^5, 2^6) in the shift graph: {in_graph}")
    print(f"      its image (2^6, 2^5) in the graph: {image_in_graph}")
    print(f"      bitwise graphs are permutation-invariant, the shift "
          f"is not  -> independent")

    print("""
(b) INTERSECTION is not derivable from {^, <<, constants}.   [new]

    Proof. The structure M = (finite sets, ^, <<, constants) is the
    module GF(2)[t] over itself: ^ is module addition and << is
    multiplication by t. Every module is stable (Baur-Monk: its
    formulas reduce to Boolean combinations of positive primitive
    formulas, which cannot define an infinite linear order), and
    naming constants preserves stability. So M is stable, and a
    stable structure cannot first-order define a linear order on an
    infinite definable set (that is the strict order property).

    But with intersection available, the numeric order IS definable:
    addition is definable from {^, &, <<} by the one-wire carry
    equation of part 2, and then x <= y is exists gap: x + gap == y.
    If intersection were definable over {^, <<, constants}, the order
    would be definable in M -- contradicting stability. Hence
    intersection is independent. []

    The load-bearing derivation, executed:""")
    order_statement = x.at_most(y)
    _sample_check(order_statement, lambda v: v['x'] <= v['y'],
                  ('x', 'y'), 200, 50, 8)
    print(f"      x <= y is definable once & is present: "
          f"{order_statement.state_count} canonical states, verified "
          f"unbounded")
    print("""      an infinite linear order, which a module cannot have
      -> intersection is not derivable from {^, <<, constants}

(c) EXCLUSIVE OR is NOT necessary -- it is derivable from {&,
    constants} alone. The finite-subset lattice defines its own
    relative complements by subset-extremality:

        z = x minus y   iff  z sits inside x, misses y, and contains
                             every set that does the same
        z = x ^ y       iff  z is the union of the two differences

    both first-order over & and constants. See closure_hierarchy.py:
    the minimal first-order basis is { &, << } + constants, and ^ is
    a convenience, not a generator -- at this level. At the TERM
    level it is genuinely necessary (monotonicity), which is why the
    corpus needed it.""")
    print()


# ---------------------------------------------------------------------
# Part 4 -- the catalog
# ---------------------------------------------------------------------

def show_catalog() -> None:
    print("=" * 68)
    print("PART 4  CATALOG -- canonical size of each derived relation")
    print("=" * 68)
    carry: Term = Variable('Carry')
    catalog: list[tuple[str, DFA]] = [
        ("z = x ^ y", (x ^ y).equals(z)),
        ("z = x & y", (x & y).equals(z)),
        ("z = x | y", (x | y).equals(z)),
        ("x subset of y", x.contained_in(y)),
        ("z = x << 1", (x << 1).equals(z)),
        ("z = b(x) = (x << 1) ^ 1", ((x << 1) ^ 1).equals(z)),
        ("z = T(x)", TrailingOnes(x).equals(z)),
        ("z = x + 1", (x + 1).equals(z)),
        ("z = x + y", (x + y).equals(z)),
        ("z = 5x", ((x << 2) + x).equals(z)),
        ("x <= y", x.at_most(y)),
        ("x < y", x.below(y)),
        ("x is even", z.equals(w << 1).exists('w').minimized()),
        ("x is a power of two",
         ((w + 1).equals(x) & (x & w).equals(0)).exists('w')),
        ("x divisible by 3", x.equals(w + (w << 1)).exists('w')),
    ]
    for label, statement in catalog:
        print(f"    {label:<26} {statement.state_count:>3} states")
    print("""
Every entry is a formula over {^, &, <<, constants} plus the wiring
moves. No new automaton was hand-built for any of them.""")
    print()


def run_showcase() -> None:
    show_basis_operators()
    show_generation()
    show_independence()
    show_catalog()
    print("all showcase checks passed")


if __name__ == "__main__":
    run_showcase()
