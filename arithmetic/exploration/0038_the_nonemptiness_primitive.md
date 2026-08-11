# 0038 — The infinite closure has a closed form, and it is one new symbol

0037 left the sentence frame needing `K | s(K) | s²(K) | …` closed both
ways, at a depth proportional to the width — an unrolling that grows with
the problem. The premise there was that the family had to be expanded in
the original primitives. It does not. It has a closed form, exactly as
`1/2 + 1/4 + 1/8 + …` has one. Code:
`output/nonemptiness_primitive.py`.

---

## 1. The closed form

Read a statement as a set of positions and the two halves of the closure
are immediate:

```
up-closure    ⋃ₖ sᵏ(T)   =  every position at or above min(T)
down-closure  ⋃ₖ hᵏ(T)   =  every position at or below max(T)
```

For `T` non-empty, `min(T) ≤ max(T)`, so together they are **every
position**. Hence

```
C(T) = 0    if T is empty
C(T) = 1    otherwise                    (1 = the universe)
```

verified for every `T < 2¹⁰`. **The infinite union is the nonemptiness
indicator.** Give it the symbol `N`.

The two halves are worth keeping in view separately, because each is
itself a closed form worth having: the up-closure is "at or above the
lowest set position", the down-closure "at or below the highest". They
are the two one-sided cousins of `N`, and the corpus already has a
neighbour of the first — the trailing-ones mask `T(x)` of 0002.

## 2. It is the primitive the workstream already named

0015/0016 concluded, from the automaton side, that *"what the framing
lacked was never negation but the existential — nonemptiness"*. Here the
same object arrives from the sentence side, as the closed form of the
shift closure. Two independent derivations landing on one symbol is the
reason to think this is the right primitive rather than a patch.

**And it costs nothing semantically.** 0011 built "at least k" as a
clamped counter; nonemptiness is the `k = 1` case at **2 states**, so `N`
is already inside the layer. Adding the symbol adds no power — it is
notation for something the layer already decides — so convexity is
untouched and the ceiling of 0034 is nowhere near.

## 3. With `N`, the test is exact

`H` inside `N(K)` holds iff, wherever `K` is empty, `H` is empty. That is
entailment on the nose, not an approximation of it:

```
3438 random satisfiable K/H pairs:  0 unsound, 0 incomplete
```

`H ^ H·N(K)` collapses to the empty set **exactly** when `K` entails `H`,
in both directions. This also supplies a check 0037 never ran: it
measured a width-proportional depth without testing soundness at those
depths. Soundness holds, and now for a reason rather than by sampling —
the closure's limit is `N`, which is empty exactly where `K` is.

## 4. The rules

Expansion, cancellation, combination — all terminating:

```
N(0) -> 0            N(1) -> 1            N(N a) -> N a
N(a | b) -> N(a) | N(b)                   N(s a) -> N(a)      [s injective]
a & N(b) -> a        whenever N(a) and N(b) have the same normal form
```

The side condition on the last rule is decided, not guessed: put the term
in **s-graded ANF** — monomials carrying a shift degree — and divide out
the largest power of `s`. Equal normal forms mean `a` and `b` are empty
together, so wherever `a` is non-empty `N(b)` is the universe, and the
rule is sound.

On 0037's worked example the whole thing is two steps:

```
K            = 2 ^ x
H     = s(K) = 4 ^ s¹(x)
H ^ H·N(K)   = 4 ^ N(2^x)&4 ^ N(2^x)s¹(x) ^ s¹(x)      -- as written, no

N(s a) -> N(a):   N(H) ↦ N(2 ^ x)      N(K) ↦ N(2 ^ x)      equal
a & N(b) -> a:    H·N(K)  ->  4 ^ s¹(x)
a ^ a -> 0:       H ^ H   ->  0
```

Every intermediate term checked semantically for `x < 2¹⁰`.

**Termination.** Measure a term by its size *counting shift degree* —
which is what the division rule consumes. `N(s a) -> N(a)` strictly
decreases it (200 of 200 random shifted statements, never larger);
`a & N(b) -> a` deletes a subterm; `a ^ a -> 0` deletes two. So the
system terminates, with a bound readable off the term — the corpus's own
requirement, and the thing the unrolling of 0037 could not offer.

## 5. What this changes

0037's headline was that the sentence frame pays a width-proportional
unrolling and the automaton is the finite form of it. **That reading is
now wrong in one direction and right in the other.** It is wrong that the
sentence frame must unroll: `N` is the finite form, on the sentence side,
and it is one symbol with three rules. It remains right that the
automaton is *a* finite form — the two are now two closed forms of the
same series, not a finite one and an infinite one.

Which reopens a question 0037 thought it had settled. The frames are
peers again: `N` closes the series in the sentence algebra, the shift
quotient closes it in the automaton algebra, and 0019's measured
incomparability (sentence poly-simulates automaton, automaton sometimes
exponentially larger) applies to the pair as it stood before.

## 6. Open

1. **Is `{N, ^, &, s, h, constants}` complete for entailment?** §3 says
   yes on 3438 random pairs, and now for a structural reason. A proof
   would make the sentence frame a genuine decision procedure for the
   shift fragment — the first canonical-form result on the sentence side
   since 0019.
2. **Confluence.** Termination is measured; confluence of the three
   rules plus ANF reduction is not checked, and a canonical form needs
   both.
3. **`N` of the other non-pointwise operators.** `N(s a) = N(a)` holds
   because `s` is injective. `N(h a) ≠ N(a)` — `h` kills a lone low bit.
   The exact law for `h`, and whether `+` and `T` have analogous laws, is
   the natural next sweep.
4. **`N` and the measure.** `|.|` is empty exactly when its argument is,
   so `N(|a|) = N(a)` — the one law relating the two levels that lives
   entirely in the sentence algebra. Whether that gives the counted tier
   a sentence-side handle, where 0037 §6c said the closure trick does not
   transfer, is the sharpest question this file opens.
