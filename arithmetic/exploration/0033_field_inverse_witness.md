# 0033 — The field-inverse witness: both live edges, one function

Directive: push through the two live edges of 0032 — the rigidity
hunt and the parity conjecture's positive test. Both landed, on the
same witness. Machine checks: `output/live_edges.py`.

## 1. Edge A: the rigidity hunt

**The squeeze theorem** narrows the search space first: cut rank ≤
ANF sparsity *in every basis* (each monomial of f∘L is rank-1 across
any cut; spot-checked under GL probes). So a GL-robust high-rank
witness must be ANF-dense under every linear change of variables —
necessary but not sufficient (0031's independent-set family is
everywhere-dense yet peaks at rank 23; GF(2) cut rank is
parity-communication, and graph structure collapses it).

Two candidates failed before one landed, all by measurement:

- **The GF(2) determinant** — poly to evaluate, GL-friendly — turned
  out to be *ring-homed*: its ANF is exactly k! Leibniz monomials
  with zero cancellation (6 and 24, asserted), FDD 99 at n = 16 —
  subexponential 2^O(√n log n). A finding in itself (§3), but no
  witness.
- **Spanning trees of toy expanders** — order-curable at machine
  sizes (below).

**The field inverse delivers**: f = low bit of x^(−1) in GF(2^n)
(the AES S-box core; the field is built by a self-validating
exp/log construction — full multiplicative period proves the modulus
irreducible). Measured mid-cut ranks:

    n = 12:  natural 62;  GL probes 63, 63, 63, 64, 63, 64  (max 64)
    n = 14:  natural 127; GL probes 127 ×5, 128              (max 128)

**Essentially full rank, in the natural basis and under every random
GL(n,2) probe, doubling per two variables.** By the rank floor
(0032), every frame of the taxonomy, in every basis probed, has size
≈ 2^(n/2) on this succinct, polynomial-time-evaluable family — the
maximal possible empirical witness for the full-portfolio
exponential bound. Certification over all of GL(n,2) simultaneously
remains the named rigidity-adjacent open; nothing stronger can be
said without crossing that wall, and nothing weaker is compatible
with these measurements. (Crypto folklore aligns: the S-box was
chosen precisely because no linearised structure tames it.)

## 2. Edge B: the parity conjecture is a one-way street

0031 conjectured: polynomial frame home ⟺ polynomial model
counting. The forward direction is trivially true (compilation
counts). **The converse is false, by measurement, on the same
witness**: the inverse is a *bijection*, so the model count of "low
bit of x^(−1) = 1" is closed-form — exactly 2^(n−1), verified — while
the rank floor denies the family any frame home. Polynomial counting
by pure algebraic structure, no representation anywhere. Hence:

> **Frame-homed ⊊ counting-tractable.** The frames capture a proper
> subclass of the counting-tractable world — the width-DP part —
> and algebraic structure (bijectivity here; matrix-tree, FKT in
> general) counts without representing, exactly as Gaussian
> elimination decides without representing (0030/0031).

Secondary exhibit, recorded with scale honesty: spanning trees of
cycle-plus-matching graphs — matrix-tree (integer Bareiss
determinant, implemented, cross-checked against brute force at
v = 8, 10) counts them in polynomial time for every graph, and the
connectivity-partition frontier argument makes every edge-order DD
exponential for true expanders; but at machine sizes the toy
instances are **order-curable** (2836 → 318 states under the
frontier-sorted order, measured), so that route's refutation is
cited-plus-argued, not measured. The inverse witness is what makes
the refutation measured.

## 3. The determinant's two faces

The determinant *statement* det_k = 1 is ring-homed (k! monomials,
subexponential FDD) — while the determinant *algorithm* is the
counting-side escape engine (matrix-tree). The same object is tame
as knowledge and untameable as a tool: representations capture what
the determinant *says*, not what it can *do*. This is the cleanest
single illustration of the whole 0031–0033 arc.

## 4. The completed picture

Frame homes = width-style dynamic programming, on both tasks. The
systematic escapes are algebraic structure invisible to
representations — Gaussian elimination, implication closure, unit
propagation (decision); bijectivity, matrix-tree, FKT (counting) —
and every escape found is linear algebra over the value structure.

Final ledger of the founding suspicion ("you cannot do materially
better than the ring's canonicalisation"):

| task | verdict |
|---|---|
| counting, fixed bases | **TRUE, unconditionally** (0032 rank floor + affine witness) |
| counting, full portfolio | maximal empirical witness (field inverse, full rank under every GL probe); certification = the rigidity wall |
| parity biconditional | one-way only: home ⇒ countable; converse **refuted, measured** |
| decision | **FALSE** (0031) |

The eigenframe theory stands as the complete complexity theory *of
representations* for this logic — taxonomy closed at one coordinate
(pool theorem), flow laws exact, floors unconditional — with its
outside now mapped and named on both sides. The remaining
mathematics beyond this point is the rigidity wall itself.
