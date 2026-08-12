# 0052 — Multiplication as a series, and the products schema behind it

Asked: express multiplication by infinite series of the existing
primitives, and see what the new useful series are. This is the
expression step only — 0050/0051 settled that the useful rewrite
direction is coalescing, not expanding, and no rewrite system is built
here. Code: `output/the_products_schema.py`.

The short answer: **one new constructor and one new row.** The
constructor is the guarded diagonal family

```
t_i  =  a^i(x) & N(a^i(1) & y)
```

and multiplication is its `+`-join. Folding the *same* family with the
other three joins gives three more products, 0042's unary schema turns
out to be the `y = Ω` column of the four, and the `+` join completes
0042's table with a row whose two cells are negation and complement.

---

## 1. The decomposition is forced, and it is a series

The natural recursion for `x·y` peels `y`'s low bit — the banned right
shift (0045). What remains is the externally indexed family: the `i`-th
partial product is `a^i(x)`, switched on by `N(a^i(1) & y)`, which is
`Ω` or `0` — **`N` as scalar**. The shift is *diagonal*: `a` advances
the accumuland `a^i(x)` and the probe `a^i(1)` together. Two tracks,
one shift, no new primitive operation. Then

```
x · y  =  Σ⁺_i  a^i(x) & N(a^i(1) & y)
```

exact — exhaustively to 128×128 and on 4000 random pairs at width 16 —
with `Σ⁺` the carry-addition of 0050, so every carry inside is the
guarded-shift `|` cell. Multiplication by a **constant** needs no `N`
at all: the guards evaluate, leaving a finite `+`-fold of shifts (and
`a`/`b`-chain recursion: `x·a(y) = a(x·y)`, `x·b(y) = a(x·y) + x`).

## 2. Four joins, four products

The same family under each join, each verified against an independent
definition (1500 pairs):

| join | product | independent definition |
|---|---|---|
| `^` | carryless product `x⊗y` | GF(2) convolution of the bit sequences |
| `\|` | Minkowski sum `x⊞y` | `{ i+j : i ∈ x, j ∈ y }` |
| `&` | erosion `x⊖y` | `{ k : k−i ∈ x for all i ∈ y }` |
| `+` | **multiplication** | `x·y` |

For `&` the guard dualises — an absent term is `Ω`, the join's
identity, not `0`. Dilation (`⊞`) and erosion (`⊖`) are mathematical
morphology's classical pair; multiplication sits beside them as the
`+` case of the same construction.

## 3. The unary schema is the Ω-column

At `y = Ω` (2000 random `x`):

```
x ⊗ Ω  =  !(x)          x ⊖ Ω  =  0     (0042's "dead" (&,a) cell)
x ⊞ Ω  =  U(x)          x · Ω  =  -x    (2-adic: Ω = −1)
```

and with the `b`-fill, the erosion at `Ω` is `T(x)` — 0042's `b` column
is the same schema with the other fill. **The unary series were never a
separate species: each is its product evaluated at the universe**, and
the `(&, a) = 0` cell stops being a degenerate corner — it is erosion
by an infinite structuring set.

## 4. The `+` row completes 0042's table

The fixpoint equations of the fourth join solve algebraically:

```
S = x + a(S)   ⟹   S − 2S = x   ⟹   S = −x       (negation)
S = x + b(S)   ⟹   S = −x − 1   =  ¬x            (complement)
```

Both identities exact at width 18; the iteration from 0 stabilises one
low bit per step (2-adic convergence).

| join \ shift | a | b |
|---|---|---|
| `^` | `!` | divergent |
| `\|` | `U` | `Ω` |
| `&` | `0` | `T` |
| `+` | **`−x`** | **`¬x`** |

The `+` row is a group join like `^`: invertible, nothing absorbing,
telescoping exact (`S − a(S) = x` *is* the defining equation). Its
cells are old friends — complement, which previously needed
`Ω = N(b 0)`, is a **cell**. And since `Ω = −1`, the constant tier and
the operator tier meet in the 2-adics:

**Lassos are the odd-denominator rationals.** `(10)^ω = −1/3`,
`(1000)^ω = −1/15`, `(01)^ω = −2/3`, `Ω = −1` — each verified as
`q·pattern ≡ p (mod 2^24)`. So 0047's lasso constants are `ℚ` with odd
denominator read 2-adically, and the constant tier is closed under all
four products.

## 5. The laws lift from the schema

- **Distribution is diagonal, in the x track**:
  `(x₁ J x₂) P y = (x₁ P y) J (x₂ P y)` exactly when `J` is `P`'s own
  join, and for no other pair — the full 4×4 table measured, diagonal
  clean, every off-diagonal broken. 0042 §2's "over its own join and
  no other", lifted verbatim. In the y track the three commutative
  products inherit it; erosion instead **anti-distributes**
  (`x⊖(y|z) = (x⊖y)&(x⊖z)`, the morphology duality).
- **`1` is the unit of all four**; `a` is a homomorphism in each
  argument. `⊗`, `⊞`, `·` commute; `⊖` does not (the dual guard breaks
  the family's symmetry).
- **`N` is multiplicative**: `N(x P y) = N(x) & N(y)` for `⊗`, `⊞`,
  `·` — three domains (GF(2)[t], set addition, ℤ₂), no zero divisors.
  A *ring-homomorphism* law for the operator 0051 proved cannot be
  expanded, where all its previous laws were lattice-shaped.

## 6. The new named series a coalescing system will want

Summing the family needs the carry. Two terms need `(p, g) =
(x^y, x&y)`; three need

```
x + y + z  =  (x ^ y ^ z)  +  a( xy ^ xz ^ yz )
```

(3000 triples, exact) — **the majority walks in as the 3-ary carry**,
and it is Post's monotone self-dual clone arriving on schedule. Folding
the whole family through this 3→2 reduction is the Wallace-tree shape
of multiplication. So the candidate named series for the coalescing
system are the layer operators: `e₁` = parity of the family (which is
`⊗` itself — the carryless product is multiplication's linear layer)
and the majority-carry layers above it.

## 7. Where the wall sits now

Residual counts (0047 §7's measurement), tails of 4 bits:

| prefix read | `x⊗y` | `x⊞y` | `x⊖y` | `x·y` |
|---|---|---|---|---|
| 1 | 4 | 4 | 4 | 4 |
| 2 | 16 | 16 | 16 | 16 |
| 3 | 64 | 64 | 64 | 64 |
| 4 | 256 | 256 | 256 | 256 |

**All four products cross the bounded-state wall, at the same measured
rate** (at these parameters — no asymptotic claim). The wall was never
`+` versus `·`: it is unary series versus binary products, in every
join. And every constant slice returns inside: `x → c·x` has **exactly
`c` residual classes** for odd `c` (3, 5, 7, 11, 21 measured) — the
carry is bounded by the constant.

So the decidable tier, stated in product language: the schema, its
products with one argument a lasso, and their compositions. The
variable-times-variable products — all four — are the other side.

## 8. Honest limits

- Everything here is numeric verification at widths 10–26 plus exact
  algebra (`S = x + 2S ⟹ S = −x` is arithmetic, not sampling). No
  claim is proved for all widths; no term-level rewrite system is
  built, deliberately.
- §7's identical residual counts are measured at one width and tail;
  the four products need not stay equal asymptotically.
- The `⊖` product's laws are stated for the guard-dualised definition
  the family forces; morphology's usual reflected-structuring-element
  conventions differ by a mirror this signature cannot express
  (negative shifts).
- "Lassos are the rationals" is verified on four witnesses and argued
  from the standard 2-adic fact, not developed.

## 9. Open

1. **The coalescing system for `·`.** The expression step is done; the
   rewrite step should follow 0050/0051's lesson (coalesce, never
   expand) with `N-fold`-style contractions. §6 says its new symbols
   are `⊗` and the majority layers; §5's diagonal distribution and
   `N`-multiplicativity are its first laws.
2. **The fourth row's b-cell divergence.** `(^, b)` diverges in 0042's
   table; whether the `(+, ·)` products over b-fill families give
   subtraction-with-borrow structure (the borrow is the b-fill carry)
   is unexplored.
3. **Guarded products.** 0050 widened the shift to `σ_{p,q}`; the same
   widening applied to the product family (`t_i` guarded by an
   arbitrary set-valued schedule, not `a^i(1)&y`) covers division-like
   and remainder-like operators, and is where the counted tier
   (0034–0036) should reconnect.
4. **The 2-adic reading as an organizing principle.** `Ω = −1`, lassos
   = ℚ_odd, `N` multiplicative because ℤ₂ is a domain. Whether the
   whole corpus reads more simply as "subsets of ℕ = ℤ₂, statements =
   zero tests" deserves its own pass — 0001's Zhegalkin positioning
   was the GF(2) half of this; the carry side is the other half.
