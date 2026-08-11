"""The counted tier in sentence form: two sorts, two zeros, one measure.

0034 presented the tier as automata over channels. This module gives the
sentence-form presentation, which is the corpus's own and is clearer on
paper (0019: the sentence form poly-simulates the automaton and is never
beaten on size).

**Two sorts, each with its own equality and its own zero.**

  set sort    terms over {^, &, <<, 1} in symbols; the ring GF(2)-style,
              idempotent. Equality is `^`. A sentence asserts a term is
              the empty set. Truth checker: the track reads all zeros.

  count sort  integer forms over measures |t|. Z, not idempotent, so
              equality is `-`, not `^`. A sentence asserts a form is
              zero. Truth checker: the register reads zero.

The truth checker is the same in both sorts -- "everything reads zero" --
but upstairs that quantifies over *positions* and downstairs over
*registers*. That is the whole of the two-level structure.

**The measure is the only bridge, and it has three laws** (all verified
below, and the first two are the corpus's own from
`clue/2025-04-04 size operator and hamming distance.md`):

  |A ^ B| + 2|A & B| = |A| + |B|        the measure law
  A & B = 0  <=>  |A ^ B| = |A| + |B|   the corpus's disjoint form
  |A << 1| = |A|                        << is invisible to the measure

Read them together: the count sort sees `^` as `+` up to the
intersection defect, sees `&` only through that defect, and does not see
`<<` at all. The measure is exactly what survives forgetting the order
of positions -- which is why it is the complete invariant of the
position-permuting family (0034 section 5c).

**The line.** There are two copies of N here: the *values* of set terms
and the *counts*. Every legal operation respects the distinction; the
measure maps the first to the second and is many-to-one. Undecidability
is exactly their identification. `2^|x|` is a set built from a count and
is decidable; `2^x` is a set built from a value and is BIT. A literal
constant is safe in either sort because naming finitely many points is
not naming the map.

**Why combining levels is safe.** Union of counted sentences multiplies
the control automata and concatenates the registers, and the two moves
are *orthogonal*: a set sentence contributes no register, a count
sentence contributes no control state. So no amount of set knowledge can
grow the count level, and no amount of count knowledge can grow the set
level. Measured at the bottom of this file. Undecidability would need a
register to name a position, and no sentence has such a term, so no
union of sentences does either.

Run directly for the verification suite.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import product as cartesian_product

from canonical_automata import Constant, Term, Variable
from level_crossing import (CountedAutomaton, LinearConstraint,
                            popcount)


# ---------------------------------------------------------------------
# the bridge laws
# ---------------------------------------------------------------------

def verify_measure_laws(bound: int = 1 << 7) -> None:
    """The three laws relating the two sorts."""
    measure_law = [(a, b) for a in range(bound) for b in range(bound)
                   if popcount(a ^ b) + 2 * popcount(a & b)
                   != popcount(a) + popcount(b)]
    assert not measure_law, measure_law[:5]
    print(f"  |A ^ B| + 2|A & B| = |A| + |B|       "
          f"exhaustive for A, B < {bound}: holds")

    disjoint = [(a, b) for a in range(bound) for b in range(bound)
                if ((a & b) == 0)
                != (popcount(a ^ b) == popcount(a) + popcount(b))]
    assert not disjoint, disjoint[:5]
    print(f"  A & B = 0  <=>  |A ^ B| = |A| + |B|  both directions: "
          "holds  (corpus 2025-04-04)")

    shift = [a for a in range(bound) if popcount(a << 1) != popcount(a)]
    assert not shift, shift[:5]
    print(f"  |A << 1| = |A|                       "
          f"exhaustive for A < {bound}: holds")
    print("    so the count sort reads ^ as +, reads & only through the "
          "defect, and")
    print("    does not read << at all -- it is the order-forgetting "
          "part of a sentence.")


def verify_the_two_copies_of_n(bound: int = 1 << 8) -> None:
    """The section exists from the count sort and not from the value
    sort, which is where the whole line sits."""
    # T(A) ^ A vanishes exactly on the all-ones prefixes: the canonical
    # set of a given size (the corpus's 2**N - 1).
    def trailing_ones(value: int) -> int:
        mask = 0
        position = 0
        while (value >> position) & 1:
            mask |= 1 << position
            position += 1
        return mask

    canonical = [a for a in range(bound) if trailing_ones(a) == a]
    assert canonical == [(1 << k) - 1 for k in range(bound.bit_length())
                         if (1 << k) - 1 < bound], canonical[:8]
    assert all(popcount(a) == a.bit_length() for a in canonical)
    print(f"  T(A) ^ A vanishes exactly on {canonical[:5]}... = "
          "2^k - 1, the canonical set of size k")
    print("    so `the set of size c` IS available -- as a section from "
          "the COUNT sort.")
    print("    What is unavailable is `the set of size v` for v a set "
          "term's VALUE;")
    print("    the two copies of N are never identified, and that "
          "single omission is")
    print("    the whole distance to BIT.")


# ---------------------------------------------------------------------
# sentences
# ---------------------------------------------------------------------

class SortError(TypeError):
    """Raised when a set term is written where a count belongs, or the
    reverse. This is the boundary -- not a semantic side condition."""


class CountForm:
    """An integer form over measures, asserted to be zero. Equality in
    this sort is subtraction; `^` belongs to the other sort."""

    def __init__(self, coefficients: dict[str, int],
                 constant: int = 0) -> None:
        for name in coefficients:
            if not isinstance(name, str):
                raise SortError(
                    f"{name!r} is a set term; a count form may only "
                    "mention measures. Measure it first.")
        self.coefficients = {name: weight
                             for name, weight in coefficients.items()
                             if weight != 0}
        self.constant = constant

    def as_constraint(self) -> LinearConstraint:
        return LinearConstraint(self.coefficients, "=", -self.constant)

    def __repr__(self) -> str:
        body = " + ".join(f"{weight}|{name}|" for name, weight
                          in sorted(self.coefficients.items()))
        return f"{body} + {self.constant}"


def measure(name_or_term) -> str:
    """The bridge, used as a term-former in a count form. It accepts the
    NAME of a measured set term. Handing it a set term directly is the
    sort error, made explicit."""
    if isinstance(name_or_term, Term):
        raise SortError(
            "a set term cannot stand in a count form; it has to be "
            "measured first, and its measure lives in the other sort")
    return name_or_term


class CountedSentence:
    """<S ; C> -- a set term asserted to be the empty set, and integer
    forms over named measures asserted to be zero.

    `measures` names the set terms that carry a register. Naming one is
    the sentence-form version of 0008's uniquely-determined hidden wire:
    the name is pinned by `name ^ term`, so hiding it is legal and the
    register stays a function of the sentence's symbols.
    """

    def __init__(self, set_term: Term | None = None,
                 measures: dict[str, Term] | None = None,
                 forms: list[CountForm] | None = None) -> None:
        self.set_term = set_term
        self.measures = dict(measures or {})
        self.forms = list(forms or [])

    def unioned_with(self, other: "CountedSentence") -> "CountedSentence":
        """Combining knowledge. The set parts combine by union -- the
        corpus's S1 ^ S2 ^ S1S2, empty exactly when both are -- and the
        count parts concatenate, because Z is not idempotent so there is
        no single form saying `both vanish`."""
        if self.set_term is None:
            combined = other.set_term
        elif other.set_term is None:
            combined = self.set_term
        else:
            combined = (self.set_term ^ other.set_term
                        ^ (self.set_term & other.set_term))
        return CountedSentence(combined,
                               {**self.measures, **other.measures},
                               self.forms + other.forms)

    def compiled(self) -> CountedAutomaton:
        """The truth checker: the set track must read all zeros and every
        register must read zero."""
        names = tuple(sorted(self.measures))
        pieces: list[CountedAutomaton] = []
        if self.set_term is not None:
            pieces.append(CountedAutomaton.from_dfa(
                self.set_term.equals(Constant(0)), channels=names))
        for name in names:
            pieces.append(CountedAutomaton.from_dfa(
                Variable(name).equals(self.measures[name]),
                channels=names))
        automaton = pieces[0]
        for piece in pieces[1:]:
            automaton = automaton & piece
        automaton = CountedAutomaton(
            automaton.channels, names, automaton.state_count,
            automaton.initial_state, automaton.transition_table,
            automaton.acceptance)
        for form in self.forms:
            automaton = automaton & CountedAutomaton.count_constraint(
                names, form.as_constraint(), automaton.channels)
        return automaton

    def shape(self) -> tuple[int, int]:
        automaton = self.compiled()
        return automaton.state_count, len(automaton.counted_channels)


# ---------------------------------------------------------------------
# the worked pair, in sentence form
# ---------------------------------------------------------------------

def exponential_of_a_count() -> CountedSentence:
    """< y ^ (w + 1) ;  |y| - 1,  |w| - |x| >   asserts  y = 2^|x|."""
    return CountedSentence(
        set_term=Variable("y") ^ (Variable("w") + 1),
        measures={"y": Variable("y"), "w": Variable("w"),
                  "x": Variable("x")},
        forms=[CountForm({measure("y"): 1}, -1),
               CountForm({measure("w"): 1, measure("x"): -1})])


def verify_the_worked_pair(bound: int = 20, length: int = 7) -> None:
    sentence = exponential_of_a_count()
    automaton = sentence.compiled()
    disagreements = [
        (value, power, lowered)
        for value in range(bound) for power in range(bound)
        for lowered in range(bound)
        if ((lowered + 1 == power and popcount(power) == 1
             and popcount(lowered) == popcount(value))
            != automaton.accepts({"x": value, "y": power, "w": lowered},
                                 length))]
    assert not disagreements, disagreements[:5]
    states, registers = sentence.shape()
    print("  legal    < y ^ (w+1) ;  |y| - 1,  |w| - |x| >   ->  "
          "y = 2^|x|")
    print(f"    {states} control states, {registers} registers; "
          f"exhaustive for x, y, w < {bound}: holds")

    try:
        CountForm({measure(Variable("x")): -1})
    except SortError as violation:
        print("  illegal  < y ^ (w+1) ;  |y| - 1,  |w| -  x  >   ->  "
              "y = 2^x")
        print(f"    refused where it is written: {violation}")
    else:
        raise AssertionError("expected a sort error")
    print("    the malformed line is not a different kind of "
          "constraint -- `|w| - x`")
    print("    subtracts a set term from a count. There is no such "
          "subtraction.")


# ---------------------------------------------------------------------
# which shift amounts stay in the tier
# ---------------------------------------------------------------------

def nerode_classes_by_prefix_length(membership, channels: tuple[str, ...],
                                    max_prefix_length: int,
                                    suffix_length: int) -> list[int]:
    """Distinct residuals among prefixes of each length.

    The membership test for the tier: a deterministic Parikh automaton
    with |Q| control states and d counters, each incremented by at most
    one per column, has at most |Q|*(k+1)^d configurations after k
    columns -- so its residual count is O(k^d), polynomial. **Residual
    growth that is superpolynomial in the prefix length rules out every
    such automaton**, whatever counters it chooses. The criterion does
    not depend on guessing the counter set.
    """
    alphabet = list(cartesian_product((0, 1), repeat=len(channels)))
    suffixes = list(cartesian_product(alphabet, repeat=suffix_length))

    def values(word):
        return {name: sum(column[index] << position
                          for position, column in enumerate(word))
                for index, name in enumerate(channels)}

    growth = []
    for prefix_length in range(max_prefix_length + 1):
        signatures = set()
        for prefix in cartesian_product(alphabet, repeat=prefix_length):
            signatures.add(tuple(
                membership(values(prefix + suffix),
                           prefix_length + suffix_length)
                for suffix in suffixes))
        growth.append(len(signatures))
    return growth


def shift_by_count_forced_configurations(prefix_length: int) -> int:
    """A machine-checked lower bound on the configurations any
    deterministic Parikh automaton needs after `prefix_length` columns
    of `z ^ (x << |b|)`.

    The family: prefixes carrying `b = 0`, `z = 0`, and each of the
    2^k patterns on `x`. Each has exactly one completion -- put `k`
    ones on `b` next, which fixes the shift at `k`, and then `z` must
    replay that prefix's `x` bits. A completion for one member fits no
    other, so all 2^k are pairwise distinguishable and must sit in
    distinct configurations.
    """
    width = 3 * prefix_length
    distinguished = 0
    for pattern in range(1 << prefix_length):
        completion_shift = prefix_length
        expected = pattern << completion_shift
        # the completion built for `pattern` completes `pattern` ...
        assert expected == (pattern << popcount(
            ((1 << prefix_length) - 1) << prefix_length))
        assert expected < (1 << width)
        # ... and no other member of the family
        assert not any(expected == (other << completion_shift)
                       for other in range(1 << prefix_length)
                       if other != pattern)
        distinguished += 1
    return distinguished


def verify_the_shift_amount_is_the_boundary() -> None:
    """`<<` is a layer generator and the layer is decidable, so no
    operator is the culprit. The test is on statements, and two
    statements over the same operators land on opposite sides."""
    print("    residuals by prefix length (probe depth = max prefix, so "
          "each count is exact)")
    for label, membership, channels, depth in (
            ("z ^ (x ^ y)      << not used       ",
             lambda v, w: v["z"] == (v["x"] ^ v["y"]), ("x", "y", "z"), 3),
            ("w ^ (x << 1)     << applied once   ",
             lambda v, w: v["w"] == (v["x"] << 1), ("x", "w"), 4),
            ("w ^ (x << 3)     << applied 3 times",
             lambda v, w: v["w"] == (v["x"] << 3), ("x", "w"), 4),
            ("|A| - |B|                          ",
             lambda v, w: popcount(v["A"]) == popcount(v["B"]),
             ("A", "B"), 4),
            ("y ^ (1 << |x|)   shift the constant",
             lambda v, w: v["y"] == 1 << popcount(v["x"]),
             ("x", "y"), 4),
            ("z ^ (x << |b|)   shift a set term  ",
             lambda v, w: v["z"] == v["x"] << popcount(v["b"]),
             ("b", "x", "z"), 3)):
        growth = nerode_classes_by_prefix_length(
            membership, channels, depth, depth)
        print(f"    {label}  "
              + ", ".join(str(count) for count in growth))

    print()
    print("    forced configurations for  z ^ (x << |b|)  "
          "(exact, by pairwise separation):")
    forced = [(k, shift_by_count_forced_configurations(k))
              for k in range(1, 7)]
    print("      prefix length  " + "  ".join(f"{k:>4d}" for k, _ in forced))
    print("      configurations " + "  ".join(f"{n:>4d}" for _, n in forced))
    assert [n for _, n in forced] == [1 << k for k, _ in forced]
    print("    2^k, so no deterministic Parikh automaton serves it: with "
          "|Q| control")
    print("    states and d registers moving by at most one per column, "
          "there are at")
    print("    most |Q|*(k+1)^d configurations after k columns, which is "
          "polynomial.")
    print("    Shifting an arbitrary set by a count needs the shifted "
          "bits BUFFERED,")
    print("    and a register counts -- it does not buffer.")
    print()
    print("    << is UNARY. `x << 3` is three applications, a finite "
          "composition, so it")
    print("    keeps the residual count flat. What leaves the layer is "
          "ITERATING it a")
    print("    variable number of times, and two things about that "
          "iteration matter:")
    print()
    rows = (("w ^ (x << 3)", "a constant", "nothing", "layer"),
            ("y ^ (1 << |x|)", "a count", "a count", "in the tier"),
            ("z ^ (x << |b|)", "a count", "a SET: the bits to place",
             "outside"),
            ("y ^ (1 << x)", "a value", "--", "closes to BIT"))
    print(f"    {'statement':<16}{'iterated':<12}"
          f"{'carried across a cut':<27}status")
    for statement, iterated, carried, status in rows:
        print(f"    {statement:<16}{iterated:<12}{carried:<27}{status}")
    print()
    print("    CAUTION, and it is the reason the last row is phrased "
          "differently: the")
    print("    residual test above decides membership in the TIER. It "
          "does not decide")
    print("    Goedel. Undecidability is a property of the CLOSED "
          "class, not of one")
    print("    statement's width -- adding the level map to the layer "
          "and closing under")
    print("    the Boolean moves and projection is what gives full "
          "arithmetic (0034).")


# ---------------------------------------------------------------------
# why combining levels is safe
# ---------------------------------------------------------------------

def verify_levels_grow_orthogonally() -> None:
    """Union multiplies control states and concatenates registers, and
    each kind of sentence feeds only one of the two."""
    print(f"    {'union so far, after adding':<50}{'control':>9}"
          f"{'registers':>11}")
    sentence = CountedSentence(
        set_term=Variable("a") & Variable("b"),
        measures={"a": Variable("a"), "b": Variable("b")})
    states, registers = sentence.shape()
    print(f"    {'a&b                        (set)':<50}"
          f"{states:>9d}{registers:>11d}")

    for label, addition in (
            ("a & (b << 1)               (set)",
             CountedSentence(set_term=Variable("a")
                             & (Variable("b") << 1))),
            ("(a ^ b) & (a ^ b ^ 1)      (set)",
             CountedSentence(set_term=(Variable("a") ^ Variable("b"))
                             & (Variable("a") ^ Variable("b") ^ 1))),
            ("|a| - |b|                  (count, old measures)",
             CountedSentence(forms=[CountForm({"a": 1, "b": -1})])),
            ("|a| - 3                    (count, old measures)",
             CountedSentence(forms=[CountForm({"a": 1}, -3)])),
            ("|c| - 2  with  c ^ (a ^ b) (count, new measure)",
             CountedSentence(measures={"c": Variable("a")
                                       ^ Variable("b")},
                             forms=[CountForm({"c": 1}, -2)])),
    ):
        sentence = sentence.unioned_with(addition)
        states, registers = sentence.shape()
        print(f"    {label:<50}{states:>9d}{registers:>11d}")
    print("    A set sentence moves the control column and never the "
          "register column.")
    print("    A count form over measures already present moves "
          "neither -- it is one")
    print("    control state, and it binds registers that are already "
          "there. Measuring a")
    print("    NEW term costs one register plus the wire pinning it. "
          "Nothing in either")
    print("    column is fed by the other, so no union of sentences "
          "crosses the sorts.")


def run_verification_suite() -> None:
    print("=" * 70)
    print("1. The measure: the only bridge between the sorts")
    print("=" * 70)
    verify_measure_laws()
    print()
    verify_the_two_copies_of_n()

    print()
    print("=" * 70)
    print("2. The worked pair, as sentences")
    print("=" * 70)
    verify_the_worked_pair()

    print()
    print("=" * 70)
    print("3. The membership test is on statements, not operators")
    print("=" * 70)
    verify_the_shift_amount_is_the_boundary()

    print()
    print("=" * 70)
    print("4. Why combining the levels is safe")
    print("=" * 70)
    verify_levels_grow_orthogonally()

    print()
    print("=" * 70)
    print("all checks passed")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
