# 0022 — The optimality suspicion: strongest form, and where it breaks

Task: make the suspicion work — "no algorithm does materially better
than the ring's canonicalisation" — and find where it breaks
irreparably. Machine-checked exhibits in
`output/stress_test_optimality.py`. Verdict up front:

> The suspicion is **true about the canonicalisation task** and
> **false about the inference task**, and the gap between those two
> tasks is not a technicality — it is a complexity-class gap
> (Parity-P versus coNP). The part of the suspicion that survives is
> exactly the part in which the ring plays no role. And the
> instrument that breaks it is the framework's own second canonical
> form: the DFA connection that felt like support is the refutation
> arriving.

## Part A — the suspicion works, in three exact senses

**A1. For the canonicalisation task, representation length and
algorithm cost really are exactly tied — unconditionally.** ANF is
unique, so its size is a property of the *statement*, not of any
algorithm. Any algorithm that outputs the ring canonical form pays at
least its length, whatever its internals. "At least one of n" has
exactly 2ⁿ−1 terms (verified). No cleverness escapes this; it needs no
P ≠ NP. The intuition that "the representation length and the
algorithm complexity are exactly tied" is a theorem — *for this task*.

**A2. Within the ring proof system, the expansion is provably
unavoidable.** Expand-and-cancel is Polynomial Calculus (0020 §4), and
PC has unconditional exponential lower bounds via the degree method.
Inside ring-world, "you cannot avoid the expansion" is not a
conjecture.

**A3. The basis itself is forced.** Stone, characteristic 2, and
convexity-needs-a-ring (0019 a). Among ring presentations there is
nothing to choose; the ring's normal form is *the* ring normal form.

This is the strongest honest version: **among algorithms that go
through the ring form, nothing materially beats expand-and-cancel, and
the ring form is canonical among ring forms.**

## Part B — where it breaks, irreparably

**B1. Sound-and-complete inference does not have to go through the
ring form — proven from inside the framework.** The automaton pipeline
decides the same entailments. On "at least one of n": every
ring-form-producing algorithm pays 2ⁿ−1 *by A1's own semantic
argument*; the automaton answered both entailment directions at
n = 48 — where the ring form has ~2.8 × 10¹⁴ terms — in 25 ms, with
22- and 50-state machines, never visiting the ring form. The
suspicion's strongest true statement (A1) is exactly what makes this
irreparable: the floor is real, and a complete method walked around
it. Note what broke it: not an exotic algorithm — the framework's own
other canonical form.

**B2. The obvious repair — "then the *automaton* is the true
canonicalisation" — dies symmetrically.** Windowed parity: ring form w
terms, minimal automaton 2^(w+1) states, and since the engine's
minimisation is Myhill–Nerode the measured count *is* the proof of
minimality. Each basis exponentially beats the other on some family.
There is no winner to crown.

**B3. No basis can be crowned, ever.** Counting: there are 2^(2ⁿ)
statements on n atoms and at most 2^(s+1) canonical objects of size s,
so *every* canonical form system has statements requiring exponential
size — unconditionally — and B1/B2 show different systems have
*different* hard statements. The space of canonical forms is a
frontier with no maximum. This is the precise sense in which the
eigenbasis analogy fails: there is provably no basis that
diagonalises everything.

**B4. The canonicalisation task overshoots the inference question —
by a complexity-class gap.** Verified identity: the *top coefficient*
of the ring form equals the parity of the number of satisfying
assignments. So producing the ring form of a CNF computes parity-SAT,
which is Parity-P-complete (Papadimitriou–Zachos); by
Valiant–Vazirani and Toda, Parity-P is hard for the *entire polynomial
hierarchy* under randomised reductions. The inference question is
coNP — the first level. Requiring inference to pass through the ring
form demands strictly more than the question asks (unless the
hierarchy collapses). **The ring canonicalisation is not the
bottleneck of inference; it is an overshoot of it.** Lower bounds on
it bound the wrong task.

**B5. What survives is basis-free — and therefore not about the
ring.** "Cannot reach polynomial time on all inputs" remains
true-shaped, but it is P ≠ NP / SETH: statements about the *problem*,
indifferent to representation. Every ring-specific part of the
suspicion is refuted above; every surviving part mentions no ring.

**A Clue-native witness that this bites the toy problem** (not a
worst-case argument — a locator): "x is divisible by 3", the
framework's own counting vocabulary (0011), is **3 automaton states at
every width** against a ring form of exactly (2^(n+1)+1)/3 terms at
degree n−1 — measured 11, 43, 171, 683, 2731, 10923 for widths
4–14. Together with 0021's a-priori-K measurement (27,648 terms vs 17
states), the framework's own workloads live on the wrong side of the
ring.

## The replacement intuition

The eigenbasis picture assumed one distinguished basis in which
everything is diagonal. What the evidence supports is the opposite
structure, and it is familiar from another field:

> **There is no eigenbasis; there are (at least) two incompatible
> decompositions, and hardness is concentration-relative.** The ring
> form is literally the Reed–Muller (Möbius) transform of the
> statement; the automaton/OBDD form is its sequential, positional
> factorisation. A statement concentrated in one can be maximally
> spread in the other — "at least one of n" and windowed parity are
> the two extreme witnesses, one in each direction. The right analogy
> is not an eigenbasis but **time-and-frequency**: an
> uncertainty-principle-shaped tradeoff between two transforms, with
> instance difficulty = concentration in the best available basis,
> and *basis-free* difficulty = the complexity-class conjectures.

This also explains a fact about practice that the eigenbasis picture
cannot: real solvers are portfolios (CDCL = resolution basis,
Gaussian engines = GF(2) basis, BDD engines = order basis), and the
portfolio beats every member — which is just B1/B2 deployed as
engineering.

## What remains genuinely pursuable

- **Basis-relative lower bounds are real mathematics with traction**:
  a PC degree lower bound for Clue-shaped constraint systems (0021)
  would make "the ring cannot avoid the expansion *on this problem
  class*" a theorem. That is the defensible descendant of the
  suspicion.
- **The frontier question**: characterise which statements are
  ANF-concentrated, automaton-concentrated, both, or neither. "Both"
  is where this framework's easy instances live (finite Clue is both:
  small K automaton, and its events are low-degree). A statement
  provably spread in *every* canonical form would be a
  representation-independent hard instance — that is where any honest
  successor of the suspicion now lives, and it is (correctly) as hard
  as the complexity conjectures it would imply.
