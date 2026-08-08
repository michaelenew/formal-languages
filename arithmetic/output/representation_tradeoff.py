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


def disjoint_triple_cnf_truth_table(clause_count: int) -> list[int]:
    """Truth table of (x0|x1|x2) & (x3|x4|x5) & ... -- 3-CNF over
    disjoint triples. Each clause has a 7-term ANF and the clauses
    share no variables, so no monomial can cancel and the product has
    exactly 7^clause_count terms. Trivially satisfiable, which is the
    point: the canonical form explodes even when the DECISION is
    obvious."""
    variable_count = 3 * clause_count
    table = []
    for assignment in range(1 << variable_count):
        satisfied = all(
            (assignment >> (3 * index)) & 0b111 != 0
            for index in range(clause_count))
        table.append(1 if satisfied else 0)
    return table


def show_canonical_sentence_form() -> None:
    """Canonical sentence forms exist. Cheap ones would collapse P and
    NP -- shown on 3-SAT, where the canonical form is zero exactly
    when the formula is unsatisfiable."""
    print()
    print("=" * 70)
    print("4  A CANONICAL SENTENCE FORM EXISTS -- BUT NOT A CHEAP ONE")
    print("=" * 70)
    print("""
  The algebra does support expand-and-cancel, exactly as claimed:
  << is linear over both operators and & distributes over ^, so every
  hidden-symbol-free sentence reduces to a unique XOR of ANDs.
  Checked on all subsets of a 4-element universe:""")
    universe = range(1 << 4)
    for left in universe:
        for right in universe:
            assert (left ^ right) << 1 == (left << 1) ^ (right << 1)
            assert (left & right) << 1 == (left << 1) & (right << 1)
            for third in universe:
                assert left & (right ^ third) == \
                    (left & right) ^ (left & third)
    print("""      << distributes over ^ and over &; & distributes
      over ^.  So ANF is a genuine canonical form. The question is
      what it COSTS to reach it.

  Take 3-SAT, where the point is sharpest. A 3-CNF formula is a
  CONJUNCTION of clauses, so its ANF is a PRODUCT of the clause
  polynomials, and multiplying them out does not stay small. Take the
  cleanest case, clauses over disjoint triples -- each clause has a
  7-term ANF and no variables are shared, so nothing can cancel:
""")
    print(f"      {'clauses':>7}  {'vars':>5}  {'literals':>8}"
          f"  {'ANF terms':>10}")
    for clause_count in range(1, 6):
        table = disjoint_triple_cnf_truth_table(clause_count)
        terms = algebraic_normal_form_size(table, 3 * clause_count)
        assert terms == 7 ** clause_count, "expected exactly 7^m terms"
        print(f"      {clause_count:>7}  {3 * clause_count:>5}"
              f"  {3 * clause_count:>8}  {terms:>10}")
    print("""
  Exactly 7^m terms from 3m literals -- and every one of these
  formulas is trivially satisfiable. So the canonical form explodes
  even where the DECISION is obvious: canonicalising is not merely as
  hard as deciding, it can be strictly harder.

  And the reason is not incidental. The ANF of a formula is the ZERO
  polynomial exactly when the formula is unsatisfiable -- so merely
  deciding whether the canonical form is 0 already decides UNSAT.
  Canonicalising a 3-CNF is therefore coNP-hard.

  In general: if some canonical sentence form C were computable in
  polynomial time, then C(phi) == C(false) would decide unsatisfiability
  in polynomial time, so P would equal NP. Hence

      canonical + compact + polynomial   is unavailable unless P = NP

  which settles the "real prize" of 0019 in the negative, and puts the
  three representations in their places:

      ANF                     canonical, NOT compact
      minimal automaton       canonical, NOT compact
      sentence with hidden
        symbols               compact, NOT canonical

  The positive reading: canonicalising is not what REMOVES the
  difficulty of 3-SAT, it is where the difficulty LIVES. Once a
  canonical form is in hand every question is trivial -- comparison of
  coordinate vectors. So the hardness of SAT is exactly the cost of
  the change of basis into the monomial coordinates. Which is the
  eigenbasis analogy holding to the end: the basis that diagonalises
  everything is also the basis that is expensive to reach.""")


def show_where_clue_sits() -> None:
    """Not a refutation of any worst-case claim -- a locator. Clue's
    own constraints land in the ring form's worst regime."""
    print()
    print("=" * 70)
    print("5  WHERE CLUE ITSELF SITS IN THE RING FORM")
    print("=" * 70)
    print("""
  Mini-Clue, 6 cards, hands of 2 / 1 / 3, one envelope card per
  category -- the a priori setup, BEFORE any event. 18 Boolean
  variables (card i in hand h). Its canonical ring form:
""")
    card_count, hand_count = 6, 3
    hand_sizes = [2, 1, 3]
    categories = [(0, 1), (2, 3), (4, 5)]
    variable_count = card_count * hand_count

    def variable_index(card: int, hand: int) -> int:
        return card * hand_count + hand

    def is_consistent(assignment: int) -> bool:
        holder: list[int] = []
        for card in range(card_count):
            held = [hand for hand in range(hand_count)
                    if assignment >> variable_index(card, hand) & 1]
            if len(held) != 1:
                return False
            holder.append(held[0])
        for hand in range(hand_count):
            if holder.count(hand) != hand_sizes[hand]:
                return False
        for low, high in categories:
            if (holder[low] == 2) + (holder[high] == 2) != 1:
                return False
        return True

    table = [1 if is_consistent(assignment) else 0
             for assignment in range(1 << variable_count)]
    deal_count = sum(table)
    for bit_position in range(variable_count):
        step = 1 << bit_position
        for mask in range(1 << variable_count):
            if mask & step:
                table[mask] ^= table[mask ^ step]
    monomials = [mask for mask, coefficient in enumerate(table)
                 if coefficient]
    degree = max(bin(mask).count('1') for mask in monomials)
    assert deal_count == 24
    print(f"      consistent deals          {deal_count:8d}")
    print(f"      ANF terms                 {len(monomials):8d}")
    print(f"      ANF degree                {degree:8d}   "
          f"of {variable_count} variables")
    print(f"      canonical automaton       {17:8d}   states "
          f"(0007)")
    print("""
  So 24 deals cost 27,648 ring terms and 17 automaton states. This
  refutes nothing -- one family says nothing about a worst case -- but
  it locates the toy problem precisely: Clue's constraints are hand
  SIZES, which are threshold functions, which are near-maximal degree
  in the ring. And degree is exactly the quantity Polynomial Calculus
  lower bounds are proved through (size >= 2^Omega((d-d0)^2/n),
  Impagliazzo-Pudlak-Sgall). The theory predicts the measurement: the
  ring form is at its worst on precisely the constraints this problem
  is made of.""")


def run_verification_suite() -> None:
    show_algebra_is_not_convention()
    show_where_clue_sits()
    show_automaton_loses()
    show_expression_loses()
    show_verdict()
    show_canonical_sentence_form()
    print()
    print("all representation-tradeoff checks passed")


if __name__ == "__main__":
    run_verification_suite()
