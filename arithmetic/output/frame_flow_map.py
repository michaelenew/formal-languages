"""The Davio-side laws, the zeta conjugacy of the shared frames, and
the complexity flow map of the frame taxonomy.

THE ZETA CONJUGACY (the Davio analogue of 0027's exact crossing law,
and more). Fix a variable order and a cut after the first k variables.
Write the statement's ANF as a LEFT-FIBER VECTOR: for each subset D of
the cut variables, fiber(D) = the XOR of the right parts of the
monomials whose left part is EXACTLY D. Then, at that cut:

    FDD width  = number of DISTINCT ENTRIES of the fiber vector
    OBDD width = number of DISTINCT ENTRIES of its ZETA TRANSFORM
                 (zeta v)(P) = XOR of fiber(D) over D a subset of P

and over GF(2) the zeta transform is an INVOLUTION (zeta of zeta is
the identity). The two shared frames are therefore exactly
zeta-conjugate, cut by cut: the same information, aggregated by
point-evaluation (Shannon) or by point-mass (Davio), exchanged by an
involution. Every separation witness in one direction maps under zeta
to a witness in the other.

THE LITERATURE WITNESS, DERIVED RATHER THAN HUNTED. 0027 measured
windowed parity (FDD small, OBDD big) but could not reproduce the
cited reverse separation and recorded it as the honest gap. The
conjugacy says: do not hunt, TRANSPORT. Applying zeta to windowed
parity's fiber vector yields fiber(L) = {data variable k+i : i in L}
-- which is the ANF fiber vector of the ONE-HOT MULTIPLEXER (output =
the data bit selected when exactly one address bit is hot). Measured
below: OBDD linear, FDD >= 2^k. Both directions of the BDD/FDD
separation (Becker-Drechsler et al.) are now machine facts, and the
reverse witness was computed by the involution, not guessed. (0027's
hunt failed precisely because it searched counting families; the
image of the known witness is a selector, not a counter.)

THE FOUR FLAT->SHARED LAWS form a 2x2 with exact mirror symmetry:

                      -> OBDD (shared Shannon)   -> FDD (shared Davio)
  minterm (flat S)    path law, LINEAR (0026)    survivor law, 2^models
  ANF     (flat D)    crossing law, 2^straddle   fiber law, LINEAR

  Each flat frame flows LINEARLY into its own sharing and
  EXPONENTIALLY (with an exact image-size ceiling) into the other.
  The fiber law (FDD <= (n+1)(terms+1)) and the survivor law
  (FDD width <= 2^models, ceiling reached by one-hot-prefix models)
  are new here; both verified.

THE FLOW MATRIX over {ANF, minterm, Walsh, OBDD, FDD} (dual ANF folds
onto ANF by the complement symmetry of 0026) and the finiteness
conjecture for the frame family close the file.

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
from taxonomy_relation_graph import walsh_support

TruthTable = list[int]
FiberVector = dict[int, frozenset[int]]


# ---------------------------------------------------------------------
# Shared-frame widths, level by level
# ---------------------------------------------------------------------

def fdd_level_widths(truth_table: TruthTable, variable_count: int,
                     variable_order: list[int]) -> list[int]:
    """Distinct functions per level of the quasi-reduced FDD (children
    of g are g0 and the derivative g0 XOR g1), for cuts 0..n."""
    ordered = reordered_table(truth_table, variable_count,
                              variable_order)
    current_level: set[bytes] = {bytes(ordered)}
    widths = [len(current_level)]
    for _ in range(variable_count):
        next_level: set[bytes] = set()
        for function in current_level:
            half = len(function) // 2
            low, high = function[:half], function[half:]
            next_level.add(low)
            next_level.add(bytes(a ^ b for a, b in zip(low, high)))
        current_level = next_level
        widths.append(len(current_level))
    return widths


def fdd_size(truth_table: TruthTable, variable_count: int,
             variable_order: list[int]) -> int:
    return sum(fdd_level_widths(truth_table, variable_count,
                                variable_order))


# ---------------------------------------------------------------------
# The fiber vector of an ANF at a cut, and its zeta transform
# ---------------------------------------------------------------------

def fiber_vector(monomials: list[int], cut: int) -> FiberVector:
    """fiber(D) = XOR of right parts of monomials with left part
    exactly D, for the nonzero fibers only."""
    low_mask = (1 << cut) - 1
    accumulated: dict[int, set[int]] = {}
    for monomial in monomials:
        left_part = monomial & low_mask
        right_part = monomial & ~low_mask
        fiber = accumulated.setdefault(left_part, set())
        fiber ^= {right_part}
    return {left: frozenset(rights)
            for left, rights in accumulated.items() if rights}


def distinct_fiber_values(fibers: FiberVector, cut: int) -> int:
    """Distinct entries of the fiber vector over ALL 2^cut subsets
    (the zero entry counts once if any subset has an empty fiber)."""
    values = set(fibers.values())
    if len(fibers) < (1 << cut):
        values.add(frozenset())
    return len(values)


def zeta_transform(fibers: FiberVector, cut: int) -> list[frozenset[int]]:
    """(zeta v)(P) = XOR of fiber(D) over subsets D of P, as a dense
    list indexed by P. Over GF(2) this is an involution."""
    dense: list[set[int]] = [set(fibers.get(subset, frozenset()))
                             for subset in range(1 << cut)]
    for bit_position in range(cut):
        step = 1 << bit_position
        for subset in range(1 << cut):
            if subset & step:
                dense[subset] ^= dense[subset ^ step]
    return [frozenset(entry) for entry in dense]


def show_zeta_conjugacy() -> None:
    print("=" * 70)
    print("1  THE ZETA CONJUGACY OF THE SHARED FRAMES")
    print("=" * 70)
    source = random.Random(11)
    variable_count = 12
    natural = list(range(variable_count))
    for _ in range(200):
        term_count = source.randrange(2, 9)
        monomials = list({source.randrange(1, 1 << variable_count)
                          for _ in range(term_count)})
        table = table_of_monomials(monomials, variable_count)
        measured = fdd_level_widths(table, variable_count, natural)
        for cut in range(variable_count + 1):
            predicted = distinct_fiber_values(
                fiber_vector(monomials, cut), cut)
            assert measured[cut] == predicted
    print("""
  THE FIBER LAW, EXACT (the Davio analogue of the exact crossing
  law): FDD width at a cut = distinct entries of the ANF's left-fiber
  vector -- fiber(D) = XOR of right parts of monomials with left part
  EXACTLY D. Verified as an equality at every cut of 200 random
  sparse statements (n = 12).""")

    zeta_variables = 10
    zeta_order = list(range(zeta_variables))
    for _ in range(40):
        term_count = source.randrange(2, 9)
        monomials = list({source.randrange(1, 1 << zeta_variables)
                          for _ in range(term_count)})
        table = table_of_monomials(monomials, zeta_variables)
        shannon_widths = subfunction_counts(table, zeta_variables,
                                            zeta_order)
        davio_widths = fdd_level_widths(table, zeta_variables,
                                        zeta_order)
        for cut in range(zeta_variables + 1):
            fibers = fiber_vector(monomials, cut)
            transformed = zeta_transform(fibers, cut)
            assert shannon_widths[cut] == len(set(transformed))
            assert davio_widths[cut] == distinct_fiber_values(fibers,
                                                              cut)
            twice = zeta_transform(
                {subset: entry
                 for subset, entry in enumerate(transformed) if entry},
                cut)
            assert twice == [fibers.get(subset, frozenset())
                             for subset in range(1 << cut)]
    print("""
  THE CONJUGACY: at every cut of 40 random statements (n = 10),
      OBDD width = distinct entries of the ZETA TRANSFORM of the
                   fiber vector (this is 0027's exact crossing law,
                   re-read: selection over down-sets IS zeta), and
      zeta o zeta = identity (verified entrywise).
  The two shared frames are ZETA-CONJUGATE, cut by cut: one vector,
  two aggregations -- point-mass (Davio) and down-set evaluation
  (Shannon) -- exchanged by an involution. Every separation witness
  maps under zeta to a witness in the opposite direction.""")


# ---------------------------------------------------------------------
# The transported witness: the one-hot multiplexer
# ---------------------------------------------------------------------

def paired_parity_monomials(pair_count: int) -> list[int]:
    """XOR of address_i AND data_i (the separated-order windowed
    parity of 0025/0027, window 0): address bits 0..k-1, data bits
    k..2k-1."""
    return [(1 << index) | (1 << (pair_count + index))
            for index in range(pair_count)]


def one_hot_multiplexer_monomials(pair_count: int) -> list[int]:
    """ANF of the one-hot multiplexer: output = data bit i when the
    address is exactly one-hot at i, else 0. Expansion of
    XOR_i [ address_i * PROD_{j != i}(1 + address_j) * data_i ]:
    for every address subset L and every i in L, the monomial
    (address bits of L) | data bit i."""
    monomials: list[int] = []
    for address_subset in range(1, 1 << pair_count):
        for index in range(pair_count):
            if address_subset >> index & 1:
                monomials.append(address_subset
                                 | (1 << (pair_count + index)))
    return monomials


def one_hot_multiplexer_table(pair_count: int) -> TruthTable:
    address_mask = (1 << pair_count) - 1
    table: TruthTable = []
    for point in range(1 << (2 * pair_count)):
        address = point & address_mask
        one_hot = address != 0 and address & (address - 1) == 0
        selected = address.bit_length() - 1
        table.append(1 if one_hot
                     and point >> (pair_count + selected) & 1 else 0)
    return table


def show_transported_witness() -> None:
    print()
    print("=" * 70)
    print("2  THE LITERATURE WITNESS, DERIVED BY ZETA THEN MEASURED")
    print("=" * 70)
    pair_count = 8
    cut = pair_count
    parity_fibers = fiber_vector(paired_parity_monomials(pair_count),
                                 cut)
    transported = zeta_transform(parity_fibers, cut)
    multiplexer_fibers = fiber_vector(
        one_hot_multiplexer_monomials(pair_count), cut)
    assert transported == [multiplexer_fibers.get(subset, frozenset())
                           for subset in range(1 << cut)]
    assert one_hot_multiplexer_table(pair_count) == table_of_monomials(
        one_hot_multiplexer_monomials(pair_count), 2 * pair_count)
    print("""
  zeta( fiber vector of windowed parity ) = fiber vector of the
  ONE-HOT MULTIPLEXER -- verified entrywise at the middle cut, and
  the expanded ANF reproduces the multiplexer's truth table. The
  reverse witness is the involution image of the known witness.
""")
    print("      k   OBDD(mux)  FDD(mux)      OBDD(wp)  FDD(wp)")
    for measured_pairs in (6, 7, 8):
        variable_count = 2 * measured_pairs
        order = list(range(variable_count))
        multiplexer = one_hot_multiplexer_table(measured_pairs)
        parity = table_of_monomials(
            paired_parity_monomials(measured_pairs), variable_count)
        multiplexer_obdd = automaton_size(multiplexer, variable_count,
                                          order)
        multiplexer_fdd = fdd_size(multiplexer, variable_count, order)
        parity_obdd = automaton_size(parity, variable_count, order)
        parity_fdd = fdd_size(parity, variable_count, order)
        assert multiplexer_obdd <= (variable_count + 1) * \
            (measured_pairs + 2)
        assert multiplexer_fdd >= 1 << measured_pairs
        assert parity_fdd <= 6 * variable_count
        assert parity_obdd >= 1 << measured_pairs
        print(f"      {measured_pairs}   {multiplexer_obdd:6d}   "
              f"{multiplexer_fdd:6d}       {parity_obdd:6d}   "
              f"{parity_fdd:5d}")
    print("""
  Both directions of the shared-frame separation are now MEASURED:
  windowed parity (FDD linear, OBDD doubling) and its zeta image the
  one-hot multiplexer (OBDD linear, FDD >= 2^k). The gap 0027
  recorded against the literature (Becker-Drechsler) is closed, and
  closed constructively: 0027's hunt searched counting families; the
  involution says the image of a parity-accumulator is a SELECTOR.""")


# ---------------------------------------------------------------------
# The four flat -> shared laws
# ---------------------------------------------------------------------

def show_flat_to_shared_square() -> None:
    print()
    print("=" * 70)
    print("3  THE FOUR FLAT -> SHARED LAWS (a 2x2 MIRROR)")
    print("=" * 70)
    source = random.Random(12)
    variable_count = 12
    natural = list(range(variable_count))

    # fiber law: ANF -> FDD is LINEAR
    for _ in range(200):
        term_count = source.randrange(2, 9)
        monomials = list({source.randrange(1, 1 << variable_count)
                          for _ in range(term_count)})
        table = table_of_monomials(monomials, variable_count)
        assert fdd_size(table, variable_count, natural) <= \
            (variable_count + 1) * (len(monomials) + 1)

    # survivor law: minterm -> FDD width <= 2^models, ceiling reached
    for _ in range(200):
        model_total = source.randrange(1, 11)
        table = [0] * (1 << variable_count)
        for point in source.sample(range(1 << variable_count),
                                   model_total):
            table[point] = 1
        widths = fdd_level_widths(table, variable_count, natural)
        assert max(widths) <= 1 << model_total

    pair_count = 8
    witness_variables = 2 * pair_count
    witness_table = [0] * (1 << witness_variables)
    for index in range(pair_count):
        witness_table[(1 << index) | (index << pair_count)] = 1
    witness_widths = fdd_level_widths(witness_table, witness_variables,
                                      list(range(witness_variables)))
    witness_obdd = automaton_size(witness_table, witness_variables,
                                  list(range(witness_variables)))
    assert witness_widths[pair_count] == 1 << pair_count
    assert witness_obdd <= (witness_variables + 1) * (pair_count + 2)
    print(f"""
  fiber law    ANF -> FDD:      FDD <= (n+1)(terms+1)   [LINEAR]
               (200 random sparse statements, n = 12 -- at most one
               distinct nonzero fiber per monomial, plus zero)
  survivor law minterm -> FDD:  width <= 2^models       [EXPONENTIAL]
               (200 random sparse-model statements; the ceiling is
               REACHED by one-hot-prefix models: {pair_count} models with
               address prefixes e_i and distinct data suffixes give
               FDD width {witness_widths[pair_count]} = 2^{pair_count} while the OBDD stays at
               {witness_obdd} by the path law)

  The completed 2x2 (exact ceilings throughout):

                     -> OBDD (shared Shannon)  -> FDD (shared Davio)
    minterm (flat S)  path law    LINEAR        survivor law  2^models
    ANF     (flat D)  crossing law 2^straddle   fiber law     LINEAR

  Each flat frame flows LINEARLY into its OWN shared form and
  EXPONENTIALLY into the other's -- flat-to-shared flow is
  decomposition-respecting, and the off-diagonal ceilings are the two
  faces of the zeta involution.""")


# ---------------------------------------------------------------------
# The flow matrix
# ---------------------------------------------------------------------

def show_flow_matrix() -> None:
    print()
    print("=" * 70)
    print("4  THE FLOW MATRIX  (row small => column?)")
    print("=" * 70)
    variable_count = 12
    point_count = 1 << variable_count
    natural = list(range(variable_count))

    parity = table_of_monomials([1 << v for v in range(variable_count)],
                                variable_count)
    full_monomial = table_of_monomials([point_count - 1],
                                       variable_count)
    at_least_one = [1 if point else 0 for point in range(point_count)]
    delta_at_zero = [1 if point == 0 else 0
                     for point in range(point_count)]

    assert anf_term_count(parity, variable_count) == variable_count
    assert sum(parity) == point_count // 2
    assert anf_term_count(full_monomial, variable_count) == 1
    assert walsh_support(full_monomial, variable_count) == point_count
    assert sum(delta_at_zero) == 1
    assert anf_term_count(delta_at_zero, variable_count) == point_count
    assert walsh_support(delta_at_zero, variable_count) == point_count
    ao_size = automaton_size(at_least_one, variable_count, natural)
    af_size = fdd_size(at_least_one, variable_count, natural)
    assert ao_size <= 3 * variable_count and af_size <= 3 * variable_count
    assert anf_term_count(at_least_one, variable_count) == \
        point_count - 1
    assert walsh_support(at_least_one, variable_count) == point_count

    # Walsh -> FDD at quasipolynomial rate, by composing the degree
    # law (deg <= log support => ANF quasipolynomial) with the fiber
    # law (FDD linear in ANF terms): measured on AND-of-parities.
    half_width = 6
    left_mask = (1 << half_width) - 1
    and_of_parities = []
    for point in range(1 << (2 * half_width)):
        left_parity = bin(point & left_mask).count('1') & 1
        right_parity = bin(point >> half_width).count('1') & 1
        and_of_parities.append(left_parity & right_parity)
    and_terms = anf_term_count(and_of_parities, 2 * half_width)
    and_support = walsh_support(and_of_parities, 2 * half_width)
    and_fdd = fdd_size(and_of_parities, 2 * half_width,
                       list(range(2 * half_width)))
    assert and_support == 4 and and_terms == half_width * half_width
    assert and_fdd <= (2 * half_width + 1) * (and_terms + 1)

    print(f"""
  Witnesses at n = 12 (E cells; the numbers are frame sizes):
    parity          ANF 12          models 2048     Walsh 2
    full monomial   ANF 1           Walsh 4096      OBDD/FDD small
    delta at zero   models 1        ANF 4096        Walsh 4096
    at-least-one    OBDD {ao_size}, FDD {af_size}   ANF 4095, models 4095,
                                                    Walsh 4096
    AND of parities Walsh support {and_support}: ANF {and_terms} = (n/2)^2,
                    FDD {and_fdd} <= (n+1)(terms+1)  [degree law o fiber law]

  row \\ col   ANF     minterm  Walsh    OBDD          FDD
  ANF          .       E        E        E 2^straddle  P linear
  minterm      E       .        CONJ     P linear      E 2^models
  Walsh        QP      CONJ     .        B 2^span *    QP composed
  OBDD         E       E        E        .             E (mux)
  FDD          E       E        E        E (wp)        .

  P  = polynomial law        QP = quasipolynomial law
  E  = witnessed exponential escape        CONJ = Donoho-Stark axis
  B* = bounded by the span law 2^d; whether Walsh-poly can actually
       escape OBDD-poly is OPEN -- Fourier dimension can reach about
       sqrt(support) (Sanyal), but the natural candidate there is an
       addressing function, which is OBDD-SMALL; no witness either
       way. The one open cell of the matrix.
  (dual ANF folds onto the ANF row/column by complement symmetry,
   against the NEGATIVE FDD; its cells mirror verbatim.)

  Readings. The two shared frames are pure sinks (their rows are all
  E: concentration there forces nothing anywhere) and mutually
  incomparable (mux / wp, both measured). Each flat frame drains
  linearly into its own shared form. Walsh is the gentle upstream of
  the DAVIO side -- quasipolynomial into ANF and hence into the FDD --
  while its Shannon-side rate is the matrix's one open cell. The
  conjugate axis minterm x Walsh crosses the flow; the free triangle
  of 0026 (ANF, dual, minterm) stays free.""")


# ---------------------------------------------------------------------
# Finitely many frames, and where complexity flows
# ---------------------------------------------------------------------

def show_finiteness_and_complexity_flow() -> None:
    print()
    print("=" * 70)
    print("5  FINITELY MANY FRAMES: THE CONJECTURE")
    print("=" * 70)
    nonzero_functions = [(0, 1), (1, 0), (1, 1)]   # x, 1+x, 1
    bases: set[frozenset[tuple[int, int]]] = set()
    for first in nonzero_functions:
        for second in nonzero_functions:
            if first != second:      # distinct nonzero => independent
                bases.add(frozenset({first, second}))
    assert len(bases) == 3
    print("""
  One coordinate over GF(2), exhaustively: the function space is
  2-dimensional, its nonzero vectors are x, 1+x, 1, and the UNORDERED
  BASES are exactly the three pairs
      {x, 1+x}  Shannon      {1, x}  positive Davio
      {1, 1+x}  negative Davio
  -- there is no fourth decomposition. (Over the integer lift the
  eigen-condition again selects finitely many: point evaluations
  (Shannon), moments {1, x} (*BMD), their negation, and the
  translation eigenbasis {1, 1-2x} = WALSH, which exists only there
  because translations are unipotent over GF(2), 0023.)

  THE FINITE FRAME CONJECTURE. A frame is an eigen-frame when it
  diagonalises a commuting family generated by the logic's own
  primitive operators -- and the logic has FINITELY MANY primitives
  (the basis theorem, 0012/0013): ^a gives translations, &m gives
  restriction idempotents, << gives the shift, flip gives complement
  conjugation. Conjecture: every eigen-frame is, up to the parameter
  moves (variable order, polarity vector, GL(n,2) change of basis),
  one of
      {Shannon, posDavio, negDavio}           x  {flat, shared}
      over GF(2), and additionally {Walsh, moment, negMoment} over
      the integer lift x {flat, shared}
  -- at most FOURTEEN KINDS, six of which are this thread's named
  frames (minterm, ANF, dual ANF, OBDD, FDD, negFDD) and the rest the
  decision-diagram literature's (MTBDD, *BMD, WHDD, ...). Finitely
  many kinds; infinitely many parameters; the parameters are already
  classified (order 0025, polarity 0024, sharing 0027/here).
  Refutation surface: exhibit a diagonalising frame not conjugate
  into the grid -- the place to look is a NON-product basis or a
  non-abelian operator family, since the per-coordinate product case
  is closed by the enumeration above.

  WHERE COMPLEXITY FLOWS (the matrix, read as subclasses; C_F = the
  statements polynomial-size in frame F):

    C_minterm  SUBSET OF  C_OBDD          (path law -- stays P)
    C_ANF      SUBSET OF  C_FDD           (fiber law -- stays P)
    C_Walsh    inside quasipoly of C_ANF, hence of C_FDD
    C_OBDD  and  C_FDD    INCOMPARABLE    (wp / mux, both measured)
    C_minterm and C_Walsh CONJUGATE       (never both, past DS bound)
    every other move: exponential escape witnessed -- P becomes E.

  The P/E boundary is not a property of a problem; it is a property
  of a problem TOGETHER WITH a frame, and the matrix says exactly
  which frame changes preserve it. The two shared frames split the
  sentence basis between them: the OBDD side executes ALL connectives
  in polynomial time in its size but pays 2^straddle to receive
  parity-structured knowledge; the FDD side receives all of the ring
  frame linearly but conjunction on it is exponential in the worst
  case (decision-diagram literature). & lives on the Shannon side, ^
  on the Davio side -- the two-operator sentence basis {^, &} is
  exactly the pair of moves that the two sharings make cheap,
  one each. A Clue-like K (counting, thresholds: minterm-side) is
  poly on the OBDD; a Tseitin-like K (parity constraints: ANF-side)
  is poly on the FDD; a K needing both at once has no home frame --
  which is where the coNP-hardness of 0018 lives.""")


def run_verification_suite() -> None:
    show_zeta_conjugacy()
    show_transported_witness()
    show_flat_to_shared_square()
    show_flow_matrix()
    show_finiteness_and_complexity_flow()
    print()
    print("all frame-flow checks passed")


if __name__ == "__main__":
    run_verification_suite()
