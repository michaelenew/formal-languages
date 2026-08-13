"""The deficit's fate: is there a finite hbar in this frame?

0056 defined the deficit delta(A, B) = 1 - reachable-pairs / product
for two observables run jointly, and measured ~0.3 for the persistent
multiplier + counter.  The question green-lit here: does delta tend to
1 (asymptotic complementarity), to a constant (a commutator norm for
the frame), or does it decompose into something classical?

It decomposes.  Completely.

  s1  COUNTER vs COUNTER: reachable pairs = lcm(m1, m2), exactly, so
      delta = 1 - 1/gcd(m1, m2).  Coprime counters are fully
      independent (delta = 0); the deficit for counters IS the Chinese
      Remainder Theorem.  Arithmetic overlap, nothing else.

  s2  MULTIPLIER vs COUNTER: the joint cost is EXACTLY linear in m,
      joint(p, m) = A_p * m + B_p, where A_p is the number of RECURRENT
      states of the order machine (verified state-by-state: recurrent
      states pair with every residue, transient ones with a fixed
      finite set).  So delta converges to the TRANSIENT FRACTION of
      the order machine -- temporal overlap, nothing else.

  s3  Conclusion, stated against the conjecture: at finite resolution
      the frame has NO irreducible incompatibility.  Every measured
      deficit is accounted for, exactly, by arithmetic overlap (CRT)
      plus transient-phase correlation.  The finite hbar is zero; the
      incompatibility is entirely concentrated at the unbounded limit
      (the Minsky wall).  The Heisenberg analogy is therefore of the
      Kochen-Specker kind (all-or-nothing, no joint refinement), not
      the Robertson kind (graded trade at every scale) -- the
      literature diagnosis of 0055's discussion, now by measurement.

Run directly for the verification suite.
"""

from __future__ import annotations

import sys
from math import gcd

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from order_count_complementarity import (count_machine,
                                         persistent_order_bit,
                                         reachable_pairs,
                                         signature_machine)


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


# ---------------------------------------------------------------------
# 1. counter vs counter: the deficit is the CRT
# ---------------------------------------------------------------------

def verify_counter_deficit_is_crt(limit=8) -> None:
    print(f"    {'m1':>3} {'m2':>3} {'pairs':>6} {'lcm':>5} "
          f"{'delta':>7} {'1-1/gcd':>8}")
    for m1 in range(2, limit + 1):
        for m2 in range(m1, limit + 1):
            pairs = reachable_pairs(count_machine(m1), count_machine(m2))
            assert pairs == lcm(m1, m2), (m1, m2, pairs)
            delta = 1 - pairs / (m1 * m2)
            reference = 1 - 1 / gcd(m1, m2)
            assert abs(delta - reference) < 1e-12
            if m2 <= 5 or m1 == m2 or gcd(m1, m2) == 1:
                print(f"    {m1:>3} {m2:>3} {pairs:>6} "
                      f"{lcm(m1, m2):>5} {delta:>7.3f} {reference:>8.3f}")
    print()
    print("  reachable pairs = lcm(m1, m2), every cell, so")
    print()
    print("      delta(C_m1, C_m2)  =  1 - 1/gcd(m1, m2)")
    print()
    print("  Coprime counters are FULLY independent (delta = 0); equal")
    print("  ones overlap maximally (delta = 1 - 1/m). The deficit")
    print("  between compatible observables is the Chinese Remainder")
    print("  Theorem -- arithmetic overlap, not incompatibility.")


# ---------------------------------------------------------------------
# 2. multiplier vs counter: the deficit is the transient fraction
# ---------------------------------------------------------------------

def recurrent_states(machine, probe=40):
    """States reachable at arbitrarily late times: reach-time sets via
    BFS by depth; a state is recurrent iff it appears at every time
    beyond some point within the probe window (checked on the tail)."""
    count, transitions, initial = machine
    reach = {t: set() for t in range(probe + 1)}
    reach[0] = {initial}
    for t in range(probe):
        for state in reach[t]:
            for bx in (0, 1):
                for by in (0, 1):
                    reach[t + 1].add(transitions[(state, bx, by)])
    tail = range(probe - 8, probe + 1)
    recurrent = {s for s in range(count)
                 if all(s in reach[t] for t in tail)}
    transient = set(range(count)) - recurrent
    return recurrent, transient


def joint_pairs_by_state(order_machine, modulus):
    """Reachable (order state, count residue) pairs, grouped by state."""
    _, trans_o, init_o = order_machine
    _, trans_c, init_c = count_machine(modulus)
    seen = {(init_o, init_c)}
    frontier = [(init_o, init_c)]
    while frontier:
        so, sc = frontier.pop()
        for bx in (0, 1):
            for by in (0, 1):
                pair = (trans_o[(so, bx, by)], trans_c[(sc, bx, by)])
                if pair not in seen:
                    seen.add(pair)
                    frontier.append(pair)
    by_state = {}
    for so, sc in seen:
        by_state.setdefault(so, set()).add(sc)
    return by_state


def verify_multiplier_deficit_is_transience(max_precision=3,
                                            moduli=(2, 3, 4, 5, 6,
                                                    7)) -> None:
    for p in range(1, max_precision + 1):
        machine = signature_machine(persistent_order_bit(p),
                                    max(p + 3, 6))
        total = machine[0]
        recurrent, transient = recurrent_states(machine)
        joints = {}
        for m in moduli:
            by_state = joint_pairs_by_state(machine, m)
            joints[m] = sum(len(v) for v in by_state.values())
            for state in recurrent:
                assert len(by_state.get(state, set())) == m, (p, m, state)
            if m == max(moduli):
                fixed = sum(len(by_state.get(s, set()))
                            for s in transient)
        slope_checks = [joints[m2] - joints[m1] ==
                        len(recurrent) * (m2 - m1)
                        for m1, m2 in zip(moduli, moduli[1:])]
        assert all(slope_checks), (p, joints)
        intercept = joints[moduli[0]] - len(recurrent) * moduli[0]
        assert intercept == fixed, (p, intercept, fixed)
        limit_delta = 1 - len(recurrent) / total
        print(f"    p={p}:  {total} states = {len(recurrent)} recurrent"
              f" + {len(transient)} transient")
        print(f"           joint(m) = {len(recurrent)}·m + {intercept}"
              f"   (exact for m = {moduli[0]}..{moduli[-1]})")
        print(f"           delta(m→∞) = 1 - {len(recurrent)}/{total}"
              f" = {limit_delta:.3f}   (the transient fraction)")
    print()
    print("  Verified state-by-state: every RECURRENT state of the")
    print("  multiplier pairs with every count residue; every TRANSIENT")
    print("  (learning-phase) state pairs with a fixed finite set. The")
    print("  joint cost is exactly linear in m, the slope is the")
    print("  recurrent state count, and the limiting deficit is the")
    print("  transient fraction -- temporal overlap, not incompatibility.")


# ---------------------------------------------------------------------
# 3. the conclusion
# ---------------------------------------------------------------------

def state_the_conclusion() -> None:
    print("  Every deficit measured in this frame decomposes, exactly:")
    print()
    print("    counter  vs counter     delta = 1 - 1/gcd     (CRT)")
    print("    multiplier vs counter   delta -> transient fraction")
    print()
    print("  Neither is incompatibility. Coprime counters and")
    print("  post-transient observables are FULLY independent -- every")
    print("  joint state is realizable, the budget is a plain sum of")
    print("  logs with no cross term. The finite-level hbar of this")
    print("  frame is ZERO.")
    print()
    print("  The incompatibility that motivated the conjecture is real")
    print("  but lives entirely at the unbounded limit: both observables")
    print("  exact, with read-back, is the Minsky wall -- undecidable at")
    print("  infinity, unconstrained at every finite scale. So the")
    print("  Heisenberg analogy resolves to the KOCHEN-SPECKER kind")
    print("  (no joint refinement exists, all-or-nothing) rather than")
    print("  the ROBERTSON kind (a graded trade at every scale). The")
    print("  frame's uncertainty is contextuality-shaped, not")
    print("  variance-shaped -- which is also where the published bridge")
    print("  to logic (liar cycles, 0056 Part A) actually connects.")


def run_verification_suite() -> None:
    sections = [
        ("Counter vs counter: the deficit is the CRT",
         verify_counter_deficit_is_crt),
        ("Multiplier vs counter: the deficit is the transient fraction",
         verify_multiplier_deficit_is_transience),
        ("The conclusion: no finite hbar", state_the_conclusion),
    ]
    for index, (title, check) in enumerate(sections, start=1):
        print("=" * 70)
        print(f"{index}. {title}")
        print("=" * 70)
        check()
        print()
    print("=" * 70)
    print("suite complete")
    print("=" * 70)


if __name__ == "__main__":
    run_verification_suite()
