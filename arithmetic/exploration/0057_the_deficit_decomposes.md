# 0057 — The deficit decomposes: there is no finite ℏ

0056 measured a ~30% reachable-pair deficit between the persistent
multiplier and the counter and asked its fate: does δ tend to 1, to a
constant (a commutator norm for the frame), or resonate? The answer is
none of these — **it decomposes, exactly, into classical parts**, and
the decomposition settles which kind of uncertainty this frame
carries. Code: `output/the_deficit.py`.

---

## 1. Counter vs counter: the deficit is the Chinese Remainder Theorem

Reachable pairs of `(popcount mod m₁, popcount mod m₂)` equal
`lcm(m₁, m₂)` — every cell of the grid m ≤ 8, exactly. Hence

```
δ(C_m₁, C_m₂)  =  1 − 1/gcd(m₁, m₂)
```

Coprime counters are **fully independent** (δ = 0, every joint state
realizable); equal ones overlap maximally (δ = 1 − 1/m). The deficit
between compatible observables is arithmetic overlap — CRT — and
nothing else. This calibrates δ: it detects *shared structure*, not
incompatibility.

## 2. Multiplier vs counter: the deficit is the transient fraction

For the persistent multiplier `P_p = (x mod 2^p)·y` paired with
`C_m`, the joint cost is **exactly linear in m**:

```
p=1:   3 states =  2 recurrent +  1 transient    joint =  2m + 1
p=2:  12 states =  7 recurrent +  5 transient    joint =  7m + 5
p=3:  50 states = 29 recurrent + 21 transient    joint = 29m + 21
```

(exact for m = 2..7), and the coefficients are verified
**state-by-state**: every *recurrent* state of the multiplier pairs
with every count residue; every *transient* (learning-phase) state
pairs with a fixed finite set of residues — the counts that can
co-occur at its bounded reach-times. So

```
δ(P_p, C_m)  →  1 − recurrent/total  =  the transient fraction
```

(0.333, 0.417, 0.420 for p = 1, 2, 3). Temporal overlap — the two
observables are correlated only while the multiplier is still
learning its constant — and nothing else.

## 3. The conclusion: no finite ℏ

Every deficit measured in this frame decomposes exactly:

| pair | deficit | cause |
|---|---|---|
| counter, counter | `1 − 1/gcd` | arithmetic overlap (CRT) |
| multiplier, counter | → transient fraction | temporal overlap |

Neither is incompatibility. Once the overlaps are subtracted —
coprime moduli, post-transient epoch — **every joint state is
realizable and the budget is a plain sum of logs with no cross
term**. The finite-level ℏ of this frame is zero.

The incompatibility that motivated the conjecture is real, but it
lives *entirely at the unbounded limit*: both observables exact, with
read-back, is the Minsky wall — undecidable at infinity,
unconstrained at every finite scale. So the Heisenberg question of
0055 resolves by measurement:

> **The frame's uncertainty is Kochen–Specker-shaped, not
> Robertson-shaped.** There is no graded trade at finite scale (no
> variance inequality, no commutator norm); there is an
> all-or-nothing obstruction to joint refinement at infinity. That is
> contextuality's signature — and it is consistent with where the
> published bridge to logic actually connects (liar cycles /
> no-global-section, 0056 Part A), and inconsistent with a Δx·Δp
> reading.

Put back in the workstream's own vocabulary: the wall was never a
price that steepens as you approach it. Finite sentences trade
resources classically and freely; the schema boundary (0054) is a
cliff, not a slope, and 0055's "push where the breakdown comes" is
free repositioning along a flat landscape that ends at an edge.

## 4. Honest limits

- Exactness claims are over the measured grids (m ≤ 8; p ≤ 3, m ≤ 7)
  with per-state verification inside them. The CRT identity is
  provable in one line (pair state = count mod lcm) — the measurement
  is its audit. The transient/recurrent decomposition is verified
  state-by-state but the "exactly linear for all m" claim beyond m = 7
  rests on the argument (transient residue sets stop depending on m
  once m exceeds the transient horizon), not further measurement.
- Only two observable families are measured. A third kind — two
  order observables sharing a variable (e.g. `(x mod 2^p)·y` vs
  `(x mod 2^q)·z`) — could conceivably show deficit not explained by
  CRT or transience; unexamined.
- "No finite ℏ" is a statement about *this* frame's state-counting
  geometry, not about quantum mechanics.

## 5. Open

1. **A third overlap type, or closure.** Sweep mixed pairs
   (order/order, order/liar-adjacent, counted-tier pairs) and test
   whether every deficit decomposes into the two identified causes.
   If yes, the decomposition theorem is: δ = arithmetic ⊕ temporal,
   always — a small classical "no-signaling" theorem for the frame.
2. **The cliff's shape.** With no finite ℏ, the interesting scaling
   is how fast finite truncations of the wall's two sides diverge —
   0055's states(p) growth (~2.3×/bit) against the counter's linear
   m: the *approach* to the cliff has structure even though the trade
   at the cliff does not.
3. **Contextuality proper.** The KS-shape verdict suggests importing
   the actual test: find three observables A, B, C where each pair is
   jointly realizable but the triple is not — the frame's analogue of
   a KS triangle. The channel census (0056) has the tooling; odd
   cycles are the candidate obstruction.
