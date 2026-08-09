# 0034 — Set construction: the game that forces it, the wall it hits, and the tier that carries it

Asked for: the `2**n` set-construction operator brought to fruition,
motivated first by a game that cannot be solved without it.

Answer in one line: **the operator is the size operator, one game axiom
forces it, unguarded it is Gödel, and the guard is a scale rule —
counters may talk to counters, never to values.**

Code: `output/level_crossing.py`, `output/infinite_clue.py`. Both run
directly; every number below is printed by one of them.

---

## 1. Why the clue workstream ended early

Boundedness is a complete escape from set construction, and finite Clue
is bounded.

On a known deck every hand size is a known constant. A constant size is
a clamped counter, and 0011 proved clamped counters regular — `|h| ≥ k`
costs `k+1` states with no bound on the set. 0007 then did the same job
inside the term language with no new primitive at all (`pow2(y) := ∃w.
add(w,1) = y ∧ y & w = 0`, and `|h| = k` as `k` disjoint `pow2`
witnesses). Neither route needs `{x}`. The operator never came up
because the bound was doing its work silently.

So the expectation was not wrong, it was *conditional*: set
construction is exactly what the boundedness assumption was hiding.
Remove the bound and it reappears immediately, and only there.

## 2. The game: Infinite Clue

Cards are the naturals; card `i` has category `i mod 3` (suspect /
weapon / room). A deal gives the envelope exactly one card of each
category and splits the rest between two players. The cards actually
dealt are an initial segment `[0, N)` and **`N` is not announced**. The
dealing rule is the one real Clue uses: the two hands are equal in size.
You are a spectator — you hold no cards and learn only public events: a
player passing on a suggestion (holds none of three cards) or refuting
one (holds at least one of three).

Every axiom is a layer statement except one. Measured minimal automata
over the three channels `(E, H1, H2)`:

| axiom | in the layer |
|---|---|
| pairwise disjoint | 2 states |
| dealt set is an initial segment | 3 states |
| one envelope card per category | 9 states |
| every pass, every refutation | `card + 3` states each |
| **`\|H1\| = \|H2\|`** | **no DFA** |

**Forcing.** The balance relation is not automatic. Its Myhill–Nerode
index is the running difference of the two counts, which is unbounded;
`residual_growth` measures distinct residuals by prefix length as
`1, 3, 5, 7, 9, 11, 13` for `|A| = |B|` and `1, 4, 7, 9, 11, 13, 15` for
the partition-of-an-initial-segment form. Both strictly increase, so no
DFA serves either, and — modulo Büchi–Bruyère, as in 0008 — the layer
*is* the automatic relations, so the rule is not expressible in the
layer at all, in any presentation.

**And no clamp substitutes.** The obvious repair is 0011's clamped
counter: count both hands up to `k` and require the clamped counts to
agree. That is sound (every balanced deal is accepted) and it is the
best regular over-approximation at clamp `k`. The measured result is a
clean diagonal — scale `m` of the game against clamp `k`:

```
scale  clamp 1 clamp 2 clamp 3 clamp 4
    1    exact   exact   exact   exact
    2     lost   exact   exact   exact
    3     lost    lost   exact   exact
    4     lost    lost    lost   exact
```

A clamp of `k` decides the game at scale `k` and loses it at `k+1`. The
game at scale `m` is the same game with `m` cards per pass; the
deduction it needs is a **bootstrap** between the balance rule and the
initial-segment rule — cards `3..3+m` land in `H2`, so `|H2| ≥ m`, so
`|H1| ≥ m`, so `N ≥ 3+2m`, so the next `m` cards are dealt and land in
`H1`. Each round of that loop advances a counter by one, so any fixed
clamp is defeated by making the game one card bigger.

**Nor does a moving or per-instance clamp.** Three readings of the
repair, and each closes:

- *A clamp that re-centres* — track the difference `|H1| − |H2|` and
  clamp that instead. Already foreclosed: the residual measurement above
  is precisely a measurement of the difference (its `2k+1` growth is the
  count of reachable differences at depth `k`). Remembering a bounded
  amount about the difference is exactly what fails.
- *A clamp that grows with the input* — then it is not a DFA, it is a
  counter, and that is not a rival proposal; it is this one.
- *A clamp recomputed large enough per instance* — possible, and it
  loses three things the framework requires. Measured on one game, with
  clues arriving one at a time:

```
clues  control states  cells known  minimal adequate clamp
    2               6           17                       0
    3              10           21                       0
    4              10           25                       1
    5              14           33                       4
```

  (1) **The bound is not compositional and moves on every event.** The
  balance axiom is literally the same object in all four rows; the clamp
  it needs is a property of the accumulated conjunction, so it cannot be
  attached to the axiom, and the K-workflow must recompute and rebuild
  at each event rather than intersecting. The counted tier carries the
  same two counters unchanged throughout.
  (2) **`unknown` becomes indistinguishable from `clamp too small`.** A
  clamp is a sound over-approximation — it can only lose verdicts, never
  invent them — so clamping turns the system into a semi-decision
  procedure for *known* with no stopping rule for *not known*. That is
  the founding requirement of the framework, not a convenience: the
  corpus asks for "I know this is true" or "I don't know that this is
  true" as *reached* verdicts.
  (3) **No canonical form.** The clamp depends on how the axiom is
  written — the union presentation of §6 reaches twice the counter value
  of the direct one on the same deals, so a clamp adequate for one is
  inadequate for the other. The tier's configuration quotient gives the
  two presentations identical signatures.

**What it buys, on a worked script.** Public events: `H1` passes
`{0,1,2}`, `H2` passes `{0,1,2}`, `H1` passes `{3,4,5}`, `H2` refutes
`{3,4,5}`, `H2` passes `{6,7,8}`.

```
layer only (no balance axiom)              counted tier (balance in force)
card   0   1   2   3   4   5   6   7   8   card   0   1   2   3   4   5   6   7   8
  E   in  in  in out out out out out out     E   in  in  in out out out out out out
 H1  out out out out out out   ?   ?   ?    H1  out out out out out out  in  in  in
 H2  out out out  in   ?   ?  out out out   H2  out out out  in  in  in out out out
```

Five cells decided only with the balance axiom. Every verdict on both
sides is cross-validated against brute-force enumeration of all legal
deals at `N ≤ 9, 11, 13` (1/6, 3/12, 9/36 deals with/without balance):
zero disagreements. Verdicts are reported at two counter windows (5 and
9) and agree.

Answer to the original expectation, precisely: **not every move needs
the operator — exactly one axiom does.** But that axiom is the dealing
rule, so every deduction in the game routes through it, which is what
the clamp diagonal shows.

## 3. The operator the game demands is the operator that was expected

The corpus wanted `{x}` ("the set containing x", i.e. `2^x`) and
separately flagged set sizes as the framework's limitation. Those are
one operator, not two:

```
y = 2^x   iff   |y| = 1  and  |y-1| = x
```

Verified forward for `x < 300` and conversely for `y < 2^16`, with no
failures. The definition uses the size operator and predecessor and
nothing else, both of which the layer has apart from the size operator
itself. The converse direction (size from set construction) holds
because `{.}` *is* the BIT relation — see §4 — and BIT interprets full
arithmetic, in which the Hamming weight is definable.

So: the operator the corpus expected on aesthetic grounds and the
operator Infinite Clue forces on structural grounds are the same object.
That coincidence is the reason to trust the target.

**Corpus correction.** `clue/2025-04-04` records three level-map lines.
`2A = 2 ** PLUS1(LOG2(A))` is an identity — `E(x+1) = 2·E(x)`, the level
map carries the coarse successor to the fine doubling — checked to
`x < 200`. The other two, `XOR(A,B) = 2 ** XOR(LOG2 A, LOG2 B)` and the
`AND` line, are **not** laws of `^` and `&`: first witnesses `a=b=0`
gives `E(0)^E(0) = 0` against `E(0^0) = 1`, and `a=0,b=1` gives
`E(0)&E(1) = 0` against `E(0&1) = 1`. They are definitions of the
*lifted* operators by conjugation, which is a different and still useful
thing — but only the successor line constrains the existing operators.

## 4. Unguarded, the operator is Gödel

With `{.}` available, top-level membership becomes hereditary membership:

```
p ∈ X   iff   {p} & X ≠ 0
```

verified for `p < 6, X < 64`. That relation is Ackermann's BIT, and `(ℕ,
BIT)` is the Ackermann coding of `(V_ω, ∈)`, which is bi-interpretable
with `(ℕ, +, ×)` — classical, cited not reproduced. BIT needs no further
operator to iterate: `x ∈ y ∈ z` is two uses of one relation.

So **Th(layer + `{.}`) is undecidable**, and by 0001's argument (a convex
syntax decides truth) *no convex syntax can carry the unguarded
operator, ever.* This sits strictly below the ceiling 0001 located: that
one needed Matiyasevich and the ∃-fragment of `(ℕ,+,×)`; this one needs
one binary relation and no arithmetic operator at all.

This is the reason 0005's "guarded convexity" frame was the right guess.
It is also why the answer cannot be "add the operator and see" — the
question is only ever *which restriction*.

## 5. The guard is a scale rule

Where does the strength enter? Not from counting, and not from set
construction as a syntactic shape. It enters at one comparison.

A counter is bounded by the length of the word. A value is exponential
in the length of the word. The two live at scales separated by exactly
the level map `E(x) = 2^x`. Therefore:

- **counter against counter** — `|H1| = |H2|`, any Presburger condition
  on the counters — costs nothing. The automaton carries the counters
  alongside its control state and never has to reconcile scales.
- **counter against value** — `|y-1| = x` for a channel `x` — is the
  level crossing itself, and by §3 and §4 it is full arithmetic.

That single comparison is the entire difference between a decidable tier
and true arithmetic. It also explains 0011's boundary in its own terms:
0011 found the true limit to be "coupling an unbounded set channel to
its own cardinality channel", which is exactly counter-against-value.

Read structurally: the framework has two levels, a fine level where sets
live at unary scale and a coarse level where counts live at binary
scale, and `{.}` is the interface. The convex system is the pair of
levels with a one-way interface — sets may be counted downward; counts
may not be turned back into sets upward. That is 0009's "level crossing"
path, and the direction restriction is what makes it work.

## 6. The tier, implemented

`CountedAutomaton` (in `output/level_crossing.py`) is a **deterministic
Parikh automaton** over the layer's own bit columns. Each counted
channel carries one counter incremented by that channel's bit, so a
counter is a monoid homomorphism of the input word — in particular it is
invariant under the layer's zero padding, which is why counted and
uncounted statements compose with no alignment bookkeeping. Acceptance
is a per-state Presburger predicate on the counters.

What it has:

- **Intersection, union, and complement.** Complement is free *because
  the machine is deterministic*: one run per word, so complementing only
  negates the acceptance predicate. The nondeterministic Parikh class
  has no such move — its universality problem is undecidable (cited:
  Ibarra on reversal-bounded counter machines; Klaedtke–Rueß). Machine
  checked at two windows: `A ∧ ¬A` empty, `A ∨ ¬A` universal,
  `|A|=|B|` entails `¬(|A|>|B|)`, neither of `|A|=|B|`, `|A|>|B|`
  entails the other, and their conjunction is empty.
- **Decidable entailment**, so the deduction test `K ⊨ H` survives
  unchanged. The three-valued game verdict is unchanged too — `K` may
  entail neither `H` nor `¬H`, which is the framework's usual
  one-sidedness, now sitting on top of a decidable relation rather than
  replacing it.
- **A canonical form.** The Myhill–Nerode quotient of the configuration
  space (control states × counter vectors). Tested the way 0006 tested
  the layer: `|H1| = |H2|` and `∃U. U = H1^H2 ∧ |U| = 2|H1|` are
  unrelated presentations of the same relation, and reduce to canonical
  forms with identical signatures (26 configurations each at window 4).

**Window semantics, stated exactly.** Counters never decrease, so
`is_empty(window)` means "no witness whose every counter stays at or
below `window`" — a precise finite relation, not an approximation of
one. Every verdict asserted by either module is reported at two windows.
The general procedure is Presburger satisfiability over the Parikh image
of the underlying DFA (Verma–Seidl–Schwentick; Klaedtke–Rueß); it is
cited, not implemented.

**A window is not a clamp**, and the distinction is worth stating
because the implementation uses one. A clamp changes the *object*:
`clamped_balance(k)` is a different relation from balance — it admits
unbalanced deals — so it is baked into whatever gets canonicalised. A
window changes only the *search* for a witness, over an object that
stays exact at every size. The failure directions are therefore
opposite: a clamp loses verdicts (sound, incomplete), a window can
invent them (complete, unsound if a witness lies past it). And they have
different repairs — the window's is the canonicity step of §8, which
computes the semilinear threshold and removes it; the clamp has none,
because no clamp is the relation.

## 7. The exclusion: you may not count what you freely hide

The tier is closed under the Boolean operations but *not* under hiding a
counted channel, and the implementation enforces this by measurement
rather than by decree. `existentially_projected` does the subset
construction over configurations and checks that every reachable subset
agrees on the hidden counter; if it does not, it raises with the witness
word:

```
hide a counted, genuinely free channel (H ⊆ X, |H| = 2):  REFUSED
  hiding 'H' leaves its counter undetermined ([0, 1]) after {'X': 1}
hide an uncounted channel:                                allowed
hide a counted but functionally determined channel:       allowed
```

The third line is the useful refinement: **a hidden channel may carry a
counter exactly when it is pinned by the visible ones** — 0008's
uniquely-determined wire, now carrying a counter. Verified by canonical
form: hiding `C` from `C = A ∧ |C| = 3` gives the identical canonical
object as counting `A` directly.

Two things worth noting about the shape of this exclusion:

- It **mirrors 0016 exactly**. There, hidden channels were free on the
  knowledge side and not on the hypothesis side, because `∀C(K(C) → H) ≡
  (∃C K(C)) → H`. The same asymmetry applies here for the same reason:
  `K ⊨ H` needs the complement of `H`, not of `K`, so a counted channel
  may be hidden inside knowledge (emptiness of a *nondeterministic*
  Parikh automaton is still decidable) and may not be hidden inside a
  hypothesis. The count channel obeys the Tseitin channel's law.
- It is an **inversion** of the layer's economics. In the layer, hiding
  was the powerful move and negation was tradeable for one relation
  (0015). At the counted tier, negation is free and hiding is the
  dangerous move. The two levels pay for opposite things.

**Infinite Clue lands inside the guard**, and not by luck: the sets a
Clue player counts are the hands, and the hands are the named channels.
The game counts what it names.

## 8. Ledger

Proved and machine-checked here:

- `y = 2^x ⟺ |y| = 1 ∧ |y-1| = x` (both directions, exhaustive in range).
- `{p} & X ≠ 0` is BIT.
- The balance relation has unbounded Myhill–Nerode index, in two forms.
- The clamp diagonal: clamp `k` decides scale `k`, loses scale `k+1`.
- Deterministic Parikh automata are closed under `∧`, `∨`, `¬`
  (argument: one run per word; checked at two windows).
- Presentation-independence of the canonical form on the balance rule.
- The hiding guard, with witnesses on all three cases.
- Infinite Clue solved, cross-validated against brute force at three
  deck bounds with and without balance, zero disagreements.

Classical, cited not reproduced:

- `(ℕ, BIT) ≅ (V_ω, ∈)` bi-interpretable with `(ℕ, +, ×)` (Ackermann),
  hence undecidable.
- Emptiness of Parikh automata is decidable via semilinearity of the
  Parikh image (Parikh; Verma–Seidl–Schwentick).
- Nondeterministic Parikh automata: universality undecidable, no
  complement (Ibarra; Klaedtke–Rueß).
- The layer is exactly the automatic relations (Büchi–Bruyère), which is
  what upgrades "no DFA" to "not expressible".

Argued but not verified — the load-bearing open step:

- **Canonicity off the window.** The Nerode congruence on configurations
  should be Presburger-definable and decidable: `(q,v) ~ (q',v')` iff
  `∀(s,s',w) ∈ R. Acc_s(v+w) ↔ Acc_{s'}(v'+w)`, where `R` is the
  Parikh-indexed reachability relation of the product automaton, which
  is semilinear and computable. If that goes through, the counted tier
  has a genuine canonical form — an infinite but finitely-presented
  automaton — and is convex in the workstream's sense rather than only
  window-convex. Only the windowed version is implemented.

Limitations of the implementation, not of the tier:

- Counters are per-channel homomorphisms (increment = the channel's
  bit). Counting a *category-restricted* set needs either a derived
  channel pinned by a layer constraint (legal, and demonstrated) or
  transition-labelled increments (the general Parikh definition, not
  implemented).
- Two players. Three or more players balanced pairwise is `p-1`
  counters and the same machinery, at `(window+1)^(p-1)` configurations
  per control state.

## 9. Where this goes next

1. **Close the canonicity step** of §8. That converts "decidable tier"
   into "convex tier" and is the last thing between this and the
   framework's own standard.
2. **The upward direction.** Everything here uses the level map
   downward. Genuine exponentiation statements (`y = 2^x` as an
   *object*, 0009's path 1 and the whole of the exponentiation prize)
   need the coarse level to be a second automaton, not a counter vector
   — counters are the abelian shadow of the coarse level. The natural
   next object is a pair of automata joined by the level map, with the
   §5 scale rule as the interface discipline.
3. **The ω-extension** (SUMMARY next-step 4) is now the only remaining
   piece of "infinite Clue" that this does not touch: unbounded decks
   are handled, genuinely infinite plays are not.
4. **Where the counted tier sits in the 0026–0033 frame taxonomy.** It
   is a new kind — not a Kronecker frame, since its state space is
   infinite and semilinear rather than a product over coordinates. The
   finite-frame conjecture of 0028 was stated over the product
   structure; the counted tier is the first natural object outside it,
   and whether it refutes or merely extends that conjecture is open.
