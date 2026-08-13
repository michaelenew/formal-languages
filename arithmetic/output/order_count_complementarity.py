"""The uncertainty frame, made quantitative.

Two measurements, one per half of the conjecture.

PART A -- the reference trichotomy.  0054 classified channels by
reference direction; here the solution COUNT of a definition is
measured against its reference structure, exhaustively:

    grounded (all self-references past)      exactly 1 solution, always
    ungrounded, consistent                   many solutions (truth-teller)
    ungrounded, contradictory                no solution (liar)

This is Kripke's grounding theory of truth, arriving in bitstream form:
the liar needs BOTH ungroundedness and negation; negation under a guard
is harmless.  Uncertainty about the channel's value enters exactly
where groundedness leaves, and nowhere else.

PART B -- order/count complementarity.  Two observables of a stream:

    ORDER  O_p  =  the low p bits of x*y        (positional structure)
    COUNT  C_m  =  popcount(x) mod m            (occupation structure)

Each alone has an exact finite price (states(p) measured in 0055; m
exactly).  The joint task is measured against the PRODUCT of the
individual prices: multiplicative = the two observables share no state,
and the budget line

    log2 states(p)  +  log2 m   <=   log2 S

is an uncertainty inequality with the carry's growth rate (~2.3x per
bit) as the exchange rate between the two resolutions.  The unbounded
limit is the classical wall: both exact with read-back = Minsky.

Run directly for the verification suite.
"""

from __future__ import annotations

import itertools
import random

# ---------------------------------------------------------------------
# PART A: the reference trichotomy
# ---------------------------------------------------------------------
#
# One channel n over one variable x. A body is a function (n, x) -> int
# at a given width, with `h` reading the future (n >> 1), so constraint
# positions above width - h_depth are excluded from the check -- they
# reference bits beyond the edge, which is exactly where the missing
# boundary at infinity lives.


def count_solutions(body, h_depth, x, width):
    interior = (1 << (width - h_depth)) - 1
    return [n for n in range(1 << width)
            if ((n ^ body(n, x)) & interior) == 0]


def verify_the_trichotomy(width=7) -> None:
    mask = (1 << width) - 1

    def down(t):
        out = 0
        for i in range(width):
            if t >> i:
                out |= 1 << i
        return out

    cases = [
        ("grounded:      n = x ^ a(n)",
         lambda n, x: x ^ ((n << 1) & mask), 0, "unique"),
        ("grounded:      n = ~a(n) & x   (negation, guarded)",
         lambda n, x: (~(n << 1)) & x & mask, 0, "unique"),
        ("truth-teller:  n = x | h(n)",
         lambda n, x: x | (n >> 1), 1, "two"),
        ("truth-teller:  n = n            (bare self)",
         lambda n, x: n, 0, "all"),
        ("liar:          n = n ^ Omega",
         lambda n, x: n ^ mask, 0, "none"),
        ("liar:          n = ~n & Omega",
         lambda n, x: (~n) & mask, 0, "none"),
    ]
    generator = random.Random(20261110)
    print(f"    {'definition':<44} {'solutions':>10}")
    for label, body, h_depth, expected in cases:
        counts = set()
        for _ in range(12):
            x = generator.randrange(1 << width)
            solutions = count_solutions(body, h_depth, x, width)
            counts.add(len(solutions))
            if expected == "two" and len(solutions) == 2:
                low, high = sorted(solutions)
                interior = (1 << (width - 1)) - 1
                # x's top bit only enters through the excluded top
                # constraint, so the least solution is the down-closure
                # of x's INTERIOR bits
                assert (low & interior) == (down(x & interior) & interior)
                assert (high & interior) == interior
        shown = sorted(counts)
        print(f"    {label:<44} {str(shown):>10}")
        if expected == "unique":
            assert counts == {1}, label
        elif expected == "none":
            assert counts == {0}, label
        elif expected == "two":
            assert counts == {2}, label
        elif expected == "all":
            assert counts == {1 << width}, label
    print()
    print("  Grounded definitions have exactly one solution -- negation")
    print("  included: `n = ~a(n) & x` is guarded, so the flip is")
    print("  harmless. The liar needs BOTH ungroundedness and negation;")
    print("  the truth-teller is ungrounded without contradiction (the")
    print("  free top bit is the missing boundary at infinity, and its")
    print("  two values are 0047's 0/Omega guard choice). `n = n` is the")
    print("  degenerate truth-teller: every value works.")


def verify_the_cycle_parity_law(width=6) -> None:
    """Two channels, depth-0 cross-references: solutions exist by the
    PARITY of negations around the cycle -- the classic liar-cycle law,
    verified exhaustively in bitstream form."""
    mask = (1 << width) - 1
    def negate(v):
        return v ^ mask

    cycles = [
        ("n1 = n2,  n2 = n1      (no negations)",
         lambda n1, n2: n2, lambda n1, n2: n1, 1 << width),
        ("n1 = ~n2, n2 = ~n1     (two negations)",
         lambda n1, n2: negate(n2), lambda n1, n2: negate(n1),
         1 << width),
        ("n1 = ~n2, n2 = n1      (one negation: odd)",
         lambda n1, n2: negate(n2), lambda n1, n2: n1, 0),
    ]
    print(f"    {'cycle':<40} {'solutions':>10}")
    for label, body1, body2, expected in cycles:
        found = sum(1 for n1 in range(1 << width)
                    for n2 in range(1 << width)
                    if n1 == body1(n1, n2) and n2 == body2(n1, n2))
        print(f"    {label:<40} {found:>10}")
        assert found == expected, label
    print()
    print("  An even number of negations around an ungrounded cycle is")
    print("  consistent (massively so: one free channel's worth of")
    print("  solutions); an odd number is a liar. Solution counts")
    print("  2^w / 2^w / 0 -- the paradox is a PARITY of flips around a")
    print("  reference loop, which in this corpus is a statement about")
    print("  Omega-monomials around a depth-0 cycle: checkable by scan.")


def census_of_ungrounded_definitions(trials=400, width=6,
                                     seed=20261110) -> None:
    """Random one-channel bodies mixing x, constants, n, a(n), h(n)
    under ^ and &: grounded ones always have exactly 1 solution; the
    ungrounded ones scatter across 0 / 1 / many."""
    generator = random.Random(seed)
    mask = (1 << width) - 1

    def random_body(budget):
        choice = generator.random()
        if budget == 0 or choice < 0.35:
            leaf = generator.choice(["x", "one", "omega", "n", "an", "hn"])
            return leaf
        op = generator.choice(["^", "&"])
        return (op, random_body(budget - 1), random_body(budget - 1))

    def references(tree, depth=0):
        if isinstance(tree, str):
            if tree == "n":
                return [depth]
            if tree == "an":
                return [depth + 1]
            if tree == "hn":
                return [depth - 1]
            return []
        return references(tree[1], depth) + references(tree[2], depth)

    def h_depth(tree):
        refs = references(tree)
        return max(0, -min(refs)) if refs else 0

    def run(tree, n, x):
        if isinstance(tree, str):
            return {"x": x, "one": 1, "omega": mask, "n": n,
                    "an": (n << 1) & mask, "hn": n >> 1}[tree]
        left, right = run(tree[1], n, x), run(tree[2], n, x)
        return (left ^ right) if tree[0] == "^" else (left & right)

    grounded_counts, ungrounded_histogram = set(), {}
    grounded_total = ungrounded_total = 0
    for _ in range(trials):
        tree = random_body(3)
        refs = references(tree)
        depth = h_depth(tree)
        is_grounded = all(r >= 1 for r in refs)
        for _ in range(3):
            x = generator.randrange(1 << width)
            solutions = count_solutions(
                lambda n, xv: run(tree, n, xv), depth, x, width)
            count = len(solutions)
            if is_grounded:
                grounded_counts.add(count)
                grounded_total += 1
            else:
                bucket = ("0 (liar)" if count == 0 else
                          "1" if count == 1 else
                          "2..15" if count < 16 else "16+")
                ungrounded_histogram[bucket] = \
                    ungrounded_histogram.get(bucket, 0) + 1
                ungrounded_total += 1
    assert grounded_counts == {1}
    print(f"  {grounded_total} grounded instances: solution count "
          f"ALWAYS exactly 1.")
    print(f"  {ungrounded_total} ungrounded instances:")
    for bucket in ("0 (liar)", "1", "2..15", "16+"):
        count = ungrounded_histogram.get(bucket, 0)
        print(f"    {bucket:<10} {count:>6}  "
              f"({100 * count / max(ungrounded_total, 1):.0f}%)")
    print()
    print("  The theorem half is absolute: groundedness forces a unique")
    print("  value, no exceptions in the census. The ungrounded half")
    print("  scatters across none / one / many -- uncertainty about the")
    print("  channel's value enters exactly where groundedness leaves,")
    print("  and only there.")


# ---------------------------------------------------------------------
# PART B: order/count complementarity
# ---------------------------------------------------------------------
#
# Exact minimal Mealy automata via signature BFS: a state is a residual
# (the map from futures to output streams, at a horizon checked for
# stability), transitions come from representative prefixes, and joint
# costs are reachable pairs of minimized components -- exact, because
# distinct pairs are behaviorally distinct once each component is
# minimized and the outputs are separate tracks.


def signature_machine(output_bit, horizon):
    """Minimal Mealy machine of a stream function via residual BFS.

    output_bit(x, y, i) is bit i of the target on full inputs; a
    residual of prefix (lx, ly, L) is the tuple over (tx, ty) tails of
    the next `horizon` output bits. Returns (states, transitions,
    initial) with states indexed by first reach.
    """
    tails = [(tx, ty) for tx in range(1 << horizon)
             for ty in range(1 << horizon)]

    def signature(lx, ly, length):
        out = []
        for tx, ty in tails:
            x = lx | (tx << length)
            y = ly | (ty << length)
            out.append(tuple(output_bit(x, y, i)
                             for i in range(length, length + horizon)))
        return tuple(out)

    initial = signature(0, 0, 0)
    index = {initial: 0}
    representative = {0: (0, 0, 0)}
    transitions = {}
    frontier = [0]
    while frontier:
        state = frontier.pop(0)
        lx, ly, length = representative[state]
        for bx in (0, 1):
            for by in (0, 1):
                nlx = lx | (bx << length)
                nly = ly | (by << length)
                sig = signature(nlx, nly, length + 1)
                if sig not in index:
                    index[sig] = len(index)
                    representative[index[sig]] = (nlx, nly, length + 1)
                    frontier.append(index[sig])
                transitions[(state, bx, by)] = index[sig]
    return len(index), transitions, 0


def transient_order_bit(precision):
    mask = (1 << precision) - 1
    return lambda x, y, i: ((x * y) & mask) >> i & 1


def persistent_order_bit(precision):
    """Bit i of (x mod 2^p) * y: multiplication by a LEARNED p-bit
    constant -- the carry lives forever, so the observable never dies."""
    mask = (1 << precision) - 1
    return lambda x, y, i: ((x & mask) * y) >> i & 1


def count_machine(modulus):
    transitions = {}
    for state in range(modulus):
        for bx in (0, 1):
            for by in (0, 1):
                transitions[(state, bx, by)] = (state + bx) % modulus
    return modulus, transitions, 0


def reachable_pairs(machine_a, machine_b):
    (_, trans_a, init_a) = machine_a
    (_, trans_b, init_b) = machine_b
    seen = {(init_a, init_b)}
    frontier = [(init_a, init_b)]
    while frontier:
        sa, sb = frontier.pop()
        for bx in (0, 1):
            for by in (0, 1):
                pair = (trans_a[(sa, bx, by)], trans_b[(sb, bx, by)])
                if pair not in seen:
                    seen.add(pair)
                    frontier.append(pair)
    return len(seen)


def verify_the_complementarity(max_precision=3, moduli=(2, 3, 4)) -> None:
    print("  Signature horizons checked stable (H vs H+1) at the small")
    print("  cases; joint = reachable pairs of minimized components,")
    print("  which is exact.")
    print()
    transient = {}
    persistent = {}
    for p in range(1, max_precision + 1):
        transient[p] = signature_machine(transient_order_bit(p), p + 2)
        persistent[p] = signature_machine(persistent_order_bit(p),
                                          max(p + 3, 6))
    assert signature_machine(transient_order_bit(2), 4)[0] ==         signature_machine(transient_order_bit(2), 5)[0]
    assert signature_machine(persistent_order_bit(2), 6)[0] ==         signature_machine(persistent_order_bit(2), 7)[0]
    print("    individual prices (minimal Mealy states):")
    print("      transient  O_p = x*y mod 2^p:        "
          + "  ".join(f"p={p}: {transient[p][0]}"
                      for p in sorted(transient)))
    print("      persistent P_p = (x mod 2^p)*y:      "
          + "  ".join(f"p={p}: {persistent[p][0]}"
                      for p in sorted(persistent)))
    print("      count      C_m = popcount(x) mod m:  m states, exact")
    print()
    print(f"    {'pair':<22} {'joint':>6} {'sum-ish':>8} {'product':>8}")
    for label, machines in (("transient + count", transient),
                            ("persistent + count", persistent)):
        for p in sorted(machines):
            for m in moduli:
                joint = reachable_pairs(machines[p], count_machine(m))
                order_states = machines[p][0]
                print(f"    {label} p={p} m={m:<2} {joint:>6} "
                      f"{order_states + m - 1:>8} {order_states * m:>8}")
    print()
    print("  THE FINDING, and it corrects the conjecture in an")
    print("  instructive direction: for the TRANSIENT order observable")
    print("  the joint cost is ADDITIVE-ish (near states + m), nowhere")
    print("  near the product -- the truncated task dies above bit p,")
    print("  the count lives forever, and observables that occupy")
    print("  different epochs of the run share their state across time.")
    print("  A dying observable evades the uncertainty trade.")
    print()
    print("  For the PERSISTENT order observable -- multiplication by a")
    print("  learned constant, whose carry never dies -- the joint cost")
    print("  climbs toward the product: complementarity is a statement")
    print("  about SIMULTANEOUS observation, and it binds exactly the")
    print("  observables that stay alive together. The uncertainty")
    print("  inequality log2(order) + log2(m) <= log2(S) holds with")
    print("  slack measured by the reachable-pair deficit; the unbounded")
    print("  limit (both exact, read-back) is the Minsky wall as before.")


def run_verification_suite() -> None:
    sections = [
        ("The reference trichotomy", verify_the_trichotomy),
        ("The cycle-parity law", verify_the_cycle_parity_law),
        ("Census: uncertainty enters where groundedness leaves",
         census_of_ungrounded_definitions),
        ("Order/count complementarity", verify_the_complementarity),
    ]
    for index, (title, check) in enumerate(sections, start=1):
        print("=" * 70)
        print(f"{index}. {title}")
        print("=" * 70)
        check()
        print()
    print("=" * 70)
    print("suite complete")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
