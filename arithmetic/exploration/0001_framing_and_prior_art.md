# 0001 — Framing, and where this sits in known theory

## The framework (per the clue/ corpus)

*Originally written as a reconstruction while the Clue files were
unreachable; now corrected against the recovered corpus, chiefly
`clue/2026-06-21 AI exploration.md`. See 0004 for the full reconciliation.*

- Statements are **object-level set expressions asserted empty**: the
  expression's symbols denote sets of import (`alice`'s hand, the card
  `lead_pipe`), and the statement is the assertion that the expression
  equals ∅, which is TRUE (written 0). E.g. `alice & lead_pipe` asserts
  alice does not hold the lead pipe.
- Operators: `^` (symmetric difference / XOR), `&` (intersection / AND,
  juxtaposition allowed), and the constant `1` (the universe). Functionally
  complete; union is derived: `a U b = a ^ b ^ ab`.
- Knowledge is one statement K, updated by union — `K := K U A` — sound
  because a union is empty iff both operands are (conjunction of empties).
- The deduction test: hypothesis H is knowably true from K iff `KH ^ H`
  (= `H & (1 ^ K)`) rewrites to 0, i.e. iff H is syntactically contained
  in K. Containment "a ⊆ b" is itself the term `ab ^ a`.
- Semantic convexity as the corpus defines it: a Galois alpha-map onto the
  semantics, plus a rewrite system converging to a unique canonical form
  (for the {^, &, 1} core: the multilinear XOR-of-AND-terms form). The
  formulation in the next section unpacks the same property operationally
  and adds one demand the corpus states informally ("knowably
  terminating"): the termination bound must be evident from the term.

## Semantic convexity, made precise

A language L with reduction relation → is **semantically convex** iff:

1. → is computable and terminating, with a termination bound *evident from
   the term itself* (no cleverness: the bound is read off syntactically,
   e.g. from a max element or a popcount);
2. normal forms are unique (confluence), so "reduce" is a function;
3. a sentence's normal form is 0 iff the sentence is semantically true.

Consequences. Truth of representable sentences is *decidable*. The judgment
is one-sided: a sentence reduces to 0 (true) or it does not (undecided);
there is no falsity judgment. H may reduce to 0, its converse may, or
neither may — the three-way situation from the synopsis.

## Where each piece lands in prior art

These are established results, cited to position the work, with their exact
limitations noted.

**1. The propositional core is the Zhegalkin algebra (1927).** {XOR, AND, 1}
over GF(2) is functionally complete, and every Boolean function has a
*unique* multilinear polynomial (algebraic normal form, ANF). Uniqueness of
ANF is exactly clause (2) of convexity for the propositional fragment, and
polynomial normalization is the no-cleverness reduction. This is good news
(the core is on bedrock) and a boundary: ANF normalization is worst-case
exponential in the number of atoms, so convexity here says nothing about
*efficiency*, only decidability with evident termination.

**2. The Gödel-skirting has a precise shape.** The framework's one-sided
judgment does not by itself escape incompleteness — decidability is the
real constraint, and the map of decidable arithmetic is known:

- (ℕ, +) — Presburger 1929: decidable, complete, admits quantifier
  elimination (in the language extended with ≤ and congruences ≡ mod m).
- (ℕ, ×) — Skolem arithmetic: decidable.
- (ℕ, +, ×): undecidable, and not just for quantified sentences — by
  Matiyasevich (Hilbert's 10th), even the ∃-fragment is undecidable.

So: **no semantically convex syntax can interpret both + and × with their
full semantics.** A convex reduction would be a decision procedure, which
cannot exist. The ceiling is sharp, and "addition first" is not merely a
first step — Presburger arithmetic (+, ≤, congruences, and anything
definable from them, including multiplication by constants) is essentially
the *maximal* convex arithmetic in the additive direction.

**3. Numbers-as-bitsets is the Büchi–Elgot encoding.** Defining n as the
set of positions of its binary 1-bits is precisely how WS1S (weak monadic
second-order logic of one successor) encodes arithmetic. Büchi–Elgot–
Trakhtenbrot: WS1S-definable = regular, hence decidable. Addition is an
*automatic* relation — a 3-track synchronous DFA with two states (carry
0/1) checks x + y = z reading binary lsb-first. This suggests the candidate
canonical form for the infinite game: the **minimal DFA**, canonical by
Myhill–Nerode, with equivalence and emptiness decidable. Multiplication is
not an automatic relation (else arithmetic would be decidable) — the same
ceiling seen from the automata side.

**4. Why set sizes broke in the infinite game — a diagnosis.** Counting is
the classic non-regular property: equicardinality |X| = |Y| of arbitrary
finite sets is not WS1S-definable (pumping: it would make {aⁿbⁿ}-style
languages regular). So the difficulty representing set sizes is not a
defect of the particular syntax tried — *no* convex syntax whose sentences
denote regular/automatic predicates over raw sets can express cardinality
of arbitrary sets. The escape consistent with the ceiling: make numbers
first-class and keep constraints in Presburger form — a hand is related to
its *size counter* by explicit additive bookkeeping (built from the addition
of 0002), rather than by a cardinality operator applied to an arbitrary
set. Finite Clue gets this for free; infinite Clue gets it iff the game's
constraints can be phrased additively (they can for "exactly n cards"
deals; see SUMMARY next steps).

**5. The product musing, placed.** The synopsis floats an operator with
"zero iff either operand is zero" — a genuine OR at the truth level, since
statements are expressions asserted empty. Two candidates:

- Intersection is already in the algebra but gives only the *if* direction:
  X & Y = ∅ follows from either being empty, yet also holds for disjoint
  nonempty sets — so `KH` in the deduction test is a sound weakening, not a
  disjunction.
- The exact law needs Cartesian-product-with-collapse (positions add,
  i + j): X × Y = ∅ iff X = ∅ or Y = ∅. Numerically this *is*
  multiplication (2^i · 2^j = 2^(i+j); the general product is the
  carry-convolution) — and it is exactly where undecidability enters
  (point 2).

So the honest OR is inseparable from arithmetic product, and its full
symbolic use is priced at the ceiling. Clue's needs are counting needs,
which stay on the additive (decidable) side. Speculative but suggestive:
unrestricted disjunction-via-product internalizes unbounded interaction of
positions — the same phenomenon Matiyasevich exploits — not pursued
further here.

## Reading order

0002 gives the constructions and proofs; `output/bitset_arithmetic.py` is
the verified implementation (its assertions check the termination measures,
not just answers); 0003 is the verification log; 0004 reconciles this
workstream with the recovered clue/ corpus (notation map, which of its open
asks are now closed, and where the ceiling redirects one of them).
