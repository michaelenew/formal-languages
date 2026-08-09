"""Infinite Clue: the smallest Clue-shaped game that the layer cannot
solve, solved on the counted tier.

The finite game was solved without any set-construction operator (0010),
and this module says why: boundedness is a complete escape. On a known
deck every hand size is a known constant, and a constant size is a
clamped counter, which 0011 proved regular. Take the bound away and the
escape closes.

**Infinite Clue.** Cards are the naturals; card i has category i mod 3
(suspect / weapon / room). A deal gives the envelope exactly one card of
each category and splits the rest between two players, and the cards
actually dealt are an initial segment [0, N) whose length N is *not
announced*. The dealing rule is the one real Clue uses: the two hands
are equal in size. You are a spectator -- you hold no cards, and you
learn only what is public: a player passing on a suggestion (holds none
of three cards) and a player refuting one (holds at least one of three).

Every axiom of that game is a layer statement except one:

  disjointness, initial segment, one envelope card per category,
  every pass, every refutation                        -- all automatic
  |H1| = |H2|                                         -- not automatic

`level_crossing.verify_balance_is_not_automatic` measures the second
line: its Myhill-Nerode index is the running difference of the two
counts, which grows without bound, so no DFA holds it and by
Buechi-Bruyere it is not expressible in the layer at all. The balance
rule is the whole gap, and it is the rule that makes the game a game.

This module builds both knowledge states -- with the balance axiom on
the counted tier of `level_crossing`, and without it in the plain layer
-- runs the same scripted game through both, and prints the deduction
grid for each. The cells where they differ are what set construction
buys. Every verdict is cross-validated against brute-force enumeration
of all deals on decks of bounded length, and reported at two counter
windows.

Run directly for the suite.
"""

from __future__ import annotations

import os
import sys
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_automata import DFA
from level_crossing import CountedAutomaton, balance_statement


ENVELOPE = "E"
HANDS = ("H1", "H2")
CHANNELS: tuple[str, ...] = tuple(sorted((ENVELOPE,) + HANDS))
CATEGORY_COUNT = 3
CATEGORY_NAMES = ("suspect", "weapon", "room")


# ---------------------------------------------------------------------
# layer statements (plain DFAs over the three channels)
# ---------------------------------------------------------------------

def _dfa(state_count: int, step, accepting) -> DFA:
    """Build a DFA over CHANNELS from a transition function on
    (state, column) and an acceptance test on states."""
    transitions = []
    for state in range(state_count):
        for bits in range(1 << len(CHANNELS)):
            column = {name: (bits >> index) & 1
                      for index, name in enumerate(CHANNELS)}
            target = step(state, column)
            if target is not None:
                transitions.append((state, column, target))
    return DFA(CHANNELS, state_count, 0, transitions,
               frozenset(state for state in range(state_count)
                         if accepting(state)))


def pairwise_disjoint() -> DFA:
    """No card is held twice. State 1 is the rejecting sink."""
    def step(state, column):
        if state == 1:
            return 1
        return 0 if sum(column.values()) <= 1 else 1
    return _dfa(2, step, lambda state: state == 0)


def dealt_cards_are_an_initial_segment() -> DFA:
    """The dealt set is [0, N): reading least significant position
    first, the dealt bits are 1^N 0^omega."""
    def step(state, column):
        dealt = 1 if any(column.values()) else 0
        if state == 0:
            return 0 if dealt else 1
        if state == 1:
            return 1 if not dealt else 2
        return 2
    return _dfa(3, step, lambda state: state in (0, 1))


def envelope_holds_one_of_each_category() -> DFA:
    """A constant-size constraint: a clamped counter per category, which
    0011 proved regular. State = (position mod 3, clamped counts)."""
    clamp = 2

    def encode(position, counts):
        index = position
        for count in counts:
            index = index * (clamp + 1) + count
        return index

    def decode(state):
        counts = []
        for _ in range(CATEGORY_COUNT):
            state, count = divmod(state, clamp + 1)
            counts.append(count)
        return state, tuple(reversed(counts))

    size = CATEGORY_COUNT * (clamp + 1) ** CATEGORY_COUNT

    def step(state, column):
        position, counts = decode(state)
        raised = list(counts)
        if column[ENVELOPE]:
            raised[position] = min(clamp, raised[position] + 1)
        return encode((position + 1) % CATEGORY_COUNT, tuple(raised))

    def accepting(state):
        _, counts = decode(state)
        return all(count == 1 for count in counts)

    return _dfa(size, step, accepting)


def card_bit(channel: str, card: int, value: int) -> DFA:
    """Bit `card` of `channel` is `value`. States 0..card count
    positions; a word that ends before position `card` has an implicit
    zero there, which is why the counting states accept exactly when
    `value` is 0."""
    good, bad = card + 1, card + 2

    def step(state, column):
        if state < card:
            return state + 1
        if state == card:
            return good if column[channel] == value else bad
        return state

    return _dfa(card + 3, step,
                lambda state: state == good or (state < card + 1
                                                and value == 0))


def holds_none_of(channel: str, cards: tuple[int, ...]) -> DFA:
    statement = card_bit(channel, cards[0], 0)
    for card in cards[1:]:
        statement = statement.intersected_with(
            card_bit(channel, card, 0)).minimized()
    return statement


def holds_at_least_one_of(channel: str, cards: tuple[int, ...]) -> DFA:
    statement = card_bit(channel, cards[0], 1)
    for card in cards[1:]:
        statement = statement.unioned_with(
            card_bit(channel, card, 1)).minimized()
    return statement


def clamped_balance(clamp: int) -> DFA:
    """The best regular over-approximation of |H1| = |H2| at a given
    clamp: count both hands up to `clamp` and require the clamped counts
    to agree. Every balanced deal is accepted, so any verdict it yields
    is sound; it is 0011's clamped counter applied to the balance rule,
    and the suite measures where it stops being complete."""
    def encode(first, second):
        return first * (clamp + 1) + second

    def step(state, column):
        first, second = divmod(state, clamp + 1)
        return encode(min(clamp, first + column[HANDS[0]]),
                      min(clamp, second + column[HANDS[1]]))

    return _dfa((clamp + 1) ** 2, step,
                lambda state: state // (clamp + 1) == state % (clamp + 1))


def deck_at_most(limit: int) -> DFA:
    """No card at position `limit` or beyond is dealt, i.e. N <= limit.
    Used only to line the automata up with brute force."""
    def step(state, column):
        if state < limit:
            return state + 1
        if state == limit:
            return limit if not any(column.values()) else limit + 1
        return limit + 1
    return _dfa(limit + 2, step, lambda state: state <= limit)


# ---------------------------------------------------------------------
# the game
# ---------------------------------------------------------------------

Move = tuple[str, str, tuple[int, ...]]     # (kind, player channel, cards)


def structural_axioms() -> DFA:
    axioms = pairwise_disjoint()
    for piece in (dealt_cards_are_an_initial_segment(),
                  envelope_holds_one_of_each_category()):
        axioms = axioms.intersected_with(piece).minimized()
    return axioms


def layer_knowledge(moves: list[Move], deck_limit: int | None = None
                    ) -> DFA:
    """Everything about the game that the layer can hold."""
    knowledge = structural_axioms()
    for kind, channel, cards in moves:
        piece = (holds_none_of(channel, cards) if kind == "pass"
                 else holds_at_least_one_of(channel, cards))
        knowledge = knowledge.intersected_with(piece).minimized()
    if deck_limit is not None:
        knowledge = knowledge.intersected_with(
            deck_at_most(deck_limit)).minimized()
    return knowledge


def counted_knowledge(knowledge: DFA,
                      balanced: bool = True) -> CountedAutomaton:
    lifted = CountedAutomaton.from_dfa(knowledge, counted_channels=HANDS)
    if not balanced:
        return lifted
    return lifted & balance_statement(*HANDS)


VERDICTS = ("in", "out", "unknown")


def _refutes(knowledge: DFA, hypothesis: DFA, balanced: bool,
             window: int) -> bool:
    """Is knowledge-and-not-hypothesis empty? The layer part of the
    conjunction is built and minimised as a plain DFA first, so the
    counted tier only ever sees a small control automaton -- the
    balance axiom is independent of it."""
    together = knowledge.intersected_with(
        hypothesis.complemented()).minimized()
    return counted_knowledge(together, balanced).is_empty(window)


def verdict(knowledge: DFA, channel: str, card: int, balanced: bool,
            window: int) -> str:
    if _refutes(knowledge, card_bit(channel, card, 1), balanced, window):
        return "in"
    if _refutes(knowledge, card_bit(channel, card, 0), balanced, window):
        return "out"
    return "unknown"


def deduction_grid(knowledge: DFA, cards: range, balanced: bool,
                   window: int) -> dict[tuple[str, int], str]:
    return {(channel, card): verdict(knowledge, channel, card,
                                     balanced, window)
            for channel in CHANNELS for card in cards}


def print_grid(title: str, grid: dict[tuple[str, int], str],
               cards: range) -> None:
    print(f"  {title}")
    header = "      card " + " ".join(f"{card:>8d}" for card in cards)
    print(header)
    for channel in CHANNELS:
        row = " ".join(f"{grid[(channel, card)]:>8s}" for card in cards)
        print(f"    {channel:>6s}  {row}")


# ---------------------------------------------------------------------
# brute force
# ---------------------------------------------------------------------

def all_deals(deck_limit: int):
    """Every legal Infinite Clue deal on a deck shorter than
    `deck_limit`, as (envelope, hand1, hand2) bitsets."""
    for length in range(0, deck_limit + 1):
        cards = list(range(length))
        by_category = [[card for card in cards
                        if card % CATEGORY_COUNT == category]
                       for category in range(CATEGORY_COUNT)]
        if not all(by_category):
            continue
        for suspect in by_category[0]:
            for weapon in by_category[1]:
                for room in by_category[2]:
                    envelope = {suspect, weapon, room}
                    rest = [card for card in cards if card not in envelope]
                    for first_size in range(len(rest) + 1):
                        for first in combinations(rest, first_size):
                            second = [card for card in rest
                                      if card not in first]
                            yield (_bits(envelope), _bits(first),
                                   _bits(second))


def _bits(cards) -> int:
    total = 0
    for card in cards:
        total |= 1 << card
    return total


def _popcount(value: int) -> int:
    return bin(value).count("1")


def brute_force_models(moves: list[Move], deck_limit: int,
                       balanced: bool) -> list[dict[str, int]]:
    models = []
    for envelope, first, second in all_deals(deck_limit):
        assignment = {ENVELOPE: envelope, "H1": first, "H2": second}
        if balanced and _popcount(first) != _popcount(second):
            continue
        if all(_move_holds(assignment, move) for move in moves):
            models.append(assignment)
    return models


def _move_holds(assignment: dict[str, int], move: Move) -> bool:
    kind, channel, cards = move
    held = [bool((assignment[channel] >> card) & 1) for card in cards]
    return not any(held) if kind == "pass" else any(held)


def brute_force_grid(moves: list[Move], deck_limit: int, cards: range,
                     balanced: bool) -> dict[tuple[str, int], str]:
    models = brute_force_models(moves, deck_limit, balanced)
    grid = {}
    for channel in CHANNELS:
        for card in cards:
            held = {bool((model[channel] >> card) & 1)
                    for model in models}
            grid[(channel, card)] = ("in" if held == {True}
                                     else "out" if held == {False}
                                     else "unknown")
    return grid, len(models)


# ---------------------------------------------------------------------
# suite
# ---------------------------------------------------------------------

SCRIPT: list[Move] = [
    ("pass", "H1", (0, 1, 2)),
    ("pass", "H2", (0, 1, 2)),
    ("pass", "H1", (3, 4, 5)),
    ("refute", "H2", (3, 4, 5)),
    ("pass", "H2", (6, 7, 8)),
]


def report_axiom_sizes() -> None:
    print("  layer axioms, as minimal automata over (E, H1, H2):")
    for label, automaton in (
            ("pairwise disjoint", pairwise_disjoint()),
            ("dealt set is an initial segment",
             dealt_cards_are_an_initial_segment()),
            ("one envelope card per category",
             envelope_holds_one_of_each_category().minimized()),
            ("all three together", structural_axioms())):
        print(f"    {label:<34} {automaton.state_count:>4d} states")
    print("    |H1| = |H2|                          no DFA "
          "(level_crossing part 2)")


def scaled_script(scale: int) -> list[Move]:
    """The same game at scale `scale`: the bootstrap between the balance
    rule and the initial-segment rule has to run `scale` rounds."""
    lower = tuple(range(3, 3 + scale))
    upper = tuple(range(3 + scale, 3 + 2 * scale))
    return [("pass", "H1", (0, 1, 2)),
            ("pass", "H2", (0, 1, 2)),
            ("pass", "H1", lower),
            ("refute", "H2", lower),
            ("pass", "H2", upper)]


def clamp_study(scales: range, clamps: range, window: int) -> None:
    """No clamp serves the game: for every clamp there is a scale that
    defeats it, and the scale that defeats clamp k is k+1."""
    header = "    scale  " + " ".join(f"clamp {clamp}"
                                      for clamp in clamps)
    print(header)
    for scale in scales:
        script = scaled_script(scale)
        cards = range(0, 3 + 2 * scale)
        knowledge = layer_knowledge(script)
        target = deduction_grid(knowledge, cards, True, window)
        row = []
        for clamp in clamps:
            approximate = knowledge.intersected_with(
                clamped_balance(clamp)).minimized()
            grid = deduction_grid(approximate, cards, False, window)
            # the clamp is sound, so it can only lose verdicts
            assert not any(grid[key] != "unknown" and grid[key]
                           != target[key] for key in target)
            row.append("  exact" if grid == target else "   lost")
        print(f"    {scale:>5d}  " + " ".join(f"{cell:>7s}"
                                              for cell in row))
    print("    a clamp of k decides the game at scale k and loses it at "
          "scale k+1;")
    print("    the counted tier decides every row with two counters and "
          "no clamp.")


def minimal_adequate_clamp(knowledge: DFA, cards: range, window: int,
                           search_limit: int = 8) -> int | None:
    """The smallest clamp whose verdicts match the counted tier's. The
    clamp is a sound over-approximation, so it can only lose verdicts,
    never invent them -- which is why 'unknown' and 'clamp too small'
    are indistinguishable from inside."""
    target = deduction_grid(knowledge, cards, True, window)
    for clamp in range(search_limit + 1):
        approximate = knowledge.intersected_with(
            clamped_balance(clamp)).minimized()
        if deduction_grid(approximate, cards, False, window) == target:
            return clamp
    return None


def clamp_moves_with_every_event(window: int) -> None:
    """The clamp is a property of the accumulated conjunction, not of the
    balance axiom -- so it cannot be attached to the axiom, and the
    K-workflow cannot maintain it incrementally. Same game, clues
    arriving one at a time."""
    script = scaled_script(4)
    cards = range(0, 11)
    print("    clues  control states  cells known  minimal clamp")
    for prefix_length in range(2, len(script) + 1):
        knowledge = layer_knowledge(script[:prefix_length])
        target = deduction_grid(knowledge, cards, True, window)
        known = sum(1 for cell in target.values() if cell != "unknown")
        clamp = minimal_adequate_clamp(knowledge, cards, window)
        print(f"    {prefix_length:>5d}  {knowledge.state_count:>14d}  "
              f"{known:>11d}  {clamp:>13d}")
    print("    the balance axiom is the same object in every row; the "
          "clamp it needs is not.")
    print("    the counted tier carries the same two counters "
          "throughout, unchanged.")


def cross_validate(deck_limit: int, cards: range, window: int) -> None:
    knowledge = layer_knowledge(SCRIPT, deck_limit=deck_limit)
    for balanced in (True, False):
        machine = deduction_grid(knowledge, cards, balanced, window)
        reference, model_count = brute_force_grid(
            SCRIPT, deck_limit, cards, balanced)
        disagreements = {key for key in machine
                         if machine[key] != reference[key]}
        label = "with balance" if balanced else "without balance"
        print(f"    N <= {deck_limit:>2d}, {label:<15} "
              f"{model_count:>7d} deals enumerated, "
              f"{len(disagreements)} disagreements")
        assert not disagreements, sorted(disagreements)


def run_verification_suite() -> None:
    cards = range(0, 9)
    windows = (5, 9)

    print("=" * 70)
    print("1. Where the game leaves the layer")
    print("=" * 70)
    report_axiom_sizes()

    print()
    print("=" * 70)
    print("2. The scripted game, decided both ways")
    print("=" * 70)
    for kind, channel, move_cards in SCRIPT:
        verb = "holds none of" if kind == "pass" else "holds one of"
        print(f"    {channel} {verb} {list(move_cards)}")
    print()

    knowledge = layer_knowledge(SCRIPT)
    print(f"  layer knowledge, minimised: {knowledge.state_count} states")
    grids = {(window, balanced):
             deduction_grid(knowledge, cards, balanced, window)
             for window in windows for balanced in (True, False)}

    print()
    print_grid("layer only (no balance axiom):",
               grids[(windows[-1], False)], cards)
    print()
    print_grid("counted tier (balance axiom in force):",
               grids[(windows[-1], True)], cards)

    print()
    gained = [key for key in grids[(windows[-1], True)]
              if grids[(windows[-1], True)][key]
              != grids[(windows[-1], False)][key]]
    print(f"  cells decided only with the balance axiom: {len(gained)}")
    for channel, card in sorted(gained):
        print(f"    {channel} / card {card}: "
              f"{grids[(windows[-1], False)][(channel, card)]} -> "
              f"{grids[(windows[-1], True)][(channel, card)]}")

    print()
    for balanced in (True, False):
        agree = grids[(windows[0], balanced)] == grids[(windows[1],
                                                        balanced)]
        label = "with balance" if balanced else "without balance"
        print(f"  windows {windows[0]} and {windows[1]} agree "
              f"({label}): {agree}")
        assert agree

    print()
    print("=" * 70)
    print("3. Why no clamped counter substitutes")
    print("=" * 70)
    clamp_study(range(1, 5), range(1, 5), window=windows[-1])
    print()
    clamp_moves_with_every_event(window=11)

    print()
    print("=" * 70)
    print("4. Cross-validation against brute force")
    print("=" * 70)
    for deck_limit in (9, 11, 13):
        cross_validate(deck_limit, cards, window=windows[-1])

    print()
    print("=" * 70)
    print("all checks passed")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
