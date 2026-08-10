"""Why `KH ^ H` stops collapsing once an operator is not pointwise.

Written in the corpus's own discipline: a statement is a set term
asserted empty, `^` is equality, `|` is joint truth (`a | b = a ^ b ^
ab`, empty exactly when both are), and juxtaposition is `&`. Note the
consequence of that last convention: `2|A|` reads as `2 & |A|`, so
*doubling* a count has to be written `s(|A|)` with `s(x) := x << 1`.
Every formula below respects that.

**The finding.** The corpus's test `KH ^ H` -- reduce and look for the
empty set -- is complete for `{^, &, 1}` for a specific reason: every
one of those operators is **pointwise**. It acts on each position
independently and identically, so a counterexample can always be
squeezed into a one-point universe, and there entailment and containment
are the same condition. That is why the test worked so well and why it
was reasonable to trust.

`<<` is the first operator that is not pointwise: it carries position
`p` to position `p+1`. The one-point universe is not closed under it,
the squeezing argument dies, and the test loses completeness. Concretely,
for `K = x ^ 2` and `H = s(x) ^ 4`:

    the entailment  K = 0  =>  H = 0    holds
    the containment H subset K          FAILS, at x = 0 among others
    KH ^ H                              is 4, 4, 0, 2, 8, ... not empty

So the residual `s(x) ^ 4 ^ s(x)x ^ 2s(x) ^ 4x` **is not knowably
empty**, and no rewrite rule can make it collapse: a rule that collapsed
it would be unsound, since the term is genuinely `4` at `x = 0`. The
missing thing was never the rule set. It is the test.

**What does work, and it is one line.** Index the statement by position.
`K = 0` is not one equation but one per position: `K_i = x_i ^ c_i`. The
shift acts on the *system* by relabelling the index -- `s`'s per-position
equations are `H_i = s_i ^ d_i` with `s_i = x_{i-1}` -- and then

    H_i = K_{i-1}      exactly, as polynomials

so `H` reduces to `K` shifted by one and thence to the empty set. That
identity is verified below. Reverse-engineering the automaton's shift
into the ANF frame therefore yields an operation on the *indexed family*
of equations, not a new axiom inside a term -- which is exactly what an
automaton is, and why 0023 found the DFA forced by the same theorem that
forced `<<`.

**On the "templating" idea.** Injecting the residual as an implied axiom
would be unsound in precisely the way above: it is true at `x = 2` and
false at `x = 0`, so adopting it lets one derive falsehoods. The sound
form of the same instinct is reduction modulo the ideal of the shift's
*position-indexed* relations (`s_0`, and `s_{i+1} ^ x_i`), which is a
Gröbner basis question -- and 0020 already identified expand-and-cancel
as Polynomial Calculus over GF(2), which is exactly the proof system for
ideal membership. The relations are finite per width and infinite over
all widths, which is the precise reason no finite position-free rule set
exists.

Run directly for the verification suite.
"""

from __future__ import annotations

import random
from itertools import product as cartesian_product


# ---------------------------------------------------------------------
# the corpus's discipline, on concrete bitsets
# ---------------------------------------------------------------------

def joint(left: int, right: int) -> int:
    """`a | b` -- empty exactly when both are. The corpus's union."""
    return left ^ right ^ (left & right)


def shift(value: int) -> int:
    """s(x) := x << 1, the corpus's n0/inc."""
    return value << 1


def size(value: int) -> int:
    return bin(value).count("1")


def verify_the_balance_pair_in_the_discipline(bound: int = 1 << 6) -> None:
    """0036 wrote 'under disjointness' as prose. In the discipline it is
    a conjunct, and the two statements are these terms."""
    first = lambda a, b: joint(size(a) ^ size(b), a & b)
    second = lambda a, b: joint(size(a ^ b) ^ shift(size(a)), a & b)

    pairs = [(a, b) for a in range(bound) for b in range(bound)]
    disagreements = [(a, b) for a, b in pairs
                     if (first(a, b) == 0) != (second(a, b) == 0)]
    assert not disagreements, disagreements[:5]
    print("  (|A| ^ |B|) | (A&B)          and   (|A^B| ^ s(|A|)) | (A&B)")
    print(f"    same zero set, exhaustively for A, B < {bound}: yes")

    witness = next((a, b) for a, b in pairs
                   if first(a, b) ^ second(a, b) != 0)
    a, b = witness
    print(f"  but their XOR is NOT identically empty: at A = {a}, B = {b}"
          f" it is {first(a, b) ^ second(a, b)}")
    print("    so the syntactic identity")
    print("      ((|A| ^ |B|) | (A&B)) ^ ((|A^B| ^ s(|A|)) | (A&B))")
    print("    does not reduce to 0. Same models, different terms -- "
          "which is the same")
    print("    phenomenon as the shift example below, not a slip.")


# ---------------------------------------------------------------------
# 1. why the test is complete for pointwise operators
# ---------------------------------------------------------------------

def _random_pointwise_statement(symbol_count: int, depth: int,
                                generator: random.Random):
    """A random term over {^, &, 1} in `symbol_count` symbols, as a
    Boolean function of the symbols' membership bits at one position."""
    if depth == 0:
        choice = generator.randrange(symbol_count + 1)
        if choice == symbol_count:
            return lambda bits: 1
        return lambda bits, index=choice: bits[index]
    left = _random_pointwise_statement(symbol_count, depth - 1, generator)
    right = _random_pointwise_statement(symbol_count, depth - 1, generator)
    if generator.random() < 0.5:
        return lambda bits: left(bits) ^ right(bits)
    return lambda bits: left(bits) & right(bits)


def verify_pointwise_completeness(trials: int = 400, symbol_count: int = 3,
                                  universe: int = 4,
                                  seed: int = 20260809) -> None:
    """For pointwise statements, entailment and containment are the same
    condition -- which is why `KH ^ H` was complete."""
    generator = random.Random(seed)
    assignments = list(cartesian_product(
        *[list(cartesian_product((0, 1), repeat=universe))
          for _ in range(symbol_count)]))
    checked = 0
    for _ in range(trials):
        knowledge = _random_pointwise_statement(symbol_count, 2, generator)
        hypothesis = _random_pointwise_statement(symbol_count, 2, generator)

        def evaluate(statement, assignment, position):
            return statement([assignment[symbol][position]
                              for symbol in range(symbol_count)])

        entails = all(
            not all(evaluate(knowledge, assignment, position) == 0
                    for position in range(universe))
            or all(evaluate(hypothesis, assignment, position) == 0
                   for position in range(universe))
            for assignment in assignments)
        contains = all(
            evaluate(hypothesis, assignment, position) <= evaluate(
                knowledge, assignment, position)
            for assignment in assignments
            for position in range(universe))
        assert entails == contains, "pointwise completeness failed"
        checked += 1
    print(f"  {checked} random statements over {{^, &, 1}}, "
          f"{symbol_count} symbols, universe {universe}:")
    print("    entailment and containment agree every time.")
    print("    Reason: a counterexample can be squeezed into a one-point "
          "universe, where")
    print("    'K is empty implies H is empty' and 'H is inside K' are "
          "the same condition.")


# ---------------------------------------------------------------------
# 2. where it breaks: the shift is not pointwise
# ---------------------------------------------------------------------

def verify_the_shift_example(bound: int = 1 << 12) -> None:
    """The corpus's own worked case, computed rather than assumed."""
    knowledge = lambda x: x ^ 2
    hypothesis = lambda x: shift(x) ^ 4
    residual = lambda x: (hypothesis(x) & knowledge(x)) ^ hypothesis(x)

    expanded = lambda x: (shift(x) ^ 4 ^ (shift(x) & x)
                          ^ (2 & shift(x)) ^ (4 & x) ^ (4 & 2))
    assert all(residual(x) == expanded(x) for x in range(bound))

    print("   x   K = x^2   H = s(x)^4   H inside K   KH ^ H")
    for x in range(6):
        inside = (hypothesis(x) & knowledge(x)) == hypothesis(x)
        print(f"  {x:>2}   {knowledge(x):>7}   {hypothesis(x):>9}   "
              f"{str(inside):>10}   {residual(x)}")

    entails = all(knowledge(x) != 0 or hypothesis(x) == 0
                  for x in range(bound))
    contains = all(
        (hypothesis(x) & knowledge(x)) == hypothesis(x)
        for x in range(bound))
    empty = all(residual(x) == 0 for x in range(bound))
    assert entails and not contains and not empty
    print(f"  entailment holds ({entails}), containment fails "
          f"({contains}), KH^H identically empty ({empty})")
    print("    So the residual is not knowably empty -- it is 4 at x = 0."
          " No rewrite rule")
    print("    can collapse it, because collapsing it would be unsound. "
          "The test lost")
    print("    completeness, and the rule set was never the missing "
          "piece.")


# ---------------------------------------------------------------------
# 3. what does work: index by position
# ---------------------------------------------------------------------

class Polynomial:
    """A multilinear GF(2) polynomial -- the corpus's ANF. Monomials are
    frozensets of variable names; the polynomial is the set of monomials
    with coefficient 1."""

    def __init__(self, monomials=()) -> None:
        self.monomials = frozenset(monomials)

    @staticmethod
    def variable(name: str) -> "Polynomial":
        return Polynomial([frozenset({name})])

    @staticmethod
    def constant(bit: int) -> "Polynomial":
        return Polynomial([frozenset()] if bit else [])

    def __xor__(self, other: "Polynomial") -> "Polynomial":
        return Polynomial(self.monomials ^ other.monomials)

    def __and__(self, other: "Polynomial") -> "Polynomial":
        product = set()
        for left in self.monomials:
            for right in other.monomials:
                joined = left | right          # idempotence: x & x = x
                product ^= {joined}
        return Polynomial(product)

    def __eq__(self, other) -> bool:
        return self.monomials == other.monomials

    def __hash__(self) -> int:
        return hash(self.monomials)

    def __repr__(self) -> str:
        if not self.monomials:
            return "0"
        return " ^ ".join(
            "1" if not monomial else "".join(sorted(monomial))
            for monomial in sorted(self.monomials, key=sorted))


def verify_position_indexed_reduction(width: int = 6) -> None:
    """`K = 0` is one equation per position, and the shift relabels the
    index. Then the deduction is one line."""
    constant_two, constant_four = 2, 4

    # K_i = x_i ^ (bit i of 2)
    knowledge = [Polynomial.variable(f"x{i}")
                 ^ Polynomial.constant((constant_two >> i) & 1)
                 for i in range(width)]
    # s_i = x_{i-1}, with s_0 = 0
    shifted = [Polynomial.constant(0) if i == 0
               else Polynomial.variable(f"x{i - 1}") for i in range(width)]
    # H_i = s_i ^ (bit i of 4)
    hypothesis = [shifted[i]
                  ^ Polynomial.constant((constant_four >> i) & 1)
                  for i in range(width)]

    print(f"    i   K_i          H_i          K_(i-1)")
    for i in range(width):
        previous = knowledge[i - 1] if i >= 1 else Polynomial.constant(0)
        print(f"    {i}   {str(knowledge[i]):<12} {str(hypothesis[i]):<12} "
              f"{previous}")
    for i in range(width):
        previous = knowledge[i - 1] if i >= 1 else Polynomial.constant(0)
        assert hypothesis[i] == previous, (i, hypothesis[i], previous)
    print("    H_i = K_(i-1) exactly, at every position -- so H reduces "
          "to K shifted by")
    print("    one index, and thence to the empty set. The shift acts on "
          "the INDEXED")
    print("    FAMILY of equations by relabelling, not inside a term by "
          "a new axiom.")
    print("    A finite description of an indexed family with a shift "
          "action is an")
    print("    automaton, which is why 0023 found the DFA forced by the "
          "theorem that")
    print("    forced <<.")


def verify_templating_would_be_unsound() -> None:
    """The proposed repair, assessed on its own terms."""
    residual = lambda x: ((shift(x) ^ 4) & (x ^ 2)) ^ (shift(x) ^ 4)
    true_at = [x for x in range(16) if residual(x) == 0]
    false_at = [x for x in range(16) if residual(x) != 0]
    print(f"  the residual vanishes at x in {true_at} and not at "
          f"x in {false_at[:6]}...")
    print("    Adopting it as an implied axiom therefore asserts "
          "something false at x = 0,")
    print("    and anything follows. The sound version of the same "
          "instinct is reduction")
    print("    modulo the ideal of the shift's position-indexed "
          "relations (s_0, and")
    print("    s_(i+1) ^ x_i) -- a Groebner basis, and 0020 already "
          "identified")
    print("    expand-and-cancel as Polynomial Calculus over GF(2), the "
          "proof system for")
    print("    ideal membership. Those relations are finite per width "
          "and infinite over")
    print("    all widths, which is exactly why no finite "
          "position-FREE rule set exists.")


def run_verification_suite() -> None:
    print("=" * 70)
    print("0. The balance pair, written in the discipline")
    print("=" * 70)
    verify_the_balance_pair_in_the_discipline()

    print()
    print("=" * 70)
    print("1. Why KH ^ H is complete for {^, &, 1}")
    print("=" * 70)
    verify_pointwise_completeness()

    print()
    print("=" * 70)
    print("2. Where it breaks: << is not pointwise")
    print("=" * 70)
    verify_the_shift_example()

    print()
    print("=" * 70)
    print("3. What does work: index by position")
    print("=" * 70)
    verify_position_indexed_reduction()

    print()
    print("=" * 70)
    print("4. The templating proposal, assessed")
    print("=" * 70)
    verify_templating_would_be_unsound()

    print()
    print("=" * 70)
    print("all checks passed")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
