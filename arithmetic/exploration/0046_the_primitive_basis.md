# 0046 — Eight primitives, and every operator on a bitstring

Objection to 0045: constants have no business being primitive. `b^k(0)`
is `2^k - 1`, and the binary expansion of any `n` is its `a`/`b` word
over `0`. Correct, and it goes further than constants. Code:
`output/the_primitive_basis.py`.

---

## 1. Three eliminations

**Constants.** Read `n` in binary, MSB first, `a` for a 0 bit and `b`
for a 1 bit, starting from `0`. Verified for every value at width 8:

```
0    00000000   0
1    00000001   b(0)
2    00000010   a(b(0))
3    00000011   b(b(0))
44   00101100   a(a(b(b(a(b(0))))))
255  11111111   b(b(b(b(b(b(b(b(0))))))))
```

and `b^k(0) = 2^k - 1`: `0 → 1 → 3 → 7 → 15`.

**And `b` itself.** `b(t) = a(t) ^ 1` for every `t`, and `0 = 1 ^ 1`.
So `{1, a, ^}` is strictly smaller than `{0, a, b}`: it derives `b`, it
derives `0`, and every constant is a `^`-sum of `a^k(1)`.

**Ω.** `N(b(0))`. The universe falls out of the one operator that
manufactures it — and unlike `b^W(0)`, **it does not need to know the
width**. That is a better reason to keep `N` than the one 0045 gave.

**The measures.** Neither `lowset` nor `lowzero` is a primitive
operation. Each is its own telescoping,

```
!(t) ^ a(!t)  = t                  U(t) ^ a(U t) = lowset(t)
                                   T(t) ^ b(T t) = lowzero(t)
```

and, since complement is available once Ω is (`¬t = t ^ N(b 0)`), they
are each other:

```
lowset(t) = lowzero(t ^ Ω)
```

which is 0041's "`T` is `U` dualised" arriving a third time.

## 2. But the two signatures are different lists

The elimination of the measures is real as *algebra* and false as
*syntax*. Telescope's entire job is to package `S(t) ^ σ_S(S t)` into an
atom no rule can reopen — that is what drops the series count and makes
the measure fall. Expand `lowset` back to `U(t) ^ a(U t)` and telescope
becomes the **identity rewrite**; the cancellation rule stops cancelling
and termination is lost.

So:

```
algebra signature   1  a  ^  &  !  U  T  N                    8 operations
rewrite signature   the same, plus b, lowset, lowzero        11 symbols
```

The three extras are not power. They are **normal forms**: names the
rules produce and must not reopen. Worth stating plainly because it is
the first place in this workstream where "what you need to compute" and
"what you need to canonicalise" come apart.

## 3. Every operator, on a bitstring

```
x = 00101100        y = 00011010        z = 00010111
```

### Elementary

| | | |
|---|---|---|
| `a(x)` | `01011000` | `x << 1`, fills a 0 |
| `b(x)` | `01011001` | `x << 1`, fills a 1 — `= a(x) ^ 1` |
| `x ^ y` | `00110110` | symmetric difference |
| `x & y` | `00001000` | intersection |
| `x \| y` | `00111110` | `= x ^ y ^ xy`, derived |

### Compound — expansion shown beside each

```
!(00101100) = 11100100          expanded:  x ^ a(x) ^ a²(x) ^ …
     00101100   (x)
   ^ 01011000
   ^ 10110000
   ^ 01100000
   ^ 11000000
   ^ 10000000
   = 11100100                   running parity of x from the low end
```

```
U(00101100) = 11111100          expanded:  x | a(x) | a²(x) | …
     00101100   (x)
   | 01011000
   | 10110000
   | 01100000
   | 11000000
   | 10000000
   = 11111100                   everything at or above the lowest 1
```

```
T(00010111) = 00000111          expanded:  z & b(z) & b²(z) & …
     00010111   (z)
   & 00101111
   & 01011111
   & 10111111
   & 01111111
   = 00000111                   the run of trailing ones
```

```
N(00101100) = 11111111          expanded:  NOTHING
N(00000000) = 00000000
```

**`N` is the only operator with no expansion**, and that is 0045 §4
restated where it can be seen: every `a`/`b` operator is LSB-causal, so
no series over `a` or `b` can build an operator whose bit 0 depends on
every bit of the input. `N` is the language's one downward channel, and
it is primitive because it has to be.

### Measures — each is a telescoping

```
on x = 00101100
   !(x) ^ a(!x)  = 00101100     = x
   U(x) ^ a(U x) = 00000100     lowest set bit
on z = 00010111
   T(z) ^ b(T z) = 00001000     lowest zero bit
```

## 4. The rewrite system, in the reduced signature

Unchanged in structure from 0044 §9 as narrowed by 0045 §5 — 32 rule
instances, ten rule names, confluent, terminating under 0043's ordering.
What changes is only what a *constant* is: a maximal `a`-chain over `1`,
folded by evaluation.

Notation: `∘_S` and `σ_S` are the series' join and shift; `m_S` its
measure. `1`, `Ω = N(b 0)`, `b(t) = a(t) ^ 1`.

| S | `∘_S` | `σ_S` | `m_S(t)` |
|---|---|---|---|
| `!` | `^` | `a` | `t` |
| `U` | `∪` | `a` | `lowset(t)` |
| `T` | `&` | `b` | `lowzero(t)` |

**Tier 0 — the constructors, not rules.** `xor` and `conj` are total
into ANF, so associativity, commutativity, idempotence, units,
annihilators and constant folding never appear as rewrites.

**Tier 1 — local rules, unordered among themselves.**

```
fold        S(c) -> S c        σ(c) -> σ c        m(c) -> m c
                               [c a maximal a-chain over 1]

absorb      N(N t) -> N t      N(U t) -> N t      N(! t) -> N t
                                                  N(T t) -> N(t1)
            U(U t) -> U t      U(N t) -> N t      U(T t) -> N(t1)
            T(T t) -> T t      T(N t) -> N t      T(U t) -> N(t1)

shift-out   S(σ_S t) -> σ_S(S t)

low-bit     U(t)1 -> t1        T(t)1 -> t1        !(t)1 -> t1
            N(t)1 -> t1                              [t ⊆ 1]
            a(t)1 -> 0         b(t)1 -> 1

low-arg     T(t1) -> t1        U(t1) -> N(t1)

N-absorb    N(p) m -> m                              [m vanishes with p]

N-lowbit    N(N(t)1) -> N(t)

N-shift     N(a t) -> N(t)     N(b t) -> Ω
```

**Tier 2 — combination, once tier 1 is exhausted on the arguments.**

```
collect     S(a) ∘_S S(b) -> S(a ∘_S b)     [S(a), S(b) both in normal form]

            !(a) ^ !(b)                  ->  !(a ^ b)
            U(a) ^ U(b) ^ U(a)U(b)       ->  U(a ^ b ^ ab)
            T(a)T(b)                     ->  T(ab)
```

**Tier 3 — cancellation, once tiers 1 and 2 are exhausted everywhere.**

```
telescope   S(t) ^ σ_S(S t) -> m_S(t)

            !(t) ^ a(!(t))   ->  t
            U(t) ^ a(U(t))   ->  lowset(t)
            T(t) ^ b(T(t))   ->  lowzero(t)
```

Telescoping is an `^` pattern for every series whatever its own join —
cancellation happens in the base, not in the series' join, which is why
this rule alone is ordered against the base algebra rather than against
the other rules.

**Termination.** `(series count, argument size, non-N series, size)`,
lexicographic — 0043's ordering, restored by 0045 §6.

## 5. Honest limits

- §1's constant elimination is verified at width 8 over every value,
  and the `b(t) = a(t) ^ 1` and `0 = 1 ^ 1` identities over every `t`.
  The a/b-chain claim is standard binary-tree numbering; nothing here
  is delicate.
- §2 is an argument, not a measurement: "expand `lowset` and telescope
  is the identity" is true by definition, and the consequence for
  termination is immediate, but the engine has not been run in that
  degenerate configuration.
- §4 restates a rule set whose confluence was measured (0044 §8, 0045
  §7), not proved.

## 6. Open

1. **Is `{1, a, ^, &, !, U, T, N}` minimal?** `!` is the `(^, a)` cell
   and `U` the `(∪, a)` cell of one schema, so they are not independent
   *constructions* — but neither is derivable from the other in the
   term language, and that is what minimality asks. 0013/0014's
   Post-style completeness question applies directly.
2. **Does `N`'s primitiveness have a normal-form price?** 0045 §8.1
   asked what plays telescoping's role for `N`. §3 sharpens it: `N` has
   no expansion at all, so it has no telescoping *to* find — the
   question is whether something else cancels it.
3. **The two-signature split (§2)** is new and probably general. Any
   rule whose job is to seal a pattern needs a symbol the algebra does
   not, and it would be worth knowing whether the corpus's other
   canonical forms carry the same kind of extra.
