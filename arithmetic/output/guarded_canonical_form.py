"""Canonicity: is there a form that is exact on the true statements?

The target is a *guarded* canonical form -- one that is sound and
complete for statements that hold (terms denoting the empty set), and is
allowed to be sloppy about which nonempty set a false statement denotes.
The hope is that whatever is undecidable gets pushed out of the true
class and into the nonzero ones.

First finding, and it reshapes the rest: **that guard buys nothing on
the decision side.** `E1 = E2` iff `E1 ^ E2 = 0`, so a complete zero test
*is* a complete equality test; there is no smaller problem to solve. What
the guard can weaken is only the *output* -- a zero test need not produce
a canonical form for the nonzero terms.

So the question becomes: is the zero test decidable at all, and if so
what is the canonical object? Both answers are here.

  1. 0045 s4 found every operator but `N` is LSB-causal. The invariant
     that actually matters is stronger: **finite state**. Each operator
     is a one- or two-state Mealy transition reading the input LSB
     upward, so any `N`-free term is a finite transducer, and "is it
     identically 0" is reachability.
  2. `N` is exactly the operator that is not finite-state, and it is
     the guard. Fix each `N` subterm to 0 or to Omega, and what remains
     is finite-state; the guess is discharged by checking it against
     what the same run computed. That is the guarded form, and it
     decides.
  3. The price is not undecidability. It is that the canonical object
     is a **minimal machine, not a term** -- see s5. Two provably equal
     terms have the same minimal machine and different rewrite normal
     forms.

Run directly for the verification suite.
"""

from __future__ import annotations

import functools
import itertools
import random

# ---------------------------------------------------------------------
# terms
# ---------------------------------------------------------------------
#
#   ("var", name)        a free variable: a FINITE subset of N
#   ("const", n)         a finite constant, n's bits read LSB-first
#   ("omega",)           the universe, all of N -- not a finite constant
#   ("a", t)             shift up:   a(t)_i = t_{i-1}
#   ("^", t, u) ("&", t, u)
#   ("!", t) ("U", t) ("T", t)          the three series
#   ("lowset", t) ("lowzero", t)        the two measures
#   ("N", t)             0 if t is empty, Omega otherwise
#
# `b` is not a constructor: b(t) = a(t) ^ 1 (0046 s1).

OMEGA = ("omega",)
ONE = ("const", 1)
ZERO = ("const", 0)

var = lambda name="x": ("var", name)
a_ = lambda t: ("a", t)
b_ = lambda t: ("^", ("a", t), ONE)
xor_ = lambda t, u: ("^", t, u)
and_ = lambda t, u: ("&", t, u)
or_ = lambda t, u: ("^", ("^", t, u), ("&", t, u))
bang = lambda t: ("!", t)
up = lambda t: ("U", t)
trail = lambda t: ("T", t)
nonzero = lambda t: ("N", t)
lowset = lambda t: ("lowset", t)
lowzero = lambda t: ("lowzero", t)

UNARY = {"a", "!", "U", "T", "N", "lowset", "lowzero"}
BINARY = {"^", "&"}


def variables(term) -> tuple:
    found = set()
    stack = [term]
    while stack:
        node = stack.pop()
        if node[0] == "var":
            found.add(node[1])
        elif node[0] in UNARY:
            stack.append(node[1])
        elif node[0] in BINARY:
            stack += [node[1], node[2]]
    return tuple(sorted(found))


def show(term) -> str:
    kind = term[0]
    if kind == "var":
        return term[1]
    if kind == "omega":
        return "Ω"
    if kind == "const":
        return str(term[1])
    if kind == "a":
        return f"a({show(term[1])})"
    if kind in UNARY:
        return f"{kind}({show(term[1])})"
    return f"({show(term[1])} {kind} {show(term[2])})"


# ---------------------------------------------------------------------
# 1. reference semantics, at a finite width
# ---------------------------------------------------------------------

def evaluate(term, env: dict, width: int) -> int:
    """Straight interpretation, masked to `width` bits."""
    mask = (1 << width) - 1
    kind = term[0]
    if kind == "var":
        return env[term[1]] & mask
    if kind == "const":
        return term[1] & mask
    if kind == "omega":
        return mask
    if kind == "a":
        return (evaluate(term[1], env, width) << 1) & mask
    if kind == "^":
        return evaluate(term[1], env, width) ^ evaluate(term[2], env, width)
    if kind == "&":
        return evaluate(term[1], env, width) & evaluate(term[2], env, width)
    inner = evaluate(term[1], env, width)
    if kind == "N":
        return mask if inner else 0
    if kind == "lowset":
        return inner & -inner & mask
    if kind == "lowzero":
        flipped = mask ^ inner
        return flipped & -flipped & mask
    total, lifted = inner, inner
    for _ in range(width + 1):
        if kind == "!":
            lifted = (lifted << 1) & mask
            total ^= lifted
        elif kind == "U":
            lifted = (lifted << 1) & mask
            total |= lifted
        else:                                   # T, shifted by b
            lifted = ((lifted << 1) | 1) & mask
            total &= lifted
    return total


# ---------------------------------------------------------------------
# 2. the bit machine
# ---------------------------------------------------------------------
#
# Every operator but `N` reads the input LSB upward with a bounded
# amount of carried state.  0045 s4 said "LSB-causal"; what makes the
# decision procedure work is the sharper property that the state is
# FINITE.  Per node:
#
#   var        no state      out = input bit
#   const n    a position counter, capped at n.bit_length()
#   omega      no state      out = 1
#   a          1 bit         out = previous input-node output
#   ^ &        no state
#   !          1 bit         parity so far     out = parity ^ t
#   U          1 bit         seen a 1          out = seen | t
#   T          1 bit         all 1s so far     out = alive & t
#   lowset     1 bit         seen a 1          out = t & ~seen
#   lowzero    1 bit         all 1s so far     out = alive & ~t
#   N          NOT finite state.  It is the guard.


class Machine:
    """A term, flattened into indexed nodes with per-node transitions."""

    def __init__(self, term):
        self.nodes = []                 # (kind, payload, child indices)
        self.index = {}
        self.root = self._add(term)
        self.guards = [i for i, node in enumerate(self.nodes)
                       if node[0] == "N"]
        self.guard_argument = [self.nodes[i][2][0] for i in self.guards]
        self.variables = variables(term)

    def _add(self, term) -> int:
        if term in self.index:
            return self.index[term]
        kind = term[0]
        if kind in UNARY:
            children = (self._add(term[1]),)
            payload = None
        elif kind in BINARY:
            children = (self._add(term[1]), self._add(term[2]))
            payload = None
        else:
            children, payload = (), term[1] if kind != "omega" else None
        self.nodes.append((kind, payload, children))
        self.index[term] = len(self.nodes) - 1
        return len(self.nodes) - 1

    # -- state ---------------------------------------------------------

    def start(self) -> tuple:
        state = []
        for kind, payload, _ in self.nodes:
            if kind == "const":
                state.append(0)                 # position counter
            elif kind in ("a", "!", "U", "lowset"):
                state.append(0)
            elif kind in ("T", "lowzero"):
                state.append(1)                 # alive
            else:
                state.append(0)                 # unused
        return tuple(state)

    def step(self, state, letter: dict, guard: tuple):
        """One bit position. Returns (next state, per-node output bits)."""
        out = [0] * len(self.nodes)
        nxt = list(state)
        assigned = dict(zip(self.guards, guard))
        for index, (kind, payload, children) in enumerate(self.nodes):
            if kind == "var":
                out[index] = letter[payload]
            elif kind == "const":
                position = state[index]
                out[index] = (payload >> position) & 1
                cap = max(payload.bit_length(), 1)
                nxt[index] = min(position + 1, cap)
            elif kind == "omega":
                out[index] = 1
            elif kind == "N":
                out[index] = assigned[index]
            elif kind == "a":
                out[index] = state[index]
                nxt[index] = out[children[0]]
            elif kind == "^":
                out[index] = out[children[0]] ^ out[children[1]]
            elif kind == "&":
                out[index] = out[children[0]] & out[children[1]]
            elif kind == "!":
                out[index] = state[index] ^ out[children[0]]
                nxt[index] = out[index]
            elif kind == "U":
                out[index] = state[index] | out[children[0]]
                nxt[index] = out[index]
            elif kind == "T":
                out[index] = state[index] & out[children[0]]
                nxt[index] = out[index]
            elif kind == "lowset":
                out[index] = out[children[0]] & (1 - state[index])
                nxt[index] = state[index] | out[children[0]]
            elif kind == "lowzero":
                out[index] = state[index] & (1 - out[children[0]])
                nxt[index] = state[index] & out[children[0]]
        return tuple(nxt), out

    def letters(self):
        names = self.variables or ("_",)
        for bits in itertools.product((0, 1), repeat=len(names)):
            yield dict(zip(names, bits))

    def run(self, env: dict, guard: tuple, width: int) -> int:
        """The root's output as an integer, over `width` positions."""
        state, total = self.start(), 0
        for position in range(width):
            letter = {name: (env[name] >> position) & 1
                      for name in self.variables}
            state, out = self.step(state, letter, guard)
            total |= out[self.root] << position
        return total


def consistent_guard(machine: Machine, env: dict, width: int) -> tuple:
    """The one guard assignment that matches this input.

    `N` subterms are resolved innermost first: by the time the j-th is
    decided, every `N` inside its argument already is.
    """
    guard = [0] * len(machine.guards)
    for slot, argument in enumerate(machine.guard_argument):
        state, seen = machine.start(), 0
        for position in range(width):
            letter = {name: (env[name] >> position) & 1
                      for name in machine.variables}
            state, out = machine.step(state, letter, tuple(guard))
            seen |= out[argument]
        guard[slot] = seen
    return tuple(guard)


# ---------------------------------------------------------------------
# 3. the decision procedure
# ---------------------------------------------------------------------

def decide_zero(term, node_cap: int = 200000):
    """Is `term` empty for every input, at every width?

    Returns None when it is, otherwise a counterexample: a dict of
    variable values (finite, LSB-first) together with the guard it forces.

    The search is reachability on (machine state, emission flags). Flags
    record, for each `N` argument and for the root, whether a 1 has been
    emitted so far -- the guard cannot be checked before the run ends,
    because `N` looks at all of its argument.
    """
    machine = Machine(term)
    tracked = list(machine.guard_argument) + [machine.root]
    letters = list(machine.letters())
    for guard in itertools.product((0, 1), repeat=len(machine.guards)):
        start = (machine.start(), (0,) * len(tracked))
        seen, frontier, source = {start: None}, [start], {}
        while frontier:
            current = frontier.pop()
            state, flags = current
            for letter in letters:
                nxt, out = machine.step(state, letter, guard)
                lifted = tuple(flag | out[node]
                               for flag, node in zip(flags, tracked))
                following = (nxt, lifted)
                if following not in seen:
                    if len(seen) >= node_cap:
                        raise RuntimeError("state cap hit: " + show(term))
                    seen[following] = (current, letter)
                    frontier.append(following)
        for config in seen:
            settled = _zero_tail(machine, config, guard, tracked)
            forced = settled[:-1]
            if forced == guard and settled[-1]:
                return _witness(machine, seen, config, guard)
    return None


def _zero_tail(machine, config, guard, tracked):
    """Keep feeding 0 until nothing moves: the input's support is finite,
    but the term can still emit above it."""
    state, flags = config
    blank = {name: 0 for name in machine.variables}
    visited = set()
    while (state, flags) not in visited:
        visited.add((state, flags))
        state, out = machine.step(state, blank, guard)
        flags = tuple(flag | out[node] for flag, node in zip(flags, tracked))
    return flags


def _witness(machine, seen, config, guard):
    word = []
    while seen[config] is not None:
        config, letter = seen[config]
        word.append(letter)
    word.reverse()
    env = {name: 0 for name in machine.variables}
    for position, letter in enumerate(word):
        for name, bit in letter.items():
            env[name] |= bit << position
    return {"input": env, "guard": guard, "positions": len(word)}


def equal(left, right):
    """Two terms, same function? Complete, at every width."""
    return decide_zero(("^", left, right)) is None


# ---------------------------------------------------------------------
# 4. checks on the machine itself
# ---------------------------------------------------------------------

def random_term(generator, budget, names=("x",), allow_n=True):
    choice = generator.random()
    if budget == 0 or choice < 0.3:
        return generator.choice([var(name) for name in names]
                                + [ONE, OMEGA, ("const", 5)])
    if choice < 0.65:
        kinds = ["a", "!", "U", "T", "lowset", "lowzero"]
        if allow_n:
            kinds.append("N")
        return (generator.choice(kinds),
                random_term(generator, budget - 1, names, allow_n))
    return (generator.choice(["^", "&"]),
            random_term(generator, budget - 1, names, allow_n),
            random_term(generator, budget - 1, names, allow_n))


def verify_the_machine_matches_the_interpreter(trials=4000, width=10,
                                               seed=20260901) -> None:
    """Compiled transitions against the straight recursive semantics."""
    generator = random.Random(seed)
    names = ("x", "y")
    checked = 0
    for _ in range(trials):
        term = random_term(generator, 3, names)
        machine = Machine(term)
        used = machine.variables or names[:1]
        for _ in range(6):
            env = {name: generator.randrange(1 << (width - 2))
                   for name in used}
            guard = consistent_guard(machine, env, width)
            assert machine.run(env, guard, width) == \
                evaluate(term, env, width), (show(term), env)
            checked += 1
    print(f"  {checked} runs over {trials} terms, two free variables:")
    print(f"  the compiled machine and the interpreter agree bit for bit")
    print(f"  -- every operator but `N` is a 1- or 2-state Mealy step.")


def verify_the_state_is_bounded(seed=20260901) -> None:
    """Nerode classes of each operator, and of `x*y` for contrast."""
    print("  reachable machine states, by operator (one variable):")
    for label, term in [("a(x)", a_(var())), ("!(x)", bang(var())),
                        ("U(x)", up(var())), ("T(x)", trail(var())),
                        ("lowset(x)", lowset(var())),
                        ("lowzero(x)", lowzero(var())),
                        ("!(U(T(a(x))))", bang(up(trail(a_(var())))))]:
        machine = Machine(term)
        reached = _reachable(machine, (0,) * len(machine.guards))
        print(f"    {label:<16} {len(reached):>3} states")
    print()
    print("  `N` has no finite-state reading at all: its bit 0 is the OR")
    print("  of every input bit, so no bounded state read LSB-upward can")
    print("  produce it. That is 0045 s4 sharpened -- LSB-causality is")
    print("  necessary, bounded state is what the decision needs.")


def _reachable(machine, guard):
    start = machine.start()
    seen, frontier = {start}, [start]
    while frontier:
        state = frontier.pop()
        for letter in machine.letters():
            nxt, _ = machine.step(state, letter, guard)
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    return seen


def verify_the_decision_matches_brute_force(trials=1500, width=11,
                                            seed=20260901) -> None:
    """`decide_zero` against exhaustive evaluation.

    One direction is checkable outright: when the decider reports a
    counterexample, evaluate it. The other only bounds -- brute force at
    a finite width cannot confirm "zero at every width" -- so a
    disagreement is only interesting when brute force finds a witness
    the decider missed.
    """
    generator = random.Random(seed)
    zero, witnessed, missed, bogus = 0, 0, [], []
    for _ in range(trials):
        term = random_term(generator, 3, ("x",))
        verdict = decide_zero(term)
        if verdict is None:
            zero += 1
            for value in range(1 << (width - 3)):
                env = {"x": value}
                if evaluate(term, env, width):
                    missed.append((show(term), value))
                    break
        else:
            witnessed += 1
            env = verdict["input"]
            found = any(evaluate(term, env, w) for w in range(1, width + 4))
            if not found:
                bogus.append((show(term), env))
    print(f"  {trials} terms: {zero} decided empty, {witnessed} refuted")
    print(f"  every refutation carries an input; {len(bogus)} do not "
          f"evaluate nonzero")
    print(f"  {len(missed)} terms called empty are nonzero under brute "
          f"force at width {width}")
    for shown, value in (missed + bogus)[:4]:
        print(f"    MISMATCH {shown}   {value}")
    assert not missed and not bogus


def verify_the_guard_is_what_n_costs(seed=20260901) -> None:
    """Terms are decided; the guard count is the only branching."""
    print("  the guard is one bit per `N` subterm, and the whole search")
    print("  is 2^k reachability sweeps:")
    for label, term in [
            ("N(x) ^ N(x)", xor_(nonzero(var()), nonzero(var()))),
            ("N(N(x)) ^ N(x)", xor_(nonzero(nonzero(var())),
                                    nonzero(var()))),
            ("N(a x) ^ N(x)", xor_(nonzero(a_(var())), nonzero(var()))),
            ("N(b x) ^ Ω", xor_(nonzero(b_(var())), OMEGA)),
            ("N(U x) ^ N(x)", xor_(nonzero(up(var())), nonzero(var()))),
            ("N(T x) ^ N(x&1)", xor_(nonzero(trail(var())),
                                     nonzero(and_(var(), ONE))))]:
        machine = Machine(term)
        verdict = decide_zero(term)
        status = "TRUE" if verdict is None else "refuted"
        print(f"    {label:<18} {len(machine.guards)} guard(s)   {status}")
    print()
    print("  Each of those is a rule 0038 or 0042 found by hand. The")
    print("  decision procedure gets them from the guard alone -- it has")
    print("  no rule for `N` at all.")


# ---------------------------------------------------------------------
# 5. the canonical object
# ---------------------------------------------------------------------

def minimal_machine(term, guard=None):
    """The minimised Mealy machine of `term` under a fixed guard.

    Reachable-then-refine, then renumber by breadth-first order, so the
    result is a canonical tuple: equal functions give equal tuples.
    """
    machine = Machine(term)
    guard = guard if guard is not None else (0,) * len(machine.guards)
    letters = list(machine.letters())
    keys = [tuple(sorted(letter.items())) for letter in letters]
    states = sorted(_reachable(machine, guard))
    transition, emission = {}, {}
    for state in states:
        for key, letter in zip(keys, letters):
            nxt, out = machine.step(state, letter, guard)
            transition[(state, key)] = nxt
            emission[(state, key)] = out[machine.root]
    block = {state: tuple(emission[(state, key)] for key in keys)
             for state in states}
    while True:
        refined = {state: (block[state],
                           tuple(block[transition[(state, key)]]
                                 for key in keys))
                   for state in states}
        labels = {value: index for index, value
                  in enumerate(sorted(set(refined.values())))}
        nxt = {state: labels[refined[state]] for state in states}
        if len(set(nxt.values())) == len(set(block.values())):
            break
        block = nxt
    representative = {}
    for state in states:
        representative.setdefault(block[state], state)
    step_to = {(block[s], key): block[transition[(s, key)]]
               for s in states for key in keys}
    order, frontier = {block[machine.start()]: 0}, [block[machine.start()]]
    while frontier:
        current = frontier.pop(0)
        for key in keys:
            target = step_to[(current, key)]
            if target not in order:
                order[target] = len(order)
                frontier.append(target)
    canonical = []
    for target in sorted(order, key=order.get):
        witness = representative[target]
        canonical.append(tuple(
            (emission[(witness, key)], order[step_to[(target, key)]])
            for key in keys))
    return tuple(canonical)


def guarded_canonical_form(term):
    """(guard, minimal machine) for every guard, inconsistent ones dropped.

    The statement holds iff every surviving entry is the zero machine.
    """
    machine = Machine(term)
    entries = []
    for guard in itertools.product((0, 1), repeat=len(machine.guards)):
        if _guard_is_reachable(machine, guard):
            entries.append((guard, minimal_machine(term, guard)))
    return tuple(sorted(entries))


def _guard_is_reachable(machine, guard):
    """Is there an input that forces exactly this guard?"""
    tracked = list(machine.guard_argument)
    if not tracked:
        return True
    start = (machine.start(), (0,) * len(tracked))
    seen, frontier = {start}, [start]
    letters = list(machine.letters())
    while frontier:
        state, flags = frontier.pop()
        for letter in letters:
            nxt, out = machine.step(state, letter, guard)
            following = (nxt, tuple(f | out[n]
                                    for f, n in zip(flags, tracked)))
            if following not in seen:
                seen.add(following)
                frontier.append(following)
    return any(_zero_tail(machine, config, guard, tracked) == guard
               for config in seen)


ZERO_MACHINE = minimal_machine(ZERO)


def verify_the_canonical_form_is_canonical(seed=20260901) -> None:
    """Provably equal terms, and what each form says about them."""
    pairs = [
        ("!(t) ^ a(!t)", "t",
         xor_(bang(var()), a_(bang(var()))), var()),
        ("U(t) ^ a(U t)", "lowset(t)",
         xor_(up(var()), a_(up(var()))), lowset(var())),
        ("T(t) ^ b(T t)", "lowzero(t)",
         xor_(trail(var()), b_(trail(var()))), lowzero(var())),
        ("lowset(t)", "lowzero(t ^ Ω)",
         lowset(var()), lowzero(xor_(var(), OMEGA))),
        ("U(x) ^ U(a x)", "lowset(x) ^ x & U(a x)",
         xor_(up(var()), up(a_(var()))),
         xor_(lowset(var()), and_(var(), up(a_(var()))))),
        ("!(U x)", "lowset(x)",
         bang(up(var())), lowset(var())),
        ("T(x) & U(x)", "T(x) & x",
         and_(trail(var()), up(var())), and_(trail(var()), var())),
    ]
    agree = 0
    for left_label, right_label, left, right in pairs:
        same = equal(left, right)
        canonical = minimal_machine(left) == minimal_machine(right)
        flag = "=" if same else "≠"
        print(f"    {left_label:<22} {flag} {right_label:<24} "
              f"minimal machines {'match' if canonical else 'DIFFER'}")
        assert same == canonical, (left_label, right_label)
        agree += same
    print()
    print(f"  {agree} of {len(pairs)} pairs are equal, and in every case")
    print("  semantic equality and machine identity are the same verdict.")
    print("  The minimal Mealy machine is a genuine canonical form -- it")
    print("  is unique up to isomorphism, and the breadth-first")
    print("  renumbering above pins the isomorphism.")


def verify_truth_is_the_zero_machine(trials=600, seed=20260901) -> None:
    generator = random.Random(seed)
    disagreed = []
    for _ in range(trials):
        term = random_term(generator, 3, ("x",))
        form = guarded_canonical_form(term)
        by_form = all(entry == ZERO_MACHINE for _, entry in form)
        by_decision = decide_zero(term) is None
        if by_form != by_decision:
            disagreed.append((show(term), by_form, by_decision))
    print(f"  {trials} terms: the statement holds iff every consistent")
    print("  guard gives the zero machine")
    if disagreed:
        for shown, by_form, by_decision in disagreed[:5]:
            print(f"    DISAGREE {shown}  form={by_form} "
                  f"decide={by_decision}")
    else:
        print("  **no disagreement** -- the guarded form decides truth")
    assert not disagreed


# ---------------------------------------------------------------------
# 6. against the rewrite system
# ---------------------------------------------------------------------

def _load_engine():
    """0044's engine, narrowed by 0045 -- `h` and its two series gone."""
    import series_confluence_anf as engine
    if "h" in engine.SHIFTS:
        engine.configure_without_h()
    return engine


def from_polynomial(poly, engine):
    """An engine ANF polynomial, read as a term of this module.

    The engine's full mask is the universe, so it reads as `Ω`; that is
    the width-independent reading (0046 s1), and the whole point of
    checking the engine against an unbounded decision procedure.
    """
    if not poly:
        return ZERO
    total = None
    for atoms, mask in sorted(poly, key=lambda m: (sorted(map(str, m[0])),
                                                   m[1])):
        piece = OMEGA if mask == engine.MASK else ("const", mask)
        for atom in sorted(atoms, key=str):
            if atom[0] == "x":
                factor = var("x")
            elif atom[0] == "shift":
                inner = from_polynomial(atom[2], engine)
                factor = a_(inner) if atom[1] == "a" else b_(inner)
            elif atom[0] == "series":
                inner = from_polynomial(atom[2], engine)
                factor = {"!": bang, "U": up, "T": trail,
                          "N": nonzero}[atom[1]](inner)
            else:
                inner = from_polynomial(atom[2], engine)
                factor = {"low-set": lowset, "low-zero": lowzero,
                          "self": lambda t: t}[atom[1]](inner)
            piece = and_(piece, factor)
        total = piece if total is None else xor_(total, piece)
    return total


def _normal_form(poly, engine):
    forms, capped = engine.normal_forms(poly)
    if capped or len(forms) != 1:
        return None
    return next(iter(forms))


def verify_the_rewrite_system_is_incomplete(trials=900, seed=20260901):
    """Two different defects, and they have to be told apart.

    INCOMPLETE -- the rules identify too little: two terms with the same
    meaning reach different normal forms, or an empty term does not
    reach `0`.

    WIDTH-BOUND -- the rules identify too much: a rewrite is
    meaning-preserving at the width the engine was measured at, and not
    at every width. `fold` evaluates constants inside a fixed WIDTH, so
    `a(Ω)` folds to the finite constant `2^W - 2`, when unboundedly it
    is the cofinite `Ω ^ 1`.

    Both are measured here against the unbounded decision procedure.
    """
    engine = _load_engine()
    generator = random.Random(seed)
    pool, empty_but_open, width_bound = [], [], []
    for index in range(trials):
        builder = (engine.random_poly if index % 2 else
                   engine.random_structured_poly)
        poly = builder(generator, 3)
        term = from_polynomial(poly, engine)
        normal = _normal_form(poly, engine)
        if normal is None:
            continue
        rewritten = from_polynomial(normal, engine)
        try:
            empty = decide_zero(term) is None
            preserved = equal(term, rewritten)
        except RuntimeError:
            continue
        if not preserved:
            width_bound.append((engine.render(poly), engine.render(normal)))
        elif empty and normal:
            empty_but_open.append((engine.render(poly),
                                   engine.render(normal)))
        pool.append((poly, term, normal, preserved))
    groups = {}
    for poly, term, normal, preserved in pool:
        if not preserved:
            continue
        key = tuple(engine.evaluate(poly, value) for value in engine.SAFE)
        groups.setdefault(key, []).append((poly, term, normal))
    unidentified = []
    for members in groups.values():
        for first, second in itertools.combinations(members[:6], 2):
            if first[2] == second[2]:
                continue
            try:
                if equal(first[1], second[1]):
                    unidentified.append((engine.render(first[2]),
                                         engine.render(second[2])))
            except RuntimeError:
                continue
    print(f"  {len(pool)} terms normalised and decided against the "
          f"unbounded semantics")
    print()
    print(f"  WIDTH-BOUND: {len(width_bound)} normal forms do not mean what "
          f"the term meant")
    for before, after in sorted(width_bound, key=lambda r: len(r[0]))[:4]:
        print(f"    {before}   ->   {after}")
    print(f"    minimal case: a(Ω) folds to the constant "
          f"{engine.SHIFTS['a'](engine.MASK)} at WIDTH="
          f"{engine.WIDTH}; unboundedly a(Ω) = Ω ^ 1, which is cofinite "
          f"and not any finite constant.")
    print()
    print(f"  INCOMPLETE: {len(empty_but_open)} terms are identically empty "
          f"and do not normalise to `0`")
    for before, after in sorted(empty_but_open, key=lambda r: len(r[0]))[:4]:
        print(f"    {before}   ->   {after}      (should be 0)")
    print()
    print(f"  INCOMPLETE: {len(unidentified)} pairs mean the same at every "
          f"width, with different normal forms")
    for first, second in sorted(unidentified,
                                key=lambda pr: len(pr[0]) + len(pr[1]))[:5]:
        print(f"    {first}   vs   {second}")
    print()
    print("  Confluence is not completeness. 0044 measured that every term")
    print("  has ONE normal form; that says nothing about whether equal")
    print("  terms reach the SAME one, and they do not.")
    return width_bound, empty_but_open, unidentified


def verify_anf_does_not_fold_constants() -> None:
    """A correction to 0044's census.

    0044 listed `fold-of-two-constants` among the rules "gone -- building
    an ANF polynomial already does them". It is not gone. A constant is a
    monomial with no atoms, and `xor` is symmetric difference on
    monomials, so two constants with different masks are two monomials
    and stay two monomials.
    """
    engine = _load_engine()
    poly = engine.xor(engine.const(1), engine.const(6))
    print(f"  engine.xor(const 1, const 6) renders as `{engine.render(poly)}`")
    print(f"    monomials: {len(poly)}   is_constant: "
          f"{engine.is_constant(poly)}   value: "
          f"{engine.constant_value(poly)}")
    print(f"    rewrites available: {engine.rewrites(poly)}")
    print(f"    but const(7) is `{engine.render(engine.const(7))}`, one "
          f"monomial -- a different normal form for the same set.")
    assert engine.is_constant(poly) and len(poly) == 2
    assert not engine.rewrites(poly)
    assert poly != engine.const(7)
    print()
    print("  So `^` of two distinct constants is a normal form that is not")
    print("  the canonical constant. ANF absorbs commutativity, units,")
    print("  annihilators and idempotence, and it absorbs folding only")
    print("  when the two masks are EQUAL, where symmetric difference")
    print("  cancels them. 0044's census overstated what the")
    print("  representation was doing.")


def verify_the_missing_laws() -> None:
    """The gaps of s6, as named laws rather than sampled instances.

    Each is TRUE at every width by the decision procedure, and each is
    missed by the rules -- the two sides reach different normal forms.
    """
    engine = _load_engine()
    x = var()
    laws = [
        ("b is derived (0046 s1)",
         b_(x), xor_(ONE, a_(x)),
         engine.shift_poly("b", engine.VARIABLE),
         engine.xor(engine.const(1),
                    engine.shift_poly("a", engine.VARIABLE))),
        ("T dies on an even argument",
         trail(a_(x)), ZERO,
         engine.series_poly("T", engine.shift_poly("a", engine.VARIABLE)),
         engine.const(0)),
        ("U saturates on an odd argument",
         up(b_(x)), OMEGA,
         engine.series_poly("U", engine.shift_poly("b", engine.VARIABLE)),
         engine.const(engine.MASK)),
        ("N is ! on a one-bit argument",
         nonzero(and_(x, ONE)), bang(and_(x, ONE)),
         engine.series_poly("N", engine.conj(engine.VARIABLE,
                                             engine.const(1))),
         engine.series_poly("!", engine.conj(engine.VARIABLE,
                                             engine.const(1)))),
        ("complementary shifts annihilate",
         and_(a_(xor_(OMEGA, x)), b_(x)), ZERO,
         engine.conj(engine.shift_poly("a", engine.xor(
             engine.const(engine.MASK), engine.VARIABLE)),
             engine.shift_poly("b", engine.VARIABLE)),
         engine.const(0)),
        ("constants do not fold under ^",
         ("const", 7), xor_(ONE, ("const", 6)),
         engine.const(7),
         engine.xor(engine.const(1), engine.const(6))),
    ]
    missed = 0
    for label, left, right, left_poly, right_poly in laws:
        holds = equal(left, right)
        left_normal = _normal_form(left_poly, engine)
        right_normal = _normal_form(right_poly, engine)
        identified = left_normal == right_normal
        assert holds, label
        missed += not identified
        print(f"    {label}")
        print(f"      {show(left)} = {show(right)}   true at every width; "
              f"rules {'identify' if identified else 'do NOT identify'} them")
        if not identified:
            print(f"      normal forms: `{engine.render(left_normal)}`  vs  "
                  f"`{engine.render(right_normal)}`")
    print()
    print(f"  {missed} of {len(laws)} true laws are invisible to the rule")
    print("  set. They are not near-misses of existing rules -- each needs")
    print("  a fact the rules have no way to state: what bit 0 of an")
    print("  argument is, that two atoms are complementary, that `b` is")
    print("  not primitive, that two constants are one constant.")


def lasso(term, limit=64):
    """A closed term's value, as an eventually periodic bitstring.

    Returns (prefix, cycle). A term with no variables is a machine with
    no input, so its run is a lasso -- which is the point of s8.
    """
    machine = Machine(term)
    assert not machine.variables, "closed terms only"
    guard = consistent_guard(machine, {}, limit)
    state, seen, bits = machine.start(), {}, []
    while state not in seen:
        seen[state] = len(bits)
        state, out = machine.step(state, {}, guard)
        bits.append(out[machine.root])
    start = seen[state]
    return bits[:start], bits[start:]


def verify_constants_must_be_lassos() -> None:
    """Why `fold` is width-bound, and what the repair is.

    The engine folds a constant argument to an int. The constants of
    this language are not closed under its own operators: `U` of any
    nonzero finite set is cofinite, and `!` of the universe alternates
    forever. An int cannot hold either. An ultimately periodic
    bitstring can, and every closed term is one -- because a closed term
    is a machine with no input, and such a machine runs into a cycle.
    """
    print("  closed terms, as (prefix)(cycle)^ω, LSB first:")
    cases = [("0", ZERO), ("1", ONE), ("Ω", OMEGA),
             ("a(Ω)", a_(OMEGA)), ("!(Ω)", bang(OMEGA)),
             ("U(a(1))", up(a_(ONE))), ("T(Ω)", trail(OMEGA)),
             ("!(1)", bang(ONE)), ("lowset(Ω)", lowset(OMEGA)),
             ("N(b(0))", nonzero(b_(ZERO)))]
    engine = _load_engine()
    for label, term in cases:
        prefix, cycle = lasso(term)
        shown = ("".join(map(str, prefix)) or "ε") +             "(" + "".join(map(str, cycle)) + ")^ω"
        finite = set(cycle) == {0}
        note = "finite" if finite else "NOT a finite constant"
        print(f"    {label:<12} {shown:<16} {note}")
    print()
    print(f"  At WIDTH={engine.WIDTH} the engine folds `a(Ω)` to "
          f"{engine.SHIFTS['a'](engine.MASK)} and `!(Ω)` to "
          f"{engine.APPLY['!'](engine.MASK)}. Both are truncations of a")
    print("  cofinite set to the window the engine happens to use, so the")
    print("  fold is sound at that width and at no other.")
    print()
    print("  **This is the new primitive the canonicalisation needs.** Not")
    print("  a new operation -- 0046's eight still generate everything --")
    print("  but a new kind of constant: the closure of {0, 1} under the")
    print("  signature is the ultimately periodic sets, and the rewrite")
    print("  system's constants have to be those, written as lassos. That")
    print("  is the same move as 0046 s2: a symbol canonicalisation needs")
    print("  and the algebra does not.")


# ---------------------------------------------------------------------
# 7. where the wall actually is
# ---------------------------------------------------------------------

def _residuals(function, prefix_bits, tail_bits):
    """Distinct Nerode residuals of a two-input bit function.

    After reading `prefix_bits` bits of each argument LSB-first, the
    residual is the whole map from remaining input to remaining output.
    Two prefixes need distinct machine states exactly when their
    residuals differ, so this counts states from below.
    """
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


def verify_the_wall_is_bounded_state(tail_bits=5) -> None:
    """LSB-causal is not the property that decides. Finite state is."""
    print("  `x * y` is LSB-causal -- bit i of the product depends only on")
    print("  bits <= i of x and y -- so 0045 s4's test passes it. What it")
    print("  must carry between positions is the pending carry, and that")
    print("  is unbounded. Residual counts, by how much prefix has been")
    print(f"  read (tails of {tail_bits} bits):")
    print()
    functions = [("x ^ y", lambda x, y: x ^ y),
                 ("x + y", lambda x, y: x + y),
                 ("x * y", lambda x, y: x * y)]
    print("    prefix " + "".join(f"{label:>10}" for label, _ in functions))
    for prefix_bits in range(0, 7):
        counts = [_residuals(function, prefix_bits, tail_bits)
                  for _, function in functions]
        print(f"    {prefix_bits:>6} " + "".join(f"{n:>10}" for n in counts))
    print()
    print("  `x ^ y` needs one state, `x + y` needs two -- the carry bit --")
    print("  and both stop growing. `x * y` multiplies its count by")
    print("  four with every further bit read.")
    print()
    print("  So the frontier of this method is not `N`, and not")
    print("  information loss. It is the point where a term must remember")
    print("  an unbounded amount about the prefix it has read. Every")
    print("  operator in the 0046 basis stays under that line, and so")
    print("  would `+`, which the corpus does not have and could take for")
    print("  free. Multiplying two variables crosses it, and that is")
    print("  where a decision procedure of this shape stops existing.")


def verify_the_truth_guard_collapses() -> None:
    """Restricting to true statements does not shrink the problem."""
    print("  The premise to check first: does 'complete only for true")
    print("  statements' ask for less than full completeness?")
    print()
    print("    E1 = E2   iff   E1 ^ E2 = 0")
    print()
    print("  `^` is in the signature, so every equality question is a")
    print("  zero question and vice versa. A procedure that recognises")
    print("  exactly the true statements therefore decides the word")
    print("  problem outright. Demonstrated:")
    generator = random.Random(20260901)
    checked = 0
    for _ in range(200):
        left = random_term(generator, 2, ("x",))
        right = random_term(generator, 2, ("x",))
        assert equal(left, right) == (decide_zero(xor_(left, right)) is None)
        checked += 1
    print(f"    {checked} random pairs: `equal(p, q)` and "
          f"`decide_zero(p ^ q)` never disagree")
    print()
    print("  So the guard cannot make the DECISION easier. What it can")
    print("  make cheaper is the OUTPUT: a zero test owes nothing to the")
    print("  nonzero terms, and need not put them in any normal form at")
    print("  all. That is the only sense in which 'guarded' is a real")
    print("  weakening, and s5 is what it buys.")


# ---------------------------------------------------------------------

def run_verification_suite() -> None:
    sections = [
        ("The truth guard does not shrink the problem",
         verify_the_truth_guard_collapses),
        ("The compiled machine is the semantics",
         verify_the_machine_matches_the_interpreter),
        ("Bounded state, per operator", verify_the_state_is_bounded),
        ("The decision procedure against brute force",
         verify_the_decision_matches_brute_force),
        ("`N` is the guard, and the guard is all it costs",
         verify_the_guard_is_what_n_costs),
        ("The minimal machine is a canonical form",
         verify_the_canonical_form_is_canonical),
        ("Truth is the zero machine, under every consistent guard",
         verify_truth_is_the_zero_machine),
        ("What the rewrite system misses", verify_the_missing_laws),
        ("ANF does not fold constants (a correction to 0044)",
         verify_anf_does_not_fold_constants),
        ("Constants have to be lassos", verify_constants_must_be_lassos),
        ("Measured against the rewrite system",
         verify_the_rewrite_system_is_incomplete),
        ("Where the wall is", verify_the_wall_is_bounded_state),
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
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    run_verification_suite()
