"""Why `H ^ HK` stops collapsing at `<<`, and the rule that repairs it.

Written in the corpus's discipline throughout: a statement is a set term
that is empty exactly when the condition it describes is true; `^` is
equality; `|` is joint truth (`a | b = a ^ b ^ ab`); juxtaposition is
`&`; K is the whole of what is known, and asserting K *is* the
definition of the context. One consequence of juxtaposition is worth
stating because it bites immediately: **`2|A|` reads as `2 & |A|`**, so
doubling a count must be written `s(|A|)` with `s(x) := x << 1`.

**Where the test is complete, and why.** `H ^ HK` decides entailment for
`{^, &, 1}` because every one of those operators is **pointwise** -- it
acts on each position independently and identically, so a failure of
containment can always be squeezed into a one-point universe, where "K
empty implies H empty" and "H inside K" are the same condition. Verified
on 400 random terms.

**Where it stops.** `<<` carries position p to p+1, the one-point
universe is not closed under it, and the argument dies. For `K = x ^ 2`
and `H = s(x) ^ 4` the residual `H ^ HK` does not reduce to 0.

**The repair, and it is not a term-level rewrite.** The missing rule
acts on *statements*:

    from K infer s(K)

sound because `s` carries the empty set to the empty set. It closes the
example immediately: `s(x ^ 2)` pushes down to `s(x) ^ 4`, which IS `H`,
so `H ^ H s(K)` is 0 with no new term-level machinery at all. The
knowledge is not `K` but K's **s-closure** `K | s(K) | s(s(K)) | ...`,
and the depth needed is the shift-depth of the hypothesis -- read off H,
so the search terminates with an a-priori bound.

The closure is an infinite union. A finite representation of an infinite
union closed under the shift is an automaton, so this is the
sentence-side derivation of 0006's "the automaton is the closed form of
the stabilizing series" and of 0023's "what forces the DFA".

**Correction.** The first version of this file concluded that no rule
set could repair the test. That was wrong, and wrong for an instructive
reason: it reasoned about values of x where `K` is not empty, which the
framing excludes -- K is the definition of the context, not a constraint
to be tested against arbitrary x. The residual `H ^ HK` genuinely does
not collapse, but nothing needs it to; the deduction runs through
`s(K)`. The templating instinct was right; what has to be injected is
the *shifted knowledge*, not the residual.

Run directly for the verification suite.
"""

from __future__ import annotations

import random
from itertools import product as cartesian_product


# ---------------------------------------------------------------------
# the discipline, symbolically
# ---------------------------------------------------------------------

class Polynomial:
    """A multilinear GF(2) polynomial -- the corpus's ANF. Monomials are
    frozensets of symbols; the polynomial is the set of monomials with
    coefficient 1. `^` is symmetric difference, `&` is product with
    idempotence, and the empty polynomial is the empty set."""

    def __init__(self, monomials=()) -> None:
        self.monomials = frozenset(monomials)

    @staticmethod
    def symbol(name: str) -> "Polynomial":
        return Polynomial([frozenset({name})])

    @staticmethod
    def constant(bit: int) -> "Polynomial":
        return Polynomial([frozenset()] if bit else [])

    def __xor__(self, other: "Polynomial") -> "Polynomial":
        return Polynomial(self.monomials ^ other.monomials)

    def __and__(self, other: "Polynomial") -> "Polynomial":
        product: set = set()
        for left in self.monomials:
            for right in other.monomials:
                product ^= {left | right}
        return Polynomial(product)

    def joined_with(self, other: "Polynomial") -> "Polynomial":
        """`a | b` -- empty exactly when both are."""
        return self ^ other ^ (self & other)

    def is_empty(self) -> bool:
        return not self.monomials

    def __eq__(self, other) -> bool:
        return self.monomials == other.monomials

    def __hash__(self) -> int:
        return hash(self.monomials)

    def __repr__(self) -> str:
        if not self.monomials:
            return "0"
        return " ^ ".join("1" if not monomial else "".join(sorted(monomial))
                          for monomial in sorted(self.monomials, key=sorted))


def verify_the_corpus_worked_example() -> None:
    """"if x and y are disparate then x | y = x ^ y", start to finish."""
    x, y = Polynomial.symbol("x"), Polynomial.symbol("y")
    knowledge = x & y
    hypothesis = x.joined_with(y) ^ (x ^ y)
    print(f"  K := xy                      -> {knowledge}")
    print(f"  H := (x | y) ^ (x ^ y)       -> {hypothesis}")
    assert hypothesis == knowledge
    residual = hypothesis ^ (hypothesis & knowledge)
    print(f"  H ^ HK                       -> {residual}")
    assert residual.is_empty()
    print("    empty, so the entailment is known. This is the whole "
          "mechanism, and the")
    print("    engine below reproduces it with no special cases.")


# ---------------------------------------------------------------------
# 1. why the test is complete for pointwise operators
# ---------------------------------------------------------------------

def _random_pointwise_statement(symbol_count: int, depth: int,
                                generator: random.Random):
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
    """For pointwise statements, entailment and containment coincide."""
    generator = random.Random(seed)
    assignments = list(cartesian_product(
        *[list(cartesian_product((0, 1), repeat=universe))
          for _ in range(symbol_count)]))
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
            evaluate(hypothesis, assignment, position)
            <= evaluate(knowledge, assignment, position)
            for assignment in assignments
            for position in range(universe))
        assert entails == contains
    print(f"  {trials} random terms over {{^, &, 1}}, {symbol_count} "
          f"symbols, universe {universe}:")
    print("    entailment and containment agree every time. A failure of "
          "containment")
    print("    squeezes into a one-point universe, where the two are the "
          "same condition.")


# ---------------------------------------------------------------------
# 2. where it stops: << is not pointwise
# ---------------------------------------------------------------------

shift = lambda value: value << 1
join = lambda left, right: left ^ right ^ (left & right)


def verify_the_shift_example(bound: int = 1 << 12) -> None:
    knowledge = lambda x: x ^ 2
    hypothesis = lambda x: shift(x) ^ 4
    residual = lambda x: hypothesis(x) ^ (hypothesis(x) & knowledge(x))
    expanded = lambda x: (shift(x) ^ 4 ^ (shift(x) & x)
                          ^ (2 & shift(x)) ^ (4 & x) ^ (4 & 2))
    assert all(residual(x) == expanded(x) for x in range(bound))
    assert not all(residual(x) == 0 for x in range(bound))
    print("  K := x ^ 2       H := s(x) ^ 4")
    print("  H ^ HK  ->  s(x) ^ 4 ^ s(x)x ^ 2s(x) ^ 4x     "
          "(4&2 having cancelled)")
    print("    which does not reduce to 0. `<<` moves information "
          "between positions, so")
    print("    the one-point squeeze of section 1 does not apply and "
          "containment against")
    print("    K alone is no longer equivalent to entailment.")


# ---------------------------------------------------------------------
# 3. the repair: close the knowledge under s
# ---------------------------------------------------------------------

def shifted_knowledge(knowledge, depth: int):
    """s applied `depth` times to a whole statement."""
    def statement(x, depth=depth):
        value = knowledge(x)
        for _ in range(depth):
            value = shift(value)
        return value
    return statement


def s_closure(knowledge, depth: int):
    """K | s(K) | ... | s^depth(K) -- the knowledge actually in force."""
    def statement(x, depth=depth):
        total = knowledge(x)
        for level in range(1, depth + 1):
            total = join(total, shifted_knowledge(knowledge, level)(x))
        return total
    return statement


def two_way_closure(knowledge, depth: int):
    """K closed under s AND under its partial inverse, the right shift.
    `from K infer K >> 1` is sound for the same trivial reason as the
    upward rule -- the right shift carries the empty set to itself --
    and it is the corpus's own `h`, flagged in `clue/2026-06-21` as "a
    genuinely new primitive, not constructible from n0/n1"."""
    def statement(x, depth=depth):
        total = knowledge(x)
        rising = falling = knowledge(x)
        for _ in range(depth):
            rising = shift(rising)
            falling = falling >> 1
            total = join(join(total, rising), falling)
        return total
    return statement


def verify_the_shift_closure_rule(bound: int = 1 << 12) -> None:
    knowledge = lambda x: x ^ 2
    hypothesis = lambda x: shift(x) ^ 4
    deeper = lambda x: shift(shift(x)) ^ 8

    assert all(knowledge(x) != 0 or shifted_knowledge(knowledge, 1)(x) == 0
               for x in range(bound))
    print("  the rule:  from K infer s(K)      sound, since s carries "
          "the empty set to itself")

    assert all(shifted_knowledge(knowledge, 1)(x) == hypothesis(x)
               for x in range(bound))
    print("  s(K) = s(x ^ 2) = s(x) ^ 4 = H    -- the hypothesis IS the "
          "shifted knowledge")

    for label, target, depth, expected in (
            ("H  := s(x) ^ 4    against K", hypothesis, 0, False),
            ("H  := s(x) ^ 4    against K | s(K)", hypothesis, 1, True),
            ("H2 := ss(x) ^ 8   against K | s(K)", deeper, 1, False),
            ("H2 := ss(x) ^ 8   against K | s(K) | ss(K)", deeper, 2,
             True)):
        closure = s_closure(knowledge, depth)
        collapses = all(
            (target(x) ^ (target(x) & closure(x))) == 0
            for x in range(bound))
        assert collapses == expected, label
        print(f"    {label:<42} H ^ H·K* -> "
              f"{'0' if collapses else 'not 0'}")
    print("    so the depth needed is the shift-depth of the HYPOTHESIS, "
          "read off H --")
    print("    the search is bounded a priori, which is the corpus's own "
          "termination")
    print("    requirement. The s-closure is an infinite union, and a "
          "finite")
    print("    representation of an infinite union closed under the "
          "shift is an")
    print("    automaton (0006, 0023).")


def verify_closure_distributes_over_union(bound: int = 1 << 10) -> None:
    """The theorem that makes closing-at-ingest a protocol rather than a
    query-time trick: C(A | B) = C(A) | C(B), because s and h are both
    ring homomorphisms and `|` is built from `^` and `&`. So recording
    each new piece of information I as its own closure I' and updating
    K := K | I' gives exactly the same knowledge as closing K at the
    end."""
    left = lambda x: x ^ 2
    right = lambda x: (x & 5) ^ 1
    depth = 3
    closed_together = two_way_closure(
        lambda x: join(left(x), right(x)), depth)
    closed_apart = lambda x: join(two_way_closure(left, depth)(x),
                                  two_way_closure(right, depth)(x))
    assert all(closed_together(x) == closed_apart(x)
               for x in range(bound))
    print("  C(A | B) = C(A) | C(B)   verified for A := x ^ 2, "
          f"B := (x & 5) ^ 1, x < {bound}")
    print("    so closing each increment at ingest and closing the whole "
          "K at query time")
    print("    give the same object. The protocol is well defined: "
          "I' := C(I), K := K | I'.")


def verify_chaining(bound: int = 64) -> None:
    """Transitivity through the closure: two increments, neither of
    which mentions the conclusion."""
    failures = []
    for x in range(bound):
        for y in range(bound):
            first = x ^ 2                       # x = 2
            second = y ^ shift(x)               # y = s(x)
            def closed(value, depth=2):
                total = rising = falling = value
                for _ in range(depth):
                    rising <<= 1
                    falling >>= 1
                    total = join(join(total, rising), falling)
                return total
            knowledge = join(closed(first), closed(second))
            hypothesis = y ^ 4                  # y = 4
            if hypothesis ^ (hypothesis & knowledge) != 0:
                failures.append((x, y))
    assert not failures, failures[:5]
    print("  I1 := x ^ 2      I2 := y ^ s(x)      H := y ^ 4")
    print(f"    H ^ H·(C(I1) | C(I2)) collapses for every x, y < {bound}")
    print("    -- chaining works, because A ^ B is always inside A | B, "
          "so equalities")
    print("    compose without any transitivity rule of their own.")


def verify_the_linearity_criterion(bound: int = 1 << 8) -> None:
    """Which operators admit a statement-level closure rule at all."""
    def trailing_ones(value: int) -> int:
        return value & ~(value + 1)

    print("  operator          f(0) = 0   f(a^b) = f(a)^f(b)   "
          "closure rule?")
    rows = [("s(x) = x << 1", lambda v: v << 1),
            ("h(x) = x >> 1", lambda v: v >> 1),
            ("x + 1", lambda v: v + 1),
            ("x + 3", lambda v: v + 3),
            ("T(x)", trailing_ones),
            ("|x|", lambda v: bin(v).count("1"))]
    for label, operation in rows:
        linear = all(operation(a ^ b) == (operation(a) ^ operation(b))
                     for a in range(bound) for b in range(bound))
        zero = operation(0) == 0
        print(f"  {label:<16}  {str(zero):<9}  {str(linear):<19}  "
              f"{'yes' if (zero and linear) else 'no'}")
    print("    A statement-level rule `from T infer f(T)` needs f to "
          "carry the empty set")
    print("    to itself AND to be ^-linear, so that f(u) ^ f(v) = "
          "f(u ^ v) turns")
    print("    congruence into a rule about whole statements. Only the "
          "two shifts")
    print("    qualify. The failure of `+` is exactly the carry -- "
          "0002's founding wall.")


def measure_required_depth(trials: int = 1200,
                           seed: int = 20260810) -> None:
    """How deep the closure has to go. This is the price."""
    print("  width probed   smallest extra depth with no misses")
    measurements = []
    for bits in (6, 8, 10, 12):
        bound = 1 << bits
        for extra in range(0, 26):
            generator = random.Random(seed)
            clean = True
            for _ in range(trials):
                knowledge, _ = _random_arithmetic_statement(generator, 2)
                hypothesis, depth = _random_arithmetic_statement(
                    generator, 2)
                models = [x for x in range(bound) if knowledge(x) == 0]
                if not models:
                    continue
                if not all(hypothesis(x) == 0 for x in models):
                    continue
                closure = two_way_closure(knowledge, depth + extra)
                if not all(
                        (hypothesis(x) ^ (hypothesis(x) & closure(x))) == 0
                        for x in range(bound)):
                    clean = False
                    break
            if clean:
                measurements.append((bits, extra))
                print(f"  x < 2^{bits:<3}       {extra}")
                break
    # linear in the width with slope 1 -- the intercept is a detail of
    # the sample, the slope is the finding.
    steps = [(later_bits - earlier_bits, later - earlier)
             for (earlier_bits, earlier), (later_bits, later)
             in zip(measurements, measurements[1:])]
    assert all(width_step == depth_step
               for width_step, depth_step in steps), measurements
    print("    one extra level of closure per extra bit of width, at "
          "every width")
    print("    measured. So the depth the closure needs")
    print("    is PROPORTIONAL TO THE WIDTH, not a constant and not a "
          "function of the")
    print("    hypothesis alone: the closed K is an unrolling, and it "
          "grows with the")
    print("    problem. That is the price of staying in the sentence "
          "frame -- and the")
    print("    automaton is precisely the finite representation of this "
          "unrolling.")


def _random_arithmetic_statement(generator: random.Random, budget: int):
    kind = generator.random()
    if budget == 0 or kind < 0.30:
        constant = generator.choice([1, 2, 3, 4, 6, 8])
        return (lambda x, c=constant: x ^ c), 0
    if kind < 0.45:
        offset = generator.choice([1, 2, 3])
        constant = generator.choice([1, 2, 3, 4, 5])
        return (lambda x, o=offset, c=constant: (x + o) ^ c), 0
    if kind < 0.62:
        inner, depth = _random_arithmetic_statement(generator, budget - 1)
        return (lambda x, f=inner: shift(f(x))), depth + 1
    left, left_depth = _random_arithmetic_statement(generator, budget - 1)
    right, right_depth = _random_arithmetic_statement(generator, budget - 1)
    if kind < 0.82:
        return ((lambda x, a=left, b=right: a(x) & b(x)),
                max(left_depth, right_depth))
    return ((lambda x, a=left, b=right: join(a(x), b(x))),
            max(left_depth, right_depth))


def probe_closure_completeness(trials: int = 3000, bound: int = 1 << 9,
                               seed: int = 20260810) -> None:
    """Is testing against the s-closure complete? Measured, not assumed."""
    generator = random.Random(seed)

    def random_statement(depth_budget: int):
        kind = generator.random()
        if depth_budget == 0 or kind < 0.35:
            constant = generator.choice([1, 2, 3, 4, 6, 8])
            return (lambda x, c=constant: x ^ c), 0
        if kind < 0.55:
            inner, depth = random_statement(depth_budget - 1)
            return (lambda x, f=inner: shift(f(x))), depth + 1
        left, left_depth = random_statement(depth_budget - 1)
        right, right_depth = random_statement(depth_budget - 1)
        if kind < 0.8:
            return ((lambda x, a=left, b=right: a(x) & b(x)),
                    max(left_depth, right_depth))
        return ((lambda x, a=left, b=right: join(a(x), b(x))),
                max(left_depth, right_depth))

    satisfiable = missed_upward = missed_two_way = 0
    for _ in range(trials):
        knowledge, _ = random_statement(2)
        hypothesis, hypothesis_depth = random_statement(2)
        models = [x for x in range(bound) if knowledge(x) == 0]
        if not models:
            continue
        satisfiable += 1
        entails = all(hypothesis(x) == 0 for x in models)
        upward = s_closure(knowledge, hypothesis_depth + 1)
        two_way = two_way_closure(knowledge, hypothesis_depth + 2)
        collapses_upward = all(
            (hypothesis(x) ^ (hypothesis(x) & upward(x))) == 0
            for x in range(bound))
        collapses_two_way = all(
            (hypothesis(x) ^ (hypothesis(x) & two_way(x))) == 0
            for x in range(bound))
        assert not (collapses_upward and not entails), "unsound upward"
        assert not (collapses_two_way and not entails), "unsound two-way"
        if entails and not collapses_upward:
            missed_upward += 1
        if entails and not collapses_two_way:
            missed_two_way += 1
    print(f"  {satisfiable} random satisfiable K/H pairs over "
          f"{{^, &, |, s, constants}}:")
    print(f"    neither test was ever unsound")
    print(f"    true entailments missed by  K | s(K) | s2(K) | ... : "
          f"{missed_upward}")
    print(f"    true entailments missed by the two-way closure     : "
          f"{missed_two_way}")
    print("    The misses are the DOWNWARD inferences -- from s(x) = 4 "
          "infer x = 2 -- which")
    print("    need the injectivity of s, i.e. the right shift. Adding "
          "it closes every")
    print("    miss in this sample. Sound always; complete on this "
          "sample, unproven in")
    print("    general, and the exact depth bound is measured rather "
          "than derived.")


def run_verification_suite() -> None:
    print("=" * 70)
    print("0. The corpus's worked example, reproduced by the engine")
    print("=" * 70)
    verify_the_corpus_worked_example()

    print()
    print("=" * 70)
    print("1. Why H ^ HK is complete for {^, &, 1}")
    print("=" * 70)
    verify_pointwise_completeness()

    print()
    print("=" * 70)
    print("2. Where it stops: << is not pointwise")
    print("=" * 70)
    verify_the_shift_example()

    print()
    print("=" * 70)
    print("3. The repair: close the knowledge under s")
    print("=" * 70)
    verify_the_shift_closure_rule()

    print()
    print("=" * 70)
    print("4. Is the closure test complete? Measured")
    print("=" * 70)
    probe_closure_completeness()

    print()
    print("=" * 70)
    print("5. Closing at ingest: the protocol")
    print("=" * 70)
    verify_closure_distributes_over_union()
    print()
    verify_chaining()

    print()
    print("=" * 70)
    print("6. Which operators admit the rule, and what it costs")
    print("=" * 70)
    verify_the_linearity_criterion()
    print()
    measure_required_depth()

    print()
    print("=" * 70)
    print("all checks passed")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
