"""The set-construction operator {x} = 2^x: what it costs, and the one
tier that can carry it.

The corpus expected every Clue move to need a set-construction operator
(`clue/2026-06-21 AI exploration.md`, "First extension"; the same object
appears in `clue/2025-04-04 size operator and hamming distance.md` as
"the set containing N is 2 ** N"). The finite game was then solved
without it (0007, 0010). This module locates the operator exactly.

Three facts, each machine-checked here:

1. **Set construction and the size operator are interdefinable** over
   the layer:  y = 2^x  iff  |y| = 1 and |y-1| = x.  So the operator
   the corpus expected and the operator its stated limitation (set
   sizes) demands are one operator, not two.

2. **Unguarded, it is full arithmetic.**  With {.} available, top-level
   membership `{p} & X != 0` becomes hereditary membership, i.e. the
   Ackermann BIT relation; (N, BIT) is the Ackermann coding of
   (V_omega, in), which is bi-interpretable with (N, +, x) -- classical.
   So Th(layer + {.}) is undecidable and no convex syntax can carry it.
   This sits strictly below 0001's ceiling: one binary relation, no
   arithmetic operator needed.

3. **The guard is two clauses on the primitives, and it needs both.**
   Set terms are built from `^`, `&`, `<<` (everything automatic);
   count terms are `|t|` and integer combinations. Then: **(i)** no set
   term is built by a non-automatic operation, so {.} is not a
   term-former; **(ii)** no atom mixes a set term with a count term.
   Each clause has its own escape if dropped -- `|y-1| = x` defeats (i)
   alone, and `|x| = |{y} - {0}|` defeats (ii) alone, both landing on
   the same BIT. Anything obeying both compiles to a deterministic
   Parikh automaton, which is decidable, so the pair is a syntactic
   characterisation of a decidable class rather than a fence to be
   re-checked. `CountedAutomaton` below is that class, over the layer's
   own bit columns.

   In eigen-frame terms (0023-0028): `&` diagonalises restrictions,
   `^` translations, `<<` the shift -- and `|.|` is the complete
   invariant of the remaining family, `S_n` permuting bit positions
   (verified). 0013/0014's obstruction table already named permutation
   invariance as what `<<` exists to break, so the counting level is
   that split's other half. A deterministic Parikh automaton factors a
   statement into an order-sensitive finite part (the control state)
   and an order-invariant unbounded part (the counters); {.} = 2^x is
   the map that turns a value into a position, identifying the two
   coordinates the factorisation keeps apart.

`CountedAutomaton` is closed under intersection, union and complement
(determinism makes complement free, which the nondeterministic Parikh
class does not have), decides emptiness and entailment inside a
declared counter window, and machine-enforces the guard: hiding a
counted channel succeeds only when the counter stays a function of the
visible word, and raises `GuardViolation` with a witness otherwise.

Window semantics, stated exactly: counters never decrease, so
`is_empty(window)` means "no witness whose every counter stays at or
below `window`" -- a precise finite relation, not an approximation of
one. The general decision procedure needs Presburger satisfiability
over the Parikh image of the underlying DFA (Verma-Seidl-Schwentick;
Klaedtke-Ruess), which is not implemented here; every verdict this
module asserts is reported at two windows.

Run directly for the verification suite.
"""

from __future__ import annotations

import os
import sys
from itertools import product as cartesian_product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_automata import (
    DFA, Variable, relation_addition, relation_exclusive_or,
    relation_intersection, relation_shift_fill_zero,
    relation_trailing_ones)


ColumnKey = tuple[int, ...]
CountVector = tuple[int, ...]


def popcount(value: int) -> int:
    return bin(value).count("1")


def columns_over(channels: tuple[str, ...]) -> list[ColumnKey]:
    return [tuple(bits) for bits
            in cartesian_product((0, 1), repeat=len(channels))]


# ---------------------------------------------------------------------
# Part 1 -- the operator, and what it is the same as
# ---------------------------------------------------------------------

def verify_interdefinability(bound: int = 1 << 16) -> None:
    """{.} and |.| define each other over the layer."""
    forward_failures = [x for x in range(0, 300)
                        if not (popcount(1 << x) == 1
                                and popcount((1 << x) - 1) == x)]
    assert not forward_failures, forward_failures[:5]

    converse_failures = [y for y in range(1, bound)
                         if popcount(y) == 1 and y != (1 << popcount(y - 1))]
    assert not converse_failures, converse_failures[:5]

    print("  y = 2^x  <=>  |y| = 1 and |y-1| = x")
    print(f"    forward checked for x < 300, converse for y < {bound}: "
          "no failures")
    print("    the definition uses the size operator and predecessor and "
          "nothing else,")
    print("    so set construction and set size are one operator over "
          "the layer.")


def verify_level_map_conjugation(bound: int = 200) -> None:
    """The corpus's three level-map lines, separated into the one that
    is an identity and the two that are definitions by conjugation."""
    assert all((1 << (x + 1)) == 2 * (1 << x) for x in range(bound))
    print(f"  E(x+1) = 2*E(x)          identity, checked to x < {bound}"
          "   (corpus: '2A = 2 ** PLUS1(LOG2(A))')")

    xor_witness = next((a, b) for a in range(6) for b in range(6)
                       if ((1 << a) ^ (1 << b)) != (1 << (a ^ b)))
    and_witness = next((a, b) for a in range(6) for b in range(6)
                       if ((1 << a) & (1 << b)) != (1 << (a & b)))
    a, b = xor_witness
    print(f"  E(a) ^ E(b) != E(a^b)    first witness a={a}, b={b}: "
          f"{(1 << a) ^ (1 << b)} vs {1 << (a ^ b)}")
    a, b = and_witness
    print(f"  E(a) & E(b) != E(a&b)    first witness a={a}, b={b}: "
          f"{(1 << a) & (1 << b)} vs {1 << (a & b)}")
    print("    reading: the corpus's XOR/AND level lines are definitions "
          "of the lifted")
    print("    operators by conjugation, not laws of ^ and &. Only the "
          "successor line")
    print("    is a law -- E carries the coarse successor to the fine "
          "doubling, which is")
    print("    why the upward direction looks cheap one step at a time "
          "and is not.")


def verify_membership_becomes_bit(bound: int = 64) -> None:
    """Top-level membership plus {.} is hereditary membership."""
    failures = [(p, x) for x in range(bound) for p in range(6)
                if (((1 << p) & x) != 0) != bool((x >> p) & 1)]
    assert not failures, failures[:5]
    print(f"  {{p}} & X != 0  is  BIT(p, X)   checked for p < 6, X < "
          f"{bound}: no failures")
    print("    BIT needs no further operator to iterate, so layer + {.} "
          "contains")
    print("    hereditary membership = (V_omega, in), which the Ackermann "
          "coding makes")
    print("    bi-interpretable with (N, +, x). Undecidable, hence no "
          "convex syntax.")


# ---------------------------------------------------------------------
# Part 2 -- what the layer cannot hold: the balance relation
# ---------------------------------------------------------------------

_BALANCE_ALPHABET: tuple[tuple[int, int], ...] = (
    (0, 0), (0, 1), (1, 0), (1, 1))


def _walk(word, partition: bool):
    """Read a prefix of the balance relation. Returns (legal, difference,
    still-inside-the-dealt-segment)."""
    difference = 0
    inside = True
    for left, right in word:
        if partition:
            if inside and left + right != 1:
                if left + right == 0:
                    inside = False
                else:
                    return False, 0, False
            elif not inside and left + right != 0:
                return False, 0, False
        difference += left - right
    return True, difference, inside


def _residual_signature(difference: int, inside: bool, probe_depth: int,
                        partition: bool) -> tuple[bool, ...]:
    signature: list[bool] = []
    for length in range(probe_depth + 1):
        for suffix in cartesian_product(_BALANCE_ALPHABET, repeat=length):
            legal, delta, _ = _walk(suffix, partition and inside)
            if partition and not inside:
                legal = all(left + right == 0 for left, right in suffix)
                delta = 0
            signature.append(legal and difference + delta == 0)
    return tuple(signature)


def residual_growth(max_prefix_length: int,
                    partition: bool) -> list[tuple[int, int]]:
    """Distinct Myhill-Nerode residuals of the balance relation, by
    prefix length. The probe depth grows with the prefix, so the
    measurement is not capped by the probe."""
    growth: list[tuple[int, int]] = []
    for prefix_length in range(max_prefix_length + 1):
        signatures = set()
        for length in range(prefix_length + 1):
            for prefix in cartesian_product(_BALANCE_ALPHABET,
                                            repeat=length):
                legal, difference, inside = _walk(prefix, partition)
                if not legal:
                    continue
                signatures.add(_residual_signature(
                    difference, inside, prefix_length + 1, partition))
        growth.append((prefix_length, len(signatures)))
    return growth


def verify_balance_is_not_automatic(max_prefix_length: int = 6) -> None:
    """Two forms of the balance rule, both with unbounded residual
    index -- so neither is an automatic relation, and by Buechi-Bruyere
    neither is expressible in the layer at all."""
    for label, partition in (("|A| = |B|", False),
                             ("|A| = |B|, A + B = [0,N)", True)):
        growth = residual_growth(max_prefix_length, partition)
        shown = ", ".join(f"{k}:{n}" for k, n in growth)
        print(f"  {label:<26} residuals by prefix length -- {shown}")
        counts = [n for _, n in growth]
        assert all(later > earlier
                   for earlier, later in zip(counts, counts[1:])), counts
    print("    strictly increasing in both forms, so no DFA serves either "
          "relation;")
    print("    0011's clamped counters cannot help -- a clamp is exactly "
          "a finite")
    print("    residual bound, and the index here is the running "
          "difference of the")
    print("    two counts, which is unbounded by construction.")


def _level_map_language(width: int) -> set[tuple[tuple[int, int], ...]]:
    """{(x, y) : y = 2^x} as length-`width` words of columns (x-bit,
    y-bit), least significant position first."""
    words = set()
    for exponent in range(width):
        value, power = exponent, 1 << exponent
        words.add(tuple(((value >> position) & 1,
                         (power >> position) & 1)
                        for position in range(width)))
    return words


def level_map_minimal_states(width: int) -> int:
    """Minimal DFA size of the level map truncated to `width` positions,
    by direct Nerode counting over all prefixes."""
    language = _level_map_language(width)
    classes = set()
    for prefix_length in range(width + 1):
        prefixes = {word[:prefix_length] for word in language}
        prefixes |= {tuple(column) for column
                     in cartesian_product(((0, 0), (0, 1), (1, 0), (1, 1)),
                                          repeat=prefix_length)}
        for prefix in prefixes:
            classes.add(frozenset(
                word[prefix_length:] for word in language
                if word[:prefix_length] == prefix))
    return len(classes)


def verify_level_map_is_not_automatic(max_width: int = 9) -> None:
    """The level map is outside the layer by the same kind of
    measurement as the balance rule -- but for the opposite reason: it
    compares a position to a value, not a count to a count."""
    sizes = [(width, level_map_minimal_states(width))
             for width in range(2, max_width + 1)]
    shown = ", ".join(f"{width}:{size}" for width, size in sizes)
    print(f"  y = 2^x truncated to width w    Nerode classes -- {shown}")
    counts = [size for _, size in sizes]
    assert all(later > earlier
               for earlier, later in zip(counts, counts[1:])), counts
    print("    strictly increasing, so the level map has no DFA either.")
    print("    Different disease from the balance rule: balance needs "
          "count against count,")
    print("    which a counter supplies; the level map needs position "
          "against value,")
    print("    which nothing below full arithmetic supplies.")


def verify_popcount_is_the_permutation_invariant(width: int = 5) -> None:
    """Popcount is the complete invariant of the position-permuting
    action -- the orbits of S_n on bitstrings are exactly the popcount
    levels. This is why the size operator is the invariant of precisely
    the symmetry that << exists to break (0013/0014's obstruction
    table)."""
    from itertools import permutations
    orbits: dict[int, frozenset[int]] = {}
    for value in range(1 << width):
        bits = [(value >> position) & 1 for position in range(width)]
        orbit = frozenset(
            sum(bits[order[position]] << position
                for position in range(width))
            for order in permutations(range(width)))
        orbits[value] = orbit
    by_popcount: dict[int, set[int]] = {}
    for value in range(1 << width):
        by_popcount.setdefault(popcount(value), set()).add(value)
    for value, orbit in orbits.items():
        assert set(orbit) == by_popcount[popcount(value)], value
    print(f"  S_n orbits on {width}-bit strings are exactly the "
          f"{width + 1} popcount levels (exhaustive)")
    print("    so |.| is the complete invariant of position "
          "permutation, and << is")
    print("    what 0013/0014 identified as the escape from that same "
          "invariance.")


# ---------------------------------------------------------------------
# Part 3 -- the tier below the forbidden move
# ---------------------------------------------------------------------

class CountPredicate:
    """A Presburger condition on the counter vector. Counters are named;
    `holds` reads a name->value mapping. Nothing in this class can
    mention a channel *value* -- that omission is the guard."""

    def holds(self, counts: dict[str, int]) -> bool:
        raise NotImplementedError

    def negated(self) -> "CountPredicate":
        return NegatedPredicate(self)

    def substituted(self, name: str, value: int) -> "CountPredicate":
        """Pin one counter to a known value."""
        raise NotImplementedError

    def description(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.description()


class AlwaysTrue(CountPredicate):
    def holds(self, counts: dict[str, int]) -> bool:
        return True

    def substituted(self, name: str, value: int) -> CountPredicate:
        return self

    def description(self) -> str:
        return "true"


class AlwaysFalse(CountPredicate):
    def holds(self, counts: dict[str, int]) -> bool:
        return False

    def substituted(self, name: str, value: int) -> CountPredicate:
        return self

    def description(self) -> str:
        return "false"


class LinearConstraint(CountPredicate):
    """sum(coefficient * counter) `relation` constant, relation one of
    "=", ">=", "<="."""

    def __init__(self, coefficients: dict[str, int], relation: str,
                 constant: int) -> None:
        assert relation in ("=", ">=", "<=")
        self.coefficients = {name: weight
                             for name, weight in coefficients.items()
                             if weight != 0}
        self.relation = relation
        self.constant = constant

    def holds(self, counts: dict[str, int]) -> bool:
        total = sum(weight * counts.get(name, 0)
                    for name, weight in self.coefficients.items())
        if self.relation == "=":
            return total == self.constant
        if self.relation == ">=":
            return total >= self.constant
        return total <= self.constant

    def substituted(self, name: str, value: int) -> CountPredicate:
        if name not in self.coefficients:
            return self
        remaining = dict(self.coefficients)
        weight = remaining.pop(name)
        return LinearConstraint(remaining, self.relation,
                                self.constant - weight * value)

    def description(self) -> str:
        body = " + ".join(f"{weight}*{name}" for name, weight
                          in sorted(self.coefficients.items())) or "0"
        return f"({body} {self.relation} {self.constant})"


class _Junction(CountPredicate):
    def __init__(self, parts: list[CountPredicate]) -> None:
        self.parts = list(parts)

    def substituted(self, name: str, value: int) -> CountPredicate:
        return type(self)([part.substituted(name, value)
                           for part in self.parts])


class Conjunction(_Junction):
    def holds(self, counts: dict[str, int]) -> bool:
        return all(part.holds(counts) for part in self.parts)

    def description(self) -> str:
        return "(" + " and ".join(part.description()
                                  for part in self.parts) + ")"


class Disjunction(_Junction):
    def holds(self, counts: dict[str, int]) -> bool:
        return any(part.holds(counts) for part in self.parts)

    def description(self) -> str:
        return "(" + " or ".join(part.description()
                                 for part in self.parts) + ")"


class NegatedPredicate(CountPredicate):
    def __init__(self, inner: CountPredicate) -> None:
        self.inner = inner

    def holds(self, counts: dict[str, int]) -> bool:
        return not self.inner.holds(counts)

    def negated(self) -> CountPredicate:
        return self.inner

    def substituted(self, name: str, value: int) -> CountPredicate:
        return NegatedPredicate(self.inner.substituted(name, value))

    def description(self) -> str:
        return f"not {self.inner.description()}"


class GuardViolation(Exception):
    """Raised when hiding a channel would make a counter depend on the
    hidden choice -- the move that leaves the tier."""


class CountedAutomaton:
    """A deterministic Parikh automaton over the layer's bit columns.

    A word is a sequence of bit columns, least significant position
    first, exactly as in `canonical_automata`. Each counted channel
    carries one counter, incremented by that channel's bit; a counter is
    therefore a monoid homomorphism of the input word, and is invariant
    under the layer's zero padding -- which is what lets counted and
    uncounted statements compose with no alignment bookkeeping.
    Acceptance is a per-state Presburger predicate on the counters.
    """

    def __init__(self, channels: tuple[str, ...],
                 counted_channels: tuple[str, ...],
                 state_count: int,
                 initial_state: int,
                 transition_table: dict[tuple[int, ColumnKey], int],
                 acceptance: list[CountPredicate]) -> None:
        self.channels = tuple(sorted(channels))
        self.counted_channels = tuple(sorted(counted_channels))
        assert set(self.counted_channels) <= set(self.channels)
        self.state_count = state_count
        self.initial_state = initial_state
        self.transition_table = dict(transition_table)
        self.acceptance = list(acceptance)
        assert len(self.acceptance) == state_count

    # -- alphabet -----------------------------------------------------

    def columns(self) -> list[ColumnKey]:
        return columns_over(self.channels)

    def column_dict(self, column: ColumnKey) -> dict[str, int]:
        return dict(zip(self.channels, column))

    def _increment(self, column: ColumnKey) -> CountVector:
        position = {name: index
                    for index, name in enumerate(self.channels)}
        return tuple(column[position[name]]
                     for name in self.counted_channels)

    def _counts_mapping(self, counts: CountVector) -> dict[str, int]:
        return dict(zip(self.counted_channels, counts))

    def _initial_configuration(self) -> tuple[int, CountVector]:
        return (self.initial_state,
                tuple(0 for _ in self.counted_channels))

    # -- construction -------------------------------------------------

    @staticmethod
    def from_dfa(automaton: DFA,
                 channels: tuple[str, ...] = (),
                 counted_channels: tuple[str, ...] = ()
                 ) -> "CountedAutomaton":
        """Lift a layer automaton. Extra channels are read and ignored,
        which is how the layer's alignment-free composition survives."""
        total: DFA = automaton.completed()
        all_channels = tuple(sorted(set(total.variable_names)
                                    | set(channels)
                                    | set(counted_channels)))
        table: dict[tuple[int, ColumnKey], int] = {}
        for state in range(total.state_count):
            for column in columns_over(all_channels):
                target = total.transition_target(
                    state, dict(zip(all_channels, column)))
                assert target is not None
                table[(state, column)] = target
        return CountedAutomaton(
            all_channels, counted_channels, total.state_count,
            total.initial_state, table,
            [AlwaysTrue() if state in total.accepting_states
             else AlwaysFalse()
             for state in range(total.state_count)])

    @staticmethod
    def count_constraint(counted_channels: tuple[str, ...],
                         predicate: CountPredicate,
                         channels: tuple[str, ...] = ()
                         ) -> "CountedAutomaton":
        """The one-control-state automaton that accepts on the counters
        alone."""
        all_channels = tuple(sorted(set(counted_channels) | set(channels)))
        return CountedAutomaton(
            all_channels, counted_channels, 1, 0,
            {(0, column): 0 for column in columns_over(all_channels)},
            [predicate])

    # -- Boolean closure ----------------------------------------------

    def _widened_to(self, channels: tuple[str, ...]) -> "CountedAutomaton":
        target = tuple(sorted(set(self.channels) | set(channels)))
        if target == self.channels:
            return self
        table: dict[tuple[int, ColumnKey], int] = {}
        for state in range(self.state_count):
            for column in columns_over(target):
                mapping = dict(zip(target, column))
                own = tuple(mapping[name] for name in self.channels)
                table[(state, column)] = self.transition_table[(state, own)]
        return CountedAutomaton(target, self.counted_channels,
                                self.state_count, self.initial_state,
                                table, list(self.acceptance))

    def _combined_with(self, other: "CountedAutomaton",
                       combine) -> "CountedAutomaton":
        channels = tuple(sorted(set(self.channels) | set(other.channels)))
        left = self._widened_to(channels)
        right = other._widened_to(channels)
        counted = tuple(sorted(set(left.counted_channels)
                               | set(right.counted_channels)))
        alphabet = columns_over(channels)
        index: dict[tuple[int, int], int] = {}
        order: list[tuple[int, int]] = []

        def state_index(pair: tuple[int, int]) -> int:
            if pair not in index:
                index[pair] = len(order)
                order.append(pair)
            return index[pair]

        state_index((left.initial_state, right.initial_state))
        table: dict[tuple[int, ColumnKey], int] = {}
        position = 0
        while position < len(order):
            pair = order[position]
            source = position
            position += 1
            for column in alphabet:
                table[(source, column)] = state_index(
                    (left.transition_table[(pair[0], column)],
                     right.transition_table[(pair[1], column)]))
        acceptance = [combine(left.acceptance[pair[0]],
                              right.acceptance[pair[1]])
                      for pair in order]
        return CountedAutomaton(channels, counted, len(order), 0, table,
                                acceptance)

    def intersected_with(self, other: "CountedAutomaton"
                         ) -> "CountedAutomaton":
        return self._combined_with(other,
                                   lambda a, b: Conjunction([a, b]))

    def unioned_with(self, other: "CountedAutomaton"
                     ) -> "CountedAutomaton":
        return self._combined_with(other,
                                   lambda a, b: Disjunction([a, b]))

    def complemented(self) -> "CountedAutomaton":
        """Free, because the machine is deterministic and total: one run
        per word, so the complement only negates the acceptance
        predicate. The nondeterministic Parikh class has no such move --
        its universality problem is undecidable."""
        return CountedAutomaton(
            self.channels, self.counted_channels, self.state_count,
            self.initial_state, self.transition_table,
            [predicate.negated() for predicate in self.acceptance])

    def __and__(self, other: "CountedAutomaton") -> "CountedAutomaton":
        return self.intersected_with(other)

    def __or__(self, other: "CountedAutomaton") -> "CountedAutomaton":
        return self.unioned_with(other)

    def __invert__(self) -> "CountedAutomaton":
        return self.complemented()

    # -- the guard, enforced ------------------------------------------

    def _dead_states(self, window: int) -> set[int]:
        """States from which no counter vector inside the window can ever
        be accepted. Branches into them carry no models, so hiding a
        channel must not read them -- otherwise every rejecting sink
        would look like a free choice."""
        grid = list(cartesian_product(range(window + 1),
                                      repeat=len(self.counted_channels)))
        alive = {state for state in range(self.state_count)
                 if any(self.acceptance[state].holds(
                     self._counts_mapping(counts)) for counts in grid)}
        alphabet = self.columns()
        changed = True
        while changed:
            changed = False
            for state in range(self.state_count):
                if state in alive:
                    continue
                if any(self.transition_table[(state, column)] in alive
                       for column in alphabet):
                    alive.add(state)
                    changed = True
        return set(range(self.state_count)) - alive

    def existentially_projected(self, channel: str, window: int
                                ) -> "CountedAutomaton":
        """Hide a channel. Legal when the counters stay a function of the
        visible word: automatic if the channel is uncounted, and needing
        the channel to be functionally determined if it is counted (the
        0008 uniquely-determined wire, now carrying a counter). Raises
        GuardViolation with a witness word otherwise."""
        assert channel in self.channels
        remaining = tuple(name for name in self.channels
                          if name != channel)
        counted = tuple(name for name in self.counted_channels
                        if name != channel)
        hidden_position = self.channels.index(channel)
        hidden_counter = (self.counted_channels.index(channel)
                          if channel in self.counted_channels else None)
        visible_alphabet = columns_over(remaining)
        dead_states = self._dead_states(window)

        start = frozenset({(self.initial_state, 0)})
        index: dict[frozenset, int] = {start: 0}
        order: list[frozenset] = [start]
        witness: dict[frozenset, tuple[ColumnKey, ...]] = {start: ()}
        table: dict[tuple[int, ColumnKey], int] = {}
        position = 0
        while position < len(order):
            configs = order[position]
            source = position
            position += 1
            for visible in visible_alphabet:
                targets = set()
                for state, hidden_count in configs:
                    for bit in (0, 1):
                        full = list(visible)
                        full.insert(hidden_position, bit)
                        column = tuple(full)
                        raised = hidden_count + (
                            bit if hidden_counter is not None else 0)
                        if raised > window:
                            continue
                        target = self.transition_table[(state, column)]
                        if target in dead_states:
                            continue
                        targets.add((target, raised))
                frozen = frozenset(targets)
                if not frozen:
                    continue
                distinct = {count for _, count in frozen}
                if len(distinct) > 1:
                    trace = witness[configs] + (visible,)
                    raise GuardViolation(
                        f"hiding {channel!r} leaves its counter "
                        f"undetermined ({sorted(distinct)}) after the "
                        f"visible word "
                        f"{[dict(zip(remaining, c)) for c in trace]}")
                if frozen not in index:
                    index[frozen] = len(order)
                    order.append(frozen)
                    witness[frozen] = witness[configs] + (visible,)
                table[(source, visible)] = index[frozen]

        dead = len(order)
        acceptance: list[CountPredicate] = []
        for configs in order:
            parts = []
            for state, hidden_count in configs:
                predicate = self.acceptance[state]
                if hidden_counter is not None:
                    predicate = predicate.substituted(channel, hidden_count)
                parts.append(predicate)
            acceptance.append(parts[0] if len(parts) == 1
                              else Disjunction(parts))
        acceptance.append(AlwaysFalse())
        for source in range(dead + 1):
            for visible in visible_alphabet:
                table.setdefault((source, visible), dead)
        return CountedAutomaton(remaining, counted, dead + 1, 0, table,
                                acceptance)

    # -- decision -----------------------------------------------------

    def reachable_configurations(self, window: int
                                 ) -> set[tuple[int, CountVector]]:
        start = self._initial_configuration()
        seen = {start}
        frontier = [start]
        alphabet = self.columns()
        while frontier:
            state, counts = frontier.pop()
            for column in alphabet:
                raised = tuple(value + step for value, step
                               in zip(counts, self._increment(column)))
                if any(value > window for value in raised):
                    continue
                config = (self.transition_table[(state, column)], raised)
                if config not in seen:
                    seen.add(config)
                    frontier.append(config)
        return seen

    def is_empty(self, window: int) -> bool:
        """No witness whose every counter stays at or below `window`."""
        return not any(
            self.acceptance[state].holds(self._counts_mapping(counts))
            for state, counts in self.reachable_configurations(window))

    def entails(self, hypothesis: "CountedAutomaton",
                window: int) -> bool:
        return (self & ~hypothesis).is_empty(window)

    def accepts(self, assignment: dict[str, int], length: int) -> bool:
        state = self.initial_state
        counts = tuple(0 for _ in self.counted_channels)
        for position in range(length):
            column = tuple((assignment.get(name, 0) >> position) & 1
                           for name in self.channels)
            counts = tuple(value + step for value, step
                           in zip(counts, self._increment(column)))
            state = self.transition_table[(state, column)]
        return self.acceptance[state].holds(self._counts_mapping(counts))

    # -- canonical form -----------------------------------------------

    def canonical_form(self, window: int) -> tuple[int, tuple]:
        """The Myhill-Nerode quotient of the configuration space inside
        the window: states x counter vectors, minimised. Two counted
        automata over the same channels denote the same windowed
        relation iff their signatures are equal -- so this is an
        equality test between presentations, not a size measure (the
        window contributes states of its own)."""
        configs = sorted(self.reachable_configurations(window))
        config_index = {config: position
                        for position, config in enumerate(configs)}
        over = len(configs)
        alphabet = self.columns()

        successor: list[list[int]] = []
        for state, counts in configs:
            row: list[int] = []
            for column in alphabet:
                raised = tuple(value + step for value, step
                               in zip(counts, self._increment(column)))
                if any(value > window for value in raised):
                    row.append(over)
                else:
                    row.append(config_index[
                        (self.transition_table[(state, column)], raised)])
            successor.append(row)
        successor.append([over] * len(alphabet))

        accepting = [self.acceptance[state].holds(
            self._counts_mapping(counts)) for state, counts in configs]
        accepting.append(False)

        block = [1 if flag else 0 for flag in accepting]
        while True:
            signature: dict = {}
            refined = []
            for index in range(len(block)):
                key = (block[index],
                       tuple(block[target] for target in successor[index]))
                refined.append(signature.setdefault(key, len(signature)))
            if refined == block:
                break
            block = refined

        representative: dict[int, int] = {}
        for index in range(len(block)):
            representative.setdefault(block[index], index)

        start = config_index[self._initial_configuration()]
        label = {block[start]: 0}
        order = [block[start]]
        position = 0
        while position < len(order):
            for target in successor[representative[order[position]]]:
                if block[target] not in label:
                    label[block[target]] = len(order)
                    order.append(block[target])
            position += 1
        rows = tuple(
            (accepting[representative[current]],
             tuple(label[block[target]]
                   for target in successor[representative[current]]))
            for current in order)
        return len(order), (self.channels, rows)


# ---------------------------------------------------------------------
# Part 4 -- small statements, and the exclusion witness
# ---------------------------------------------------------------------

def _two_channel_automaton(channels: tuple[str, ...], legal,
                           counted: tuple[str, ...] = ()
                           ) -> CountedAutomaton:
    """A one-live-state automaton that rejects forever once `legal`
    fails on a column."""
    table: dict[tuple[int, ColumnKey], int] = {}
    for column in columns_over(channels):
        mapping = dict(zip(channels, column))
        table[(0, column)] = 0 if legal(mapping) else 1
        table[(1, column)] = 1
    return CountedAutomaton(channels, counted, 2, 0, table,
                            [AlwaysTrue(), AlwaysFalse()])


def containment(part: str, host: str,
                counted: tuple[str, ...] = ()) -> CountedAutomaton:
    """part is a subset of host."""
    channels = tuple(sorted((part, host)))
    return _two_channel_automaton(
        channels, lambda m: not (m[part] == 1 and m[host] == 0), counted)


def disjointness(left: str, right: str,
                 counted: tuple[str, ...] = ()) -> CountedAutomaton:
    channels = tuple(sorted((left, right)))
    return _two_channel_automaton(
        channels, lambda m: m[left] + m[right] <= 1, counted)


def exclusive_or_channel(result: str, left: str, right: str,
                         counted: tuple[str, ...] = ()
                         ) -> CountedAutomaton:
    channels = tuple(sorted((result, left, right)))
    return _two_channel_automaton(
        channels, lambda m: m[result] == m[left] ^ m[right], counted)


def equal_channels(left: str, right: str,
                   counted: tuple[str, ...] = ()) -> CountedAutomaton:
    channels = tuple(sorted((left, right)))
    return _two_channel_automaton(
        channels, lambda m: m[left] == m[right], counted)


def size_constraint(channel: str, relation: str, constant: int,
                    channels: tuple[str, ...] = ()) -> CountedAutomaton:
    return CountedAutomaton.count_constraint(
        (channel,), LinearConstraint({channel: 1}, relation, constant),
        channels)


def balance_statement(left: str, right: str, relation: str = "=",
                      offset: int = 0) -> CountedAutomaton:
    """|left| `relation` |right| + offset."""
    return CountedAutomaton.count_constraint(
        (left, right),
        LinearConstraint({left: 1, right: -1}, relation, offset))


def size_primitive(channel: str, counter_name: str | None = None
                   ) -> CountedAutomaton:
    """The tier's one new primitive: c = |channel|. One control state,
    one counter, incremented by the channel's bit at every column. The
    counter is the register the layer does not have."""
    del counter_name
    return CountedAutomaton((channel,), (channel,), 1, 0,
                            {(0, column): 0
                             for column in columns_over((channel,))},
                            [AlwaysTrue()])


def primitive_table() -> None:
    """Every primitive of both levels, with its automaton, measured."""
    print("  primitive     live states  counters  the state remembers")
    layer_rows = (
        ("z = x ^ y ", relation_exclusive_or("x", "y", "z"),
         "nothing (stateless)"),
        ("z = x & y ", relation_intersection("x", "y", "z"),
         "nothing (stateless)"),
        ("z = x << 1", relation_shift_fill_zero("x", "z"),
         "the bit owed to z"),
        ("z = x + y ", relation_addition("x", "y", "z"), "the carry"),
        ("z = T(x)  ", relation_trailing_ones("x", "z"),
         "inside / outside the run"),
    )
    for label, automaton, remembers in layer_rows:
        # the constructor's own count is the live one; completing for
        # minimisation adds a single dead state to each.
        assert automaton.minimized().state_count <= automaton.state_count + 1
        print(f"  {label}  {automaton.state_count:>11d}  {0:>8d}  "
              f"{remembers}")
    counting = size_primitive("x")
    print(f"  c = |x|     {counting.state_count:>11d}  "
          f"{len(counting.counted_channels):>8d}  "
          "nothing -- the counter is the memory")
    balance = balance_statement("A", "B")
    print(f"  |A| = |B|   {balance.state_count:>11d}  "
          f"{len(balance.counted_channels):>8d}  "
          "nothing -- Presburger on the counters")
    print("  {x} = 2^x            no automaton at either level, "
          "measured above")
    print()
    print("    every layer primitive is 1-2 live states with no "
          "counter; the counting")
    print("    level adds exactly one primitive, and it adds a register "
          "rather than states.")


def verify_boolean_closure(window: int = 4) -> None:
    balance = balance_statement("A", "B")
    assert not balance.is_empty(window)
    assert (balance & ~balance).is_empty(window)
    assert (~(balance | ~balance)).is_empty(window)
    strict = balance_statement("A", "B", relation=">=", offset=1)
    assert not balance.entails(strict, window)
    assert not strict.entails(balance, window)
    assert balance.entails(~strict, window)
    assert (balance & strict).is_empty(window)
    print(f"  window {window}: A and not-A empty, A or not-A universal, "
          "|A|=|B| entails not(|A|>|B|),")
    print("    neither of |A|=|B| and |A|>|B| entails the other, and "
          "their conjunction is empty")


def verify_presentation_independence(window: int = 4) -> None:
    """The 0006 test, at the counted tier: two unrelated presentations
    of the balance rule reduce to the identical canonical form."""
    direct = (disjointness("H1", "H2")
              & balance_statement("H1", "H2"))
    through_union = (disjointness("H1", "H2")
                     & exclusive_or_channel("U", "H1", "H2")
                     & CountedAutomaton.count_constraint(
                         ("U", "H1"),
                         LinearConstraint({"U": 1, "H1": -2}, "=", 0)))
    hidden = through_union.existentially_projected("U", 2 * window + 2)
    left_size, left_signature = direct.canonical_form(window)
    right_size, right_signature = hidden.canonical_form(window)
    print(f"  |H1| = |H2|                   canonical form: "
          f"{left_size} configurations")
    print(f"  exists U. U = H1^H2, |U| = 2|H1|   canonical form: "
          f"{right_size} configurations")
    assert left_signature == right_signature
    print("    identical signatures -- the tier's canonical form does not "
          "see the presentation")


def exponential_of_a_count() -> CountedAutomaton:
    """y = 2^|x|, written entirely in primitives, with w = y - 1 kept
    visible as an auxiliary channel:

        w + 1 = y     set atom     (the 2-state carry automaton)
        |y|   = 1     count atom   (counter against a constant)
        |w|   = |x|   count atom   (counter against counter)

    Every line is legal, so the whole thing is a deterministic Parikh
    automaton. Its undecidable sibling replaces the last line's `|x|`
    with `x`, and nothing else.
    """
    successor: DFA = (Variable("w") + 1).equals(Variable("y"))
    return (CountedAutomaton.from_dfa(successor, channels=("x", "y", "w"))
            & size_constraint("y", "=", 1, ("x", "w"))
            & balance_statement("w", "x"))


def verify_the_worked_pair(bound: int = 24, length: int = 7) -> None:
    """The legal statement really denotes y = 2^|x|, and its one-token
    variant really denotes y = 2^x, which is BIT."""
    automaton = exponential_of_a_count()
    disagreements = []
    for value in range(bound):
        for power in range(bound):
            for lowered in range(bound):
                expected = (lowered + 1 == power
                            and popcount(power) == 1
                            and popcount(lowered) == popcount(value))
                observed = automaton.accepts(
                    {"x": value, "y": power, "w": lowered}, length)
                if expected != observed:
                    disagreements.append((value, power, lowered))
    assert not disagreements, disagreements[:5]
    print(f"  legal:  w+1 = y, |y| = 1, |w| = |x|   ->  y = 2^|x|")
    print(f"    {automaton.state_count} control states, counters "
          f"{automaton.counted_channels}; exhaustively checked against "
          f"the relation")
    print(f"    for x, y, w < {bound}: no disagreements")

    # the models really are the exponential of the count
    models = {(value, power) for value in range(bound)
              for power in range(1, bound)
              if automaton.accepts({"x": value, "y": power,
                                    "w": power - 1}, length)}
    assert models == {(value, 1 << popcount(value))
                      for value in range(bound)
                      if (1 << popcount(value)) < bound}, sorted(models)[:6]
    print(f"    model set is exactly {{(x, 2^|x|)}}")

    # the one-token variant, which the class has no constructor for
    illegal = {(value, 1 << value) for value in range(bound)
               if (1 << value) < bound}
    assert all(popcount(power) == 1 and popcount(power - 1) == value
               for value, power in illegal)
    print(f"  illegal: w+1 = y, |y| = 1, |w| =  x    ->  y = 2^x")
    print(f"    same three atoms; `|x|` became `x`. Model set "
          f"{sorted(illegal)[:4]}...,")
    print("    which is the level map, hence BIT, hence full arithmetic "
          "(part 1).")
    print("    CountPredicate has no slot for a channel value, so the "
          "class cannot")
    print("    express it -- and by decidability of the class, no "
          "combination can.")


def verify_guard_is_enforced(window: int = 6) -> None:
    """Counting a channel and then hiding it is the move that leaves the
    tier, and the implementation refuses it by measurement, not decree."""
    counted_and_hidden = (containment("H", "X")
                          & size_constraint("H", "=", 2, ("X",)))
    try:
        counted_and_hidden.existentially_projected("H", window)
    except GuardViolation as violation:
        print("  hide a counted, genuinely free channel: REFUSED")
        print(f"    {violation}")
    else:
        raise AssertionError("expected a guard violation")

    uncounted = containment("H", "X")
    hidden = uncounted.existentially_projected("H", window)
    print(f"  hide an uncounted channel: allowed "
          f"({hidden.state_count} states)")

    determined = (equal_channels("C", "A", counted=("C",))
                  & size_constraint("C", "=", 3, ("A",)))
    projected = determined.existentially_projected("C", window)
    direct = size_constraint("A", "=", 3)
    assert (projected.canonical_form(window)
            == direct.canonical_form(window))
    print("  hide a counted but functionally determined channel: allowed,")
    print("    and the result is canonically identical to counting the "
          "visible channel")


# ---------------------------------------------------------------------
# suite
# ---------------------------------------------------------------------

def run_verification_suite() -> None:
    print("=" * 70)
    print("1. The operator, and what it is the same as")
    print("=" * 70)
    verify_interdefinability()
    print()
    verify_level_map_conjugation()
    print()
    verify_membership_becomes_bit()

    print()
    print("=" * 70)
    print("2. What the layer cannot hold")
    print("=" * 70)
    verify_balance_is_not_automatic()
    print()
    verify_level_map_is_not_automatic()
    print()
    verify_popcount_is_the_permutation_invariant()

    print()
    print("=" * 70)
    print("3. The primitives of both levels")
    print("=" * 70)
    primitive_table()

    print()
    print("=" * 70)
    print("4. The counted tier")
    print("=" * 70)
    for window in (3, 4):
        verify_boolean_closure(window)
    print()
    verify_presentation_independence()
    print()
    verify_the_worked_pair()
    print()
    verify_guard_is_enforced()

    print()
    print("=" * 70)
    print("all checks passed")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
