"""Mini-Clue solved end-to-end on the canonical-automata layer,
hand sizes included -- the K workflow.

Deck (6 cards, one bit each):
    mustard=1, plum=2  (suspects)   knife=4, pipe=8   (weapons)
    hall=16, study=32  (rooms)      FULL_DECK = 63

Players: Alice (hand A, 2 cards), Bob (hand B, 1 card), envelope E
(one card of each category; its size 3 is NOT asserted -- the workflow
derives it).

Knowledge is ONE canonical automaton over tracks (A, B, E): the
relation of all deals consistent with everything known.
  - update:      knowledge := knowledge intersected with the new
                 fact's automaton, reminimized
  - deduction:   knowledge entails hypothesis iff
                 knowledge & ~hypothesis is empty  (one-sided)
Polarity per 0006: knowledge shrinks as it grows in content;
TRUE = containment.

Hand sizes live INSIDE the term language -- no cardinality primitive:
  power_of_two(y)    :=  exists w:  w + 1 = y  and  y & w = 0
                         (a successor disjoint from its predecessor is
                          exactly a power of two; y = 0 is impossible
                          as a successor)
  hand has k cards   :=  exists k pairwise-disjoint powers of two
                         XORing to the hand
This is the counting story of 0001 section 4 realized: sizes enter
through addition and projection, never through a non-regular counting
operator.

Every stage is cross-validated against a brute-force enumeration of
all 64^3 = 262,144 deals. Run this file directly.
"""

from __future__ import annotations

import os
import sys
from typing import Callable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_automata import (
    DFA, Term, Variable, Constant, ExclusiveOr, Intersection, Addition,
    statement_of_equality)

MUSTARD, PLUM, KNIFE, PIPE, HALL, STUDY = 1, 2, 4, 8, 16, 32
FULL_DECK: int = 63
SUSPECT_CARDS: int = MUSTARD | PLUM
WEAPON_CARDS: int = KNIFE | PIPE
ROOM_CARDS: int = HALL | STUDY
CARD_NAMES: dict[int, str] = {
    MUSTARD: "mustard", PLUM: "plum", KNIFE: "knife",
    PIPE: "pipe", HALL: "hall", STUDY: "study"}

DealPredicate = Callable[[int, int, int], bool]


def conjunction_of(*statements: DFA) -> DFA:
    combined: DFA = statements[0]
    for statement in statements[1:]:
        combined = combined.intersected_with(statement)
    return combined.minimized()


def power_of_two_statement(term: Term, witness_tag: str) -> DFA:
    """power_of_two(term): exists w. w + 1 = term and term & w = 0."""
    witness_name: str = f"Witness_{witness_tag}"
    witness: Term = Variable(witness_name)
    combined: DFA = conjunction_of(
        statement_of_equality(Addition(witness, Constant(1)), term),
        statement_of_equality(Intersection(term, witness), Constant(0)))
    return combined.existentially_projected({witness_name}).minimized()


def hand_size_statement(hand_variable_name: str, card_count: int,
                        witness_tag: str) -> DFA:
    """The hand holds exactly card_count cards, via that many pairwise
    disjoint power-of-two witnesses XORing to the hand."""
    witness_names: list[str] = [
        f"Part_{witness_tag}_{witness_index}"
        for witness_index in range(card_count)]
    constraints: list[DFA] = [
        power_of_two_statement(Variable(witness_name),
                               f"{witness_tag}_{witness_index}")
        for witness_index, witness_name in enumerate(witness_names)]
    for first_index in range(card_count):
        for second_index in range(first_index + 1, card_count):
            constraints.append(statement_of_equality(
                Intersection(Variable(witness_names[first_index]),
                             Variable(witness_names[second_index])),
                Constant(0)))
    combined_witnesses: Term = Variable(witness_names[0])
    for witness_name in witness_names[1:]:
        combined_witnesses = ExclusiveOr(combined_witnesses,
                                         Variable(witness_name))
    constraints.append(statement_of_equality(
        combined_witnesses, Variable(hand_variable_name)))
    return conjunction_of(*constraints).existentially_projected(
        set(witness_names)).minimized()


def holds_card_statement(hand_variable_name: str, card: int) -> DFA:
    return statement_of_equality(
        Intersection(Variable(hand_variable_name), Constant(card)),
        Constant(card))


def lacks_cards_statement(hand_variable_name: str, cards: int) -> DFA:
    return statement_of_equality(
        Intersection(Variable(hand_variable_name), Constant(cards)),
        Constant(0))


def hand_is_exactly_statement(hand_variable_name: str,
                              cards: int) -> DFA:
    return statement_of_equality(Variable(hand_variable_name),
                                 Constant(cards))


def consistent_deals(knowledge: DFA) -> list[tuple[int, int, int]]:
    """Brute-force: which of the 64^3 deals does knowledge accept?"""
    accepted_deals: list[tuple[int, int, int]] = []
    for alice_hand in range(64):
        for bob_hand in range(64):
            for envelope_hand in range(64):
                if knowledge.accepts_assignment(
                        {'A': alice_hand, 'B': bob_hand,
                         'E': envelope_hand}):
                    accepted_deals.append(
                        (alice_hand, bob_hand, envelope_hand))
    return accepted_deals


def deals_satisfying(
        predicate: DealPredicate) -> list[tuple[int, int, int]]:
    return [(alice_hand, bob_hand, envelope_hand)
            for alice_hand in range(64)
            for bob_hand in range(64)
            for envelope_hand in range(64)
            if predicate(alice_hand, bob_hand, envelope_hand)]


def report_stage(knowledge: DFA, label: str,
                 predicate: DealPredicate) -> list[tuple[int, int, int]]:
    accepted_deals = consistent_deals(knowledge)
    expected_deals = deals_satisfying(predicate)
    assert accepted_deals == expected_deals, \
        f"{label}: automaton disagrees with brute force"
    print(f"{label}: canonical {knowledge.state_count} states, "
          f"{len(accepted_deals)} consistent deals "
          f"(brute-force match)")
    return accepted_deals


def print_judgment(knowledge: DFA, hypothesis: DFA,
                   description: str) -> None:
    """One-sided judgment on a single hypothesis."""
    verdict: str = ("KNOWN TRUE" if knowledge.entails(hypothesis)
                    else "unknown")
    print(f"    {description}: {verdict}")


def count_of_set_bits(value: int) -> int:
    return value.bit_count()


def format_hand(hand: int) -> str:
    return "{" + ", ".join(name for card, name in CARD_NAMES.items()
                           if hand & card) + "}"


def run_workflow() -> None:
    # ---- K0: the a-priori knowledge ---------------------------------
    partition_statement: DFA = conjunction_of(
        statement_of_equality(
            ExclusiveOr(Variable('A'),
                        ExclusiveOr(Variable('B'), Variable('E'))),
            Constant(FULL_DECK)),
        statement_of_equality(
            Intersection(Variable('A'), Variable('B')), Constant(0)),
        statement_of_equality(
            Intersection(Variable('A'), Variable('E')), Constant(0)),
        statement_of_equality(
            Intersection(Variable('B'), Variable('E')), Constant(0)))
    size_statements: DFA = conjunction_of(
        hand_size_statement('A', 2, "alice"),
        hand_size_statement('B', 1, "bob"))
    envelope_statements: DFA = conjunction_of(
        power_of_two_statement(
            Intersection(Variable('E'), Constant(SUSPECT_CARDS)),
            "envelope_suspect"),
        power_of_two_statement(
            Intersection(Variable('E'), Constant(WEAPON_CARDS)),
            "envelope_weapon"),
        power_of_two_statement(
            Intersection(Variable('E'), Constant(ROOM_CARDS)),
            "envelope_room"))
    knowledge_0: DFA = conjunction_of(
        partition_statement, size_statements, envelope_statements)

    def a_priori_predicate(alice_hand: int, bob_hand: int,
                           envelope_hand: int) -> bool:
        return (alice_hand ^ bob_hand ^ envelope_hand == FULL_DECK
                and alice_hand & bob_hand == 0
                and alice_hand & envelope_hand == 0
                and bob_hand & envelope_hand == 0
                and count_of_set_bits(alice_hand) == 2
                and count_of_set_bits(bob_hand) == 1
                and count_of_set_bits(
                    envelope_hand & SUSPECT_CARDS) == 1
                and count_of_set_bits(
                    envelope_hand & WEAPON_CARDS) == 1
                and count_of_set_bits(envelope_hand & ROOM_CARDS) == 1)

    report_stage(knowledge_0,
                 "K0 (partition + |A|=2 + |B|=1 + envelope categories)",
                 a_priori_predicate)

    # Derived, never asserted: the envelope holds exactly 3 cards
    print_judgment(knowledge_0,
                   hand_size_statement('E', 3, "envelope_size"),
                   "|E| = 3 (derived from partition)")
    # And a non-fact stays unknown:
    print_judgment(knowledge_0, holds_card_statement('E', PLUM),
                   "plum in envelope")

    # ---- Event 1: Alice passes on (plum, knife, hall) ---------------
    suggestion_cards: int = PLUM | KNIFE | HALL
    knowledge_1: DFA = conjunction_of(
        knowledge_0, lacks_cards_statement('A', suggestion_cards))
    report_stage(
        knowledge_1,
        "K1 = K0 + Alice holds none of {plum, knife, hall}",
        lambda alice_hand, bob_hand, envelope_hand:
        a_priori_predicate(alice_hand, bob_hand, envelope_hand)
        and alice_hand & suggestion_cards == 0)

    # ---- Event 2: Bob passes on the same suggestion -----------------
    knowledge_2: DFA = conjunction_of(
        knowledge_1, lacks_cards_statement('B', suggestion_cards))
    report_stage(
        knowledge_2,
        "K2 = K1 + Bob holds none of {plum, knife, hall}",
        lambda alice_hand, bob_hand, envelope_hand:
        a_priori_predicate(alice_hand, bob_hand, envelope_hand)
        and alice_hand & suggestion_cards == 0
        and bob_hand & suggestion_cards == 0)

    print("  deductions at K2:")
    print_judgment(knowledge_2, holds_card_statement('E', PLUM),
                   "plum in envelope")
    print_judgment(knowledge_2, holds_card_statement('E', KNIFE),
                   "knife in envelope")
    print_judgment(knowledge_2, holds_card_statement('E', HALL),
                   "hall in envelope")
    print_judgment(knowledge_2,
                   hand_is_exactly_statement('E', suggestion_cards),
                   "envelope = {plum, knife, hall} exactly")
    print("  one-sidedness at K2 (mustard is in A or B, but neither "
          "is knowable):")
    print_judgment(knowledge_2, holds_card_statement('A', MUSTARD),
                   "mustard in Alice's hand")
    print_judgment(knowledge_2, lacks_cards_statement('A', MUSTARD),
                   "mustard NOT in Alice's hand")
    print_judgment(knowledge_2, holds_card_statement('B', MUSTARD),
                   "mustard in Bob's hand")
    print_judgment(knowledge_2, lacks_cards_statement('E', MUSTARD),
                   "mustard NOT in envelope")

    # ---- Event 3: Bob shows the pipe --------------------------------
    knowledge_3: DFA = conjunction_of(
        knowledge_2, holds_card_statement('B', PIPE))
    final_deals = report_stage(
        knowledge_3, "K3 = K2 + Bob shows pipe",
        lambda alice_hand, bob_hand, envelope_hand:
        a_priori_predicate(alice_hand, bob_hand, envelope_hand)
        and alice_hand & suggestion_cards == 0
        and bob_hand & suggestion_cards == 0
        and bool(bob_hand & PIPE))

    print("  deductions at K3 (everything is forced):")
    print_judgment(knowledge_3,
                   hand_is_exactly_statement('A', MUSTARD | STUDY),
                   "Alice = {mustard, study}")
    print_judgment(knowledge_3, hand_is_exactly_statement('B', PIPE),
                   "Bob = {pipe}")
    print_judgment(knowledge_3,
                   hand_is_exactly_statement('E', suggestion_cards),
                   "envelope = {plum, knife, hall}")
    assert len(final_deals) == 1
    alice_hand, bob_hand, envelope_hand = final_deals[0]
    print(f"  unique consistent deal: A={format_hand(alice_hand)} "
          f"B={format_hand(bob_hand)} E={format_hand(envelope_hand)}")
    print("  accusation: Professor Plum, in the hall, with the knife")

    # The test never lies in the other direction either:
    assert not knowledge_2.entails(holds_card_statement('B', PIPE))
    print("all stages cross-validated against 262,144-deal brute force")


if __name__ == "__main__":
    run_workflow()
