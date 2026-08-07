# 0017 — Compact representation buys no cheaper inference

The question, stated as theory rather than engineering: does the
automaton formulation's compactness make *inference* cheaper, or does
the exponential simply move? **It moves — and the true cost is worse
than exponential.** Measured and cited below; the measurement lives in
`output/succinctness.py` §4.

## The proposed argument, and where it does and does not work

The sketch: (i) every DFA has an exactly equivalent statement in the
original framing; (ii) DFA → statement is polynomial; (iii) inference
in the statement framing is bounded by sentence length, worst case
exponential; therefore (iv) inference over DFAs is exponential.

Assessed honestly:

- **(ii) is correct, and is this workstream's own result** — 0015's
  run-encoding construction converts any automaton to a positive
  statement with O(s) hidden channels and O(s²) atoms. Good instinct;
  the construction exists.
- **(i) needs the shift.** Over {^, &, 1} alone every expression is
  *bitwise*: each position is judged independently. Bitwise relations
  are closed under conjunction **and projection**, so hidden channels
  over that signature buy literally nothing, and most automatic
  relations (order, addition, nonemptiness) have no equivalent
  statement at all. With the shift present, (i) holds. *(This also
  corrects an overstatement in 0015 — see its amended table.)*
- **(iii) is where the argument leaks.** The statement produced by
  (ii) carries hidden channels, and reducing it is not bounded by its
  length: eliminating existentials is precisely the expensive step.
  For statements *without* hidden channels the bound does hold —
  canonical form ≤ 2ⁿ terms in n symbols, so inference is at most
  exponential and, by 0016's exact counts, that is tight.
- **(iv) does not follow from (i)–(iii) as stated**, because the chain
  runs in the direction of an *upper* bound: it caps DFA inference by
  translation plus statement-side cost. A lower bound needs a hard
  problem reduced *into* DFA inference.

So the sketch is a valid reduction skeleton pointed the wrong way —
but its conclusion is right, and provable by other means.

## The actual answer: non-elementary, not exponential

The layer's relations are exactly the WS1S-definable ones (0001 §3),
and its formula language has ¬, ∃ and the base relations, so deciding
whether a sentence holds *is* the WS1S decision problem.

- **Meyer / Stockmeyer**: deciding WS1S is **non-elementary** — no
  fixed tower of exponentials bounds it, as a function of formula
  size. *(Cited, standard.)*
- **Fischer–Rabin**: even the purely additive fragment (Presburger,
  which this layer contains) requires at least 2^2^(cn) time.
  *(Cited, standard.)*

So the expectation that compactness cannot buy cheap inference is
**correct and then some**: inference is not merely exponential, it is
worse than any elementary bound, and the automaton procedure is
essentially optimal rather than wasteful.

## The exponential, measured

A formula of *linear* size whose canonical automaton is
*exponential* — compose "triple it" k times:

    T_1(a,b) = (b = a + (a << 1))
    T_{k+1}(a,b) = ∃m. T_k(a,m) ∧ T_1(m,b)

| k | atoms | canonical states |
|---|---|---|
| 1 | ~3 | 4 |
| 2 | ~6 | 10 |
| 3 | ~9 | 28 |
| 4 | ~12 | 82 |
| 5 | ~15 | 244 |
| 6 | ~18 | 730 |

Exactly 3ᵏ + 1 states from O(k) atoms. And this is the *optimistic*
case — a single exponential, from ∃ alone with no alternation. Adding
quantifier alternation is what produces the tower.

(A first attempt used iterated doubling, b = a + 2ᵏ, expecting the
same blow-up; it stays at k + 3 states, because adding a power of two
in binary needs only to walk to position k. Multiplicative composition
is what forces the carry magnitude into the state. Recorded because
the negative result is informative: not every compact formula
canonicalises expensively.)

## Where the cost actually sits — and why finite Clue was fast

    formula  →  canonical automaton      non-elementary in general
    automaton, automaton →  verdict      polynomial in state counts

Inference against an *already-canonical* K is cheap; reaching
canonical form is what costs. That is exactly why the K-workflow
(0007, 0010) runs full-size Clue in seconds: it pays canonicalisation
once per event, always on a small formula with no alternation, and
every subsequent question is a containment check against a K that is
already canonical. The framework's design — keep one canonical K,
update incrementally — is precisely the arrangement that avoids ever
building a large alternating formula.

The general lesson, which holds for both framings:

> Semantic convexity guarantees a terminating, no-cleverness
> reduction. It says nothing about the cost of that reduction, and the
> cost is provably not elementary. The two framings do not differ in
> that; they differ in *where* the blow-up is paid — in the sentence
> for the expression algebra, in the canonicalisation for the
> automata.
