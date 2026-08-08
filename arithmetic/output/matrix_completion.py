"""Completing the flow matrix: the negFDD joins by the up-zeta law,
the shared-frame triad, and the Walsh -> OBDD cell resolved per-frame.

THE UP-ZETA LAW (the negative-Davio cut law). Negative Davio's two
moves are substitute-at-1 (keeps every monomial, strips the variable)
and derivative (keeps only monomials containing it, strips it). A
choice sequence with derivative-set D therefore keeps exactly the
monomials whose left part CONTAINS D -- so the reachable nodes at a
cut are the UP-SET sums of the ANF's left-fiber vector:

    negFDD width = distinct entries of (zeta-up v),
                   (zeta-up v)(D) = XOR of fiber(D') over D' >= D

completing the trio (all verified exact, and both zetas are
involutions):

    FDD    reads  v            (point mass)
    OBDD   reads  zeta-down v  (down-set sums)
    negFDD reads  zeta-up v    (up-set sums)

One vector, three aggregations. Complementing the address variables
reverses the subset lattice, which exchanges zeta-down with zeta-up
-- so every OBDD/FDD result conjugates into a negFDD result.

THE TRIAD. Three statements, each the unique killer of one shared
frame (k = 8 pairs, measured below):

                       OBDD     FDD    negFDD
    windowed parity     BIG    small    small     (v on singletons)
    one-hot mux        small    BIG     small     (v = zeta-down wp)
    co-one-hot mux     small   small     BIG      (address-reversed)

This fills all four cross-polarity cells of the flow matrix:
  ANF     -> negFDD  E  (anti-fiber ceiling 2^t; co-singleton
                         selector: t = k terms force width 2^k)
  dualANF -> FDD     E  (complement mirror, measured directly)
  FDD     -> negFDD  E  (co-one-hot mux)
  negFDD  -> FDD     E  (one-hot mux)
and re-derives the starred negFDD row (wp: negFDD-small, OBDD-big).

THE WALSH -> OBDD CELL, resolved per-frame. The binary-address
multiplexer (k address bits, 2^k data bits, n = k + 2^k) has
order-free Walsh support Theta(n^2) -- it is the classic
dimension-versus-sparsity extremal shape -- yet in the DATA-FIRST
order its OBDD must remember every data assignment: >= 2^(2^k)
states, superpolynomial in n. So within a fixed frame (order is a
frame parameter, the house convention since 0026) the cell is E.
The escape is SUBEXPONENTIAL in the Walsh size, not free: by the
span law OBDD <= (n+1) 2^d, and Fourier dimension d = O(sqrt(sigma)
log sigma) (Sanyal, cited), so OBDD <= 2^O(sqrt(sigma) log sigma) in
EVERY order -- and the multiplexer meets 2^Theta(sqrt(sigma)),
making the ceiling tight up to the log. In its address-first order
the same statement is linear, so the BEST-frame variant of the cell
(does Walsh-poly imply OBDD-poly in some order?) remains open.

Run this file directly.
"""

from __future__ import annotations

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anf_automaton_tradeoff import (automaton_size, subfunction_counts,
                                    reordered_table, table_of_monomials,
                                    anf_term_count)
from taxonomy_relation_graph import (walsh_support,
                                     walsh_support_span_dimension,
                                     dual_term_count)
from frame_flow_map import (fdd_level_widths, fdd_size, fiber_vector,
                            distinct_fiber_values, zeta_transform,
                            paired_parity_monomials,
                            one_hot_multiplexer_table, FiberVector)

TruthTable = list[int]


# ---------------------------------------------------------------------
# The negative-Davio shared frame
# ---------------------------------------------------------------------

def negfdd_level_widths(truth_table: TruthTable, variable_count: int,
                        variable_order: list[int]) -> list[int]:
    """Distinct functions per level of the quasi-reduced negFDD:
    the negative-Davio children of g are g(variable = 1) and the
    derivative."""
    ordered = reordered_table(truth_table, variable_count,
                              variable_order)
    current_level: set[bytes] = {bytes(ordered)}
    widths = [len(current_level)]
    for _ in range(variable_count):
        next_level: set[bytes] = set()
        for function in current_level:
            half = len(function) // 2
            low, high = function[:half], function[half:]
            next_level.add(high)
            next_level.add(bytes(a ^ b for a, b in zip(low, high)))
        current_level = next_level
        widths.append(len(current_level))
    return widths


def negfdd_size(truth_table: TruthTable, variable_count: int,
                variable_order: list[int]) -> int:
    return sum(negfdd_level_widths(truth_table, variable_count,
                                   variable_order))


def up_zeta_transform(fibers: FiberVector,
                      cut: int) -> list[frozenset[int]]:
    """(zeta-up v)(D) = XOR of fiber(D') over supersets D' of D.
    Over GF(2) this is an involution, like its down-set partner."""
    dense: list[set[int]] = [set(fibers.get(subset, frozenset()))
                             for subset in range(1 << cut)]
    for bit_position in range(cut):
        step = 1 << bit_position
        for subset in range(1 << cut):
            if not subset & step:
                dense[subset] ^= dense[subset | step]
    return [frozenset(entry) for entry in dense]


def show_up_zeta_law() -> None:
    print("=" * 70)
    print("1  THE UP-ZETA LAW: THE negFDD JOINS THE TRIO")
    print("=" * 70)
    source = random.Random(21)
    variable_count = 10
    natural = list(range(variable_count))
    for _ in range(200):
        term_count = source.randrange(2, 9)
        monomials = list({source.randrange(1, 1 << variable_count)
                          for _ in range(term_count)})
        table = table_of_monomials(monomials, variable_count)
        shannon_widths = subfunction_counts(table, variable_count,
                                            natural)
        positive_widths = fdd_level_widths(table, variable_count,
                                           natural)
        negative_widths = negfdd_level_widths(table, variable_count,
                                              natural)
        for cut in range(variable_count + 1):
            fibers = fiber_vector(monomials, cut)
            up = up_zeta_transform(fibers, cut)
            assert negative_widths[cut] == len(set(up))
            assert positive_widths[cut] == \
                distinct_fiber_values(fibers, cut)
            assert shannon_widths[cut] == \
                len(set(zeta_transform(fibers, cut)))
            twice = up_zeta_transform(
                {subset: entry for subset, entry in enumerate(up)
                 if entry}, cut)
            assert twice == [fibers.get(subset, frozenset())
                             for subset in range(1 << cut)]
            # anti-fiber ceiling: at most 2^terms distinct up-sums
            assert negative_widths[cut] <= 1 << len(monomials)
    print("""
  Verified at every cut of 200 random statements (n = 10): the three
  shared frames read ONE fiber vector three ways --
      FDD    width = distinct entries of v          (point mass)
      OBDD   width = distinct entries of zeta-down v
      negFDD width = distinct entries of zeta-up v
  -- zeta-up is an involution like its partner, and the anti-fiber
  ceiling holds: negFDD width <= 2^terms. Complementing the address
  variables reverses the subset lattice and exchanges the two zetas,
  so the polarity square closes by conjugation.""")


# ---------------------------------------------------------------------
# The triad and the four cross-polarity cells
# ---------------------------------------------------------------------

def co_one_hot_multiplexer_table(pair_count: int) -> TruthTable:
    """Output = data bit i when the address has exactly one ZERO (at
    position i), else 0 -- the one-hot multiplexer with complemented
    address."""
    address_mask = (1 << pair_count) - 1
    table: TruthTable = []
    for point in range(1 << (2 * pair_count)):
        inverted = ~point & address_mask
        one_zero = inverted != 0 and inverted & (inverted - 1) == 0
        selected = inverted.bit_length() - 1
        table.append(1 if one_zero
                     and point >> (pair_count + selected) & 1 else 0)
    return table


def co_singleton_selector_monomials(pair_count: int) -> list[int]:
    """k monomials (address variables all-but-i) AND data_i -- the
    sparse-ANF statement whose up-sums shatter."""
    address_mask = (1 << pair_count) - 1
    return [(address_mask ^ (1 << index)) | (1 << (pair_count + index))
            for index in range(pair_count)]


def show_triad_and_cross_polarity_cells() -> None:
    print()
    print("=" * 70)
    print("2  THE TRIAD, AND THE FOUR CROSS-POLARITY CELLS")
    print("=" * 70)
    pair_count = 8
    variable_count = 2 * pair_count
    order = list(range(variable_count))

    windowed = table_of_monomials(paired_parity_monomials(pair_count),
                                  variable_count)
    multiplexer = one_hot_multiplexer_table(pair_count)
    co_multiplexer = co_one_hot_multiplexer_table(pair_count)

    print(f"\n      statement (k = {pair_count}, n = {variable_count})"
          f"        OBDD    FDD  negFDD")
    sizes: dict[str, tuple[int, int, int]] = {}
    for label, table in (("windowed parity", windowed),
                         ("one-hot multiplexer", multiplexer),
                         ("co-one-hot multiplexer", co_multiplexer)):
        measured = (automaton_size(table, variable_count, order),
                    fdd_size(table, variable_count, order),
                    negfdd_size(table, variable_count, order))
        sizes[label] = measured
        print(f"      {label:<28} {measured[0]:5d}  {measured[1]:5d}"
              f"   {measured[2]:5d}")
    linear_bound = 8 * variable_count
    exponential_floor = 1 << pair_count
    assert sizes["windowed parity"][0] >= exponential_floor
    assert sizes["windowed parity"][1] <= linear_bound
    assert sizes["windowed parity"][2] <= linear_bound
    assert sizes["one-hot multiplexer"][0] <= linear_bound
    assert sizes["one-hot multiplexer"][1] >= exponential_floor
    assert sizes["one-hot multiplexer"][2] <= linear_bound
    assert sizes["co-one-hot multiplexer"][0] <= linear_bound
    assert sizes["co-one-hot multiplexer"][1] <= linear_bound
    assert sizes["co-one-hot multiplexer"][2] >= exponential_floor
    print("""
  Each shared frame has exactly ONE killer in the triad and handles
  the other two -- the triad realises the three aggregations of one
  vector (wp puts v on singletons; the mux is its down-zeta image,
  0028; complementing the address reverses the lattice and gives the
  co-mux as the up-zeta image). Pairwise incomparability of all
  three shared frames is now measured in both directions for every
  pair. The four cross-polarity cells:""")

    # ANF -> negFDD: E, anti-fiber ceiling reached by t = k monomials
    selector_monomials = co_singleton_selector_monomials(pair_count)
    selector_table = table_of_monomials(selector_monomials,
                                        variable_count)
    selector_widths = negfdd_level_widths(selector_table,
                                          variable_count, order)
    assert len(selector_monomials) == pair_count
    assert selector_widths[pair_count] == 1 << pair_count
    print(f"""
    ANF -> negFDD       E   co-singleton selector: {pair_count} ANF terms
                            force negFDD width {selector_widths[pair_count]} = 2^{pair_count}
                            (anti-fiber ceiling 2^t, reached)""")

    # dualANF -> FDD: the complement mirror, measured directly
    complement_mask = (1 << variable_count) - 1
    translated_selector = [selector_table[point ^ complement_mask]
                           for point in range(1 << variable_count)]
    translated_dual_terms = dual_term_count(translated_selector,
                                            variable_count)
    translated_widths = fdd_level_widths(translated_selector,
                                         variable_count, order)
    assert translated_dual_terms == pair_count
    assert translated_widths[pair_count] == 1 << pair_count
    print(f"""    dualANF -> FDD      E   its full complement: {translated_dual_terms} dual terms
                            force FDD width {translated_widths[pair_count]} (measured, not
                            just starred)""")
    print(f"""    FDD -> negFDD       E   co-one-hot mux: FDD {sizes['co-one-hot multiplexer'][1]},
                            negFDD {sizes['co-one-hot multiplexer'][2]}
    negFDD -> FDD       E   one-hot mux: negFDD {sizes['one-hot multiplexer'][2]},
                            FDD {sizes['one-hot multiplexer'][1]}
    negFDD -> OBDD      E   windowed parity: negFDD {sizes['windowed parity'][2]},
                            OBDD {sizes['windowed parity'][0]}  (was starred, now
                            measured)""")


# ---------------------------------------------------------------------
# The Walsh -> OBDD cell: the binary-address multiplexer
# ---------------------------------------------------------------------

def binary_multiplexer_table(address_count: int) -> TruthTable:
    """n = address_count + 2^address_count variables: the address
    (low bits) selects which data bit is the output."""
    data_count = 1 << address_count
    variable_count = address_count + data_count
    address_mask = data_count - 1
    table: TruthTable = []
    for point in range(1 << variable_count):
        address = point & address_mask
        table.append(point >> (address_count + address) & 1)
    return table


def show_walsh_to_obdd_cell() -> None:
    print()
    print("=" * 70)
    print("3  THE WALSH -> OBDD CELL: RESOLVED PER-FRAME")
    print("=" * 70)
    print("""
      k   n     Walsh sigma   dim d   OBDD address-first   OBDD data-first""")
    for address_count in (2, 3, 4):
        data_count = 1 << address_count
        variable_count = address_count + data_count
        table = binary_multiplexer_table(address_count)
        address_first = list(range(variable_count))
        data_first = list(range(address_count, variable_count)) + \
            list(range(address_count))
        sigma = walsh_support(table, variable_count)
        dimension = walsh_support_span_dimension(table, variable_count)
        good_order = automaton_size(table, variable_count,
                                    address_first)
        bad_order = automaton_size(table, variable_count, data_first)
        assert sigma <= 4 * (variable_count + 1) ** 2
        assert dimension == variable_count
        assert good_order <= (variable_count + 1) * (data_count + 2)
        assert bad_order >= 1 << data_count
        print(f"      {address_count}  {variable_count:2d}      "
              f"{sigma:5d}       {dimension:3d}        "
              f"{good_order:6d}            {bad_order:8d}")
    print("""
  The binary-address multiplexer: Walsh support Theta(n^2) in EVERY
  order (the spectrum is order-free), full Fourier dimension d = n,
  OBDD linear in the address-first order -- and >= 2^(2^k) =
  2^(n - k) in the data-first order, which must remember every data
  assignment before reading the address. Within a fixed frame the
  cell is therefore E: Walsh-small does NOT force OBDD-small.

  The escape is exactly subexponential in the Walsh size: the span
  law caps OBDD at (n+1) 2^d in every order, Fourier dimension obeys
  d = O(sqrt(sigma) log sigma) (Sanyal 2015, cited -- consistent
  here: d = n against sigma about 4 n^2), and the multiplexer meets
  2^Theta(sqrt(sigma)). So the cell's rate is 2^Theta(sqrt(sigma)),
  tight up to the log in the exponent -- the ONLY cell of the matrix
  whose escape is subexponential rather than 2^Theta(n). What
  remains open is only the BEST-frame variant: this witness is
  linear in its good order, and whether every Walsh-small statement
  has SOME order with a small OBDD is not settled either way.""")


def run_verification_suite() -> None:
    show_up_zeta_law()
    show_triad_and_cross_polarity_cells()
    show_walsh_to_obdd_cell()
    print("""
  THE MATRIX, COMPLETED (per-frame; * = by complement symmetry):

  row \\ col   ANF    dualANF  minterm  Walsh   OBDD      FDD     negFDD
  ANF          .      E        E        E       E 2^str   P fib   E 2^t
  dualANF      E      .        E *      E *     E * 2^str E 2^t   P fib *
  minterm      E      E *      .        CONJ    P path    E 2^mu  E 2^mu *
  Walsh        QP     QP *     CONJ     .       E sub     QP      QP *
  OBDD         E      E *      E        E       .         E mux   E comux
  FDD          E      E        E        E       E wp      .       E comux
  negFDD       E *    E *      E *      E *     E wp      E mux   .

  E sub = the subexponential cell (2^Theta(sqrt(sigma)), best-frame
  variant open). Every other off-diagonal cell is P, QP, CONJ, or a
  measured/mirrored full-exponential escape. No unmeasured cells
  remain.
""")
    print("all matrix-completion checks passed")


if __name__ == "__main__":
    run_verification_suite()
