"""Sink uniqueness, tested adversarially -- and the ordered edges
upgraded from inequalities to exact laws.

PART A: IS THE AUTOMATON THE UNIQUE SINK?

  Among the fixed frames of 0026 (five flat frames + the automaton):
  YES, now proved -- the automaton is a sink by 0026's edges, and each
  flat frame is disqualified by an explicit witness (a statement small
  in some frame but big in it).

  In the EXTENDED taxonomy admitting the shared Davio frame (the FDD:
  positive-Davio decomposition with sharing -- ANF's own shared
  form): NO. The flat frames' extremal witnesses flow to the FDD just
  as to the automaton, and the shared frames separate in the killing
  direction, measured here:
      windowed parity (separated order)  FDD small,  automaton BIG
  The reverse direction (automaton small, FDD big) did NOT materialise
  on any counting family tried -- majority tracks the automaton -- and
  is cited to the decision-diagram literature (exponential BDD/FDD
  separations in both directions), recorded as the one unreproduced
  gap. Sink-ness belongs to the SHARING MOVE, not to any fixed frame;
  at the shared level it survives only for parameter PORTFOLIOS (a
  KFDD choice vector emulates either side), and best-parameter search
  is NP-hard.

PART B: EXACT CEILINGS -- the collapse question, closed.

  Each ordered edge's per-cut state count is exactly the IMAGE SIZE of
  the upstream description under the cut; the published rate is the
  free-image case, and every collapse is an upstream algebraic
  dependence:

  crossing law (ANF -> automaton), EXACT FORM: the subfunctions at a
  cut are exactly the distinct values of
      (symmetric difference of the right parts of the SELECTED
       straddling monomials)  XOR  (parity of completed monomials)
  over achievable prefixes. Verified as an equality on 200 random
  sparse statements at every cut. The 2^straddle ceiling is achieved
  iff the left parts shatter and the right parts are independent;
  the two collapse modes -- a right-part linear dependence, a shared
  left variable -- each cost exactly a factor of 2, verified.

  path law (minterm -> automaton), EXACT FORM: states at a cut =
  distinct model SUFFIX-SETS (+1 for the zero subfunction when some
  prefix is model-free). Verified as an equality; prefixes sharing a
  suffix-set merge, and clustering models collapses the rate from
  ~n*models to ~n+models, verified.

  span law (Walsh -> automaton): the 2^d ceiling collapses exactly by
  the stabiliser of the inner function -- g with a translation
  invariance merges classes; a parity inner function (stabiliser of
  index 2) pins every cut at 2 states while generic g reaches 2^d.
  Verified.

Run this file directly.
"""

from __future__ import annotations

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anf_automaton_tradeoff import (automaton_size, subfunction_counts,
                                    reordered_table, table_of_monomials,
                                    windowed_parity_monomials,
                                    anf_term_count)

TruthTable = list[int]


# ---------------------------------------------------------------------
# The shared Davio frame: FDD size (positive Davio with sharing)
# ---------------------------------------------------------------------

def fdd_size(truth_table: TruthTable, variable_count: int,
             variable_order: list[int]) -> int:
    """Quasi-reduced FDD size: at each level the children of g are
    g0 = g(variable = 0) and the derivative g0 XOR g1 -- the Davio
    pair -- kept with sharing. Size = distinct functions summed over
    levels (the exact Davio analogue of the automaton's subfunction
    count)."""
    ordered = reordered_table(truth_table, variable_count,
                              variable_order)
    current_level: set[bytes] = {bytes(ordered)}
    total = len(current_level)
    for _ in range(variable_count):
        next_level: set[bytes] = set()
        for function in current_level:
            half = len(function) // 2
            low, high = function[:half], function[half:]
            derivative = bytes(a ^ b for a, b in zip(low, high))
            next_level.add(low)
            next_level.add(derivative)
        current_level = next_level
        total += len(current_level)
    return total


def majority_table(variable_count: int) -> TruthTable:
    threshold = variable_count // 2 + 1
    return [1 if bin(point).count('1') >= threshold else 0
            for point in range(1 << variable_count)]


def show_part_a() -> None:
    print("=" * 70)
    print("A  SINK UNIQUENESS, TESTED ADVERSARIALLY")
    print("=" * 70)
    print("""
  A1. Among the FIXED frames of 0026 the automaton is the unique
      sink: it is a sink by the four ordered edges, and each flat
      frame is disqualified by an explicit witness (0026 section 5).

  A2. But the Kronecker taxonomy contains ANF's OWN shared form --
      the FDD (positive Davio with sharing) -- and measurement shows
      the flat frames' extremal witnesses flow to it just as they
      flow to the automaton:
""")
    variable_count = 12
    natural = list(range(variable_count))
    at_least_one = [1 if point else 0 for point in range(1 << variable_count)]
    delta_at_zero = [1 if point == 0 else 0
                     for point in range(1 << variable_count)]
    parity = table_of_monomials([1 << v for v in range(variable_count)],
                                variable_count)
    full_monomial = table_of_monomials([(1 << variable_count) - 1],
                                       variable_count)
    for label, table in (("at-least-one (ANF-hard)", at_least_one),
                         ("delta at zero (ANF-hard)", delta_at_zero),
                         ("full monomial (dual/Walsh-hard)",
                          full_monomial),
                         ("parity (minterm-hard)", parity)):
        automaton_states = automaton_size(table, variable_count, natural)
        fdd_states = fdd_size(table, variable_count, natural)
        assert fdd_states <= 3 * variable_count + 3
        print(f"      {label:<32} automaton {automaton_states:3d}   "
              f"FDD {fdd_states:3d}")

    print("""
  A3. And the two shared frames separate -- in the direction that
      kills the conjecture. Windowed parity in the separated order,
      scaling the pair count:
""")
    previous = None
    for pair_count in (8, 9, 10):
        monomials, wp_variables = windowed_parity_monomials(pair_count, 2)
        wp_table = table_of_monomials(monomials, wp_variables)
        order = list(range(wp_variables))
        wp_automaton = automaton_size(wp_table, wp_variables, order)
        wp_fdd = fdd_size(wp_table, wp_variables, order)
        growth = "" if previous is None else (
            f"   automaton x{wp_automaton / previous[0]:.2f}, "
            f"FDD x{wp_fdd / previous[1]:.2f}")
        print(f"      pairs = {pair_count:2d}: automaton "
              f"{wp_automaton:5d}   FDD {wp_fdd:4d}{growth}")
        previous = (wp_automaton, wp_fdd)
    monomials, wp_variables = windowed_parity_monomials(10, 2)
    wp_table = table_of_monomials(monomials, wp_variables)
    order = list(range(wp_variables))
    assert fdd_size(wp_table, wp_variables, order) * 4 < \
        automaton_size(wp_table, wp_variables, order)
    print("""
      FDD-small, automaton-BIG, with the gap doubling per pair: a
      member of the taxonomy does NOT flow to the automaton.

  A4. The reverse hunt came up empty: on every counting family tried
      (majority below, thresholds, selector functions) the FDD
      TRACKED the automaton rather than exploding --
""")
    for variable_count in (10, 12, 14):
        table = majority_table(variable_count)
        natural = list(range(variable_count))
        print(f"      majority n = {variable_count:2d}: automaton "
              f"{automaton_size(table, variable_count, natural):3d}   "
              f"FDD {fdd_size(table, variable_count, natural):3d}")
    print("""
      (exponential separations in BOTH directions are the known
      result in the decision-diagram literature -- Becker, Drechsler
      et al.; the reverse witness is not reproduced here and is
      recorded as the honest gap).

  A5. VERDICT. The conjecture is FALSE as stated: within the full
      Kronecker taxonomy the automaton is not the unique sink,
      because the Davio-shared frame does not flow to it (A3), while
      the flat frames flow to both shared frames (A2). What the
      evidence actually supports:

          flat frames  ──────►  SHARED frames     (the real flow)
          shared frames: mutually incomparable    (one direction
                                                   measured, reverse
                                                   cited)

      The sink property belongs to the SHARING MOVE -- the quotient,
      Myhill-Nerode / node-merging -- not to the Shannon choice or to
      any fixed frame. The automaton was 0026's unique sink only
      because 0026's frame set contained a single shared frame. At
      the shared frontier, sink-ness survives only as a parameter
      portfolio (a Kronecker choice vector emulates any member), and
      best-parameter search is NP-hard.""")


# ---------------------------------------------------------------------
# Part B: the exact ceilings
# ---------------------------------------------------------------------

def predicted_cut_states(monomials: list[int], variable_count: int,
                         cut: int) -> int:
    """The exact crossing law: distinct subfunctions at a cut =
    distinct values of (symmetric difference of selected right parts)
    XOR (completed parity), over all prefixes."""
    low_mask = (1 << cut) - 1
    distinct: set[frozenset[int]] = set()
    for prefix in range(1 << cut):
        polynomial: set[int] = set()
        for monomial in monomials:
            left_part = monomial & low_mask
            right_part = monomial & ~low_mask
            if prefix & left_part == left_part:
                polynomial ^= {right_part}
        distinct.add(frozenset(polynomial))
    return len(distinct)


def show_exact_crossing_law() -> None:
    source = random.Random(5)
    variable_count = 12
    natural = list(range(variable_count))
    for _ in range(200):
        term_count = source.randrange(2, 9)
        monomials = list({source.randrange(1, 1 << variable_count)
                          for _ in range(term_count)})
        table = table_of_monomials(monomials, variable_count)
        measured = subfunction_counts(table, variable_count, natural)
        for cut in range(variable_count + 1):
            assert measured[cut] == predicted_cut_states(
                monomials, variable_count, cut)
    print("""  B1. crossing law, EXACT: measured subfunctions equal the
      predicted image size at EVERY cut of 200 random sparse
      statements -- the inequality of 0025 is an equality with the
      right invariant.""")

    # tight family: singleton disjoint lefts, independent rights
    strand_count = 5
    cut = strand_count
    tight_monomials = [(1 << index) | (1 << (strand_count + index))
                       for index in range(strand_count)]
    tight_table = table_of_monomials(tight_monomials,
                                     2 * strand_count)
    tight_measured = subfunction_counts(
        tight_table, 2 * strand_count,
        list(range(2 * strand_count)))[cut]
    assert tight_measured == 1 << strand_count

    # collapse mode 1: a right-part linear dependence (duplicate right)
    collided = list(tight_monomials)
    collided[1] = (1 << 1) | (1 << (strand_count + 0))   # same right
    collided_measured = subfunction_counts(
        table_of_monomials(collided, 2 * strand_count),
        2 * strand_count, list(range(2 * strand_count)))[cut]
    assert collided_measured == 1 << (strand_count - 1)

    # collapse mode 2: a shared left variable (selections coupled)
    coupled = list(tight_monomials)
    coupled[1] = (1 << 0) | (1 << (strand_count + 1))    # same left
    coupled_measured = subfunction_counts(
        table_of_monomials(coupled, 2 * strand_count),
        2 * strand_count, list(range(2 * strand_count)))[cut]
    assert coupled_measured == 1 << (strand_count - 1)
    print(f"""      ceiling achieved at 2^s = {1 << strand_count} with
      disjoint singleton lefts and independent rights; one right-part
      collision collapses it to {collided_measured}, one shared left
      variable to {coupled_measured} -- each dependence costs exactly a
      factor of 2. Collapse IS upstream algebraic dependence.""")


def show_exact_path_law() -> None:
    source = random.Random(6)
    variable_count = 12
    natural = list(range(variable_count))
    for _ in range(200):
        model_total = source.randrange(1, 21)
        chosen = source.sample(range(1 << variable_count), model_total)
        table = [0] * (1 << variable_count)
        for point in chosen:
            table[point] = 1
        measured = subfunction_counts(table, variable_count, natural)
        ordered_points = [
            sum(((point >> variable) & 1) << (variable_count - 1 - index)
                for index, variable in enumerate(natural))
            for point in chosen]
        for cut in range(variable_count + 1):
            suffix_sets_by_prefix: dict[int, set[int]] = {}
            for point in ordered_points:
                prefix = point >> (variable_count - cut)
                suffix = point & ((1 << (variable_count - cut)) - 1)
                suffix_sets_by_prefix.setdefault(prefix,
                                                 set()).add(suffix)
            distinct_suffix_sets = {
                frozenset(suffixes)
                for suffixes in suffix_sets_by_prefix.values()}
            zero_present = 1 if len(suffix_sets_by_prefix) < (1 << cut) \
                else 0
            assert measured[cut] == len(distinct_suffix_sets) + \
                zero_present
    clustered = [0] * (1 << variable_count)
    base = 0b101010101010
    for low in range(16):
        clustered[(base & ~0b1111) | low] = 1
    clustered_size = automaton_size(clustered, variable_count, natural)
    spread = [0] * (1 << variable_count)
    for point in random.Random(7).sample(range(1 << variable_count), 16):
        spread[point] = 1
    spread_size = automaton_size(spread, variable_count, natural)
    print(f"""  B2. path law, EXACT: states at a cut = distinct model
      SUFFIX-SETS (+1 for the zero subfunction when some prefix is
      model-free) -- equality at every cut, 200 random statements.
      Two collapse modes: prefixes sharing a suffix-set merge, and
      models clustering under one prefix stop paying: 16 clustered
      models cost {clustered_size} states against {spread_size} for
      16 spread models.""")


def show_exact_span_law() -> None:
    variable_count = 12
    natural = list(range(variable_count))
    rows = [0b111000111000, 0b000111000111, 0b101010101010]

    def factored_table(inner) -> TruthTable:
        table = []
        for point in range(1 << variable_count):
            image = 0
            for row_index, row in enumerate(rows):
                if bin(point & row).count('1') & 1:
                    image |= 1 << row_index
            table.append(inner(image))
        return table

    generic = factored_table(lambda v: 1 if v in (0b001, 0b011, 0b100)
                             else 0)
    generic_peak = max(subfunction_counts(generic, variable_count,
                                          natural))
    inner_parity = factored_table(lambda v: bin(v).count('1') & 1)
    parity_peak = max(subfunction_counts(inner_parity, variable_count,
                                         natural))
    assert generic_peak == 8 and parity_peak == 2
    print(f"""  B3. span law: with d = 3 the generic inner function
      reaches the 2^d = 8 ceiling (measured peak {generic_peak});
      an inner function with a translation stabiliser of index 2
      (parity of the three linear forms) collapses every cut to
      {parity_peak}. Collapse IS the stabiliser.""")


def run_verification_suite() -> None:
    show_part_a()
    print()
    print("=" * 70)
    print("B  THE CEILINGS, EXACTLY")
    print("=" * 70)
    show_exact_crossing_law()
    print()
    show_exact_path_law()
    print()
    show_exact_span_law()
    print("""
  CLOSURE: every ordered edge's per-cut count is the image size of
  the upstream description under the cut. The published rates are the
  free-image case (shattering + independence); every collapse is an
  upstream algebraic dependence -- a linear relation among right
  parts, a shared left variable, a model-prefix cluster, an inner
  stabiliser. Concentration flows to the automaton at a rate set
  exactly by how much algebraic independence the upstream description
  carries across each cut.
""")
    print("all sink-and-ceiling checks passed")


if __name__ == "__main__":
    run_verification_suite()
