# 0053 — The product rewrite system: what coalesces, and four walls

The coalescing system for 0052's products, built to be pushed until it
breaks. It broke in four places, each isolated below; it also caught
two of its own rules unsound during construction, and both catches are
themselves findings. Code: `output/product_rewrite_system.py`.

---

## 1. Design: what construction absorbs

Following 0050/0051 — coalescing only, no expansion — and 0048's
lesson that the constructor is the strongest rule:

- **`+` is sugar**: `x + y = x ^ y ^ a(C(x, y))`. The carry `C` is the
  *only* new symbol addition needs, and `C(t,1) = T(t)` makes `succ`
  free.
- **Negation is sugar**: `-P = P ^ a(U(P))` — see §3; this
  two-monomial form was *found by the system*, not designed in.
- **`mul` atoms hold a multiset of factors**, flattened and sorted at
  construction: associativity and commutativity absorbed, the ANF move
  one level up.
- **`cmul` (⊗) is bilinear over `^`**, the representation's own join,
  so the constructor expands it monomial-by-monomial: distribution
  over `^` costs nothing. That is what "native join" buys.
- **`dil` (⊞) stays opaque** — it distributes over `|`, which the
  representation does not have. Deliberate: the asymmetry with `cmul`
  is the measurement.

Rules: 30 names, all coalescing. 0 unsound in the final audit (two
were caught and fixed on the way — §5). Soundness is checked at widths
22 and 30 on the low bits, which is exact because every operator is
LSB-causal.

## 2. The carry's laws

The user supplied mid-exploration the carry's recurrence in ANF form:

```
C(x,y)  =  xy ^ x·a(C) ^ y·a(C)
```

— bit *i* of `C` is the **majority of column *i−1*** of `{x, y, C}`,
the full-adder carry-out, which ties the carry to 0052 §6: `C` is the
fixpoint of the majority step. Verified exactly, alongside the
`g | (p & aC)` form. Unlike that form, this one lives in the
representation's **own join**, so it yields rules directly:

```
k-fold   m·PQ ^ m·P·a(C(P,Q)) ^ m·Q·a(C(P,Q))  ->  m·C(P,Q)
k-low    C(P,Q) & 1  ->  PQ & 1
k-neg    C(P, -P)  ->  U(P)          (verified: the carry of a number
                                      and its negation is the up-closure)
k-one    C(P, 1)   ->  T(P)
k-shift  C(aP, aQ) ->  a(C(P,Q))
```

plus `u-compdual`: `T(P ^ Ω) → U(P) ^ Ω` (the trailing ones of a
complement are the complement of the up-closure — verified), which the
additive inverse needs.

## 3. The system found the two-monomial negation

The first peak census reported 11 unjoined `k-neg` vs `u-compdual`
peaks: `k-neg` matched the four-monomial pattern
`(P^Ω) ^ 1 ^ a(T(P^Ω))`, and `u-compdual` rewriting the `T` inside
destroyed the redex. Chasing the join: `u-compdual` plus the
constructor identity `a(Ω) = Ω ^ 1` collapse the four monomials to

```
-P  =  P ^ a(U(P))
```

(verified exactly). Making *that* the canonical sugar closes the
critical pair — the joined form of the peak becomes the definition —
and the census dropped to **0 unjoined peaks of 103**. This is
Knuth–Bendix acting on a *constructor*, and the payoff is a genuinely
better identity: negation is "flip everything above the lowest set
bit", one shift and one `U`.

## 4. What reduces to 0 — and the walls

Seventeen laws, each verified true and each reduced to `0` by the
system: commutativity and associativity (construction), units, zero,
`x·Ω = −x`, shift-homomorphism, **`x + (−x) = 0`** (k-neg + u-compdual),
`succ`, carry-shift, the C-fixpoint itself (k-fold), `C&1` (k-low),
`N(xy) = N(x)N(y)`, both Ω-columns (`x⊗Ω = !(x)`, `x⊞Ω = U(x)`),
cmul-distribution over `^` (construction), and — after orienting it as
a fold —

```
p-dist-fold    m·xy ^ m·xz ^ m·a(C(xy, xz))  ->  m·x(y+z)
```

**distribution over `+`.** The wall 0049 hit with containment repeated
here in miniature: written left-to-right distribution looks like
expansion; read right-to-left it loses atoms and is coalescing. Every
"missing law" so far has fallen to the same move — orient the join of
the peak as a contraction (N-fold, k-fold, k-neg, p-dist-fold).

**Constant multiplication coalesces completely**: for c = 2..13,
`mul(x, c)` reaches a mul-free normal form — *unique* in every case —
in the `{^, a, C, T}` addition tier, e.g.

```
3x  -->*  x ^ a(x) ^ a(C(a(x), x))
```

The four walls that remain:

**W1 — the Frobenius.** `x ⊗ x` has zero rewrites. It is the
position-doubling map (squaring in GF(2)[[t]]), nothing in the
signature names it, and it is the kernel of `x² = (x⊗x) + carries`.
A system that wants squares needs it *named* — 0046's two-signature
split again: expressible only as a stuck product.

**W2 — the native join.** `dil-dist over |` and `cmul-assoc` do not
reduce. The first is structural: `|` is not the representation's join,
so the pattern cannot even be stated economically (`x⊞(y|z)` holds its
argument opaquely). The second is a design artifact with a known fix
(multiset `cmul` atoms, as for `mul` — complicated by bilinearity
living at the monomial level) — noted, not built.

**W3 — termination is audited, not proved, and the audit says why.**
57 of 1168 applications violate the layered measure (Ω-factor count,
Dershowitz–Manna on mul loads, atom count, argument load, size). The
violations classify exactly: *sibling duplication* (p-const/p-omega
duplicate neighbouring atoms through `add`/`neg` — 0051 §1's
phenomenon, which only the multiplicative interpretation handles, not
redone here); *Ω-circularity* (`u-one` turns `U(1)` into a fresh `Ω`
factor, re-arming `p-omega` — the tiers cannot be ordered around it);
and *p-dist-fold's growth* (the fold builds one bigger mul from two
smaller ones — informally each fold consumes a shareable factor pair,
but the measure does not see it). No divergence observed: 495 of 500
normal-form searches exhaust completely.

**W4 — lasso constants.** `p-const` must exclude `Ω`-carrying
constants: peeling `−1` regresses forever (`−x = x + 2(−x) + …`),
caught live as a census blow-up. Consequence: multiplication by
*integer* constants coalesces; multiplication by a general **lasso
(rational) constant has no rule at all** — `x · (1/3)` is stuck. The
constant tier 0052 showed closed under the products is only
half-served by the rewrite system.

## 5. Two unsound rules caught during construction

Both catches are findings about the representation:

1. **`p-const`, first version**: guarded peeling by "the `1`-monomial
   is present". But bit 0 is a **parity, not a membership** — `Ω` has
   bit 0 too, and `Ω ^ 1` (= −2) has bit 0 = 1^1 = 0. The audit's
   first run produced `mul{Ω^1, y}` peeled as if odd. ANF cancellation
   is invisible to membership tests; every bit-level guard must XOR
   over the monomials that touch the bit.
2. **`p-const`, second version**: allowing `Ω`-chains as constants
   made peeling non-terminating (W4). Soundness per step, divergence
   in the limit — the rule was "sound and wrong".

And one non-rule bug of the same family: `a(Ω) = Ω ^ 1` at
construction means the pair `{Ω, 1}` *is* a shifted `Ω`, and
shift-peeling that missed it stranded every `Ω^1` factor.

## 6. State of the audits

```
soundness    405 applications, 0 unsound (widths 22/30)
law table    17 of 19 true statements reduce to 0
peaks        0 unjoined of 79 in the final run (bounded, sampled)
searches     495/500 exhaust; 5 hit the node cap
termination  audited, 57/1168 violations, all classified (W3)
```

The fold rules never fire on random terms — k-fold, p-dist-fold and
k-low needed seeded redexes, 0044's sampling lesson for the third
time.

## 7. Honest limits

- Soundness is finite-width low-bits agreement at two widths, not
  proof; the LSB-causality argument makes it exact for every operator
  except `N`, which small inputs keep honest but do not certify.
- Termination is **not established** (W3) — audited with classified
  violations and no observed divergence. The multiplicative
  interpretation of 0051 extended with product atoms is the known
  route and was not carried out.
- The peak census is sampled and bounded; 0 unjoined is evidence, not
  confluence. The inherited non-confluence of the base system (0051)
  is still present in principle.
- The unary layer here is minimal (no settle/prefix analysis); several
  base-tier joins rely on it and were patched case-by-case (`u-one`,
  `u-omega`).
- Erosion (`⊖`) was left out of the rule set entirely — its
  anti-distribution and non-commutativity deserve their own pass.

## 8. Open

1. **Name the Frobenius.** `F(x) = x⊗x` (position doubling) plus the
   carry layers gives squaring; with p-dist-fold that is most of a
   coalescing route to general `x·y` products of sums.
2. **Multiset `cmul`** at the monomial level, absorbing ⊗-associativity
   the way mul multisets absorbed ·-associativity.
3. **Lasso multiplication**: `x·(−1/3)`-style rules. The 2-adic
   reading (0052 §9) says these are exactly "multiply by a rational",
   and the periodicity of the lasso should quotient the peeling
   regress into a finite cycle — a `p-lasso` rule that recognizes the
   cycle instead of unrolling it.
4. **The variable peeling guard.** `p-const` needs a known bit 0;
   variables need `N(y&1)` as that guard — which is 0047's guard
   mechanism arriving in the product tier. A guarded `p-var-const`
   rule would give the system long division's first step.
5. **Termination via the extended multiplicative interpretation**, and
   then a real confluence attempt on the terminating core.
