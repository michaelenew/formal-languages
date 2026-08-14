# 0064 — The epistricted wall and the sign problem

Threads 1 and 2 of the queued program: impose the trust wall on
classical points and find where it stops; then price what's left
over. Both answers are exact. Code: `output/the_epistricted_wall.py`.

---

## 1. A trust wall does real quantum-looking work

The toy bit (Spekkens): ontic space {0,1,2,3}, knowledge wall = "you
may know at most half." Verified: the six maximal epistemic states
answer exactly one of the three pair-partition questions each (an
uncertainty relation *from the wall alone*); Bayes-plus-rerandomize
updating makes repeated questions consistent and complementary
questions disturbing; the 24 reversible maps match the single-qubit
Clifford count, the 6 states / 3 questions match the stabilizer
states / mutually unbiased bases. The user's proposed move —
distribution + explicit knowability wall — reproduces the stabilizer
fragment's structure from classical points.

## 2. Where it stops: exactly the parity

The triangle's contextual model (P(differ) = 1 on every edge) needs
ontic support inside the global solution set — which is empty — and
any distribution over atoms has expected anticorrelation ≤ 2/3. So
**no epistemic restriction over classical points reaches the
contextual model**: the wall recovers the noncontextual polytope and
stops at the parity. The boundary of the epistemic program *is* the
contextual fraction.

## 3. The sign problem, exactly

Insist on classical points anyway: solve for signed q over the 8
atoms with the anticorrelated marginals. Exact elimination: the
solution space is a 1-parameter family (rank 7), and the minimal
total negativity over all of it is

```
negativity(triangle model) = 1/2,  exactly
```

with witness q = −1/4 on each **constant world** (the phase fiber!)
and +1/4 on each mixed world. The best noncontextual model (truth
2/3) is an honest distribution — negativity 0. The triangle now has
two computed nonclassicality coordinates: contextual fraction 1/3,
negativity 1/2. Sampling a signed measure is the classical
simulation wall — "an inefficient split shows up as intractability,"
as a number. (Literature frame: negativity ⟺ contextuality, Spekkens
2008; contextuality as the magic resource — cited, not verified.)

Noteworthy detail: the negative quasi-mass sits exactly on the deck
fiber (the constants) — the sign problem is *located* on the phase.

## Honest limits

- The toy-bit ↔ stabilizer match is verified at the level of counts
  and structure (6/3/24, complementarity, disturbance), not as a
  full isomorphism of theories.
- Negativity minimal over the marginal-matching family for *this*
  scenario; other quasiprobability frames (Wigner-style) could price
  it differently — 1/2 is the minimum for atom-diagonal
  representations.

## Open

1. Does the negativity of the frame's *graded* paradoxes track
   log₂(holonomy) (odometer-type models priced in signed mass)?
2. The epistricted version of the *hexagon* (the double cover):
   does the wall reproduce the covered model completely — i.e., is
   the epistemic program exactly "everything below the first
   nontrivial holonomy class"?
