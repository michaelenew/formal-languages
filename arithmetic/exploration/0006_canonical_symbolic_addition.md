# 0006 — Canonical symbolic addition

The first prize, claimed for the addition fragment: terms with **free
variables** now reduce to unique canonical objects by a knowably
terminating, no-cleverness procedure, and the one-sided judgment
(true / undecided) extends to symbolic statements. Implementation and
machine-checked results in `output/canonical_automata.py`.

Design decision recorded first: the statement-layer ⊗ of 0005 §1 is
**declined** — operator economy matters (each operator interacts with all
others and convexity must survive every interaction), and a closed
multiplication is preferred as the long-run OR-carrier since it also
grounds exponentiation. 0005 stands as the record of why the zero law
itself is cheap; the design bet is that its right home is a closed ×.

## The canonical form

A statement over free variables x₁…x_k denotes a relation on numbers
(= finite sets). Its canonical form is the **minimal complete synchronous
DFA** recognizing the relation, one track per variable, read lsb-first,
padding-invariant, states named in BFS order:

- **Uniqueness**: Myhill–Nerode — the minimal complete DFA of a language
  is unique; BFS naming makes it strictly unique (comparable with `==`).
  This is the arithmetic analogue of ANF uniqueness, playing exactly the
  role clause (2) of convexity demands.
- **Knowable termination**: every compilation step has an a-priori bound
  readable off the term — product ≤ |A|·|B| states, projection ≤ 2^|A|,
  minimization only shrinks — so a bound for the whole reduction is
  computable *upfront from the term's structure*. No cleverness.
- **Truth = universality**: a statement is knowably true iff its
  canonical automaton is the one-state universal automaton — the
  automatic-fragment analogue of "reduces to 0". Entailment K ⊨ H is
  language containment, decided by emptiness of K ∩ ¬H. The judgment
  stays one-sided: not-universal is "undecided as a law", not "false"
  (and the same object read as a constraint may be perfectly satisfiable).

Polarity note: in the term algebra, K grows by ∪ (union of empty sets)
and the test is H ⊆ K. Here K is the relation of valuations consistent
with knowledge: it *shrinks* by ∩ as knowledge grows, and the test is
K ⊆ H. The two are Galois-dual readings of the same shape, and the
decision still bottoms out in an emptiness check — K ∩ ¬H = ∅ is the
KH ^ H pattern with the complement on the other side.

## Automata are the closed forms of the stabilizing series

The construction that makes this work: each operator's *relation* is
finite-state even though (Prop 4) no finite term composition computes it.

- z = x + y: **2 live states** — the carry bit (3 complete-minimal, dead
  state included; the suite reports complete sizes). This is the
  stabilizing carry series of 0002 Props 5/6 collapsed into its
  transition structure.
- z = T(x): **2 live states** — in/out of the trailing-ones region; the
  series x & b(x) & b(b(x)) & ⋯ likewise collapsed.
- a, b: 2–3 live states (the owed bit).

The locality barrier said finite compositions of {^, &, a, b} have
bounded influence windows; the automaton escapes by carrying *state*
across positions instead of widening a window. So the expressive step
"base ops → base ops + stabilizing series" is exactly the step
"combinational → sequential", and the canonical automaton is the closed
form the series were reaching for.

## Machine-checked results (all in the suite, seeded)

- **succ two ways, the decisive test**: `x ^ b(T(x))` and `add(x, 1)` —
  syntactically unrelated terms, one built from the series successor, one
  from full addition with a constant — compile to the **identical**
  canonical automaton (3 states, dead state included). Prop 3 falls out
  of pure canonicalization with no insight anywhere in the pipeline.
- Commutativity, associativity, unit of add: universal (the "reduces to
  0" verdict, symbolically, for all inputs at once).
- The corpus's carry-save identity add(x^y^w, a(xy ^ xw ^ yw)) = x+y+w
  (clue/2026-06-21): universal.
- One-sidedness preserved: add(x,y) = x is neither universal nor empty.
- Strict entailment: y = a(x) ⊨ ∃w. y = add(w,w), converse fails —
  existential projection works, so derived predicates (evenness, and via
  ∃w. add(x,w) = y, the order x ≤ y) come free.
- Multiplication by constants stays in the fragment: z = 3x via
  add(x, a(x)), 4 canonical states.

Canonical sizes are startlingly small: the entire theory of addition fits
in a 3-state object. (For comparison, ground ANF over n atoms can need
2^n terms for cardinality facts — 0001 §4's succinctness point, now
visible concretely.)

## Where the fragment ends, precisely

The reachable relations here are the base-2 **automatic relations**
(Büchi arithmetic territory, which strictly contains Presburger). Two
consequences for the declined-and-deferred paths:

- **Closed ×**: the graph z = x·y is not an automatic relation (else
  arithmetic would be decidable), so full multiplication cannot enter
  *this* canonical layer with completeness. Whatever closed form × takes,
  its complete home must be a guarded tier (0005 §2) or a genuinely new
  canonical object — that is now a sharply posed problem rather than a
  hope.
- **Exponentiation**: y = 2^x in this encoding couples a track's *value*
  to a *position* — the BIT/level-shift map, the corpus's `{x} = 2^x`
  cliff (0005 §3). Not automatic either. Since exponentiation is called
  critical for certain statements, this is the honest statement of what
  it will cost: a new device, not an extension of this one.

## Not yet done

- The K-workflow: K as a canonical automaton updated by intersection,
  driving a real deduction loop (finite Clue end-to-end, sizes included
  via counter circuits built from add). Next.
- Quantifier alternation (∀ = ¬∃¬) is available but each alternation can
  exponentiate; fine for decidability, worth measuring for practice.
- The ω-extension for the infinite game still carries the Büchi
  canonicity caveat (0005 §3).
