# 0037 — Why `H ^ HK` stops collapsing at `<<`, and the rule that repairs it

Written in the corpus's discipline throughout: a statement is a set term
that is empty exactly when the condition it describes is true, `^` is
equality, `|` is joint truth (`a | b = a ^ b ^ ab`), juxtaposition is
`&`, and **asserting K *is* the definition of the context** — there is no
"but what if x were 1" once K says `x ^ 2`. One consequence of
juxtaposition bites immediately: `2|A|` reads as `2 & |A|`, so doubling a
count must be written `s(|A|)` with `s(x) := x << 1`. Code:
`output/pointwise_and_the_containment_test.py`.

**This file replaces an earlier version whose headline was wrong.** That
version concluded no rule set could repair the test. It reached that by
reasoning about values of `x` where `K` is not empty — exactly the move
the framing excludes. The repair exists, it is one rule, and it is
below.

---

## 1. The mechanism, reproduced

The corpus's own example — "if `x` and `y` are disparate then
`x | y = x ^ y`" — run through the engine with no special cases:

```
K := xy                      ->  xy
H := (x | y) ^ (x ^ y)       ->  xy
H ^ HK                       ->  0
```

Empty, so the entailment is known. Everything below is measured against
this as the standard of what "works" means.

## 2. Why the test is complete for `{^, &, 1}`

Because every one of those operators is **pointwise** — it acts on each
position independently and identically. So if `H ⊄ K`, restrict the
universe to the single offending position; the operators are unchanged
by the restriction, and there `K` is empty while `H` is not. Entailment
fails too. Contrapositively entailment implies containment, and the
converse is immediate.

Machine-checked on 400 random terms over three symbols and a
four-element universe: the two verdicts agree every time. This is a
theorem about the pointwise fragment, not a lucky coincidence, and it is
why the test earned its trust.

## 3. Where it stops

`<<` carries position `p` to `p+1`. A one-point universe is not closed
under it and the squeeze dies. With `K := x ^ 2` and `H := s(x) ^ 4`:

```
H ^ HK  ->  s(x) ^ 4 ^ s(x)x ^ 2s(x) ^ 4x        (4&2 having cancelled)
```

which does not reduce to 0. Containment against **K alone** is no longer
equivalent to entailment.

## 4. The repair: close the knowledge under `s`

The missing rule is not a term-level rewrite. It acts on *statements*:

> **from `K` infer `s(K)`**

sound for the most elementary reason available — `s` carries the empty
set to the empty set, so if `K` is empty then so is `s(K)`.

And it closes the example on contact. `s(K) = s(x ^ 2)`, and pushing `s`
to the leaves through its own distributivity gives `s(x) ^ 4`, which **is
`H`**. So `H ^ H·s(K)` is `H ^ H` = 0, with no new term-level machinery
at all.

The knowledge in force is therefore not `K` but its **s-closure**
`K | s(K) | s(s(K)) | …`. Measured:

```
H  := s(x) ^ 4    against K                     H ^ H·K*  ->  not 0
H  := s(x) ^ 4    against K | s(K)              H ^ H·K*  ->  0
H2 := ss(x) ^ 8   against K | s(K)              H ^ H·K*  ->  not 0
H2 := ss(x) ^ 8   against K | s(K) | ss(K)      H ^ H·K*  ->  0
```

**The depth needed is the shift-depth of the hypothesis**, read off `H`.
So the search is bounded a priori, which is exactly the corpus's own
termination requirement — knowably terminating, no cleverness.

This also answers "what would reverse-engineering the automaton's shift
into ANF look like". The closure is an *infinite union*, and a finite
representation of an infinite union closed under the shift is an
automaton. So this is the sentence-side derivation of 0006's "the
automaton is the closed form of the stabilizing series", and of 0023's
"what forces the DFA". The templating instinct was right; what has to be
injected is the **shifted knowledge**, not the residual.

## 5. The closure is sound but not complete, and the gap is the inverse

Measured on 2424 random satisfiable `K`/`H` pairs over
`{^, &, |, s, constants}`:

```
neither test was ever unsound
true entailments missed by  K | s(K) | s2(K) | ...  :  67
true entailments missed by the two-way closure      :   0
```

The misses are all **downward** inferences — from `s(x) = 4` infer
`x = 2` — which need the *injectivity* of `s`. The second rule is the
mirror of the first and just as elementary:

> **from `K` infer `K >> 1`**

sound because the right shift also carries the empty set to itself. That
is the corpus's own `h`, flagged in `clue/2026-06-21` as "a genuinely new
primitive, not constructible from anything you have" — and here it
appears not as a term-former but as the second half of a closure rule.
Adding it closes every miss in the sample.

Status, stated exactly: both closures are **sound always** (checked, no
unsound verdicts in 2424 pairs). The two-way closure is **complete on
this sample**; general completeness is unproven, and the depth bound
(`shift-depth of H`, plus a margin in the two-way case) is measured
rather than derived.

## 6. What this means for the measure

`|.|` is not pointwise either, so §3 applies to it as well and the
containment test against a bare `K` will miss entailments. The question
0035/0036 should have been asking is whether `|.|` admits a closure rule
of the same shape. It does not, in the same form: `s` is a bijection of
statements up to the bottom bit, so closing under it and its inverse
stays inside the sentence algebra, whereas `|.|` maps a statement to an
object of a different sort. That asymmetry is the sentence-side version
of the two-copies-of-ℕ line, and it is why the counted tier needed a
register while `<<` needs only a closure rule.

## 7. Open

1. **Prove or refute completeness of the two-way closure** over
   `{^, &, |, s, h, constants}`. The sample says complete; a proof would
   make the sentence frame's shift fragment a genuine decision procedure
   and would be the first canonical-form result on the sentence side
   since 0019.
2. **Derive the depth bound** rather than measuring it. The upward bound
   is the shift-depth of `H`; the two-way bound is not yet pinned.
3. **Is the closure the automaton?** Conjecture: the s-closure of `K`,
   presented finitely, is exactly the minimal automaton of `K`'s
   relation. If so, 0006's claim becomes an identity rather than an
   analogy.
4. **`|.|` in the same frame.** §6 says the closure trick does not
   transfer. Whether there is a different statement-level rule for the
   measure — one that stays in the sentence algebra — is the sharpest
   remaining question for the sentence side of the counted tier.
