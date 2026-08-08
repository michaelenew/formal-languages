# 0029 — The matrix completed: the up-zeta law, the triad, and the subexponential cell

Target: fill in the flow matrix — the four unmeasured cross-polarity
shared cells and the one open law cell (Walsh → OBDD). All five are
now settled. Machine checks: `output/matrix_completion.py`; figure
regenerated (`output/frame_flow_grid.png`).

## 1. The up-zeta law: the negFDD joins the trio

Negative Davio's two moves are substitute-at-1 (keeps every monomial,
strips the variable) and derivative (keeps only monomials containing
it). A choice sequence with derivative-set D therefore keeps exactly
the monomials whose left part **contains** D, so:

    negFDD width at a cut = distinct entries of ζ↑v,
    (ζ↑v)(D) = ⊕ fiber(D') over supersets D' ⊇ D

— verified exact at every cut of 200 random statements, with ζ↑ an
involution like its down-set partner. The trio is complete: **the
three shared frames read one fiber vector three ways** —

    FDD     v        (point mass)
    OBDD    ζ↓v      (down-set sums)
    negFDD  ζ↑v      (up-set sums)

Complementing the address variables reverses the subset lattice,
exchanging ζ↓ with ζ↑ — so the whole polarity square closes by
conjugation, and 0028's ζ-conjugacy generalises from a pair to a
triangle of frames around one vector.

Corollary, the **anti-fiber ceiling**: negFDD width ≤ 2^t for a
t-term ANF (each up-sum selects a subset of the ≤ t nonzero fibers),
the exact mirror of the crossing law's 2^straddle — so ANF flows
linearly to its own sharing (fiber law) and exponentially to the
*opposite-polarity* sharing, completing the pattern of 0028 §1.

## 2. The triad, and the four cross-polarity cells

Three statements, each the unique killer of one shared frame
(k = 8, n = 16, measured):

                            OBDD    FDD   negFDD
    windowed parity         1021     95     103      (v on singletons)
    one-hot multiplexer       95    774     103      (= ζ↓ image, 0028)
    co-one-hot multiplexer    95    102    1021      (= address-reversed)

Pairwise incomparability of all three shared frames is now measured
in both directions for every pair. The four formerly-hatched cells:

- **ANF → negFDD: E.** The co-singleton selector
  (⊕ᵢ x_{[k]∖i}·dataᵢ, t = 8 terms) forces negFDD width 256 = 2^t —
  the anti-fiber ceiling, reached (up-sums over co-singleton lefts
  shatter).
- **dualANF → FDD: E.** Its full complement, measured directly (not
  just starred): 8 dual terms force FDD width 256.
- **FDD → negFDD: E.** Co-one-hot mux: FDD 102, negFDD 1021.
- **negFDD → FDD: E.** One-hot mux: negFDD 103, FDD 774.

Also upgraded from starred to measured: negFDD → OBDD (wp: 103 vs
1021) and OBDD → negFDD (co-mux: 95 vs 1021).

## 3. The Walsh → OBDD cell: resolved per-frame, subexponential

The **binary-address multiplexer** (k address bits, 2^k data bits,
n = k + 2^k) is the classic dimension-versus-sparsity extremal shape:

    k   n    Walsh σ   dim d   OBDD address-first   OBDD data-first
    2   6      17        6            21                    37
    3  11      65       11            59                   533
    4  20     257       20           183               131,349

σ = 4^k + 1 = Θ(n²) — and the spectrum is order-free — yet the
data-first frame must remember every data assignment before reading
the address: OBDD ≥ 2^(2^k) = 2^(n−k). So **within a fixed frame the
cell is E**: Walsh-small does not force OBDD-small.

But the escape is *exactly subexponential* in the Walsh size: the
span law caps OBDD at (n+1)·2^d in every order, Fourier dimension
obeys d = O(√σ·log σ) (Sanyal 2015, cited; consistent here — d = n
against σ ≈ 4n²), and the multiplexer meets 2^Θ(√σ). Rate
**2^Θ(√σ)**, tight up to the log in the exponent — the only cell of
the matrix whose escape is subexponential rather than 2^Θ(n). The
one remaining open refinement is the **best-frame variant**: this
witness is linear in its address-first order, and whether every
Walsh-small statement has *some* order with a small OBDD is not
settled either way.

## 4. The completed matrix

    row \ col   ANF    dualANF  minterm  Walsh   OBDD      FDD     negFDD
    ANF          ·      E        E        E       E 2^str   P fib   E 2^t
    dualANF      E      ·        E *      E *     E * 2^str E 2^t   P fib *
    minterm      E      E *      ·        CONJ    P path    E 2^μ   E 2^μ *
    Walsh        QP     QP *     CONJ     ·       E sub     QP      QP *
    OBDD         E      E *      E        E       ·         E mux   E comux
    FDD          E      E        E        E       E wp      ·       E comux
    negFDD       E *    E *      E *      E *     E wp      E mux   ·

No unmeasured cells remain. Structure of the completed object: three
green own-sharing edges (path, fiber, fiber*), the Walsh row gentle
(QP into the whole Davio side, subexponential into Shannon-shared),
one conjugate axis, a solid-red 3×3 shared block realised by a
single triad, and everything else full-exponential.

## Status

- The flow matrix over the seven named frames: **complete** (per
  frame; the house convention since 0026 — order and polarity are
  frame parameters).
- Remaining opens, all refinements rather than blanks: the
  best-frame Walsh → OBDD question; the ℤ-lift shared kinds of the
  finite frame conjecture (MTBDD, *BMD, WHDD — a fourth aggregation
  family, presumably a moment analogue of the zetas); the
  non-product refutation surface of the finiteness conjecture.
