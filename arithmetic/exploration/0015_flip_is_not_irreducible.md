# 0015 — Flip is not irreducible: negation is worth exactly one relation

0014 left this open, with a stated expectation that flip would turn
out irreducible. **It is not.** Every automatic relation can be
rebuilt with share and hide only — no negation anywhere — over a
fixed finite signature. Verified in `output/flip_elimination.py`,
where `DFA.complemented` is replaced by a function that raises during
the whole construction, so the absence of negation is *enforced*
rather than asserted.

## The exchange rate

    pp-closure( &, <<, constants )   NOT everything
                                     (0013: ∩ is a polymorphism, so ^
                                      cannot be reached)
    pp-closure( &, ^, <<, 0, 1 )     everything
    FO-closure( &, <<, constants )   everything

Holding {&, <<, constants} fixed, **adding ^ to the signature buys
exactly what adding flip to the logic buys.** They are
interchangeable, one for one.

This reverses the reading of 0013 in a satisfying way. 0013 said "^ is
redundant, because flip gives it to you." The complement is equally
true: *flip is redundant, because ^ gives it to you.* Neither is more
fundamental. The corpus's decision to carry ^ as an operator was never
a redundancy — **it was paying for negation up front**, in the
signature instead of the logic.

## The construction

Carry the target automaton's **run** in hidden channels:

    H     an all-ones prefix ("horizon") containing every input bit
    HL    = (H << 1) ^ 1, one position longer
    Q_p   one track per state, marking the positions where the run
          sits in state p

Every constraint is local, hence conjunctive:

- H and HL are all-ones prefixes; every input sits inside H
- the Q_p partition HL
- position 0 lies in Q_initial
- (Q_p & H & input-pattern) << 1 sits inside Q_δ(p, pattern)
- the position just above H lies in a state that accepts padding

The horizon is what makes the encoding legal: state tracks must be
*finite sets*, so a naive "state after the input ends" track would run
to infinity. Bounding the run at a hidden finite horizon, and checking
at that one boundary position that the remaining all-zero padding
would be accepted, keeps every channel finite.

And the place ^ earns its keep is precise: matching an input pattern
needs *relative complement* — the positions inside HL where a channel
is 0 — which is `HL ^ (HL & v)`. That single step is the whole of
what negation was doing.

Machine-verified on targets that were themselves obtained by
complementation: x ≠ 0, x is odd, x is NOT a power of two, x > y.

## The readable special case

Not everything needs the general machinery. Nonemptiness — the event
the corpus's expression algebra could not state (0005 §1) — takes one
hidden channel:

    x ≠ 0  ⟺  ∃q:  q is an all-ones prefix
                    q misses x
                    the position just above q is in x

(q is the run of zeros below x's lowest set bit.) The lesson that
matters for the framework: **what the original framing was missing was
never negation — it was hidden channels.**

## Consequence for the original framing

The corpus's statement framing is conjunctions of emptiness
assertions over {^, &, 1}-expressions: no negation *and no
existentials*. Those two absences are not equal in weight:

| framing | expressive power |
|---|---|
| emptiness assertions, no ∃ | strictly weaker (cannot state nonemptiness) |
| + hidden channels (∃) | **exactly the automatic relations = DFA** |
| + negation instead | also exactly the automatic relations |

So the original framing, extended with hidden channels and nothing
else, *is* exactly DFA-equivalent. The K-workflow's deduction test
still wants complement (K ∩ ¬H), but that is a use of negation at the
*meta* level — deciding entailment — not a requirement on the
statement language itself. Statements can stay positive.

## What survives of the level hierarchy

0013's three levels are real but **signature-relative**, exactly as
0014 said, and now sharply:

- For the *fixed* signature {&, <<, constants}, pp ⊊ FO. Proved
  (∩-polymorphism).
- For the signature {&, ^, <<, 0, 1}, pp = FO. Proved (this file).

So "pp is weaker than FO" is not a fact about the layer; it is a fact
about a particular signature. Choose the signature that already
contains ^ and the distinction disappears. The obstruction table of
0014 is unaffected — it was stated presentation-independently for
exactly this reason.

## Open

- **Minimality of the positive signature.** {&, ^, <<, 0, 1} suffices
  for pp; is any proper subset enough? {&, <<, constants} is not
  (0013). Whether ^ can be dropped in favour of some other single
  relation, or whether the constants 0 and 1 are both needed, is
  unchecked.
- ~~**Cost.** Whether a polynomial-size positive definition always
  exists.~~ **Answered in 0016, and the question as posed here
  conflated two things.** The *definition* this construction produces
  is already polynomial — O(s) hidden channels and O(s²) atoms at
  fixed arity. What is exponential is *evaluating* it (each hidden
  channel is projected by a subset construction). Writing the
  knowledge down stays small; deciding with it is what can cost.
