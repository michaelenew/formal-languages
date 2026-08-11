# 0045 — The right shift is `&` in disguise, and it comes out

Objection to 0044 §9: `h` has no business being a primitive. `&` was the
only operator that could erase information; a second information
destroyer would be a real addition to the language, and Post's lattice
says a two-valued logic has one information-losing direction, not two.

The objection is correct on every count. Code:
`output/removing_the_right_shift.py`.

---

## 1. `h` is not a second squasher

```
a(h(v))  =  (Ω ^ 1) v          for every v
```

verified on the whole range. So `h` is masking by a constant, followed
by the injective `a`-inverse. But the identity on its own is only
suggestive — an operator's information loss *is* the partition it
induces on inputs, so the statement that settles it is the one about
kernels:

```
ker h  =  ker (& (Ω ^ 1))      2048 classes, identical
```

`h` identifies two values **iff** `& (Ω^1)` does. It destroys the low
bit and nothing else, and it destroys it by masking. Post's ordering
direction is still the only place information leaves the language.

## 2. The general procedure

`a` is an algebra homomorphism — it commutes with `^` and `&` and scales
constants — so it pushes to the leaves, and at an `h` it cancels. For a
base-algebra term `E` of `h`-depth `d`:

```
a^d(E)  is h-free,  and  a^d(E) = E << d   exactly
```

which is stronger than the zero-equivalence asked for: not "empty at the
same points" but an exact scaling, from which `E = 0 ⟺ a^d(E) = 0` is
immediate. The rewrite is one line per constructor:

```
a^d(x)      = a^d(x)                  a^d(c)     = c << d
a^d(a t)    = a(a^d t)                a^d(b t)   = a(a^d t) ^ 2^d
a^d(h t)    = a^(d-1)((Ω^1) t)        a^d(u ∘ v) = a^d u ∘ a^d v
```

The `h` line is §1's identity spending one shift to cancel one `h`, so
the recursion terminates on `h`-depth. Verified on 1849 random terms
carrying an `h`, depth up to 3, over 256 inputs. Worked example:

```
h(x & 12) ^ a(x)      ->      ((x & 12) & (Ω^1)) ^ a(a(x))
```

## 3. What the series column costs: exactly the two cells that were
never in the corpus

0042 §1's table, with the column that leaves:

| join \ shift | a | b | **h — dropped** |
|---|---|---|---|
| `^` | `!` | divergent | **`!ʰ`** |
| `\|` | `U` | Ω | **`D`** |
| `&` | 0 | `T` | 0 |

The `h` column *is* `{!ʰ, D}` — and 0042 §6.3 had already recorded that
those two "fall out of the schema but do not appear in the corpus's
operator list". Removing `h` deletes the two cells the corpus never
had, and what remains is

```
{!, U, T}  +  N
```

**the corpus's own series, exactly.** Nothing that was ever used is
lost.

## 4. `N` is the one operator that flows downward

Measured, by flipping a bit above position *i* and asking whether output
bit *i* moves:

| operator | LSB-causal |
|---|---|
| `a`, `b`, `!`, `U`, `T` | yes |
| `N` | **no** |
| `h` | **no** |

Every `h`-free operator is LSB-causal: information moves up, never down.
So nothing over `{x, ^, &, a, b, !, U, T, constants}` can compute `N`,
whose bit 0 is the OR of every bit of `x`.

That is not an obstacle — **`N` is already primitive** (0038's rules,
and 0042 §3's finding that `N` is not a cell of the schema). It is the
sharper statement of what the `h` column was for: the language needs
*one* downward channel, and `N` is it. `h` was a second one, and a
redundant one.

**The honest cost:** 0042 §3's `N = U | D` stops being a sentence of the
language, because `D` is gone. `N` keeps its behaviour and all its
rules; it loses its derivation. The explanation of why `N` has no
telescoping — that it is two `|` cells joined, so no single extremum
survives — remains true of the semantics but is no longer a computation
inside the syntax.

## 5. The rewrite system, `h` removed

0044's suite re-run with `SHIFTS = {a, b}` and `SERIES = {!, U, T}`:

```
soundness   1361 applications over 128 inputs           all sound
termination strictly decreasing, both term pools
redexes     all 16 canonical redexes fire, one normal form each
divergence  1498 random     -> no term has two normal forms
             681 structured -> no term has two normal forms
```

**Still confluent.** The ten rule *names* are unchanged — nothing had to
be added to compensate — but the tables inside them shrink:

| | with `h` | without |
|---|---|---|
| `absorb` entries | 18 | **10** |
| `low-bit` series cases | 4 | **3** |
| `low-arg` cases | 3 | **2** |
| `collect` instances | 5 | **3** |
| `telescope` instances | 5 | **3** |
| total rule instances | 47 | **32** |

And one rule disappears outright: `h(D t) & 1 → N(h t) & 1`, which
needed `h` *and* `D`.

## 6. The measure reverts

That vanished rule was expensive. It was the one that traded a named
series for `N` at the cost of a **bigger argument**, and it alone forced
0044 §5 to reorder the termination measure from 0043's

```
(series count, argument size, non-N series, size)
```

to `(series count, non-N series, argument size, size)`. With `h` gone,
0043's ordering is verified sufficient again on both term pools.

So the objection was load-bearing twice over: `h` was not a second
information destroyer, and the one rule that only existed to police it
was also the one distorting the termination order.

## 7. Honest limits

- §2's procedure covers `h` in the **base algebra** — composed with `^`,
  `&`, `a`, `b` and constants. It does **not** push through a series
  argument: there is no identity turning `U(h t)` or `T(h t)` into
  something `h`-free, because `a` does not commute with `T`. §3 makes
  that moot by removing the `h`-series rather than translating them, but
  a term like `U(h x)` in the *old* language has no §2 image.
- §4's causality test is exhaustive at width 10 for the listed
  operators, not a proof for every h-free expression. The closure
  argument — that a composition of LSB-causal maps is LSB-causal — is
  immediate but unformalised here.
- The confluence re-run inherits 0044 §8's limits: graph search rather
  than critical pairs, single-variable, node caps reported (2 of 1498
  and 19 of 681).

## 8. Open

1. **Does `N` have a telescoping after all?** 0042 §3 blamed its absence
   on `N = U | D`. With `D` gone that explanation is unavailable, and
   the question of what plays the cancellation role for `N` is open
   again — 0038's rules were found case by case, and §4 says `N` is the
   language's only downward channel, which is a much more specific thing
   to look for a law about.
2. **Is `{^, &, a, b, constants}` + `N` a minimal signature?** §4 shows
   `N` is not generated by the rest. Whether `b` is generated by `a`
   (`b(t) = a(t) ^ 1` — yes, so `b` is *not* primitive) shrinks the list
   further, and 0013/0014's Post-style completeness question applies
   directly to what remains.
3. **The `h`-side operators, if ever wanted**, are now recoverable only
   by adding a downward channel richer than `N`. That is a cleaner
   statement of what 0042 §6.3 was asking than 0042 could make.
