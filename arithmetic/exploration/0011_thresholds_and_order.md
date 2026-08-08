# 0011 — Thresholds and order: locating the boundary precisely

Prompted by two conjectured limits: that the nonemptiness flip does not
generalize to "size of this set is at least 3", and that "greater than"
is inexpressible without an upper bound. **Both conjectures are false**
— machine-checked — and the *actual* boundary sits one step further
out. New constructors in `output/clue_solver.py`
(`cardinality_at_least_statement`, threshold clue events) and
`output/canonical_automata.py` (`statement_of_less_or_equal`).

## Threshold counting: the flip generalizes completely

{h : |h| ≥ k} is regular for every fixed k: a counter that **clamps at
the threshold** and accepts there — k+1 states total, *regardless of
how large the set is*, because the machine never needs to count past
k. Nonemptiness is literally the k = 1 case; "at least 3" is the same
automaton with two more states. Machine-checked (full relation
equality, k = 1, 2, 3):

    at_least(k)  ==  flip( exactly(0) ∪ … ∪ exactly(k−1) )

so the flip view and the counter view coincide — the layer's Boolean
closure makes every threshold, interval, or finite union of counts
expressible against a *fixed* number. Threshold clue events ("they
hold at least two rooms") are implemented via the usual hidden masked
channel and verified against exhaustive ground truth.

## Order needs no bound at all

x ≤ y on numbers is automatic with **2 canonical states**: reading
least-significant-bit first, a later differing bit overrides the
verdict (later = more significant), so the machine only remembers "≤
so far" vs "> so far". (A hand-built 3-state version — equal / less /
greater — minimizes to 2: "equal so far" and "less so far" are
future-indistinguishable. The canonical form found this; I had not.)
Consistently with the basis theorem, it is also *derived* by pure
wiring with one hidden gap wire:

    x ≤ y   ⟺   ∃ gap:  x + gap = y

and the suite checks the wiring derivation collapses to the identical
canonical automaton, sampling 512-bit unbounded values. Strict order,
intervals, min/max relations all follow by the usual moves.

## The boundary, precisely

What made the conjectures feel true is real, but it lives exactly here:

- **Inside the layer**: any count compared against a *constant*
  (=k, ≥k, ≤k, intervals, Boolean combinations); any order or
  arithmetic comparison between *number channels*, unbounded.
- **Outside the layer** (non-regular, pumping / 0001 §4): coupling an
  unbounded **set channel to its own cardinality as a number channel**
  (popcount(A) = n), and comparing **two unbounded cardinalities**
  (|A| ≥ |B|, |A| = |B|). The failure is not thresholds or order — it
  is *unbounded counting*: a machine would need unboundedly many
  states to carry a count it cannot clamp.

The consequence for modeling: sizes may enter as first-class number
channels and be compared freely (that side is all inside), but the tie
between a set and its size channel must be maintained **by
construction** — counter widgets applied per event, bounded-universe
counting, or witness decompositions — never demanded from a size
*operator* on raw sets. In a bounded game the tie is trivially
maintainable (the deck bounds every count, so every count clamps),
which is why finite Clue never feels the boundary; the infinite game
feels exactly it, and nothing else.

## Clue-like reach gained

Games whose clues are threshold-shaped are now directly in scope with
no new theory: "at least two of the named cards", "no more than one
room in hand", "more suspects than weapons in hand — *given either
count is bounded by a known constant*". The unbounded version of that
last clue is the boundary itself.
