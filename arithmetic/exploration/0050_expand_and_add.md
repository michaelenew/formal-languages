# 0050 — Expand instead of collect, and addition in the sentence frame

Two corrections and one construction. Code: `output/expand_and_add.py`.

**The correction that matters:** containment is not a relation needing
its own derivation system. It is a *statement* — `A ^ AB`, the assertion
that `A` is empty where it misses `B` — and a canonical form that sends
true statements to `0` handles it with no order theory at all. 0048 and
0049 both built machinery around it that was not needed.

---

## 1. Expansion, not collection

0043 chose `collect` — `S(a) ∘ S(b) → S(a ∘ b)` — as the combining rule,
and that choice was made before there was a canonical form to judge it
against. The other orientation is 0042 §2's fixpoint law run **forward**,

```
S(t)  ->  t  ∘  σ_S(S t)
```

with ANF's symmetric difference left to do the cancelling.

**Telescoping falls out at one unfolding, for all three cells:**

| | | |
|---|---|---|
| `!(t) ^ a(!t)` | `= t` | depth 1 |
| `U(t) ^ a(U t)` | `= lowset(t)` | depth 1 |
| `T(t) ^ b(T t)` | `= lowzero(t)` | depth 1 |

Expand `S(t)` to `t ∘ σ(S t)` and the partner annihilates. So
`telescope` is not a rule — it is the fixpoint law plus ANF.

Two things had to be right for that. The **measures must unfold too**,

```
lowset(t)  = t & ¬a(U t)          lowzero(t) = ¬t & b(T t)
```

(each is its own telescoping solved for the measure; both verified),
because otherwise expansion stops one step short of the identity it is
reaching for. And expansion must be **positional** — one occurrence
unfolded at a time, with the search picking which. A telescoping pair
needs the shifted copy held fixed while the bare one unfolds; a stranded
`a(x) & lowset(x)` needs the unfolding to happen *under* the shift. No
uniform pass does both.

**`collect` is NOT subsumed, at any depth**, and that is worth knowing.
Expanding `!(x) ^ !(y)` gives `x ^ y ^ a(!x) ^ a(!y)`; expanding
`!(x^y)` gives `x ^ y ^ a(!(x^y))`. The difference is the same question
one shift up, forever. `collect` is 0042 §2's **second** law,
distribution, and it is independent of the fixpoint. 0044 ordered the
two against each other as rivals; they are not the same fact.

**As a sentence test** — the corpus's own criterion, "does the statement
reduce to `0`", not "do two terms share a normal form" — with both
`collect` and `telescope` deleted and expansion in their place:

```
82 true statements `A ^ B` built from equal pairs
80 reduce to 0            2 do not
```

and the two that do not are both `T(T x)·T(b x)` shapes needing
`collect`, which §1 showed expansion does not subsume. So the cost of
deleting `collect` is 2 of 82, and nothing else is missing.

**Three corrections to an earlier draft of this file**, all of them
defects in the *procedure*, none in the algebra or the primitives:

1. Expansion as a uniform pass is the wrong operation. Telescoping needs
   the shifted copy held **fixed** while the bare one unfolds; stranded
   terms like `a(x) & lowset(x)` need the opposite, an unfolding
   **under** the shift. No single pass does both. Expansion has to be a
   **positional rewrite** — unfold one occurrence, let the search pick
   which — like every other rule.
2. `a(U t)` must be reachable. `a` is a homomorphism, so expansion
   pushes through it; leaving it opaque stranded `a(x) & lowset(x)`,
   which is `0`.
3. A capped search is not a failed search. `normal_forms` reporting
   `capped` means it stopped early, not that its results are wrong —
   every rule preserves meaning, so reaching `0` on one path is a proof.
   Discarding capped results as unusable hid the last of the misses.

An earlier draft reported "15 unidentified pairs" as if it measured the
sentence form. It measured those three bugs.

## 2. Containment is just a statement

The user's framing, and it is right:

```
A ⊑ B      is      A ^ AB
```

Under expand-and-cancel, every containment 0049 needed a derivation
system for goes straight to `0`:

```
T(t) ^ T(t)t                  -> 0   depth 0
T(t) ^ T(t)a(T t) ^ T(t)1     -> 0   depth 1
x ^ U(x)x                     -> 0   depth 0
!(x) ^ !(x)U(x)               -> 0   depth 0
a(!x) ^ U(x)a(!x)             -> 0   depth 0
lowset(x) ^ lowset(x)x        -> 0   depth 0
```

The second line is exactly the identity **0049 §6 called the wall**. It
was a wall only because `contain` was written as a factor-drop between
two atoms, and the statement is a polynomial. Expansion opens it.

So 0049's conclusion needs correcting: the obstacle was never that ANF
cannot see order. It was that the *rule* was the wrong shape, and the
right shape was already in 0042 §2.

## 3. What a series costs, by join

Monomials in the ANF of `k` terms of a series:

| join | k=1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| `^` | 1 | 2 | 3 | 4 | 5 | 6 |
| `\|` | 1 | 3 | 7 | 15 | 31 | 63 |
| `&` | 1 | 1 | 1 | 1 | 1 | 1 |

`&` is free (one monomial, `k` factors), `^` is linear, `|` is `2^k − 1`.
So the `|` cell's partial sums are the expensive ones, and its closed
form `U` is the only thing between the sentence and an exponential.
0049 §5 measured this as the price of failing to *recognise* a join;
here it is the price of *expanding* one. Same number, both directions.

## 4. Addition

```
p = x ^ y                 g = x & y
C = g | (p & a(C))                       the carry set
x + y = p ^ a(C)
```

Verified exactly, both the closed form and the fixpoint equation, on
4000 random pairs at width 24. **Nothing but `^`, `&`, `|`, `a`.**

And `C = g | (p & a(C))` is 0042 §1's schema shape `S = base ∘ σ(S)`
with the shift no longer fixed:

```
C  =  ⋁_k σ_p^k(g)              σ_p(z) = p & a(z)
```

verified by unfolding. **Addition is the `|` cell over a guarded shift**,
and the schema's own two shifts are the constant cases of one affine
family:

```
σ_{p,q}(z) = (p & a(z)) ^ q          a = σ_{Ω,0}      b = σ_{Ω,1}
```

So `U` is the `p = Ω` member of the family the carry already lives in.
The schema did not need a new cell — it needed the shift widened from
two constants to an affine map, and addition was inside it all along.

**`succ` is the `y = 1` case.** Verified for every `x < 2^14`:

```
C(x, 1) = T(x)          so   x + 1 = (x ^ 1) ^ a(T x) = x ^ b(T x)
```

The trailing-ones mask was never a special construction: it is the carry
set of adding one. 0041's `T`/`succ` circle — "neither is prior" — is
that identity read in both directions.

**All three universal laws survive** (0042 §2), measured on 2000 pairs:

| law | |
|---|---|
| fixpoint | holds, by definition |
| distribution over the base, guard fixed | **holds** — so `collect` applies to the carry unchanged |
| telescoping, measure `g & ¬σ_p(C)` | **holds** |

and the measure specialises correctly: at `p = Ω, g = t` it is
`t & ¬a(U t)` = `lowset(t)`, the plain `|` cell's own measure. The
guarded cell is a **full member** of the schema, not a degenerate one.

## 5. Honest limits

- §1's "80 of 82" is one generator at depth 3 over a sampled pool, with
  a bounded search (3 unfolding rounds, capped normal-form search). It
  measures reach on that sample, not completeness. Raising the search
  budget does not move the 2 survivors, which is why they are attributed
  to the missing `collect` rather than to the budget.
- Termination is **not** established for expand-and-cancel. Expansion
  grows terms; here it is applied a bounded number of times and the
  local rules run to a normal form in between. Whether some bound always
  suffices, and what it is, is untouched — this is a canonicalisation
  *procedure* with a depth parameter, not a terminating rewrite system.
- §4's addition is verified numerically at width 24 and by unfolding,
  not proved. The guarded-shift claim is checked on the `|` cell only;
  the other joins over `σ_p` are unexamined.
- The affine family `σ_{p,q}` is *stated* from three data points
  (`a`, `b`, `σ_p`). Nothing here shows it is the right closure, or that
  the nine-cell table survives the widening.

## 6. Open

1. **Redo 0042's table over affine shifts.** Nine cells became five for
   two constant shifts. With `σ_{p,q}` the table is a family, and the
   question "which cells are non-trivial" becomes "for which `(join, p,
   q)` does the series converge". `(^, b)` diverged; whether guarding
   fixes it is immediate to ask and would say whether the carry's
   `^`-sibling exists.
2. **Terminate the expansion.** §5's first limit is the real one. The
   natural measure is that unfolding pushes series atoms up the shift
   ladder, so a term whose series arguments are all `a^k(t)` with `k`
   bounded by the term's depth may be a normal form.
3. **Multiplication.** 0047 §7 put the wall at unbounded state and
   located it at `x·y`. With the guarded shift in hand, `x·y` is a sum
   of `2^i`-shifted copies guarded by `y`'s bits — which is the same
   shape one level up. Whether that is a *second* widening of the shift
   or the point where the family genuinely stops is the sharp question,
   and it is where the boundary of this workstream should now be tested.
