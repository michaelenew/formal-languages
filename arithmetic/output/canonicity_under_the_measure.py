"""Canonicity under the measure: what fails, what survives, and the
parameter group.

The question: introducing `|.|` (equivalently `{.}`, 0034 section 3),
does a canonical form survive? The answer is graded, and the middle case
is not the one this file set out to find.

**Unguarded -- no canonical form, unconditionally.** A canonical form
reached by a terminating reduction IS a decision procedure for truth.
Layer + `{.}` is BIT is full arithmetic (0034 section 4), which is
undecidable. So no terminating confluent rewrite system exists -- not
"none found", none exists. The rewrite-side diagnosis is separate and
weaker but concrete: every layer rule is bounded by a syntactic measure
readable off the term (0002), and `{.}` has no such measure, because it
takes a term of bit-length L to one of bit-length 2^L. Measured below.

**Guarded -- the attempted impossibility failed, and instructively.**
The plan was a Pareto obstruction: show control states and registers
trade against each other, so "the smallest representation" is not
well-defined. Every trade that can actually be built turns out to
concern a *regular* sub-part, which the minimal automaton absorbs --
`popcount(x) = 0 mod m` has an m-state register-free presentation and a
1-state one-register presentation, but the language is regular and its
Nerode index is exactly m, so the second is simply not minimal. On the
non-regular part, control and registers do not trade. Recorded below as
a failed construction, because it is evidence in the opposite direction.

**What is actually true: the register content is determined up to
GL(d, Z).** The two presentations of the balance rule that 0034 section
6 found canonically identical -- `|A| = |B|` and `|A^B| = 2|A|` under
disjointness -- have register vectors related by the integer matrix
[[1,0],[1,1]], determinant 1. Verified below, together with the failure
of a singular matrix, which collapses models that the language
separates. Argument for the general case: a DPA's register map is the
abelian part of its transition monoid, and a change of register basis is
an invertible integer matrix; so the canonical form carries a parameter
group exactly as the frame taxonomy carries order, polarity and
GL(n,2) (0024, 0030). **GL(d, Z) is the count sort's analogue of
GL(n,2).** Stated as an argued conjecture, not a theorem: only the
instance is machine-checked.

Run directly for the verification suite.
"""

from __future__ import annotations

import os
import sys
from itertools import product as cartesian_product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from level_crossing import (AlwaysFalse, AlwaysTrue, CountPredicate,
                            CountedAutomaton, LinearConstraint,
                            columns_over, disjointness,
                            exclusive_or_channel, popcount)


class ModularConstraint(CountPredicate):
    """counter = residue (mod modulus). Presburger arithmetic includes
    divisibility by a constant, so this is a legal count atom."""

    def __init__(self, name: str, modulus: int, residue: int) -> None:
        self.name = name
        self.modulus = modulus
        self.residue = residue

    def holds(self, counts: dict[str, int]) -> bool:
        return counts.get(self.name, 0) % self.modulus == self.residue

    def substituted(self, name: str, value: int) -> CountPredicate:
        if name != self.name:
            return self
        return (AlwaysTrue() if value % self.modulus == self.residue
                else AlwaysFalse())

    def description(self) -> str:
        return f"({self.name} = {self.residue} mod {self.modulus})"


# ---------------------------------------------------------------------
# 1. the rewrite-side diagnosis
# ---------------------------------------------------------------------

def verify_no_monotone_term_measure(bound: int = 12) -> None:
    """Every layer operator moves bit-length by a bounded amount; the
    level map squares the alphabet of lengths. A syntactic measure that
    decreases under the layer's rules cannot survive `{.}`."""
    print("  operator      bit-length of the result, for inputs of "
          "bit-length L")
    rows = [
        ("x ^ y", lambda a, b: (a ^ b).bit_length(), "<= L"),
        ("x & y", lambda a, b: (a & b).bit_length(), "<= L"),
        ("x << 1", lambda a, b: (a << 1).bit_length(), "L + 1"),
        ("x + y", lambda a, b: (a + b).bit_length(), "L + 1"),
        ("{x} = 2^x", lambda a, b: (1 << a).bit_length(), "2^L"),
    ]
    for label, operation, claim in rows:
        widths = []
        for length in range(1, bound):
            largest = (1 << length) - 1
            widths.append(operation(largest, largest >> 1))
        print(f"  {label:<12}  {widths[:6]} ...   {claim}")
    # the layer's operators are bounded by L + 1; the level map is not
    assert all((((1 << length) - 1) << 1).bit_length() <= length + 1
               for length in range(1, bound))
    assert all((1 << ((1 << length) - 1)).bit_length()
               > 2 ** length - 1 for length in range(1, 6))
    print("    the layer's rules move the measure by at most one; the "
          "level map moves it")
    print("    exponentially, so no measure that certifies the layer's "
          "termination")
    print("    certifies its own. This is the diagnosis; the proof is "
          "undecidability.")


# ---------------------------------------------------------------------
# 2. the failed Pareto construction
# ---------------------------------------------------------------------

def modular_popcount_in_control(channel: str, modulus: int
                                ) -> CountedAutomaton:
    """m control states, no register."""
    alphabet = columns_over((channel,))
    table = {}
    for residue in range(modulus):
        for column in alphabet:
            table[(residue, column)] = (residue + column[0]) % modulus
    return CountedAutomaton(
        (channel,), (), modulus, 0, table,
        [AlwaysTrue() if residue == 0 else AlwaysFalse()
         for residue in range(modulus)])


def modular_popcount_in_register(channel: str, modulus: int
                                 ) -> CountedAutomaton:
    """one control state, one register."""
    return CountedAutomaton(
        (channel,), (channel,), 1, 0,
        {(0, column): 0 for column in columns_over((channel,))},
        [ModularConstraint(channel, modulus, 0)])


def nerode_index(membership, max_prefix_length: int,
                 probe_depth: int) -> int:
    """Residual classes of a one-channel language. Every prefix is
    probed by the SAME suffix set, so signatures are comparable across
    prefix lengths."""
    suffixes = [suffix for length in range(probe_depth + 1)
                for suffix in cartesian_product((0, 1), repeat=length)]
    classes = set()
    for prefix_length in range(max_prefix_length + 1):
        for prefix in cartesian_product((0, 1), repeat=prefix_length):
            classes.add(tuple(membership(prefix + suffix)
                              for suffix in suffixes))
    return len(classes)


def verify_the_pareto_construction_fails(width: int = 8) -> None:
    """The intended obstruction, and why it is not one."""
    print("  m   control-only   register   same language   Nerode index "
          "of the language")
    for modulus in range(2, 6):
        control = modular_popcount_in_control("x", modulus)
        register = modular_popcount_in_register("x", modulus)
        agree = all(
            control.accepts({"x": value}, width)
            == register.accepts({"x": value}, width)
            == (popcount(value) % modulus == 0)
            for value in range(1 << width))
        assert agree
        index = nerode_index(
            lambda word, m=modulus: sum(word) % m == 0,
            2 * modulus, modulus + 1)
        assert index == modulus, (modulus, index)
        print(f"  {modulus}   {control.state_count} states, 0 reg"
              f"   1 state, 1 reg   yes             {index}")
    print("    The two presentations look like a Pareto pair -- neither "
          "dominates on")
    print("    (control, registers). But the language is REGULAR, its "
          "Nerode index is")
    print("    exactly m, and the canonical form is the m-state minimal "
          "automaton. The")
    print("    register presentation is not a rival minimum, it is "
          "simply not minimal.")
    print("    Every control/register trade that can be built works "
          "this way: the traded")
    print("    part is regular, and the minimal automaton absorbs it. "
          "On the non-regular")
    print("    part the two resources do not trade, so there is no "
          "Pareto frontier and")
    print("    the intended impossibility argument does not exist.")


# ---------------------------------------------------------------------
# 3. what survives: the register basis is free up to GL(d, Z)
# ---------------------------------------------------------------------

def _determinant_two_by_two(matrix) -> int:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def verify_register_basis_is_free_up_to_gl(bound: int = 1 << 7) -> None:
    """The two presentations of balance differ by a unimodular change of
    register basis, and a singular one destroys the language."""
    unimodular = ((1, 0), (1, 1))
    assert _determinant_two_by_two(unimodular) == 1

    disjoint = [(a, b) for a in range(bound) for b in range(bound)
                if a & b == 0]
    mismatches = [
        (a, b) for a, b in disjoint
        if (popcount(a), popcount(a ^ b))
        != (unimodular[0][0] * popcount(a) + unimodular[0][1] * popcount(b),
            unimodular[1][0] * popcount(a) + unimodular[1][1] * popcount(b))]
    assert not mismatches, mismatches[:5]
    print(f"  (|A|, |A^B|) = M (|A|, |B|) with M = {unimodular}, "
          f"det = {_determinant_two_by_two(unimodular)}")
    print(f"    verified on every disjoint pair below {bound}")

    # and the two presentations really are the same statement
    direct = disjointness("A", "B") & CountedAutomaton.count_constraint(
        ("A", "B"), LinearConstraint({"A": 1, "B": -1}, "=", 0))
    through_union = (disjointness("A", "B")
                     & exclusive_or_channel("U", "A", "B")
                     & CountedAutomaton.count_constraint(
                         ("U", "A"),
                         LinearConstraint({"U": 1, "A": -2}, "=", 0)))
    hidden = through_union.existentially_projected("U", 10)
    assert direct.canonical_form(4) == hidden.canonical_form(4)
    print("    and their canonical forms are identical (0034 section 6, "
          "rechecked here)")

    singular = ((1, 1), (1, 1))
    assert _determinant_two_by_two(singular) == 0
    balanced = next((a, b) for a, b in disjoint
                    if popcount(a) == popcount(b) and popcount(a) >= 1)
    unbalanced = next(
        (a, b) for a, b in disjoint
        if popcount(a) + popcount(b) == popcount(balanced[0])
        + popcount(balanced[1]) and popcount(a) != popcount(b))
    image = lambda pair: (popcount(pair[0]) + popcount(pair[1]),) * 2
    assert image(balanced) == image(unbalanced)
    print(f"  a singular M = {singular} sends the balanced pair "
          f"{balanced} and the")
    print(f"    unbalanced pair {unbalanced} to the same register vector "
          f"{image(balanced)},")
    print("    so no acceptance predicate on the image separates them: "
          "the freedom is")
    print("    exactly GL(d, Z), not arbitrary relabelling.")
    print()
    print("    Reading: a DPA's register map is the abelian part of its "
          "transition")
    print("    monoid, so changing which counts the registers hold is a "
          "change of basis")
    print("    in Z^d. The canonical form therefore carries a parameter "
          "group, exactly")
    print("    as the frame taxonomy carries order, polarity and "
          "GL(n,2) (0024, 0030).")
    print("    GL(d, Z) is the count sort's GL(n,2). Argued in general, "
          "checked here")
    print("    only on this instance.")


def run_verification_suite() -> None:
    print("=" * 70)
    print("1. Unguarded: the rewrite-side diagnosis")
    print("=" * 70)
    verify_no_monotone_term_measure()

    print()
    print("=" * 70)
    print("2. Guarded: the intended impossibility, and why it fails")
    print("=" * 70)
    verify_the_pareto_construction_fails()

    print()
    print("=" * 70)
    print("3. What survives: canonical up to GL(d, Z)")
    print("=" * 70)
    verify_register_basis_is_free_up_to_gl()

    print()
    print("=" * 70)
    print("all checks passed")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
