# 0018 — Is "what's in the envelope" always exponential?

Short answer: **in the worst case yes — but conditionally, and not
"always".** Precisely:

- The problem is **coNP-complete**. So no polynomial algorithm exists
  unless P = NP — but it is *not proven* exponential; proving that
  would settle P vs NP.
- On real instances it is not exponential at all: full-size Clue
  solves in ~5 s with K peaking at 145 states (0010).
- **Both framings sit in the same class.** Sentence-based and
  automaton-based inference are equally hard; they differ in *when*
  the cost is paid, not how much.

## Why coNP-complete

**Membership.** A counterexample to "card c is in the envelope" is a
single consistent deal placing c elsewhere: polynomial to write down
and polynomial to check against the knowledge. So the complement is in
NP, and the problem is in coNP.

**Hardness, by reduction from Hitting Set** (and with knowledge that
stays *consistent*, so the reduction is not the degenerate one):

Given sets S₁…S_m over universe U and a bound k, build a game with
deck U ∪ {s} plus padding, a player P with hand size k, and knowledge

    for each j:  "P holds at least one of  S_j ∪ {s}"
    "only P or the envelope may hold s"

- K is *always* consistent: P can simply take s, satisfying every
  constraint at once.
- s can be outside P's hand exactly when U contains a hitting set of
  size k — the constraints then force P to be one.
- With s confined to P or the envelope, s is in the envelope iff s is
  not in P's hand.

So **K ⊨ "s is not in the envelope" iff no hitting set of size k
exists** — a coNP-hard question. Combined with membership,
coNP-complete. ∎

The disjunctive "holds at least one of these three" event is what
carries the hardness: it is a hitting-set constraint in disguise.
Ordinary passes and seen refutations are unit constraints and are
easy; the *unseen* refutation is where the complexity enters. (Which
is a small vindication of 0010's emphasis on that event as the
representationally interesting one — it turns out to be the
computationally interesting one too.)

## For the finite game, canonical K is an OBDD

A sharper identification, and a useful one:

> For a fixed deck of n cards, canonical K reads exactly one column
> per card, so it *is* the **ordered binary decision diagram** of the
> "consistent deals" predicate, with the card order as the variable
> order.

(The minimal DFA of a fixed-length language is the quasi-reduced OBDD
in that order.) Everything known about OBDDs then applies:

- **Build once, query cheaply** — exactly the K-workflow's shape, and
  why 0010's whole-grid survey is one linear sweep.
- **Size depends on variable order**, and optimal ordering is NP-hard.
  Measured (`output/succinctness.py` §5): identical knowledge over 8
  shuffled card orders gives 265–301 states, all agreeing on the same
  9106 consistent deals. A modest but real tuning knob at this scale.
- **The worst case follows without needing OBDD lower-bound
  citations**: every update is polynomial in the current |K| at fixed
  player count, so if K stayed polynomial in the deck size throughout,
  the whole workflow would be polynomial — contradicting
  coNP-hardness. Hence **unless P = NP, K must sometimes grow
  superpolynomially.** The exponential is the problem, not the
  encoding.

## Where the two framings actually differ

Not in complexity class — in amortisation:

| | sentence framing | automaton framing |
|---|---|---|
| per event | cheap (conjoin) | canonicalise (can be costly) |
| per query | a fresh coNP-hard decision | linear sweep of K |
| all 84 grid cells | 84 decisions | **one** sweep |

The automaton framing front-loads. That is a strictly better deal when
queries outnumber events — which is exactly Clue, where after each
event you want the entire who-holds-what grid — and a worse deal if
you only ever ask one question.

## Why real Clue is easy anyway

Both the hardness and the OBDD blow-up are worst-case statements about
*adversarially structured* knowledge. Real Clue knowledge is
overwhelmingly unit constraints (passes, seen cards) with a few
disjunctions over 3-card sets drawn from a small deck, and the
constraints overlap heavily. An attempt to force blow-up with
hitting-set-shaped knowledge (14 cards, up to 10 random 3-card
refutations, hand size 4) never exceeded 95 states — minimisation
collapsed it every time. The exponential exists; Clue does not reach
it.

## Honest limits of this note

- The reduction shows hardness for *Clue-like* knowledge in general
  (arbitrary refutation sets over an arbitrary deck). It does not
  address parameterised questions — e.g. whether the problem is
  fixed-parameter tractable in the number of unseen refutations, which
  looks plausible and is unexplored.
- "Real Clue is easy" is an empirical observation over the runs in
  this workstream, not a theorem about the distribution of game
  states.
