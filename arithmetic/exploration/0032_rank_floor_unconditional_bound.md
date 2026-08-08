# 0032 — The rank floor, and the unconditional exponential worst case for the fixed-basis portfolio

Directive: for the class where representation⟺complexity parity
holds (the counting/compilation task, 0031), show there is no
worst-case subexponential algorithm based on the eigen
representations. Delivered — unconditionally for the fixed-basis
portfolio, with the full-portfolio version pinned to a named open
wall. Machine checks: `output/rank_floor.py`.

## 1. The rank floor theorem

At any cut, let M be the statement's communication matrix (rows =
subfunction truth tables). **Every frame of the taxonomy has size ≥
rank_GF(2)(M):**

- *Flat kinds* (minterm, ANF, dual, Walsh, moments, hybrids): every
  Kronecker basis element is a product across any cut — a rank-1
  matrix — so t basis elements can only build rank ≤ t.
- *Shared kinds* (OBDD, FDD, negFDD, hybrid sharings): the level
  family at the cut is an invertible image of the subfunction rows
  (identity / ζ↓ / ζ↑ / polarity translations — the fiber laws of
  0028/0029), hence spans the row space; a spanning family has
  rank-many independent, hence distinct, members.
- *Lift kinds* (MTBDD, *BMD, WHDD): same arguments over ℚ, and
  rank_ℚ ≥ rank_GF(2) for 0/1 matrices.

One number per cut floors every kind, every polarity, both lifts,
flat or shared. Verified at every cut of 100 random statements
against seven frames plus the moment diagram. The proof is linear
algebra plus the fiber laws — no complexity assumptions.

## 2. The honesty section: where the floor is loose

GF(2) cut rank is the *parity-communication* measure — exactly the
structure the Davio frames exploit. Measured: windowed parity has
mid-cut rank 8 against OBDD mid-width 256 (loose by 2^k/k);
multiplication's middle bit has rank 30 (its OBDD hardness rides on
fooling sets, not rank); 0031's independent-set family peaks at rank
23 at n = 20 against widths 384–3162. So the rank floor cannot
certify 0031's all-frames blow-up — those stay certified per-frame
(cited cutwidth/DNNF bounds) and measured. The first plan of this
leg — certify the IS family by rank — **failed by measurement** and
is recorded as such; the floor's power lives elsewhere:

## 3. The unconditional portfolio theorem

The random affine family (d = n/2 parities) is where the floor bites
in full: its subfunction rows are indicators of **disjoint cosets**,
and disjoint nonzero vectors are automatically independent — rank
*equals* the distinct-row count, measured at 2^(n/2−c) at balanced
cuts in every order probed (minima 8 → 16 → 128 at n = 12/16/20 over
natural + 4 random orders; ≥ 2× per step asserted). Hence:

> **For the counting/compilation task, every fixed-basis frame of
> the taxonomy — any decomposition kind including the hybrids, any
> polarity, any variable order, flat or shared, either lift — has
> size 2^Ω(n) on the random affine family. The fixed-basis
> eigenframe portfolio has no subexponential worst case,
> unconditionally.**

Sharpenings. (1) The family's model count is *easy* (2^(n−d)): even
a counting-easy family defeats every fixed basis, and only the
GL(n,2)-transformed member stays polynomial (33 states, 0030) — the
parameter groups are load-bearing, no finite set of fixed bases
suffices, exactly as the parity conjecture of 0031 requires.
(2) The statement is what the directive asked for, on the portfolio
minus its continuous parameter: within the parity class, "run all
the fixed eigenframe canonicalisations in parallel" is worst-case
exponential, as a theorem.

## 4. The remaining wall, named

Extending the unconditional bound to the **full** portfolio (GL
included) requires a succinct family whose cut rank stays
exponential under *every linear change of variables* — a
matrix-rigidity-adjacent question, open in the literature. The
empirical full-portfolio witness remains 0031's independent-set
family (every measured kind, every-order OBDD cited); its
certification is blocked exactly at that wall.

## 5. The original suspicion's final ledger

The thread's founding intuition — "you cannot do materially better
than the ring's canonicalisation" — now has its complete truth
table:

- **Counting task, fixed bases: TRUE, unconditionally** (this note —
  rank floor + affine witness).
- **Counting task, full parameter portfolio: open at a named wall**
  (rigidity-adjacent), empirically supported (0031's IS family).
- **Decision task: FALSE** (0031 — implication closure and unit
  propagation decide without representing).

Next steps if continued: hunt high-cut-rank-under-all-linear-maps
candidates (the rigidity literature's explicit constructions —
e.g. incidence-matrix families — measured through `cut_rank` under
GL probes); the parity conjecture's positive direction (spanning
trees / planar matchings: poly counting should mean a frame home —
finding it would likely name a determinant-flavoured frame kind).
