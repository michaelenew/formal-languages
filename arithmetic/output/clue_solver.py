"""A mechanical solver for finite Clue-like games on the canonical
automata layer -- the original problem statement, solved for the
bounded case.

The game: cards partitioned into categories; players hold hands of
known sizes; an envelope holds one card per category. Information
arrives as events:

  - own hand           (the observer sees their cards)
  - pass               a player holds NONE of three suggested cards
  - seen refutation    a player shows the observer a specific card
  - unseen refutation  a player shows SOMEONE ELSE a card: they hold
                       AT LEAST ONE of the three -- a nonemptiness
                       fact, expressed by the flip move (complement of
                       "holds none"). This is exactly the event the
                       original expression algebra could not represent
                       (0005 section 1); on the automata layer it is
                       one line.

Knowledge K is one canonical automaton over one channel per hand
(players + envelope): the relation of all deals consistent with
everything seen. Update is intersection; deduction is containment.

The deduction extraction is global, not per-query: ONE forward /
backward reachability sweep over K yields, for every card and every
hand at once, whether any consistent deal includes the card and
whether any excludes it -- so every cell of the "who holds what" grid
gets its one-sided verdict (KNOWN IN / KNOWN OUT / unknown) in a
single pass, and the exact count of consistent deals falls out of the
same dynamic program. "The most you can deduce" is a linear sweep of
the canonical form.

Hand sizes use a direct counter automaton (cardinality_statement),
machine-checked in the suite against 0007's witness-based derivation
(exists k disjoint powers of two XORing to the hand) -- the counter is
an implementation shortcut for a relation already proved to live in
the layer.

Run this file directly: it checks the counter agreement, then plays a
full seeded 12-card, 3-player game with honest mechanics, validating
every round that (1) the true deal stays consistent, (2) every KNOWN
verdict is true of the actual deal, (3) sampled grid verdicts agree
with the entailment test, and (4) the consistent-deal count never
increases; it must end with the envelope exactly identified.
"""

from __future__ import annotations

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_automata import (
    DFA, StateIndex, Transition, Variable, Constant, ExclusiveOr,
    Intersection, statement_of_equality)
from clue_k_workflow import hand_size_statement


# ---------------------------------------------------------------------
# Statements
# ---------------------------------------------------------------------

def cardinality_statement(channel_name: str, count: int) -> DFA:
    """The hand on this channel holds exactly `count` cards: a counter
    automaton -- state = number of set bits seen, clamped one past the
    target (the overflow state absorbs and never accepts)."""
    overflow_state: StateIndex = count + 1
    transitions: list[Transition] = []
    for bits_seen in range(count + 2):
        transitions.append((bits_seen, {channel_name: 0}, bits_seen))
        transitions.append((bits_seen, {channel_name: 1},
                            min(bits_seen + 1, overflow_state)))
    return DFA((channel_name,), count + 2, 0, transitions,
               frozenset({count}))


def cardinality_at_least_statement(channel_name: str,
                                   minimum_count: int) -> DFA:
    """The hand holds AT LEAST `minimum_count` cards: the counter
    CLAMPS at the threshold and accepts there, so no bound on the hand
    is ever needed -- threshold counting requires only threshold-many
    states regardless of how large the set is. Nonemptiness
    (holds_at_least_one_statement) is the minimum_count = 1 case."""
    transitions: list[Transition] = []
    for bits_seen in range(minimum_count + 1):
        transitions.append((bits_seen, {channel_name: 0}, bits_seen))
        transitions.append((bits_seen, {channel_name: 1},
                            min(bits_seen + 1, minimum_count)))
    return DFA((channel_name,), minimum_count + 1, 0, transitions,
               frozenset({minimum_count}))


def masked_cardinality_at_least_statement(
        channel_name: str, card_mask: int, minimum_count: int,
        hidden_tag: str) -> DFA:
    """At least `minimum_count` of the cards in `card_mask` lie on this
    channel -- the threshold clue event ('they hold at least two
    rooms')."""
    hidden_name: str = f"MaskedAtLeast_{hidden_tag}"
    masked_hand: DFA = statement_of_equality(
        Intersection(Variable(channel_name), Constant(card_mask)),
        Variable(hidden_name))
    counted: DFA = masked_hand.intersected_with(
        cardinality_at_least_statement(hidden_name, minimum_count))
    return counted.existentially_projected({hidden_name}).minimized()


def masked_cardinality_statement(channel_name: str, card_mask: int,
                                 count: int, hidden_tag: str) -> DFA:
    """Exactly `count` of the cards in `card_mask` lie on this channel,
    via a hidden channel carrying the masked hand."""
    hidden_name: str = f"Masked_{hidden_tag}"
    masked_hand: DFA = statement_of_equality(
        Intersection(Variable(channel_name), Constant(card_mask)),
        Variable(hidden_name))
    counted: DFA = masked_hand.intersected_with(
        cardinality_statement(hidden_name, count))
    return counted.existentially_projected({hidden_name}).minimized()


def holds_card_statement(channel_name: str, card_mask: int) -> DFA:
    return statement_of_equality(
        Intersection(Variable(channel_name), Constant(card_mask)),
        Constant(card_mask))


def holds_none_statement(channel_name: str, card_mask: int) -> DFA:
    return statement_of_equality(
        Intersection(Variable(channel_name), Constant(card_mask)),
        Constant(0))


def holds_at_least_one_statement(channel_name: str,
                                 card_mask: int) -> DFA:
    """The nonemptiness event: the flip move applied to 'holds none'.
    The one-sided expression algebra could not say this; the automata
    layer says it in one line."""
    return holds_none_statement(channel_name, card_mask).complemented()


def hand_is_exactly_statement(channel_name: str,
                              card_mask: int) -> DFA:
    return statement_of_equality(Variable(channel_name),
                                 Constant(card_mask))


# ---------------------------------------------------------------------
# Game specification
# ---------------------------------------------------------------------

class GameSpecification:
    """Cards grouped in categories, players with fixed hand sizes, an
    envelope holding one card per category."""

    def __init__(self, category_to_cards: dict[str, list[str]],
                 player_hand_sizes: dict[str, int]) -> None:
        self.category_to_cards: dict[str, list[str]] = category_to_cards
        self.player_hand_sizes: dict[str, int] = player_hand_sizes
        self.card_names: list[str] = [
            card_name for card_names in category_to_cards.values()
            for card_name in card_names]
        self.bit_of_card: dict[str, int] = {
            card_name: bit_position
            for bit_position, card_name in enumerate(self.card_names)}
        self.card_count: int = len(self.card_names)
        self.full_deck_mask: int = (1 << self.card_count) - 1
        self.category_masks: dict[str, int] = {
            category_name: sum(1 << self.bit_of_card[card_name]
                               for card_name in card_names)
            for category_name, card_names in category_to_cards.items()}
        self.player_names: list[str] = list(player_hand_sizes)
        self.channel_names: list[str] = (
            self.player_names + ["Envelope"])
        dealt_card_count = sum(player_hand_sizes.values())
        assert dealt_card_count + len(category_to_cards) == (
            self.card_count), "hand sizes + envelope must cover deck"

    def mask_of_cards(self, card_names: list[str]) -> int:
        return sum(1 << self.bit_of_card[card_name]
                   for card_name in card_names)


# ---------------------------------------------------------------------
# The solver
# ---------------------------------------------------------------------

KNOWN_IN = "KNOWN IN"
KNOWN_OUT = "KNOWN OUT"
UNKNOWN = "unknown"


class ClueSolver:
    """Holds K, updates it by intersection, and extracts the full
    deduction grid by one forward/backward sweep."""

    def __init__(self, specification: GameSpecification) -> None:
        self.specification: GameSpecification = specification
        knowledge: DFA = self._partition_statement()
        for player_name, hand_size in (
                specification.player_hand_sizes.items()):
            knowledge = knowledge.intersected_with(
                cardinality_statement(player_name,
                                      hand_size)).minimized()
        for category_name, category_mask in (
                specification.category_masks.items()):
            knowledge = knowledge.intersected_with(
                masked_cardinality_statement(
                    "Envelope", category_mask, 1,
                    category_name)).minimized()
        self.knowledge: DFA = knowledge

    def _partition_statement(self) -> DFA:
        specification = self.specification
        channel_names = specification.channel_names
        xor_of_hands = Variable(channel_names[0])
        for channel_name in channel_names[1:]:
            xor_of_hands = ExclusiveOr(xor_of_hands,
                                       Variable(channel_name))
        combined: DFA = statement_of_equality(
            xor_of_hands, Constant(specification.full_deck_mask))
        for first_index in range(len(channel_names)):
            for second_index in range(first_index + 1,
                                      len(channel_names)):
                combined = combined.intersected_with(
                    statement_of_equality(
                        Intersection(
                            Variable(channel_names[first_index]),
                            Variable(channel_names[second_index])),
                        Constant(0))).minimized()
        return combined

    def learn(self, event_statement: DFA) -> None:
        self.knowledge = self.knowledge.intersected_with(
            event_statement).minimized()

    # -- the one-sweep deduction extraction ---------------------------

    def _compiled_transition_table(
            self) -> tuple[list[dict[str, int]], list[list[int]]]:
        """Flatten K's transitions to integer indices for the sweep:
        a list of columns and, per state, the target for each column
        (-1 for a missing transition)."""
        knowledge = self.knowledge
        columns: list[dict[str, int]] = knowledge.alphabet()
        table: list[list[int]] = [
            [-1] * len(columns) for _ in range(knowledge.state_count)]
        for state in range(knowledge.state_count):
            for column_index, column in enumerate(columns):
                target = knowledge.transition_target(state, column)
                if target is not None:
                    table[state][column_index] = target
        return columns, table

    def deal_survey(self) -> tuple[
            dict[tuple[str, str], str], int]:
        """One forward/backward pass over K, at deck-width word length:
        returns the full deduction grid (every card x every channel ->
        KNOWN IN / KNOWN OUT / unknown) and the exact number of
        consistent deals."""
        specification = self.specification
        knowledge = self.knowledge
        word_length: int = specification.card_count
        columns, table = self._compiled_transition_table()
        state_count: int = knowledge.state_count

        # forward[position][state] = number of ways to reach state
        # after reading `position` columns
        forward: list[list[int]] = [
            [0] * state_count for _ in range(word_length + 1)]
        forward[0][knowledge.initial_state] = 1
        for position in range(word_length):
            for state, ways in enumerate(forward[position]):
                if ways == 0:
                    continue
                for column_index in range(len(columns)):
                    target = table[state][column_index]
                    if target >= 0:
                        forward[position + 1][target] += ways
        # backward[position][state] = number of ways to finish an
        # accepted word from state with `word_length - position`
        # columns left
        backward: list[list[int]] = [
            [0] * state_count for _ in range(word_length + 1)]
        for state in knowledge.accepting_states:
            backward[word_length][state] = 1
        for position in range(word_length - 1, -1, -1):
            for state in range(state_count):
                total_ways = 0
                for column_index in range(len(columns)):
                    target = table[state][column_index]
                    if target >= 0:
                        total_ways += backward[position + 1][target]
                backward[position][state] = total_ways

        consistent_deal_count: int = sum(
            forward[word_length][state]
            for state in knowledge.accepting_states)
        assert consistent_deal_count > 0, "knowledge is inconsistent"

        grid: dict[tuple[str, str], str] = {}
        for card_name in specification.card_names:
            bit_position = specification.bit_of_card[card_name]
            for channel_name in specification.channel_names:
                seen_in = False
                seen_out = False
                for state, ways in enumerate(forward[bit_position]):
                    if ways == 0:
                        continue
                    for column_index, column in enumerate(columns):
                        target = table[state][column_index]
                        if target < 0 or (
                                backward[bit_position + 1][target] == 0):
                            continue
                        if column[channel_name] == 1:
                            seen_in = True
                        else:
                            seen_out = True
                    if seen_in and seen_out:
                        break
                if seen_in and not seen_out:
                    grid[(card_name, channel_name)] = KNOWN_IN
                elif seen_out and not seen_in:
                    grid[(card_name, channel_name)] = KNOWN_OUT
                else:
                    grid[(card_name, channel_name)] = UNKNOWN
        return grid, consistent_deal_count

    def envelope_solution(
            self, grid: dict[tuple[str, str], str]) -> dict[str, str] | None:
        """The solved envelope, one card per category, or None if any
        envelope cell is still unknown."""
        specification = self.specification
        solution: dict[str, str] = {}
        for category_name, card_names in (
                specification.category_to_cards.items()):
            for card_name in card_names:
                if grid[(card_name, "Envelope")] == UNKNOWN:
                    return None
                if grid[(card_name, "Envelope")] == KNOWN_IN:
                    solution[category_name] = card_name
        return solution


# ---------------------------------------------------------------------
# Honest game simulation
# ---------------------------------------------------------------------

class GameSimulation:
    """Plays a full game with honest mechanics. The harness knows the
    true deal; the solver observes as the first player and receives
    only legitimate events."""

    def __init__(self, specification: GameSpecification,
                 random_seed: int) -> None:
        self.specification = specification
        self.random_source = random.Random(random_seed)
        self.true_hands: dict[str, int] = self._deal()
        self.observer_name: str = specification.player_names[0]
        self.solver = ClueSolver(specification)
        self.solver.learn(hand_is_exactly_statement(
            self.observer_name, self.true_hands[self.observer_name]))

    def _deal(self) -> dict[str, int]:
        specification = self.specification
        envelope_mask = 0
        remaining_card_names: list[str] = []
        for card_names in specification.category_to_cards.values():
            chosen = self.random_source.choice(card_names)
            envelope_mask |= 1 << specification.bit_of_card[chosen]
            remaining_card_names.extend(
                card_name for card_name in card_names
                if card_name != chosen)
        self.random_source.shuffle(remaining_card_names)
        hands: dict[str, int] = {"Envelope": envelope_mask}
        deal_position = 0
        for player_name, hand_size in (
                specification.player_hand_sizes.items()):
            hand_mask = specification.mask_of_cards(
                remaining_card_names[
                    deal_position:deal_position + hand_size])
            hands[player_name] = hand_mask
            deal_position += hand_size
        return hands

    def _choose_suggestion(self, suggester_name: str,
                           grid: dict[tuple[str, str], str]) -> list[str]:
        """The observer targets cards whose envelope cell is unknown;
        other players suggest at random."""
        specification = self.specification
        suggestion: list[str] = []
        for card_names in specification.category_to_cards.values():
            if suggester_name == self.observer_name:
                unknown_cards = [
                    card_name for card_name in card_names
                    if grid[(card_name, "Envelope")] == UNKNOWN]
                pool = unknown_cards or card_names
            else:
                pool = card_names
            suggestion.append(self.random_source.choice(pool))
        return suggestion

    def _run_suggestion(self, suggester_name: str,
                        suggestion: list[str]) -> None:
        """Honest Clue mechanics: players after the suggester in table
        order pass (hold none) or refute (show one held card, chosen
        as their lowest-indexed held card -- the solver does not
        assume anything about this choice)."""
        specification = self.specification
        suggestion_mask = specification.mask_of_cards(suggestion)
        player_names = specification.player_names
        suggester_index = player_names.index(suggester_name)
        for offset in range(1, len(player_names)):
            responder_name = player_names[
                (suggester_index + offset) % len(player_names)]
            held_mask = self.true_hands[responder_name] & suggestion_mask
            if held_mask == 0:
                if responder_name != self.observer_name:
                    self.solver.learn(holds_none_statement(
                        responder_name, suggestion_mask))
                continue
            # responder refutes
            if responder_name == self.observer_name:
                pass  # the observer's own hand is already known
            elif suggester_name == self.observer_name:
                shown_mask = held_mask & -held_mask
                self.solver.learn(holds_card_statement(
                    responder_name, shown_mask))
            else:
                self.solver.learn(holds_at_least_one_statement(
                    responder_name, suggestion_mask))
            return
        # nobody could refute

    def _assert_grid_faithful(
            self, grid: dict[tuple[str, str], str],
            spot_check_count: int) -> None:
        """(a) Every KNOWN verdict holds in the true deal; (b) sampled
        cells agree with the entailment test."""
        specification = self.specification
        for (card_name, channel_name), verdict in grid.items():
            card_mask = 1 << specification.bit_of_card[card_name]
            actually_in = bool(
                self.true_hands[channel_name] & card_mask)
            if verdict == KNOWN_IN:
                assert actually_in, "false KNOWN IN"
            elif verdict == KNOWN_OUT:
                assert not actually_in, "false KNOWN OUT"
        all_cells = list(grid)
        for card_name, channel_name in self.random_source.sample(
                all_cells, spot_check_count):
            card_mask = 1 << specification.bit_of_card[card_name]
            entailed_in = self.solver.knowledge.entails(
                holds_card_statement(channel_name, card_mask))
            entailed_out = self.solver.knowledge.entails(
                holds_none_statement(channel_name, card_mask))
            verdict = grid[(card_name, channel_name)]
            assert entailed_in == (verdict == KNOWN_IN)
            assert entailed_out == (verdict == KNOWN_OUT)

    def play(self, maximum_rounds: int) -> dict[str, str]:
        specification = self.specification
        previous_deal_count: int | None = None
        true_assignment = dict(self.true_hands)
        for round_number in range(1, maximum_rounds + 1):
            grid, deal_count = self.solver.deal_survey()
            assert self.solver.knowledge.accepts_assignment(
                true_assignment), "true deal ruled out"
            self._assert_grid_faithful(grid, spot_check_count=2)
            if previous_deal_count is not None:
                assert deal_count <= previous_deal_count, \
                    "consistent deals increased"
            previous_deal_count = deal_count
            solution = self.solver.envelope_solution(grid)
            known_cells = sum(
                1 for verdict in grid.values() if verdict != UNKNOWN)
            print(f"round {round_number:2d}: "
                  f"K = {self.solver.knowledge.state_count:4d} states, "
                  f"{deal_count:5d} consistent deals, "
                  f"{known_cells}/{len(grid)} cells known"
                  + (f", SOLVED: {solution}" if solution else ""))
            if solution is not None:
                self._assert_grid_faithful(grid, spot_check_count=12)
                return solution
            for player_name in specification.player_names:
                current_grid, _ = self.solver.deal_survey()
                suggestion = self._choose_suggestion(player_name,
                                                     current_grid)
                self._run_suggestion(player_name, suggestion)
        raise AssertionError("envelope not solved within round limit")


# ---------------------------------------------------------------------
# Verification suite
# ---------------------------------------------------------------------

def run_verification_suite() -> None:
    # The counter automaton agrees with 0007's witness-based
    # cardinality derivation (which proved counting lives in the
    # layer) -- checked as full relation equality.
    for count in (1, 2, 3):
        counter_version = cardinality_statement('A', count)
        witness_version = hand_size_statement('A', count,
                                              f"agree_{count}")
        assert counter_version.describes_same_relation_as(
            witness_version)
    print("cardinality counter == witness-based derivation "
          "(k = 1, 2, 3, full relation equality)  OK")

    # 'At least k' generalizes the nonemptiness flip exactly: the
    # clamped counter equals the complement of the union of the
    # below-threshold exact counts -- full relation equality, and no
    # bound on the counted set anywhere.
    for minimum_count in (1, 2, 3):
        below_threshold: DFA = cardinality_statement('A', 0)
        for exact_count in range(1, minimum_count):
            below_threshold = below_threshold.unioned_with(
                cardinality_statement('A', exact_count))
        assert cardinality_at_least_statement(
            'A', minimum_count).describes_same_relation_as(
            below_threshold.complemented())
    print("at-least-k counter == flip of union of exact counts "
          "below k (k = 1, 2, 3, full relation equality)  OK")

    # Threshold clue event against ground truth
    threshold_statement = masked_cardinality_at_least_statement(
        'A', 0b1101, 2, "unit_test")
    for hand_mask in range(64):
        expected = bin(hand_mask & 0b1101).count('1') >= 2
        assert threshold_statement.accepts_assignment(
            {'A': hand_mask}) == expected
    print("masked at-least threshold event: exhaustive 6-bit ground "
          "truth  OK")

    compact_specification = GameSpecification(
        category_to_cards={
            "suspect": ["mustard", "plum", "scarlet", "green"],
            "weapon": ["knife", "pipe", "rope", "wrench"],
            "room": ["hall", "study", "lounge", "kitchen"],
        },
        player_hand_sizes={"Alice": 3, "Bob": 3, "Carol": 3})
    full_size_specification = GameSpecification(
        category_to_cards={
            "suspect": ["mustard", "plum", "scarlet", "green",
                        "peacock", "orchid"],
            "weapon": ["knife", "candlestick", "revolver", "rope",
                       "pipe", "wrench"],
            "room": ["hall", "lounge", "dining", "kitchen", "ballroom",
                     "conservatory", "billiard", "library", "study"],
        },
        player_hand_sizes={"Alice": 6, "Bob": 6, "Carol": 6})
    for label, specification, random_seed in (
            ("compact 12-card game", compact_specification, 7),
            ("full-size 21-card game", full_size_specification, 11)):
        print(f"--- {label} ---")
        simulation = GameSimulation(specification, random_seed)
        solution = simulation.play(maximum_rounds=60)
        true_envelope = simulation.true_hands["Envelope"]
        solved_mask = specification.mask_of_cards(
            list(solution.values()))
        assert solved_mask == true_envelope, "wrong accusation"
        print(f"accusation verified against the true deal: {solution}")
    print("all checks passed")


if __name__ == "__main__":
    run_verification_suite()
