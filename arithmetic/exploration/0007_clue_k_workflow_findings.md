# 0007 — The K workflow on mini-Clue, hand sizes included: findings

`output/clue_k_workflow.py` runs the framework against its toy problem on
the canonical-automata layer: knowledge K is one canonical automaton over
tracks (A, B, E), updated by intersection, queried by containment. Every
stage is cross-validated against brute-force enumeration of all 64³ =
262,144 deals. Total runtime ≈ 5 s, almost all of it the brute-force
validation, not the automata.

## Setup

Six cards (mustard, plum | knife, pipe | hall, study), Alice holds 2,
Bob holds 1, envelope holds one card per category. K0 asserts: partition
(XOR to the full deck + pairwise disjointness), |A| = 2, |B| = 1, and the
three envelope category constraints. |E| is deliberately *not* asserted.

## Finding 1: cardinality is definable inside the term language

The corpus's original set-size gap closes with no new primitive:

    pow2(y)  :=  ∃w. add(w, 1) = y  ∧  y & w = 0
    |h| = k  :=  ∃p₁…p_k pairwise-disjoint pow2's with h = p₁ ^ ⋯ ^ p_k

The pow2 characterization works because y = w+1 with y & w = 0 forces w
to be all-ones below y's single bit (and y = 0 is impossible as a
successor). Sizes therefore enter through add and projection alone —
the "sizes as additive bookkeeping" claim of 0001 §4, now constructive.
Cost: one existential witness per counted card, fine for constant sizes.

## Finding 2: deduction through sizes works — |E| = 3 was derived

`K0 ⊨ size_is(E, 3)` returns KNOWN TRUE even though no size fact about E
was ever stated: it follows from the partition and |A|, |B|. First
nontrivial arithmetic deduction of the framework on its own toy problem.

## Finding 3: the classic Clue inference chain, mechanically

- Event 1 (Alice passes on plum/knife/hall) and Event 2 (Bob passes on
  the same): K2 knows the *entire envelope* — plum, knife, hall, and
  even `E = {plum, knife, hall}` exactly, because |E| = 3 caps it. The
  accusation is decided two events in, while the players' hands are
  still uncertain.
- One-sidedness, concretely: at K2, "mustard in A" is unknown AND
  "mustard not in A" is unknown (three deals remain, split both ways),
  while "mustard not in E" is KNOWN TRUE. Exactly the
  true/converse/neither trichotomy the framework promises.
- Event 3 (Bob shows the pipe) forces everything: unique consistent
  deal, all three hands entailed exactly.

## Finding 4: knowledge compresses the automaton

| stage | canonical states | consistent deals |
|---|---|---|
| K0 | 17 | 24 |
| K1 | 16 | 6 |
| K2 | 13 | 3 |
| K3 | 8 | 1 |

More knowledge → smaller canonical object, monotonically, in this run.
That is *not* a theorem (canonical size is description complexity, not
model count; intersections can enlarge automata in general) but it is
suggestive: in this workflow the canonical form behaves like a knowledge
state, not like a growing log of assertions. Worth watching whether
monotone-shrinkage has a characterization (candidate connection: K's
updates here are all conjunctions with "simple" facts whose canonical
forms are small).

## Finding 5: the alpha-map, checked exactly

At every stage the automaton's accepted deal-set equals the brute-force
model set — 262,144 checks × 4 stages, zero disagreements. For this
finite instance the Galois alpha-map of the symbolic layer is verified
extensionally, not just argued.

## Honest limits observed

- Everything here is the *finite* game; tracks are 6 bits. The ω-side
  canonicity question (0005 §3, 0006) is untouched.
- Witness-per-card sizing is constant-k only. "All hands have equal
  size" (unknown k) would need genuine Presburger counting over the
  automatic layer — fine in principle, not yet built.
- The suggestion/refutation event "Bob showed *some* card from
  {plum, knife, hall}" (card unseen) is a disjunctive fact. On this
  layer it is representable directly — the union of the three automata,
  i.e. ¬(B∩{p,k,h} = ∅) as an automaton — but note what that means for
  the term algebra: the automata layer absorbs disjunction through its
  Boolean closure, the term layer still cannot write it (0005 §1, path
  declined pending closed ×). The K workflow is agnostic: any automaton
  can be intersected in.

## Files

- `output/clue_k_workflow.py` — the runnable workflow (seed-free,
  deterministic).
