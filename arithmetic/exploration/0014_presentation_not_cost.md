# 0014 — The operator/logic split is presentation, not cost

Correction to how 0013 framed its own result. 0013 treated the wiring
moves (share, hide, flip) as free and the base relations (&, <<) as
the costly ingredients, and reported "the minimal basis is {&, <<}"
as if that were an absolute fact about the layer. **It is not.** The
line between "signature" and "logic" is a bookkeeping choice, and
moving it moves the basis. The results of 0013 are all still correct;
their *status* changes from absolute to presentation-relative, and the
presentation-independent content has to be stated differently.

## The demonstration: flip is worth one relation

0013's headline was that XOR needs flip, because it needs superlatives
("the largest z inside x that misses y"). Put relative complement into
the signature instead, and XOR is reachable with **no negation at
all** — share and hide only (verified, `closure_hierarchy.py`):

    z = x ∪ y   ⟺  x ⊆ z ∧ y ⊆ z ∧ ∃w (w = z \ x ∧ w ⊆ y)
    z = x ^ y   ⟺  ∃p ∃q (p = x \ y ∧ q = y \ x ∧ z = p ∪ q)

So flip's contribution *in this instance* is exactly one relation's
worth. It is not a different kind of ingredient — it is the same kind,
accounted for on the other side of the ledger.

## The demonstration in the other direction: this layer is WS1S

The same layer, presented as weak monadic second-order logic of one
successor, has signature {membership, successor-of-position} and **no
set operators at all**:

- intersection becomes the logic's own ∧ applied to membership atoms:
  Z = X ∩ Y is ∀p (p ∈ Z ↔ (p ∈ X ∧ p ∈ Y));
- the shift becomes the successor relation of the underlying word
  structure: Z = X << 1 is ∀p (p ∈ Z ↔ ∃q (q ∈ X ∧ p = S(q))).

Both of "our" generators have crossed the line into the logic. Same
closed class of relations, entirely different split. That is as
direct a refutation of the free/costly framing as one could ask for.

## What is actually presentation-independent

Two things survive any re-drawing of the line:

1. **The closed class itself** — the automatic relations. That is the
   one semantic object. Every "basis" is a presentation *of* it.
2. **The obstructions.** Each is a property closed under the
   relevant construction, so anything built entirely from ingredients
   having it also has it. Any presentation whatsoever must therefore
   include ingredients that break, *somewhere among them*:

   | obstruction | what is unreachable without breaking it |
   |---|---|
   | monotonicity | XOR |
   | intersection-closure | XOR, and union |
   | permutation invariance | any notion of bit position |
   | stability | order, addition, all arithmetic |

   **Who breaks them — an operator, a connective, or a quantifier —
   is convention. That they must be broken is not.**

So the honest statement of 0013's theorem is:

> In the presentation where the signature holds relations and the
> logic holds {∧, ∃, ¬, =}, the minimal signature is {&, <<} plus
> constants. Under a different split the minimal signature differs;
> what does not differ is that the ingredients, taken together, must
> break permutation invariance and stability.

The three-level table of 0013 then reads correctly not as
free-versus-costly but as a **budget split**: the more the logic is
given, the less the signature needs. Conservation, not discount.

## Correction also made to 0013's citation

0013 said polymorphisms are "a complete invariant for
pp-definability", citing Geiger and Bodnarchuk–Kalužnin–Kotov–Romov.
That Galois correspondence is a **finite-domain** theorem; our domain
(finite subsets of ℕ) is infinite, where the correspondence needs
local closure and does not transfer as stated. Every negative result
in 0013 uses only the *easy* direction — the preservation lemma,
proved inline and valid over any domain — so the results stand; the
completeness claim has been withdrawn to a mention of Pol–Inv as the
general form of the corpus's own symmetry observation.

## Open, and sharpened by this reframing — now ANSWERED in 0015

Can flip *always* be traded, not just in the XOR instance? I.e. is
there a finite set of relations R with
pp-closure(base ∪ R) = FO-closure(base) = all automatic relations?

**Yes.** R = {^-graph} suffices: every automatic relation is
pp-definable from {&, ^, <<, 0, 1} by carrying the target automaton's
run in hidden channels bounded by a hidden finite horizon (0015,
machine-verified with negation physically disabled). So negation is
fully eliminable from this layer's presentation and the levels are
pure accounting, exactly as this file argued. The exchange rate is
one relation: holding {&, <<, constants} fixed, ^ in the signature
and flip in the logic buy the same thing.
