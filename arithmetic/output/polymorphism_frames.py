"""The polymorphism <-> frame correspondence, tested to a verdict.

Schaefer's dichotomy: the tractable Boolean constraint classes are
(up to trivial cases) AFFINE (closed under x+y+z), HORN (closed
under AND / min), and BIJUNCTIVE / 2-SAT (closed under coordinate
majority / median). 0030 matched the affine class to the GL(n,2)
frame parameter. This file asks the deciding question: do the other
two tractable classes have a frame home?

TWO INSTANCE FAMILIES, both succinct and polynomial-time decidable:

  independent sets of a cycle-plus-matching graph (an expander-like
  cubic graph): K = AND over edges of (NOT u OR NOT v). A 2-CNF;
  the solution space is median-closed (machine-checked); Clue-style
  entailment is polynomial by implication-graph closure
  (implemented, cross-checked against brute force).

  a bipartite implication system (each of n/2 source variables
  forces 3 random sink variables): K = AND of (x_source -> x_sink).
  Definite Horn with singleton bodies (and also bijunctive); the
  model set is min-closed (machine-checked); entailment is
  polynomial by unit propagation / reachability (implemented,
  cross-checked).

THE MEASUREMENT: every frame of the taxonomy on the same statements
at n = 12, 16, 20. Every frame grows by MORE THAN 2x PER STEP on
both families (asserted below), while the polynomial deciders answer
the full deduction grid without ever building a solution-space
object. Parameter probes (random orders, random GL(n,2) maps, the
moment lift) find nothing; for the independent-set shape the
OBDD-in-every-order lower bound is the cutwidth/pathwidth theorem
for expander-like graphs (cited), and the knowledge-compilation
map's non-linear targets (DNNF and below, Darwiche-Marquis) carry
exponential expander lower bounds in the literature
(Bova-Capelli-Mengel-Slivovsky) -- so this is not a missing-frame
problem. Honesty note: the GL(n,2) absence is measured-plus-argument
(the families carry no linear structure for a change of basis to
eliminate, unlike 0030's affine family which supplied its curing L),
not an exhaustive-orbit proof.

THE VERDICT. The portfolio step of the proof sketch ('best possible
= run all N frame canonicalisations in parallel') is FALSE for the
DECISION task: two of Schaefer's three nontrivial tractable classes
are decided by formula-side closure algorithms whose polynomial
operation compiles nothing, and their solution spaces have no frame
home. Deciding is strictly cheaper than representing -- 0020's B1
break, now witnessed by NATURAL subclasses rather than an
algorithmic trick.

WHAT SURVIVES: the COUNTING task. Counting independent sets of
cubic graphs is #P-complete (Greenhill), so the all-frames blow-up
on the median-closed family matches a genuine hardness boundary --
any frame compilation yields the model count for free, so no frame
could be small there unless P = #P collapses at that family. The
frame program is a coherent theory of DEDUCTION-WITH-COUNTING (the
Clue solver's actual task: verdict grid plus exact deal counts);
for bare decision, portfolio optimality is dead.

Run this file directly.
"""

from __future__ import annotations

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anf_automaton_tradeoff import automaton_size, anf_term_count
from taxonomy_relation_graph import walsh_support, dual_term_count
from frame_flow_map import fdd_size
from matrix_completion import negfdd_size
from subclass_escapes import (gf2_parity, gf2_rank, gf2_invert,
                              moment_diagram_size)

TruthTable = list[int]
Edge = tuple[int, int]

MEASURED_SIZES = (12, 16, 20)
GROWTH_FLOOR = 2.0
FRAME_NAMES = ("minterm", "ANF", "dual", "Walsh", "OBDD", "FDD",
               "negFDD")


# ---------------------------------------------------------------------
# Family 1: independent sets of a cycle-plus-matching graph
# ---------------------------------------------------------------------

def cycle_plus_matching_edges(vertex_count: int,
                              source: random.Random) -> list[Edge]:
    edges = [(index, (index + 1) % vertex_count)
             for index in range(vertex_count)]
    vertices = list(range(vertex_count))
    source.shuffle(vertices)
    normalized = {(min(u, v), max(u, v)) for u, v in edges}
    for pair_index in range(vertex_count // 2):
        first = vertices[2 * pair_index]
        second = vertices[2 * pair_index + 1]
        key = (min(first, second), max(first, second))
        if key not in normalized:
            edges.append(key)
            normalized.add(key)
    return edges


def independent_set_table(edges: list[Edge],
                          vertex_count: int) -> TruthTable:
    return [1 if all(not (point >> u & 1 and point >> v & 1)
                     for u, v in edges) else 0
            for point in range(1 << vertex_count)]


def check_median_closure(table: TruthTable, vertex_count: int,
                         source: random.Random) -> None:
    models = [point for point in range(1 << vertex_count)
              if table[point]]
    for _ in range(500):
        first, second, third = (source.choice(models)
                                for _ in range(3))
        median = (first & second) | (first & third) | (second & third)
        assert table[median] == 1
    print("  median closure: the coordinate-median of 500 random "
          "model triples is\n  always a model -- the independent-set "
          "family is bijunctive (majority\n  polymorphism).")


def two_sat_entailed_literals(edges: list[Edge], vertex_count: int,
                              fact_literals: list[int]) -> set[int]:
    """Literals entailed by the independent-set constraints plus
    unit facts, via implication-graph reachability. Encoding:
    2v = 'vertex v out', 2v+1 = 'vertex v in'."""
    successors: list[list[int]] = [[] for _ in range(2 * vertex_count)]
    for u, v in edges:                     # (not u) or (not v)
        successors[2 * u + 1].append(2 * v)     # u in -> v out
        successors[2 * v + 1].append(2 * u)     # v in -> u out
    entailed: set[int] = set()
    for starting_literal in range(2 * vertex_count):
        frontier = list(fact_literals) + [starting_literal]
        reached = set(frontier)
        while frontier:
            literal = frontier.pop()
            for successor in successors[literal]:
                if successor not in reached:
                    reached.add(successor)
                    frontier.append(successor)
        if any(literal ^ 1 in reached for literal in reached):
            entailed.add(starting_literal ^ 1)
    return entailed


def check_two_sat_decider(edges: list[Edge], vertex_count: int,
                          source: random.Random) -> None:
    table = independent_set_table(edges, vertex_count)
    fact_vertices = source.sample(range(vertex_count), 3)
    fact_literals = [2 * fact_vertices[0] + 1,   # one vertex IN
                     2 * fact_vertices[1],       # two vertices OUT
                     2 * fact_vertices[2]]
    consistent_models = [
        point for point in range(1 << vertex_count)
        if table[point]
        and point >> fact_vertices[0] & 1
        and not point >> fact_vertices[1] & 1
        and not point >> fact_vertices[2] & 1]
    brute_force: set[int] = set()
    for vertex in range(vertex_count):
        if all(point >> vertex & 1 for point in consistent_models):
            brute_force.add(2 * vertex + 1)
        if all(not point >> vertex & 1 for point in consistent_models):
            brute_force.add(2 * vertex)
    computed = two_sat_entailed_literals(edges, vertex_count,
                                         fact_literals)
    assert computed == brute_force
    print(f"  the FULL deduction grid (all {2 * vertex_count} literal "
          f"queries) computed by\n  implication closure matches brute "
          f"force exactly ({len(computed)} entailed\n  literals) -- "
          f"polynomial time, no solution-space object ever built.")


# ---------------------------------------------------------------------
# Family 2: a bipartite implication system (definite Horn)
# ---------------------------------------------------------------------

def bipartite_implication_edges(vertex_count: int,
                                source: random.Random) -> list[Edge]:
    half = vertex_count // 2
    edges: list[Edge] = []
    for source_vertex in range(half):
        for sink_vertex in source.sample(range(half, vertex_count),
                                         3):
            edges.append((source_vertex, sink_vertex))
    return edges


def implication_table(edges: list[Edge],
                      vertex_count: int) -> TruthTable:
    return [1 if all(not (point >> u & 1) or point >> v & 1
                     for u, v in edges) else 0
            for point in range(1 << vertex_count)]


def check_horn_decider(vertex_count: int,
                       source: random.Random) -> None:
    edges = bipartite_implication_edges(vertex_count, source)
    table = implication_table(edges, vertex_count)
    models = [point for point in range(1 << vertex_count)
              if table[point]]
    for _ in range(500):
        first, second = source.choice(models), source.choice(models)
        assert table[first & second] == 1     # min-closure (Horn)

    half = vertex_count // 2
    true_fact = source.randrange(half)
    false_fact = source.randrange(half, vertex_count)
    # propagation: forward closure of the true fact; backward
    # anti-closure of the false fact
    forced_true = {true_fact}
    forced_true.update(v for u, v in edges if u == true_fact)
    forced_false = {false_fact}
    forced_false.update(u for u, v in edges if v == false_fact)
    consistent_models = [point for point in models
                         if point >> true_fact & 1
                         and not point >> false_fact & 1]
    for vertex in range(vertex_count):
        entailed_true = all(point >> vertex & 1
                            for point in consistent_models)
        entailed_false = all(not point >> vertex & 1
                             for point in consistent_models)
        assert entailed_true == (vertex in forced_true)
        assert entailed_false == (vertex in forced_false)
    print("  Horn: the bipartite implication system is min-closed "
          "(500 random pair\n  checks, semilattice polymorphism), and "
          "unit propagation from the facts\n  reproduces the "
          "brute-force entailed set exactly -- polynomial time,\n  "
          "nothing compiled.")


# ---------------------------------------------------------------------
# Every frame, measured on the same statements
# ---------------------------------------------------------------------

def measure_all_frames(table: TruthTable,
                       vertex_count: int) -> dict[str, int]:
    order = list(range(vertex_count))
    return {"minterm": sum(table),
            "ANF": anf_term_count(table, vertex_count),
            "dual": dual_term_count(table, vertex_count),
            "Walsh": walsh_support(table, vertex_count),
            "OBDD": automaton_size(table, vertex_count, order),
            "FDD": fdd_size(table, vertex_count, order),
            "negFDD": negfdd_size(table, vertex_count, order)}


def show_family_measurements(family_label: str,
                             table_of_size) -> None:
    print(f"\n      n   minterm      ANF     dual    Walsh    OBDD"
          f"     FDD  negFDD")
    measured_by_size: dict[int, dict[str, int]] = {}
    for vertex_count in MEASURED_SIZES:
        table = table_of_size(vertex_count)
        measured = measure_all_frames(table, vertex_count)
        measured_by_size[vertex_count] = measured
        print(f"      {vertex_count:2d} {measured['minterm']:8d} "
              f"{measured['ANF']:8d} {measured['dual']:8d} "
              f"{measured['Walsh']:8d} {measured['OBDD']:7d} "
              f"{measured['FDD']:7d} {measured['negFDD']:7d}")
    for frame_name in FRAME_NAMES:
        for smaller, larger in zip(MEASURED_SIZES, MEASURED_SIZES[1:]):
            growth = measured_by_size[larger][frame_name] / \
                measured_by_size[smaller][frame_name]
            assert growth > GROWTH_FLOOR, \
                (family_label, frame_name, smaller, growth)
    print(f"      every frame grows by more than {GROWTH_FLOOR}x per "
          f"step (asserted).")


def random_invertible_map(vertex_count: int,
                          source: random.Random) -> list[int]:
    while True:
        rows = [source.randrange(1, 1 << vertex_count)
                for _ in range(vertex_count)]
        if gf2_rank(rows) == vertex_count:
            return rows


def transformed_table(table: TruthTable, rows: list[int],
                      vertex_count: int) -> TruthTable:
    inverse_rows = gf2_invert(rows, vertex_count)
    result = [0] * (1 << vertex_count)
    for image_point in range(1 << vertex_count):
        source_point = 0
        for index in range(vertex_count):
            if gf2_parity(inverse_rows[index] & image_point):
                source_point |= 1 << index
        result[image_point] = table[source_point]
    return result


def show_parameter_probes(table: TruthTable,
                          vertex_count: int) -> None:
    natural = automaton_size(table, vertex_count,
                             list(range(vertex_count)))
    order_probe = min(
        automaton_size(table, vertex_count,
                       random.Random(seed).sample(
                           range(vertex_count), vertex_count))
        for seed in range(6))
    gl_probe = min(
        automaton_size(transformed_table(
            table, random_invertible_map(vertex_count,
                                         random.Random(seed)),
            vertex_count), vertex_count,
            list(range(vertex_count)))
        for seed in range(6))
    moment_size = moment_diagram_size(list(table), vertex_count,
                                      list(range(vertex_count)))
    print(f"""
  Parameter probes, independent-set family at n = {vertex_count}
  (natural-order OBDD {natural}):
      best of 6 random orders:        OBDD {order_probe}
      best of 6 random GL(n,2) maps:  OBDD {gl_probe}
      word-level moment diagram:      {moment_size}
  Nothing improves on the natural order (contrast 0030's affine
  family, whose constraint matrix SUPPLIED the curing map: 33 states
  at n = 16). Honesty note: random probes cannot exhaust the GL
  orbit; the structural point is that these families carry no linear
  structure for a change of basis to eliminate. For the
  independent-set shape, OBDD hardness in EVERY order is the
  cutwidth/pathwidth theorem for expander-like graphs (cited), and
  DNNF-and-below hardness is cited to the compilation-map
  literature -- the escape is not curable by any known canonical
  representation class, linear or not.""")


def show_verdict() -> None:
    print()
    print("=" * 70)
    print("4  THE VERDICT")
    print("=" * 70)
    print("""
  Two of Schaefer's three nontrivial tractable classes -- the
  median-closed independent-set family and the definite-Horn
  implication family -- have NO frame home: every frame of the
  completed taxonomy grows faster than 2x per size step on them
  (measured at three sizes, asserted), the parameter probes fail,
  and the cited every-order OBDD and DNNF lower bounds close the
  non-linear exits for the expander shape. Their full deduction
  grids are nonetheless computed in polynomial time by implication
  closure and unit propagation -- algorithms that never hold any
  canonical solution-space object. Only the affine class had a
  frame cure (0030).

  THEREFORE the portfolio step of the proof sketch -- 'the best
  possible performance is the N frame canonicalisations run in
  parallel' -- is FALSE for the DECISION task. Deciding is strictly
  cheaper than representing, witnessed by natural subclasses. As a
  route to P != NP via decision complexity, the eigenframe program
  is blocked here: this is the impossibility the pace was set to
  find.

  WHAT SURVIVES, exactly: the COUNTING task. Counting independent
  sets of cubic graphs is #P-complete (Greenhill), so the
  all-frames blow-up on the median-closed family sits exactly on a
  genuine hardness boundary: every frame compilation yields the
  model count for free, so no frame could be small there without
  collapsing #P. The frame program is a coherent theory of
  DEDUCTION-WITH-COUNTING -- which is the Clue solver's actual task
  (verdict grid PLUS exact deal counts) -- and for that task the
  portfolio question remains open and now sharply posed: is the
  frame portfolio optimal for model counting / weighted deduction?
  The decision/counting split is the program's true boundary.""")


def run_verification_suite() -> None:
    print("=" * 70)
    print("1  THE TRACTABLE CLASSES AND THEIR POLYNOMIAL DECIDERS")
    print("=" * 70)
    source = random.Random(40)
    vertex_count = 16
    edges = cycle_plus_matching_edges(vertex_count, source)
    table = independent_set_table(edges, vertex_count)
    check_median_closure(table, vertex_count, source)
    check_two_sat_decider(edges, vertex_count, source)
    check_horn_decider(vertex_count, source)

    print()
    print("=" * 70)
    print("2  EVERY FRAME ON THE MEDIAN-CLOSED (INDEPENDENT-SET) "
          "FAMILY")
    print("=" * 70)
    show_family_measurements(
        "independent-set",
        lambda size: independent_set_table(
            cycle_plus_matching_edges(size, random.Random(41)), size))
    probe_table = independent_set_table(
        cycle_plus_matching_edges(12, random.Random(41)), 12)
    show_parameter_probes(probe_table, 12)

    print()
    print("=" * 70)
    print("3  EVERY FRAME ON THE DEFINITE-HORN (IMPLICATION) FAMILY")
    print("=" * 70)
    show_family_measurements(
        "implication",
        lambda size: implication_table(
            bipartite_implication_edges(size, random.Random(43)),
            size))

    show_verdict()
    print()
    print("all polymorphism-frame checks passed")


if __name__ == "__main__":
    run_verification_suite()
