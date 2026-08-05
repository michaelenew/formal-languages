"""Addition under semantic convexity, on numbers-as-bitsets.

Encoding: a finite set S of naturals is the number n(S) = sum(2^i for
i in S). The empty set is 0. Python ints are the representation;
bitwise operators are the set operators (^ = symmetric difference /
XOR, & = intersection / AND).

Primitive operators of the syntax:
    shift_left_filling_zero(x) = 2x       (the corpus's n0/inc; 0002's a)
    shift_left_filling_one(x)  = 2x + 1   (the corpus's n1; 0002's b)

Everything below is built from {^, &, the two shifts, finite constants}
plus one syntax-level construct: the *stabilizing series* -- an iterated
monotone sequence in the lattice of subsets whose termination is
syntactically evident (a strictly decreasing/increasing chain of finite
sets, with an a-priori bound given by the max element or popcount of
the inputs).

Constructions (numbered as in exploration/0002):
    trailing_ones_mask       Prop 2: the stabilizing intersection
                             x & b(x) & b(b(x)) & ...   (the corpus's $)
    successor                Prop 3: x ^ b(T(x))
    add_by_carry_recursion   Prop 5: (x^y, a(x&y)) iterated; measure =
                             popcount sum
    add_by_least_fixpoint    Prop 6: Kleene carry-lookahead fixpoint
    add_by_doubling_limit    the Kogge-Stone form of
                             clue/2026-06-21 AI exploration.md

Each function asserts its own termination measure as it runs, so a
passing test run is also a check of the convexity bounds, not just of
the answers.  Run this file directly for the verification suite.
"""

from __future__ import annotations


class SeriesResult:
    """A stabilizing series' limit plus the number of terms consumed
    before the first plateau."""

    def __init__(self, limit: int, series_terms_consumed: int) -> None:
        self.limit: int = limit
        self.series_terms_consumed: int = series_terms_consumed


class AdditionResult:
    """A computed sum plus the number of iteration steps taken."""

    def __init__(self, total: int, steps_taken: int) -> None:
        self.total: int = total
        self.steps_taken: int = steps_taken


def shift_left_filling_zero(value: int) -> int:
    """n -> 2n. On sets: {i} -> {i+1}."""
    return value << 1


def shift_left_filling_one(value: int) -> int:
    """n -> 2n + 1. On sets: S -> {0} union {i+1 for i in S}."""
    return (value << 1) | 1


def trailing_ones_mask(value: int) -> SeriesResult:
    """T(x) = x & b(x) & b(b(x)) & ...  (Prop 2).

    Lemma 2b: the first plateau IS the limit (the count of non-trailing
    survivors strictly decreases until it hits 0), so the stopping rule
    needs no cleverness. Lemma 2c: the series stabilizes within
    max_bit(x) + 1 terms -- an a-priori syntactic bound, asserted here.
    """
    stabilization_bound: int = value.bit_length() + 1
    previous_intersection: int = value
    series_term: int = value
    terms_consumed: int = 0
    while True:
        series_term = shift_left_filling_one(series_term)
        current_intersection: int = previous_intersection & series_term
        terms_consumed += 1
        assert terms_consumed <= stabilization_bound, \
            "stabilization bound violated (Lemma 2c)"
        if current_intersection == previous_intersection:
            return SeriesResult(current_intersection, terms_consumed)
        previous_intersection = current_intersection


def successor(value: int) -> int:
    """value + 1 = value ^ b(T(value))  (Prop 3)."""
    mask: SeriesResult = trailing_ones_mask(value)
    return value ^ shift_left_filling_one(mask.limit)


def add_by_carry_recursion(left_addend: int,
                           right_addend: int) -> AdditionResult:
    """left + right by the carry recursion  (Prop 5).

    step: (x, y) -> (x ^ y, a(x & y)) until the carry is empty.
    Measure: popcount(x) + popcount(y) strictly decreases while the
    carry is nonempty, so the loop runs at most that many steps. The
    measure is asserted on every step.
    """
    steps_taken: int = 0
    while left_addend & right_addend:
        popcount_measure: int = (left_addend.bit_count()
                                 + right_addend.bit_count())
        left_addend, right_addend = (
            left_addend ^ right_addend,
            shift_left_filling_zero(left_addend & right_addend))
        steps_taken += 1
        assert (left_addend.bit_count() + right_addend.bit_count()
                < popcount_measure), \
            "popcount measure failed to decrease (Prop 5)"
    return AdditionResult(left_addend ^ right_addend, steps_taken)


def add_by_least_fixpoint(left_addend: int,
                          right_addend: int) -> AdditionResult:
    """left + right via the carry-lookahead least fixpoint  (Prop 6).

    carry = least fixpoint of F(C) = a(g or (p & C)), with
    g = x & y (generate), p = x ^ y (propagate);  x + y = p ^ carry.
    F is monotone and the chain starts at 0, so the Kleene chain is
    increasing and its first repeat is the least fixpoint -- the same
    stabilizing-series shape as trailing_ones_mask, in the increasing
    direction. (The union stays inside the algebra:
    u or v = u ^ v ^ (u & v).)
    """
    generate_set: int = left_addend & right_addend
    propagate_set: int = left_addend ^ right_addend
    carry_set: int = 0
    iterations: int = 0
    iteration_bound: int = max(left_addend.bit_length(),
                               right_addend.bit_length()) + 2
    while True:
        next_carry_set: int = shift_left_filling_zero(
            generate_set | (propagate_set & carry_set))
        iterations += 1
        assert iterations <= iteration_bound, \
            "least-fixpoint iteration bound violated"
        if next_carry_set == carry_set:
            return AdditionResult(propagate_set ^ carry_set, iterations)
        assert next_carry_set & carry_set == carry_set, \
            "Kleene chain not increasing"
        carry_set = next_carry_set


def add_by_doubling_limit(left_addend: int,
                          right_addend: int) -> AdditionResult:
    """left + right via the doubling-limit (Kogge-Stone) form from
    clue/2026-06-21 AI exploration.md:

        G_0 = x & y,  P_0 = x ^ y
        G_{s+1} = G_s ^ (P_s & Shift_s(G_s))
        P_{s+1} = P_s & Shift_s(P_s)
        x + y = x ^ y ^ a(limit of G)      (Shift_s = shift by 2^s)

    Note it uses only ^ and & -- the XOR stands in for OR because the
    two terms are disjoint (a block cannot both generate and fully
    propagate); asserted below. Termination: the propagate set strictly
    shrinks while nonzero and is extinguished once the shift distance
    exceeds the bit width, so ~log2(width) steps; the generate set is
    increasing and stabilizes once propagation stops.
    """
    generate_set: int = left_addend & right_addend
    propagate_set: int = left_addend ^ right_addend
    shift_distance: int = 1
    steps_taken: int = 0
    step_bound: int = max(left_addend.bit_length(),
                          right_addend.bit_length(),
                          1).bit_length() + 2
    while propagate_set:
        assert generate_set & propagate_set == 0, \
            "generate/propagate not disjoint"
        carried_generate: int = propagate_set & (
            generate_set << shift_distance)
        assert generate_set & carried_generate == 0, \
            "XOR-for-OR disjointness violated"
        generate_set = generate_set ^ carried_generate
        propagate_set = propagate_set & (
            propagate_set << shift_distance)
        shift_distance <<= 1
        steps_taken += 1
        assert steps_taken <= step_bound, "log-step bound violated"
    return AdditionResult(
        left_addend ^ right_addend
        ^ shift_left_filling_zero(generate_set),
        steps_taken)


def add_constant_by_iterated_successor(value: int,
                                       constant: int) -> int:
    """The constant-offset family n -> n + constant, as iterated
    successor."""
    for _ in range(constant):
        value = successor(value)
    return value


def sum_is_knowably(left_addend: int, right_addend: int,
                    hypothesized_total: int) -> bool:
    """The convexity test for the hypothesis
    'left + right = hypothesized_total'.

    The hypothesis term is add(left, right) ^ hypothesized_total; it
    reduces to the empty set (0, i.e. TRUE) iff the hypothesis holds.
    One-sided judgment: the result is 'reduced to 0' or 'did not' --
    never 'false'.
    """
    addition: AdditionResult = add_by_carry_recursion(left_addend,
                                                      right_addend)
    return addition.total ^ hypothesized_total == 0


# ---------------------------------------------------------------------
# Verification suite
# ---------------------------------------------------------------------

def run_verification_suite(random_seed: int = 20260804) -> None:
    import random
    random_source = random.Random(random_seed)

    # Prop 2: T(x) against the closed-form oracle 2^t - 1
    for value in range(1 << 14):
        series: SeriesResult = trailing_ones_mask(value)
        assert series.limit == ((~value & (value + 1)) - 1), \
            f"trailing_ones_mask failed at {value}"
    print("Prop 2  trailing_ones_mask: exhaustive 0..2^14  OK")

    # Prop 3: successor exhaustive + large random
    for value in range(1 << 14):
        assert successor(value) == value + 1, \
            f"successor failed at {value}"
    for _ in range(500):
        value = random_source.getrandbits(256)
        assert successor(value) == value + 1
    print("Prop 3  successor: exhaustive 0..2^14 + 500 random "
          "256-bit  OK")

    # Prop 5: carry recursion exhaustive small, random large; step bound
    for left_value in range(256):
        for right_value in range(256):
            addition: AdditionResult = add_by_carry_recursion(
                left_value, right_value)
            assert addition.total == left_value + right_value
            assert addition.steps_taken <= (left_value.bit_count()
                                            + right_value.bit_count())
    for _ in range(500):
        left_value = random_source.getrandbits(512)
        right_value = random_source.getrandbits(512)
        addition = add_by_carry_recursion(left_value, right_value)
        assert addition.total == left_value + right_value
        assert addition.steps_taken <= (left_value.bit_count()
                                        + right_value.bit_count())
    print("Prop 5  add_by_carry_recursion: exhaustive 256x256 + 500 "
          "random 512-bit, steps <= popcount bound  OK")

    # Least-fixpoint variant agrees
    for _ in range(500):
        left_value = random_source.getrandbits(512)
        right_value = random_source.getrandbits(512)
        addition = add_by_least_fixpoint(left_value, right_value)
        assert addition.total == left_value + right_value
    print("        add_by_least_fixpoint: 500 random 512-bit  OK")

    # Doubling-limit (Kogge-Stone) form from clue/2026-06-21
    for left_value in range(256):
        for right_value in range(256):
            addition = add_by_doubling_limit(left_value, right_value)
            assert addition.total == left_value + right_value
    for _ in range(500):
        left_value = random_source.getrandbits(512)
        right_value = random_source.getrandbits(512)
        addition = add_by_doubling_limit(left_value, right_value)
        assert addition.total == left_value + right_value
    print("        add_by_doubling_limit (XOR-for-OR disjointness "
          "asserted): exhaustive 256x256 + 500 random 512-bit  OK")

    # Constant-offset family
    for value in range(1000):
        for constant in (1, 2, 3, 7):
            assert (add_constant_by_iterated_successor(value, constant)
                    == value + constant)
    print("        constant-offset family (+1,+2,+3,+7): 0..1000  OK")

    # Prop 4 witness (locality): bit k of the successor depends on bit 0
    witness_bit_position: int = 96
    all_ones_value: int = (1 << witness_bit_position) - 1
    all_ones_but_lowest: int = all_ones_value - 1
    assert ((successor(all_ones_value) >> witness_bit_position) & 1
            != (successor(all_ones_but_lowest)
                >> witness_bit_position) & 1)
    print("Prop 4  locality witness: bit 96 of successor flips with "
          "bit 0  OK")

    # Deduction test H ^ HK shape on arithmetic hypotheses
    assert sum_is_knowably(1337, 4958, 6295)
    assert not sum_is_knowably(1337, 4958, 6296)
    print("        sum_is_knowably one-sided test  OK")

    print("all checks passed")


if __name__ == "__main__":
    run_verification_suite()
