"""Stress-testing the suspicion: "no algorithm can do materially
better than the ring's canonicalisation."

Four machine-checked exhibits, feeding exploration/0022:

  1. A family where EVERY algorithm that produces the ring canonical
     form must pay 2^n - 1 (the bound is semantic -- ANF size is a
     property of the statement, not of any algorithm), while the
     automaton pipeline answers the same entailment questions at
     n = 48 in milliseconds without ever producing it.

  2. The symmetric family (windowed parity): automaton provably
     exponential (minimisation = Myhill-Nerode, so the measured state
     count IS the lower bound), ring form linear. This kills the
     repair "then let the automaton be the canonical procedure".

  3. The identity that shows canonicalisation OVERSHOOTS inference:
     the top ANF coefficient equals the parity of the number of
     satisfying assignments. So producing the ring form solves
     parity-SAT, a Parity-P-complete task, while the inference
     question is only coNP. Checked on random functions.

  4. A Clue-native instance of the split: "x is divisible by 3" is a
     3-state automaton at every width, while its ring form grows
     without bound (measured).

Run this file directly.
"""

from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_automata import DFA, Variable
from clue_solver import holds_at_least_one_statement
from representation_tradeoff import (windowed_parity_relation,
                                     algebraic_normal_form_size)


def show_semantic_bound_versus_automaton() -> None:
    print("=" * 70)
    print("1  THE RING FORM'S COST IS SEMANTIC; THE AUTOMATON SKIPS IT")
    print("=" * 70)
    print("""
  "At least one of n cards": the ANF has exactly 2^n - 1 terms
  (verified below), and ANF size is a property of the STATEMENT --
  so every algorithm that outputs the ring canonical form pays at
  least 2^n - 1, whatever its internals. Not a lower bound on
  expand-and-cancel; a lower bound on the task.
""")
    for variable_count in (4, 8, 12, 14):
        term_count = algebraic_normal_form_size(
            [1 if mask else 0 for mask in range(1 << variable_count)],
            variable_count)
        assert term_count == (1 << variable_count) - 1
        print(f"      n = {variable_count:2d}   ANF terms "
              f"{term_count:8d}   (= 2^n - 1, exact)")
    print("""
  The automaton pipeline answers entailment on the same statements
  without producing that object. At n = 48, where the ring form has
  2^48 - 1 = 281,474,976,710,655 terms:""")
    wide_mask = (1 << 48) - 1
    narrow_mask = (1 << 20) - 1
    start = time.time()
    knowledge: DFA = holds_at_least_one_statement('A', narrow_mask)
    hypothesis: DFA = holds_at_least_one_statement('A', wide_mask)
    assert knowledge.entails(hypothesis)
    assert not hypothesis.entails(knowledge)
    elapsed = time.time() - start
    print(f"""
      "holds one of the first 20" entails "holds one of the first 48":
      decided both directions in {elapsed * 1000:.0f} ms, automata of
      {knowledge.state_count} and {hypothesis.state_count} states.

  So a sound-and-complete method beat the semantic floor of the ring
  form by a factor of ~10^13 -- by never visiting it.""")


def show_symmetric_family() -> None:
    print()
    print("=" * 70)
    print("2  THE SYMMETRIC FAMILY KILLS THE BASIS-SWAP REPAIR")
    print("=" * 70)
    print("""
  Windowed parity, parity(X & (Y << w)) even: the ring form is w
  terms; the minimal automaton is 2^(w+1) states. Because the engine's
  minimisation is Myhill-Nerode, the measured count IS the proof of
  minimality -- no smaller automaton exists:
""")
    for window in (2, 4, 6):
        automaton = windowed_parity_relation(window)
        assert automaton.state_count == 1 << (window + 1)
        print(f"      w = {window}   ring terms {window:2d}   minimal "
              f"automaton states {automaton.state_count:4d}"
              f"   (= 2^(w+1))")
    print("""
  So neither form dominates: swapping the distinguished basis from
  ring to automaton reproduces the same failure in mirror image.""")


def show_canonicalisation_overshoots() -> None:
    print()
    print("=" * 70)
    print("3  CANONICALISATION OVERSHOOTS THE QUESTION")
    print("=" * 70)
    import random
    random_source = random.Random(20260808)
    variable_count = 8
    for _ in range(300):
        table = [random_source.randint(0, 1)
                 for _ in range(1 << variable_count)]
        satisfying_parity = sum(table) & 1
        coefficients = list(table)
        for bit_position in range(variable_count):
            step = 1 << bit_position
            for mask in range(1 << variable_count):
                if mask & step:
                    coefficients[mask] ^= coefficients[mask ^ step]
        top_coefficient = coefficients[(1 << variable_count) - 1]
        assert top_coefficient == satisfying_parity
    print("""
  Verified on 300 random functions of 8 variables: the TOP coefficient
  of the ring canonical form equals the parity of the number of
  satisfying assignments.

  Consequence: producing the ring form of a CNF computes parity-SAT,
  which is Parity-P-complete (Papadimitriou-Zachos) -- and by
  Valiant-Vazirani and Toda, Parity-P is hard for the entire
  polynomial hierarchy under randomised reductions. The inference
  question ("does K entail H") is coNP -- the FIRST level. So any
  route to inference that passes through the ring canonical form
  computes strictly more than the question asks, unless the hierarchy
  collapses. The canonicalisation is not the bottleneck of inference;
  it is an overshoot of it.""")


def show_clue_native_split() -> None:
    print()
    print("=" * 70)
    print("4  A CLUE-NATIVE INSTANCE: DIVISIBILITY BY 3")
    print("=" * 70)
    congruence: DFA = Variable('x').equals(
        Variable('w') + (Variable('w') << 1)).exists('w').minimized()
    print(f"""
  "x is divisible by 3" (0011's congruence, in the framework's own
  vocabulary): {congruence.state_count} automaton states at EVERY
  width. Its ring form, measured by width:
""")
    for width in (4, 6, 8, 10, 12, 14):
        table = [1 if value % 3 == 0 else 0
                 for value in range(1 << width)]
        term_count = algebraic_normal_form_size(table, width)
        degree = 0
        coefficients = list(table)
        for bit_position in range(width):
            step = 1 << bit_position
            for mask in range(1 << width):
                if mask & step:
                    coefficients[mask] ^= coefficients[mask ^ step]
        for mask, coefficient in enumerate(coefficients):
            if coefficient:
                degree = max(degree, bin(mask).count('1'))
        print(f"      width {width:2d}   ring terms {term_count:6d}"
              f"   degree {degree:2d}")
    print("""
  Unbounded growth against a constant 3 states. Congruences are not
  exotic: they are the framework's own counting vocabulary (0011).""")


def run_verification_suite() -> None:
    show_semantic_bound_versus_automaton()
    show_symmetric_family()
    show_canonicalisation_overshoots()
    show_clue_native_split()
    print()
    print("all stress-test checks passed")


if __name__ == "__main__":
    run_verification_suite()
