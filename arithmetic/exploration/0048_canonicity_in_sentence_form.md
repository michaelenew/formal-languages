# 0048 — Canonicity in sentence form: the mask goes, and containment is left

Two objections to 0047. First, `7` vs `1 ^ 6` was never a gap in the
algebra — constants are not primitive (0046 §1), and that pair only
exists because the engine carried an integer mask on every monomial.
Second, the machine speaks to *procedure*; a sentence speaks to
*structure*, and the thresholds should be visible in sentence form.

Both hold. Deleting the mask discharges four of 0047's seven laws with
no rule at all and removes the width-bound family outright. What is left
divides cleanly in three, and the third is the real threshold. Code:
`output/sentence_canonical_form.py`.

---

## 1. The representation, with the mask deleted

```
monomial    a set of atoms, multiplied by `&`.  The EMPTY monomial is Ω,
            because Ω & t = t -- Ω is the multiplicative unit.
polynomial  a set of monomials, joined by `^`.  The EMPTY polynomial is 0.
atoms       x, 1, and a(P), !(P), U(P), T(P), lowset(P), lowzero(P), N(P).
```

No integer appears anywhere. `b(t) = a(t) ^ 1` is not a constructor, and
`Ω = N(1)` is reached by a rule, not assumed.

The one construction that carries the weight: **`a` pushes to the
leaves.** It is a homomorphism for *both* joins — `a(P^Q) = a(P)^a(Q)`
and `a(P&Q) = a(P)&a(Q)`, since bit *i* of either side reads bit *i−1*
of each argument — so it never needs to wrap a compound. Pushing it down
makes

```
a(Ω) = Ω ^ 1
```

a fact of construction rather than a constant to evaluate at some width.
That single line is **0047 §5's entire width-bound family, repaired**.
Routing every `a` through the constructor is also what stops `a(Ω)` and
`Ω ^ 1` being two normal forms.

## 2. What the representation does for free

0047 §5's seven laws, re-asked:

| law | |
|---|---|
| `b(x) = a(x) ^ 1` | **free** |
| `a(Ω) = Ω ^ 1` | **free** |
| `7 = 1 ^ 6` | **free** |
| `a(Ω ^ x) & b(x) = 0` | **free** |
| `T(a x) = 0` | needs a rule |
| `U(b x) = Ω` | needs a rule |
| `N(x&1) = !(x&1)` | needs a rule |

Four of seven, and the objection is vindicated: none of those four was
ever about the algebra. The three that survive are all about **the low
bits of the argument**, which is §3.

## 3. One syntactic analysis, three rules

`known_prefix(P, d)` returns the low *d* bits of `P` that are fixed for
every input, `None` elsewhere — the machine table of 0047 §2 run over
`{0, 1, unknown}` instead of over bits. It is checked against the oracle
on 288000 bit-positions with no error. Three rules read off it:

```
settle    S(P) -> its settled value, when a known bit of P reaches the
                 absorbing element of S's join
low-bit   a monomial masked to bit 0, decided by bit 0 of its factors
          -- and separately S(t) & 1 -> t & 1
confine   S(P) -> collapsed, when P's support is bounded to bit 0
```

`settle` and `low-bit` are the same analysis at opposite ends: `settle`
asks what a known prefix of the *argument* does to the operator above
it, `low-bit` asks what known bit 0 of the *factors* does to a monomial
masked to bit 0. `a(t)&1 = 0` and `b(t)&1 = 1` are both the second, which
is why neither is written down.

**How deep the prefix must go** — this is "bounded state", in sentences:

| position `settle` fires at | times | max `a`-depth of the argument |
|---|---|---|
| 0 | 1442 | 2 |
| 1 | 32 | 2 |
| 2 | 2 | 2 |
| 3 | 1 | 2 |

It never fires above the argument's own shift depth, because a known bit
can only come from a shift, from `1`, or from a settled operator
underneath. The bound is syntactic and the term carries it.

## 4. The join decides which rule a cell needs

```
cell   join   absorbing   settles?   measure   settles?
!      ^      none        no         self      no
U      |      Ω           yes        lowset    yes
T      &      0           yes        lowzero   yes
```

`^` makes the two-element algebra a **group** — every element
invertible, nothing absorbing — so no finite prefix of the argument ever
settles `!`, and its measure is the identity and inherits that. `|` and
`&` are not groups, and their absorbing elements are exactly what a
prefix can reach.

So which *kind* of rule a cell of 0042's schema needs is read off its
join alone:

```
^   ->  cancellation only    (telescope; the inverse exists)
|   ->  saturation at Ω      (settle)
&   ->  annihilation at 0    (settle)
```

0042 gave one schema for the operators. This is one schema for their
rules.

*(Corrects a claim made mid-build: I first asserted that `lowset` and
`lowzero` never settle. They do — at the same bit their series does.
Only `!` and its identity measure never settle, and keying the split to
the join rather than to "series vs measure" is what survives.)*

## 5. The rule set

Eleven rules. `settle`, `low-bit`, `confine`, `unit`, `absorb`,
`shift-out`, `N-see-through`, `N-absorb`, `contain`, `collect`,
`telescope`. Against 0043's fourteen and 0044's ten. All 2284 sampled
applications preserve meaning against the unbounded decision procedure,
and no two non-equal terms share a normal form.

What changed from 0044:

- **`fold` is gone.** There is no constant domain. What survives is
  `unit`: the operators on `0` and on `Ω`, a closed finite table with no
  width in it. `!(Ω)` alternates forever and is its own normal form —
  there is no finite term over `{1, a, ^, &}` equal to it.
- **`low-arg` became `confine`**, at any operator rather than a list.
- **`N-shift` split in two**, because it was two facts: the `b` case is
  `settle` (a known 1 at bit 0), the `a` case is `N-see-through` (`a` is
  injective and fixes 0, so `N` cannot tell). `("N","!")` in the absorb
  table is the same fact about `!`.
- **`telescope` needs a common factor.** Restricted to bare monomials it
  misses `(!(t) ^ a(!t)) & m`, which is the shape a distributed
  telescoping takes in ANF.
- **`contain` is new**, and it is §6.

*(Two claims I made and had to correct against measurement: that the
mask-free representation absorbs `low-bit` — it absorbs only the shift
half, and `S(t)&1 = t&1` is a real rule; and that `N-absorb` could use a
vanishing test that ORed across the argument's monomials — it cannot,
which made `N(x)·T(a(x)^1)·1 -> T(a(x)^1)·1` look sound when at `x = 0`
the two sides are 0 and 1. `lowzero` is the one operator that does not
fix 0.)*

## 6. The threshold: containment

Driving the residue down, every family that survives is the same one.
The schema carries an order,

```
T(t)  ⊆  t  ⊆  U(t)  ⊆  N(t)
```

and `U(t)` is the **top of everything the schema builds from `t`** —
measured: `t`, `!(t)`, `T(t)`, `U(t)`, `lowset(t)` and every `a`-shift of
any of them sit under `U(t)`. The two exceptions are exactly the ones
the structure predicts: `lowzero(t)` is the dual and sits under
`U(t ^ Ω)`, and `N(t)` sits above everything.

Adding `contain` (`A & B -> A` when `A ⊆ B`) cuts the unidentified pairs
from 36 to 19. **And the 19 that remain are also containments** — just
ones the syntactic test cannot derive, because both need `A ⊆ B` with
`B` a compound rather than a bare atom:

```
T(t) ⊆ b(T t)       gives   T(t)·a(T t) = T(t) ^ t&1
N(t & 1) ⊆ U(t)     gives   N(t&1) | U(t) = U(t)
```

So the threshold, in sentence form:

> **Every gap that survives the mask-free representation is a
> containment, and containment is the one thing an ANF engine cannot see
> on principle.** `⊆` reads `A & B = A`; ANF is built on `^`; `^` makes
> the algebra a group; a group admits no compatible order. The order
> facts have to be imported from outside the representation.

That is 0045's Post argument arriving from the other side. There it was
"only the ordering direction loses information". Here it is "only the
ordering direction is invisible to the canonical form" — the same
distinction between the group operation and the lattice operations,
seen once in the semantics and once in the syntax.

## 7. Honest limits

- The rule set is **not complete and is not claimed to be**. 19 of the
  sampled pairs are still unidentified, all classified in §6. Nor is it
  confluent-by-measurement here: 0044's divergence search has not been
  re-run over this representation.
- Meaning-preservation, the prefix analysis and every containment in §6
  are checked against 0047's decision procedure, which is itself
  verified rather than proved. The machine is used **only as an
  oracle**; nothing in the rule set depends on it.
- Single variable throughout.
- `contain` implements a deliberately conservative fragment of `⊆` —
  atom-against-atom only. §6's point is precisely that the natural
  statements need more than that, so the 19 survivors measure the gap
  between "there is an order" and "the representation can name it".
- `unit`'s table and `_under_U` are hand-written and verified
  case-by-case at the listed entries, not derived from the schema.

## 8. Open

1. **Give containment a representation.** The obvious move is to leave
   ANF for the `&`-side — a monomial is already a meet, so a normal form
   that keeps monomials in an antichain under `⊆` would absorb `contain`
   the way ANF absorbs commutativity. Whether that survives contact with
   `^` is the question.
2. **Is `U(t)` provably the top of the `t`-orbit?** §6 measures it on the
   listed operators; a proof would say the `|` cell of 0042's schema is
   the join of the whole orbit by construction, which is nearly its
   definition and ought to be one line.
3. **Re-run 0044 §8's divergence search** over this representation. The
   rule count went from ten to eleven but four of the ten changed
   shape, so the confluence verdict does not carry over.
4. **`!(Ω)` has no finite name.** It is the first object in this
   workstream that is a normal form only because nothing else can be
   said about it. Whether the alternating set deserves a symbol — the
   way 0046 §2 gave the measures one — is open, and it is the same
   question the lasso constants of 0047 §6 were reaching for, now
   restricted to the one case that actually arises.
