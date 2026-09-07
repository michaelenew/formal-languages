# 0004 — Two bridges: the invariants are Post classes, and the obstructions are the spectrum of x d/dx

Two observations raised in discussion, both confirmed here.

## 1. The composition invariants are Post classes (Pol–Inv)

Every non-universality argument in 0001 §2b and 0003 §1 has the same
shape: a property P such that (i) the leaves have P, (ii) P is preserved
by composition, (iii) some target lacks P. That is exactly a **clone**
membership argument: the set of all operations with property P is
closed under composition and projections, so it is a clone, and the
candidate operator generates only what lies inside it. In Post's
language for Boolean functions, these are the closed classes; in the
Pol–Inv Galois connection (`arithmetic/0013`), each is the set of
polymorphisms of an invariant relation.

| invariant used | closed class | Boolean analogue in Post's lattice |
|---|---|---|
| total (defined everywhere) | total functions | — (all Boolean functions are total) |
| single-valued | trivial-monodromy functions | — |
| polynomially bounded growth | slow-growth functions | — |
| maps [1, ∞) into itself | preserves a subset | T₁ (preserves the constant 1) |
| f(−x, −y) = −f(x, y) | commutes with negation | D (self-dual: f(¬x) = ¬f(x)) |
| algebraic | algebraic functions | — |

Post's completeness theorem says a set of Boolean operations is
complete iff it lies in none of five maximal clones (T₀, T₁, M, D, L).
The EL analogue reads: F is universal only if it escapes each closed
class above. The necessary direction is exactly 0001 §2b. The
sufficient direction — that these (or some finite list) are the maximal
clones below the EL clone — is **not available**: Rosenberg's
classification of maximal clones is for finite domains, and over an
infinite domain the clone lattice is uncountable with no finite list of
maximal clones. So the bridge lands at the same open item as
`arithmetic/SUMMARY` next-step 3 (prove the Post-style criterion),
one domain up.

Two smaller points from the same bridge:

- The packaging lemma (0001 §1) is the EL version of a **Webb
  function**: for k-valued logic, `max(x, y) + 1 mod k` is a single
  binary operation generating everything, built from a lattice
  operation and a cyclic bijection. EML is built from a group operation
  and the bijection exp. Same recipe: one "mixing" operation, one
  bijection, packaged.
- The lemma needs φ(identity) as the constant. In Post terms, the
  choice of constant decides which T-type classes the generated set
  escapes; that is why constant e leaves EML stuck at depth 4
  (0001 §2c) while constant 1 does not.

## 2. Totality and single-valuedness are spectral properties of θ = x d/dx

The two obstructions of 0003 §1, and the algebraic branching of the
stylewarning argument, are all statements about the **local spectrum of
the Euler operator** θ = x d/dx at a point (take the point to be 0).
θ is the operator whose eigenbasis is the power frame (0001 §3b); its
local generalized eigenvectors are exactly the terms of a Nilsson-class
expansion Σ x^λ (log x)^k, which is the local form of every solution of a
Fuchsian equation. Checked symbolically:

    θ x^λ = λ x^λ                       eigenvector, eigenvalue λ
    θ: ½(log x)² ↦ log x ↦ 1 ↦ 0         Jordan chain at eigenvalue 0

So a function's local behaviour is classified by *where its θ-spectrum
lives*:

| local θ-spectrum at the point | function class | which obstruction |
|---|---|---|
| ℕ, no Jordan blocks | analytic (Taylor) | none: total and single-valued |
| ℤ, no Jordan blocks | meromorphic (Laurent) | **totality fails** (poles: 1/x has eigenvalue −1) |
| ℚ, no Jordan blocks | algebraic branching (Puiseux) | **single-valuedness fails**, finite monodromy (√x: eigenvalue ½) |
| ℂ, Jordan blocks allowed | exp-log / Nilsson class | **single-valuedness fails**, unipotent monodromy (log: Jordan block at 0) |
| unbounded below | essential singularity (e^{1/x}) | irregular point: monodromy replaced by Stokes data |

Reading the two obstructions off the table: **totality** = "no negative
eigenvalues"; **single-valuedness** = "integer eigenvalues and no Jordan
blocks". The monodromy operator M (continue once around the point)
acts on the eigenvector x^λ by the phase e^{2πiλ}, and on the log chain
as a unipotent shift:

    M: log x ↦ log x + 2πi,      (M − I)² = 0 on span{1, log x},   M not diagonalizable.

The "zero eigenvalue" in the question is this: the Jordan block of θ at
eigenvalue 0 *is* the logarithm. The "infinite eigenvalue" is the
essential singularity, where the spectrum is unbounded below and exp's
irregular point sits.

The integral transform is the Mellin transform, M[f](s) = ∫ x^{s−1} f dx,
which diagonalizes θ; the obstructions appear in the transform domain
as (checked on f = e^{−x}, whose transform is Γ(s)):

    M[θ f](s)      = −s · M[f](s)            θ is multiplication by −s
    M[log x · f](s) = d/ds M[f](s)           log is differentiation in s: the Jordan block
    M[x^{−1} f](s)  converges only for Re s > 1   a pole shrinks the strip

So a pole of order n moves the boundary of the fundamental strip to
Re s = n, and a logarithm turns a simple pole of the transform into a
double pole. Formally, M[x^a] is a delta at s = −a and M[x^a log x] is
its derivative: eigenvector ↔ delta, Jordan chain ↔ derivative of delta.

## 3. The same unipotent block, one workstream over

`arithmetic/0024` §1 found that translations x ↦ x ^ a over GF(2) are
unipotent, (T_a + I)² = 0, hence have no eigenbasis, and that the fix is
to lift coefficients to ℤ (the Walsh frame lives only after the lift).
Here the monodromy of log is unipotent, (M − I)² = 0, hence has no
eigenbasis, and the fix is to lift the domain to the universal cover
(0003 §3), where M becomes the translation log x ↦ log x + 2πi and log
becomes a coordinate. **Both workstreams meet the same obstruction — a
unipotent operator with no eigenbasis — and cure it the same way, by a
lift.** The branch cut of 0001 §5 is what remains when the lift is
undone by projection.

## Open

- Is there a *finite* list of closed classes whose avoidance is also
  sufficient for EL-universality of a single operator? (The Post/
  Rosenberg question for this clone; expected hard.)
- The table in §2 is local at one point. A global statement would
  assign to each EL function its θ-spectrum at every singular point
  plus Stokes data at irregular ones; whether that data classifies
  EML-expressibility (in the spirit of the monodromy argument for the
  quintic) is worth pursuing.
