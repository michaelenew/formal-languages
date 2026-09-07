# 0002 — Where Gödel enters: the integers are the kernel of exp

Follow-up to 0001 §3c–4c. The question: is the undecidable corner in
Risch's algorithm a Gödel phenomenon, and if so through which door?

## 1. The door is periodicity

Gödel-style undecidability enters analysis at one specific point: the
moment a class of expressions can *name the integers*. Once "x is an
integer" is expressible, any question of the form "does this expression
have a zero" contains Hilbert's tenth problem (Matiyasevich: no algorithm
decides whether a polynomial has integer roots), and Gödel/Turing
undecidability follows.

For the exp-log class the integers are already named, and by the very
map that makes EML universal:

    ker(exp : ℂ → ℂ*) = 2πi ℤ,      so      x ∈ ℤ  ⇔  exp(2πi x) = 1.

exp is universal because it carries + to × (the packaging lemma of 0001
rides on this). Its kernel is ℤ for the same reason: periodicity is what
a homomorphism from (ℂ, +) onto (ℂ*, ×) must have. So **the property that
makes one operator suffice is the same property that puts the integers
inside the language.** The arithmetic workstream's ceiling (0001 there:
no convex syntax carries full + and ×) is met here from the analytic
side: exp is the bridge between + and ×, and ℤ sits on the bridge.

## 2. The ladder, with the status of each rung

| problem | class | status | why |
|---|---|---|---|
| identity of two *functions* in an exp/log tower | EL functions | **decidable relative to constants** | Risch structure theorem, resting on Ax's theorem (Schanuel for function fields, proved 1971) |
| is a closed constant term zero | EL numbers | **open**; decidable if Schanuel | Richardson 1997: his procedure terminates on every input iff Schanuel holds. "≠ 0" is unconditionally semi-decidable by evaluation (EL numbers are computable) |
| elementary antiderivative exists | EL functions | same as the row above | Risch reduces it to the constant zero-test |
| does an expression have a *real* zero; is it identically zero | reals with π, exp, sin, \|·\| | **undecidable** | Richardson 1968, via sin(πx) = 0 ⇔ x ∈ ℤ plus \|·\| to turn "has a zero" into "is identically zero"; corollary: elementary integrability is undecidable for that class |
| first-order theory of (ℂ, +, ×, exp) | complex exponential field | **undecidable** | ℤ is definable as ker(exp)/2πi, so the theory interprets arithmetic |
| first-order theory of (ℝ, +, ×, exp) | real exponential field | **decidable if Schanuel** | Macintyre–Wilkie 1996; real exp is not periodic, so ℤ is not definable (o-minimality) |

Two things the table makes visible.

**The Risch corner is not Gödel; it sits below Gödel.** Risch asks a
*quantifier-free* question about one closed term: is this specific
constant zero. Gödel/Matiyasevich need a quantifier ("there exists an
integer solution"). The EL constant problem sits strictly between ground
arithmetic (is 2 + 3 − 5 zero: trivial) and existential arithmetic
(undecidable): it is a ground-term problem whose difficulty comes from
transcendence, not from quantifiers. Schanuel's conjecture says it lands
on the decidable side. Nothing known contradicts that, and the
undecidability of Th(ℂ, exp) does not touch it, because a single closed
term cannot quantify over the kernel.

**Where the quantifier appears, undecidability appears at once.** The
moment the question becomes "does f(x) have a zero" over the reals with
sin available, Richardson's construction turns a Diophantine equation
into an expression that vanishes somewhere iff the equation has an
integer solution. Integration is then undecidable *for that class*,
because a suitable integrand has an elementary antiderivative iff a
companion expression is identically zero.

## 3. The correspondence with Gödel, stated precisely

Gödel's theorem has two halves: provability is recursively enumerable
(you can list the theorems), truth is not (there is no complete listing).
The EL constant problem has the same shape with the roles fixed:

- "c ≠ 0" is recursively enumerable: evaluate c to more and more digits;
  a nonzero value eventually shows itself. This is the unconditional half
  (0001 §3c: the opposite polarity to this repository's convexity).
- "c = 0" needs a *certificate* — an algebraic relation among the
  exponentials and logarithms in c. Schanuel's conjecture is exactly the
  claim that every true zero has such a certificate of a fixed syntactic
  form (the only relations are the obvious ones). In the language of this
  repository: **Schanuel is the completeness theorem for the obvious
  rewrite rules on exp-log constants; Ax is the same completeness theorem
  one level up, for functions, and it is proved.**

So the honest correspondence is:

| this repository | exp-log world |
|---|---|
| convexity = completeness of a rewrite system | Ax (functions, proved), Schanuel (constants, conjectured) |
| the ceiling: + and × together over ℤ | exp carries + to ×, and ker(exp) = 2πiℤ |
| ∃-fragment already undecidable (Matiyasevich) | "has a zero" with sin over ℝ undecidable (Richardson) |
| ground terms trivially decidable | ground EL terms: open, the Schanuel rung |

The one genuinely new feature relative to the arithmetic workstream is
the middle rung: transcendence makes even ground terms non-trivial, so
there is a decidability question *below* the quantifier line that
arithmetic does not have. That rung is where Risch lives.

## 4. Consequence for a convex EML language

An EML language with a variable is convex at the function level (Ax)
relative to its constant sub-language, which is EML without the
variable. Its convexity therefore reduces to Schanuel's conjecture, and
to nothing else. It stays below the Gödel line as long as its sentences
are closed terms asserted zero — the same discipline as `K = 0` in the
Clue corpus. Adding "there exists x with T(x) = 0" as a sentence form
crosses the line immediately, by §1. That is the exact analogue of
0005's guarded-convexity boundary in the arithmetic workstream: the
existential over the kernel is the one operator that cannot have a
closed home.

## Open

- Richardson's undecidability uses |·| and real zeros. Whether the
  *identity* problem for real expressions in exp, sin, π *without*
  absolute value is undecidable was settled later in the literature
  (Wang 1974 for zeros; Laczkovich 2003 removes π); I have not re-derived
  those and cite them only as pointers.
- Whether the EL constant problem could be undecidable *without*
  Schanuel failing — i.e. whether there is a route to undecidability that
  does not go through the kernel — I see no mechanism for, and know of
  no result.
