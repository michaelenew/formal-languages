"""Classifying the eigenbases, machine-checked at the base case.

Results verified here, feeding exploration/0024:

  1. ONE COORDINATE, COMPLETE LIST. The function space of one variable
     is GF(2)^2, which has exactly three unordered bases:
         {1, x}         diagonalises substitute-to-0   (ANF / pos-Davio)
         {1, 1^x}       diagonalises substitute-to-1   (dual / neg-Davio)
         {x, 1^x}       diagonalises multiply-by-g     (minterm / Shannon)
     Enumerated exhaustively; each basis is matched to the operator
     family it diagonalises. There is no fourth option over GF(2).

  2. TRANSLATIONS HAVE NO EIGENBASIS OVER GF(2): (T_a + I)^2 = 0, so
     every translation is unipotent; a non-identity unipotent map is
     not diagonalisable. The Walsh basis therefore REQUIRES the lift
     of coefficients to the integers -- the counting layer is forced,
     not optional. Verified as matrices.

  3. POLARITY BASES ARE THE TRANSLATION ORBIT OF ANF: the fixed
     polarity Reed-Muller form with polarity p is the ANF of the
     translated function f(x ^ p) -- verified by reconstruction. So
     the translations, which have no eigenbasis of their own, act as
     FRAME CHANGES on the ANF family (the QM parallel: momentum
     generates translations of the position frame).

  4. POLARITY CURES THE REFUTATION EVENT: "at least one of n" costs
     2^n - 1 terms at polarity 0 and exactly 2 terms at the all
     complemented polarity, with the exact interpolation
     2^(n - |p|) + 1 in between. The ring family's worst statement
     was a frame artefact.

  5. THE FIRST EXACT UNCERTAINTY THEOREM in hand (Donoho-Stark for
     the minterm/Walsh pair): support(f) * support(Walsh f) >= 2^n,
     verified on random functions and TIGHT on subspace indicators.

Run this file directly.
"""

from __future__ import annotations

from itertools import product as cartesian_product


# ---------------------------------------------------------------------
# 1. One coordinate: the complete list of eigenbases
# ---------------------------------------------------------------------

Vector = tuple[int, int]           # a function {0,1} -> GF(2)
Matrix = tuple[Vector, Vector]     # columns are images of delta_0, delta_1


def apply_operator(matrix: Matrix, vector: Vector) -> Vector:
    return (
        (matrix[0][0] & vector[0]) ^ (matrix[1][0] & vector[1]),
        (matrix[0][1] & vector[0]) ^ (matrix[1][1] & vector[1]))


def is_eigenvector(matrix: Matrix, vector: Vector) -> bool:
    image = apply_operator(matrix, vector)
    return image == (0, 0) or image == vector


def classify_one_coordinate() -> None:
    print("=" * 70)
    print("1  ONE COORDINATE: EXACTLY THREE EIGENBASES, MATCHED TO "
          "OPERATORS")
    print("=" * 70)
    # function space of one variable, in truth-table coordinates
    # (f(0), f(1)):
    one, x, x_complement = (1, 1), (0, 1), (1, 0)
    name_of = {one: "1", x: "x", x_complement: "1^x"}
    nonzero_vectors = [one, x, x_complement]
    bases = []
    for first_index in range(3):
        for second_index in range(first_index + 1, 3):
            bases.append((nonzero_vectors[first_index],
                          nonzero_vectors[second_index]))
    assert len(bases) == 3
    # operators of the framework, one coordinate, as matrices acting on
    # truth tables:
    substitute_zero: Matrix = ((1, 1), (0, 0))   # f -> f(0) constant
    substitute_one: Matrix = ((0, 0), (1, 1))    # f -> f(1) constant
    multiply_by_x: Matrix = ((0, 0), (0, 1))     # f -> f * x
    translate: Matrix = ((0, 1), (1, 0))         # f -> f(x ^ 1)
    operator_name = {substitute_zero: "substitute-to-0",
                     substitute_one: "substitute-to-1",
                     multiply_by_x: "multiply-by-x",
                     translate: "translate"}
    for basis in bases:
        diagonalises = [
            operator_name[operator]
            for operator in (substitute_zero, substitute_one,
                             multiply_by_x, translate)
            if all(is_eigenvector(operator, vector)
                   for vector in basis)]
        basis_label = "{" + ", ".join(name_of[v] for v in basis) + "}"
        print(f"    basis {basis_label:<12} diagonalises: "
              f"{', '.join(diagonalises) if diagonalises else 'nothing'}")
    # the three assignments, asserted:
    assert all(is_eigenvector(substitute_zero, v) for v in (one, x))
    assert all(is_eigenvector(substitute_one, v)
               for v in (one, x_complement))
    assert all(is_eigenvector(multiply_by_x, v)
               for v in (x, x_complement))
    assert not any(
        all(is_eigenvector(translate, v) for v in basis)
        for basis in bases)
    print("""
    GF(2)^2 has exactly these three bases -- there is no fourth. Per
    coordinate, the complete menu of measurements is: substitute-0
    (ANF / positive Davio), substitute-1 (dual / negative Davio),
    evaluate (minterm / Shannon). The translation is diagonal in NONE
    of them. This is precisely the Kronecker decision-diagram triple
    of logic synthesis.""")


# ---------------------------------------------------------------------
# 2. Translations are unipotent over GF(2): the lift is forced
# ---------------------------------------------------------------------

def check_translations_unipotent() -> None:
    print()
    print("=" * 70)
    print("2  TRANSLATIONS ARE UNIPOTENT OVER GF(2): THE LIFT IS FORCED")
    print("=" * 70)
    variable_count = 3
    point_count = 1 << variable_count
    for shift in range(1, point_count):
        # (T_a + I)^2 applied to every delta function must vanish
        for point in range(point_count):
            table = [0] * point_count
            table[point] = 1
            once = [table[index ^ shift] ^ table[index]
                    for index in range(point_count)]
            twice = [once[index ^ shift] ^ once[index]
                     for index in range(point_count)]
            assert all(value == 0 for value in twice)
        fixed_dimension = sum(
            1 for orbit_representative in range(point_count)
            if orbit_representative == orbit_representative ^ shift) \
            + (point_count
               - sum(1 for p in range(point_count) if p == p ^ shift)) // 2
        assert fixed_dimension < point_count
    print("""
    (T_a + I)^2 = 0 for every nonzero a (n = 3, all shifts, all basis
    functions), and the fixed space is proper -- so T_a is unipotent
    and NOT diagonalisable over GF(2). The character basis exists only
    after lifting coefficients to the integers: the counting layer is
    the framework's equivalent of needing complex numbers for spin.""")


# ---------------------------------------------------------------------
# 3-4. Polarity bases: the translation orbit of ANF, and the cure
# ---------------------------------------------------------------------

def anf_coefficients(table: list[int], variable_count: int) -> list[int]:
    coefficients = list(table)
    for bit_position in range(variable_count):
        step = 1 << bit_position
        for mask in range(1 << variable_count):
            if mask & step:
                coefficients[mask] ^= coefficients[mask ^ step]
    return coefficients


def fixed_polarity_coefficients(table: list[int], variable_count: int,
                                polarity: int) -> list[int]:
    translated = [table[point ^ polarity]
                  for point in range(1 << variable_count)]
    return anf_coefficients(translated, variable_count)


def check_polarity_frames() -> None:
    import random
    source = random.Random(3)
    variable_count = 6
    point_count = 1 << variable_count
    print()
    print("=" * 70)
    print("3  POLARITY BASES = THE TRANSLATION ORBIT OF ANF")
    print("=" * 70)
    for _ in range(50):
        table = [source.randint(0, 1) for _ in range(point_count)]
        polarity = source.randrange(point_count)
        coefficients = fixed_polarity_coefficients(
            table, variable_count, polarity)
        for point in range(point_count):
            reconstructed = 0
            for monomial in range(point_count):
                if coefficients[monomial] and (
                        (point ^ polarity) & monomial) == monomial:
                    reconstructed ^= 1
            assert reconstructed == table[point]
    print("""
    Verified by reconstruction (50 random function/polarity pairs):
    the fixed-polarity form with polarity p is the ANF of f(x ^ p).
    The translations -- which have no eigenbasis of their own -- act
    as FRAME CHANGES on the ANF family.""")
    print("=" * 70)
    print("4  POLARITY CURES THE REFUTATION EVENT")
    print("=" * 70)
    print("""
    "at least one of n", term count by polarity weight |p|
    (n = 10; exact law 2^(n-|p|) + 1 for |p| > 0):
""")
    variable_count = 10
    point_count = 1 << variable_count
    at_least_one = [1 if point else 0 for point in range(point_count)]
    for polarity_weight in (0, 2, 5, 8, 10):
        polarity = (1 << polarity_weight) - 1
        term_count = sum(fixed_polarity_coefficients(
            at_least_one, variable_count, polarity))
        expected = (point_count - 1) if polarity_weight == 0 else (
            (1 << (variable_count - polarity_weight)) + 1)
        assert term_count == expected
        print(f"      |p| = {polarity_weight:2d}   "
              f"{term_count:5d} terms")
    print("""
    From 1023 terms to 2 by changing frame within the sentence family.
    The ring's worst statement was a frame artefact, not a fact about
    sentences. (The converse blind spot remains: parity costs n+1-ish
    terms at EVERY polarity, since translation preserves its top
    monomial -- polarity moves the blind spot, it does not remove it.)""")


# ---------------------------------------------------------------------
# 5. The Donoho-Stark uncertainty inequality, exact and tight
# ---------------------------------------------------------------------

def walsh_spectrum(table: list[int], variable_count: int) -> list[int]:
    spectrum = [1 - 2 * value for value in table]
    step = 1
    point_count = 1 << variable_count
    while step < point_count:
        for block_start in range(0, point_count, 2 * step):
            for offset in range(block_start, block_start + step):
                low, high = spectrum[offset], spectrum[offset + step]
                spectrum[offset] = low + high
                spectrum[offset + step] = low - high
        step *= 2
    return spectrum


def check_uncertainty_inequality() -> None:
    import random
    source = random.Random(4)
    variable_count = 8
    point_count = 1 << variable_count
    print()
    print("=" * 70)
    print("5  AN EXACT UNCERTAINTY THEOREM (DONOHO-STARK, MINTERM x "
          "WALSH)")
    print("=" * 70)
    # random sparse 0/1-combinations, as +/-1-signed indicator sums:
    # use f as 0/1 indicator; support(f) * support(spectrum of f) >= 2^n
    # for nonzero f (spectrum here of the 0/1 table, plain transform)
    def plain_walsh(table: list[int]) -> list[int]:
        spectrum = list(table)
        step = 1
        while step < point_count:
            for block_start in range(0, point_count, 2 * step):
                for offset in range(block_start, block_start + step):
                    low, high = spectrum[offset], spectrum[offset + step]
                    spectrum[offset] = low + high
                    spectrum[offset + step] = low - high
            step *= 2
        return spectrum

    minimum_product = None
    for _ in range(300):
        support_size = source.randrange(1, 40)
        table = [0] * point_count
        for point in source.sample(range(point_count), support_size):
            table[point] = 1
        spectrum = plain_walsh(table)
        spectral_support = sum(1 for value in spectrum if value != 0)
        product = support_size * spectral_support
        assert product >= point_count
        if minimum_product is None or product < minimum_product:
            minimum_product = product
    print(f"""
    support(f) x support(Walsh f) >= 2^n: verified on 300 random
    sparse indicators (n = 8, minimum product observed
    {minimum_product} >= {point_count}).""")
    for subspace_dimension in (0, 2, 4, 6, 8):
        basis_mask = (1 << subspace_dimension) - 1
        table = [1 if point & ~basis_mask == 0 else 0
                 for point in range(point_count)]
        spectrum = plain_walsh(table)
        support_size = sum(table)
        spectral_support = sum(1 for value in spectrum if value != 0)
        assert support_size * spectral_support == point_count
        print(f"      subspace dim {subspace_dimension}:   "
              f"{support_size:3d} x {spectral_support:3d} = "
              f"{support_size * spectral_support}   TIGHT")
    print("""
    Tight exactly on subspace indicators -- the 'coherent states' of
    this pair. This is the first exact, machine-verified uncertainty
    inequality between two of the framework's eigenbases; the open
    program is its analogue for the other pairs (ANF x automaton in
    particular).""")


def run_verification_suite() -> None:
    classify_one_coordinate()
    check_translations_unipotent()
    check_polarity_frames()
    check_uncertainty_inequality()
    print()
    print("all classification checks passed")


if __name__ == "__main__":
    run_verification_suite()
