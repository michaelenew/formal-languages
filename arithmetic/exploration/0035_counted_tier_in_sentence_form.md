# 0035 — The counted tier in sentence form: two sorts, two zeros, one measure

0034 presented the tier as automata over channels, and used `=` for two
different equalities. Both were the wrong frame. 0019 established that
the sentence form poly-simulates the automaton and is never beaten on
size, so the sentence form is the one to write in; and the corpus's
equality is `^`, with truth being "the term is the empty set". This file
redoes §5 of 0034 in that frame. Code: `output/counted_sentence_form.py`.

---

## 1. Two sorts, two equalities, two zeros

| | set sort | count sort |
|---|---|---|
| terms | `^`, `&`, `<<`, `1` over symbols | integer forms over measures `\|t\|` |
| structure | idempotent ring | ℤ, not idempotent |
| **equality is** | **`^`** | **`−`** |
| a sentence asserts | the term is the empty set | the form is zero |
| truth checker | the track reads all zeros | the register reads zero |
| "both hold" | union, `S₁ ^ S₂ ^ S₁S₂` | a *system* — no single form does it |

The truth checker is the same in both sorts — *everything reads zero* —
but upstairs that quantifies over **positions** and downstairs over
**registers**. That is the whole of the two-level structure, and it is
why the corpus's one-sided judgment survives intact: a sentence is true
when nothing is left, in either sort.

The `^` overloading in 0034 was the actual error. `^` is the set sort's
equality. The count sort is ℤ, where `a ^ a = 0` is false and `a − a = 0`
is the law. Writing `^` between counts, or `−` between sets, is not a
notational slip — it is the sort violation itself.

A **counted sentence** is a pair `⟨ S ; C ⟩`: a set term asserted empty,
and a list of integer forms asserted zero.

## 2. The measure is the only bridge, and it has three laws

All three verified exhaustively; the first two are the corpus's own,
from `clue/2025-04-04 size operator and hamming distance.md`:

```
|A ^ B| + 2|A & B| = |A| + |B|          the measure law
A & B = 0   <=>   |A ^ B| = |A| + |B|   the corpus's disjoint form
|A << 1| = |A|                          << is invisible to the measure
```

Read together: the count sort sees `^` as `+` **up to the intersection
defect**, sees `&` **only through that defect**, and does not see `<<`
**at all**. So `|·|` is not a ring map — it is a *measure*: additive on
disjoint elements, with `2|A & B|` as the exact failure of additivity.

The third law is the structural one. `<<` is the position operator — the
one 0013/0014 identified as the escape from permutation invariance — and
the measure cannot see it. The measure is precisely what survives
forgetting the order of positions, which is 0034 §5c's statement that
`|·|` is the complete invariant of the position-permuting family, now
readable off a one-line identity instead of an orbit computation.

## 3. The line: two copies of ℕ, never identified

Both sorts are ℕ. The set sort's terms have **values**; the count sort
has **counts**. The measure maps values to counts and is many-to-one.

Undecidability is exactly the **identification of the two copies**.

It is worth being precise about what is *not* forbidden, because the
obvious guesses are all wrong:

- **A section is not forbidden.** `T(A) ^ A` vanishes exactly on
  `0, 1, 3, 7, 15, …` — the corpus's own "canonical set of size N",
  `2^N − 1` — so *the set of size c* is perfectly writable, as a
  sentence, for `c` a count. The tier has a section of the measure.
- **Constants are not forbidden.** `|y| − 1` is legal. Naming finitely
  many points of a map is not naming the map.
- **Hiding is not what separates them.** Both statements in §4 may hide
  their auxiliary symbol, because it is pinned.

What is forbidden is the single move of writing a **value** where a
**count** belongs. That is why:

> `2^|x|` — a set built from a count — is **decidable**.
> `2^x` — a set built from a value — is **BIT**.

## 4. The pair, as sentences

**Decidable.** `⟨ y ^ (w + 1) ; |y| − 1, |w| − |x| ⟩`

Reading: the set part says `y = w + 1`. The first form says `y` is a
singleton, so `y = 2^k`; then `w = 2^k − 1` is `k` ones, so `|w| = k`.
The second form sets `k = |x|`. So the sentence asserts `y = 2^|x|`.

Built and run: **3 control states, 3 registers**, checked exhaustively
against the relation for `x, y, w < 20`, no disagreements.

**Undecidable.** `⟨ y ^ (w + 1) ; |y| − 1, |w| − x ⟩`

Same set part, same first form. The second form now subtracts a *set
term* from a *count*.

That is not a different kind of constraint. **There is no such
subtraction.** The implementation refuses it at construction:

```
SortError: a set term cannot stand in a count form; it has to be
measured first, and its measure lives in the other sort
```

The reason this is the right place to refuse it, rather than a
convenience: everything that passes the sort check compiles to a
deterministic Parikh automaton, and that class is decidable. The check
is a syntactic characterisation of a decidable class, not a fence to be
re-tested against each new trick.

## 4b. `<<` is unary, and the construct is *iteration*

`<<` is the natural suspect, since the level map is literally
`{x} = 1 << x`. But `<<` is **unary**, as the corpus framed it: `x << 3`
is three applications, a finite composition, and finite composition
never leaves the layer. `<<` is also a proved-necessary layer generator
(0008) and the layer is decidable, so no operator is the culprit.

What leaves the layer is **iterating a unary operator a variable number
of times** — the same construct 0002 met when a finite composition could
not compute the successor, and answered there with the stabilizing
series. Two independent features of the iteration decide where it lands:

| statement | iterated | carried across a cut | status |
|---|---|---|---|
| `w ^ (x << 3)` | a constant | nothing | layer |
| `y ^ (1 << \|x\|)` | a count | a count | **in the tier** |
| `z ^ (x << \|b\|)` | a count | a **set** — the bits to place | **outside** |
| `y ^ (1 << x)` | a value | — | closes to BIT |

Same operator in all four rows.

Row three is the one that was not obvious, and it is why "iterate by a
count is fine" would have been an overclaim. **The membership test**: a
deterministic Parikh automaton with `|Q|` control states and `d`
registers, each moving by at most one per column, has at most
`|Q|·(k+1)^d` configurations after `k` columns — polynomial in `k`. So
superpolynomial residual growth rules out every such automaton, whatever
registers it picks; the criterion needs no guess about the register set.

Measured residuals by prefix length (probe depth equal to the maximum
prefix, so each count is exact):

```
z ^ (x ^ y)      << not used         1,  2,  2,  2
w ^ (x << 1)     << applied once     1,  3,  3,  3,  3
w ^ (x << 3)     << applied 3 times  1,  3,  5,  9,  9
|A| - |B|                            1,  3,  5,  7,  9
y ^ (1 << |x|)   shift the constant  1,  4,  6,  8, 10
z ^ (x << |b|)   shift a set term    1,  6, 18, 50
```

The first three rows are the point about unarity, measured: constant
iteration keeps the residual count flat, and `x << 3` costs a flat 9
because it buffers exactly three bits. `x << |b|` has to buffer an
unbounded number.

For the last row, an exact lower bound rather than an extrapolation.
Take the `2^k` prefixes carrying `b = 0`, `z = 0` and every pattern on
`x`. Each has exactly one completion — put `k` ones on `b` next, which
fixes the shift at `k`, and then `z` must replay that prefix's `x` bits.
A completion built for one member fits no other, so all `2^k` are
pairwise distinguishable and need distinct configurations:

```
prefix length     1     2     3     4     5     6
configurations    2     4     8    16    32    64
```

`2^k` against a polynomial bound. **Shifting an arbitrary set by a count
needs the shifted bits buffered, and a register counts — it does not
buffer.** `1 << |x|` escapes only because the thing being shifted is the
constant `1`, so there is nothing to buffer: the sentence pins `y` by
its *shape* (`|y| − 1`, one bit set) and its *offset* (`|w| − |x|`),
never by replaying bits.

This is the sharpest form of the sort discipline. The count sort and the
set sort are both ℕ; a register can hold a count and cannot hold a set;
and a statement is in the tier exactly when what it must remember across
a cut is a count and not a set.

**One caution, and it is why the last row above is phrased differently
from the other three.** The residual test decides membership in the
*tier*. It does not decide Gödel. Undecidability is a property of the
**closed class**, not of any single statement's width — adding the level
map to the layer and closing under the Boolean moves and projection is
what yields full arithmetic (0034 §4). Concretely, `y = 2^x` truncated
to width `w` has a *polynomial* minimal automaton (`5, 8, 11, 15, 20,
25, 31, 38` at `w = 2..9`, measured in `level_crossing.py`), so a
statement can be narrow and still generate an undecidable theory. Two
different lines, and they must not be run together:

- **in the tier / outside the tier** — a width question about one
  statement, decided by the residual test;
- **decidable / Gödel** — a closure question about a class, decided by
  what the class contains and is closed under.

## 5. Why combining the levels does not collapse

The question this file was written to answer: `K` for Infinite Clue has
set sentences *and* a count form, both levels present at once — so why
is the union decidable?

Because the two levels grow in **orthogonal directions** under union,
and neither feeds the other. Measured, unioning one sentence at a time:

```
union so far, after adding                      control  registers
a&b                        (set)                      2          2
a & (b << 1)               (set)                      3          2
(a ^ b) & (a ^ b ^ 1)      (set)                      3          2
|a| - |b|                  (count, old measures)      3          2
|a| - 3                    (count, old measures)      3          2
|c| - 2  with  c ^ (a ^ b) (count, new measure)       5          3
```

- A **set sentence** moves the control column and never the register
  column. No amount of set knowledge can grow the count level.
- A **count form over measures already present** moves neither: it is
  one control state, and it binds registers that already exist.
- Measuring a **new** term costs exactly one register plus the wire
  pinning it (`c ^ (a ^ b)` — 0008's uniquely-determined hidden wire,
  which is why hiding it stays legal).

Mechanically: union multiplies the control automata and concatenates the
registers, so the *shape* — finite control × free commutative register
file, with a decidable acceptance condition — is invariant under union.
Collapse would need a register to name a position. No sentence has such
a term, so no union of sentences has one either. **Presence of both
levels is not interaction between them.**

This also says exactly which extension would be fatal, and it is not an
extension anyone would propose by accident: a rule letting the count
sort's value re-enter the set sort as a position. The measure laws of §2
are all sort-preserving rewrites — from `A & B = 0` you may rewrite
`|A ^ B|` into `|A| + |B|`, and the result is still a count form — so
the bridge can be used freely without ever producing a mixed term.

## 6. What this changes about 0034

- §5's one-clause rule and then two-clause rule are both superseded by
  the sort statement: **one sort discipline, two equalities, and a
  measure that only runs one way.** 0034's clause (i) (`{·}` is not a
  term-former) and clause (ii) (no mixed atom) are the two places a term
  could violate the single discipline, not two independent rules.
- The channel presentation stands as the compilation target; it is not
  the frame to reason in.
- Nothing measured in 0034 changes.

## 7. Open — refined by 0036

Canonicity off the window. In sentence terms the question is now
sharper: the set sort has a canonical form (ANF / minimal automaton) and
the count sort has one (Presburger normal form, itself a minimal DFA in
base 2), and what is unproved is that the *pair* has one — i.e. that the
Nerode congruence on `control × registers` is Presburger-definable. That
is the last step between "decidable tier" and "convex tier".
