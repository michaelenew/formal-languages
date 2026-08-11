# 0042 — The series zoo is one schema, and it carries its own rewrite rules

Asked: collapse the series zoo, and categorise how `N` and `T` compose
and decompose into a convex rewrite system. Code:
`output/the_series_schema.py`.

---

## 1. Nine cells, five survivors, and they are the corpus's operators

Every series in the corpus has the shape

```
S(x)  =  x  ∘  σ(x)  ∘  σ²(x)  ∘  …
```

for a join `∘ ∈ {^, |, &}` and a shift `σ ∈ {a, b, h}` — where `a(x)=2x`
fills with zeros, `b(x)=2x+1` fills with ones, and `h(x)=x>>1` drops the
low bit. Nine cells, enumerated and identified:

| join \ shift | a (fill 0) | b (fill 1) | h (right) |
|---|---|---|---|
| `^` | **`!`** xor series | *divergent* | **`!ʰ`** suffix parity |
| `\|` | **`U`** up-closure | universe | **`D`** down-closure |
| `&` | 0 | **`T`** trailing ones | 0 |

**Five non-trivial cells, and they are exactly the operators the corpus
carries separately.** The other four are constants or never settle —
`(^, b)` diverges because `b` fills with ones forever, so no position
ever stabilises.

That is the collapse: `!`, `!ʰ`, `U`, `D`, `T` are one construction with
two parameters, not five primitives.

## 2. Three universal laws, and two that the join decides

Verified for every survivor:

```
fixpoint       S(x) = x ∘ σ(S x)
distribution   S(a ∘ b) = S(a) ∘ S(b)         over ITS OWN join, and no other
telescoping    S(x) ^ σ(S x) = <the measure>
```

Those three are the expansion, combination and cancellation rules a
convex system needs. Two further properties split by **join**, and they
are exclusive:

| join | measures | closure | invertible |
|---|---|---|---|
| `^` | `x` itself | no | **yes** |
| `\|` | the extremal element | **yes** | no |
| `&` | the extremal **gap** | **yes** | no |

A `^` series can be undone — `x = S(x) ^ σ(S x)` *is* its telescoping
identity — and so is never idempotent. A `|` or `&` series keeps only
one extremum, so it is idempotent and cannot be undone.

Filled in: `!` and `!ʰ` measure `x`; `U` the lowest set bit; `D` the
highest set bit; `T` the lowest **zero** bit. Which is 0041's `T`
identity taking its place in a table rather than standing alone.

## 3. `N` is not a cell

```
N(x) = U(x) | D(x)              verified
```

`N` is two `|` cells joined. `U` and `D` each measure one extreme;
joined, they lose both and keep only whether an extreme exists at all.

**That is why `N` behaves unlike the rest and why its rules had to be
found separately in 0038.** It is not a member of the family — it is a
combination of two members, and combination is exactly what destroys the
telescoping (there is no single extremum left to return).

## 4. How `N` and `T` compose: everything collapses

Row applied first, then column:

| | `N` | `T` | `U` | `D` |
|---|---|---|---|---|
| `N` | `N(x)` | `N(x)` | `N(x)` | `N(x)` |
| `T` | `N(x&1)` | `T(x)` | `N(x&1)` | `T(x)` |
| `U` | `N(x)` | `N(x&1)` | `U(x)` | `N(x)` |
| `D` | `N(x)` | `D(x)` | `N(x)` | `D(x)` |

**Every composite collapses to something already named.** No composite
generates a new operator, which is the property a terminating rewrite
system wants — the closure of `{N, T, U, D}` under composition is
itself.

Reading the table: `N` absorbs everything on either side (`N∘f = N` for
every `f` here, and `f∘N = N` for `f ∈ {T, U}`); `T` and `D` absorb each
other; and exactly **two** entries move information rather than deleting
it:

```
N(T x)  ->  N(x & 1)
T(U x)  ->  N(x & 1)
```

Both say the same thing from two directions: `T(x)` is empty exactly
when `x`'s low bit is clear, and `U(x)` reaches position 0 exactly then
too. Those two are the rules worth writing down; the rest are
absorptions.

## 5. The rewrite system this gives

Collecting §2 and §4, for a series `S` with join `∘`, shift `σ`, measure
`m`:

```
expansion      S(x)         ->  x ∘ σ(S x)              [unfold once]
combination    S(a ∘ b)     ->  S(a) ∘ S(b)             [push inward]
cancellation   S(x) ^ σ(S x) ->  m(x)                   [telescope]
idempotence    S(S x)       ->  S(x)                    [| and & only]
absorption     the §4 table                             [composites]
```

Every rule either strictly reduces the number of series symbols or
replaces a series by a measure, so a size measure counting series depth
decreases — the same shape as 0038's termination argument.

**What is not yet checked is confluence**, which a canonical form needs
as much as termination. That is the honest remaining gap, and it is the
same gap 0038 §6 left open; the difference is that the rule set is now
finite, uniform, and derived from the schema rather than assembled
case by case.

## 6. Open

1. **Confluence** of §5, over `{^, &, |, a, b, h}` plus the five series
   and `N`. The rules are now few enough to attempt by critical-pair
   analysis rather than by sampling.
2. **Is `N`'s behaviour generic for joins of cells?** `N = U | D` loses
   the telescoping. Whether every combination of two cells does, and
   what replaces it, would say whether the family is closed under
   combination or whether `N` is the only useful joint.
3. **The `h`-side members are new to the corpus.** `!ʰ` (suffix parity)
   and `D` (down-closure) fall out of the schema but do not appear in
   the corpus's operator list. Whether they are useful — `D` already
   appears inside `N` — or merely formal, is unexamined.
