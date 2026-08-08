# 0023 — Eigenbases of the problem: the QM upgrade, and what forces the DFA

Responds to three points: (1) the previous refutations leaned on
instances where the claim is worst-case; (2) the uncertainty-principle
observation *strengthens* rather than weakens the eigenbasis analogy —
position and momentum both have eigenbases in QM, they are just
eigenbases of different operators, so non-uniqueness is expected and
3SAT/Sudoku are simply non-eigen frames; (3) sentences are visibly
forced by the problem, but what forces the DFA? Machine checks in
`output/eigenbasis_structure.py`.

## 1. The worst-case re-arm — and the width split

The methodological critique is accepted: family exhibits do not refute
a worst-case claim. Re-armed properly, worst case against worst case,
no instances anywhere:

| task (3-CNF, n variables) | worst-case bound | status |
|---|---|---|
| decide satisfiability | O(1.308ⁿ) — PPSZ/Hertli | proven |
| produce the ring form | ≥ 7^(n/3) ≈ 1.913ⁿ — disjoint triples, exact | proven |

Both bounds unconditional. So for 3-CNF — the example invoked — **"you
may as well canonicalise" is false at the worst-case level**: deciding
is exponentially cheaper than canonicalising, as a statement about the
two tasks' worst cases. (The role the earlier "instances" were playing
was to prove the lower bound row of this table; a worst case *is* a
sup over instances.)

For **unbounded clause width** the claim flips to plausible: under
SETH both tasks sit near 2ⁿ, and no separation is known. So the truth
is *width-split*: false where we can prove things, open-and-plausible
where we cannot. Recorded as such.

## 2. The eigenbasis upgrade, made literal

The QM reframing is adopted, because it makes checkable predictions:
each canonical form should be the eigenbasis *of an operator family*,
the families should fail to commute, and concentration should trade.
All three verified:

- **The ring (ANF) basis is the common eigenbasis of the restriction
  operators** R_m : f(x) ↦ f(x & m), with eigenvalues 0/1 — a monomial
  x^S survives R_m iff S ⊆ m. Verified on 200 random function/mask
  pairs. (Substitution is "measuring by killing positions".)
- **The Walsh (character) basis is the common eigenbasis of the
  translation operators** T_a : f(x) ↦ f(x ^ a), with eigenvalues ±1 —
  phases, exactly as in QM. Verified likewise. This basis requires
  lifting coefficients from GF(2) to ℤ — which is precisely what the
  framework's counting layer already is.
- **The automaton basis is the canonical decomposition of the
  quotient (shift) action** — by definition: the states of the minimal
  automaton are the distinct Brzozowski *derivatives* of the
  statement, and the engine's `minimized()` computes exactly this
  quotient (Myhill–Nerode).
- **The families do not commute**: R₁T₂ ≠ T₂R₁, witnessed by a
  statement where one order accepts half the space and the other
  accepts nothing. No common eigenbasis exists; concentration must
  trade. The measured table (parity / at-least-one / bent inner
  product / windowed parity across ring, Walsh, automaton): every
  statement is small somewhere, no basis is small everywhere.

So the corrected picture is exactly the proposed one: **multiple
eigenbases, one per observable family, pairwise incompatible — and
3SAT/Sudoku/CNF are non-eigen frames**, identifiable as such by a
crisp criterion: an eigen frame is a *canonical* form (unique per
semantic object); CNF/DNF lack uniqueness, hence non-eigen.

## 3. What forces the DFA (the direct question)

The evidence asked for exists, and it is the strongest kind available:
**the DFA is forced by the same theorem that forced `<<`.**

Recall the minimal basis result (0013): the framework's necessary
generators are {&, <<} — the ring half and the shift half, each
provably indispensable (& by stability, << by bit-permutation
invariance). Now observe what the two forced eigen-decompositions are
attached to:

- The **ring normal form** is the canonical decomposition induced by
  the *ring* structure — the {^, &} half. Stone forced that structure;
  ANF is its normal form. This is the "sentences are forced" intuition,
  and it is right.
- The **minimal automaton** is the canonical decomposition induced by
  the *shift* structure — the << half. The quotient operators
  (Brzozowski derivatives — the standard name is already
  "derivative") are the adjoints of <<: reading one position is
  dividing by the shift. The minimal automaton is the coarsest
  quotient of the statement by "no continuation distinguishes these
  prefixes" — a definition that mentions **no machine concept
  whatsoever**, only the statement's semantics and the position
  structure. Myhill–Nerode says this machine-free quotient *is* the
  minimal DFA.

So the two bases sit exactly over the two proven-necessary
generators. If the DFA were "chosen", the shift would be droppable —
and it is proven not to be (0008: no wiring of {^, &, constants}
yields <<). Sentences are the canonical form of the algebra's
multiplicative half; automata are the canonical form of its
sequential half. Neither is optional because neither generator is.

The structural seat for this pairing is a known duality: terms are the
**initial algebra** side (construction — how statements are built),
automata the **final coalgebra** side (observation — how statements
respond to being read), with the minimal automaton as the statement's
image in the final coalgebra (universal coalgebra; Rutten; the
algebra–coalgebra account of Brzozowski's algorithm,
Bonchi–Bonsangue–Rutten–Silva). Construction versus observation is as
close to position-versus-momentum as this setting can make literal.

One honest caveat, which sharpens rather than weakens the QM analogy:
the automaton family has **frame freedom** — the reading order (0018:
265–301 states for the same knowledge under shuffled card orders).
The position basis in QM likewise exists only after choosing
coordinate axes. The *family* is forced; the frame within it is a
parameter. (The ring basis has its own smaller frame freedom: the
choice of which polarity is "0".)

## 4. Are there other eigenbases?

At least four are now on the table, each with its operator family:

| basis | eigen-family | coefficient ring | status |
|---|---|---|---|
| ANF (ring) | restrictions x ↦ x&m | GF(2) | forced (Stone) |
| dual ANF | co-restrictions x ↦ x∨m | GF(2) | sibling of ANF |
| minimal automaton | shift quotients | — (structural) | forced (<< necessity) |
| Walsh characters | translations x ↦ x^a | ℤ (the counting layer) | verified here |

The generating principle, stated as the QM analogy demands: **one
eigenbasis per (maximal commuting) family of observables definable
from the necessary generators.** Restrictions come from &, quotients
from <<, translations from ^ lifted to counting. Open, and now
well-posed:

- Classify the maximal commuting observable families over the
  generators — that is the classification of eigenbases.
- Which of them are *convexity-compatible* (unique canonical object
  plus a knowably terminating reduction)? ANF and the automaton are;
  Walsh is (as a transform) but its statement-reduction story is
  unexplored; CNF-like frames are not (no uniqueness) — which is
  exactly why 3SAT is a non-eigen presentation, as proposed.
- The uncertainty program: quantitative tradeoffs between
  concentrations in pairs of these bases (the measured table is the
  data; an inequality would be the theorem).
