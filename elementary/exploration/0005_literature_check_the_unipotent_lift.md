# 0005 — Literature check: the "shared unipotent block" of 0004 §3 is standard, twice

0004 §3 called it a surprise that the log's monodromy and the GF(2)
translations of `arithmetic/0024` are both unipotent operators with no
eigenbasis, both cured by a lift. Checked against the literature: both
halves are textbook, and the *pairing* is the ordinary way each field
already thinks. Recorded here so the claim is downgraded from "surprise"
to "recognised instance", with pointers.

## 1. The analytic half: unipotent monodromy is the definition of a log pole

- **Fuchs / Frobenius / Nilsson.** At a regular singular point every
  solution is a finite sum of x^λ · g(x) · (log x)^k with g holomorphic;
  these are the Nilsson-class functions, and in one variable regularity
  is *equivalent* to this form. The Mellin transform of such a term has
  a pole of order k + 1 at −λ: the log is exactly the extra pole order.
  This is the whole of 0004 §2's table, stated in the standard language
  (Nilsson 1965; any Fuchsian-ODE text; recent survey
  [arXiv 2406.14253](https://arxiv.org/pdf/2406.14253), Mellin form in
  [arXiv 2304.04538](https://arxiv.org/pdf/2304.04538)).
- **Deligne's canonical extension.** A flat connection with *unipotent*
  local monodromy extends canonically to a bundle whose connection has
  logarithmic poles with nilpotent residues; the residue is
  N = log(T_u) = −Σ (1/k)(I − T_u)^k, a finite sum because T_u − I is
  nilpotent. So "unipotent monodromy ⇔ logarithmic pole with nilpotent
  residue" is a theorem, and the 2×2 block (M − I)² = 0 of 0004 is its
  smallest case. (Deligne, *Équations différentielles à points
  singuliers réguliers*, 1970; see
  [arXiv 0710.2869](https://arxiv.org/pdf/0710.2869),
  [arXiv math/0405069](https://arxiv.org/pdf/math/0405069).)
- **The monodromy theorem.** Local monodromy of a geometric family is
  always *quasi*-unipotent (Grothendieck, Landman): some power is
  unipotent. The semisimple part carries the roots-of-unity phases
  (0004's ℚ row, algebraic branching), the unipotent part carries the
  logs. So the two multivaluedness rows of 0004's table are the Jordan
  decomposition T = T_s T_u of one operator, which is how the subject
  states it.
- **Log geometry.** Kato's log structures and Hyodo–Kato cohomology
  build the nilpotent monodromy operator N into the geometry itself: the
  triple (D, φ, N) with N nilpotent is the arithmetic-geometry version of
  "the log is a Jordan chain". The word "log" in "log structure" is
  literally this logarithm. ([Hyodo–Kato 1994](https://www.numdam.org/article/AST_1994__223__221_0.pdf),
  [arXiv 1802.02234](https://arxiv.org/abs/1802.02234).)

The "lift" of 0003 §3 (pass to the universal cover, where M becomes the
translation log x ↦ log x + 2πi) is likewise standard: it is the passage
from the local system to its canonical extension, or in the Kato–
Nakayama picture, to the real blow-up where the log becomes a
coordinate.

## 2. The finite-field half: representations of 2-groups over GF(2) are unipotent

- For a cyclic group of order pᵃ acting on a vector space over a field
  of characteristic p, the generator satisfies (T − I)^{pᵃ} = 0, so the
  only eigenvalue is 1 and every indecomposable representation is a
  single Jordan block. 0024's (T_a + I)² = 0 over GF(2) is the case
  p = 2, a = 1, and "no eigenbasis" is the statement that the regular
  representation of ℤ/2 over GF(2) is one 2×2 Jordan block.
  (Any modular representation text; e.g.
  [Bump's lectures](https://math.berkeley.edu/~fengt/mod_rep_theory.pdf).)
- The cure is also standard: **Brauer characters** are defined by
  lifting eigenvalues from characteristic p to characteristic 0 through
  a chosen isomorphism of roots of unity (Teichmüller lift / Witt
  vectors). The Walsh–Hadamard frame of 0024 — characters ±1 of an
  elementary abelian 2-group, which exist only after lifting
  coefficients to ℤ — is precisely the Brauer-character lift for that
  group. ([Brauer characters](https://www.cambridge.org/core/books/abs/course-in-finite-group-representation-theory/brauer-characters/336B89EC77F6639C324BACA822A3B119),
  [Teichmüller character](https://en.wikipedia.org/wiki/Teichm%C3%BCller_character).)

## 3. Verdict on the pairing

Both are instances of one elementary fact: a unipotent operator on a
module over a ring where it cannot be diagonalised becomes tractable
after a change of coefficients or of base — characteristic 0 for the
group ring, the universal cover (or the canonical extension) for the
monodromy. The two fields even meet: Hyodo–Kato's N lives in a p-adic
setting where both lifts (Witt vectors *and* log structures) are in play
at once. So the correct statement for this repository is:

> The framework's translations (0024) and the log's monodromy (0004) are
> both unipotent Jordan blocks; the Walsh lift and the universal-cover
> lift are the standard cures (Brauer/Teichmüller lift; Deligne canonical
> extension). Recognised, not new.

What *is* specific to this repository, and not in that literature, is
the reason the two came up together: both workstreams are hunting for
eigenbases that make a rewrite system canonical (convexity), and
unipotence is exactly the obstruction to an eigenbasis. That framing is
the repository's; the objects are old.

## 4. The other bridge, checked

- **Rosenberg's theorem** is for finite domains. On an infinite set the
  number of maximal clones equals the size of the whole clone lattice,
  and under the continuum hypothesis not every clone on a countable set
  is even contained in a maximal one. So 0004 §1's "the sufficient half
  is open" is, more precisely, "has no finite form"; a Post-style
  completeness criterion for EL-universality would have to come from
  the analytic structure, not from clone theory.
  ([survey](https://arxiv.org/pdf/math/0701030),
  [Rosenberg's classification](https://arxiv.org/pdf/math/0211420).)
- **Webb 1935** did show that every finite k-valued logic is generated
  by a single binary operation; the particular formula I quoted
  (max(x, y) + 1 mod k) I could not confirm from the accessible sources,
  so 0004 §1 should be read as "a Webb-type function", formula
  unverified. ([Martin 1954](https://projecteuclid.org/euclid.jsl/1183731786).)
