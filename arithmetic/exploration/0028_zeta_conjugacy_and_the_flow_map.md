# 0028 — The zeta conjugacy, the transported witness, and the complexity flow map

Directive for this leg: do the Davio-side analogue first, then verify
the literature's claim. Both done — and doing them in that order is
what closed them, because the Davio analogue *implies* a construction
for the literature witness. Machine checks: `output/frame_flow_map.py`.

## 1. The fiber law (the Davio-side crossing law), exact

Fix an order and a cut after the first k variables. Write the ANF as
a **left-fiber vector**: for each subset D of the cut variables,

    fiber(D) = XOR of the right parts of the monomials whose left
               part is EXACTLY D.

**Fiber law.** FDD width at the cut = number of distinct entries of
the fiber vector. Verified as an equality at every cut of 200 random
sparse statements. (Mechanism: the positive-Davio children are
g ↦ g mod x and g ↦ ∂g/∂x; a length-k choice sequence kills every
monomial whose left part is not exactly the derivative-set, so the
reachable nodes at the cut are precisely the fiber values.)

Two corollaries, immediate:

- **ANF → FDD is LINEAR**: at most one distinct nonzero fiber per
  monomial, so FDD ≤ (n+1)(terms+1). The Davio mirror of the path
  law. Verified.
- **minterm → FDD is EXPONENTIAL, ceiling 2^μ** (the survivor law):
  a sparse-model statement's reachable Davio nodes are XOR-subsets
  of per-model suffix deltas selected by a down-set rule, so width
  ≤ 2^models; the ceiling is *reached* by one-hot-prefix models
  (μ = 8 models force FDD width 256 = 2^8 while the OBDD sits at 71
  by the path law). Verified.

So the flat → shared square completes as a perfect mirror:

                     → OBDD (shared Shannon)   → FDD (shared Davio)
    minterm (flat S)  path law     LINEAR       survivor law  2^μ
    ANF     (flat D)  crossing law 2^straddle   fiber law     LINEAR

**Each flat frame flows linearly into its own shared form and
exponentially into the other's.** 0027's "sharing is the sink-maker"
gains its precise form: sharing is a sink only for its own
decomposition; cross-decomposition flow pays an exact image-size
ceiling.

## 2. The zeta conjugacy of the shared frames

0027's exact crossing law says the OBDD's subfunctions at a cut are
the XORs of *down-set-selected* right parts. Re-read against the
fiber law, that is the statement:

    OBDD width = distinct entries of ζv,  where (ζv)(P) = ⊕_{D⊆P} v(D)
    FDD  width = distinct entries of v            (v = fiber vector)

and over GF(2) the zeta transform ζ is an **involution** (ζ∘ζ = id;
the Möbius function is 1 everywhere mod 2). Both facts verified
entrywise at every cut of 40 random statements. Hence:

> **The two shared frames are ζ-conjugate, cut by cut.** One vector;
> two aggregations — point-mass (Davio) and down-set evaluation
> (Shannon) — exchanged by an involution. Every separation witness in
> one direction maps under ζ to a witness in the other direction.

## 3. The literature witness, derived rather than hunted

0027 could not reproduce the cited reverse BDD/FDD separation
(OBDD-small, FDD-big) and recorded it as the honest gap. The
conjugacy turns the hunt into a computation: **transport the known
witness**. Applying ζ to windowed parity's fiber vector
(w({i}) = {data_i}, else 0) gives fiber(L) = {data_i : i ∈ L} — which
is the fiber vector of the **one-hot multiplexer** (output = the data
bit selected when the address is exactly one-hot). Verified
entrywise; the expanded ANF reproduces the multiplexer's truth table.
Measured (k = address width, n = 2k):

    k    OBDD(mux)  FDD(mux)     OBDD(wp)  FDD(wp)
    6        59        196          253       59
    7        76        389          509       76
    8        95        774         1021       95

FDD(mux) ≥ 2^k against a linear OBDD: **both directions of the
shared-frame separation are now measured**, closing the one
citation-only claim in the corpus (Becker–Drechsler et al.). And the
postmortem on 0027's failed hunt is structural: it searched counting
families, but the ζ-image of a parity-accumulator is a *selector*.
A pleasing measured detail: OBDD(mux) = FDD(wp) exactly at every k —
the involution visible in the raw sizes (address-side widths exchange
by ζ; the data-side residues of the two functions happen to match
width-for-width).

## 4. The flow matrix

All frame pairs over {ANF, minterm, Walsh, OBDD, FDD}, dual ANF
folded by the complement symmetry (its cells mirror against the
negative FDD):

    row \ col   ANF     minterm  Walsh    OBDD          FDD
    ANF          ·       E        E        E 2^straddle  P linear
    minterm      E       ·        CONJ     P linear      E 2^μ
    Walsh        QP      CONJ     ·        B 2^span *    QP composed
    OBDD         E       E        E        ·             E (mux)
    FDD          E       E        E        E (wp)        ·

P = polynomial law; QP = quasipolynomial (degree law; Walsh → FDD
composes degree law with fiber law, verified on AND-of-parities);
E = witnessed exponential escape; CONJ = the Donoho–Stark axis.
The starred cell is the matrix's **one open cell**: the span law
bounds Walsh → OBDD by 2^d, Fourier dimension can reach ~√support
(Sanyal), but the natural candidate there is an addressing function —
which is OBDD-small — so no witness either way.

Readings: the two shared frames are pure sinks (rows all E) and
mutually incomparable (both witnesses measured, §3); each flat frame
drains linearly into its own sharing; Walsh is the gentle upstream of
the *Davio* side specifically — its Shannon-side rate is the open
cell; the conjugate axis crosses the flow; 0026's free triangle
stays free.

## 5. The finite frame conjecture, and where complexity flows

**Finiteness.** A frame is an eigen-frame when it diagonalises a
commuting family generated by the logic's own primitives — and the
logic has finitely many primitives (the basis theorem): ^ gives
translations, & gives restriction idempotents, << gives the shift
(sharing = its quotient), flip gives complement conjugation. One
coordinate over GF(2) is exhaustively enumerable: exactly three
bases (Shannon, positive Davio, negative Davio) — re-verified — and
over the ℤ lift the eigen-condition adds finitely many more (point
evaluations, moments, Walsh — the last existing only there because
translations are unipotent over GF(2)). **Conjecture: every
eigen-frame is, up to the parameter moves (order, polarity, GL(n,2)
change of basis), one of at most fourteen kinds** — {Shannon, ±Davio}
× {flat, shared} over GF(2), plus {Walsh, ±moment} × {flat, shared}
over ℤ; six are this thread's named frames, the rest are the decision
diagram literature's (MTBDD, *BMD, WHDD). Finitely many kinds,
infinitely many parameters, and the parameters are already classified
(order 0025, polarity 0024, sharing 0027/here). Refutation surface: a
diagonalising frame not conjugate into the grid — necessarily a
non-product basis or a non-abelian operator family, since the
per-coordinate product case is closed by enumeration.

**Complexity flow.** Read the matrix as subclasses (C_F = statements
polynomial-size in F):

- C_minterm ⊆ C_OBDD and C_ANF ⊆ C_FDD — P is preserved along the
  two linear edges (each flat frame's problems stay feasible in its
  own shared frame).
- C_Walsh sits inside quasipoly of C_ANF, hence of C_FDD.
- C_OBDD and C_FDD are incomparable; C_minterm and C_Walsh are
  conjugate (never both, past the Donoho–Stark bound).
- Every other frame move has a witnessed P → E escape.

The P/E boundary is a property of a problem *together with a frame*,
and the matrix states exactly which frame changes preserve it. The
deepest reading ties back to the sentence basis: **the two shared
frames split {^, &} between them** — the OBDD executes all
connectives polynomially in its size but pays 2^straddle to receive
parity-shaped knowledge; the FDD receives the whole ring frame
linearly but worst-case conjunction on it is exponential (literature).
A counting/threshold K (Clue) is polynomial on the OBDD side; a
parity-constraint K (Tseitin) is polynomial on the FDD side; a K
needing both at once has no home frame — which is where 0018's
coNP-hardness lives.

## Status

- Davio-side analogues: crossing → fiber law (exact), path → survivor
  law (exact, ceiling reached); the span/degree Davio analogues are
  subsumed by composition (Walsh → FDD quasipoly).
- The literature's both-direction BDD/FDD separation: **verified by
  machine**, witness derived by ζ. 0027's honest gap is closed.
- Open: the matrix's one open cell (Walsh → OBDD tightness); the ℤ
  row of the grid (*BMD, WHDD cells unmeasured); the non-product
  refutation surface of the finiteness conjecture; FDD-side
  conjunction cost measured rather than cited.
