# 0060 — The core is the tax, and every maximal paradox is the odometer

0059's two structural opens, both closed. The floor statement extends
to lossy revision maps with no change to the formula, and the odometer
is proved maximal in a strong sense: an expensive paradox *cannot be
built without the carry* (exponential separation), and every maximal
paradox is the odometer up to frame-compatible relabeling. Code:
`output/lossy_revision_and_the_carry.py`.

---

## 1. The lemma extends: forced entropy = log₂(shortest core cycle)

A body with `&` makes the revision map T lossy — a functional graph:
transient trees hanging off a **core** of disjoint cycles (the
eventual image, on which T is a bijection). Verified by exact
rational elimination on random `^/&/a` bodies (width 5; 9 of 12
lossy): the stationary space dimension equals the number of core
cycles, and every cycle-uniform is stationary. So stationary
distributions are exactly mixtures of core-cycle uniforms — transients
carry no stationary mass — and the tax formula is unchanged:

```
forced entropy  =  log₂(shortest cycle of the core)
```

## 2. The trichotomy is core geometry; absorption is the cheapener

Deterministic solutions are exactly the 1-cycles, so the trichotomy
reads directly off the functional graph:

| tier | core geometry |
|---|---|
| grounded (guarded) | a single fixed point — **total absorption** |
| truth-teller | several cycles, at least one fixed point |
| liar | no 1-cycle; tax ≥ 1 bit |

Groundedness = total absorption is 0054's 2-adic contraction seen as
a graph: guarded exemplars verified to have one-point cores. And
0059's open question — can absorption make a paradox cheaper than its
cycle structure suggests? — resolves cleanly: **the core's cycle
structure *is* the tax; absorption is how a paradox gets a small
core.** The absorbed liar `n := Ω ^ (n & 1)` has a 2-atom core and
2^w − 2 transients at every width — tax 1 bit, *and* revision settles
in one step. An invertible map can never do this (every atom sits in
a cycle).

Census (400 random bodies, width 6): 224 one-point cores, 103 with
fixed points among other cycles, 73 liars. The floor law held in
every cell. Liar shortest-cycle histogram {2: 64, 4: 5, 8: 4} — most
random paradoxes are 1-bit, but taxes of 2 and 3 bits occur in the
wild; 39 of 73 liars had cores ≤ 1/4 of the state space.

## 3. Carry-free paradoxes are exponentially cheap

A carry-free revision body is GF(2)-affine causal: `v ↦ Lv ^ b`.
Causal + invertible forces unit diagonal, so L = I + N with N
strictly lower triangular (nilpotent): L^(2^r) = I for
r = ⌈log₂ w⌉, and the affine map's order divides 2^(r+1). Hence

```
carry-free tax  ≤  ⌈log₂ w⌉ + 1  bits        (proved; verified
carry tax reaches   w            bits          exhaustively w = 4, 5)
```

Exhaustive sweep (every causal invertible matrix × every offset):
max cycle 8 at both w = 4 (= the bound) and w = 5 (bound 16 — the
bound is proved, not tight). Full period 2^w: never. **The
separation is exponential (log w vs w): an expensive paradox cannot
be built from XOR alone.** The carry — the channel that walls off
multiplication in 0053/0054 — is *necessary* for an expensive
paradox, not merely sufficient.

## 4. Hull–Dobell in the frame

Which carry bodies `n := a·n + b` are maximal? Exhaustive at
w = 4, 5, 6: full period exactly when **b is odd and a ≡ 1 (mod 4)**
— the classical Hull–Dobell family (full-period linear congruential
generators). The maximal paradoxes with carry form a familiar
classical family; §5 shows they are all the *same* paradox.

## 5. Every maximal paradox is the odometer

**Theorem** (proved in the source, verified exhaustively). Every
full-period *causal* map — bit i of output depending only on bits
≤ i of input, which every frame body is — is conjugate to
`n ↦ n + 1` by a causal bijection with causal inverse.

Proof shape: causality means T induces a truncation T_j at every
level j, and the projected orbit of 0 *is* the T_j-orbit; a
full-period orbit visits all residues mod 2^j and returns to 0 at
2^w, forcing T_j full-period at every level. Then orbit indexing
φ(T^k(0)) = k satisfies "v ≡ v′ mod 2^j ⟺ φ(v) ≡ φ(v′) mod 2^j",
which is causality of φ and φ⁻¹ at once, and φ∘T∘φ⁻¹ = +1 by
construction.

Verified: all 32/128 full-period affine maps at w = 4/5, and all 142
full-period maps among 4000 random causal bijections at w = 5
(hit rate ≈ 2⁻ʷ as expected) — every one causally conjugate to the
odometer.

So the answer to 0059 §8.4 is yes, in a stronger form than
conjectured: **up to causal change of variable there is exactly one
maximal single-channel paradox, and it is the carry's own clock.**
The two ends of the paradox spectrum are now both canonical: the liar
(period 2, one bit, the cheapest) and the odometer (full period,
everything, the only maximal one).

## Honest limits

- The lossy lemma's elimination check is at width 5 (12 instances)
  plus structural verification (floor = log₂ min core cycle) across
  the full 400-body census at width 6; the lemma itself is standard
  for deterministic pushforwards, and the code is the audit.
- The carry-free ceiling is proved for GF(2)-*affine* causal maps.
  Nonlinear carry-free bodies (with `&`) are covered by §1–2 only as
  sampled census data, not by the unipotent bound; a lossy `&` body's
  core cycles are permutations of a subset, and whether a *core* can
  host a long XOR-only cycle that the affine bound forbids globally
  is untested (the census's max observed liar cycle was 8 at w = 6).
- "Every frame body is causal" assumes bodies built from `^, &, a,
  constants` and carry-sum; the co-guarded `h` (down-shift) breaks
  causality and is outside this theorem.
- Random-causal-bijection verification is sampling (4000 draws), but
  the theorem covering them is proved; the sampling checks the proof's
  implementation, not the claim's universality.

## Open

1. **Long cycles inside lossy cores.** Can an `&`-body's core carry a
   cycle longer than the affine ceiling without simulating a carry?
   If not, "carry-free tax ≤ log w + 1" extends beyond affine and the
   carry-necessity theorem becomes unconditional for the frame.
2. **The h-channel.** Co-guarded references break causality; the
   odometer-uniqueness theorem does not apply. Whether `h` enables a
   *different* maximal paradox (or none — h's boundary-at-infinity
   may forbid full period) is open.
3. **The instrument program (next).** With the tax now fully
   structural — log₂ of the shortest core cycle, carry-graded — the
   information-theoretic tie to the mixture weight (0059 §6) is the
   remaining thread: the paradox as a measurement instrument for its
   own invisible coordinate.
