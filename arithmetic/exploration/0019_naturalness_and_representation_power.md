# 0019 — Is this basis natural, and is the sentence form ever beaten?

Testing a two-part suspicion: (a) {^, &, <<, 1} is a *natural* basis,
not a convention — an "eigenbasis" for what these statements express;
(b) nothing can do materially better than expand-and-cancel on the
sentence form. Measured in `output/representation_tradeoff.py`.

**Three of the four claims hold. One is false, and precisely where it
is false is informative.**

## (a) The algebra is not a convention — I was too broad in 0014

0014 said the operator/logic split is bookkeeping. That is correct
about *where the line falls between signature and logic*, and it does
not extend to the choice of algebra. Two reasons the algebra is
forced:

**Stone.** Boolean algebras and Boolean *rings* are the same objects,
with ring addition = symmetric difference and multiplication = meet.
So ^ and & are not one functionally complete pair among many — they
are the ring operations a Boolean algebra already carries. Nothing was
chosen.

**Characteristic 2 is forced.** In any commutative ring where every
element is idempotent, (x+x)² = x+x gives 4x = 2x, hence 2x = 0. An
idempotent ring *must* have characteristic 2: every element is its own
additive inverse. So `a ^ a → 0` — the *cancel* step of
expand-and-cancel — is not a rule someone picked. It falls out of
wanting a ring at all.

**And convexity wants a ring.** Cancellation needs additive inverses.
{AND, OR, NOT} has none (union has no inverses) and correspondingly no
unique normal form — CNF and DNF are not canonical. Semantic convexity
therefore *selects* this algebra rather than tolerating it. The
"eigenbasis" intuition formalises as: the ANF monomials are a genuine
linear basis of the 2ⁿ-dimensional GF(2) space of Boolean functions,
expand-and-cancel is coordinate computation in that basis, and
uniqueness of the canonical form is exactly the basis property.

So the naturalness hunch is right, and my earlier framing was too
broad. Corrected in 0014's cross-reference.

## (b) The sentence form is never beaten *as a representation*

Two families, both measured:

| family | expression terms | canonical automaton states |
|---|---|---|
| "at least one of n" | 2ⁿ − 1 | **2** |
| parity(X & (Y << w)) even | **w** | 2^(w+1) |

The second is new and is the decisive one: the automaton must carry w
bits of Y while waiting for the matching bits of X, so its canonical
form is exponential, while the expression is a XOR of w products with
*no hidden symbols at all*. Measured 4, 8, 16, …, 256 states for
w = 1…7, spot-checked against ground truth.

So **ANF and the automaton are incomparable** — each is exponentially
smaller on some family. Neither representation dominates.

But allow hidden symbols and it becomes one-sided:

    automaton → sentence     ALWAYS polynomial   (0015: O(s) hidden
                             symbols, O(s²) atoms, by carrying the run)
    sentence → automaton     sometimes EXPONENTIAL   (the w-family)

> **The sentence form with hidden symbols polynomially simulates the
> canonical automaton and is sometimes exponentially more compact. The
> automaton never wins on size.**

What the automaton wins is not size but *amortisation*: being
canonical, it answers entailment by containment and yields the whole
deduction grid in one sweep (0010). The sentence stays small precisely
by deferring that work.

## (c) "No algorithm can do materially better" — see 0020

> **This section's argument is withdrawn.** It refuted the claim by
> exhibiting one family ("at least one of n") where an automaton beats
> the ANF exponentially. That is a *subclass* argument and does not
> touch a **worst-case** claim — the same move as a sort that is O(1)
> on already-sorted input. The correct comparison is worst-case
> against worst-case, and under it the question splits four ways with
> four different statuses. See **0020**, which supersedes this
> section.

The original text, kept for the record: the strong form is refuted by
the "at least one of n" row above, where a 2-state automaton beats a
2ⁿ−1-term ANF.

The suspicion is right in a weaker and still substantial form:

- **Worst-case complexity class: no advantage exists.** Finite-game
  inference is coNP-complete either way (0018); the general layer is
  non-elementary either way (0017). No representation escapes.
- **Instance-wise: advantages exist in both directions**, and they are
  exponential.

So "materially better" holds asymptotically-in-the-worst-case and
fails per-family. The tie between representation length and algorithm
cost that motivated the suspicion is real *for expand-and-cancel* —
that algorithm is linear in its canonical form — but it is a property
of that algorithm, not of the problem.

## Summary of the four claims

| claim | verdict |
|---|---|
| {^, &, 1} is natural, not convention | **holds** (Stone; characteristic 2 forced; convexity needs a ring) |
| the canonical form is a genuine basis | **holds** (linear basis of the GF(2) function space) |
| the sentence form is never beaten as a representation | **holds** with hidden symbols (poly-simulates the automaton, sometimes exponentially smaller) |
| nothing beats expand-and-cancel materially | **see 0020** — splits four ways; the subclass refutation once given here is withdrawn |

## Open

- Is there a *characterisation* of which relations are exponentially
  smaller as sentences than as automata? The w-family suggests
  "long-range pairings with local structure"; OBDD width theory is the
  obvious place to look.
- ~~Whether a *canonical* sentence form exists is unknown, and would
  be the real prize.~~ **Resolved below — the prize is unavailable.**

## (d) A canonical sentence form exists; a cheap one would give P = NP

The algebra does support expand-and-cancel exactly as claimed, and
this is verified: `<<` distributes over both `^` and `&`, and `&`
distributes over `^`, so every hidden-symbol-free sentence reduces to
a unique XOR of ANDs. ANF *is* a genuine canonical form. The question
the prize turned on was never existence — it was cost.

**3-SAT settles it, in two steps.**

*Canonicalising explodes even when deciding is trivial.* Take 3-CNF
over disjoint triples: each clause has a 7-term ANF, no variables are
shared, so nothing can cancel and the product has exactly 7^m terms —
verified 7, 49, 343, 2401, 16807 for m = 1…5 against 3m literals. And
every one of these formulas is *trivially satisfiable*. So
canonicalisation is not merely as hard as deciding; on this family it
is strictly harder.

*And it cannot be made cheap.* The ANF of a formula is the **zero
polynomial exactly when the formula is unsatisfiable**, so merely
checking whether the canonical form is 0 already decides UNSAT.
Canonicalising a 3-CNF is coNP-hard. Generally: if any canonical
sentence form C were polynomial-time computable, then comparing
C(φ) with C(false) would decide unsatisfiability in polynomial time,
so **P = NP**. Hence

> **canonical + compact + polynomial is unavailable unless P = NP**

and the three representations take their places:

| representation | canonical | compact |
|---|---|---|
| ANF | ✓ | ✗ |
| minimal automaton | ✓ | ✗ |
| sentence with hidden symbols | ✗ | ✓ |

**Where the intuition needs inverting.** The thought was that most of
3-SAT's apparent complexity comes from many representations of one
sentence, and that canonicalising cuts that away leaving the core
problem. The second half is right and the first half is backwards:
canonicalising does not *remove* the difficulty, it is *where the
difficulty lives*. Once a canonical form is in hand every question is
trivial — comparison of coordinate vectors. So the hardness of SAT is
exactly the cost of the change of basis into monomial coordinates.

Which is the eigenbasis analogy holding all the way to the end, and
worth stating as the workstream's compact summary of this thread:

> **The basis that diagonalises everything is also the basis that is
> expensive to reach.** Semantic convexity buys a canonical form in
> which all questions are trivial; it does not and cannot buy a cheap
> route into it.

## Still open

- Is there a *characterisation* of which relations are exponentially
  smaller as sentences than as automata? The w-family suggests
  "long-range pairings with local structure"; OBDD width theory is the
  obvious place to look.
