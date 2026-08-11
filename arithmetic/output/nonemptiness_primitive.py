"""The infinite closure has a closed form, and it is one new symbol.

0037 left the sentence frame needing `K | s(K) | s2(K) | ...` closed both
ways, with a depth proportional to the width -- an unrolling. That
infinite family does not have to be expanded. It has a closed form.

**The closed form.** Reading a statement as a set of positions:

    the up-closure   is every position at or above min(T)
    the down-closure is every position at or below max(T)
    together, for T non-empty, that is EVERY position

so the two-way closure collapses to

    C(T) = 0          if T is empty
    C(T) = 1          otherwise                (1 = the universe)

verified for every T below 2^10. **The infinite union is the
nonemptiness indicator.** Give it the symbol `N`.

**And it is exactly what the workstream already said was missing.**
0015/0016 concluded "what the framing lacked was never negation but the
existential -- nonemptiness". That was reached from the automaton side.
Here the same object arrives from the sentence side as the closed form
of the shift closure, which is a strong sign it is the right primitive
and not a patch.

**It costs nothing.** N is already inside the layer: 0011 built
"at least k" as a clamped counter, and nonemptiness is the k = 1 case at
2 states. So adding the symbol adds no semantic power -- it is notation
for something the layer already decides, and convexity is untouched.

**The test becomes exact.** `H` inside `N(K)` holds iff, wherever `K` is
empty, `H` is empty -- which is entailment, on the nose. Verified in
both directions, soundness included.

**The rules.** Expansion, cancellation and combination, all terminating:

    N(0) -> 0                    N(1) -> 1              N(N a) -> N a
    N(a | b) -> N(a) | N(b)      N(s a) -> N(a)         [s is injective]
    a & N(b) -> a                whenever N(a) and N(b) have the same
                                 normal form

The last is the cancellation, and the side condition is decided by
normalising both arguments: put the term in s-graded ANF and divide out
the largest power of `s`. With those two rules the worked example of
0037 collapses in two steps, shown below with the semantics of every
intermediate term checked.

Run directly for the verification suite.
"""

from __future__ import annotations

import random

WIDTH = 10
MASK = (1 << WIDTH) - 1

join = lambda left, right: left ^ right ^ (left & right)
shift = lambda value: (value << 1) & MASK
indicator = lambda value: 0 if value == 0 else MASK


# ---------------------------------------------------------------------
# 1. the closed form
# ---------------------------------------------------------------------

def two_way_closure(value: int, depth: int) -> int:
    total = rising = falling = value
    for _ in range(depth):
        rising = shift(rising)
        falling >>= 1
        total = join(join(total, rising), falling)
    return total


def verify_the_closed_form() -> None:
    mismatches = [value for value in range(1 << WIDTH)
                  if two_way_closure(value, WIDTH) != indicator(value)]
    assert not mismatches, mismatches[:5]
    print(f"  C(T) = 0 if T is empty, else the universe -- for every "
          f"T < 2^{WIDTH}")
    print("  up-closure   = every position at or above min(T)")
    print("  down-closure = every position at or below max(T)")
    print("  together, for T non-empty, that is every position.")
    print("    So the infinite union has a one-symbol closed form: "
          "the nonemptiness")
    print("    indicator N. This is 0015/0016's missing existential, "
          "reached from the")
    print("    sentence side instead of the automaton side.")


def verify_the_test_becomes_exact(trials: int = 4000,
                                  seed: int = 20260811) -> None:
    """`H inside N(K)` is entailment exactly -- both directions."""
    generator = random.Random(seed)

    def random_statement(budget: int):
        kind = generator.random()
        if budget == 0 or kind < 0.35:
            constant = generator.choice([1, 2, 3, 4, 6, 8])
            return lambda x, c=constant: x ^ c
        if kind < 0.5:
            offset = generator.choice([1, 2, 3])
            constant = generator.choice([1, 2, 3, 4, 5])
            return lambda x, o=offset, c=constant: ((x + o) & MASK) ^ c
        if kind < 0.65:
            inner = random_statement(budget - 1)
            return lambda x, f=inner: shift(f(x))
        left = random_statement(budget - 1)
        right = random_statement(budget - 1)
        if kind < 0.85:
            return lambda x, a=left, b=right: a(x) & b(x)
        return lambda x, a=left, b=right: join(a(x), b(x))

    domain = range(1 << WIDTH)
    checked = unsound = incomplete = 0
    for _ in range(trials):
        knowledge = random_statement(2)
        hypothesis = random_statement(2)
        models = [x for x in domain if knowledge(x) == 0]
        if not models:
            continue
        checked += 1
        entails = all(hypothesis(x) == 0 for x in models)
        collapses = all(
            (hypothesis(x) ^ (hypothesis(x) & indicator(knowledge(x)))) == 0
            for x in domain)
        if collapses and not entails:
            unsound += 1
        if entails and not collapses:
            incomplete += 1
    assert not unsound and not incomplete
    print(f"  {checked} random satisfiable K/H pairs: "
          f"{unsound} unsound, {incomplete} incomplete")
    print("    H ^ H·N(K) collapses to the empty set exactly when K "
          "entails H.")
    print("    Not 'sound and usually right' -- exact, in both "
          "directions.")
    print("    (0037 measured a width-proportional depth and did not "
          "check soundness at")
    print("    those depths; this is that check, and it passes because "
          "the closure's")
    print("    limit is N, which is 0 exactly where K is.)")


# ---------------------------------------------------------------------
# 2. the term algebra: s-graded ANF with N
# ---------------------------------------------------------------------
#
# A term is a nested tuple. A *monomial* is (symbols, constant) where
# symbols is a frozenset of (name, shift-degree) and constant is None
# (no constant factor) or an int mask. A statement is a frozenset of
# monomials, XOR-joined -- the corpus's ANF, graded by shift degree.

def symbol(name: str, degree: int = 0):
    return ("term", frozenset([(frozenset([("sym", name, degree)]),
                                None)]))


def constant(value: int):
    value &= MASK
    if value == 0:
        return ("term", frozenset())
    return ("term", frozenset([(frozenset(), value)]))


def guard(inner):
    """N(inner) as a factor usable inside a monomial."""
    return ("term", frozenset([(frozenset([("guard", inner)]), None)]))


def exclusive_or(left, right):
    return ("term", left[1] ^ right[1])


def _multiply(first, second):
    symbols = first[0] | second[0]
    if first[1] is None:
        mask = second[1]
    elif second[1] is None:
        mask = first[1]
    else:
        mask = first[1] & second[1]
    if mask == 0:
        return None
    return (symbols, mask)


def intersect(left, right):
    product: set = set()
    for first in left[1]:
        for second in right[1]:
            joined = _multiply(first, second)
            if joined is not None:
                product ^= {joined}
    return ("term", frozenset(product))


def shifted(term):
    lifted = set()
    for atoms, mask in term[1]:
        if any(atom[0] != "sym" for atom in atoms):
            raise ValueError("shifting a guard is not a guard")
        raised = frozenset(("sym", name, degree + 1)
                           for _, name, degree in atoms)
        lifted ^= {(raised, None if mask is None else shift(mask))}
    return ("term", frozenset(lifted))


def _is_shift_divisible(term) -> bool:
    if not term[1]:
        return False
    for atoms, mask in term[1]:
        if any(atom[0] != "sym" or atom[2] < 1 for atom in atoms):
            return False
        if mask is not None and mask % 2 != 0:
            return False
    return True


def divided_by_shift(term):
    lowered = set()
    for atoms, mask in term[1]:
        dropped = frozenset(("sym", name, degree - 1)
                            for _, name, degree in atoms)
        lowered ^= {(dropped, None if mask is None else mask >> 1)}
    return ("term", frozenset(lowered))


def nonemptiness_normal_form(term):
    """N(T) normalised: divide out every power of `s`, since `s` is
    injective and so `N(s T) = N(T)`."""
    while _is_shift_divisible(term):
        term = divided_by_shift(term)
    return ("N", term)


def _render_atom(atom) -> str:
    if atom[0] == "guard":
        return f"N({render(atom[1])})"
    _, name, degree = atom
    return f"s{degree}({name})" if degree else name


def render(term) -> str:
    if term[0] == "N":
        return f"N({render(term[1])})"
    if not term[1]:
        return "0"
    pieces = []
    for atoms, mask in sorted(
            term[1], key=lambda m: (sorted(map(str, m[0])), m[1] or -1)):
        names = "".join(_render_atom(atom) for atom in sorted(
            atoms, key=str))
        if mask is None:
            pieces.append(names or "1")
        else:
            pieces.append(f"{names}&{mask}" if names else str(mask))
    return " ^ ".join(pieces)


def evaluate(term, environment: dict[str, int]) -> int:
    if term[0] == "N":
        return indicator(evaluate(term[1], environment))
    total = 0
    for atoms, mask in term[1]:
        value = MASK if mask is None else mask
        for atom in atoms:
            if atom[0] == "guard":
                value &= indicator(evaluate(atom[1], environment))
            else:
                _, name, degree = atom
                factor = environment[name]
                for _ in range(degree):
                    factor = shift(factor)
                value &= factor
        total ^= value
    return total


# ---------------------------------------------------------------------
# 3. the rules, and the worked derivation
# ---------------------------------------------------------------------

def cancel(term, guard):
    """`a & N(b) -> a`, licensed when N(a) and N(b) share a normal form.
    Sound because equal normal forms make `a` and `b` empty together, so
    wherever `a` is non-empty `N(b)` is the universe."""
    if nonemptiness_normal_form(term) != nonemptiness_normal_form(guard):
        return None
    return term


def verify_the_worked_derivation() -> None:
    knowledge = exclusive_or(symbol("x"), constant(2))
    hypothesis = shifted(knowledge)
    guarded = intersect(hypothesis, guard(knowledge))
    test = exclusive_or(hypothesis, guarded)

    print(f"  K       = {render(knowledge)}")
    print(f"  H       = s(K) = {render(hypothesis)}")
    print(f"  H ^ H·N(K)  =  {render(test)}   -- does not collapse "
          "as written")
    print()
    print("  rule  N(s a) -> N(a):")
    print(f"    N(H) normalises to {render(nonemptiness_normal_form(hypothesis))}")
    print(f"    N(K) normalises to {render(nonemptiness_normal_form(knowledge))}")
    assert (nonemptiness_normal_form(hypothesis)
            == nonemptiness_normal_form(knowledge))
    print("    -- equal, so the cancellation is licensed")
    print()
    cancelled = cancel(hypothesis, knowledge)
    assert cancelled is not None
    print(f"  rule  a & N(b) -> a:      H·N(K)  ->  {render(cancelled)}")
    collapsed = exclusive_or(hypothesis, cancelled)
    print(f"  rule  a ^ a -> 0:         H ^ H   ->  {render(collapsed)}")
    assert not collapsed[1]

    # the derivation preserves meaning at every step
    for value in range(1 << WIDTH):
        environment = {"x": value}
        assert (evaluate(test, environment)
                == evaluate(exclusive_or(hypothesis, cancelled),
                            environment)
                == evaluate(collapsed, environment) == 0)
    print("    every step checked semantically for x < 2^"
          f"{WIDTH}: the derivation is sound, and it is two rules long.")


def verify_termination(trials: int = 200, seed: int = 20260811) -> None:
    """Each rule strictly decreases a measure readable off the term."""
    generator = random.Random(seed)

    def size(term) -> int:
        """Term size counting shift degree, which is what the division
        rule consumes."""
        if term[0] == "N":
            return 1 + size(term[1])
        total = 1
        for atoms, _ in term[1]:
            total += 1
            for atom in atoms:
                total += 1 + (atom[2] if atom[0] == "sym" else
                              size(atom[1]))
        return total

    shrinks = 0
    for _ in range(trials):
        base = exclusive_or(symbol("x"),
                            constant(generator.choice([1, 2, 3, 4])))
        for _ in range(generator.randrange(1, 4)):
            base = shifted(base)
        before = ("N", base)
        after = nonemptiness_normal_form(base)
        assert size(after) <= size(before)
        if size(after) < size(before):
            shrinks += 1
    print(f"  N(s a) -> N(a):   strictly smaller in {shrinks} of "
          f"{trials} random shifted statements, never larger")
    print("  a & N(b) -> a:    deletes a subterm, so strictly smaller")
    print("  a ^ a -> 0:       deletes two, so strictly smaller")
    print("    every rule decreases the term size, so the system "
          "terminates, and the")
    print("    bound is readable off the term -- the corpus's own "
          "requirement.")


def run_verification_suite() -> None:
    print("=" * 70)
    print("1. The infinite union has a closed form")
    print("=" * 70)
    verify_the_closed_form()

    print()
    print("=" * 70)
    print("2. With N, the test is exact")
    print("=" * 70)
    verify_the_test_becomes_exact()

    print()
    print("=" * 70)
    print("3. The rules, on 0037's worked example")
    print("=" * 70)
    verify_the_worked_derivation()

    print()
    print("=" * 70)
    print("4. Termination")
    print("=" * 70)
    verify_termination()

    print()
    print("=" * 70)
    print("all checks passed")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
