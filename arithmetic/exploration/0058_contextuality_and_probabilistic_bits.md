# 0058 — Contextuality proper, and the wall under probabilistic bits

0057 closed with two dares: import the actual Kochen–Specker test
(find contexts pairwise realizable but jointly not), and go the
literal route — make the bits probabilistic and feel for the Gödel
wall in that regime. Both done. The frame turns out to contain the
two standard contextuality proofs *verbatim*, paradox under
randomization becomes a compulsory fair coin with a measurable
entropy price, and the wall under noise splits cleanly into a
per-bit regime where it is exponentially thin and a per-word regime
where it does not thin at all. Code:
`output/contextuality_and_noise.py`.

---

## 1. The Specker triangle

Three channel constraints — `e12: n₁ = ¬n₂`, `e23: n₂ = ¬n₃`,
`e31: n₃ = ¬n₁` — staged as measurement contexts:

```
context          solutions
each single             4
each pair               2
the triple              0
```

Every pair is jointly satisfiable; the triple is not. This is
Specker's parable of the seer (the ur-example of contextuality),
and in this frame it is nothing new: it is 0056's cycle-parity law
— an odd number of negations around a reference cycle — *staged as
contexts*. Local consistency without a global section, and the
obstruction is one parity around the loop.

## 2. The Mermin–Peres square drops in verbatim

The standard state-independent contextuality proof is, at its
logical core, a GF(2) linear system: nine bits, six parity contexts
(three rows summing to 0; columns summing to 0, 0, 1). Brute force
over all 2⁹ assignments:

- the best assignment satisfies **5 of 6** contexts;
- **every** 5-subset is jointly satisfiable;
- the sum of all six equations is `0 = 1` — each variable appears
  exactly twice and cancels.

The corpus's representation *is* GF(2) polynomial algebra, so the
square requires no translation, and the obstruction — sum the
equations, read the constant — is the **same parity scan that
detects liars** (0056). Contextual fraction: 1/6 of contexts must
fail, matching the known value for the magic square's logical
skeleton.

Honest scope: this is the logical core only. Quantum mechanics
additionally supplies nine *operators* realizing these contexts as
commuting measurements; the frame shares the obstruction structure,
not the Hilbert-space realization.

## 3. Probabilistic bits: paradox is forced entropy

The literal route: make each channel bit Bernoulli(p) and ask which
distributions are consistent with the definition (fixed points of
the induced map on parameters).

```
definition                      distributional solutions   forced entropy
grounded  (n = x, x given)      one — a delta                    0
truth-teller (n = n)            a continuum, incl. both deltas   0
liar  (n = ¬n)                  EXACTLY ONE: p = 1/2             1 bit
odd 3-cycle (Specker)           EXACTLY ONE: all p = 1/2         3 bits
```

The liar — zero deterministic solutions — has exactly one
distributional solution, the fair coin. **Paradox does not survive
randomization; it becomes compulsory maximal uncertainty.** Forced
entropy is positive exactly when no deterministic valuation exists,
which is the actual content of Kochen–Specker: *no dispersion-free
states on a contextual system, while mixed states exist*. The frame
reproduces "paradox = forced mixedness" quantitatively — the
Specker triangle costs exactly 3 bits of compulsory entropy, one
per edge of the cycle.

Scope: product distributions over the cycle's bits. Correlated
distributions could shift the entropy budget — unexplored, and
exactly where a quantum state would differ from a classical
mixture.

## 4. The wall under noise: thin per bit, solid per word

The mechanism that makes exact arithmetic need unbounded feedback
is the carry influence chain — a generate (both bits 1) followed by
a run of propagate positions (exactly one bit set). Measured at
width 24 over random pairs, its tail halves per unit length,
tracking the `n·2^-(L+1)` reference.

Two consequences, and the audit forced them apart:

**Per bit, the wall is thin.** A feedback window of w positions —
the carry into a bit computed from only the w positions below it —
errs only when an influence chain spans the whole window. Measured
error is `2^-(w+1)` to three decimals (0.12503 vs 0.12500 at w=2,
0.00043 vs 0.00049 at w=10). Any fixed tolerance is met by a fixed
window: almost every instance is finite-state to any error budget.

**Per word, the wall does not thin at all.** The carry into a
uniformly random position is asymptotically a fair coin, so an
adder that drops even ONE inter-block carry is wrong on ~half of
all words — 0.498 measured at a single boundary — no matter how
large the blocks grow. Demanding correctness *everywhere* keeps a
constant-probability failure that no finite feedback bound removes.

So randomness does not remove the obstruction — it relocates it,
cleanly, from expectation to certainty. **Gödel, in this frame,
constrains certainty, not expectation**: the same verdict as 0057
(a cliff, not a slope), now measured along a third axis — average
case versus worst case.

## 5. What the audit caught

Two conjectures in the first draft were wrong, and both corrections
sharpened the result:

1. **Runs of carry bits are not the feedback length.** A carry
   *persists* with probability 3/4 per position (it survives by
   regeneration — both bits 1 — as well as propagation), so the
   naive "longest run of carries" decays slower than 2^-L. But a
   regenerating position emits its carry regardless of carry-in: it
   passes no information from below. The information-carrying
   quantity is the generate-then-propagate chain, and *that* halves
   per unit — the statistic was fixed to measure influence, not
   presence.
2. **The blocked adder's whole-word error does not collapse.**
   Predicted to vanish with block size; measured at 0.50 with one
   boundary and staying there. Not a bug — the carry into a random
   position is a fair coin, so any dropped boundary is wrong half
   the time. The per-bit/per-word split of §4 *is* this correction,
   promoted to the finding.

## 6. Honest limits

- Sections 1–2 are exhaustive (2³ and 2⁹ assignments); section 3's
  fixed points are grid-verified with damped iteration for the
  cycle; section 4 is Monte Carlo (40k/60k/6k trials, seeded) with
  the 2^-L references printed beside the measurements.
- The Mermin–Peres import is the logical skeleton, not the quantum
  realization; the frame has no analogue of the operator algebra
  that makes the square *state-independent* in QM.
- Forced entropy is computed over product distributions only. A
  joint-distribution treatment (does correlation buy back entropy?)
  is the natural next probe, and is precisely the classical/quantum
  boundary in the contextuality literature.
- "Certainty, not expectation" is a statement about random *inputs*
  to exact questions. Random *semantics* (noisy channel dynamics,
  bits that flip during resolution) is a different regime,
  untouched.

## 7. Open

1. **Correlated distributions.** Re-run §3 over joint distributions
   on the cycle's bits. If correlation cannot reduce the forced
   entropy, the 1-bit-per-edge price is a theorem, not a product
   artifact; if it can, the gap measures how far the frame sits
   from the quantum side of the contextuality boundary.
2. **Contextual fraction as the N-ness measure.** §2's "1/6 must
   fail" is a graded contextuality measure on statements. 0054
   §10.3 wanted a minimal-ungrounded-channels measure; whether the
   two coincide (fraction of contexts sacrificed = channels that
   must go ungrounded) is checkable with the census tooling.
3. **The wall in the noisy-semantics regime.** Bits that flip with
   probability ε during channel resolution: does the guarded tier's
   contraction still force unique (now approximate) solutions, and
   does the schema wall acquire a finite signature — or does noise
   in the dynamics, unlike noise in the inputs, actually blur the
   cliff?
