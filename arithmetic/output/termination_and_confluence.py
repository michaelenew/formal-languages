"""Does expand-and-cancel terminate? Is it confluent? No, and no.

Both are theorems with finite, machine-checkable certificates, and both
say something structural rather than reporting a defect.

  TERMINATION.  The inner loop -- the local rules with `collect` and
  `telescope` deleted -- terminates, by a reduction order (s1, a real
  proof, audited by machine on every sampled application).  Expansion
  does not: `!(x)` has a reduction graph that is a SINGLE INFINITE PATH
  (s2), so no strategy helps.  Stronger, the system is not even weakly
  normalizing: `U(x)` has no normal form at all (s3), because normal
  forms are local functions plus N-guards, and the series are exactly
  the non-local operators.  Non-termination is not a bug -- it is
  0002 Prop 4's "the series is necessary", promoted to the whole
  rewrite system.

  CONFLUENCE.  Fails, with a finite certificate (s4):

      !(x&1)  --confine-->  N(x&1)
      !(x&1)  --expand--->  x&1 ^ a(!(x&1))  -->*  x&1 ^ a(N(x&1))

  and both results are irreducible, distinct, and provably equal.  The
  diagnosis is exact (s5): every non-joinable peak involves a rule that
  MANUFACTURES an `N`, and `N` is the one operator with no fixpoint law
  (0042 s3) -- expansion cannot chase what confine produces.  Knuth-
  Bendix says the repair is to orient the join as a new rule, `N-fold`:
  `p ^ a(N p) -> N(p)` for `p` confined to bit 0 -- which is N's own
  telescoping on the one domain where it has one (s6).

  CONSEQUENCE (s7).  Since every rule preserves meaning and `0` is
  irreducible, reaching `0` on ANY path is a proof.  Non-confluence
  means a true statement can also reduce to a stuck nonzero term --
  exhibited -- so no deterministic strategy is complete and the
  procedure MUST be a search.  In sentence form, `N` is where
  determinism dies; 0047 said the same thing about the machine ("`N`
  is the guard") from the other side.

Run directly for the verification suite.
"""

from __future__ import annotations

import itertools
import random

import expand_and_add as E
import sentence_canonical_form as S
from sentence_canonical_form import (OMEGA, ONE, X, Y, ZERO, atom, conj,
                                     equal, render, xor)

E.without_collect_and_telescope()

GUARDED = ("!", "U", "T", "N", "lowset", "lowzero")


# ---------------------------------------------------------------------
# 1. the inner loop terminates: a multiplicative reduction order
# ---------------------------------------------------------------------
#
# A counting measure fails here, for a reason worth keeping: `shift-out`
# on the `b` shift replaces one atom by the two-monomial polynomial
# `a(S t) ^ 1`, so every sibling atom in the monomial is DUPLICATED and
# any global count can grow.  A multiplicative interpretation absorbs
# duplication natively -- a monomial is the PRODUCT of its atom weights,
# so replacing an atom of weight w by a polynomial of weight W < w
# shrinks the monomial no matter what it is multiplied by.
#
#   W(polynomial)  =  sum of monomial weights     (0 for `0`)
#   M(monomial)    =  product of atom weights     (1 for `Ω`)
#   w(x) = w(1)    =  2
#   w(a(P))        =  A * (W(P) + 1)
#   w(S(P))        =  2 * K^(W(P) + 1)     S a series or measure
#   w(N(P))        =      K^(W(P) + 1)
#
# with A = 2 and K = 2048.  Every constructor is strictly monotone, so
# a strict drop anywhere is a strict drop everywhere (and accidental
# XOR cancellations only remove more weight).  Each rule reduces to one
# arithmetic lemma:
#
#   settle, unit   2K^(n+1) > B0        B0 = the biggest settle output
#   absorb         c*K^(2K^(n+1)+1) > 2K^(2n+1)   (exponent dominates)
#   shift-out      2K^(2n+3) > 2(2K^(n+1)+1) + 2  (b-case incl. the ^1)
#   confine        2K^(n+1) > K^(n+1)   and   2K^(n+1) > n
#   low-bit        2K^(n+1) > n + 1     (lowzero emits t ^ Ω)
#   low-bit/prefix M >= 4 > 2           (a masked monomial dies)
#   N-see-through  K^(2n+3) > K^(n+1)
#   N-absorb       a monomial loses a factor >= K
#   contain        a monomial loses a factor >= 2
#
# All are instances of "K^linear beats linear", checked exactly below
# over n = 0..600.  The weights themselves are towers for nested series
# (K^(K^...)) and cannot be evaluated on deep terms, so the exact
# per-application audit runs on every application whose weight is
# computable, and the lemma grid carries the rest.

A_WEIGHT = 2
K_WEIGHT = 2048
EXPONENT_CAP = 20000


class _TooBig(Exception):
    pass


def weight(poly) -> int:
    total = 0
    for atoms in poly:
        piece = 1
        for kind, *rest in atoms:
            if kind in S.LEAF:
                piece *= 2
                continue
            inner = weight(rest[0])
            if kind == "a":
                piece *= A_WEIGHT * (inner + 1)
            else:
                if inner + 1 > EXPONENT_CAP:
                    raise _TooBig
                piece *= (1 if kind == "N" else 2) *                     K_WEIGHT ** (inner + 1)
        total += piece
    return total


def verify_the_arithmetic_lemmas() -> None:
    K, A = K_WEIGHT, A_WEIGHT
    biggest_settle = weight(S.prefix_constant([1] * S.PREFIX_DEPTH)) + 1
    assert 2 * K > biggest_settle          # settle/unit at the smallest arg
    for n in range(601):
        # absorb: both sides are powers of K, so compare exponents --
        # the tower K^(2K^(n+1)+1) itself is not evaluatable
        assert 2 * K ** (n + 1) + 1 > 2 * n + 2
        assert 2 * K ** (A * (n + 1) + 1) > A * (2 * K ** (n + 1) + 1)
        assert 2 * K ** (A * (n + 1) + 3) > A * (2 * K ** (n + 1) + 1) + 2
        assert 2 * K ** (n + 1) > K ** (n + 1)
        assert 2 * K ** (n + 1) > n + 1
        assert K ** (A * (n + 1) + 1) > K ** (n + 1)
    print(f"  every per-rule inequality holds exactly for n = 0..600,")
    print(f"  A = {A}, K = {K}; the biggest settle/unit output weighs "
          f"{biggest_settle}")
    print(f"  < 2K = {2 * K}. Beyond the grid each is 'exponential beats")
    print(f"  linear', monotone in n.")


def verify_the_order_on_computable_terms(trials=4000,
                                         seed=20261006) -> None:
    generator = random.Random(seed)
    checked, skipped, failures = 0, 0, []
    per_rule = {}
    for index in range(trials):
        builder = S.random_poly if index % 2 else S.structured_poly
        poly = builder(generator, 2)
        try:
            before = weight(poly)
        except _TooBig:
            skipped += 1
            continue
        for rule, result in S.rewrites(poly):
            try:
                after = weight(result)
            except _TooBig:
                skipped += 1
                continue
            checked += 1
            per_rule[rule] = per_rule.get(rule, 0) + 1
            if not after < before:
                failures.append((rule, render(poly), render(result)))
    print(f"  {checked} rule applications with computable weight "
          f"({skipped} towers skipped):")
    for rule in sorted(per_rule, key=per_rule.get, reverse=True):
        print(f"    {rule:<15} {per_rule[rule]:>6} applications, "
              f"all strictly decreasing")
    for rule, before, after in failures[:4]:
        print(f"    VIOLATION {rule}: {before} -> {after}")
    assert not failures
    print()
    print("  The interpretation is strictly monotone in every position,")
    print("  so termination of the local rules follows from the per-rule")
    print("  lemmas alone; this audit checks the composition on every")
    print("  application small enough to evaluate.")


def verify_the_inner_loop_terminates() -> None:
    verify_the_arithmetic_lemmas()
    print()
    verify_the_order_on_computable_terms()
    print()
    print("  A counting measure provably CANNOT work: shift-out's b-case")
    print("  duplicates sibling atoms, and 0044/0048 never noticed only")
    print("  because their measures were checked on samples where the")
    print("  duplication happened not to bite. The multiplicative order")
    print("  settles it: the local rules terminate from every term.")


# ---------------------------------------------------------------------
# 1b. the inner loop is not confluent either -- and here it is decidable
# ---------------------------------------------------------------------

def verify_the_inner_loop_is_not_confluent(trials=3000,
                                           seed=20261006) -> None:
    """L terminates (s1), so its complete normal-form set is computable
    exactly, and 'two distinct normal forms' is a finite certificate.

    The smallest one found:

        1x | U(1x)   -->*   N(1x)
        1x | U(1x)   -->*   N(1x) ^ 1x ^ N(1x)·1x

    both irreducible, both the same set. The second SHOULD reduce: it is
    `1x | N(1x)` and `1x` vanishes wherever `N(1x)` does -- but 0048's
    port of `N-absorb` tests each atom of the sibling monomial against
    the guard's argument one at a time, and dropped 0044's `inside`
    clause, which caught the case where the sibling equals the argument
    as a WHOLE monomial. A correction to 0048: its `verify` harness
    silently skipped terms whose normal form was not unique
    (`if capped or len(forms) != 1: continue`), so this was never
    tested, and 0048 s5's `0 unsound identifications` was measured on
    the survivors only.
    """
    certificate = xor(xor(atom("U", conj(ONE, X)), conj(ONE, X)),
                      conj(atom("U", conj(ONE, X)), conj(ONE, X)))
    forms, capped = S.normal_forms(certificate, node_cap=4000)
    assert not capped and len(forms) == 2
    for form in forms:
        assert not S.rewrites(form)
    first, second = sorted(forms, key=S.size)
    assert equal(first, second)
    print(f"    {render(certificate)}")
    for form in (first, second):
        print(f"      -->*  {render(form)}      irreducible")
    print()
    generator = random.Random(seed)
    divergent, scanned = [], 0
    for index in range(trials):
        builder = S.random_poly if index % 2 else S.structured_poly
        poly = builder(generator, 2)
        forms, capped = S.normal_forms(poly, node_cap=2500)
        if capped:
            continue
        scanned += 1
        if len(forms) > 1:
            assert all(equal(f, g) for f, g in
                       itertools.combinations(forms, 2))
            divergent.append(poly)
    print(f"  {scanned} terms scanned exhaustively: {len(divergent)} have")
    print(f"  more than one normal form, every divergent pair verified")
    print(f"  semantically equal -- the rules are sound, and the inner")
    print(f"  loop is terminating but NOT confluent. By Newman's lemma a")
    print(f"  terminating system with a non-unique normal form fails")
    print(f"  local confluence; the certificate above is the failing peak.")


# ---------------------------------------------------------------------
# 2. expansion does not terminate: one infinite path
# ---------------------------------------------------------------------

def _orbit_term(steps: int):
    """X_k = x ^ a(x) ^ ... ^ a^{k-1}(x) ^ a^k(!(x))."""
    total, chain = ZERO, X
    for _ in range(steps):
        total = xor(total, chain)
        chain = S.shift_a(chain)
    tail = atom("!", X)
    for _ in range(steps):
        tail = S.shift_a(tail)
    return xor(total, tail)


def verify_the_infinite_path(steps=40) -> None:
    """The reduction graph of `!(x)` is one infinite path.

    At every step the term has NO local redex and EXACTLY ONE
    expansion, whose result is the next term of the closed form.  That
    is the strongest possible non-termination: there is no strategy to
    save, because there is never a choice.
    """
    current = _orbit_term(0)
    assert current == atom("!", X)
    sizes = []
    for k in range(steps):
        assert not S.rewrites(current), f"local redex at step {k}"
        moves = set(E.expansions(current))
        expected = _orbit_term(k + 1)
        assert moves == {expected}, f"branching at step {k}"
        sizes.append(S.size(current))
        current = expected
    assert all(p < q for p, q in zip(sizes, sizes[1:]))
    print(f"  X_k = x ^ a(x) ^ ... ^ a^(k-1)(x) ^ a^k(!(x))")
    print(f"  checked for k = 0..{steps}: X_k has no local redex, exactly")
    print(f"  one expansion, and it is X_(k+1); sizes strictly increase")
    print(f"  ({sizes[0]} -> {sizes[-1]}).")
    print()
    print("  The induction is one line: X_k's only operator atom is the")
    print("  `!` under a^k, its argument `x` fires no local rule, and its")
    print("  unique unfolding is X_(k+1).  So the path is infinite and")
    print("  expand-and-cancel does not terminate -- under ANY strategy,")
    print("  since no term on the path offers a choice.")


# ---------------------------------------------------------------------
# 3. it is not even weakly normalizing: U(x) has no normal form
# ---------------------------------------------------------------------

def a_depth(poly) -> int:
    best = 0
    for atoms in poly:
        for kind, *rest in atoms:
            if kind in S.LEAF:
                continue
            best = max(best, a_depth(rest[0]) + (1 if kind == "a" else 0))
    return best


def random_flat(generator, budget):
    """Series-free, N-free: the candidate normal-form shapes."""
    choice = generator.random()
    if budget == 0 or choice < 0.35:
        return generator.choice([X, X, ONE, OMEGA])
    if choice < 0.6:
        return S.shift_a(random_flat(generator, budget - 1))
    return (xor if generator.random() < 0.5 else conj)(
        random_flat(generator, budget - 1),
        random_flat(generator, budget - 1))


def verify_flat_terms_are_local(trials=250, width=11,
                                seed=20261006) -> None:
    """Bit i of a series-free N-free term depends only on input bits in
    the window [i - d, i], where d is the term's a-depth.

    By structural induction: `x` and constants have d = 0, `^` and `&`
    take the max, `a` adds one.  Checked exhaustively at width 11.
    """
    generator = random.Random(seed)
    machine_cache = {}
    checked = 0
    for _ in range(trials):
        poly = random_flat(generator, 3)
        depth = a_depth(poly)
        term = S.to_term(poly)
        machine = machine_cache.setdefault(term, S.oracle.Machine(term))
        for value in range(0, 1 << width, 7):
            env = {"x": value} if machine.variables else {}
            base = machine.run(env, (), width)
            for position in range(width):
                for flip in range(width):
                    if position - depth <= flip <= position:
                        continue
                    flipped = {"x": value ^ (1 << flip)} \
                        if machine.variables else {}
                    other = machine.run(flipped, (), width)
                    assert (base >> position) & 1 == \
                        (other >> position) & 1, (render(poly), value,
                                                  position, flip)
                    checked += 1
    print(f"  {trials} series-free terms, {checked} window checks at "
          f"width {width}: every bit is a function of its window alone.")


def verify_no_series_is_local() -> None:
    """Each series and measure fails d-locality for EVERY d: for each
    depth, a witness pair agreeing on the whole window [i-d, i] whose
    outputs differ at bit i."""
    width = 12
    print(f"    {'op':<9} witnesses for d = 0..8, at i = d+1")
    for kind in GUARDED:
        term = (kind, S.oracle.var("x"))
        machine = S.oracle.Machine(term)
        for depth in range(9):
            position = depth + 1
            if kind in ("!", "U", "N"):
                one_, two = 1, 0
            elif kind == "T":
                mask = (1 << (position + 1)) - 2       # bits 1..i
                one_, two = mask | 1, mask
            elif kind == "lowzero":
                mask = (1 << position) - 2             # bits 1..i-1
                one_, two = mask | 1, mask
            else:                                       # lowset
                one_, two = 1 << position, (1 << position) | 1
            values = []
            for value in (one_, two):
                guard = S.oracle.consistent_guard(machine, {"x": value},
                                                  width)
                values.append(machine.run({"x": value}, guard, width))
            window_agree = all((one_ >> f) & 1 == (two >> f) & 1
                               for f in range(max(0, position - depth),
                                              position + 1))
            bit_differs = ((values[0] >> position) & 1) !=                 ((values[1] >> position) & 1)
            assert window_agree and bit_differs, (kind, depth)
        print(f"    {kind:<9} not d-local for any d in 0..8")
    print()
    print("  So no series-free term computes any of them (s3's lemma says")
    print("  a series-free term IS d-local for d = its a-depth), and the")
    print("  same holds with N-atoms present: on the family x_r = 1<<r the")
    print("  guard flags are eventually constant (next check), so a")
    print("  flat-plus-guards term agrees with one local function on a")
    print("  tail of the family, and U separates x_p from x_q inside a")
    print("  shared window there. Every reduct of U(x) contains a series")
    print("  atom, every term containing one is reducible, so U(x) has NO")
    print("  normal form: expand-and-cancel is not weakly normalizing.")


def verify_guard_flags_settle(trials=200, width=14,
                              seed=20261006) -> None:
    """N(P(x_r)) is eventually constant along x_r = 1 << r."""
    generator = random.Random(seed)
    checked = 0
    for _ in range(trials):
        poly = random_flat(generator, 2)
        term = ("N", S.to_term(poly))
        machine = S.oracle.Machine(term)
        flags = []
        for r in range(width - 2):
            env = {"x": 1 << r} if machine.variables else {}
            guard = S.oracle.consistent_guard(machine, env, width)
            flags.append(1 if machine.run(env, guard, width) else 0)
        tail = flags[a_depth(poly) + 2:]
        assert len(set(tail)) <= 1, (render(poly), flags)
        checked += 1
    print(f"  {checked} guards N(P) over flat P: the flag on x_r = 1<<r")
    print(f"  is constant once r clears P's a-depth -- each monomial of a")
    print(f"  flat P is a constant mask times at most one shifted copy of")
    print(f"  x_r, so nonzero-ness stops depending on r.")


# ---------------------------------------------------------------------
# 4. non-confluence: the certificate
# ---------------------------------------------------------------------

def verify_not_confluent() -> None:
    """A finite certificate: one term, two distinct irreducible reducts.

        !(x&1) --confine--> N(x&1)
        !(x&1) --expand---> x&1 ^ a(!(x&1)) -->L*  x&1 ^ a(N(x&1))

    Both are normal forms (no local rule, no expansion -- N has no
    unfolding and nothing under it is reachable), both mean the same
    set, and they are different terms.  Expand-and-cancel is NOT
    confluent.
    """
    start = atom("!", conj(X, ONE))
    confined = [result for rule, result in S.rewrites(start)
                if rule == "confine"]
    assert len(confined) == 1
    left = confined[0]
    expanded = E.expansions(start)
    assert len(expanded) == 1
    forms, capped = S.normal_forms(expanded[0])
    assert not capped and len(forms) == 1
    right = next(iter(forms))
    for name, form in (("A", left), ("B", right)):
        assert not S.rewrites(form), name
        assert not E.expansions(form), name
    assert left != right
    assert equal(left, right)
    print(f"    start   {render(start)}")
    print(f"    A       {render(left)}        via confine")
    print(f"    B       {render(right)}   via expand, then reduce")
    print()
    print("  A and B are checked irreducible (no local rule, no expansion),")
    print("  distinct, and equal at every width. That is a finite")
    print("  counterexample to confluence.")
    print()
    print("  Why here: `confine` knows `!(p) = N(p)` on a one-bit `p`, but")
    print("  `N` has NO fixpoint law (0042 s3) -- it is the one operator")
    print("  the schema cannot unfold -- so once one copy of the redex has")
    print("  been confined and the other expanded, nothing can chase the")
    print("  `a(N(...))` tail back down. The failure of confluence is the")
    print("  failure of N to have an expansion, made local.")
    return left, right


# ---------------------------------------------------------------------
# 5. the peak census: every failure is an N
# ---------------------------------------------------------------------

N_MAKERS = {"confine", "absorb", "low-bit"}     # rules that can mint an N


def _joinable(first, second, budget=3, cap=140, extra=None):
    """Can the two reducts reach a common term by reduce/expand search?"""
    def local_forms(poly):
        forms, _ = S.normal_forms(poly, node_cap=2500)
        if extra is None:
            return forms
        grown = set(forms)
        for form in forms:
            for _, result in extra(form):
                more, _ = S.normal_forms(result, node_cap=2500)
                grown |= more
        return grown

    def closure(poly):
        seen = set(local_forms(poly))
        frontier = set(seen)
        for _ in range(budget):
            grown = set()
            for term in frontier:
                for nxt in E.expansions(term):
                    grown |= local_forms(nxt)
                if len(grown) > cap:
                    break
            frontier = grown - seen
            seen |= grown
        return seen
    left = closure(first)
    if second in left:
        return True
    return bool(left & closure(second))


def survey_the_peaks(trials=160, seed=20261006, repaired=False):
    generator = random.Random(seed)
    extra = (lambda p: n_fold(p) + annihilate(p)) if repaired else None
    joined, failed = 0, []
    for index in range(trials):
        builder = S.random_poly if index % 2 else S.structured_poly
        poly = builder(generator, 2)
        steps = [(rule, result) for rule, result in S.rewrites(poly)]
        if repaired:
            steps += n_fold(poly) + annihilate(poly)
        steps += [("expand", result) for result in E.expansions(poly)]
        for (rule_l, left), (rule_r, right) in \
                itertools.combinations(steps[:6], 2):
            if left == right:
                continue
            if _joinable(left, right, extra=extra):
                joined += 1
            else:
                failed.append((rule_l, rule_r, poly))
    label = "repaired (N-fold + annihilate added)" if repaired else \
        "as shipped by 0050"
    print(f"  {label}:")
    print(f"    {joined + len(failed)} peaks from {trials} terms: "
          f"{joined} joined, {len(failed)} not (bounded search)")
    if failed:
        minted = sum(1 for rule_l, rule_r, _ in failed
                     if rule_l in N_MAKERS or rule_r in N_MAKERS)
        kinds = sorted({(min(l, r), max(l, r)) for l, r, _ in failed})
        print(f"    {minted} of {len(failed)} failures involve an "
              f"N-minting rule; unjoined pairs: {kinds[:6]}")
    return failed


def survey_before_and_after(trials=120) -> None:
    before = survey_the_peaks(trials)
    print()
    after = survey_the_peaks(trials, repaired=True)
    print()
    print("  The two completion rules were not guessed -- each is a peak")
    print("  the census surfaced, oriented by the s1 order. Whatever")
    print("  remains unjoined is reported above; a bounded join search")
    print("  proves nothing about those, and the repaired system's")
    print("  confluence is a conjecture, not a theorem. The THEOREM is")
    print("  the negative one: the 0050 system is not confluent.")


# ---------------------------------------------------------------------
# 6. the Knuth-Bendix repair: N's one telescoping
# ---------------------------------------------------------------------

def n_fold(poly):
    """`C·p ^ C·a(N p) -> C·N(p)` for `p` confined to bit 0.

    The certificate's join, oriented as a rule -- and a real law: a
    one-bit `p` propagates upward through `N` exactly as a `^` series
    would, so N restricted to bit-0 arguments has the fixpoint
    `N(p) = p ^ a(N p)`. The schema could not give N an expansion
    (0042 s3); Knuth-Bendix hands it a CONTRACTION instead, on the one
    domain where it has one. The common factor `C` is needed for the
    same reason 0050 needed it for telescope: ANF distributes products,
    so the pattern is a pair of monomial families, not a pair of atoms.
    """
    steps = []
    for atoms in poly:
        for element in atoms:
            if element[0] != "a":
                continue
            target = S._sole_atom(element[1])
            if target is None or target[0] != "N":
                continue
            argument = target[1]
            if S.support_bound(argument) != 1:
                continue
            rest = frozenset([frozenset(atoms - {element})])
            partner = conj(rest, argument)
            if not partner or not partner <= poly:
                continue
            replacement = conj(rest, frozenset([frozenset([target])]))
            steps.append(("N-fold",
                          xor(xor(xor(poly, frozenset([atoms])), partner),
                              replacement)))
    return steps


def annihilate(poly):
    """A monomial confined to a window it is known to miss is `0`.

    Generalizes `low-bit`'s prefix case from mask-1 monomials to any
    monomial with a finite support bound -- e.g. `a(a(1))·a(1)`, the
    product of two disjoint constants, which the expansion of a measure
    on a constant manufactures and nothing else could remove.
    """
    steps = []
    for atoms in poly:
        monomial = frozenset([atoms])
        bound = S.support_bound(monomial)
        if bound is None:
            continue
        if bound == 0 or                 set(S.known_prefix(monomial, bound)) == {0}:
            steps.append(("annihilate", xor(poly, monomial)))
    return steps


def repaired_rewrites(poly):
    return list(S.rewrites(poly)) + n_fold(poly) + annihilate(poly)


def verify_the_repairs_are_sound(trials=250, seed=20261006) -> None:
    generator = random.Random(seed)
    checked = 0
    for index in range(trials):
        builder = S.random_poly if index % 2 else S.structured_poly
        poly = builder(generator, 2)
        for rule, result in n_fold(poly) + annihilate(poly):
            assert equal(poly, result), (rule, render(poly))
            checked += 1
    demo = xor(conj(S.shift_a(S.shift_a(ONE)), S.shift_a(ONE)), X)
    fired = {rule for rule, _ in annihilate(demo)}
    assert "annihilate" in fired
    print(f"  {checked} applications of N-fold and annihilate checked")
    print(f"  against the decision procedure: all meaning-preserving.")
    print(f"  Both also fit s1's reduction order: N-fold trades a")
    print(f"  monomial pair for one lighter monomial (2K^e + c > K^e),")
    print(f"  annihilate deletes a monomial outright.")


def verify_the_repair_heals_the_witness() -> None:
    left, right = atom("N", conj(X, ONE)), None
    start = atom("!", conj(X, ONE))
    expanded = E.expansions(start)[0]
    forms, _ = S.normal_forms(expanded)
    right = next(iter(forms))
    folded = n_fold(right)
    print(f"    B = {render(right)}")
    for rule, result in folded:
        print(f"    {rule}:  B -> {render(result)}")
        assert result == left
        assert equal(result, right)
    assert folded, "N-fold does not fire on the witness"
    print()
    print("  The oriented join fires and lands exactly on A: this critical")
    print("  pair closes. Completion is NOT run to a fixpoint here -- new")
    print("  overlaps of N-fold against the other rules are unchecked --")
    print("  so this is the first step of Knuth-Bendix, not a confluence")
    print("  proof. What it settles is the direction: N's missing law is")
    print("  a contraction, not an expansion.")


# ---------------------------------------------------------------------
# 7. what non-confluence means for the procedure
# ---------------------------------------------------------------------

def verify_truth_can_get_stuck() -> None:
    """A statement that IS true, with a reduct from which 0 is
    unreachable -- so no deterministic strategy decides truth, and the
    search in `decides` is forced, not a convenience."""
    statement = xor(atom("!", conj(X, ONE)), atom("N", conj(X, ONE)))
    assert equal(statement, ZERO)
    quick = [result for rule, result in S.rewrites(statement)
             if rule == "confine"]
    assert quick and quick[0] == ZERO
    stuck = E.expansions(statement)[0]
    forms, capped = S.normal_forms(stuck)
    assert not capped
    survivors = [f for f in forms if f != ZERO
                 and not S.rewrites(f) and not E.expansions(f)]
    print(f"    statement    {render(statement)}      (true: = 0)")
    print(f"    fast path    confine both -> 0 in one step")
    for form in survivors[:1]:
        print(f"    slow path    expand first -> ... -> {render(form)}")
        print(f"                 irreducible, nonzero, and TRUE")
    assert survivors
    print()
    print("  Reaching 0 is a proof (every rule preserves meaning; 0 is")
    print("  irreducible). But a true statement can also reduce to a")
    print("  stuck nonzero term, so 'reduce and read off the answer' is")
    print("  not a decision procedure -- 'search for 0' is. 0047 said N")
    print("  is the guard the machine must case-split on; this is the")
    print("  sentence form of the same fact: N is where determinism dies.")


def run_verification_suite() -> None:
    sections = [
        ("The inner loop terminates: a reduction order",
         verify_the_inner_loop_terminates),
        ("The inner loop is not confluent",
         verify_the_inner_loop_is_not_confluent),
        ("Expansion is one infinite path from !(x)",
         verify_the_infinite_path),
        ("Series-free terms are window-local", verify_flat_terms_are_local),
        ("No series is local; U(x) has no normal form",
         verify_no_series_is_local),
        ("Guard flags settle on the witness family",
         verify_guard_flags_settle),
        ("Non-confluence: the certificate", verify_not_confluent),
        ("The peak census, before and after repair",
         survey_before_and_after),
        ("The repairs are sound", verify_the_repairs_are_sound),
        ("The Knuth-Bendix repair heals the certificate",
         verify_the_repair_heals_the_witness),
        ("Truth can get stuck: search is mandatory",
         verify_truth_can_get_stuck),
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
