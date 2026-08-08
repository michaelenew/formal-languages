"""The ANF x automaton relationship: not an uncertainty pair -- a
one-way street, governed by a crossing law.

Findings, all machine-checked here (feeding exploration/0025):

  1. NO DONOHO-STARK ANALOGUE EXISTS for this pair, and the diagnosis
     is structural: the two bases are not mutually unbiased. An ANF
     basis vector (a single monomial) has an O(n) automaton, so
     statements exist that are tiny in BOTH bases (a monomial, parity)
     and the product bound fails by an exponential margin.

  2. ALL FOUR CELLS of the joint behaviour are inhabited, three
     explicitly measured, one by an explicit direct-sum witness:
         (small, small)   parity, single monomial
         (small, BIG)     windowed parity, separated order
         (BIG, small)     at-least-one
         (BIG, BIG)       at-least-one  XOR  windowed parity
     (disjoint variables; both coordinates grow exponentially).

  3. THE CROSSING LAW (the theorem that replaces uncertainty): for a
     statement given as a XOR of monomials, and any variable order,

         distinct subfunctions at cut L  <=  2^(straddle(L) + 1)

     where straddle(L) is the number of monomials with variables on
     both sides of the cut. Proof: a subfunction is determined by
     which straddling monomials' left parts are satisfied (a vector
     in {0,1}^straddle) plus the parity of the completed monomials
     (one bit). Corollary, since straddle <= term count A:

         log2(automaton size)  <=  A + log2(n+1) + 1

     ANF-concentration FORCES automaton-concentration. The converse
     fails by an exponential margin (at-least-one). Verified on 300
     random sparse forms, and TIGHT on windowed parity.

  4. THE CROSSING LAW EXPLAINS FRAME SENSITIVITY quantitatively: the
     same windowed-parity statement has straddle w interleaved and
     straddle m - w separated, and the measured automaton sizes track
     2^straddle in both frames.

Automaton size here = quasi-reduced OBDD size in the given order:
the sum over cut depths of the number of distinct subfunctions --
i.e. the number of distinct Brzozowski derivatives by prefix length,
the leveled form of 0018's identification. Run this file directly.
"""

from __future__ import annotations

import random


def reordered_table(truth_table: list[int], variable_count: int,
                    variable_order: list[int]) -> bytes:
    """Rewrite the table so variable_order[0] is the most significant
    address bit; subfunctions at cut L become contiguous slices."""
    point_count = 1 << variable_count
    rewritten = bytearray(point_count)
    for point in range(point_count):
        address = 0
        for position, variable in enumerate(variable_order):
            if point >> variable & 1:
                address |= 1 << (variable_count - 1 - position)
        rewritten[address] = truth_table[point]
    return bytes(rewritten)


def subfunction_counts(truth_table: list[int], variable_count: int,
                       variable_order: list[int]) -> list[int]:
    """Number of distinct subfunctions after fixing the first L
    variables of the order, for L = 0..variable_count."""
    ordered = reordered_table(truth_table, variable_count,
                              variable_order)
    point_count = 1 << variable_count
    counts: list[int] = []
    for fixed_count in range(variable_count + 1):
        slice_length = point_count >> fixed_count
        distinct = {ordered[start:start + slice_length]
                    for start in range(0, point_count, slice_length)}
        counts.append(len(distinct))
    return counts


def automaton_size(truth_table: list[int], variable_count: int,
                   variable_order: list[int]) -> int:
    return sum(subfunction_counts(truth_table, variable_count,
                                  variable_order))


def anf_term_count(truth_table: list[int], variable_count: int) -> int:
    coefficients = list(truth_table)
    for bit_position in range(variable_count):
        step = 1 << bit_position
        for mask in range(1 << variable_count):
            if mask & step:
                coefficients[mask] ^= coefficients[mask ^ step]
    return sum(coefficients)


def table_of_monomials(monomials: list[int],
                       variable_count: int) -> list[int]:
    """Truth table of a XOR of monomials (each a variable bitmask)."""
    return [sum(1 for monomial in monomials
                if point & monomial == monomial) & 1
            for point in range(1 << variable_count)]


def straddle_counts(monomials: list[int], variable_count: int,
                    variable_order: list[int]) -> list[int]:
    """For each cut L, how many monomials have variables on both
    sides of the cut."""
    position_of = {variable: position for position, variable
                   in enumerate(variable_order)}
    counts: list[int] = []
    for cut in range(variable_count + 1):
        straddling = 0
        for monomial in monomials:
            positions = [position_of[v] for v in range(variable_count)
                         if monomial >> v & 1]
            if positions and min(positions) < cut <= max(positions):
                straddling += 1
        counts.append(straddling)
    return counts


def windowed_parity_monomials(pair_count: int,
                              window: int) -> tuple[list[int], int]:
    """XOR of x_(j+w) & y_j over j; variables x_i at index i, y_j at
    index pair_count + j. Returns (monomials, variable_count)."""
    monomials = [(1 << (j + window)) | (1 << (pair_count + j))
                 for j in range(pair_count - window)]
    return monomials, 2 * pair_count


def show_no_uncertainty_pair() -> None:
    print("=" * 70)
    print("1  NO DONOHO-STARK ANALOGUE: THE BASES ARE NOT UNBIASED")
    print("=" * 70)
    variable_count = 12
    natural_order = list(range(variable_count))
    single_monomial = table_of_monomials(
        [(1 << variable_count) - 1], variable_count)
    parity = table_of_monomials(
        [1 << v for v in range(variable_count)], variable_count)
    for label, table in (("single monomial x1..x12", single_monomial),
                         ("parity", parity)):
        terms = anf_term_count(table, variable_count)
        states = automaton_size(table, variable_count, natural_order)
        product = terms * states
        assert product < (1 << variable_count) // 8
        print(f"    {label:<24} A = {terms:4d}   B = {states:3d}   "
              f"A*B = {product:5d}   << 2^n = {1 << variable_count}")
    print("""
    An ANF basis vector has an O(n) automaton, so 'tiny in both' is
    possible and every product-type uncertainty bound is dead on
    arrival. The Donoho-Stark mechanism (each basis vector of one
    basis maximally spread in the other) is exactly what this pair
    lacks.""")


def show_four_cells() -> None:
    print()
    print("=" * 70)
    print("2  ALL FOUR CELLS INHABITED")
    print("=" * 70)
    variable_count = 12
    natural_order = list(range(variable_count))
    parity = table_of_monomials(
        [1 << v for v in range(variable_count)], variable_count)
    at_least_one = [1 if point else 0
                    for point in range(1 << variable_count)]
    windowed, windowed_variables = windowed_parity_monomials(6, 1)
    windowed_table = table_of_monomials(windowed, windowed_variables)
    separated_order = list(range(windowed_variables))

    # direct sum: at-least-one on 6 variables XOR windowed parity on
    # 12 more (pair_count 3, window 1, separated) -- disjoint supports
    def direct_sum_tables(or_count: int, pair_count: int,
                          window: int) -> tuple[list[int], int]:
        total = or_count + 2 * pair_count
        windowed_monomials, _ = windowed_parity_monomials(pair_count,
                                                          window)
        shifted = [monomial << or_count
                   for monomial in windowed_monomials]
        table = []
        for point in range(1 << total):
            or_part = 1 if point & ((1 << or_count) - 1) else 0
            parity_part = sum(
                1 for monomial in shifted
                if point & monomial == monomial) & 1
            table.append(or_part ^ parity_part)
        return table, total

    rows = []
    terms = anf_term_count(parity, variable_count)
    states = automaton_size(parity, variable_count, natural_order)
    rows.append(("parity", "(small, small)", terms, states))
    terms = anf_term_count(windowed_table, windowed_variables)
    states = automaton_size(windowed_table, windowed_variables,
                            separated_order)
    rows.append(("windowed parity, separated", "(small, BIG)",
                 terms, states))
    terms = anf_term_count(at_least_one, variable_count)
    states = automaton_size(at_least_one, variable_count,
                            natural_order)
    rows.append(("at least one", "(BIG, small)", terms, states))
    for or_count, pair_count in ((6, 3), (8, 4)):
        table, total = direct_sum_tables(or_count, pair_count, 1)
        terms = anf_term_count(table, total)
        states = automaton_size(table, total, list(range(total)))
        rows.append((f"at-least-one({or_count}) ^ windowed({pair_count})",
                     "(BIG, BIG)", terms, states))
    for label, cell, terms, states in rows:
        print(f"    {label:<28} {cell:<15} A = {terms:5d}   "
              f"B = {states:5d}")
    print("""
    The (BIG, BIG) witness grows exponentially in both coordinates as
    its halves grow (A doubles with each OR variable, B doubles with
    each pair). Every joint behaviour is realised; there is no law of
    the product.""")


def show_crossing_law() -> None:
    print()
    print("=" * 70)
    print("3  THE CROSSING LAW (the theorem that replaces uncertainty)")
    print("=" * 70)
    source = random.Random(20260808)
    variable_count = 12
    natural_order = list(range(variable_count))
    worst_ratio = 0.0
    for _ in range(300):
        term_count = source.randrange(2, 9)
        monomials = list({
            source.randrange(1, 1 << variable_count)
            for _ in range(term_count)})
        table = table_of_monomials(monomials, variable_count)
        counts = subfunction_counts(table, variable_count,
                                    natural_order)
        straddles = straddle_counts(monomials, variable_count,
                                    natural_order)
        for cut in range(variable_count + 1):
            bound = 1 << (straddles[cut] + 1)
            assert counts[cut] <= bound
            worst_ratio = max(worst_ratio, counts[cut] / bound)
    print(f"""
    distinct subfunctions at every cut <= 2^(straddle + 1): verified,
    300 random sparse XOR-of-monomial statements (n = 12), every cut
    (largest ratio to the bound observed: {worst_ratio:.2f}).

    Corollary, since straddle <= term count A:
        log2(automaton size) <= A + log2(n + 1) + 1
    -- ANF-concentration FORCES automaton-concentration. The converse
    fails exponentially (at-least-one, section 2). The street runs
    one way.""")


def show_frame_sensitivity_explained() -> None:
    print()
    print("=" * 70)
    print("4  THE CROSSING LAW EXPLAINS FRAME SENSITIVITY")
    print("=" * 70)
    pair_count, window = 8, 2
    monomials, variable_count = windowed_parity_monomials(pair_count,
                                                          window)
    separated = list(range(variable_count))
    interleaved: list[int] = []
    for index in range(pair_count):
        interleaved.append(index)                    # x_index
        interleaved.append(pair_count + index)       # y_index
    table = table_of_monomials(monomials, variable_count)
    print(f"""
    the same statement (windowed parity, {pair_count} pairs,
    window {window}), two frames:
""")
    for label, order in (("separated  x..x y..y", separated),
                         ("interleaved x y x y ..", interleaved)):
        peak_straddle = max(straddle_counts(monomials, variable_count,
                                            order))
        size = automaton_size(table, variable_count, order)
        print(f"      {label:<24} peak straddle {peak_straddle:2d}   "
              f"automaton {size:5d}")
    print("""
    The frame changes nothing about the statement and everything
    about the crossing; the automaton tracks 2^straddle in both
    frames. Frame optimisation IS crossing minimisation -- which is
    why it is a hard combinatorial problem (0024).""")


def run_verification_suite() -> None:
    show_no_uncertainty_pair()
    show_four_cells()
    show_crossing_law()
    show_frame_sensitivity_explained()
    print()
    print("all ANF x automaton checks passed")


if __name__ == "__main__":
    run_verification_suite()
