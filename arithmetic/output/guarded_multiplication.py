"""Guarded multiplication inside the canonical-automata layer.

Full multiplication z = x * y is not an automatic relation (0006), so
it cannot enter the canonical layer complete. What CAN enter is the
width-guarded family

    mult_k(x, y, z)  :=  z = x * y  and  y < 2^k

one automaton per guard width k, built by pure wiring from the
existing basis:

    y < 2^k          :=  y & (2^k - 1) = y            (a finite mask)
    selector_i       :=  (y_i = 1 and t_i = a^i(x))
                          or (y_i = 0 and t_i = 0)    (union move)
    mult_k           :=  guard  and  all selectors
                          and  z = t_0 + ... + t_{k-1},
                         with every t_i hidden

Semantics of this guard style (0009 calls it *domain restriction*):
the automaton is COMPLETE about every tuple inside the guard and
REJECTS every tuple outside it -- there is no "unknown" region, so
convexity is fully preserved. The price is that the guard must be
known: using mult_k asserts y < 2^k into K. In bounded games (Clue
hands, finite decks) that assertion is free knowledge, so bounded
games get genuinely convex multiplication with nothing new added to
the logic.

The suite measures the price of widening the guard: canonical state
counts of mult_k as k grows (the shape of the non-automaticity wall),
against the contrast series of multiplication by a fixed constant,
which stays cheap. Run this file directly.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_automata import (
    DFA, Term, Variable, Constant, Intersection, Addition,
    ShiftFillZero, statement_of_equality)


def shifted_left(term: Term, shift_count: int) -> Term:
    for _ in range(shift_count):
        term = ShiftFillZero(term)
    return term


def bit_is_set_statement(variable_name: str, bit_position: int) -> DFA:
    power: int = 1 << bit_position
    return statement_of_equality(
        Intersection(Variable(variable_name), Constant(power)),
        Constant(power))


def bit_is_clear_statement(variable_name: str,
                           bit_position: int) -> DFA:
    return statement_of_equality(
        Intersection(Variable(variable_name),
                     Constant(1 << bit_position)),
        Constant(0))


def below_power_of_two_statement(variable_name: str,
                                 guard_width: int) -> DFA:
    """variable < 2^guard_width, as containment in a finite mask."""
    mask: int = (1 << guard_width) - 1
    return statement_of_equality(
        Intersection(Variable(variable_name), Constant(mask)),
        Variable(variable_name))


def partial_product_statement(multiplicand_name: str,
                              multiplier_name: str,
                              partial_name: str,
                              bit_position: int) -> DFA:
    """partial = multiplicand shifted by bit_position if that bit of
    the multiplier is set, else 0 -- one row of schoolbook
    multiplication, expressed with the union move."""
    row_selected: DFA = bit_is_set_statement(
        multiplier_name, bit_position).intersected_with(
        statement_of_equality(
            Variable(partial_name),
            shifted_left(Variable(multiplicand_name), bit_position)))
    row_skipped: DFA = bit_is_clear_statement(
        multiplier_name, bit_position).intersected_with(
        statement_of_equality(Variable(partial_name), Constant(0)))
    return row_selected.unioned_with(row_skipped).minimized()


def guarded_multiplication(guard_width: int) -> DFA:
    """The canonical automaton for z = x * y with y < 2^guard_width.

    Complete inside the guard, rejecting outside it. Channels during
    construction: x, y, z plus guard_width hidden partial products,
    all projected away at the end."""
    partial_names: list[str] = [
        f"Partial_{bit_position}"
        for bit_position in range(guard_width)]
    combined: DFA = below_power_of_two_statement('y', guard_width)
    for bit_position, partial_name in enumerate(partial_names):
        combined = combined.intersected_with(partial_product_statement(
            'x', 'y', partial_name, bit_position)).minimized()
    total_term: Term = Variable(partial_names[0])
    for partial_name in partial_names[1:]:
        total_term = Addition(total_term, Variable(partial_name))
    combined = combined.intersected_with(
        statement_of_equality(Variable('z'), total_term))
    return combined.existentially_projected(
        set(partial_names)).minimized()


def constant_multiplication(constant: int) -> DFA:
    """The canonical automaton for z = constant * x, as a chain of
    shifted additions -- the contrast series that stays cheap."""
    shift_terms: list[Term] = [
        shifted_left(Variable('x'), bit_position)
        for bit_position in range(constant.bit_length())
        if (constant >> bit_position) & 1]
    total_term: Term = shift_terms[0]
    for shift_term in shift_terms[1:]:
        total_term = Addition(total_term, shift_term)
    return statement_of_equality(Variable('z'), total_term)


# ---------------------------------------------------------------------
# Verification suite
# ---------------------------------------------------------------------

def run_verification_suite() -> None:
    # Completeness inside the guard, rejection outside it, exhaustively
    for guard_width in (1, 2, 3):
        automaton: DFA = guarded_multiplication(guard_width)
        for multiplicand in range(64):
            for multiplier in range(1 << guard_width):
                product = multiplicand * multiplier
                assert automaton.accepts_assignment(
                    {'x': multiplicand, 'y': multiplier, 'z': product})
                assert not automaton.accepts_assignment(
                    {'x': multiplicand, 'y': multiplier,
                     'z': product + 1})
                if multiplicand > 1 and multiplier > 0:
                    assert not automaton.accepts_assignment(
                        {'x': multiplicand, 'y': multiplier,
                         'z': product + multiplicand * 2})
            # outside the guard: rejected, even with the true product
            outside_multiplier = 1 << guard_width
            assert not automaton.accepts_assignment(
                {'x': multiplicand, 'y': outside_multiplier,
                 'z': multiplicand * outside_multiplier})
        print(f"mult_{guard_width} (y < {1 << guard_width}): complete "
              f"inside guard, rejects outside, exhaustive x < 64  OK   "
              f"[{automaton.state_count} canonical states]")

    # The shape of the wall: canonical sizes as the guard widens,
    # against constant multiplication which stays cheap
    print("guard-width curve (the wall, measured):")
    for guard_width in (1, 2, 3, 4):
        automaton = guarded_multiplication(guard_width)
        print(f"    mult_{guard_width}: y < {1 << guard_width:3d}  ->  "
              f"{automaton.state_count} canonical states")
    print("constant-multiplication contrast (stays cheap):")
    import random
    random_source = random.Random(20260805)
    for constant in (3, 5, 7, 11, 13, 21, 43):
        automaton = constant_multiplication(constant)
        for _ in range(200):
            sample = random_source.randrange(1 << 24)
            assert automaton.accepts_assignment(
                {'x': sample, 'z': constant * sample})
            assert not automaton.accepts_assignment(
                {'x': sample, 'z': constant * sample + 1})
        print(f"    z = {constant:2d}x  ->  "
              f"{automaton.state_count} canonical states")

    print("all checks passed")


if __name__ == "__main__":
    run_verification_suite()
