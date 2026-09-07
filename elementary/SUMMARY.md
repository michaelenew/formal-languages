# Elementary functions from one operator — SUMMARY

**Goal.** Understand Odrzywołek's result that `eml(x, y) = exp(x) − Log(y)`
with the constant 1 generates the scientific-calculator basis of
elementary functions: why it works, what other single-operator bases
exist, what plays the role of an eigenbasis (in the sense of
`arithmetic/0023–0024`), and whether it yields a semantically convex
integration procedure.

## State of the art (this workstream)

**Established here, machine-checked (`output/eml_bases.py`):**

- **Packaging lemma.** For an abelian group (G, ⋆) and a bijection φ,
  `F(x, y) = φ(x) ⋆ inv(φ⁻¹(y))` with the constant `φ(identity)`
  generates φ, φ⁻¹, ⋆ and inv, by four explicit words. EML is the
  instance (ℂ, +), φ = exp, constant exp(0) = 1. The theorem therefore
  splits into an algebraic packaging step (general, cheap: the
  continuous Sheffer/NAND move) and the classical exp-log closure. The
  constant is forced: with e instead of 1 nothing basic appears at
  depth ≤ 4.
- **Other bases.** The lemma gives a family. `exp(x) / Log(y)` with
  constant e (EDL, the multiplicative twin) is EL-universal on a region,
  with words valid on a much thinner region than EML's (subtraction
  keeps imaginary parts bounded, division does not). Four necessary
  conditions with proofs — transcendence, exponential growth, a branch
  point, an inverse — exclude `exp(x) − y`, `x − Log(y)`,
  `exp(x) + Log(y)` (positivity invariant) and `sinh(x) − asinh(y)`
  (parity invariant). EML is the minimal combination passing all four.
- **Eigen-frames.** Differentiation is triangular in the exp/log tower an
  EML tree spells out: exp-generators are eigenvectors
  (`D e^u = u' e^u`), log-generators are Jordan chains (`D log u = u'/u`,
  one level down). EML's two arguments are exactly that split; Liouville's
  theorem says the only way out of the field is through the Jordan tops.
  The additive frame (D, eigenbasis e^{λt}, Fourier) and multiplicative
  frame (θ = x d/dx, eigenbasis x^λ, Mellin) are conjugate by exp —
  `D(g∘exp) = (θg)∘exp` — so EML is the intertwiner packaged with its
  inverse.
- **Convex integration = Risch.** Differentiation is a term rewrite on EML
  trees (`d eml(u,v) = eml(u,1)·u' − v'/v`); integration is Risch on the
  tree's tower, demonstrated on eight trees including four non-elementary
  verdicts. Convexity audit: termination and canonicity hold relative to
  the tower; semantic completeness needs the zero-test on the constant
  field, which for EML constants (the EL numbers) is decidable iff
  Schanuel's conjecture (Richardson), while "≠ 0" is unconditionally
  semi-decidable (EL numbers are computable, Carney 2026). The level
  discipline matches `arithmetic/0034–0035`: the constant field is the
  same language one level down; Ax's theorem closes the function level,
  Schanuel would close the constant level. The one-sided judgment has the
  **opposite polarity** to this repository's: nonzero is certified, zero
  is undecided.
- **Branch cuts.** The reported `ln` word equals Log x − 2πi on the
  negative real axis (exact arithmetic); float64 hides this by rounding
  luck. EML identities are identities of germs / in the differential
  field, not of functions on ℂ.

- **The Gödel ladder (0002).** The integers enter the exp-log world as
  the kernel of exp: x ∈ ℤ ⇔ exp(2πi x) = 1, so the map that makes one
  operator universal (+ carried to ×) is the map that names ℤ. Risch's
  undecidable corner is the ground-term constant problem, which sits
  *below* the Gödel line (no quantifier; open, decidable under Schanuel);
  the line is crossed the moment "has a zero" is asked (Richardson 1968,
  undecidable with sin and |·| over ℝ; Th(ℂ, exp) undecidable since it
  defines ℤ). Ax is the completeness theorem for exp-log rewriting at the
  function level (proved); Schanuel is the same at the constant level
  (conjectured).

- **No everywhere-invertible basis (0003).** Two theorems: words in
  total functions are total (but x/y, ln, 1/x are partial), and words in
  single-valued functions are single-valued (but ln, √ are not); over ℂ
  an injective entire function is affine, so no transcendental generator
  is injective at all, and for exp the failure is exactly ker(exp) =
  2πiℤ. Over ℝ, `sinh(x) − asinh(y)` is a bijection in each slot and,
  with constant asinh(1/2), generates 0, +, −, sinh, asinh and e^{±x}
  exactly (e^x = sinh x + sinh(x+c) − sinh(x−c), checked), but provably
  never ln or division. On the log Riemann surface exp and ln are
  mutually inverse bijections and every EML identity holds at every
  point: the cut is a projection artifact.

- **Two bridges (0004).** Every non-universality invariant is a clone
  membership argument (Pol–Inv; positivity ↔ Post's T₁, parity ↔ the
  self-dual class D), so 0001 §2b is the necessary half of a Post-style
  criterion whose sufficient half is open over an infinite domain. The
  packaging lemma is the EL analogue of a Webb function. Totality and
  single-valuedness are spectral properties of θ = x d/dx at a point:
  poles = negative eigenvalues, roots = non-integer eigenvalues, log =
  the Jordan block at eigenvalue 0, essential singularities = spectrum
  unbounded below; in the Mellin domain θ is multiplication by −s, log
  is d/ds, a pole shrinks the strip (all checked). The monodromy of log
  is unipotent, (M − I)² = 0 — the same obstruction as the unipotent
  translations of `arithmetic/0024`, cured the same way, by a lift.

**Plausible, not proved:** the EL class is not closed under elementary
integration (∫dx/(x⁵ − x − 1) needs the S₅ roots; an instance of Chow's
conjecture that some algebraic numbers are not EL).

## Files

- `exploration/0001_eml_packaging_bases_and_frames.md` — the lemma, the
  basis family and necessary conditions, the search table, the
  eigen-frame reading, the integration audit, branch cuts, open items.
- `exploration/0002_the_godel_ladder.md` — where undecidability enters
  (the kernel of exp), the decidability ladder with the status of each
  rung, and the exact correspondence with this repository's ceiling.
- `exploration/0003_everywhere_invertible_bases.md` — why no basis can
  consist of everywhere-invertible generators, the real Latin-square
  operator and how far it gets, and invertibility on the log surface.
- `exploration/0004_two_bridges_post_and_the_theta_spectrum.md` — the
  invariants as Post classes; the obstructions as the local spectrum of
  x d/dx and its Mellin picture; the shared unipotent block with 0024.
- `output/eml_bases.py` — identities and the cut defect (exact and
  float), the lemma on four instances, the closure search over twelve
  candidate operators, explicit words with node counts for the whole
  calculator basis, the non-universality invariants, differentiation
  and Risch on EML trees, the intertwiner. Run directly (~15 min, the
  search dominates; `QUICK=1` skips the search and runs in seconds).

## Next steps, in order of leverage

1. Settle the mirror `Log(x) − exp(y)`: find a word for 0 from some
   constant, or an invariant excluding it.
2. Uniform subtraction: does any EML word equal x − y on all of ℂ²? A
   proof either way would sharpen what "calculator" means for EML.
3. Prove non-closure under integration for ∫dx/(x⁵ − x − 1) (needs: the
   roots of x⁵ − x − 1 are not EL numbers).
4. A canonical form for EML trees themselves (the tower normal form
   with a fixed generator order), and the rewrite system realising it —
   the analogue of ANF for this language; its cost profile against tree
   size is the uncertainty question of `arithmetic/0024` one level up.
