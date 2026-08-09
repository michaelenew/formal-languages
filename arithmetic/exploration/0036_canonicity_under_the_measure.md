# 0036 — Canonicity under the measure: what fails, what survives, and the parameter group

Asked for: show why there is no canonical form once `|.|` / `{.}` is
introduced. The honest answer is graded, and the middle case came out
the other way from what this file set out to prove. Code:
`output/canonicity_under_the_measure.py`.

---

## 1. Three senses of "canonical form", which have to be kept apart

The question is ambiguous, and the ambiguity is doing real work:

**(a) Some computable canonical form exists.** This is nearly free. If a
class is recursively enumerable and equivalence in it is decidable, then
"the least equivalent representation in a fixed enumeration" is a
canonical form, computable, and it terminates with a bound readable off
the input (the input itself is in the enumeration). It compresses
nothing and is reached by search rather than rewriting. **The layer has
this too**, so it cannot be what distinguishes anything.

**(b) A canonical form reached by terminating rewriting from the term.**
The corpus's actual requirement — "a knowably terminating no-cleverness
algorithm", with a-priori bounds composable from the term (0006).

**(c) A canonical form determined by the semantics.** What makes ANF
canonical is Stone; what makes the minimal automaton canonical is
Myhill–Nerode. Nobody chose them.

Layer: has (c), hence (b) and (a). The rest of this file asks where the
measure leaves each.

## 2. Unguarded: no canonical form, unconditionally — (a) fails

A canonical form reached by a terminating reduction **is** a decision
procedure for truth: reduce, then look at whether the result is `0`. So
(a) fails as soon as the theory is undecidable, and layer + `{.}` is BIT
is full arithmetic (0034 §4). Hence no terminating confluent rewrite
system for the unguarded operator exists — not "none has been found",
none exists, and no cleverness will produce one.

This is the proof. The corpus's own diagnosis is separate and weaker,
and worth stating because it is what one actually notices first
(`clue/2026-06-21`: "substitutions that have no guaranteed termination
point"). Every layer rule is bounded by a syntactic measure readable off
the term. Bit-length of the result, for inputs of bit-length `L`:

```
x ^ y      <= L
x & y      <= L
x << 1     L + 1
x + y      L + 1
{x} = 2^x  2^L         2, 4, 8, 16, 32, 64, ...
```

The layer's operators move the measure by at most one; the level map
moves it exponentially. So no measure certifying the layer's termination
certifies `{.}`'s. That is a diagnosis, not a proof — a cleverer measure
is not excluded by it. Undecidability is what excludes every measure.

## 3. Guarded: the intended impossibility, and why it does not exist

The plan was a **Pareto obstruction**. The tier has two resources —
control states and registers — where the layer has one. If they trade
against each other, "the smallest representation" is not well-defined,
and (c) fails for the tier the way it cannot fail for the layer.

The construction: `popcount(x) ≡ 0 mod m` has two presentations, and
neither dominates the other.

```
m   control-only     register        same language   Nerode index
2   2 states, 0 reg   1 state, 1 reg   yes             2
3   3 states, 0 reg   1 state, 1 reg   yes             3
4   4 states, 0 reg   1 state, 1 reg   yes             4
5   5 states, 0 reg   1 state, 1 reg   yes             5
```

An unbounded trade — `m` control states bought with one register — and
`(1, 0)` is impossible, since a one-state register-free automaton
accepts everything or nothing. It looks like a frontier.

**It is not one.** The language is *regular*; its Nerode index is
exactly `m`; its canonical form is the `m`-state minimal automaton. The
register presentation is not a rival minimum, it is simply not minimal.

And every control/register trade that can be built works this way: what
gets traded is a **regular** sub-part, and the minimal automaton absorbs
it. On the non-regular part the two resources do not trade at all —
comparing two unbounded counts needs the registers, and no amount of
control substitutes. So there is no Pareto frontier, and the intended
impossibility argument does not exist.

Recorded as a failed construction because it is evidence in the
*opposite* direction: it suggests the split between control and register
is semantically forced rather than chosen.

## 4. What is actually true: the register content is free up to GL(d, ℤ)

The split is forced. What is *not* forced is the **basis** of the
register space.

0034 §6 found two unrelated presentations of the balance rule that reduce
to identical canonical forms: `|A| = |B|`, and `|A^B| = 2|A|` under
disjointness. Their register vectors are related by an integer matrix:

```
(|A|, |A^B|) = M (|A|, |B|),    M = [[1,0],[1,1]],    det M = 1
```

verified on every disjoint pair below 128, with the two canonical forms
rechecked identical. And the freedom is exactly unimodularity, not
arbitrary relabelling: the singular `M = [[1,1],[1,1]]` sends the
balanced pair `(1, 2)` and the unbalanced pair `(0, 3)` to the same
register vector `(2, 2)`, so no acceptance predicate on the image can
separate them.

The general argument: a deterministic Parikh automaton's register map is
the **abelian part of its transition monoid**, so changing which counts
the registers hold is a change of basis in ℤ^d. Two presentations
denoting the same relation differ by an invertible integer matrix, and
the canonical form is the invariant of that action.

So the measure does not destroy canonicity. It adds a **parameter
group** — and the frame taxonomy already has parameters: order,
polarity, GL(n,2), sharing, lift (0024, 0030). 0030 also showed the
GL(n,2) parameter is *mandatory*, not decorative: the random affine
family escapes all seven frames simultaneously and is cured only by it.
**GL(d, ℤ) is the count sort's GL(n,2).** Argued in general; only the
instance above is machine-checked.

## 5. Status, corrected

| sense | layer | counted tier | unguarded `{.}` / `\|.\|` |
|---|---|---|---|
| (a) some computable canonical form | yes | **yes** (decidable equivalence) | **no** (undecidable) |
| (b) reached by terminating rewriting | yes | open | no |
| (c) determined by the semantics | yes (Myhill–Nerode) | **up to GL(d, ℤ)** — argued | no |

This corrects the open item as 0034 §8 and 0035 §7 stated it. Canonicity
for the tier is not simply "open": (a) holds outright, and (c) is not
in doubt as an *existence* question — it is a question about the
parameter group and about finite presentability. The remaining work is
sharper than before:

1. **Prove the GL(d, ℤ) statement.** Two deterministic Parikh automata
   denote the same relation iff their control quotients agree and their
   register maps differ by a unimodular matrix. Only the instance is
   checked.
2. **Finite presentability off the window.** The Nerode quotient of the
   configuration space is semantically defined but infinite; the open
   step is that it is Presburger-presentable, via the product
   automaton's semilinear Parikh-indexed reachability (0034 §8).
3. **Sense (b)** — whether the canonical form is reachable by rewriting
   rather than by construction-then-minimisation. Untouched.

## 6. The structural reading

Why the layer needed no parameter and the tier does:

- The layer's canonical form is **coordinate-free**. The state set *is*
  the set of residuals, a finite set, and a finite set has no
  coordinates to choose.
- The measure makes the residual set **infinite** — `|A| = |B|` has
  residuals indexed by the running difference, measured `1, 3, 5, 7, 9`
  (0035 §4b). An infinite state space can only be written down by
  coordinatising it: "the states are ℤ^d and the moves are the register
  increments". Naming a register *is* choosing coordinates.
- Different coordinatisations are equally valid, and the ones that
  preserve the language are exactly the invertible ones.

That is the whole of it. **The measure does not cost canonicity; it
costs coordinate-freedom** — and the frame taxonomy is the workstream's
existing theory of exactly that cost.
