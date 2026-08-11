# 0044 — Rebuilt on an ANF base: five rules vanish, one appears, and the sampling was wrong

0043 §6.1 asked for the rebuild: drop `|` as a primitive, let terms *be*
ANF polynomials over `^` and `&`, and see how many of its fourteen rules
were bookkeeping for a convention. Code:
`output/series_confluence_anf.py`.

The prediction was right about the bookkeeping and wrong about
everything else.

---

## 1. What was asked: five rules were the convention

Terms are now polynomials — a set of monomials XOR-joined, a monomial a
set of idempotent atoms with a constant mask — and `|` is built as
`a ^ b ^ ab` at construction time. The two constructors `xor` and `conj`
are total functions into normal form, so:

| 0043 rule | why it is gone |
|---|---|
| `fold` (two constants) | `conj`/`xor` fold masks as they build |
| `unit` (`a ^ 0`, `a & Ω`) | never representable |
| `annihilator` (`a & 0`) | never representable |
| `idem-op` (`a ^ a`, `a & a`) | symmetric difference / set union of atoms |
| `commute` | monomials and atoms are *sets* |
| `split-constant` | existed to expose a constant to `fold` through `\|` |

**Six of fourteen, discharged.** 0043 §3's guess — that its two
surviving divergent terms were a `|`-as-primitive artifact — held: both
are identities in ANF, and neither reappears.

## 2. What was not asked: the sampling in 0043 was blind

Port the rules, run 0043's own check — 3000 random terms at depth 3,
whole rewrite graph explored per term — and the rule census reads:

```
fold 1730   low-bit 305   low-arg 240   absorb 136   shift-out 75
N-shift 27  |  N-lowbit 0   collect 0   telescope 0
```

`collect`, `telescope` and `N-lowbit` are **the schema's three
structural rules** — combination, cancellation, and the one composite
0038 had to find by hand. Random terms essentially never build their
redexes. 0043's confluence verdict was measured on a sample that never
exercised the rules the whole construction is about.

So the engine now carries `interesting_subterms`: for every series,
`S(x)`, `σ_S(S x)`, `S(σ_S x)`, `S(S x)`, `S(x)&1`, `S(x&1)`, `S(1)`,
`N(S x)`, `S(N x)`, plus `N(N(x)&1)` and the `N`-shift pair — the
redexes each rule exists for — and `random_structured_poly` joins them.
Against that pool the same rules fire 623, 46 and 1 times.

**Six of the eight completion rounds below are visible only to the
targeted pool.** The two columns are printed side by side in §6 of the
run for exactly this reason.

## 3. Round zero: a rule was unsound

Before confluence, correctness. The first search returned a term whose
two normal forms **differed in meaning**:

```
N(T(D(x)))  ->  N(x)        and  ->  N(x) & 1
```

`N(x)` is 0 or Ω; `N(x)&1` is 0 or 1. My port had folded 0043's
`N-lowbit` (`N(N t & 1) → N(t)`) into the `low-arg` rule as
`N(t & 1) → t & 1`, which is false — `N` of a bit is the *whole
universe*, not the bit. It survived a 250-term soundness check because
no random term at that size built the redex.

Restored as its own rule, and the soundness check raised to 3000 terms
over all 128 inputs, plus 600 structured terms over a 26-point spread.

## 4. The eight rounds

| # | witness | what it forced |
|---|---|---|
| 1 | `!h(Ω) ^ !h(x) ^ …` | `fold` outranks `collect` on a constant argument |
| 2 | `D(h x) & 1` | `low-bit` vs `shift-out` — see §5 |
| 3 | `!(a x) ^ !(x)` | `collect` vs `telescope` |
| 4 | `U(N x) \| U(x)` | `collect` vs `absorb` |
| 5 | `N(x&1) & x & 1` | **`N-absorb`**, new |
| 6 | `N(x&1) & 1` | `low-bit` extends to `N` on a low-bit argument |
| 7 | `!(x)N(!(x))N(T x)x&1` | `N(! t) = N(t)` — 0042's table stopped at `{N,T,U,D}` |
| 8 | `N(T x)T(T x) ^ U(1) ^ …` | `telescope` last, not first — see §5 |

Rounds 1, 3 and 4 collapse into **one** side condition, which is the
main structural result of the rebuild:

```
collect fires only between series atoms that are irreducible alone
```

`collect` buries its arguments inside a new series where nothing else
can reach them, so every rule that could act on `S(arg)` by itself —
`fold` on a constant, `absorb` on a nested series, `shift-out` then
`telescope` on a shifted sibling — must go first. That is 0043's round 1
restated in general form: *combination must not destroy the redex that
cancellation needs*. 0043 found the instance and fixed the orientation;
here the same fact appears three more times and gets one rule.

## 5. Two orderings the base algebra forces

**`telescope` is a last resort.** It is the only rule whose redex the
base algebra creates and destroys behind its back: any rewrite can turn
one monomial into a copy of another, and XOR then annihilates both,
taking `S(t)` or `σ_S(S t)` with it. Round 3 looked like it wanted
telescope *first* —

```
!(x) ^ !(x)N(b x) ^ N(b x) ^ U(N x) ^ a(!(x))
```

where `N(b x) → Ω` collapses `!(x)N(b x)` onto `!(x)` and cancels the
`!(x)` telescope needed. But first is wrong for the mirror reason
(round 8): telescope can take a monomial a pending `fold` was about to
annihilate. **Last** is the orientation that works — let cancellation
finish, then cancel what survived.

**`shift-out` cannot be blocked, so `low-bit` must reach through it.**
`D(h t) & 1` goes to `N(h t) & 1` by `low-bit` or to `h(D t) & 1` by
`shift-out`, and nothing reaches inside `h`. Gating `shift-out` on the
mask fails, because a later `fold` can narrow a mask to bit 0 after
`shift-out` has already run. The rule that joins them is
`h(D t) & 1 → N(h t) & 1`, and it trades a named series for `N` at the
cost of a bigger argument — so the termination measure had to be
reordered to

```
(series count, non-N series, argument size, size)
```

lexicographic. `collect` cuts the first, the `D→N` rules the second,
`shift-out` the third, `fold` the fourth. Verified strictly decreasing
on every application over both term pools.

## 6. `N-absorb` — the one genuinely new rule

```
N(p) & m  ->  m       whenever m vanishes wherever p does
```

Every operator in the language is zero-preserving except `b`, so a
monomial vanishes with `p` as soon as one of its atoms is built from
`p`; and 0042 §4's `N(T t) = N(t & 1)` supplies the one case the
recursion cannot see (`T(x)` vanishes with `x & 1`, not with `x`).

This is not bookkeeping. It is the statement that **`N` is a guard, not
a factor** — `N(p)` is the whole universe wherever anything derived from
`p` is non-zero, so it is redundant exactly there. 0043 never needed it
because, with `|` primitive, `N(p) & m` and `m` sat in different
monomial shapes and the sample never put them side by side.

## 7. Where it lands

```
soundness   2615 applications over 128 inputs  +  6410 over 26   all sound
termination strictly decreasing on every application, both pools
redexes     all 22 canonical redexes fire their rule, one normal form each
divergence  2996 random terms      -> no term has two normal forms
            1137 structured terms  -> no term has two normal forms
```

**Ten rules, where 0043 had fourteen, and zero divergence where 0043 had
two.** Six of 0043's are gone into the constructors; `N-absorb` is new;
`collect`'s three side conditions became one; and two rules acquired an
ordering.

```
fold        S(c), σ(c), m(c)          -> the value
absorb      S1(S2 t)                  -> 0042 §4, plus N∘! and N∘!h
shift-out   S(σ_S t)                  -> σ_S(S t)
low-bit     S(t) & 1                  -> t&1 [U,T,!] | N(t)&1 [D]
                                      -> t [N, t low-bit] | 0 [a] | 1 [b]
            h(D t) & 1                -> N(h t) & 1
low-arg     S(t & 1)                  -> t&1 [D,T] | N(t&1) [U]
N-absorb    N(p) & m                  -> m,  m vanishing with p
N-lowbit    N(N(t) & 1)               -> N(t)
N-shift     N(a t) -> N(t),  N(b t)   -> Ω
collect     S(a) ∘_S S(b)             -> S(a ∘_S b), both irreducible
telescope   S(t) ^ σ_S(S t)           -> m_S(t), last resort
```

One small thing fell out: telescoping a `^` series now returns its
argument rather than a `self(...)` atom, since 0042 §2 says the measure
of a `^` series *is* the argument. The old form was an atom no rule
could open.

## 8. Honest limits

- Still exhaustive graph search per term, not a critical-pair proof.
  Stronger than 0043 — two independent pools, one of them built from
  the redexes — but not a theorem.
- 63 of 1200 structured terms hit the 4000-node cap and are unexamined.
  Reported, not hidden.
- Still single-variable. 0043 §6.3's concern is untouched, and
  `collect` in particular has more redexes with two symbols.
- Confluence now depends on two *strategy* conditions (`collectable`,
  `LAST_RESORT`), not only on rule orientation. That is ordinary
  priority rewriting and the normal form is still unique, but it is a
  weaker object than an unordered confluent system.

## 9. The rule set, in canonical form and priority order

No `|` anywhere: joins are `^` and juxtaposition, `0` is the empty set
(true), `Ω` the universe, `1` the bit-0 constant. `t`, `p`, `m` are
polynomials; `c` a constant. Per 0042 §1, each series `S` carries a join
`∘_S`, a shift `σ_S` and a measure `m_S`:

| S | `∘_S` | `σ_S` | `m_S(t)` |
|---|---|---|---|
| `!` | `^` | `a` | `t` |
| `!ʰ` | `^` | `h` | `t` |
| `U` | `\|` | `a` | lowest set bit |
| `D` | `\|` | `h` | highest set bit |
| `T` | `&` | `b` | lowest zero bit |

The priority is three tiers, and each tier's condition is just
*exhaustion of the tier above*.

---

### Tier 0 — the constructors, not rules

`xor` and `conj` are total functions into normal form, so associativity,
commutativity, idempotence, units, annihilators and constant folding
never appear as rewrites. This tier is where six of 0043's fourteen
went.

### Tier 1 — the local rules (unordered among themselves)

```
fold        S(c) -> S c        σ(c) -> σ c        m(c) -> m c

absorb      N(N t) -> N t      N(U t) -> N t      N(D t) -> N t
            N(! t) -> N t      N(!ʰ t) -> N t     N(T t) -> N(t1)
            U(U t) -> U t      U(N t) -> N t      U(D t) -> N t
                                                  U(T t) -> N(t1)
            D(D t) -> D t      D(N t) -> N t      D(U t) -> N t
                                                  D(T t) -> T t
            T(T t) -> T t      T(N t) -> N t      T(D t) -> D t
                                                  T(U t) -> N(t1)

shift-out   S(σ_S t) -> σ_S(S t)

low-bit     U(t)1 -> t1        T(t)1 -> t1        !(t)1 -> t1
            D(t)1 -> N(t)1     h(D t)1 -> N(h t)1
            N(t)1 -> t1                              [t ⊆ 1]
            a(t)1 -> 0         b(t)1 -> 1

low-arg     D(t1) -> t1        T(t1) -> t1        U(t1) -> N(t1)

N-absorb    N(p) m -> m                              [m vanishes with p]

N-lowbit    N(N(t)1) -> N(t)

N-shift     N(a t) -> N(t)     N(b t) -> Ω
```

`m vanishes with p` is decided syntactically: every operator is
zero-preserving except `b`, so a monomial vanishes with `p` as soon as
one of its atoms is built from `p` — plus the one case recursion cannot
see, `T(t)` vanishing with `t1` (0042 §4's `N(T t) = N(t1)`).

### Tier 2 — combination, once tier 1 is exhausted on the arguments

```
collect     S(a) ∘_S S(b) -> S(a ∘_S b)      [S(a), S(b) both in normal form]
```

Written out, with `∘_S` expanded — this is what dropping the `|`
primitive costs and buys:

```
!           !(a) ^ !(b)                  ->  !(a ^ b)
!ʰ          !ʰ(a) ^ !ʰ(b)                ->  !ʰ(a ^ b)
U           U(a) ^ U(b) ^ U(a)U(b)       ->  U(a ^ b ^ ab)
D           D(a) ^ D(b) ^ D(a)D(b)       ->  D(a ^ b ^ ab)
T           T(a)T(b)                     ->  T(ab)
```

The `|` cells need a **three-monomial** match, which is exactly why
random terms almost never present one.

### Tier 3 — cancellation, once tiers 1 and 2 are exhausted everywhere

```
telescope   S(t) ^ σ_S(S t) -> m_S(t)
```

```
!           !(t)  ^ a(!(t))    ->  t
!ʰ          !ʰ(t) ^ h(!ʰ(t))   ->  t
U           U(t)  ^ a(U(t))    ->  lowset(t)
D           D(t)  ^ h(D(t))    ->  highset(t)
T           T(t)  ^ b(T(t))    ->  lowzero(t)
```

Note what canonical form exposes: **telescoping is an `^` pattern for
every series, whatever its own join.** Cancellation does not happen in
the series' join — it happens in the base. That is the structural reason
this rule alone has to be ordered against the base algebra rather than
against the other rules.

### The measure

Strictly decreasing on every rule above, lexicographic:

```
(series count, non-N series count, total series-argument size, size)
```

`collect` cuts the first, the `D → N` low-bit rules the second,
`shift-out` the third, `fold` the fourth.

## 10. Open

1. **Is `N-absorb` derivable?** It arrived as a completion round, but
   §6 reads like a law of the schema rather than a repair. If it is
   `N`'s analogue of the distribution law, it belongs in 0042 §2's
   table, and the `vanishes_with` test belongs with it.
2. **Can `telescope`'s ordering be removed?** It exists because XOR
   cancellation is invisible to the rule set. A representation that
   made cancellation a rewrite — or a measure that survived it — would
   restore unordered confluence.
3. **Two symbols**, still. Now with a targeted pool to generate from,
   which is the part that was missing when 0043 asked.
