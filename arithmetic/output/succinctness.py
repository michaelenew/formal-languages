"""Hidden channels are Tseitin variables: what naming the carry buys.

Two questions, both settled here.

1. ARE HIDDEN CHANNELS ALREADY AVAILABLE in the corpus's original
   framing -- just name the implied variable and constrain it?

   Yes on the KNOWLEDGE side, and for a precise reason: for a
   hypothesis H that does not mention the hidden symbol C,

       for-all C ( K(C) implies H )   is equivalent to
       ( exists C : K(C) ) implies H

   so leaving C free in K is *identical* to existentially quantifying
   it. No explicit quantifier is needed.

   NO on the HYPOTHESIS side. There the implication runs the other
   way, and

       K implies exists C : H(C)      is NOT equivalent to
       for-all C ( K implies H(C) )

   so a free C in H makes the test sound but incomplete -- it demands
   that EVERY candidate witness work. Nonemptiness facts can be
   LEARNED for free; nonemptiness QUESTIONS need a real quantifier.
   Both halves are verified below.

2. IS THE SIZE COST EXPONENTIAL? For expressions with no hidden
   symbols, yes -- and this is measured below, in the corpus's own
   algebra, on the corpus's own two sticking points:

       "at least one of n cards"   2^n - 1  XOR-of-AND terms
                                   ... versus 3 constraints and ONE
                                   hidden channel
       carry into bit i            exponential in i
                                   ... versus one hidden channel per
                                   bit, each locally constrained

   With hidden symbols the blow-up disappears. This is exactly the
   classical Tseitin transformation: auxiliary variables convert an
   exponential normal form into a linear conjunction of local
   constraints. The flip-elimination construction of 0015 is the same
   phenomenon -- it is polynomial-size (one hidden track per state,
   O(states^2) atoms at fixed arity); what is exponential there is
   EVALUATING it (each projection determinizes), not writing it.

Run this file directly.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_automata import (
    DFA, Variable, relation_intersection, relation_exclusive_or,
    relation_shift_fill_zero, relation_constant, relation_equality)


# ---------------------------------------------------------------------
# 1. Free hidden symbols on the knowledge side, quantified on the
#    hypothesis side
# ---------------------------------------------------------------------

def nonemptiness_body(subject: str, prefix: str) -> DFA:
    """The BODY of the nonemptiness witness, with the hidden channel
    left free: prefix is an all-ones run below subject's lowest bit,
    and the position just above prefix lies in subject."""
    shifted, one, long_prefix, top = (
        "_shifted", "_one", "_longPrefix", "_top")
    zero, meet = "_zero", "_meet"
    body = relation_shift_fill_zero(prefix, shifted)
    body = body.intersected_with(relation_constant(one, 1))
    body = body.intersected_with(
        relation_exclusive_or(shifted, one, long_prefix))
    body = body.intersected_with(
        relation_intersection(prefix, long_prefix, meet))
    body = body.intersected_with(relation_equality(meet, prefix))
    body = body.intersected_with(
        relation_exclusive_or(long_prefix, prefix, top))
    body = body.intersected_with(
        relation_intersection(prefix, subject, zero))
    body = body.intersected_with(
        relation_constant("_zeroConst", 0))
    body = body.intersected_with(
        relation_equality(zero, "_zeroConst"))
    top_meet = "_topMeet"
    body = body.intersected_with(
        relation_intersection(top, subject, top_meet))
    body = body.intersected_with(relation_equality(top_meet, top))
    return body.exists(shifted, one, long_prefix, top, zero,
                       "_zeroConst", meet, top_meet).minimized()


def show_quantifier_asymmetry() -> None:
    print("=" * 68)
    print("1  HIDDEN SYMBOLS: FREE ON THE LEFT, QUANTIFIED ON THE RIGHT")
    print("=" * 68)
    subject = Variable('x')
    nonempty = (~subject.equals(0)).minimized()

    body_free = nonemptiness_body('x', 'q')          # q still free
    body_hidden = body_free.exists('q')              # q quantified

    # Knowledge side: leaving the witness free is the same as
    # quantifying it, for hypotheses that do not mention it.
    assert body_free.entails(nonempty)
    assert body_hidden.entails(nonempty)
    assert body_hidden.describes_same_relation_as(nonempty)
    print("""
  KNOWLEDGE SIDE.  Take K = the nonemptiness witness body, with the
  invented symbol q left free, and H = "x is nonempty".
      K with q free      entails H:  {}
      K with q hidden    entails H:  {}
  Identical, and this is not luck: for H not mentioning q,
  for-all q (K(q) -> H) and (exists q K(q)) -> H are the same
  statement. Inventing a symbol and constraining it IS existential
  quantification, with no quantifier in the language.""".format(
        body_free.entails(nonempty), body_hidden.entails(nonempty)))

    # Hypothesis side: the interchange fails.
    knowledge = nonempty
    entails_hidden = knowledge.entails(body_hidden)
    entails_free = knowledge.entails(body_free)
    assert entails_hidden and not entails_free
    print("""  HYPOTHESIS SIDE.  Now put the witness in the HYPOTHESIS:
  K = "x is nonempty", H = the same witness body.
      K entails H with q hidden:  {}
      K entails H with q free:    {}
  The free reading demands that EVERY q be a witness, not merely
  some q, so the test goes quiet on a truth it should confirm --
  sound but incomplete. Nonemptiness facts can be LEARNED for free;
  nonemptiness QUESTIONS need a real quantifier.""".format(
        entails_hidden, entails_free))


# ---------------------------------------------------------------------
# 2. The size measurement, in the corpus's own algebra
# ---------------------------------------------------------------------

def algebraic_normal_form_size(truth_table: list[int],
                               variable_count: int) -> int:
    """Number of XOR-joined AND-terms in the unique multilinear
    (Zhegalkin) form -- the corpus's canonical expression form."""
    coefficients = list(truth_table)
    for bit_position in range(variable_count):
        step = 1 << bit_position
        for mask in range(1 << variable_count):
            if mask & step:
                coefficients[mask] ^= coefficients[mask ^ step]
    return sum(coefficients)


def truth_table_at_least_one(variable_count: int) -> list[int]:
    return [1 if mask else 0 for mask in range(1 << variable_count)]


def truth_table_at_least_two(variable_count: int) -> list[int]:
    return [1 if bin(mask).count('1') >= 2 else 0
            for mask in range(1 << variable_count)]


def truth_table_carry(bit_count: int) -> list[int]:
    """Carry into position bit_count, as a function of
    x_0..x_{n-1}, y_0..y_{n-1}."""
    table: list[int] = []
    for mask in range(1 << (2 * bit_count)):
        left = mask & ((1 << bit_count) - 1)
        right = mask >> bit_count
        table.append(((left + right) >> bit_count) & 1)
    return table


def show_size_measurements() -> None:
    print()
    print("=" * 68)
    print("2  THE PRICE OF NOT NAMING THE HIDDEN SYMBOL")
    print("=" * 68)
    print("""
  Expression size in the corpus's canonical form (XOR of ANDs, the
  unique multilinear normal form), with NO hidden symbols allowed:
""")
    print("    'at least one of n cards'      (the refutation event)")
    for variable_count in range(1, 13):
        size = algebraic_normal_form_size(
            truth_table_at_least_one(variable_count), variable_count)
        assert size == (1 << variable_count) - 1
        if variable_count in (1, 2, 3, 6, 9, 12):
            print(f"        n = {variable_count:2d}   {size:6d} terms"
                  f"   (= 2^n - 1)")
    print("""        ... versus THREE constraints and ONE hidden
        channel, at every n (0015's nonemptiness witness).
""")
    print("    'at least two of n cards'      (a threshold clue)")
    for variable_count in (2, 3, 6, 9, 12):
        size = algebraic_normal_form_size(
            truth_table_at_least_two(variable_count), variable_count)
        print(f"        n = {variable_count:2d}   {size:6d} terms")
    print("""
    carry into bit i           (the corpus's own addition problem)""")
    previous = None
    for bit_count in range(1, 8):
        size = algebraic_normal_form_size(
            truth_table_carry(bit_count), 2 * bit_count)
        ratio = "" if previous is None else f"   x{size / previous:.2f}"
        print(f"        i = {bit_count}    {size:6d} terms{ratio}")
        previous = size
    print("""        ... versus ONE hidden channel per bit, each fixed
        by a local constraint: linear in i.

  The pattern is the classical Tseitin transformation. Auxiliary
  variables turn an exponential normal form into a linear conjunction
  of local constraints; without them the normal form is forced to
  name every interaction explicitly. The corpus's two hardest cases --
  refutations and addition -- are exactly the two cases where the
  saving is exponential.""")


def show_construction_size() -> None:
    print()
    print("=" * 68)
    print("3  SO THE 0015 CONSTRUCTION IS POLYNOMIAL, NOT EXPONENTIAL")
    print("=" * 68)
    print("""
  Counting the flip-elimination construction of 0015 for a target
  automaton with s states over k channels:

      hidden channels     s + 2          (one per state, plus two
                                          horizon tracks)
      partition atoms     O(s^2)
      transition atoms    O(s * 2^k * k)
      remaining atoms     O(s + k)

  so at fixed arity the definition has O(s^2) atoms and O(s) hidden
  channels: POLYNOMIAL in the size of the automaton.

  What is exponential is EVALUATING that definition -- each hidden
  channel is projected away by a subset construction, and turning a
  guessed run back into a deterministic automaton is exponential in
  general. That is a cost of canonicalisation, not of expression.
  The distinction matters: writing the knowledge down stays small;
  it is deciding with it that can be expensive.""")


def run_verification_suite() -> None:
    show_quantifier_asymmetry()
    show_size_measurements()
    show_construction_size()
    print()
    print("all succinctness checks passed")


if __name__ == "__main__":
    run_verification_suite()
