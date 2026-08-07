# 0012 — The formula surface, and & proved independent

Two things: a direct executable showcase of the basis
(`output/basis_showcase.py`), and a new result closing half of the
independence problem 0008 left open.

## The formula surface

Writing wiring diagrams by hand was obscuring the algebra, so terms
and statements now carry Python operators. Terms:

    x ^ y       symmetric difference     basis
    x & y       intersection             basis
    x << 1      shift filling zero (2x)  basis
    x | y       union                    derived (x ^ y ^ xy)
    x + y       addition                 derived (0008)
    5, 63       integers lift to constants automatically

Statements (automata) carry the three wiring moves, which **are** the
first-order connectives:

    K & H       share    conjunction
    K | H       union    disjunction
    ~K          flip     negation
    K.exists('w')        hide     existential quantification

with comparisons as methods returning statements — `.equals`,
`.at_most`, `.below`, `.contained_in` — rather than bound to `==`,
which would break the ordinary Python contract for terms as values.

The point worth stating plainly: **wiring-closure = first-order
definability**. Once that identification is made, every basis question
becomes a standard definability question, which is what makes the
proof below available.

Sample of the surface, all machine-verified in the showcase:

    b(x)              ((x << 1) ^ 1).equals(z)
    T(x)              (z & ((z << 1) ^ 1)).equals(z)
                       & (z & x).equals(z)
                       & ((((z << 1) ^ 1) ^ z) & x).equals(0)
    x + y             (carry.equals(((x & y) | ((x ^ y) & carry)) << 1)
                       & z.equals(x ^ y ^ carry)).exists('Carry')
    x <= y            exists gap: x + gap == y
    x even            z.equals(w << 1).exists('w')
    x a power of two  ((w + 1).equals(x) & (x & w).equals(0)).exists('w')
    3 | x             x.equals(w + (w << 1)).exists('w')

Canonical sizes for the whole catalog sit between 2 and 6 states.

## New result: & is not derivable from {^, <<, constants}

0008 proved the shift independent (bit-permutation invariance) and
left both remaining independence questions open. One is now closed.

**Theorem.** Intersection is not first-order definable from
{^, <<, constants} over the finite subsets of ℕ.

*Proof.* Let M = (finite subsets of ℕ, ^, <<, constants). Identifying
finite sets with GF(2)[t], ^ is module addition and << is
multiplication by t; scalar multiplication by any polynomial is a
term (sums of shifts), so M is the module GF(2)[t] over itself.

1. **M is stable.** Every module is stable — by Baur–Monk, formulas
   in a module reduce to Boolean combinations of positive primitive
   formulas, which cannot define an infinite linear order. Naming
   constants preserves stability. *(Cited: Baur, Monk, Fisher; see
   Prest, Model Theory and Modules.)*
2. **& would give an infinite linear order.** From {^, &, <<},
   addition is definable by the one-wire carry equation (0008,
   re-verified in the showcase), and then x ≤ y is
   ∃gap: x + gap = y (0011, machine-checked to collapse to the
   2-state comparison automaton). ≤ is a linear order on the infinite
   domain, so M would have the strict order property.
3. SOP implies unstable, contradicting 1. Hence & is not definable
   over {^, <<, constants}. ∎

The shape is worth noting: the *order derivation from 0011* — built
while refuting a conjectured limitation — is exactly what powers this
independence proof. A construction became the load-bearing step of an
impossibility result.

**Still open: is ^ derivable from {&, <<, constants}?** The same
argument does not transfer: (finite sets, &, <<) already defines the
subset order (x ⊆ y iff x & y = x), which has infinite chains, so
that structure is unstable on its own and no contradiction arises.
A different invariant is needed. This is now the single remaining gap
in the basis result.

## Status of the basis

- Generation: the wiring-closure of {^, &, <<} with constants is the
  entire canonical layer (0008, modulo Büchi–Bruyère).
- Necessity of <<: proved (0008).
- Necessity of &: proved (here).
- Necessity of ^: open.
