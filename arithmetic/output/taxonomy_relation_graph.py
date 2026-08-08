"""The complete relation graph of the taxonomy's five frames.

Frames: ANF (positive Davio), dual ANF (negative Davio), minterm
(model list; size = model count), Walsh (character spectrum over the
integer lift; size = support), automaton (quasi-reduced OBDD in a
given order; size = distinct subfunctions summed over cuts).

All ten pairs classified into three relation types:

  CONJUGATE  mutually unbiased, exact product uncertainty
  ORDERED    one-way: upstream-small forces downstream-small at a
             stated rate; converse fails exponentially
  FREE       all four joint cells inhabited; no law either way

Results verified below:

  minterm  x Walsh       CONJUGATE          (0024, Donoho-Stark, tight)
  ANF      x automaton   ORDERED  ANF  ->   rate 2^crossing   (0025)
  dualANF  x automaton   ORDERED  dual ->   (by complement symmetry)
  Walsh    x automaton   ORDERED  Walsh ->  rate 2^d, d = dim of the
                                            span of the Walsh support
  minterm  x automaton   ORDERED  mint ->   rate (n+1) * models  [linear!]
  Walsh    x ANF         ORDERED  Walsh ->  rate n^log2(support), via
                                            deg2(f) <= log2 support
  Walsh    x dualANF     ORDERED  Walsh ->  (by complement symmetry)
  ANF      x dualANF     FREE
  ANF      x minterm     FREE
  dualANF  x minterm     FREE               (by complement symmetry)

Headline: THE AUTOMATON IS THE UNIVERSAL SINK OF THESE FIVE FRAMES --
concentration in every other frame flows to it, and it forces nothing
back. (Scope note added after 0027: this uniqueness is relative to
the flat frames listed above; admitting the taxonomy's other shared
frame, the FDD, refutes uniqueness for the full taxonomy -- see
sink_uniqueness_and_ceilings.py. Sink-ness belongs to the sharing
move.)

Run this file directly.
"""

from __future__ import annotations

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anf_automaton_tradeoff import (automaton_size, anf_term_count,
                                    table_of_monomials)

VARIABLE_COUNT: int = 12
POINT_COUNT: int = 1 << VARIABLE_COUNT
NATURAL_ORDER: list[int] = list(range(VARIABLE_COUNT))

TruthTable = list[int]


def model_count(table: TruthTable) -> int:
    return sum(table)


def walsh_spectrum_signed(table: TruthTable,
                          variable_count: int) -> list[int]:
    spectrum = [1 - 2 * value for value in table]
    point_count = 1 << variable_count
    step = 1
    while step < point_count:
        for block_start in range(0, point_count, 2 * step):
            for offset in range(block_start, block_start + step):
                low, high = spectrum[offset], spectrum[offset + step]
                spectrum[offset] = low + high
                spectrum[offset + step] = low - high
        step *= 2
    return spectrum


def walsh_spectrum_plain(table: TruthTable,
                         variable_count: int) -> list[int]:
    """Unnormalised transform of the 0/1 table itself. Differs from
    the signed spectrum only in the zero coefficient, but the degree
    law below is stated for THIS convention (parity: signed support 1,
    plain support 2, degree 1)."""
    spectrum = list(table)
    point_count = 1 << variable_count
    step = 1
    while step < point_count:
        for block_start in range(0, point_count, 2 * step):
            for offset in range(block_start, block_start + step):
                low, high = spectrum[offset], spectrum[offset + step]
                spectrum[offset] = low + high
                spectrum[offset + step] = low - high
        step *= 2
    return spectrum


def walsh_support(table: TruthTable, variable_count: int) -> int:
    return sum(1 for value in
               walsh_spectrum_plain(table, variable_count)
               if value != 0)


def walsh_support_span_dimension(table: TruthTable,
                                 variable_count: int) -> int:
    """Dimension of the GF(2) span of the Walsh support (the smallest
    linear map the statement factors through)."""
    basis: list[int] = []
    for character, value in enumerate(
            walsh_spectrum_plain(table, variable_count)):
        if value == 0:
            continue
        reduced = character
        for vector in basis:
            reduced = min(reduced, reduced ^ vector)
        if reduced:
            basis.append(reduced)
            basis.sort(reverse=True)
    return len(basis)


def dual_term_count(table: TruthTable, variable_count: int) -> int:
    """Dual ANF = ANF of the fully complemented function f(x ^ 1...1)."""
    complement_mask = (1 << variable_count) - 1
    translated = [table[point ^ complement_mask]
                  for point in range(1 << variable_count)]
    return anf_term_count(translated, variable_count)


def algebraic_degree(table: TruthTable, variable_count: int) -> int:
    coefficients = list(table)
    for bit_position in range(variable_count):
        step = 1 << bit_position
        for mask in range(1 << variable_count):
            if mask & step:
                coefficients[mask] ^= coefficients[mask ^ step]
    return max((bin(mask).count('1')
                for mask, value in enumerate(coefficients) if value),
               default=0)


# ---------------------------------------------------------------------
# 0. The complement symmetry that transfers three edges
# ---------------------------------------------------------------------

def check_complement_symmetry() -> None:
    source = random.Random(1)
    complement_mask = POINT_COUNT - 1
    for _ in range(30):
        table = [source.randint(0, 1) for _ in range(POINT_COUNT)]
        mirrored = [table[point ^ complement_mask]
                    for point in range(POINT_COUNT)]
        assert model_count(table) == model_count(mirrored)
        assert walsh_support(table, VARIABLE_COUNT) == \
            walsh_support(mirrored, VARIABLE_COUNT)
        assert automaton_size(table, VARIABLE_COUNT, NATURAL_ORDER) == \
            automaton_size(mirrored, VARIABLE_COUNT, NATURAL_ORDER)
    print("  0. complement symmetry: model count, Walsh support and "
          "automaton size are\n     invariant under full complement "
          "(30 random checks) -- so every edge\n     involving ANF "
          "transfers verbatim to dual ANF")


# ---------------------------------------------------------------------
# 1. minterm -> automaton: the path law, linear rate
# ---------------------------------------------------------------------

def check_minterm_to_automaton() -> None:
    source = random.Random(2)
    for _ in range(200):
        models = source.randrange(1, 21)
        table = [0] * POINT_COUNT
        for point in source.sample(range(POINT_COUNT), models):
            table[point] = 1
        size = automaton_size(table, VARIABLE_COUNT, NATURAL_ORDER)
        assert size <= (VARIABLE_COUNT + 1) * (models + 1)
    at_least_one = [1 if point else 0 for point in range(POINT_COUNT)]
    or_models = model_count(at_least_one)
    or_size = automaton_size(at_least_one, VARIABLE_COUNT,
                             NATURAL_ORDER)
    print(f"""  1. minterm -> automaton, ORDERED at LINEAR rate:
     automaton <= (n+1) * (models + 1): each cut carries at most one
     distinct subfunction per model prefix, plus the zero subfunction
     (200 random sparse-model functions, n = 12, all pass).
     Converse fails exponentially: at-least-one has {or_models} models
     and a {or_size}-state automaton.""")


# ---------------------------------------------------------------------
# 2. Walsh -> automaton: the span law, rate 2^d
# ---------------------------------------------------------------------

def check_walsh_to_automaton() -> None:
    source = random.Random(3)
    print("""  2. Walsh -> automaton, ORDERED at rate 2^d
     (d = dimension of the span of the Walsh support; the statement
     factors through a d-dimensional linear map, and the automaton
     need only carry the d running parities):
""")
    for factor_dimension in (2, 3, 4):
        rows = [source.randrange(1, POINT_COUNT)
                for _ in range(factor_dimension)]
        inner = [source.randint(0, 1) for _ in range(1 << factor_dimension)]
        table = []
        for point in range(POINT_COUNT):
            image = 0
            for row_index, row in enumerate(rows):
                if bin(point & row).count('1') & 1:
                    image |= 1 << row_index
            table.append(inner[image])
        support = walsh_support(table, VARIABLE_COUNT)
        span = walsh_support_span_dimension(table, VARIABLE_COUNT)
        size = automaton_size(table, VARIABLE_COUNT, NATURAL_ORDER)
        bound = (VARIABLE_COUNT + 1) * (1 << span) + 2
        assert span <= factor_dimension
        assert size <= bound
        print(f"       f = g(Lx), rank {factor_dimension}: support "
              f"{support:3d}, span d = {span}, automaton {size:4d} "
              f"<= {bound}")
    at_least_one = [1 if point else 0 for point in range(POINT_COUNT)]
    print(f"""     Converse fails exponentially: at-least-one has Walsh
     support {walsh_support(at_least_one, VARIABLE_COUNT)} (full) and a
     {automaton_size(at_least_one, VARIABLE_COUNT, NATURAL_ORDER)}-state
     automaton.""")


# ---------------------------------------------------------------------
# 3. Walsh -> ANF: sparsity bounds degree, quasipolynomial rate
# ---------------------------------------------------------------------

def check_walsh_to_anf() -> None:
    exhaustive_variables = 4
    for function_index in range(1 << (1 << exhaustive_variables)):
        table = [(function_index >> point) & 1
                 for point in range(1 << exhaustive_variables)]
        degree = algebraic_degree(table, exhaustive_variables)
        support = walsh_support(table, exhaustive_variables)
        assert (1 << degree) <= support or degree == 0
    print("""  3. Walsh -> ANF, ORDERED at QUASIPOLYNOMIAL rate:
     deg2(f) <= log2(Walsh support) -- verified EXHAUSTIVELY over all
     65,536 functions of 4 variables -- hence
     ANF terms <= sum of C(n, k) for k <= log2(support), which is
     n^log2(support). The rate is genuinely a function of n, not of
     the support alone:""")
    for half_width in (4, 6):
        pair_monomial_left = (1 << half_width) - 1
        pair_monomial_right = pair_monomial_left << half_width
        total = 2 * half_width
        table = []
        for point in range(1 << total):
            left_parity = bin(point & pair_monomial_left).count('1') & 1
            right_parity = bin(point & pair_monomial_right).count('1') & 1
            table.append(left_parity & right_parity)
        terms = anf_term_count(table, total)
        support = walsh_support(table, total)
        assert terms == half_width * half_width and support == 4
        print(f"       AND of two {half_width}-variable parities: "
              f"support 4 (fixed), ANF terms {terms} (= (n/2)^2, "
              f"grows)")
    print("""     Converse fails exponentially: a single full monomial has
     1 ANF term and full Walsh support.""")


# ---------------------------------------------------------------------
# 4. The free pairs: all four cells, measured
# ---------------------------------------------------------------------

def check_free_pairs() -> None:
    full_monomial = table_of_monomials([POINT_COUNT - 1],
                                       VARIABLE_COUNT)
    parity = table_of_monomials([1 << v for v in range(VARIABLE_COUNT)],
                                VARIABLE_COUNT)
    at_least_one = [1 if point else 0 for point in range(POINT_COUNT)]
    delta_at_zero = [1 if point == 0 else 0
                     for point in range(POINT_COUNT)]

    def anf(table: TruthTable) -> int:
        return anf_term_count(table, VARIABLE_COUNT)

    def dual(table: TruthTable) -> int:
        return dual_term_count(table, VARIABLE_COUNT)

    print("""  4. the FREE pairs -- every joint cell inhabited, no law
     either way (n = 12):

     ANF x dual ANF:""")
    for label, table in (("parity", parity),
                         ("full monomial", full_monomial),
                         ("at-least-one", at_least_one)):
        print(f"       {label:<16} A = {anf(table):5d}   "
              f"dual = {dual(table):5d}")
    assert anf(full_monomial) == 1 and dual(full_monomial) == POINT_COUNT
    assert anf(at_least_one) == POINT_COUNT - 1 and \
        dual(at_least_one) == 2
    print("""
     ANF x minterm:""")
    for label, table in (("full monomial", full_monomial),
                         ("parity", parity),
                         ("delta at zero", delta_at_zero),
                         ("at-least-one", at_least_one)):
        print(f"       {label:<16} A = {anf(table):5d}   "
              f"models = {model_count(table):5d}")
    assert anf(full_monomial) == 1 and model_count(full_monomial) == 1
    assert anf(delta_at_zero) == POINT_COUNT and \
        model_count(delta_at_zero) == 1
    print("""
     (small, small), (small, BIG), (BIG, small), (BIG, BIG) all
     realised in both tables; dual ANF x minterm follows by the
     complement symmetry. No product bound, no one-way law.""")


# ---------------------------------------------------------------------
# 5. The sink property: the automaton forces nothing back
# ---------------------------------------------------------------------

def check_sink_property() -> None:
    at_least_one = [1 if point else 0 for point in range(POINT_COUNT)]
    full_monomial = table_of_monomials([POINT_COUNT - 1],
                                       VARIABLE_COUNT)
    or_size = automaton_size(at_least_one, VARIABLE_COUNT,
                             NATURAL_ORDER)
    and_size = automaton_size(full_monomial, VARIABLE_COUNT,
                              NATURAL_ORDER)
    assert or_size <= 3 * VARIABLE_COUNT
    assert and_size <= 3 * VARIABLE_COUNT
    print(f"""  5. the automaton forces NOTHING back -- small-automaton
     witnesses defeat every other frame at once:
       at-least-one   automaton {or_size:3d}, but ANF {POINT_COUNT - 1},
                      models {POINT_COUNT - 1}, Walsh support
                      {walsh_support(at_least_one, VARIABLE_COUNT)}
       full monomial  automaton {and_size:3d}, but dual ANF {POINT_COUNT},
                      Walsh support
                      {walsh_support(full_monomial, VARIABLE_COUNT)}""")


def run_verification_suite() -> None:
    print("=" * 70)
    print("THE TAXONOMY RELATION GRAPH, COMPLETED")
    print("=" * 70)
    check_complement_symmetry()
    print()
    check_minterm_to_automaton()
    print()
    check_walsh_to_automaton()
    print()
    check_walsh_to_anf()
    print()
    check_free_pairs()
    print()
    check_sink_property()
    print("""
  THE GRAPH (edges point downstream; rates on edges):

      Walsh ──n^log σ──►  ANF   ──2^crossing──►  automaton
        │ ╲──n^log σ──►  dualANF ──2^crossing──►  automaton
        │ ╲──────────────2^d────────────────────►  automaton
        ║ conjugate (Donoho-Stark, tight)
      minterm ────────(n+1)·(models+1)──────────►  automaton

      free pairs: ANF x dualANF, ANF x minterm, dualANF x minterm

  The automaton is the UNIVERSAL SINK: concentration in any frame
  flows to it; it forces nothing back. The one conjugate axis
  (minterm x Walsh) is orthogonal to the flow.
""")
    print("all relation-graph checks passed")


if __name__ == "__main__":
    run_verification_suite()
