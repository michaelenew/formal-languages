# 0010 — Finite Clue-like games: solved mechanically

The original problem statement — *the most you can deduce from any
given set of information in Clue* — is now met for finite games, on the
canonical automata layer, with real game mechanics. Implementation:
`output/clue_solver.py` (generic over deck/categories/players); the
suite plays a compact 12-card game and **full-size 21-card Clue**
(6 suspects, 6 weapons, 9 rooms, three 6-card hands) to a verified
accusation.

## What "solved" means here, exactly

After every event, the solver produces the complete deduction grid:
for every card and every hand (players + envelope), a three-valued
verdict — KNOWN IN / KNOWN OUT / unknown — that *provably matches the
semantics*: KNOWN means it holds in every deal consistent with the
information so far; unknown means consistent deals genuinely disagree.
That is the framework's convexity promise (true / undecided, exactly)
delivered at game scale, mechanically, with no cleverness anywhere in
the loop.

## The event that used to be impossible

Real Clue turns on the **unseen refutation**: a player shows someone
else a card, so all you learn is "they hold at least one of the three
named cards." That is a *nonemptiness* fact — exactly the kind of
statement the original expression algebra could not represent (0005
§1: assertions there are emptiness-shaped). On the automata layer it
is one line: the flip move applied to "holds none". The layer's
Boolean closure — which exists because the judgment already needed
flip — closes precisely the representational gap that blocked the
corpus. Also implemented: passes (holds-none), seen refutations
(holds-card), own hand, all honest per table order.

## "The most you can deduce" is one linear sweep

The naive loop is one entailment query per grid cell per round
(84 cells × 2 directions for full-size). Instead, a single
forward/backward reachability pass over K at deck-width word length
yields **every cell's verdict at once**: cell (card i, hand h) is
KNOWN IN iff no consistent path uses a column with h's bit clear at
position i, and the same pass (run with counts instead of booleans)
gives the **exact number of consistent deals** with no enumeration.
Cost: O(states × deck size × alphabet). Exhaustive deduction is a
linear scan of the canonical form — the canonical object is not just
a decision procedure, it is a *survey* structure. Spot-checks assert
the sweep agrees with the entailment test cell-by-cell every round.

## Measurements (seeded, reproducible)

- Compact 12-card game: solved in 8 rounds, ~1 s total; K peaked at
  52 states and shrank monotonically to 14.
- **Full-size 21-card Clue: solved in 8 rounds, ~5 s total.** K
  peaked at **145 canonical states while tracking 110,880 consistent
  deals** (round 1) — a ~760:1 compression of the possibility space
  into its description, before any information beyond the setup and
  the observer's own hand. End state: 29 states, 3 deals, envelope
  fully identified while 6 hand-cells remained unknown — the solver
  correctly separates "accusation known" from "everything known".
- Canonical size again shrank monotonically with knowledge in every
  observed run (cf. 0007's observation; still unproven in general).

Validations, every round: the true deal is never ruled out; every
KNOWN verdict holds in the true deal; the deal count never increases;
sampled grid cells match `entails`. Final accusation checked against
the hidden envelope.

## Honest scope notes

- **Assumption**: the refuter's *choice* of which card to show is
  treated as uninformative (harness policy: lowest-indexed held card;
  the solver does not model choice strategy). Modeling strategic
  choice is epistemics beyond the deal relation, out of scope.
- Counting entered as the direct counter automaton, machine-checked
  equal (full relation equality, k ≤ 3) to 0007's witness-based
  derivation — the principled grounding stands, the counter is just
  the fast constructor for the same relation.
- Guarded multiplication (0009) was *not needed*: the bounded game's
  arithmetic is counting and addition, as 0005 §1 predicted. It waits
  ready for games whose rules genuinely multiply.

## Status

The bounded/finite realm is closed for Clue-like games: representation
(including nonemptiness events), exhaustive deduction, exact model
counting, and validated one-sidedness, at full game scale, in seconds.
This is the scaffold. Extensions from here (SUMMARY next steps): the
ω/infinite game, level crossing for exponentiation, the ^/&
independence proofs, variable-size counting, and the (now
twice-observed) monotone-shrinkage law of canonical knowledge.
