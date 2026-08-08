"""Flip is NOT irreducible: negation is worth exactly one relation.

0014 left this open -- can the flip move always be traded for
relations in the signature, or is something about negation genuinely
irreducible? Answer: it can always be traded, and the exchange rate
is one relation. Precisely:

    pp-closure( &, <<, constants )        is NOT everything
                                          (0013: intersection is a
                                           polymorphism, so ^ escapes)
    pp-closure( &, ^, <<, 0, 1 )         IS everything
    FO-closure( &, <<, constants )       IS everything

Holding {&, <<, constants} fixed, adding ^ to the signature buys
exactly what adding flip to the logic buys. **XOR and negation are
interchangeable**: the corpus's decision to carry ^ as an operator was
not a redundancy, it was paying for negation up front.

The construction: every automatic relation is pp-defined by carrying
the target automaton's RUN in hidden channels.

    H    an all-ones prefix ("horizon") containing every input bit
    HL   = (H << 1) ^ 1, one position longer
    Q_p  one track per state, marking positions where the run sits
         in state p

All constraints are local, hence conjunctive:

    H, HL are all-ones prefixes; every input sits inside H
    the Q_p partition HL
    position 0 lies in Q_initial
    (Q_p & H & input-pattern) << 1  sits inside Q_delta(p, pattern)
    the position just above H lies in a state that accepts padding

Relative complement inside HL is HL ^ (HL & v), which is why the
input-pattern match needs no negation -- and is exactly where the ^
in the signature earns its keep.

Every construction below uses ONLY conjunction (share) and existential
projection (hide). This is enforced, not merely intended: during the
whole run, DFA.complemented is replaced by a function that raises.

Run this file directly.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_automata import (
    DFA, Variable, relation_intersection, relation_exclusive_or,
    relation_shift_fill_zero, relation_constant, relation_equality)


class FreshChannelSource:
    def __init__(self) -> None:
        self.count: int = 0

    def fresh(self, tag: str = "t") -> str:
        self.count += 1
        return f"_{tag}{self.count}"


CHANNELS = FreshChannelSource()


def conjoin(*parts: DFA) -> DFA:
    combined: DFA = parts[0]
    for part in parts[1:]:
        combined = combined.intersected_with(part).minimized()
    return combined


def closed_over(parts: list[DFA], temporaries: list[str]) -> DFA:
    """Conjoin, then immediately hide the temporary channels, so only
    persistent channels stay alive."""
    combined: DFA = conjoin(*parts)
    live = [name for name in temporaries
            if name in combined.variable_names]
    return combined.exists(*live).minimized() if live else combined


# --- gadgets: share and hide over {&, ^, <<, 0, 1} -------------------

def gadget_subset(inner: str, outer: str) -> DFA:
    meet = CHANNELS.fresh()
    return closed_over([relation_intersection(inner, outer, meet),
                        relation_equality(meet, inner)], [meet])


def gadget_disjoint(left: str, right: str) -> DFA:
    meet, zero = CHANNELS.fresh(), CHANNELS.fresh()
    return closed_over([relation_intersection(left, right, meet),
                        relation_constant(zero, 0),
                        relation_equality(meet, zero)], [meet, zero])


def gadget_union(left: str, right: str, result: str) -> DFA:
    meet, difference = CHANNELS.fresh(), CHANNELS.fresh()
    return closed_over(
        [relation_intersection(left, right, meet),
         relation_exclusive_or(left, right, difference),
         relation_exclusive_or(difference, meet, result)],
        [meet, difference])


def gadget_horizons(horizon: str, horizon_long: str) -> DFA:
    """horizon_long = (horizon << 1) ^ 1, with horizon an all-ones
    prefix (equivalently, horizon sits inside horizon_long)."""
    shifted, one = CHANNELS.fresh(), CHANNELS.fresh()
    return closed_over(
        [relation_shift_fill_zero(horizon, shifted),
         relation_constant(one, 1),
         relation_exclusive_or(shifted, one, horizon_long),
         gadget_subset(horizon, horizon_long)], [shifted, one])


def gadget_initial(track: str) -> DFA:
    one = CHANNELS.fresh()
    return closed_over([relation_constant(one, 1),
                        gadget_subset(one, track)], [one])


def gadget_transition(source_track: str, target_track: str,
                      horizon: str, horizon_long: str,
                      input_names: list[str], column: dict[str, int],
                      is_dead: bool) -> DFA:
    """(source & horizon & matching-pattern) << 1 sits inside the
    target track."""
    parts: list[DFA] = []
    temporaries: list[str] = []
    selector = CHANNELS.fresh()
    parts.append(relation_intersection(source_track, horizon, selector))
    temporaries.append(selector)
    current = selector
    for name in input_names:
        refined = CHANNELS.fresh()
        temporaries.append(refined)
        if column[name] == 1:
            parts.append(relation_intersection(current, name, refined))
        else:
            complement, meet = CHANNELS.fresh(), CHANNELS.fresh()
            temporaries += [complement, meet]
            parts.append(relation_intersection(horizon_long, name, meet))
            parts.append(relation_exclusive_or(horizon_long, meet,
                                               complement))
            parts.append(relation_intersection(current, complement,
                                               refined))
        current = refined
    moved = CHANNELS.fresh()
    temporaries.append(moved)
    parts.append(relation_shift_fill_zero(current, moved))
    if is_dead:
        zero = CHANNELS.fresh()
        temporaries.append(zero)
        parts += [relation_constant(zero, 0),
                  relation_equality(moved, zero)]
    else:
        parts.append(gadget_subset(moved, target_track))
    return closed_over(parts, temporaries)


def gadget_accepting_top(horizon: str, horizon_long: str,
                         good_tracks: list[str]) -> DFA:
    """The single position just above the horizon lies in a state that
    accepts the all-zero padding."""
    top, meet = CHANNELS.fresh(), CHANNELS.fresh()
    parts: list[DFA] = [
        relation_intersection(horizon_long, horizon, meet),
        relation_exclusive_or(horizon_long, meet, top)]
    temporaries: list[str] = [top, meet]
    running = good_tracks[0]
    for track in good_tracks[1:]:
        accumulator = CHANNELS.fresh()
        temporaries.append(accumulator)
        parts.append(gadget_union(running, track, accumulator))
        running = accumulator
    parts.append(gadget_subset(top, running))
    return closed_over(parts, temporaries)


def states_accepting_padding(target: DFA) -> set[int]:
    """States from which reading all-zero columns reaches acceptance."""
    zero_column = {name: 0 for name in target.variable_names}
    good: set[int] = set()
    for state in range(target.state_count):
        visited: set[int] = set()
        current: int | None = state
        while current is not None and current not in visited:
            if current in target.accepting_states:
                good.add(state)
                break
            visited.add(current)
            current = target.transition_target(current, zero_column)
    return good


def positive_definition_of(target: DFA) -> DFA:
    """Rebuild any automatic relation with share and hide only."""
    target = target.minimized()
    input_names = list(target.variable_names)
    horizon = CHANNELS.fresh("Horizon")
    horizon_long = CHANNELS.fresh("HorizonLong")
    tracks = [CHANNELS.fresh(f"State{index}")
              for index in range(target.state_count)]
    accumulators: list[str] = []

    formula = gadget_horizons(horizon, horizon_long)
    for name in input_names:
        formula = conjoin(formula, gadget_subset(name, horizon))
    for index, track in enumerate(tracks):
        formula = conjoin(formula, gadget_subset(track, horizon_long))
        for other in tracks[index + 1:]:
            formula = conjoin(formula, gadget_disjoint(track, other))
    running = tracks[0]
    for track in tracks[1:]:
        accumulator = CHANNELS.fresh()
        accumulators.append(accumulator)
        formula = conjoin(formula,
                          gadget_union(running, track, accumulator))
        running = accumulator
    formula = conjoin(formula,
                      relation_equality(running, horizon_long))
    formula = conjoin(formula,
                      gadget_initial(tracks[target.initial_state]))
    for state in range(target.state_count):
        for column in target.alphabet():
            successor = target.transition_target(state, column)
            formula = conjoin(formula, gadget_transition(
                tracks[state],
                tracks[successor] if successor is not None else tracks[0],
                horizon, horizon_long, input_names, column,
                is_dead=(successor is None)))
    good = sorted(states_accepting_padding(target))
    assert good, "target has no state that accepts padding"
    formula = conjoin(formula, gadget_accepting_top(
        horizon, horizon_long, [tracks[state] for state in good]))
    hidden = [horizon, horizon_long] + tracks + accumulators
    return formula.exists(*[name for name in hidden
                            if name in formula.variable_names])


def nonemptiness_by_hand() -> DFA:
    """The readable special case: x is nonempty, with ONE hidden
    channel and no negation --

        x != 0  <=>  exists q:  q is an all-ones prefix,
                                q misses x,
                                the position just above q is in x

    This is the event the corpus's expression algebra could not state
    (0005 section 1). What it was missing was never negation; it was
    hidden channels.
    """
    prefix, shifted, one = (CHANNELS.fresh(), CHANNELS.fresh(),
                            CHANNELS.fresh())
    long_prefix, top = CHANNELS.fresh(), CHANNELS.fresh()
    parts = [
        relation_shift_fill_zero(prefix, shifted),
        relation_constant(one, 1),
        relation_exclusive_or(shifted, one, long_prefix),
        gadget_subset(prefix, long_prefix),
        relation_exclusive_or(long_prefix, prefix, top),
        gadget_disjoint(prefix, 'x'),
        gadget_subset(top, 'x'),
    ]
    return closed_over(parts, [prefix, shifted, one, long_prefix, top])


# ---------------------------------------------------------------------
# Verification suite, with negation physically disabled
# ---------------------------------------------------------------------

class NegationUsed(Exception):
    pass


def run_verification_suite() -> None:
    x, y, w = Variable('x'), Variable('y'), Variable('w')

    # Targets are built normally (negation allowed HERE -- these are
    # the relations to be reproduced, not the reproductions).
    targets: list[tuple[str, DFA]] = [
        ("x = 0", x.equals(0)),
        ("x != 0", (~x.equals(0)).minimized()),
        ("x is odd", (~(x & 1).equals(0)).minimized()),
        ("x is NOT a power of two",
         (~(((w + 1).equals(x) & (x & w).equals(0)).exists('w'))
          ).minimized()),
        ("x > y", (~x.at_most(y)).minimized()),
    ]

    # From here on, negation is physically unavailable.
    def refuse_negation(self: DFA) -> DFA:
        raise NegationUsed("complement called during a pp construction")

    original_complement = DFA.complemented
    DFA.complemented = refuse_negation
    try:
        by_hand = nonemptiness_by_hand()
        assert by_hand.describes_same_relation_as(
            targets[1][1]), "hand-built nonemptiness failed"
        print(f"  nonemptiness by hand, one hidden channel, no "
              f"negation: verified ({by_hand.state_count} states)")
        for label, target in targets:
            rebuilt = positive_definition_of(target)
            assert rebuilt.describes_same_relation_as(target), label
            print(f"  {label:<26} rebuilt with share + hide only: "
                  f"verified", flush=True)
    finally:
        DFA.complemented = original_complement

    print("""
  Every relation above was rebuilt using conjunction and existential
  projection alone, over the fixed signature {&, ^, <<, 0, 1} -- with
  DFA.complemented replaced by a function that raises, so the absence
  of negation is enforced rather than asserted.

  => flip is not irreducible. Holding {&, <<, constants} fixed,
     ^ in the signature and flip in the logic buy the same thing.""")
    print("all flip-elimination checks passed")


if __name__ == "__main__":
    run_verification_suite()
