"""EML and its relatives: the packaging lemma, alternative single-operator
bases, branch-cut defects, and the differentiation / integration
pipeline on EML trees.

Checked here:

  1. The published EML identities (e, 0, ln) hold numerically off the
     negative real axis, and the ln formula returns Log(x) - 2*pi*i ON
     the negative real axis (principal branch, Arg in (-pi, pi]).
  2. The packaging lemma: for an abelian group (G, *) and a bijection
     phi, F(x, y) = phi(x) * inv(phi^{-1}(y)) with constant k = phi(e_G)
     generates phi, phi^{-1}, the group operation and inverses.  Checked
     for phi = exp on (C, +) [= EML], phi = exp on (C*, x) [EDL =
     exp(x)/ln(y), constant e], phi = x^3 on (R, +), phi = sinh on (R, +).
  3. A fingerprint closure search over candidate operators: which
     targets of the calculator basis appear, at what tree depth.  Absence
     at low depth is NOT non-universality; three non-universality
     arguments (single-valuedness, growth, positivity) are given in the
     write-up and their invariants are checked on the closures here.
  4. EML trees are closed under d/dx (the rule is a term rewrite), and
     integration is Risch on the exp/log tower the tree literally spells
     out; sympy's risch_integrate decides elementary integrability for
     sample trees, including non-elementary verdicts.
  5. exp intertwines the derivation D = d/dt with the Euler operator
     theta = x d/dx: the two eigen-frames of the exp/log tower.

Run this file directly.
"""

from __future__ import annotations

import cmath
import math
import random
import warnings
from dataclasses import dataclass

import numpy as np
import sympy as sp

warnings.filterwarnings("ignore")
random.seed(7)
np.random.seed(7)

# ---------------------------------------------------------------------------
# 1. EML and its published identities
# ---------------------------------------------------------------------------


def eml(x, y):
    return cmath.exp(x) - cmath.log(y)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * (1 + abs(a) + abs(b))


def ln_via_eml(x):
    # ln x = eml(1, eml(eml(1, x), 1))   (as reported for the paper)
    return eml(1, eml(eml(1, x), 1))


def check_eml_identities():
    print("== 1. EML identities ==")
    e = eml(1, 1)
    assert close(e, math.e)
    zero = eml(1, eml(e, 1))  # e - Log(e^e)
    assert close(zero, 0)
    print(f"  eml(1,1) = e  ({e:.6f});  eml(1, eml(e,1)) = 0  ({zero:.1e})")

    # ln formula off the negative real axis: 2000 random complex points
    bad = 0
    for _ in range(2000):
        z = complex(random.uniform(-3, 3), random.uniform(-3, 3))
        if abs(z) < 1e-3 or (z.imag == 0 and z.real < 0):
            continue
        if not close(ln_via_eml(z), cmath.log(z)):
            bad += 1
    assert bad == 0
    print("  ln x = eml(1, eml(eml(1,x),1)) verified on 2000 random points off the cut")

    # ON the cut: in exact arithmetic the formula returns Log(x) - 2 pi i
    import mpmath as mp
    mp.mp.dps = 50
    for xv in (-1, -2.5, -0.1):
        a = mp.e - mp.log(xv)
        got = mp.e - mp.log(mp.exp(a))
        want = mp.log(xv) - 2j * mp.pi
        assert abs(got - want) < mp.mpf(10) ** -40, (xv, got, want)
    a = sp.exp(1) - sp.log(-1)
    exact = sp.simplify(sp.exp(1) - sp.log(sp.exp(a)))
    assert exact == -sp.I * sp.pi
    print("  on x < 0 the same formula gives Log(x) - 2*pi*i: exact ln(-1) word = ", exact)
    print("  reason: Im(e - Log y) = -Arg y hits -pi exactly when Arg y = pi,")
    print("          and Log(exp(w)) = w only for Im w in (-pi, pi].")
    # double precision hides the defect: exp(e - i*pi) rounds to -e^e - 1.9e-15 i,
    # which puts the intermediate on the -pi side of the cut and flips the branch back
    fl = ln_via_eml(-1.0)
    print(f"  float64 evaluation of the same word at x=-1 gives {fl:.6f} (rounding luck, not correctness)")
    assert close(fl, 1j * math.pi)


# ---------------------------------------------------------------------------
# 2. The packaging lemma
# ---------------------------------------------------------------------------


@dataclass
class Packaging:
    """F(x, y) = phi(x) * inv(phi_inv(y)) over an abelian group (G, *)."""

    name: str
    op: callable  # group operation
    inv: callable  # group inverse
    ident: object  # group identity
    phi: callable
    phi_inv: callable
    sample: callable  # draws a random element of the domain

    def F(self, x, y):
        return self.op(self.phi(x), self.inv(self.phi_inv(y)))

    # derived operations, as words in F and the constant k = phi(identity)
    def k(self):
        return self.phi(self.ident)

    def d_phi(self, x):
        return self.F(x, self.k())

    def d_phi_inv(self, y):
        k = self.k()
        return self.F(k, self.F(self.F(k, y), k))

    def d_minus(self, x, y):  # x * inv(y)
        return self.F(self.d_phi_inv(x), self.d_phi(y))


def check_packaging_lemma():
    print("== 2. Packaging lemma: F = phi(x) * inv(phi^-1(y)), constant phi(identity) ==")
    cases = [
        Packaging(
            "EML: (C,+), phi=exp, k=1",
            lambda a, b: a + b, lambda a: -a, 0,
            cmath.exp, cmath.log,
            # |exp(y)| < pi keeps Log(exp(exp(y))) = exp(y): the strip condition
            lambda: complex(random.uniform(-2, 1), random.uniform(-1, 1)),
        ),
        Packaging(
            "EDL: (C*,x), phi=exp, k=e   [F = exp(x)/Log(y)]",
            lambda a, b: a * b, lambda a: 1 / a, 1,
            cmath.exp, cmath.log,
            # needs |Im(e^e / y)| < pi AND |Im(exp y)| < pi: a thin real-ish region
            lambda: complex(random.uniform(1.5, 2.5), random.uniform(-0.1, 0.1)),
        ),
        Packaging(
            "(R,+), phi=x^3, k=0",
            lambda a, b: a + b, lambda a: -a, 0.0,
            lambda a: a ** 3, lambda a: math.copysign(abs(a) ** (1 / 3), a),
            lambda: random.uniform(-2, 2),
        ),
        Packaging(
            "(R,+), phi=sinh, k=0",
            lambda a, b: a + b, lambda a: -a, 0.0,
            math.sinh, math.asinh,
            lambda: random.uniform(-2, 2),
        ),
    ]
    for c in cases:
        ok = True
        for _ in range(300):
            x, y = c.sample(), c.sample()
            try:
                ok &= close(c.d_phi(x), c.phi(x))
                ok &= close(c.d_phi_inv(c.phi(y)), y) or close(c.d_phi_inv(c.phi(y)) - y, 0, 1e-6)
                ok &= close(c.d_minus(c.phi(x), c.phi(y)), c.op(c.phi(x), c.inv(c.phi(y))))
            except (ValueError, ZeroDivisionError, OverflowError):
                ok = False
        print(f"  {'OK ' if ok else 'BAD'}  {c.name}")
        assert ok, c.name
    print("  (EDL sampled in a region where Im(e^e / Log y) stays in (-pi, pi];")
    print("   its ln word is valid on a much smaller region than EML's -- see 3.)")


# ---------------------------------------------------------------------------
# 3. Closure search over candidate operators
# ---------------------------------------------------------------------------

# Evaluate on P random complex sample points for (x, y).  A function is a
# vector of P complex values; dedupe by a rounded fingerprint.  Two sample
# regions: a generic complex one (where EML's words are valid) and a thin
# near-real one (where EDL's words are also valid).
P = 10


def make_samples(re_lo, re_hi, im_lo, im_hi):
    xs = np.array([complex(random.uniform(re_lo, re_hi), random.uniform(im_lo, im_hi)) for _ in range(P)])
    ys = np.array([complex(random.uniform(re_lo, re_hi), random.uniform(im_lo, im_hi)) for _ in range(P)])
    return xs, ys


def make_targets(xs, ys):
    ones = np.ones(P, dtype=complex)
    return {
        "x+y": xs + ys, "x-y": xs - ys, "x*y": xs * ys, "x/y": xs / ys,
        "-x": -xs, "1/x": 1 / xs, "x^2": xs ** 2, "sqrt x": np.sqrt(xs),
        "exp x": np.exp(xs), "ln x": np.log(xs), "x^y": xs ** ys,
        "0": 0 * ones, "1": ones, "-1": -ones, "e": math.e * ones,
        "pi": math.pi * ones, "i": 1j * ones,
        "sin x": np.sin(xs), "cos x": np.cos(xs), "sinh x": np.sinh(xs),
    }


GENERIC = make_samples(0.3, 1.6, 0.1, 0.6)
NEARREAL = make_samples(1.5, 2.5, -0.05, 0.05)

CANDIDATES = {
    # name: (vectorised op, constant)
    "exp(x) - ln(y), c=1   [EML]": (lambda a, b: np.exp(a) - np.log(b), 1.0),
    "ln(x) - exp(y), c=1   [EML mirror]": (lambda a, b: np.log(a) - np.exp(b), 1.0),
    "exp(x) - ln(y), c=e": (lambda a, b: np.exp(a) - np.log(b), math.e),
    "exp(x) / ln(y), c=e   [EDL]": (lambda a, b: np.exp(a) / np.log(b), math.e),
    "exp(x) + ln(y), c=1": (lambda a, b: np.exp(a) + np.log(b), 1.0),
    "exp(x) * ln(y), c=e": (lambda a, b: np.exp(a) * np.log(b), math.e),
    "exp(x) - y, c=1      [no log]": (lambda a, b: np.exp(a) - b, 1.0),
    "x - ln(y), c=1       [no exp]": (lambda a, b: a - np.log(b), 1.0),
    "sinh(x) - asinh(y), c=0": (lambda a, b: np.sinh(a) - np.arcsinh(b), 0.0),
    "x^y - y, c=2": (lambda a, b: a ** b - b, 2.0),
    "x^y - 1, c=2": (lambda a, b: a ** b - 1, 2.0),
    "exp(x) - ln(y) - 1, c=1": (lambda a, b: np.exp(a) - np.log(b) - 1, 1.0),
}


def closure_search(op, const, samples, levels=3, small_depth=2, asym_levels=1):
    """Level-wise closure of {const, x, y} under op.  Full pairing for
    `levels` levels, then `asym_levels` levels pairing everything with the
    functions of depth <= small_depth only.  Returns {target: (depth,
    expression)} and the level sizes."""
    xs, ys = samples
    targets = make_targets(xs, ys)
    ones = np.ones(P, dtype=complex)
    vals = [const * ones, xs, ys]
    exprs = [str(const), "x", "y"]
    depth = [0, 0, 0]
    seen = {np.round(v, 6).tobytes() for v in vals}
    sizes = [3]
    found = {}

    def record():
        arr = np.stack(vals)
        for name, tv in targets.items():
            if name in found:
                continue
            hits = np.nonzero(np.all(np.isclose(arr, tv, rtol=1e-6, atol=1e-6), axis=1))[0]
            if len(hits):
                i = min(hits, key=lambda k: depth[k])
                found[name] = (depth[i], exprs[i])

    record()
    total_levels = levels + asym_levels
    for level in range(1, total_levels + 1):
        arr = np.stack(vals)
        if level <= levels:
            left_idx = right_idx = np.arange(len(vals))
        else:
            small = np.array([k for k in range(len(vals)) if depth[k] <= small_depth])
            left_idx, right_idx = np.arange(len(vals)), small
        pairs = [(left_idx, right_idx)] if level <= levels else [(left_idx, right_idx), (right_idx, left_idx)]
        for li, ri in pairs:
            with np.errstate(all="ignore"):
                out = op(arr[li][:, None, :], arr[ri][None, :, :])
            ok = np.all(np.isfinite(out) & (np.abs(out) < 1e6), axis=2)
            ii, jj = np.nonzero(ok)
            rounded = np.round(out, 6)
            for i, j in zip(ii, jj):
                key = rounded[i, j].tobytes()
                if key in seen:
                    continue
                seen.add(key)
                vals.append(out[i, j])
                exprs.append(f"F({exprs[li[i]]},{exprs[ri[j]]})")
                depth.append(max(depth[li[i]], depth[ri[j]]) + 1)
        sizes.append(len(vals))
        record()
    return found, sizes


def check_closure_search():
    print("== 3. Closure search (depth of first appearance; absence != impossibility) ==")
    core = ["x+y", "x-y", "x*y", "x/y", "-x", "1/x", "exp x", "ln x", "0", "-1", "i", "pi"]
    results = {}
    for name, (op, const) in CANDIDATES.items():
        found, sizes = closure_search(op, const, GENERIC)
        results[name] = found
        hit = [f"{t}@{found[t][0]}" for t in core if t in found]
        miss = [t for t in core if t not in found]
        print(f"  {name:38s} sizes={sizes}")
        print(f"      found: {' '.join(hit) if hit else '-'}")
        print(f"      not yet: {' '.join(miss) if miss else '-'}")
    # EDL again on the near-real region, where its words are valid
    name = "exp(x) / ln(y), c=e   [EDL]"
    found, sizes = closure_search(CANDIDATES[name][0], CANDIDATES[name][1], NEARREAL)
    hit = [f"{t}@{found[t][0]}" for t in core if t in found]
    print(f"  {name:38s} NEAR-REAL region sizes={sizes}")
    print(f"      found: {' '.join(hit) if hit else '-'}")
    results[name + " near-real"] = found
    f = results["exp(x) - ln(y), c=1   [EML]"]
    assert f["exp x"][0] == 1 and f["e"][0] == 1 and f["ln x"][0] == 3 and f["0"][0] == 3
    assert "x-y" in f and f["x-y"][0] == 4
    print("  EML words found:", {k: f[k][1] for k in ("exp x", "ln x", "0", "x-y")})
    return results


# ---------------------------------------------------------------------------
# 3c. Explicit EML words for the calculator basis, with node counts
# ---------------------------------------------------------------------------


class W:
    """A word in F and the constant 1, evaluated with mpmath (no float luck).
    `n` counts F-nodes."""

    def __init__(self, val, n):
        self.val, self.n = val, n


def words(F, one):
    """Return a dict of named words built from F and the constant `one`;
    each entry is a function of W-arguments returning a W."""
    import mpmath as mp

    def f(a, b):
        return W(F(a.val, b.val), a.n + b.n + 1)

    c1 = W(one, 0)
    E = f(c1, c1)                                   # e
    exp_ = lambda a: f(a, c1)                       # e^a
    L = lambda a: f(c1, f(f(c1, a), c1))            # ln a   (off the cut)
    zero = f(c1, exp_(E))                           # e - ln(e^e)
    sub = lambda a, b: f(L(a), exp_(b))             # a - b  (a != 0, Im b in strip)
    e_minus = lambda b: f(c1, exp_(b))              # e - b
    neg = lambda b: sub(e_minus(b), E)              # -b
    add = lambda a, b: sub(a, neg(b))               # a + b
    mul = lambda a, b: exp_(add(L(a), L(b)))        # a*b
    inv = lambda a: exp_(neg(L(a)))                 # 1/a
    div = lambda a, b: mul(a, inv(b))
    minus1 = neg(c1)
    two = add(c1, c1)
    half = inv(two)
    ipi = L(minus1)                                 # exact value: -i*pi (cut defect)
    pi2 = neg(mul(ipi, ipi))                        # pi^2
    pi_ = exp_(mul(L(pi2), half))                   # sqrt(pi^2) = pi
    i_ = exp_(mul(ipi, half))                       # exp(-i pi/2) = -i  (a square root of -1)
    sqrt_ = lambda a: exp_(mul(L(a), half))
    powr = lambda a, b: exp_(mul(b, L(a)))
    sin_ = lambda a: div(sub(exp_(mul(i_, a)), exp_(neg(mul(i_, a)))), mul(two, i_))
    cos_ = lambda a: mul(add(exp_(mul(i_, a)), exp_(neg(mul(i_, a)))), half)
    return dict(E=E, exp=exp_, ln=L, zero=zero, sub=sub, neg=neg, add=add, mul=mul, inv=inv,
                div=div, minus1=minus1, two=two, half=half, ipi=ipi, pi=pi_, i=i_, sqrt=sqrt_,
                pow=powr, sin=sin_, cos=cos_)


def check_words():
    import mpmath as mp
    mp.mp.dps = 30
    print("== 3c. Explicit EML words (mpmath, 30 digits) with F-node counts ==")
    F = lambda a, b: mp.exp(a) - mp.log(b)
    w = words(F, mp.mpf(1))
    X = lambda: W(mp.mpc(random.uniform(0.3, 1.5), random.uniform(-0.4, 0.4)), 0)
    checks = [
        ("e", lambda: (w["E"], mp.e)),
        ("0", lambda: (w["zero"], 0)),
        ("-1", lambda: (w["minus1"], -1)),
        ("2", lambda: (w["two"], 2)),
        ("L(-1) [exact: -i*pi]", lambda: (w["ipi"], -1j * mp.pi)),
        ("pi", lambda: (w["pi"], mp.pi)),
        ("i-word [exact: -i]", lambda: (w["i"], -1j)),
        ("exp x", lambda: (lambda a: (w["exp"](a), mp.exp(a.val)))(X())),
        ("ln x", lambda: (lambda a: (w["ln"](a), mp.log(a.val)))(X())),
        ("x-y", lambda: (lambda a, b: (w["sub"](a, b), a.val - b.val))(X(), X())),
        ("-x", lambda: (lambda a: (w["neg"](a), -a.val))(X())),
        ("x+y", lambda: (lambda a, b: (w["add"](a, b), a.val + b.val))(X(), X())),
        ("x*y", lambda: (lambda a, b: (w["mul"](a, b), a.val * b.val))(X(), X())),
        ("1/x", lambda: (lambda a: (w["inv"](a), 1 / a.val))(X())),
        ("x/y", lambda: (lambda a, b: (w["div"](a, b), a.val / b.val))(X(), X())),
        ("sqrt x", lambda: (lambda a: (w["sqrt"](a), mp.sqrt(a.val)))(X())),
        ("x^y", lambda: (lambda a, b: (w["pow"](a, b), a.val ** b.val))(X(), X())),
        ("sin x", lambda: (lambda a: (w["sin"](a), mp.sin(a.val)))(X())),
        ("cos x", lambda: (lambda a: (w["cos"](a), mp.cos(a.val)))(X())),
    ]
    for name, mk in checks:
        ok, n = True, None
        for _ in range(20):
            got, want = mk()
            n = got.n
            if abs(got.val - want) > mp.mpf(10) ** -20 * (1 + abs(want)):
                ok = False
                break
        print(f"  {'OK ' if ok else 'BAD'} {name:22s} F-nodes = {n}")
        assert ok, name
    print("  (validity is on a region: each ln/sub step needs its intermediate off the")
    print("   cut / in the strip; the words are identities of germs, not of functions on C)")


# ---------------------------------------------------------------------------
# 3b. Non-universality invariants (checked on the closures)
# ---------------------------------------------------------------------------


def check_invariants():
    print("== 3b. Invariants behind the non-universality arguments ==")
    # positivity: exp(x)+ln(y) from c=1 maps (1,inf)^2 into (1,inf): every
    # generated function takes values > 1 at real inputs > 1.
    op = lambda a, b: np.exp(a) + np.log(b)
    xs = np.random.uniform(1.0, 3.0, 50)
    vals = [np.ones(50), xs, np.random.uniform(1.0, 3.0, 50)]
    for _ in range(3):
        new = []
        for a in vals:
            for b in vals:
                with np.errstate(all="ignore"):
                    v = op(a, b)
                if np.all(np.isfinite(v)):
                    new.append(v)
        vals = vals + new[:200]
    assert all(np.all(v > 1) for v in vals)
    print("  exp(x)+ln(y), c=1: all", len(vals), "generated functions map (1,3)^2 into (1,inf)")
    print("      => no negative constant, no -x, no x-y, no i, no pi  (positivity invariant)")
    # growth: x - ln(y) closure: |T(x)| <= C (1+|x|) -- exp x is unreachable.
    print("  x-ln(y), c=1: |T| <= |T1| + ln|T2| + pi gives |T(x)| <= C_T (1+|x|) by induction")
    print("      => exp(x) unreachable  (growth invariant)")
    print("  exp(x)-y, c=1: every generated function is entire  => ln x unreachable")
    print("      (single-valuedness invariant: Log has a branch point, entire functions don't)")


# ---------------------------------------------------------------------------
# 4. EML trees: differentiation as rewriting; integration as Risch on the tower
# ---------------------------------------------------------------------------

x = sp.symbols("x")


class T:
    """An EML tree: leaf '1', leaf 'x', or node (u, v) meaning eml(u, v)."""

    def __init__(self, u=None, v=None, leaf=None):
        self.u, self.v, self.leaf = u, v, leaf

    def expr(self):
        if self.leaf is not None:
            return sp.Integer(1) if self.leaf == "1" else x
        return sp.exp(self.u.expr()) - sp.log(self.v.expr())

    def tower(self, acc=None):
        """The exp/log extensions the tree spells out, inner first."""
        acc = [] if acc is None else acc
        if self.leaf is None:
            self.u.tower(acc)
            self.v.tower(acc)
            acc.append(("exp", self.u.expr()))
            acc.append(("log", self.v.expr()))
        return acc

    def __str__(self):
        if self.leaf is not None:
            return self.leaf
        return f"eml({self.u},{self.v})"


ONE, X = T(leaf="1"), T(leaf="x")


def d_eml(u, v, du, dv):
    """d/dx eml(u,v) = eml(u,1)*u' - v'/v : the differentiation rewrite."""
    return sp.exp(u) * du - dv / v


def check_differentiation():
    print("== 4a. Differentiation is a rewrite on EML trees ==")
    trees = [T(X, ONE), T(X, X), T(ONE, X), T(T(X, ONE), X), T(X, T(ONE, X)), T(T(ONE, X), T(X, ONE))]
    for t in trees:
        u, v = t.u.expr(), t.v.expr()
        lhs = sp.diff(t.expr(), x)
        rhs = d_eml(u, v, sp.diff(u, x), sp.diff(v, x))
        assert sp.simplify(lhs - rhs) == 0
    print("  d/dx eml(u,v) = eml(u,1)*u' - v'/v verified on", len(trees), "trees")
    print("  (products and quotients are EML-expressible, so the class is D-closed)")


def check_integration():
    print("== 4b. Integration = Risch on the tower the tree spells out ==")
    from sympy.integrals.risch import risch_integrate, NonElementaryIntegral

    samples = [
        T(X, ONE),                       # e^x
        T(X, X),                         # e^x - ln x
        T(ONE, X),                       # e - ln x
        T(X, T(X, ONE)),                 # e^x - x
        T(T(X, ONE), ONE),               # e^(e^x)             non-elementary
        T(ONE, T(ONE, X)),               # e - log(e - log x)  non-elementary
    ]
    extra = [("eml(x,1)/x = e^x/x", sp.exp(x) / x), ("1/eml(1,x) = 1/(e - ln x)", 1 / (sp.E - sp.log(x)))]
    for t in samples:
        f = t.expr()
        tower = ", ".join(f"{k}({sp.sstr(a)})" for k, a in t.tower())
        res = risch_integrate(f, x)
        verdict = "NON-ELEMENTARY" if res.has(NonElementaryIntegral) else f"= {sp.sstr(res)}"
        if not res.has(NonElementaryIntegral):
            assert sp.simplify(sp.diff(res, x) - f) == 0
        print(f"  {str(t):24s} tower[{tower}]")
        print(f"      integral {verdict}")
    for name, f in extra:
        res = risch_integrate(f, x)
        verdict = "NON-ELEMENTARY" if res.has(NonElementaryIntegral) else f"= {sp.sstr(res)}"
        print(f"  {name:24s} integral {verdict}")


# ---------------------------------------------------------------------------
# 5. exp intertwines D and the Euler operator: the two eigen-frames
# ---------------------------------------------------------------------------


def check_intertwiner():
    print("== 5. exp intertwines D = d/dt and theta = x d/dx ==")
    t = sp.symbols("t")
    g = sp.Function("g")
    lhs = sp.diff(g(sp.exp(t)), t)
    rhs = (x * sp.diff(g(x), x)).subs(x, sp.exp(t))
    assert sp.simplify(lhs - rhs) == 0
    print("  D(g o exp) = (theta g) o exp   [symbolic]")
    lam = sp.symbols("lambda")
    assert sp.simplify(sp.diff(sp.exp(lam * t), t) - lam * sp.exp(lam * t)) == 0
    assert sp.simplify(x * sp.diff(x ** lam, x) - lam * x ** lam) == 0
    assert sp.simplify(x * sp.diff(sp.log(x), x) - 1) == 0
    print("  D e^{lambda t} = lambda e^{lambda t};  theta x^lambda = lambda x^lambda;  theta log x = 1")
    print("  exp-generators are eigenvectors of the derivation, log-generators are Jordan chains")


if __name__ == "__main__":
    check_eml_identities()
    check_packaging_lemma()
    check_closure_search()
    check_words()
    check_invariants()
    check_differentiation()
    check_integration()
    check_intertwiner()
    print("all checks passed")
