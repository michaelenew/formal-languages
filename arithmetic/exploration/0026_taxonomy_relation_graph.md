# 0026 — The taxonomy relation graph, completed: the automaton is the universal sink

All ten pairs among the five frames {ANF, dual ANF, minterm, Walsh,
automaton} are now classified into the three relation types
established in 0024/0025 — conjugate (mutual product uncertainty),
ordered (one-way simulation at a stated rate), free (all four joint
cells inhabited, no law either way). Machine checks:
`output/taxonomy_relation_graph.py`.

## The graph

    Walsh ──n^log σ──►  ANF    ──2^crossing──►  automaton
      │ ╲──n^log σ──►  dualANF ──2^crossing──►  automaton
      │ ╲─────────────2^d──────────────────────►  automaton
      ║ conjugate (Donoho–Stark, tight)
    minterm ─────────(n+1)·(models+1)──────────►  automaton

    free: ANF × dualANF,  ANF × minterm,  dualANF × minterm

| pair | type | mechanism / rate |
|---|---|---|
| minterm × Walsh | **conjugate** | Donoho–Stark, tight on subspaces (0024) |
| ANF → automaton | ordered | crossing law, 2^straddle (0025) |
| dualANF → automaton | ordered | complement symmetry |
| Walsh → automaton | ordered | **span law**: 2^d, d = dim⟨Walsh support⟩ |
| minterm → automaton | ordered | **path law**: (n+1)(μ+1), *linear* |
| Walsh → ANF | ordered | **degree law**: deg₂ ≤ log₂ σ, so n^{log σ} |
| Walsh → dualANF | ordered | complement symmetry |
| ANF × dualANF | free | four cells measured |
| ANF × minterm | free | four cells measured |
| dualANF × minterm | free | complement symmetry |

The symmetry doing triple duty: dual ANF is ANF conjugated by the
full complement, and model count, Walsh support, and automaton size
are all invariant under that conjugation (verified) — so every
ANF-edge transfers verbatim.

## The three new laws

**Path law (minterm → automaton), linear rate.** With μ models, each
cut carries at most one distinct subfunction per model prefix plus the
zero subfunction: automaton ≤ (n+1)(μ+1). Verified on 200 random
sparse-model statements. Converse fails exponentially (at-least-one:
4095 models, 25 states). *The cheapest edge in the graph* — the
semantic frame flows to the automaton at linear cost.

**Span law (Walsh → automaton), rate 2^d.** The span of the Walsh
support is the smallest linear map L the statement factors through
(f = g∘L); the automaton need only carry the d running parities of
L's rows, so automaton ≤ (n+1)·2^d + 2. Verified on random factored
functions (rank 2–4), with d, not the possibly-much-larger support
σ ≤ 2^d, setting the rate. Converse fails exponentially.

**Degree law (Walsh → ANF), quasipolynomial rate.** deg₂(f) ≤ log₂ σ
— verified **exhaustively over all 65,536 functions of 4 variables**
(0/1-transform convention; the signed and plain spectra differ only in
the zero coefficient, and the law lives on that difference: parity has
signed support 1, plain support 2, degree 1). Known in the Fourier
sparsity literature; grounded here by exhaustion. Hence ANF terms ≤
Σ_{k ≤ log σ} C(n,k) ≈ n^{log σ}, and the n-dependence is genuine:
AND of two (n/2)-variable parities has σ = 4 forever while its ANF
grows as (n/2)². Converse fails exponentially (single monomial: 1 term,
full support).

## The headline

> **The automaton is the universal sink of the taxonomy.**
> Concentration in *every* other frame flows to it — linearly from the
> semantic frame, at 2^crossing from the ring frames, at 2^span from
> the spectral frame — and it forces nothing back: at-least-one
> (25 states) simultaneously defeats ANF, minterm and Walsh, and the
> full monomial (25 states) defeats dual ANF and Walsh.

This closes the "does the DFA deserve its seat" question with a
stronger answer than the forcing argument of 0023: the automaton does
not sit *across from* the sentence frame as a peer. It sits
*downstream of everything*. Whatever frame knowledge happens to be
concentrated in, the automaton inherits that concentration at a known
rate — which is the precise reason a K-workflow built on the automaton
frame was robust across every statement family this thread has thrown
at it, and why no other single frame could have played that role: every
other frame has an exponentially-costly blind spot against some
neighbour; the automaton alone has none against any of them.

The residual structure of the graph is equally clean: one conjugate
axis (minterm × Walsh — counting versus spectrum, a genuine
uncertainty tradeoff, orthogonal to the flow) and a free triangle
among {ANF, dualANF, minterm} (polarity/semantics: no constraints at
all). QM's homogeneous geometry does not survive: the frame space is
a *directed flow with one conjugate axis across it*.

## Honest scope notes

- "Automaton" throughout = quasi-reduced OBDD in a stated order; the
  sink property is per-frame (order fixed). The rates degrade under
  adversarial order (0025 §4), but the *existence* of the ordered
  edges is order-uniform: the laws hold for every order, with the
  order-dependent quantities (crossing) where noted; the path, span
  and degree laws as stated are order-free.
- The degree law's exhaustive base is n = 4; the general statement is
  cited to the Fourier-sparsity literature rather than reproved.
- Frames outside the five (affine rotations, mixed Kronecker
  polarities) inherit classifications by conjugation where the
  relevant invariants are preserved; a full audit of the extended
  family is not done here.

## What this leaves open

- The lower halves of the ordered edges (when the rate is achieved vs
  collapses) — the crossing-ceiling question of 0025, now three times
  over.
- Whether any *sixth* genuinely distinct frame escapes the sink — a
  canonical form in which some statement is small while its automaton
  is exponential *and* which is not upstream-dominated by the five.
  The counting argument guarantees hard statements for every frame; it
  does not guarantee another frame with the automaton's sink property.
  Conjecture, recorded: within the Kronecker taxonomy and its affine
  extension, the automaton is the unique sink.
