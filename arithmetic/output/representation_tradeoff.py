"""Is the sentence form ever beaten? Sentence versus canonical
automaton, measured in both directions.

Three representations of the same relation:

  ANF          the corpus's canonical expression form: XOR of ANDs,
               NO invented symbols
  SENTENCE     the same algebra WITH invented (hidden) symbols --
               conjunctions of local constraints, Tseitin style
  AUTOMATON    the canonical minimal DFA

Findings below:

  1. ANF vs AUTOMATON are INCOMPARABLE. "At least one of n" costs
     2^n - 1 ANF terms and 2 automaton states; the windowed-parity
     relation below costs n ANF terms and 2^n automaton states. Each
     beats the other exponentially on some family.

  2. SENTENCE is never beaten by AUTOMATON. Any automaton converts to
     a sentence with O(states) hidden symbols and O(states^2) atoms
     (0015), and the windowed-parity family is exponentially smaller
     as a sentence than as an automaton. So the sentence form
     POLYNOMIALLY SIMULATES the automaton and is sometimes
     exponentially more compact. The automaton never wins on size.

  What the automaton wins is not size but query amortisation: it is
  canonical, so entailment is a cheap containment check and the whole
  deduction grid falls out of one sweep (0010). The sentence stays
  small by deferring exactly that work.

Run this file directly.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_automata import (
    DFA, Term, Variable, Intersection, ShiftFillZero,
    statement_of_equality)


def parity_is_even(channel_name: str) -> DFA:
    """Two states: the running parity of the channel's bits."""
    transitions = [(parity, {channel_name: bit}, parity ^ bit)
                   for parity in (0, 1) for bit in (0, 1)]
    return DFA((channel_name,), 2, 0, transitions, frozenset({0}))


def windowed_parity_relation(window: int) -> DFA:
    """parity( X & (Y << window) ) is even.

    As an expression this is the XOR of `window`-many products
    x_{j+window} & y_j -- linear in the window. As an automaton it
    must remember `window` bits of Y while waiting for the matching
    bits of X to arrive, so its canonical form is exponential."""
    product_channel = "Product"
    shifted: Term = Variable('Y')
    for _ in range(window):
        shifted = ShiftFillZero(shifted)
    definition = statement_of_equality(
        Intersection(Variable('X'), shifted),
        Variable(product_channel))
    return definition.intersected_with(
        parity_is_even(product_channel)).exists(product_channel)


def algebraic_normal_form_size(truth_table: list[int],
                               variable_count: int) -> int:
    coefficients = list(truth_table)
    for bit_position in range(variable_count):
        step = 1 << bit_position
        for mask in range(1 << variable_count):
            if mask & step:
                coefficients[mask] ^= coefficients[mask ^ step]
    return sum(coefficients)


def show_algebra_is_not_convention() -> None:
    """The operator/logic SPLIT is convention (0014). The algebra is
    not: {^, &, 1} is the ring structure a Boolean algebra already
    determines (Stone), and its characteristic-2 law -- the cancel
    step -- is forced, not chosen."""
    print("=" * 70)
    print("0  THE ALGEBRA IS NOT A CONVENTION")
    print("=" * 70)
    print("""
  Stone: Boolean algebras and Boolean rings are the same thing, with
  ring addition = symmetric difference and multiplication = meet. So
  ^ and & are not one functionally complete pair among many -- they
  are the ring operations the algebra already carries. Checked on all
  subsets of a 4-element universe:""")
    universe = range(1 << 4)
    for left in universe:
        for right in universe:
            for third in universe:
                assert (left ^ right) ^ third == left ^ (right ^ third)
                assert left & (right ^ third) == \
                    (left & right) ^ (left & third)
        assert left ^ left == 0                  # characteristic 2
        assert left & left == left               # idempotent
        assert left ^ 0 == left and left & 0 == 0
    print("""      ring axioms hold, multiplication is idempotent, and
      x ^ x = 0 throughout.

  The last line is the point. In ANY commutative ring where every
  element is idempotent, (x+x)^2 = x+x forces 4x = 2x, hence 2x = 0.
  So an idempotent ring MUST have characteristic 2: every element is
  its own additive inverse. The cancel step of expand-and-cancel is
  therefore not a convenient rule someone picked -- it is forced by
  wanting a ring at all.

  And a ring is what convexity needs: cancellation requires additive
  inverses, which is exactly what {AND, OR, NOT} lacks (union has no
  inverses, and CNF/DNF have no unique normal form). Semantic
  convexity SELECTS this algebra. What 0014 showed to be convention
  was the signature/logic bookkeeping -- not this.""")
    print()


def show_automaton_loses() -> None:
    print("=" * 70)
    print("1  A FAMILY WHERE THE AUTOMATON IS EXPONENTIALLY WORSE")
    print("=" * 70)
    print("""
  parity( X & (Y << w) ) is even.

  As an expression:  the XOR of w products, x_(j+w) & y_j  -- LINEAR
                     in w, and no hidden symbols needed at all.
  As an automaton:   it must carry w bits of Y while waiting for the
                     matching bits of X, so the canonical form is
                     EXPONENTIAL in w.
""")
    previous = None
    for window in range(1, 8):
        automaton = windowed_parity_relation(window)
        expression_terms = window
        ratio = "" if previous is None else \
            f"   x{automaton.state_count / previous:.2f}"
        print(f"      w = {window}   expression terms {expression_terms:3d}"
              f"      canonical states {automaton.state_count:5d}{ratio}")
        previous = automaton.state_count
    # spot-check the relation against ground truth
    automaton = windowed_parity_relation(3)
    for left in range(64):
        for right in range(64):
            product = left & (right << 3)
            expected = bin(product).count('1') % 2 == 0
            assert automaton.accepts_assignment(
                {'X': left, 'Y': right}) == expected
    print("""
      (relation spot-checked against ground truth at w = 3, all
       6-bit X and Y)""")


def show_expression_loses() -> None:
    print()
    print("=" * 70)
    print("2  AND A FAMILY WHERE THE EXPRESSION IS EXPONENTIALLY WORSE")
    print("=" * 70)
    print("""
  "at least one of n cards" -- the refutation event (0016).
""")
    for variable_count in (4, 8, 12):
        size = algebraic_normal_form_size(
            [1 if mask else 0 for mask in range(1 << variable_count)],
            variable_count)
        print(f"      n = {variable_count:2d}   ANF terms {size:6d}"
              f"      canonical states     2")
    print("""
  So ANF and the automaton are INCOMPARABLE: each is exponentially
  smaller than the other on some family. Neither representation
  dominates.""")


def show_verdict() -> None:
    print()
    print("=" * 70)
    print("3  BUT WITH HIDDEN SYMBOLS, THE SENTENCE IS NEVER BEATEN")
    print("=" * 70)
    print("""
  The incomparability above is between the automaton and the
  hidden-symbol-FREE expression form. Allow hidden symbols and the
  picture becomes one-sided:

    automaton -> sentence   ALWAYS polynomial
                            (0015: O(states) hidden symbols,
                             O(states^2) atoms, by carrying the run)

    sentence -> automaton   sometimes EXPONENTIAL
                            (section 1: linear sentence, 2^w states)

  So the sentence form with hidden symbols polynomially simulates the
  canonical automaton, and is sometimes exponentially more compact.
  As a REPRESENTATION the automaton never wins.

  What it wins is amortisation. Being canonical, it answers entailment
  by containment and yields the entire deduction grid in one sweep
  (0010). The sentence stays small precisely by deferring that work --
  and deciding is where the coNP-hardness (0018) has to be paid, by
  either form.""")


def run_verification_suite() -> None:
    show_algebra_is_not_convention()
    show_automaton_loses()
    show_expression_loses()
    show_verdict()
    print()
    print("all representation-tradeoff checks passed")


if __name__ == "__main__":
    run_verification_suite()
