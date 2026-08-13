# 0054 — The channel form: rules folded into syntax, and the wall as one property

The user's directive, and it lands: name the hidden channels, write
their defining identities into the sentence as facts, and manipulate
them with more fundamental laws. Rewrite rules dissolve into
substitutions; "the rule list isn't exhaustive" stops being a
criticism because there is no rule list; and what breaks is expressed
by the sentence itself — **one syntactic property, the reference
structure of the hidden channels, separates reducible from
case-split-decidable from unknowable**. Code: `output/channel_form.py`.

---

## 1. The pattern

The carry is not an operator with thirty rules. It is a fresh variable
`c` pinned by an in-sentence fact — the user's identity:

```
c ^ xy ^ x·a(c) ^ y·a(c)          (bit i of c = majority of column i−1)
```

and "x + y = 1" is one polynomial:

```
I := (x ^ y ^ a(c) ^ 1)  |  (c ^ xy ^ x·a(c) ^ y·a(c))
```

`I = 0` iff both disjuncts are — verified exhaustively over 16384
input pairs: empty exactly at the 2 solutions of `x + y = 1`. One
sentence over `{^, &, a, |}` and a hidden wire. This is 0008's
"addition as one hidden wire" and 0019(d)'s hidden-symbol sentences,
now with the *definition* carried inside the statement.

## 2. Guardedness: a syntactic scan that buys a semantic theorem

Call a channel definition **guarded** if every channel reference in it
sits under at least one `a` — a reference to the *past*. Then:

> **A guarded system has exactly one solution.** Bit `i` of every
> channel is a function of bits `< i`, so the definition is a
> contraction in the 2-adic metric and Banach's fixpoint theorem gives
> existence and uniqueness.

Verified on 1000 random systems of 1–3 mutually recursive channels:
the iteration settles, every fact holds, and every single-bit
perturbation of any channel breaks some fact. Guardedness itself is a
one-pass scan of the sentence.

**The operator tier is the guarded-channel tier.** Each schema cell's
fixpoint law (0042 §2) *is* its definition:

```
s = t ^ a(s)          solves to  !(t)
u = t | a(u)          solves to  U(t)
w = t & (a(w) ^ 1)    solves to  T(t)
c = xy ^ (x^y)·a(c)   solves to  C(x,y)
```

## 3. A rewrite rule, derived inside the syntax

0053's `k-one` (`C(t,1) → T(t)`), replayed as a derivation:

```
def_C(x, 1):    c = x·1 ^ x·a(c) ^ 1·a(c)
annihilate:     1·a(c) = 0                    (bit 0 of a shift)
result:         c = x·1 ^ x·a(c)
def_T(x):       w = x·(a(w)^1) = x·a(w) ^ x·1
```

— a **literal match** (machine-checked), so uniqueness of guarded
solutions concludes `c = w`. Substitution, one cancellation, one
meta-principle. No rule engine. `succ` costs a substitution.

## 4. Guarded ⟹ finite-state, and the loop to 0047 closes

A guarded system with k depth-1 channels carries exactly its previous
channel bits as state: at most `2^k` states. Measured: `!`, `U`, `T`,
`C` each hit their bound of 2; the pair `C + !` hits 4. **The
guarded-channel sentences are the finite-state tier** — 0047's machine
was never a separate construction; it is what a guarded sentence
compiles to. Their zero test is decidable, and a nonzero residue after
coalescing is honest contingency: **the known unknown, wearing its
variables**.

## 5. The co-guarded channel: `N`, and why its definition cannot pin it

`N` has no guarded definition (guarded ⟹ LSB-causal; `N` is not —
0045). Its natural definition references the *future*:

```
n = t | h(n)
```

A guarded recursion starts at bit 0 — the boundary exists. A
co-guarded one starts at infinity — the boundary does not. Verified
exhaustively at width 12: solving downward with boundary 0 gives the
down-closure `D(t)`; with boundary 1 it gives `Ω`; **both satisfy
every interior step**. The definition has least and greatest solutions
and cannot choose. And `U(D(t)) = N(t)` for every `t`.

So the pieces line up: `h` was banned as an *operator* (0045); it
returns as a reference *direction*, and one `h`-reference in a channel
definition is the exact syntactic marker of the `N` tier — solutions
non-unique, the 0/Ω guess of 0047's machine being precisely the choice
of solution, decidable by case split, undecidable by causal reduction
(0051's stuck-truth theorem, now visible in the sentence).

## 6. The schema wall: where the fact-list becomes a fact-schema

A guarded system's residual count is bounded by its state count
`2^k`. Multiplication measures `4^p` residuals after `p` bits
(0047 §7), so:

| p | residuals of `x·y` | channels needed |
|---|---|---|
| 1 | 4 | k ≥ 2 |
| 2 | 16 | k ≥ 4 |
| 3 | 64 | k ≥ 6 |
| 4 | 256 | k ≥ 8 |

**Any guarded system computing `x·y` to `p` bits needs `k ≥ 2p`
channels.** The channel list is forced to grow with the precision —
to become a channel *schema*, `c_i` for every `i`, an infinite
fact-family. Co-guarded channels do not rescue it (each adds a finite
solution choice; a finite union of finite-state maps is finite-state).
The school algorithm meets the bound with Θ(p) wires, so it is tight
up to a constant.

That is the wall as an expression:

> **The sentence's fact-list must become a fact-schema.** The moment a
> statement needs "for every position `i`, a channel `c_i` defined
> from `c_{i-1}`", it has left the decidable tier — and quantifying
> over that index is exactly what an induction axiom licenses. In this
> workstream's syntax, the Gödel boundary is the line between a
> conjunction and a schema.

## 7. W4 dissolves: division is a guarded sentence

The opening objection — the rational tier being open means the rules
aren't exhaustive — resolves by dissolving. `x·(1/3)`, stuck in 0053
with no rule, is the implicit fact `3m = x`:

```
fact 1:   x ^ m ^ a(m) ^ a(c)              (3m = m + 2m)
fact 2:   c ^ m·a(m) ^ (m^a(m))·a(c)       (its carry)
```

Two channels, triangular per bit (`m_i` from the past, `c_i` from the
past and `m_i` — the relaxed guardedness: self-references under `a`,
same-position cross-references acyclic). 3 is a 2-adic unit, so a
unique solution exists for **every** `x`; verified on 3000 random
values, `3·m = x` exactly. Division by three, with no division
operator, no lasso constant, no rule.

A rule *list* can never be exhaustive. A *sentence* either has a
finite guarded channel list or it does not — a property of each
statement, checkable by scan, rather than of the system.

## 8. The trichotomy — the single syntactic answer

| channels of the sentence | tier | verdict |
|---|---|---|
| all references past (`a`), finitely many | finite-state | reducible; nonzero residue = contingency (**known unknown**) |
| a future reference (`h`) | `N` tier | non-unique solutions; one case split per channel; reduction alone provably insufficient |
| an indexed family (schema) | product tier | no finite sentence pins the channels (**knowably unknowable by any finite fact-list — and the sentence shows it**) |

"Known unknown" is a guarded residue with variables on display —
decidable instance by instance. "Knowably unknowable" is a sentence
whose channel requirement is visibly infinite or visibly co-directed:
the syntax expresses the break, which is what folding the rules into
the sentence was for.

## 9. Honest limits

- The contraction theorem, the finite-state bound, and the co-guarded
  non-uniqueness are real arguments verified by machine; the schema
  lower bound `k ≥ 2p` rests on 0047's *measured* residuals (p ≤ 4)
  — the standard fooling-set argument extends it to all p, cited not
  re-proved.
- The channel form here evaluates and solves; it does not yet
  *canonicalize* — the coalescing engine of 0048–0053 has not been
  rebuilt over channel sentences. §3 shows one rule becoming a
  derivation; the claim that *all* thirty do is a program, not a
  result.
- Relaxed guardedness (triangular cross-references) is used in §7 and
  verified there; its general theory (acyclicity check, uniqueness
  proof) is stated, not developed.
- `x·y = z` as a *relation* with z free might admit different channel
  structure than `x·y` as a function; the lower bound covers the
  function reading.

## 10. Open

1. **Rebuild the coalescing engine over channel sentences** — rules as
   derived lemmas, cached; the k-one derivation is the template. The
   confluence question then becomes: which lemma applications commute,
   and 0051's certificates should reappear as co-guarded obstructions.
2. **Bounded schemas.** `x·y` needs `2p` channels for `p` bits — so
   any *bounded-width* statement about products is back inside the
   tier. The counted tier (0034–0036) and its Presburger layer likely
   live exactly here: statements whose schema instantiates finitely.
3. **The `h`-tier's algebra.** One co-guarded channel = one case
   split; k of them = 2^k. Is there a normal form with the minimal
   number of co-guarded channels — a measure of how much "N-ness" a
   statement carries? 0047's guard count asked this as a machine
   question; it is now a syntax question.
4. **Induction as a controlled axiom.** §6 says the wall is the
   schema. Admitting one schema with a designated shape (`c_i` from
   `c_{i-1}`, uniformly) and reasoning about it as a single object is
   precisely adding an induction principle — the controlled way to
   step over the line, with the syntax still displaying where the
   step was taken.
