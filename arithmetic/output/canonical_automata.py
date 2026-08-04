"""Canonical symbolic addition: terms with free variables reduce to
canonical minimal automata.

The symbolic-convexity gap (0002 section "What this does not yet give"):
ground terms reduce by the carry recursion, but symbolic terms like
add(x, y) have no ground popcount to bound the recursion. This module
closes the gap for the addition fragment. The canonical form of a
statement is the minimal complete synchronous DFA of the relation it
denotes, read lsb-first over one track per free variable:

  - Myhill-Nerode: the minimal complete DFA is unique, so the canonical
    form is unique -- the arithmetic analogue of ANF uniqueness.
  - Every compilation step carries an a-priori size bound readable off
    the term (product <= |A|*|B|, determinization <= 2^n, minimization
    shrinks), so the reduction is knowably terminating with no
    cleverness.
  - A statement is TRUE iff its canonical automaton is the universal
    one-state automaton -- the automatic-fragment analogue of "reduces
    to 0".  Entailment K |= H is language containment, decided by
    emptiness of K & ~H.  The judgment stays one-sided: universal /
    not-universal, containment / no-containment.

Encoding: a tuple of finite sets (numbers) is a word over {0,1}^k,
letter i giving bit i of every track; any amount of zero-padding is
accepted (decode-based languages), which is what makes projection of
internal tracks sound.

Base relations (each a hand-built DFA, correctness sampled in the
suite): z = x^y, z = x&y, z = a(x), z = b(x), z = add(x,y) (the 2-state
carry automaton -- the closed form of the stabilizing series of 0002),
z = T(x) (trailing-ones, 2 states), x = c, z = x.

Terms: ('var', name) | ('const', n) | ('a'|'b'|'T', t) |
('xor'|'and'|'add', t1, t2).  Run this file directly for the suite.
"""

from itertools import product as iproduct


class DFA:
    """Partial DFA; missing transitions are an implicit dead state.

    vars: sorted tuple of track names.  Letters are bit tuples aligned
    with vars.  States are 0..n-1.
    """

    def __init__(self, varnames, n, init, trans, accept):
        self.vars = tuple(varnames)
        self.n = n
        self.init = init
        self.trans = trans          # dict[(state, letter)] -> state
        self.accept = frozenset(accept)

    def letters(self):
        return list(iproduct((0, 1), repeat=len(self.vars)))


def _proj_letter(letter, from_vars, to_vars):
    idx = {v: i for i, v in enumerate(from_vars)}
    return tuple(letter[idx[v]] for v in to_vars)


def product_dfa(A, B):
    """Intersection; extra tracks of either side are cylindrified.
    State bound: |A| * |B| (a-priori)."""
    varnames = tuple(sorted(set(A.vars) | set(B.vars)))
    letters = list(iproduct((0, 1), repeat=len(varnames)))
    states = {(A.init, B.init): 0}
    order = [(A.init, B.init)]
    trans = {}
    i = 0
    while i < len(order):
        sa, sb = order[i]
        for L in letters:
            ta = A.trans.get((sa, _proj_letter(L, varnames, A.vars)))
            tb = B.trans.get((sb, _proj_letter(L, varnames, B.vars)))
            if ta is None or tb is None:
                continue
            if (ta, tb) not in states:
                states[(ta, tb)] = len(order)
                order.append((ta, tb))
            trans[(i, L)] = states[(ta, tb)]
        i += 1
    accept = {si for (sa, sb), si in states.items()
              if sa in A.accept and sb in B.accept}
    return DFA(varnames, len(order), 0, trans, accept)


def complete(A):
    letters = A.letters()
    if all((s, L) in A.trans for s in range(A.n) for L in letters):
        return A
    trans = dict(A.trans)
    dead = A.n
    for s in range(A.n + 1):
        for L in letters:
            trans.setdefault((s, L), dead)
    return DFA(A.vars, A.n + 1, A.init, trans, A.accept)


def complement(A):
    A = complete(A)
    return DFA(A.vars, A.n, A.init, A.trans,
               set(range(A.n)) - set(A.accept))


def project(A, gone):
    """Existential projection of tracks `gone`, with padding closure
    (a state accepts if an accepting state is reachable via letters
    that are zero on every remaining track -- the projected tracks may
    need more bits than the surviving word carries).
    State bound after determinization: 2^|A| (a-priori)."""
    gone = set(gone)
    keep = tuple(v for v in A.vars if v not in gone)
    # padding closure on the NFA states
    zero_edges = {s: set() for s in range(A.n)}
    for (s, L), t in A.trans.items():
        if all(b == 0 for b, v in zip(L, A.vars) if v in keep):
            zero_edges[s].add(t)
    closed = set(A.accept)
    frontier = set(closed)
    while frontier:
        frontier = {s for s in range(A.n)
                    if s not in closed and zero_edges[s] & closed}
        closed |= frontier
    # NFA transitions over surviving tracks
    ntrans = {}
    for (s, L), t in A.trans.items():
        ntrans.setdefault((s, _proj_letter(L, A.vars, keep)), set()).add(t)
    # subset construction
    letters = list(iproduct((0, 1), repeat=len(keep)))
    start = frozenset([A.init])
    states = {start: 0}
    order = [start]
    trans = {}
    i = 0
    while i < len(order):
        cur = order[i]
        for L in letters:
            nxt = frozenset(t for s in cur for t in ntrans.get((s, L), ()))
            if not nxt:
                continue
            if nxt not in states:
                states[nxt] = len(order)
                order.append(nxt)
            trans[(i, L)] = states[nxt]
        i += 1
    accept = {si for sub, si in states.items() if sub & closed}
    return DFA(keep, len(order), 0, trans, accept)


def minimize(A):
    """Unique minimal complete DFA (Myhill-Nerode), states renamed in
    BFS order over sorted letters: strict canonical form, comparable
    with ==."""
    A = complete(A)
    letters = sorted(A.letters())
    reach = {A.init}
    frontier = [A.init]
    while frontier:
        s = frontier.pop()
        for L in letters:
            t = A.trans[(s, L)]
            if t not in reach:
                reach.add(t)
                frontier.append(t)
    # Moore partition refinement
    block = {s: (s in A.accept) for s in reach}
    while True:
        sig = {s: (block[s],) + tuple(block[A.trans[(s, L)]] for L in letters)
               for s in reach}
        newids = {}
        for s in sorted(reach):
            newids.setdefault(sig[s], len(newids))
        newblock = {s: newids[sig[s]] for s in reach}
        if newblock == block:
            break
        block = newblock
    # canonical BFS naming of the quotient
    name = {block[A.init]: 0}
    order = [block[A.init]]
    qtrans = {}
    i = 0
    while i < len(order):
        b = order[i]
        s = next(s for s in reach if block[s] == b)
        for L in letters:
            tb = block[A.trans[(s, L)]]
            if tb not in name:
                name[tb] = len(order)
                order.append(tb)
            qtrans[(i, L)] = name[tb]
        i += 1
    accept = {name[block[s]] for s in reach if s in A.accept and
              block[s] in name}
    return DFA(A.vars, len(order), 0, qtrans, accept)


def canonical_key(A):
    A = minimize(A)
    return (A.vars, A.n, A.init, tuple(sorted(A.trans.items())),
            tuple(sorted(A.accept)))


def is_empty(A):
    seen = {A.init}
    frontier = [A.init]
    while frontier:
        s = frontier.pop()
        if s in A.accept:
            return False
        for L in A.letters():
            t = A.trans.get((s, L))
            if t is not None and t not in seen:
                seen.add(t)
                frontier.append(t)
    return A.init not in A.accept


def is_universal(A):
    return is_empty(complement(A))


def entails(K, H):
    """K |= H as language containment: K & ~H empty. One-sided."""
    return is_empty(product_dfa(K, complement(H)))


# ---------------------------------------------------------------------
# Base relation automata
# ---------------------------------------------------------------------

def _rel2(x, z, table, n, init, accept):
    """Helper for 2-track relations given per-state bit tables."""
    varnames = tuple(sorted((x, z)))
    flip = varnames != (x, z)
    trans = {}
    for (s, xb, zb), t in table.items():
        L = (zb, xb) if flip else (xb, zb)
        trans[(s, L)] = t
    return DFA(varnames, n, init, trans, accept)


def rel_xor(x, y, z):
    varnames = tuple(sorted((x, y, z)))
    idx = {v: i for i, v in enumerate(varnames)}
    trans = {}
    for L in iproduct((0, 1), repeat=3):
        if L[idx[z]] == L[idx[x]] ^ L[idx[y]]:
            trans[(0, L)] = 0
    return DFA(varnames, 1, 0, trans, {0})


def rel_and(x, y, z):
    varnames = tuple(sorted((x, y, z)))
    idx = {v: i for i, v in enumerate(varnames)}
    trans = {}
    for L in iproduct((0, 1), repeat=3):
        if L[idx[z]] == (L[idx[x]] & L[idx[y]]):
            trans[(0, L)] = 0
    return DFA(varnames, 1, 0, trans, {0})


def rel_add(x, y, z):
    """z = x + y: the 2-state carry automaton -- the closed form of the
    stabilizing carry series (0002 Props 5/6)."""
    varnames = tuple(sorted((x, y, z)))
    idx = {v: i for i, v in enumerate(varnames)}
    trans = {}
    for c in (0, 1):
        for L in iproduct((0, 1), repeat=3):
            xb, yb, zb = L[idx[x]], L[idx[y]], L[idx[z]]
            if zb == xb ^ yb ^ c:
                trans[(c, L)] = (xb & yb) | (xb & c) | (yb & c)
    return DFA(varnames, 2, 0, trans, {0})


def rel_shift0(x, z):
    """z = a(x) = 2x. State = pending bit owed to z."""
    table = {}
    for e in (0, 1):
        for xb in (0, 1):
            table[(e, xb, e)] = xb
    return _rel2(x, z, table, 2, 0, {0})


def rel_shift1(x, z):
    """z = b(x) = 2x + 1. Start state demands z's low bit be 1."""
    table = {}
    for xb in (0, 1):
        table[(2, xb, 1)] = xb        # state 2 = start
        for e in (0, 1):
            table[(e, xb, e)] = xb
    return _rel2(x, z, table, 3, 2, {0})


def rel_T(x, z):
    """z = T(x), the trailing-ones mask: 2 states (in/out of the
    trailing-ones region) -- the closed form of the series
    x & b(x) & b(b(x)) & ... (0002 Prop 2)."""
    table = {
        (1, 1, 1): 1,   # in region, x bit 1: mask bit 1, stay
        (1, 0, 0): 0,   # in region, x bit 0: mask bit 0, leave
        (0, 0, 0): 0,   # out: mask bit 0 regardless
        (0, 1, 0): 0,
    }
    return _rel2(x, z, table, 2, 1, {0, 1})


def rel_eq(x, z):
    table = {(0, 0, 0): 0, (0, 1, 1): 0}
    return _rel2(x, z, table, 1, 0, {0})


def rel_const(x, c):
    """x = c. States 0..bitlen(c); state i accepting iff c >> i == 0."""
    nbits = max(c.bit_length(), 1)
    trans = {}
    for i in range(nbits):
        trans[(i, ((c >> i) & 1,))] = i + 1
    trans[(nbits, (0,))] = nbits
    accept = {i for i in range(nbits + 1) if c >> i == 0}
    return DFA((x,), nbits + 1, 0, trans, accept)


# ---------------------------------------------------------------------
# Term compilation
# ---------------------------------------------------------------------

def _internal(v):
    return v.startswith("_")


def compile_term(term, counter=None):
    """Returns (dfa, result_var). Internal tracks are projected eagerly,
    so track count stays at most 4 at any step."""
    if counter is None:
        counter = [0]

    def fresh():
        counter[0] += 1
        return f"_{counter[0]}"

    kind = term[0]
    if kind == 'var':
        v = term[1]
        return DFA((v,), 1, 0, {(0, (0,)): 0, (0, (1,)): 0}, {0}), v
    if kind == 'const':
        r = fresh()
        return rel_const(r, term[1]), r
    if kind in ('a', 'b', 'T'):
        A, u = compile_term(term[1], counter)
        r = fresh()
        base = {'a': rel_shift0, 'b': rel_shift1, 'T': rel_T}[kind](u, r)
        D = product_dfa(A, base)
        if _internal(u):
            D = project(D, {u})
        return minimize(D), r
    if kind in ('xor', 'and', 'add'):
        A1, u1 = compile_term(term[1], counter)
        A2, u2 = compile_term(term[2], counter)
        r = fresh()
        base = {'xor': rel_xor, 'and': rel_and, 'add': rel_add}[kind]
        D = product_dfa(product_dfa(A1, A2), base(u1, u2, r))
        drop = {u for u in (u1, u2) if _internal(u)}
        if drop:
            D = project(D, drop)
        return minimize(D), r
    raise ValueError(f"unknown term {term!r}")


def stmt_eq(t1, t2):
    """The statement 't1 = t2' as a canonical automaton over the free
    variables. This is the symbolic H ^ HK substrate: equality is XOR
    reducing to 0, here realized as the equality relation on the two
    result tracks with internals projected away."""
    counter = [0]
    A1, r1 = compile_term(t1, counter)
    A2, r2 = compile_term(t2, counter)
    if r1 == r2:
        D = product_dfa(A1, A2)
    else:
        D = product_dfa(product_dfa(A1, A2), rel_eq(r1, r2))
    drop = {u for u in (r1, r2) if _internal(u)}
    if drop:
        D = project(D, drop)
    return minimize(D)


def exists(A, varname):
    return minimize(project(A, {varname}))


def accepts(A, assign):
    """Does the automaton accept this variable assignment?"""
    n = max([v.bit_length() for v in assign.values()] + [1]) + 1
    s = A.init
    for i in range(n):
        L = tuple((assign[v] >> i) & 1 for v in A.vars)
        s = A.trans.get((s, L))
        if s is None:
            return False
    return s in A.accept


# ---------------------------------------------------------------------
# Verification suite
# ---------------------------------------------------------------------

def _verify(seed=20260804):
    import random
    rng = random.Random(seed)
    x, y, w, z = (('var', v) for v in 'xywz')

    # Base add automaton against ground arithmetic
    ADD = rel_add('x', 'y', 'z')
    for _ in range(2000):
        a_, b_ = rng.randrange(1 << 16), rng.randrange(1 << 16)
        assert accepts(ADD, {'x': a_, 'y': b_, 'z': a_ + b_})
        assert not accepts(ADD, {'x': a_, 'y': b_,
                                 'z': a_ + b_ + rng.randrange(1, 9)})
    print("base add automaton: 2000 accept + 2000 reject samples  OK")

    # THE decisive test: succ two ways -> identical canonical automaton.
    # x ^ b(T(x)) (the stabilizing-series successor, 0002 Prop 3)
    # vs add(x, 1): same canonical object, mechanically.
    succ_series = stmt_eq(('xor', x, ('b', ('T', x))), z)
    succ_add = stmt_eq(('add', x, ('const', 1)), z)
    assert canonical_key(succ_series) == canonical_key(succ_add)
    print(f"succ via series == succ via add(x,1): identical canonical "
          f"automaton ({succ_series.n} states)  OK")

    # Laws of addition as universality (the 'reduces to 0' analogue)
    assert is_universal(stmt_eq(('add', x, y), ('add', y, x)))
    assert is_universal(stmt_eq(('add', ('add', x, y), w),
                                ('add', x, ('add', y, w))))
    assert is_universal(stmt_eq(('add', x, ('const', 0)), x))
    print("commutativity, associativity, unit: universal  OK")

    # Carry-save identity (clue/2026-06-21):
    # add(x^y^w, a(xy ^ xw ^ yw)) = x + y + w
    lhs = ('add', ('xor', x, ('xor', y, w)),
           ('a', ('xor', ('and', x, y),
                  ('xor', ('and', x, w), ('and', y, w)))))
    rhs = ('add', x, ('add', y, w))
    assert is_universal(stmt_eq(lhs, rhs))
    print("carry-save identity: universal  OK")

    # One-sidedness: a non-law is not universal and not empty
    ne = stmt_eq(('add', x, y), x)
    assert not is_universal(ne) and not is_empty(ne)
    print("add(x,y) = x: neither universal nor empty (undecided as a "
          "law, satisfiable as a constraint)  OK")

    # Entailment, strict: y = a(x)  |=  exists w: y = add(w,w)
    K = stmt_eq(y, ('a', x))
    H = exists(stmt_eq(y, ('add', w, w)), 'w')
    assert entails(K, H) and not entails(H, K)
    print("y = 2x entails (exists w: y = w+w), and not conversely  OK")

    # Multiplication by a constant stays in the fragment: z = 3x
    THREE = stmt_eq(('add', x, ('a', x)), z)
    for _ in range(500):
        v = rng.randrange(1 << 24)
        assert accepts(THREE, {'x': v, 'z': 3 * v})
        assert not accepts(THREE, {'x': v, 'z': 3 * v + 1})
    print(f"z = 3x via add(x, a(x)): 500 samples "
          f"({THREE.n} canonical states)  OK")

    # Canonical sizes (complete minimal automata, dead state included)
    for label, D in [("z = x + y", minimize(ADD)),
                     ("z = x + 1", succ_add),
                     ("z = T(x)", stmt_eq(('T', x), z)),
                     ("z = 3x", THREE)]:
        print(f"    canonical size  {label}: {minimize(D).n} states")

    print("all checks passed")


if __name__ == "__main__":
    _verify()
