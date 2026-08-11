# 0041 — T re-expressed: it is not a new series, it is `U` in a mirror

Asked: re-express the corpus's `$`/`T` (the trailing-ones mask,
`x & b(x) & b(b(x)) & …` with `b(y) = 2y+1`) in elementary terms, and see
whether other primitives reconstruct it. **Two reconstructions**, and
they say different things. Code: `output/canonicalising_T.py`.

---

## 1. With addition: a finite term, and a circle

```
T(x) = x & neg(x + 1)
```

No series at all. Verified for every `x < 2¹¹`.

But it closes a circle with the successor, which the corpus defines the
other way round:

```
succ(x) = x ^ b(T x)                (corpus, verified here)
T(x)    = x & neg(succ x)           (this file)
```

So **`T` and `succ` are interdefinable, each a two-symbol term in the
other, and neither is prior.** The corpus derived succ from T; T comes
back from succ just as cheaply. That is worth knowing before treating
either as the primitive.

## 2. With the up-closure: no new operator at all

One identity bridges the two shifts:

```
neg(b(y)) = s(neg y)                b and a are complement-conjugate
```

verified. De Morgan then turns the intersection series into the union
series of 0039:

```
T(x) = neg( U(neg x) )              U(x) = x | s(x) | s(s(x)) | …
```

verified. **`$` and `U` are one operator seen through complement.** So
every law of one is a law of the other, and `T` gains its whole algebra
for free:

| | union side | intersection side |
|---|---|---|
| fixpoint | `U(x) = x \| s(U x)` | `T(x) = x & b(T x)` |
| telescoping | `U(x) ^ s(U x) = lowest **set** bit` | `T(x) ^ b(T x) = lowest **zero** bit` |

Both rows verified. The second is 0039's telescoping family gaining its
`T` member, and it is the piece canonicalisation most directly wants:
**`T ^ b(T)` is what the series measures, and it measures the lowest
zero** — the exact mirror of `U ^ s(U)` measuring the lowest set bit.

## 3. And no finite shift-term reaches it

Measured: bit `6` of `T(x)` depends on x's bits `0, 1, 2, 3, 4, 5, 6` —
every bit at or below it. A term of shift-depth `d` reaches only bits
`i−d … i`. So no finite term over `{^, &, <<}` matches `T`; it needs
`+` or a series.

That is 0002's locality argument arriving on the term side rather than
the operator side, and it says the two reconstructions above are the
only two shapes available: borrow `+`, or keep the series and recognise
it as `U`.

## 4. The canonicalisation payoff

0040 showed the tiles over `{x, s(x), …}` are the length-n windows of
x's bit string. The same holds for `T`'s own symbols:

```
n = 2, 3, 4:  tiles over {x, b(x), …} are the length-n windows of x,
              with ONES padding the bottom instead of zeros
```

verified. `b` fills with ones where `a` fills with zeros, and that is
the only difference.

So **`T` inherits 0040 unchanged**: its tiles are de Bruijn states, its
realisable set is the set of runs, and its canonical object is the same
sliding-window automaton with one padding convention flipped. There is
no separate canonicalisation problem for `T`.

## 5. What this settles, and what it opens

Settled: `T` is not an independent primitive on any reading. It is
`succ` under complement-and-mask, it is `U` under De Morgan, and its
canonical form is 0040's automaton. The corpus's operator list
`{^, &, a, b, T, !, $}` is therefore redundant in a specific way — `$`
and the union-series are the same thing, and `!` (the XOR-series) is the
third member of the same telescoping family.

Opens, in order of interest:

1. **Is the whole series family one operator with three joins?** `!`
   joins with `^`, `U` with `|`, `T` with `&`. Their telescopings are
   `x`, the lowest set bit, the lowest zero bit. That looks like one
   construction parameterised by the join, and if so the corpus's series
   zoo collapses to a single schema — which would be the cleanest
   possible canonicalisation result for this fragment.
2. **What does the `+` reconstruction cost?** `T(x) = x & neg(x+1)` is
   finite but circular with succ. Whether the circle can be broken — a
   term for one of them over `{^, &, <<, N}` with no series and no
   addition — is open, and 0038's `N` is the obvious candidate to try
   since it was not available when 0002 ran the locality argument.
3. **Does 0040's window reading survive a non-shift symbol?** `b` is
   still a shift, so §4 is not yet evidence that the reading is general.
   `{x, x+1}` and `{x, T(x)}` remain the experiments that would tell.
