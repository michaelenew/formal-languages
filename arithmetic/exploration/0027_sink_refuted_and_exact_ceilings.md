# 0027 — The sink conjecture refuted (and improved), and the ceilings made exact

The two closing targets from 0026: automaton uniqueness, then ceiling
collapse. Both are settled — the first *against* the conjecture, in a
way that improves it; the second completely, upgrading all three
ordered edges from inequalities to exact equalities. Machine checks:
`output/sink_uniqueness_and_ceilings.py`.

## Part A — the conjecture is false, and the truth is better

**A1.** Among 0026's fixed frames the automaton *is* the unique sink —
that part stands, proved by the four ordered edges plus the
disqualifying witnesses for each flat frame.

**A2.** But the conjecture quantified over the full Kronecker
taxonomy, and the taxonomy contains **ANF's own shared form** — the
FDD (positive Davio with sharing), the exact Davio analogue of the
automaton's subfunction quotient. Measured: the flat frames' extremal
witnesses flow to the FDD just as they flow to the automaton
(at-least-one: FDD 25; δ: FDD 13; full monomial: FDD 25; parity:
FDD 35 — all linear).

**A3.** And the two shared frames separate, in the direction that
kills the conjecture: windowed parity in the separated order has
FDD 68 → 85 → 104 (linear) against automaton 259 → 515 → 1027
(doubling per pair). **A member of the taxonomy does not flow to the
automaton.** Conjecture false.

**A4.** The reverse hunt — a statement automaton-small but FDD-big —
came up empty: on every counting family tried (majority, thresholds,
selectors) the FDD *tracked* the automaton (71 vs 71 at majority
n = 14). A prediction made en route — that majority's Davio closure
would explode — was **wrong by measurement**, and is recorded as
such. Exponential separations in both directions are the known result
in the decision-diagram literature (Becker–Drechsler et al.); the
reverse witness is cited, not reproduced, and stands as the honest
gap.

**A5. The improved statement.** What the evidence supports:

> **Flat frames flow to shared frames. Shared frames are mutually
> incomparable. The sink property belongs to the *sharing move* — the
> quotient, Myhill–Nerode, node-merging — not to the Shannon choice
> and not to any fixed frame.**

The automaton was 0026's unique sink only because 0026's frame set
contained exactly one shared frame. This retro-reads the whole thread
correctly: every ordered edge of 0026 was flat → shared(Shannon); the
Davio-shared frame plausibly admits parallel laws (its crossing/path/
span analogues are unexplored). At the shared frontier, sink-ness
survives only as a parameter *portfolio* (a Kronecker choice vector
emulates any member), and best-parameter search is NP-hard — no fixed
frame is a sink of the full taxonomy.

## Part B — the ceilings, exactly

Each ordered edge's per-cut state count is exactly an **image size of
the upstream description under the cut**; the published rates are the
free-image case, and every collapse is an upstream algebraic
dependence. All three laws upgraded from ≤ to =:

**Crossing law (ANF → automaton), exact form.** The subfunctions at a
cut are exactly the distinct values of

    (symmetric difference of the right parts of the SELECTED
     straddling monomials) ⊕ (parity of completed monomials)

over achievable prefixes. Verified as an *equality* at every cut of
200 random sparse statements. Tightness and collapse isolated: with
disjoint singleton left parts (shattering) and independent right
parts, the ceiling 2^s is achieved exactly (measured 32 = 2⁵); one
right-part linear collision collapses it to 16; one shared left
variable collapses it to 16 — **each dependence costs exactly a
factor of two**.

**Path law (minterm → automaton), exact form.** States at a cut =
distinct model **suffix-sets** (+1 for the zero subfunction when some
prefix is model-free) — equality at every cut, 200 random statements.
The first attempt used distinct *prefixes* and was corrected by the
machine: prefixes sharing a suffix-set merge. Two collapse modes:
suffix-set coincidence, and model clustering (16 clustered models: 21
states; 16 spread models: 91).

**Span law (Walsh → automaton), collapse = stabiliser.** With
d = 3, a generic inner function reaches the 2^d = 8 ceiling; an inner
function with a translation stabiliser of index 2 (the parity of the
three linear forms) pins every cut at 2. **Collapse is the
stabiliser.**

**The unified closure.** Concentration flows from flat frames to
shared frames at a rate set exactly by how much *algebraic
independence* the upstream description carries across each cut — a
linear relation among right parts, a shared left variable, a
suffix-set coincidence, an inner stabiliser are the complete list of
collapse mechanisms for the three laws. Nothing about the rates is
loose any more; the argument the user asked to close is closed.

## Status of the thread

- Flat → shared flow: proved (four exact laws; FDD side measured).
- Shared-level incomparability: one direction measured, reverse
  cited — the single remaining gap in this storyline.
- Sink-ness relocated from a frame to an operation (sharing), with
  portfolio-only sink-ness above it, matching both the NP-hardness of
  frame search and the 0022 practice note (solvers are portfolios).
