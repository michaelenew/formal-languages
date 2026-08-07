# 0013 — The Post-style structure: three closures, three bases

## In plain terms, first

"Can you build XOR out of AND and shift?" has no answer until you say
what *build* means. There are exactly three answers, because there are
three natural amounts of the wiring calculus (0008: share, hide, flip)
you might allow:

1. **Nesting only** — plug outputs into inputs, `f(g(x), h(y))`. This
   is the level the corpus's expression language works at.
2. **Share + hide** — also allow hidden helper channels: "there
   exists some w such that these constraints all hold". This is where
   addition lives (the hidden carry wire).
3. **Share + hide + flip** — also allow negation. Now "there is no w
   such that…" is sayable, and therefore "for every w…", and
   therefore **superlatives**: *the largest set such that…*

XOR needs superlatives, and that is the whole story. With AND alone
you can say "z sits inside x" (z & x = z) and "z misses y"
(z & y = 0) — but that describes many sets, including the empty one.
Say instead *the largest* such z and you have pinned down exactly
x minus y; do it twice and union them (also a superlative: the
smallest common superset) and you have x ^ y. Superlatives need
"every", "every" needs "there is no", and "there is no" needs flip.
So XOR is unreachable at levels 1 and 2, and free at level 3.

Which level is the real one? **Level 3** — the framework's own
deduction test is `K & ~H is empty`, so flip was always in the
language. That is why the basis collapses to {&, <<}.

The rest of this file is the same content stated precisely, with the
standard names for the invariants that make each level's answer a
proof rather than an observation.

---

The open question of 0008/0012 — is ^ derivable from {&, <<,
constants}? — is **answered, and the answer is level-dependent**. That
turns out to be the interesting content: the basis question has three
different answers depending on which closure operation is meant, and
the three levels are governed by three known invariants. Executable:
`output/closure_hierarchy.py`.

## The leg-up from the corpus

`clue/older/Posts Functional Completeness Theorem.md` records Post's
engine exactly: *"any composition wherein all elementary functions
have property X must also exhibit property X"*, so a generating set
must break every X. And `clue/2025-01-09 generalized AND and XOR and
nilary FC.md` goes further, defining for a function f and a test t

    f satisfies t  iff  f(t(rows)) == t(f(columns))

and observing **"f satisfies t implies t satisfies f by symmetry"**.
That symmetric commutation relation is precisely the one underlying
the **Pol–Inv Galois connection** of universal algebra (Geiger;
Bodnarchuk–Kalužnin–Kotov–Romov): operations and relations that
commute, with clones and relational clones as the two closed sides.
The corpus rediscovered the connection's defining relation
independently; the literature supplies the closure theorem. That is
the leg-up, and it is what makes the following classification
routine rather than ad hoc.

## The three levels

| closure | operations | governing invariant | is ^ needed? |
|---|---|---|---|
| **term** | composition (nesting) | monotonicity — Post's class M | **yes** |
| **pp** | ∧, ∃, = | polymorphisms (Geiger/BKKR) | **yes** (and ∪ too) |
| **first-order** | ∧, ∃, =, ¬ | invariance; stability | **no** |

**Term level.** &, <<, and constants are all monotone for ⊆;
monotonicity is closed under composition; ^ is not monotone. So ^ is
not a composition of them — the corpus's own Post-class argument,
verified. This is why the original {^, &, 1} needed XOR: at the term
level its work is real.

**pp level.** Drop negation. The preservation lemma is elementary: if
every base relation is closed under coordinatewise F, so is every
pp-definable relation (conjunction preserves closure; and if (a,w₁),
(b,w₂) ∈ R with R F-closed then (F(a,b), F(w₁,w₂)) ∈ R, so projections
stay closed). Take F = ∩: the graphs of &, of <<, and of every
constant are ∩-closed, while the graphs of ^ **and of ∪** are not.
So neither is pp-definable. Strictly sharper than the term level —
∪ is monotone yet still unreachable, so pp closure sees more than
composition does. Geiger/BKKR give the converse, making polymorphisms
a complete invariant here.

**First-order level.** Add negation, and ∀ comes with it. The
finite-subset lattice then defines its own relative complements by
subset-extremality:

    z = x ∪ y   ⟺  x ⊆ z ∧ y ⊆ z ∧ ∀u((x ⊆ u ∧ y ⊆ u) → z ⊆ u)
    z = x \ y   ⟺  z ⊆ x ∧ z & y = 0 ∧ ∀u((u ⊆ x ∧ u & y = 0) → u ⊆ z)
    z = x ^ y   ⟺  ∃p ∃q (p = x \ y ∧ q = y \ x ∧ z = p ∪ q)

with ⊆ itself just (x & y) = x. All three verified equal to their
native forms. **Negation is exactly what collapses the basis.**

## The result

> **The minimal first-order basis of the canonical layer is
> {&, <<} + constants, and both generators are necessary.**

- Generation: {&, constants} gives ^ (above), and {^, &, <<} gives
  the whole layer (0008, modulo Büchi–Bruyère).
- **<< necessary**: any formula names finitely many constants; permute
  bit positions above them. Bitwise graphs and those constants are
  invariant, first-order definitions inherit invariance, and the
  shift's graph is not invariant — (2⁵, 2⁶) is in it, its image
  (2⁶, 2⁵) is not.
- **& necessary**: (finite sets, <<, constants) is a reduct of the
  module GF(2)[t] over itself, and reducts of stable structures are
  stable. With & present, ^ follows (level 3), then addition, then
  x ≤ y as ∃gap: x + gap = y — an infinite linear order, i.e. the
  strict order property, which no stable structure has (0012).

So the corpus's original XOR is **indispensable at the term level and
redundant at the wiring level**. Nothing was wrong with the earlier
claim; the closure operation changed underneath it. Worth stating
plainly because it is the kind of thing that silently invalidates a
basis result: *"basis" is meaningless without naming the closure.*

## What each generator is, in one line each

The two necessity proofs are not merely technical — each names the
world you fall into by dropping that generator:

- **{&, constants} alone** = the permutation-invariant fragment: pure
  set algebra, no notion of position, no arithmetic.
- **{<<, constants} alone** = a stable structure: linear, orderless,
  a module.

So **& is exactly the escape from stability** (it buys order,
arithmetic, all nonlinearity) and **<< is exactly the escape from
permutation invariance** (it buys position structure — the register,
everything sequential). Two generators, two independent escapes, and
the layer is their join. That is the Post-shaped answer: not a lattice
of five maximal classes as in the Boolean case, but two maximal
fragments, each characterized by a preservation property, whose
generators are the two things the corpus had been circling.

## Open / next

- The two maximal fragments above are *known* proper sub-fragments,
  but they are not proved **maximal** (no proof that every fragment
  strictly between them and the full layer collapses). Proving
  maximality would give a genuine Post-style completeness criterion:
  "a set of relations generates the layer iff it escapes stability and
  escapes permutation invariance." That criterion is *conjectured*
  here, and is the natural next theory target.
- The corpus's N-valued generalization (`2025-01-09`) sits naturally
  on the pp/polymorphism side; whether the two-escape criterion has an
  N-valued analogue is unexplored.
