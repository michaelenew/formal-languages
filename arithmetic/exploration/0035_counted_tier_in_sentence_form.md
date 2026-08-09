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

## 7. Open, unchanged from 0034 §8

Canonicity off the window. In sentence terms the question is now
sharper: the set sort has a canonical form (ANF / minimal automaton) and
the count sort has one (Presburger normal form, itself a minimal DFA in
base 2), and what is unproved is that the *pair* has one — i.e. that the
Nerode congruence on `control × registers` is Presburger-definable. That
is the last step between "decidable tier" and "convex tier".
