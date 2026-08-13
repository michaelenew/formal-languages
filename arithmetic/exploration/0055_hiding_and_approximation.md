# 0055 — Two trades at the wall: hide the state, or bound it

Two questions. Can uncertainty be introduced into the state to move
where Gödel hits? And what is the best approximation with finite bits —
is `&` the 0-bit member of a family indexed by carry length? Both
answered; the second conjecture confirmed where it's sharp and
corrected where measurement disagreed. Code:
`output/hiding_and_approximation.py`.

---

## 1. The Parikh reading is exactly right, and it refines 0054's scan

A Parikh automaton's counters are write-only during the run, read once
at the end — and this is precisely the corpus's own counted tier:
0034–0036's `CountedAutomaton` enforces that hiding guard by machine.
In channel language the criterion is another syntactic scan:

> **A channel is dangerous iff it is unbounded AND some definition
> body reads it.** Bounded read-back = finite state. Unbounded
> write-only = counted tier. Unbounded read-back = the wall.

Demonstrated at the corners: popcount equality runs an *unbounded*
counter that no step ever branches on (accumulate, compare at the end
— decidable, Presburger acceptance); addition runs a *1-bit* carry
read at every step. The classical anchors calibrate the third corner:
two counters with zero-tests are Turing-complete (Minsky). So the
danger was never the size of the memory — **it is the feedback loop.**
Multiplication's schema is read-back by its own definition (the carry
re-enters the datapath), which is *why* it is the wall and counting
never was.

## 2. So yes: uncertainty in the state is a real trade, in two dual forms

- **HIDE (Parikh's trade):** keep the state exact but forbid reading
  it until the end. Gödel relocates from "unbounded state" to "state
  feedback". What you buy: unbounded *accumulation* (counting,
  cardinality comparisons) stays decidable. What you give up: the
  state cannot steer the computation — no carry, no products.
- **BOUND (the approximation trade):** keep reading, truncate the
  state to k bits. Gödel relocates from non-termination to error
  rate: every statement gets a verdict, and the verdict is wrong on a
  measured set. §3–§5 price this trade exactly.

These are the two ways of making the dangerous quadrant safe —
remove the read-back, or remove the unboundedness — and they produce
the counted tier and the approximation family respectively.

## 3. `&` is the 0-state member — forced, unique, and measured

Per-bit agreement with `x·y`, all 16 columnwise functions, exhaustive
8-bit inputs:

```
f       bit0  bit1  bit2  bit3  bit4   mean
x&y     1.00  0.62  0.53  0.52  0.49   0.582
0       0.75  0.62  0.56  0.53  0.52   0.562
x (=y)  0.75  0.62  0.56  0.53  0.52   0.562
```

`&` is exact at bit 0 and **forced**: bit 0 of `x·y` is `x₀y₀`, and a
position-uniform f right at bit 0 must equal AND on all four inputs.
It also wins mean agreement over all bits. A 1-state machine must be
position-uniform, so `&` is *the* 0-bit approximation, in both the
guaranteed and the expected sense. Conjecture confirmed.

**Why `&`:** the diagonal identity. The i = j layer of the
partial-product array is

```
Σ x_i·y_i·4^i  =  spread(x & y)  =  F(x & y)
```

— the Frobenius of `&`. Below bit 1 there are no cross terms (first
at bit 1) and no carries (first at bit 2), so the diagonal is all
there is. The operator 0053 could not name (W1) turns out to be the
shape of the cheapest approximation.

## 4. The family's exact price list — cheaper than the wall's posted price

Minimal Mealy states of `x·y mod 2^p` (residual classes, exact):

| p (exact low bits) | states | log₂ |
|---|---|---|
| 1 | 2 | 1.0 |
| 2 | 5 | 2.3 |
| 3 | 12 | 3.6 |
| 4 | 28 | 4.8 |

Two things worth keeping. The p = 1 member costs 2 states — the
"am I past bit 0 yet" flag — which is why `&`, at 1 state, guarantees
1 bit but can't be beaten to a second. And the growth is **~1.2 bits
of state per guaranteed bit, not the 2 bits** 0054's full-product
bound charges: the truncated task's don't-cares above the horizon
collapse residuals. **Approximation buys a genuine discount on the
wall's price, not just a cutoff.** (Measured at p ≤ 4; no asymptotic
claim.)

## 5. The family, with its tail corrected by measurement

The conjecture guessed "exact below the carry horizon, `&` above."
Measured, mean agreement over all bits:

| p | guaranteed | 0 above the horizon | & above the horizon |
|---|---|---|---|
| 0 | 0 | 0.562 | **0.582** |
| 1 | 1 | **0.594** | 0.582 |
| 2 | 2 | **0.640** | 0.629 |
| 4 | 4 | **0.754** | 0.748 |
| 6 | 6 | **0.876** | 0.874 |

The `&`-tail loses from p ≥ 1: above bit 1 the cross terms dominate
and the diagonal *anticorrelates* with the carry-heavy mid-range —
even the constant 0 agrees with `x·y`'s high bits more often than `&`
does (products of random inputs are 0-biased up there). So the
corrected family:

```
1 state        &               1 bit guaranteed, best position-uniform
states(p)      x·y mod 2^p     p bits guaranteed, best tail 0
```

One member per carry-state length, `&` at the bottom — the
conjecture's shape survives, with the tail corrected.

## 6. Honest limits

- The read-back criterion's dangerous corner (unbounded + read-back =
  undecidable) is cited to Minsky, not re-proved; the safe corners are
  demonstrated in-corpus (popcount ↔ counted tier; carry ↔ finite
  state).
- State counts are exact for the truncated functions at p ≤ 4;
  agreement tables are exhaustive at width 8. No asymptotics claimed
  for either.
- "Best approximation" here means best per-bit agreement under uniform
  inputs, and best guaranteed low-bit prefix. Other metrics (2-adic
  expected valuation, worst-case integer error) are not measured and
  could reorder the tails.
- The HIDE trade is characterized, not rebuilt — the counted tier
  already exists in the corpus (level_crossing.py); what is new is its
  identification with the write-only channel class of 0054's syntax.

## 7. Open

1. **The mixed quadrant.** k bits of read-back PLUS unbounded
   write-only accumulation: strictly between the counted tier and the
   wall. Reverse-Parikh automata territory — does the corpus's
   sentence form reach anything new there (e.g. "the number of carry
   overflows equals popcount(y)")?
2. **Three-valued reduction.** The BOUND trade turns the rewrite
   system's stuck terms into "unknown" verdicts with a measured error
   rate. A coalescing system over k-bit-truncated carries would decide
   everything, wrongly on a set of measure ~2^{-p}-ish — worth
   building to see whether the error concentrates on the same
   sentences the exact system got stuck on.
3. **The price-list asymptotics.** states(p) = 2, 5, 12, 28: ratio
   ~2.3. Whether it converges to 2^{1+ε}, and what ε says about the
   carry's intrinsic entropy, is a clean standalone question.
4. **Position-uniformity as a resource.** `&` is optimal among 1-state
   machines because 1 state forces uniformity; the p = 1 member buys
   its second state just to know where bit 0 is. A hierarchy indexed
   by "states spent on position" vs "states spent on data" would
   separate the two costs the family currently mixes.
