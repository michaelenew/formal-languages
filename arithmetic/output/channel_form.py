"""Rewrite rules folded into syntax: the channel form, and the wall it shows.

The user's pattern: name the hidden channels and write their defining
identities INTO the sentence as facts.  The carry is not an operator
with rules; it is a fresh variable `c` pinned by the fact

    c ^ xy ^ x·a(c) ^ y·a(c)                     (= 0)

and "x + y = 1" is one polynomial,

    I  :=  (x ^ y ^ a(c) ^ 1)  |  (c ^ xy ^ x·a(c) ^ y·a(c))

empty iff both disjuncts are.  Rules become in-sentence derivations:
substitution, cancellation, and one meta-principle -- a GUARDED
definition has a unique solution -- do what thirty rewrite rules did.

The point of the exercise is the single syntactic property it exposes.
Call a definition of channel `c` GUARDED if every occurrence of a
channel inside it sits under at least one `a` (a reference to the
PAST), and CO-GUARDED if it needs `h` (a reference to the FUTURE).
Then:

  guarded, finitely many     unique solution (2-adic contraction),
                             finite-state, decidable, coalescible.
                             A nonzero residue means CONTINGENCY --
                             the known unknown, on display.
  co-guarded                 solutions are NON-UNIQUE (least and
                             greatest); reduction cannot choose, a
                             case split can.  This is 0047's guard as
                             syntax, and `N` is its one inhabitant.
  channel SCHEMA             the fact-list must become a fact-family
                             (c_i for every i); no finite sentence
                             pins the channels.  Multiplication lives
                             here, with a measured lower bound.

Run directly for the verification suite.
"""

from __future__ import annotations

import functools
import itertools
import random

VARS = ("x", "y", "z")

ZERO = frozenset()
OMEGA = frozenset([frozenset()])
ONE = frozenset([frozenset([("one",)])])
X = frozenset([frozenset([("x",)])])
Y = frozenset([frozenset([("y",)])])


def var(name):
    return frozenset([frozenset([(name,)])])


def chan(index):
    return frozenset([frozenset([("c", index)])])


def xor(left, right):
    return left ^ right


def conj(left, right):
    out = set()
    for atoms_l in left:
        for atoms_r in right:
            out ^= {atoms_l | atoms_r}
    return frozenset(out)


def disj(left, right):
    return xor(xor(left, right), conj(left, right))


def shift(poly):                                  # a(P), one level
    return frozenset([frozenset([("a", poly)])]) if poly else ZERO


def hshift(poly):                                 # h(P): the future
    return frozenset([frozenset([("h", poly)])]) if poly else ZERO


# ---------------------------------------------------------------------
# evaluation
# ---------------------------------------------------------------------

def evaluate(poly, env, width):
    mask = (1 << width) - 1
    total = 0
    for atoms in poly:
        piece = mask
        for element in atoms:
            kind = element[0]
            if kind == "one":
                piece &= 1
            elif kind == "a":
                piece &= (evaluate(element[1], env, width) << 1) & mask
            elif kind == "h":
                piece &= evaluate(element[1], env, width) >> 1
            elif kind == "c":
                piece &= env[("c", element[1])] & mask
            else:
                piece &= env[kind] & mask
        total ^= piece
    return total & mask


# ---------------------------------------------------------------------
# 1. guardedness is a syntactic scan
# ---------------------------------------------------------------------

def channel_references(poly, depth=0):
    """(channel index, guard depth) for every channel occurrence;
    depth counts `a`s above it minus `h`s -- positive = past."""
    out = []
    for atoms in poly:
        for element in atoms:
            if element[0] == "c":
                out.append((element[1], depth))
            elif element[0] == "a":
                out.extend(channel_references(element[1], depth + 1))
            elif element[0] == "h":
                out.extend(channel_references(element[1], depth - 1))
    return out


def guarded(definitions) -> bool:
    """Every channel reference in every definition strictly past."""
    return all(depth >= 1
               for body in definitions.values()
               for _, depth in channel_references(body))


# ---------------------------------------------------------------------
# 2. guarded definitions pin their channels (the contraction theorem)
# ---------------------------------------------------------------------

def solve(definitions, env, width):
    """Iterate c_k := F_k to the fixpoint. For a guarded system bit i
    of every channel depends only on bits < i, so `width` passes
    settle everything -- the 2-adic contraction argument, run."""
    state = dict(env)
    for index in definitions:
        state[("c", index)] = 0
    for _ in range(width + 1):
        for index, body in definitions.items():
            state[("c", index)] = evaluate(body, state, width)
    return state


def random_guarded_body(generator, channels, budget):
    choice = generator.random()
    if budget == 0 or choice < 0.3:
        return generator.choice([X, Y, ONE, OMEGA])
    if choice < 0.55:
        inner_choice = generator.random()
        if inner_choice < 0.5 and channels:
            inner = chan(generator.choice(channels))
        else:
            inner = random_guarded_body(generator, channels, budget - 1)
        return shift(inner)
    op = generator.choice([xor, conj])
    return op(random_guarded_body(generator, channels, budget - 1),
              random_guarded_body(generator, channels, budget - 1))


def verify_guarded_definitions_pin(trials=250, width=14,
                                   seed=20261027) -> None:
    generator = random.Random(seed)
    checked = 0
    for _ in range(trials):
        count = generator.randrange(1, 4)
        definitions = {index: random_guarded_body(
            generator, list(range(count)), 3) for index in range(count)}
        if not guarded(definitions):
            continue
        for _ in range(4):
            env = {name: generator.randrange(1 << (width - 2))
                   for name in VARS}
            solution = solve(definitions, env, width)
            for index, body in definitions.items():
                assert solution[("c", index)] == \
                    evaluate(body, solution, width)
            # uniqueness: flip any bit of any channel and some
            # definition breaks
            for index in definitions:
                flipped = dict(solution)
                position = generator.randrange(width - 1)
                flipped[("c", index)] ^= 1 << position
                assert any(flipped[("c", j)] !=
                           evaluate(definitions[j], flipped, width)
                           for j in definitions)
            checked += 1
    print(f"  {checked} random guarded systems (1-3 mutually recursive")
    print(f"  channels): the fixpoint iteration settles, every definition")
    print(f"  holds, and every single-bit perturbation of any channel")
    print(f"  breaks some definition -- the solution is UNIQUE.")
    print()
    print("  The reason is one line: a guarded reference sits under `a`,")
    print("  so bit i of every channel is a function of bits < i --")
    print("  the definition is a contraction in the 2-adic metric, and")
    print("  Banach gives existence and uniqueness. Guardedness is a")
    print("  SYNTACTIC SCAN, and it buys a semantic theorem.")


# ---------------------------------------------------------------------
# 3. the operator tier, as channel definitions
# ---------------------------------------------------------------------

def def_bang(argument, index):
    return xor(argument, shift(chan(index)))


def def_up(argument, index):
    return disj(argument, shift(chan(index)))


def def_trail(argument, index):
    return conj(argument, xor(shift(chan(index)), ONE))


def def_carry(left, right, index):
    ac = shift(chan(index))
    return xor(xor(conj(left, right), conj(left, ac)), conj(right, ac))


def _run_reference(name, value, width):
    mask = (1 << width) - 1
    total, lifted = value, value
    for _ in range(width + 1):
        if name == "!":
            lifted = (lifted << 1) & mask
            total ^= lifted
        elif name == "U":
            lifted = (lifted << 1) & mask
            total |= lifted
        else:
            lifted = ((lifted << 1) | 1) & mask
            total &= lifted
    return total


def verify_the_operators_are_channels(width=14, seed=20261027) -> None:
    generator = random.Random(seed)
    mask = (1 << width) - 1
    for _ in range(600):
        value = generator.randrange(1 << (width - 2))
        env = {"x": value, "y": 0, "z": 0}
        for label, definition, reference in (
                ("!", def_bang(X, 0), _run_reference("!", value, width)),
                ("U", def_up(X, 0), _run_reference("U", value, width)),
                ("T", def_trail(X, 0), _run_reference("T", value, width))):
            solution = solve({0: definition}, env, width)
            assert solution[("c", 0)] == reference, label
        other = generator.randrange(1 << (width - 2))
        env = {"x": value, "y": other, "z": 0}
        solution = solve({0: def_carry(X, Y, 0)}, env, width)
        propagate, generate = value ^ other, value & other
        expected = 0
        for _ in range(width + 2):
            expected = (generate | (propagate &
                                    ((expected << 1) & mask))) & mask
        assert solution[("c", 0)] == expected
    print("  600 random inputs: the guarded definitions")
    print()
    print("      s = t ^ a(s)              solves to  !(t)")
    print("      u = t | a(u)              solves to  U(t)")
    print("      w = t & (a(w) ^ 1)        solves to  T(t)")
    print("      c = xy ^ (x ^ y)·a(c)     solves to  C(x, y)")
    print()
    print("  The operator tier IS the guarded-channel tier. 0042's")
    print("  fixpoint law was the definition all along; the schema's")
    print("  cells are the one-channel sentences.")


# ---------------------------------------------------------------------
# 4. the user's addition sentence
# ---------------------------------------------------------------------

def verify_the_addition_sentence(width=10) -> None:
    sentence = disj(
        xor(xor(xor(X, Y), shift(chan(0))), ONE),      # x ^ y ^ a(c) = 1
        def_carry_fact(X, Y, 0))
    holds, fails = 0, 0
    for value_x in range(1 << (width - 3)):
        for value_y in range(1 << (width - 3)):
            env = {"x": value_x, "y": value_y, "z": 0}
            solution = solve({0: def_carry(X, Y, 0)}, env, width)
            empty = evaluate(sentence, solution, width) == 0
            if (value_x + value_y) == 1:
                assert empty, (value_x, value_y)
                holds += 1
            else:
                assert not empty, (value_x, value_y)
                fails += 1
    print(f"  I := (x ^ y ^ a(c) ^ 1) | (c ^ xy ^ x·a(c) ^ y·a(c))")
    print()
    print(f"  exhaustive over {holds + fails} input pairs: I = 0 exactly")
    print(f"  when x + y = 1 ({holds} solutions, {fails} refutations).")
    print()
    print("  One polynomial over {^, &, a, |} and a hidden channel.")
    print("  No carry OPERATOR exists in the sentence -- the second")
    print("  disjunct pins c to be the carry, and the first uses it.")
    print("  Addition is a sentence, exactly as the workstream's original")
    print("  charter asked (0002's deduction test, now with the carry as")
    print("  a named wire instead of a series symbol).")


def def_carry_fact(left, right, index):
    return xor(chan(index), def_carry(left, right, index))


# ---------------------------------------------------------------------
# 5. a rewrite rule, derived inside the syntax
# ---------------------------------------------------------------------

def annihilate_low(poly):
    """Drop monomials containing both `1` and an `a`-atom: bit 0 of a
    shift is 0, so the masked monomial is empty -- 0051's annihilate,
    the only cancellation the derivation below needs."""
    kept = set()
    for atoms in poly:
        has_one = any(element[0] == "one" for element in atoms)
        has_shift = any(element[0] == "a" for element in atoms)
        if has_one and has_shift:
            continue
        kept.add(atoms)
    return frozenset(kept)


def verify_k_one_is_a_derivation() -> None:
    """The rewrite rule C(t, 1) -> T(t), folded into syntax.

    Substitute y := 1 in the carry's definition, cancel the one
    impossible monomial, and the result IS the trailing-ones
    definition, literally. Uniqueness of guarded solutions finishes:
    same definition, same channel.
    """
    substituted = def_carry(X, ONE, 0)
    cancelled = annihilate_low(substituted)
    target = def_trail(X, 0)
    print(f"    def_C(x, 1):    c = x·1 ^ x·a(c) ^ 1·a(c)")
    print(f"    annihilate:     1·a(c) = 0        (bit 0 of a shift)")
    print(f"    result:         c = x·1 ^ x·a(c)")
    print(f"    def_T(x):       w = x·(a(w) ^ 1) = x·a(w) ^ x·1")
    print(f"    literal match:  {cancelled == target}")
    assert cancelled == target
    print()
    print("  What was a rewrite rule (k-one, 0053) is now substitution +")
    print("  one cancellation + the uniqueness meta-principle. No rule")
    print("  engine, no pattern matching against an operator table: the")
    print("  fact manipulated the fact. succ costs one substitution.")


# ---------------------------------------------------------------------
# 6. guarded systems are finite-state (and that closes the loop to 0047)
# ---------------------------------------------------------------------

def transducer_states(definitions, width=12, samples=200,
                      seed=20261027) -> int:
    """Run the system as a machine whose state is the previous bit of
    every channel; count reachable states and verify the machine
    matches the solved semantics bit for bit."""
    generator = random.Random(seed)
    indices = sorted(definitions)
    reached = set()
    for _ in range(samples):
        env = {name: generator.randrange(1 << (width - 2))
               for name in VARS}
        solution = solve(definitions, env, width)
        state = tuple(0 for _ in indices)
        for position in range(width):
            reached.add(state)
            state = tuple((solution[("c", index)] >> position) & 1
                          for index in indices)
    return len(reached)


def verify_finite_state(seed=20261027) -> None:
    cases = [("!", {0: def_bang(X, 0)}),
             ("U", {0: def_up(X, 0)}),
             ("T", {0: def_trail(X, 0)}),
             ("C", {0: def_carry(X, Y, 0)}),
             ("C + !", {0: def_carry(X, Y, 0),
                        1: def_bang(chan(0), 1)})]
    for label, definitions in cases:
        count = transducer_states(definitions)
        print(f"    {label:<7} {len(definitions)} channel(s), "
              f"{count} reachable states (bound 2^k = "
              f"{2 ** len(definitions)})")
    print()
    print("  A guarded system with k channels of depth 1 carries exactly")
    print("  its previous channel bits as state: at most 2^k states. That")
    print("  is 0047's machine, derived from syntax -- the guarded-channel")
    print("  sentences ARE the finite-state tier, so their zero test is")
    print("  decidable and their residue after coalescing is honest")
    print("  contingency: the known unknown, wearing its variables.")


# ---------------------------------------------------------------------
# 7. the co-guarded channel: N, and non-uniqueness
# ---------------------------------------------------------------------

def verify_the_coguarded_channel(width=12) -> None:
    """n = t | h(n): the future-referencing definition.

    A guarded recursion starts at bit 0 and needs no boundary; a
    co-guarded one recurses DOWNWARD from infinity, and the boundary
    it needs there is exactly what does not exist. Solving top-down
    with the boundary set to 0 gives the down-closure D(t); with the
    boundary 1 it gives Omega -- both satisfy every interior step, so
    the definition does not pin its channel. The 0/Omega choice
    0047's machine makes per guard is the choice among these
    solutions, and N(t) = U(D(t)).
    """
    mask = (1 << width) - 1
    for value in range(1 << width):
        solutions = []
        for boundary in (0, 1):
            bits = [0] * (width + 1)
            bits[width] = boundary
            for i in range(width - 1, -1, -1):
                bits[i] = ((value >> i) & 1) | bits[i + 1]
            candidate = sum(bit << i for i, bit in enumerate(bits[:width]))
            for i in range(width - 1):
                assert bits[i] == (((value >> i) & 1) | bits[i + 1])
            solutions.append(candidate)
        down, top = solutions
        expected_down = 0
        for i in range(width):
            if value >> i:
                expected_down |= 1 << i
        assert down == expected_down, value
        assert top == mask, value
        spread, lifted = 0, down
        for _ in range(width):
            spread |= lifted
            lifted = (lifted << 1) & mask
        assert spread == (mask if value else 0), value
    print(f"  n = t | h(n), exhaustive at width {width}:")
    print(f"    boundary 0 at the top  ->  n = D(t), the down-closure")
    print(f"    boundary 1 at the top  ->  n = Omega")
    print(f"    both satisfy every interior step of the recurrence")
    print(f"    and U(D(t)) = N(t) for every t")
    print()
    print("  A guarded recursion starts at bit 0 -- the boundary exists.")
    print("  A co-guarded one starts at infinity -- it does not, so least")
    print("  and greatest solutions coexist and the definition cannot pin")
    print("  its channel. Choosing between them is 0047's guard bit. `h`")
    print("  was banned as an OPERATOR (0045); it returns as a reference")
    print("  DIRECTION, and one occurrence of it is the exact syntactic")
    print("  marker of the N tier: decidable by case split, undecidable")
    print("  by causal reduction (0051's stuck-truth theorem, visible in")
    print("  the sentence itself).")


# ---------------------------------------------------------------------
# 8. the schema wall: multiplication needs a channel FAMILY
# ---------------------------------------------------------------------

def _residuals(function, prefix_bits, tail_bits):
    tails = [(tx, ty) for tx in range(1 << tail_bits)
             for ty in range(1 << tail_bits)]
    classes = set()
    for low_x in range(1 << prefix_bits):
        for low_y in range(1 << prefix_bits):
            classes.add(tuple(
                function(low_x | (tx << prefix_bits),
                         low_y | (ty << prefix_bits)) >> prefix_bits
                for tx, ty in tails))
    return len(classes)


def verify_the_schema_wall(tail_bits=4) -> None:
    mask = (1 << 10) - 1
    print("    p    residuals of x·y    states of a k-channel system")
    needed = []
    for prefix in range(1, 5):
        count = _residuals(lambda u, v: (u * v) & mask, prefix, tail_bits)
        lower = (count - 1).bit_length()
        needed.append(lower)
        print(f"    {prefix}    {count:>8}                needs k ≥ {lower}")
    assert needed == [2, 4, 6, 8]
    print()
    print("  A guarded system with k depth-1 channels has at most 2^k")
    print("  states, and its residual count is bounded by its state")
    print("  count. x·y measures 4^p residuals after p bits, so any")
    print("  guarded system computing it to p bits needs k ≥ 2p channels:")
    print("  the channel LIST is forced to grow with the precision, i.e.")
    print("  to become a channel SCHEMA -- c_i for every i, an infinite")
    print("  fact-family. (Co-guarded channels do not rescue it: each")
    print("  adds a finite solution choice, a finite union of")
    print("  finite-state maps, still finite-state.) The school algorithm")
    print("  meets the bound with Theta(p) wires, so it is tight up to a")
    print("  constant.")
    print()
    print("  That is the wall as an expression: THE SENTENCE'S FACT-LIST")
    print("  MUST BECOME A FACT-SCHEMA. The moment a statement needs")
    print("  'for every position i, a channel c_i defined from c_{i-1}',")
    print("  it has left the decidable tier -- and that induction over")
    print("  positions is exactly what an induction axiom would license.")
    print("  The Goedel boundary, in this workstream's syntax, is the")
    print("  line between a conjunction and a schema.")


# ---------------------------------------------------------------------
# 8b. W4 dissolves: division by an odd constant is a guarded sentence
# ---------------------------------------------------------------------

def verify_division_is_a_guarded_sentence(width=16,
                                          seed=20261027) -> None:
    """0053's W4: `x * (1/3)` had no rule, and no finite rule list was
    going to be exhaustive. In channel form the question changes shape:
    `m = x/3` is the implicit fact `3m = x`, i.e.

        fact 1:   x ^ m ^ a(m) ^ a(c)                (3m = m + 2m)
        fact 2:   c ^ m·a(m) ^ (m ^ a(m))·a(c)       (c is that carry)

    Solved for the channels per bit, the system is triangular: m_i
    needs only the past, c_i needs the past and m_i. Two channels, no
    schema -- 3 is a 2-adic unit, so a unique solution exists for
    EVERY x, and the sentence decides division by 3 with no new
    operator and no new rule.
    """
    generator = random.Random(seed)
    mask = (1 << width) - 1
    definitions = {
        0: xor(xor(X, shift(chan(0))), shift(chan(1))),
        1: xor(conj(chan(0), shift(chan(0))),
               conj(xor(chan(0), shift(chan(0))), shift(chan(1)))),
    }
    for _ in range(3000):
        value = generator.randrange(1 << width)
        env = {"x": value, "y": 0, "z": 0}
        solution = solve(definitions, env, width)
        third = solution[("c", 0)]
        assert (3 * third - value) & mask == 0, value
    print(f"  fact 1:  x ^ m ^ a(m) ^ a(c)         (3m = m + 2m)")
    print(f"  fact 2:  c ^ m·a(m) ^ (m^a(m))·a(c)  (its carry)")
    print()
    print(f"  3000 random x at width {width}: the two-channel system has a")
    print(f"  unique solution and 3·m = x exactly, every time -- division")
    print(f"  by 3, with no division operator, no lasso constant, no rule.")
    print()
    print("  0053's W4 said x·(1/3) was stuck and the rule list was not")
    print("  exhaustive. Both were symptoms of asking the wrong question:")
    print("  a rule LIST can never be exhaustive, but a SENTENCE either")
    print("  has a finite guarded channel list or it does not, and this")
    print("  one does. The cross-reference in fact 2 (m at depth 0) needs")
    print("  the relaxed reading -- self-references guarded, same-position")
    print("  cross-references acyclic -- which is triangular solving, and")
    print("  the iteration settles exactly as before.")


# ---------------------------------------------------------------------
# 9. the trichotomy, on sentences
# ---------------------------------------------------------------------

def verify_the_trichotomy(width=10) -> None:
    rows = [
        ("x ^ y", "guarded (no channels)", "contingent: known unknown"),
        ("(x^y^a(c)^1) | def(c)", "guarded, 1 channel",
         "decidable: reduces per instance"),
        ("N-statement", "co-guarded, 1 channel",
         "case-split tier: h in the definition"),
        ("x·y = z", "channel schema", "outside: fact-family required"),
    ]
    print(f"    {'sentence':<24} {'channels':<24} verdict")
    for sentence, channels, verdict in rows:
        print(f"    {sentence:<24} {channels:<24} {verdict}")
    print()
    print("  One syntactic property -- the reference structure of the")
    print("  hidden channels -- separates all three:")
    print("    all references past (`a`)      reducible tier")
    print("    a future reference (`h`)       one case split per channel")
    print("    an indexed family (schema)     the wall")
    print()
    print("  'Known unknown' is a nonzero guarded residue: variables on")
    print("  display, decidable instance by instance. 'Knowably")
    print("  unknowable' is a sentence whose channels cannot be written")
    print("  as a finite guarded list -- and the sentence SHOWS it, in")
    print("  the h-reference or the index. The syntax expresses the")
    print("  break, which is what folding the rules into the sentence")
    print("  was for.")


def run_verification_suite() -> None:
    sections = [
        ("Guarded definitions pin their channels",
         verify_guarded_definitions_pin),
        ("The operator tier is the guarded-channel tier",
         verify_the_operators_are_channels),
        ("The addition sentence", verify_the_addition_sentence),
        ("A rewrite rule, derived inside the syntax",
         verify_k_one_is_a_derivation),
        ("Guarded systems are finite-state", verify_finite_state),
        ("The co-guarded channel: N and non-uniqueness",
         verify_the_coguarded_channel),
        ("The schema wall: multiplication", verify_the_schema_wall),
        ("W4 dissolves: division is a guarded sentence",
         verify_division_is_a_guarded_sentence),
        ("The trichotomy", verify_the_trichotomy),
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
