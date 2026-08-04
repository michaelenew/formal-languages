"""Addition under semantic convexity, on numbers-as-bitsets.

Encoding: a finite set S of naturals is the number n(S) = sum(2^i for i in S).
The empty set is 0. Python ints are the representation; bitwise ops are the
set operators (^ = symmetric difference / XOR, & = intersection / AND).

Primitive operators of the syntax:
    a(x) = 2x       (shift left, fill 0)
    b(x) = 2x + 1   (shift left, fill 1)

Everything below is built from {^, &, a, b, finite constants} plus one
syntax-level construct: the *stabilizing series* — an iterated monotone
sequence in the lattice of subsets whose termination is syntactically
evident (a strictly decreasing/increasing chain of finite sets, with an
a-priori bound given by the max element or popcount of the inputs).

Constructions (numbered as in exploration/0002):
    T(x)      Prop 2: trailing-ones mask, as the stabilizing intersection
              x & b(x) & b(b(x)) & ...
    succ(x)   Prop 3: x ^ b(T(x))
    add(x,y)  Prop 5: carry recursion (x^y, a(x&y)), measure = popcount sum
    add_lfp   Kleene least-fixpoint carry-lookahead variant

Each function asserts its own termination measure as it runs, so a passing
test run is also a check of the convexity bounds, not just of the answers.

Run this file directly to execute the verification suite.
"""


def a(x: int) -> int:
    """Shift left filling 0: n -> 2n. On sets: {i} -> {i+1}."""
    return x << 1


def b(x: int) -> int:
    """Shift left filling 1: n -> 2n+1. On sets: S -> {0} | {i+1 for i in S}."""
    return (x << 1) | 1


def trailing_ones(x: int) -> tuple[int, int]:
    """T(x) = x & b(x) & b(b(x)) & ...  (Prop 2).

    Returns (T, k) where k is the number of series terms consumed before
    the first plateau. Lemma 2b: the first plateau IS the limit (the count
    of non-trailing survivors strictly decreases until it hits 0), so the
    stopping rule needs no cleverness. Lemma 2c: k <= max_bit(x) + 1 is an
    a-priori syntactic bound, asserted here.
    """
    bound = x.bit_length() + 1  # max element + 1, plus slack for x = 0
    prev = x
    term = x
    k = 0
    while True:
        term = b(term)
        cur = prev & term
        k += 1
        assert k <= bound, "stabilization bound violated (Lemma 2c)"
        if cur == prev:  # first plateau = limit (Lemma 2b)
            return cur, k
        prev = cur


def succ(x: int) -> int:
    """x + 1 = x ^ b(T(x))  (Prop 3)."""
    t, _ = trailing_ones(x)
    return x ^ b(t)


def add(x: int, y: int) -> tuple[int, int]:
    """x + y by carry recursion  (Prop 5).

    step: (x, y) -> (x ^ y, a(x & y)) until the carry is empty.
    Measure: popcount(x) + popcount(y) strictly decreases while the carry
    is nonempty, so the loop runs at most popcount(x)+popcount(y) steps.
    Returns (sum, steps_taken); the measure is asserted each step.
    """
    steps = 0
    while x & y:
        measure = x.bit_count() + y.bit_count()
        x, y = x ^ y, a(x & y)
        steps += 1
        assert x.bit_count() + y.bit_count() < measure, \
            "popcount measure failed to decrease (Prop 5)"
    return x ^ y, steps


def add_lfp(x: int, y: int) -> tuple[int, int]:
    """x + y via the carry-lookahead least fixpoint.

    C = lfp of F(C) = a((x & y) | ((x ^ y) & C));   x + y = x ^ y ^ C.
    F is monotone and C_0 = 0, so the Kleene chain is increasing and its
    first repeat is the least fixpoint — same stabilizing-series shape as
    trailing_ones, in the increasing direction. (| is sugar:
    u | v = u ^ v ^ (u & v), still inside the {^, &} algebra.)
    Returns (sum, iterations).
    """
    g = x & y       # carry generate
    p = x ^ y       # carry propagate
    c = 0
    k = 0
    bound = max(x.bit_length(), y.bit_length()) + 2
    while True:
        nxt = a(g | (p & c))
        k += 1
        assert k <= bound, "lfp iteration bound violated"
        if nxt == c:
            return p ^ c, k
        assert nxt & c == c, "Kleene chain not increasing"
        c = nxt


def add_ks(x: int, y: int) -> tuple[int, int]:
    """x + y via the doubling-limit (Kogge-Stone) form from
    clue/2026-06-21 AI exploration.md:

        G_0 = x & y,  P_0 = x ^ y
        G_{s+1} = G_s ^ (P_s & Sh_s(G_s)),  P_{s+1} = P_s & Sh_s(P_s)
        x + y = x ^ y ^ a(lim G_s)          (Sh_s = shift by 2^s)

    Note it uses only ^ and & — the XOR stands in for OR because the two
    terms are disjoint (a block cannot both generate and fully propagate);
    asserted below. Termination: P_{s+1} strictly shrinks while nonzero
    (P & Sh(P) = P forces P = 0 since shifting raises the min element), and
    P_s = 0 once 2^s exceeds the bit width, so ~log2(width) steps; G is
    increasing and stabilizes once P = 0. Returns (sum, doubling_steps).
    """
    g, p = x & y, x ^ y
    shift = 1
    steps = 0
    bound = max(x.bit_length(), y.bit_length(), 1).bit_length() + 2
    while p:
        assert g & p == 0, "generate/propagate not disjoint"
        step_term = p & (g << shift)
        assert g & step_term == 0, "XOR-for-OR disjointness violated"
        g, p = g ^ step_term, p & (p << shift)
        shift <<= 1
        steps += 1
        assert steps <= bound, "log-step bound violated"
    return x ^ y ^ a(g), steps


def plus_const(x: int, c: int) -> int:
    """The constant-offset family n -> n + c, as iterated succ."""
    for _ in range(c):
        x = succ(x)
    return x


def deducible_eq(u: int, v: int, w: int) -> bool:
    """The convexity test for the hypothesis 'u + v = w'.

    The hypothesis term is add(u, v) ^ w; it reduces to the empty set (0,
    i.e. TRUE) iff the hypothesis holds. One-sided judgment: the result is
    'reduced to 0' or 'did not' — never 'false'.
    """
    s, _ = add(u, v)
    return s ^ w == 0


# ----------------------------------------------------------------------
# Verification suite
# ----------------------------------------------------------------------

def _verify(seed: int = 20260804) -> None:
    import random
    rng = random.Random(seed)

    # Prop 2: T(x) against the closed-form oracle 2^t - 1
    for x in range(1 << 14):
        t, _ = trailing_ones(x)
        assert t == ((~x & (x + 1)) - 1), f"T failed at {x}"
    print("Prop 2  trailing_ones: exhaustive 0..2^14  OK")

    # Prop 3: succ exhaustive + large random
    for x in range(1 << 14):
        assert succ(x) == x + 1, f"succ failed at {x}"
    for _ in range(500):
        x = rng.getrandbits(256)
        assert succ(x) == x + 1
    print("Prop 3  succ: exhaustive 0..2^14 + 500 random 256-bit  OK")

    # Prop 5: add exhaustive small, random large; step bound
    for x in range(256):
        for y in range(256):
            s, steps = add(x, y)
            assert s == x + y, f"add failed at {x},{y}"
            assert steps <= x.bit_count() + y.bit_count()
    for _ in range(500):
        x, y = rng.getrandbits(512), rng.getrandbits(512)
        s, steps = add(x, y)
        assert s == x + y
        assert steps <= x.bit_count() + y.bit_count()
    print("Prop 5  add: exhaustive 256x256 + 500 random 512-bit, "
          "steps <= popcount bound  OK")

    # lfp variant agrees
    for _ in range(500):
        x, y = rng.getrandbits(512), rng.getrandbits(512)
        s, _ = add_lfp(x, y)
        assert s == x + y
    print("        add_lfp: 500 random 512-bit  OK")

    # Doubling-limit (Kogge-Stone) form from clue/2026-06-21
    for x in range(256):
        for y in range(256):
            s, _ = add_ks(x, y)
            assert s == x + y, f"add_ks failed at {x},{y}"
    for _ in range(500):
        x, y = rng.getrandbits(512), rng.getrandbits(512)
        s, steps = add_ks(x, y)
        assert s == x + y
    print("        add_ks (doubling form, XOR-for-OR disjointness "
          "asserted): exhaustive 256x256 + 500 random 512-bit  OK")

    # Constant-offset family
    for x in range(1000):
        for c in (1, 2, 3, 7):
            assert plus_const(x, c) == x + c
    print("        plus_const family (+1,+2,+3,+7): 0..1000  OK")

    # Prop 4 witness (locality): bit k of succ depends on bit 0
    k = 96
    x1, x2 = (1 << k) - 1, (1 << k) - 2   # differ only in bit 0
    assert (succ(x1) >> k) & 1 != (succ(x2) >> k) & 1
    print("Prop 4  locality witness: bit 96 of succ flips with bit 0  OK")

    # Deduction test H ^ HK shape on arithmetic hypotheses
    assert deducible_eq(1337, 4958, 6295)
    assert not deducible_eq(1337, 4958, 6296)
    print("        deducible_eq one-sided test  OK")

    print("all checks passed")


if __name__ == "__main__":
    _verify()
