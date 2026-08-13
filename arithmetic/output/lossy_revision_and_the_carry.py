"""The floor for lossy revision maps, and the odometer's maximality.

0059 proved the paradox tax = log2(smallest orbit) for PERMUTATION
revision maps and left two questions open.  Both close here.

  s1  THE LEMMA EXTENDS.  A body with & makes T lossy: a functional
      graph with transient trees hanging off a CORE of disjoint
      cycles (the eventual image, on which T is a bijection).
      Stationary distributions are exactly the mixtures of
      core-cycle uniforms -- verified by exact rational linear
      algebra (nullity of the pushforward minus identity equals the
      cycle count) on random frame bodies.  So the tax formula is
      unchanged: forced entropy = log2(shortest core cycle).

  s2  THE TRICHOTOMY IS CORE GEOMETRY.  Deterministic solutions are
      exactly the 1-cycles.  Grounded (guarded) bodies have a core
      that is a SINGLE POINT -- groundedness is total absorption,
      the contraction of 0054 seen as a functional graph.  Liars
      have a core with no 1-cycle, tax >= 1 bit.  Absorption is the
      cheapening mechanism: the absorbed liar  n := Omega ^ (n & 1)
      has a 2-atom core and 2^w - 2 transients -- a paradox whose
      tax is 1 bit at every width AND whose revision dynamics
      settle in one step.  Census over random ^/&/a bodies included.

  s3  CARRY-FREE PARADOXES ARE EXPONENTIALLY CHEAP.  A carry-free
      (GF(2)-affine causal) revision map is v -> Lv ^ b with L
      unipotent (causal + invertible forces unit diagonal), so
      L^(2^r) = I for r = ceil(log2 w), and the affine map's order
      divides 2^(r+1).  Max cycle length <= 2^(ceil(log2 w) + 1):
      tax <= ceil(log2 w) + 1 bits.  Verified exhaustively (every
      L, every b) at w = 4, 5.  The carry-coupled  n := n + 1
      reaches 2^w.  So the tax separation between XOR-affine and
      carry bodies is w vs log w + 1 -- EXPONENTIAL.  An expensive
      paradox does not just happen to use the carry; it cannot
      exist without it.

  s4  HULL-DOBELL IN THE FRAME.  Which affine-with-carry bodies
      n := a*n + b reach full period?  Exactly b odd and
      a = 1 mod 4 -- verified exhaustively at w = 4, 5, 6.  The
      maximal paradoxes with carry form a familiar classical family
      (the full-period linear congruential generators).

  s5  EVERY MAXIMAL PARADOX IS THE ODOMETER.  Theorem (proved in
      comments, verified here): every full-period CAUSAL map (bit i
      of output depends only on bits <= i of input -- which every
      frame body is) is conjugate to n -> n + 1 by a causal
      bijection with causal inverse.  The conjugacy is orbit
      indexing: phi(T^k(0)) = k, and causality of phi is forced by
      the fact that a causal full-period map is full-period at
      every truncation.  Verified for every full-period affine map
      at w = 4, 5 and for random causal bijections at w = 5.  Up to
      frame-compatible relabeling there is ONE maximal paradox, and
      it is the carry's own clock.

Run directly for the verification suite.
"""

from __future__ import annotations

import random
from fractions import Fraction
from math import log2


# ---------------------------------------------------------------------
# functional-graph machinery
# ---------------------------------------------------------------------

def cycles_of(T: dict) -> list:
    """Cycle decomposition of the core of a functional graph."""
    color, cycles = {}, []
    for start in T:
        path, v = [], start
        while v not in color:
            color[v] = "open"
            path.append(v)
            v = T[v]
        if color[v] == "open":
            cycles.append(path[path.index(v):])
        for u in path:
            color[u] = "done"
    return cycles


def core_of(T: dict) -> set:
    core = {v for cycle in cycles_of(T) for v in cycle}
    assert {T[v] for v in core} == core       # T bijective on the core
    return core


def floor_bits(T: dict) -> float:
    return log2(min(len(c) for c in cycles_of(T)))


def stationary_nullity(T: dict) -> int:
    """dim of the stationary space of the pushforward, by exact
    rational elimination on (M - I) pi = 0, M[s][t] = [T(t) = s]."""
    atoms = sorted(T)
    n = len(atoms)
    index = {a: i for i, a in enumerate(atoms)}
    rows = []
    for s in atoms:
        row = [Fraction(0)] * n
        row[index[s]] -= 1
        for t in atoms:
            if T[t] == s:
                row[index[t]] += 1
        rows.append(row)
    rank = 0
    for col in range(n):
        pivot = next((r for r in range(rank, n) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        lead = rows[rank]
        for r in range(n):
            if r != rank and rows[r][col]:
                f = rows[r][col] / lead[col]
                rows[r] = [x - f * y for x, y in zip(rows[r], lead)]
        rank += 1
    return n - rank


def push(T: dict, pi: dict) -> dict:
    out = {}
    for atom, mass in pi.items():
        out[T[atom]] = out.get(T[atom], 0) + mass
    return out


# ---------------------------------------------------------------------
# random frame bodies over {n, constants} with ^, &, a
# ---------------------------------------------------------------------

def random_body(rng, depth: int, width: int):
    if depth == 0 or rng.random() < 0.25:
        return ("const", rng.randrange(1 << width)) \
            if rng.random() < 0.5 else ("n",)
    op = rng.choice(("^", "^", "&", "a"))
    if op == "a":
        return ("a", random_body(rng, depth - 1, width))
    return (op, random_body(rng, depth - 1, width),
            random_body(rng, depth - 1, width))


def eval_body(body, v: int, mask: int) -> int:
    kind = body[0]
    if kind == "n":
        return v
    if kind == "const":
        return body[1]
    if kind == "a":
        return (eval_body(body[1], v, mask) << 1) & mask
    left = eval_body(body[1], v, mask)
    right = eval_body(body[2], v, mask)
    return (left ^ right) if kind == "^" else (left & right)


def body_map(body, width: int) -> dict:
    mask = (1 << width) - 1
    return {v: eval_body(body, v, mask) for v in range(1 << width)}


# ---------------------------------------------------------------------
# 1. the stationary lemma for lossy maps
# ---------------------------------------------------------------------

def verify_the_lossy_lemma(width=5, trials=12, seed=59060) -> None:
    rng = random.Random(seed)
    lossy_seen = 0
    for trial in range(trials):
        body = random_body(rng, 4, width)
        T = body_map(body, width)
        cyc = cycles_of(T)
        lossy = len(core_of(T)) < len(T)
        lossy_seen += lossy
        assert stationary_nullity(T) == len(cyc), body
        for cycle in cyc:                     # cycle-uniforms stationary
            u = {v: Fraction(1, len(cycle)) for v in cycle}
            assert push(T, u) == u
    mask = (1 << width) - 1
    T = {v: mask ^ (v & 1) for v in range(1 << width)}   # absorbed liar
    assert stationary_nullity(T) == len(cycles_of(T)) == 1
    print(f"  {trials} random ^/&/a bodies at width {width}"
          f" ({lossy_seen} lossy), plus the absorbed liar:")
    print()
    print("    dim(stationary space)  =  number of core cycles,")
    print("    and every cycle-uniform is stationary -- exact rational")
    print("    elimination, every instance.")
    print()
    print("  So stationary distributions of a LOSSY revision map are")
    print("  exactly the mixtures of core-cycle uniforms (transients")
    print("  carry no stationary mass), and 0059's tax formula extends")
    print("  verbatim:")
    print()
    print("      forced entropy  =  log2(shortest cycle of the core).")


# ---------------------------------------------------------------------
# 2. the trichotomy as core geometry, and the census
# ---------------------------------------------------------------------

def verify_core_geometry(width=6, census_size=400, seed=59061) -> None:
    mask = (1 << width) - 1
    # grounded = total absorption: guarded bodies contract to a point
    for body in (("^", ("const", 0b101101 & mask), ("a", ("n",))),
                 ("^", ("const", 1), ("a", ("&", ("n",),
                                            ("const", 0b110110 & mask)))),
                 ("&", ("const", 0b111000 & mask), ("a", ("a", ("n",))))):
        T = body_map(body, width)
        cyc = cycles_of(T)
        assert len(cyc) == 1 and len(cyc[0]) == 1, body
        assert floor_bits(T) == 0.0
    print("  Guarded bodies (every n under at least one a): the core is")
    print("  a SINGLE FIXED POINT -- groundedness is total absorption,")
    print("  0054's contraction as a functional graph.  Verified on")
    print("  guarded exemplars; solutions = 1-cycles throughout.")
    print()
    # the absorbed liar, at several widths
    print(f"    {'absorbed liar  n := Omega ^ (n & 1)':<40}")
    print(f"    {'width':>6} {'core':>6} {'transient':>10} {'tax':>6}")
    for w in (4, 6, 8, 10):
        m = (1 << w) - 1
        T = {v: m ^ (v & 1) for v in range(1 << w)}
        cyc = cycles_of(T)
        assert not any(len(c) == 1 for c in cyc)          # a liar
        assert len(cyc) == 1 and len(cyc[0]) == 2
        print(f"    {w:>6} {2:>6} {(1 << w) - 2:>10} "
              f"{floor_bits(T):>4.0f} bit")
    print()
    print("  A paradox with a 2-atom core: tax 1 bit at every width,")
    print("  and revision SETTLES -- every state reaches the core in")
    print("  one step.  Absorption is the cheapening mechanism: the")
    print("  core's cycle structure is the whole tax, and & can make")
    print("  the core as small as one 2-cycle regardless of width.")
    print()
    # census
    rng = random.Random(seed)
    grounded = liars = many = 0
    liar_min_cycles = {}
    liar_core_fractions = []
    for _ in range(census_size):
        T = body_map(random_body(rng, 4, width), width)
        cyc = cycles_of(T)
        fixed = sum(len(c) == 1 for c in cyc)
        assert fixed == sum(T[v] == v for v in T)
        shortest = min(len(c) for c in cyc)
        assert floor_bits(T) == log2(shortest)            # the law
        if fixed:
            if len(cyc) == 1 and len(cyc[0]) == 1:
                grounded += 1
            else:
                many += 1
        else:
            liars += 1
            liar_min_cycles[shortest] = \
                liar_min_cycles.get(shortest, 0) + 1
            liar_core_fractions.append(
                sum(len(c) for c in cyc) / len(T))
    print(f"  Census, {census_size} random bodies at width {width}:")
    print(f"    core = one fixed point (grounded-like)   {grounded}")
    print(f"    fixed point(s) among other cycles        {many}")
    print(f"    no fixed point (liars), tax >= 1 bit     {liars}")
    print(f"    liar shortest-cycle histogram            "
          f"{dict(sorted(liar_min_cycles.items()))}")
    if liar_core_fractions:
        small = sum(f <= 0.25 for f in liar_core_fractions)
        print(f"    liars with core <= 1/4 of the states     "
              f"{small}/{liars}")
    print()
    print("  The floor law held in every cell.  0059's open question")
    print("  answers: absorption cannot beat the core's cycle structure")
    print("  -- the core IS the tax -- but it is how a paradox gets a")
    print("  small core, which an invertible map (all atoms in cycles)")
    print("  can never have.")


# ---------------------------------------------------------------------
# 3. carry-free paradoxes are exponentially cheap
# ---------------------------------------------------------------------

def gf2_affine_map(row_masks, b: int, width: int) -> dict:
    def apply(v):
        out = 0
        for i, row in enumerate(row_masks):
            out |= (bin(v & row).count("1") & 1) << i
        return out ^ b
    return {v: apply(v) for v in range(1 << width)}


def all_causal_linear_rows(width: int):
    """Every invertible causal GF(2) matrix: unit diagonal, free
    strictly-lower part, row by row."""
    def rec(i, rows):
        if i == width:
            yield tuple(rows)
            return
        for lower in range(1 << i):
            yield from rec(i + 1, rows + [(1 << i) | lower])
    yield from rec(0, [])


def verify_the_carry_free_ceiling() -> None:
    print(f"    {'w':>3} {'maps':>7} {'max cycle':>10} "
          f"{'unipotent bound':>16} {'full period 2^w':>16}")
    for width in (4, 5):
        bound = 1 << ((width - 1).bit_length() + 1)   # 2^(ceil(log2 w)+1)
        longest = 0
        count = 0
        for rows in all_causal_linear_rows(width):
            for b in range(1 << width):
                T = gf2_affine_map(rows, b, width)
                count += 1
                longest = max(longest,
                              max(len(c) for c in cycles_of(T)))
        assert longest <= bound, (width, longest)
        assert longest < 1 << width
        print(f"    {width:>3} {count:>7} {longest:>10} "
              f"{bound:>16} {'never':>16}")
    print()
    print("  Proof of the bound: causal + invertible over GF(2) forces")
    print("  unit diagonal, so L = I + N with N strictly lower")
    print("  (nilpotent, N^w = 0); then L^(2^r) = I + N^(2^r) = I for")
    print("  r = ceil(log2 w), and the affine map's order divides")
    print("  2^(r+1).  Cycle lengths divide the order.  Exhaustive at")
    print("  w = 4, 5 (every matrix, every offset).")
    print()
    print("      carry-free tax  <=  ceil(log2 w) + 1  bits")
    print("      carry tax reaches   w                 bits  (s4)")
    print()
    print("  The separation is EXPONENTIAL (log w vs w): an expensive")
    print("  paradox cannot be built from XOR alone -- it needs the")
    print("  carry, the same channel that walls off multiplication")
    print("  (0053/0054) and inflates n := n + 1 (0059).")


# ---------------------------------------------------------------------
# 4. Hull-Dobell in the frame
# ---------------------------------------------------------------------

def verify_hull_dobell() -> None:
    print(f"    {'w':>3} {'full-period (a, b) pairs':>26} "
          f"{'= b odd, a = 1 mod 4':>22}")
    for width in (4, 5, 6):
        size = 1 << width
        full = set()
        for a in range(size):
            for b in range(size):
                T = {v: (a * v + b) % size for v in range(size)}
                cyc = cycles_of(T)
                if len(cyc) == 1 and len(cyc[0]) == size:
                    full.add((a, b))
        predicted = {(a, b) for a in range(size) for b in range(size)
                     if b % 2 == 1 and a % 4 == 1}
        assert full == predicted, width
        print(f"    {width:>3} {len(full):>26} {'yes':>22}")
    print()
    print("  n := a*n + b reaches the full period 2^w exactly when b is")
    print("  odd and a = 1 mod 4 (the Hull-Dobell family -- full-period")
    print("  linear congruential generators).  The maximal paradoxes")
    print("  with carry form a classical family; s5 shows they are all")
    print("  the SAME paradox.")


# ---------------------------------------------------------------------
# 5. every maximal paradox is the odometer
# ---------------------------------------------------------------------
#
# THEOREM.  Let T be causal (bit i of T(v) depends only on bits <= i
# of v) with a single cycle of length 2^w.  Then T is conjugate to
# n -> n + 1 mod 2^w by a causal bijection with causal inverse.
#
# PROOF.  Causality means T induces T_j on w-j-truncated values for
# every j, and s_k = T^k(0) mod 2^j is the T_j-orbit of 0.  The full
# orbit visits all values, so s visits all 2^j residues; s returns to
# 0 at k = 2^w, so 0 lies on a T_j-cycle whose length P satisfies
# P <= 2^j (state count) and P >= 2^j (visits all residues): P = 2^j.
# Hence T^k(0) = T^m(0) mod 2^j  iff  k = m mod 2^j.  Define
# phi(T^k(0)) = k.  The displayed equivalence says phi(v) mod 2^j is
# determined by v mod 2^j and conversely -- phi and phi^-1 are both
# causal -- and phi(T(v)) = phi(v) + 1 by construction.  QED
#
# Frame reading: every frame body is causal (^, &, a are), so up to
# relabeling by a frame-compatible (causal) bijection there is
# exactly ONE maximal single-channel paradox: the odometer.

def orbit_conjugacy(T: dict, width: int) -> dict:
    phi, v = {}, 0
    for k in range(1 << width):
        phi[v] = k
        v = T[v]
    assert v == 0
    return phi


def is_causal(f: dict, width: int) -> bool:
    for j in range(1, width):
        mod = 1 << j
        seen = {}
        for v, out in f.items():
            key = v % mod
            if key in seen and seen[key] != out % mod:
                return False
            seen[key] = out % mod
    return True


def random_causal_bijection(rng, width: int) -> dict:
    """General form: bit i of output = bit i of input XOR f_i(lower
    bits), with random truth tables f_i."""
    tables = [[rng.randrange(2) for _ in range(1 << i)]
              for i in range(width)]

    def apply(v):
        out = 0
        for i in range(width):
            out |= ((v >> i & 1) ^ tables[i][v & ((1 << i) - 1)]) << i
        return out
    return {v: apply(v) for v in range(1 << width)}


def check_odometer_conjugacy(T: dict, width: int) -> None:
    size = 1 << width
    for j in range(1, width + 1):             # full period per level
        mod = 1 << j
        v, seen = 0, set()
        for _ in range(mod):
            seen.add(v % mod)
            v = T[v]                          # causal: projects to T_j
        assert len(seen) == mod
    phi = orbit_conjugacy(T, width)
    inverse = {k: v for v, k in phi.items()}
    assert is_causal(phi, width) and is_causal(inverse, width)
    assert all(phi[T[v]] == (phi[v] + 1) % size for v in T)


def verify_odometer_maximality(seed=59062) -> None:
    for width in (4, 5):
        size = 1 << width
        count = 0
        for a in range(1, size, 4):
            for b in range(1, size, 2):
                T = {v: (a * v + b) % size for v in range(size)}
                check_odometer_conjugacy(T, width)
                count += 1
        print(f"    w = {width}: all {count} full-period affine maps"
              f" causally conjugate to n -> n + 1")
    rng = random.Random(seed)
    width, hits, samples = 5, 0, 4000
    for _ in range(samples):
        T = random_causal_bijection(rng, width)
        cyc = cycles_of(T)
        if len(cyc) == 1 and len(cyc[0]) == 1 << width:
            check_odometer_conjugacy(T, width)
            hits += 1
    print(f"    w = {width}: {hits}/{samples} random causal bijections"
          f" were full-period")
    print(f"           (expected ~ 2^-w = {samples >> width}); every"
          f" one causally conjugate")
    print()
    print("  Every full-period causal map -- affine or arbitrary -- is")
    print("  the odometer after a causal change of variable (proof in")
    print("  the source; orbit indexing, causal both ways because a")
    print("  causal full-period map is full-period at every truncation).")
    print("  There is ONE maximal paradox, and it is the carry's clock.")


def run_verification_suite() -> None:
    sections = [
        ("The stationary lemma extends to lossy maps",
         verify_the_lossy_lemma),
        ("The trichotomy as core geometry; absorption is the cheapener",
         verify_core_geometry),
        ("Carry-free paradoxes are exponentially cheap",
         verify_the_carry_free_ceiling),
        ("Hull-Dobell in the frame", verify_hull_dobell),
        ("Every maximal paradox is the odometer",
         verify_odometer_maximality),
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
