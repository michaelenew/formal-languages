# 0037 — Why `KH ^ H` stops collapsing: the test, not the rule set

Written in the corpus's discipline throughout: a statement is a set term
asserted empty, `^` is equality, `|` is joint truth (`a | b = a ^ b ^
ab`, empty exactly when both are), juxtaposition is `&`. One consequence
of that last convention is worth stating because it bites immediately:
**`2|A|` reads as `2 & |A|`**, so doubling a count must be written
`s(|A|)` with `s(x) := x << 1`. Code:
`output/pointwise_and_the_containment_test.py`.

---

## 1. 0036's two statements, written properly

0036 said "under disjointness" in prose. In the discipline it is a
conjunct:

```
(|A| ^ |B|)      | (A&B)
(|A^B| ^ s(|A|)) | (A&B)
```

Same zero set, verified exhaustively for `A, B < 64`. But the syntactic
identity

```
((|A| ^ |B|) | (A&B)) ^ ((|A^B| ^ s(|A|)) | (A&B))
```

**does not reduce to 0** — at `A = B = 1` it is `2`. Two statements with
the same models and different terms. That is not a slip in the writing;
it is the same phenomenon as §3 below, showing up first.

## 2. Why the test was complete, and it is a real reason

`KH ^ H` is complete for `{^, &, 1}` because **every one of those
operators is pointwise**: it acts on each position independently and
identically. So if `H ⊄ K` at some assignment and some position `u`,
restrict the universe to `{u}` alone — the operators are unchanged by
the restriction — and there `K = ∅` while `H ≠ ∅`, so entailment fails
too. Contrapositively, entailment implies containment, and the converse
is trivial. Entailment and containment are the same condition.

Machine-checked on 400 random terms over `{^, &, 1}` with three symbols
and a four-element universe: the two verdicts agree every time.

This is why the test worked so well for so long, and why trusting it was
reasonable. It is a theorem about the pointwise fragment, not a lucky
coincidence.

## 3. Where it breaks: `<<` is the first non-pointwise operator

`<<` carries position `p` to position `p+1`. A one-point universe is not
closed under it, so the squeeze argument dies. Taking the corpus's own
worked case, `K = x ^ 2` and `H = s(x) ^ 4`:

```
 x   K = x^2   H = s(x)^4   H inside K   KH ^ H
 0         2           4        False      4
 1         3           6        False      4
 2         0           0         True      0
 3         1           2        False      2
 4         6          12        False      8
 5         7          14        False      8
```

- the entailment `K = ∅ ⇒ H = ∅` **holds** (checked to `x < 4096`);
- the containment `H ⊆ K` **fails**;
- `KH ^ H` is **not identically empty**.

So the residual `s(x) ^ 4 ^ s(x)x ^ 2s(x) ^ 4x` is *not* knowably empty
— it is `4` at `x = 0`. **No rewrite rule can make it collapse, because
a rule that collapsed it would be unsound.** The search for the missing
rules was a search for something that cannot exist. What was lost is not
the rule set; it is the completeness of the test, and it was lost at
exactly the first operator that moves information between positions.

This is 0015/0016's finding arriving from the rewrite side. There, the
framing's gap was diagnosed as `∃` and negation — "K ∧ ¬H is empty" is
the entailment test, and it is what the automaton machinery computes.
Containment is the sound, position-free *approximation* to it, and the
approximation is exact only on the pointwise fragment.

## 4. What does work, and it is one line

Index the statement by position. `K = ∅` is then not one equation but
one per position, and the shift acts on the *index*, with `s_i = x_{i-1}`
and `s_0 = 0`:

```
 i   K_i          H_i          K_(i-1)
 0   x0           0            0
 1   1 ^ x1       x0           x0
 2   x2           1 ^ x1       1 ^ x1
 3   x3           x2           x2
 4   x4           x3           x3
```

**`H_i = K_(i-1)` exactly, at every position** — verified as polynomial
identity. So `H` reduces to `K` shifted by one index, and thence to the
empty set. The deduction that no position-free rule could reach is one
relabelling away once positions are named.

That answers "reverse-engineering the automaton's shift into the ANF
frame": what it yields is **an operation on the indexed family of
equations, not a new axiom inside a term**. A finite description of an
indexed family of equations carrying a shift action *is* an automaton —
which is why 0023 found the DFA forced by the same theorem that forced
`<<`, and why 0013/0014 listed `<<` as the escape from permutation
invariance. Naming positions is the price of a non-pointwise operator.

## 5. The templating proposal, assessed

Injecting the residual as an implied axiom is unsound in exactly the way
§3 shows: it vanishes at `x = 2` and is `4` at `x = 0`, so adopting it
asserts something false and everything follows.

The sound form of the same instinct is reduction **modulo the ideal of
the shift's position-indexed relations** — `s_0`, and `s_{i+1} ^ x_i` —
which is a Gröbner basis question. And this is already the workstream's
own territory: 0020 identified expand-and-cancel as **Polynomial
Calculus over GF(2)**, which is precisely the proof system for ideal
membership. The templating rules are the basis; the reduction is PC.

The decisive detail: those relations are **finite per width and infinite
over all widths**. That is the precise reason no finite *position-free*
rule set exists, and it is a sharper statement than "none was found".

## 6. Consequence for the measure, and a correction to 0035

`|.|` is not pointwise either — the count of a set depends on every
position at once. So the containment test is incomplete for it for the
same reason, and the two-level discipline of 0035 is the position-free
way to stay sound: keep the count in a register and never let it meet a
value.

**Correction to 0035 §1.** It said the count sort's equality is `−` and
not `^`, on the grounds that ℤ is not idempotent. That was too narrow.
Counts are numbers, numbers are bitsets, and `a ^ b = 0` iff `a = b`, so
`^` is a perfectly good equality downstairs. More: the acceptance
predicate need not be restricted to Presburger. If it is
Büchi-arithmetic definable — that is, if the count level carries the
layer's own signature `{^, &, <<, 1}` plus `+` — the tier stays
decidable, because the achievable register vectors form a semilinear
hence Büchi-definable set, and intersecting two Büchi-definable sets and
asking for nonemptiness is a sentence of Büchi arithmetic. Boolean
closure survives for the same reason (Büchi-definable sets are closed
under complement).

So the corrected picture is better than the one 0035 drew, and it is the
one the corpus's notation was pointing at: **the count level is a second
copy of the layer's own language, and the discipline is about *level*,
not about which operators are available.** `|.|` is the only bridge, it
runs one way, and no term may mix levels. Argued from decidability of
Büchi arithmetic plus the cited semilinearity; not separately verified
here.

## 7. Open

- Does the level hierarchy continue? A count level can have its own
  `|.|`, giving a level 2 whose counts are bounded by the length of a
  level-1 number. Whether every finite level stays decidable is open,
  and it is the stratified-`V_ω` question of 0005 in a usable form.
- The Gröbner basis of §5 per width: is there a uniform description
  (one rule schema plus an index shift) that a rewrite engine could
  carry without unrolling? That is the sentence-side version of "the
  automaton is the closed form of the stabilizing series" (0006).
