"""Mini-Clue solved end-to-end on the canonical-automata layer,
hand sizes included -- the K workflow.

Deck (6 cards, one bit each):
    mustard=1, plum=2  (suspects)   knife=4, pipe=8   (weapons)
    hall=16, study=32  (rooms)      FULL = 63

Players: Alice (hand A, 2 cards), Bob (hand B, 1 card),
envelope E (one card of each category; its size 3 is NOT asserted --
the workflow derives it).

Knowledge K is ONE canonical automaton over tracks (A, B, E):
the relation of all deals consistent with everything known.
  - update:      K := K  intersect  (new fact's automaton), reminimized
  - deduction:   K entails H  iff  K & ~H is empty  (one-sided)
Polarity per 0006: K shrinks as knowledge grows; TRUE = containment.

Hand sizes live INSIDE the term language -- no cardinality primitive:
  pow2(y)      :=  exists w:  add(w, 1) = y  and  y & w = 0
                   (y = w+1 disjoint from w  <=>  y is a power of two;
                    y = 0 is impossible since w+1 >= 1)
  |h| = k      :=  exists p1..pk, pairwise disjoint pow2's,
                   h = p1 ^ ... ^ pk
This is the counting story of 0001 §4 realized: sizes enter through
add and projection, never through a non-regular counting operator.

Every stage is cross-validated against a brute-force enumeration of all
64^3 = 262,144 deals. Run this file directly.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_automata import (
    DFA, product_dfa, minimize, project, stmt_eq, entails,
    is_empty, is_universal, accepts)

MUSTARD, PLUM, KNIFE, PIPE, HALL, STUDY = 1, 2, 4, 8, 16, 32
FULL = 63
NAMES = {MUSTARD: "mustard", PLUM: "plum", KNIFE: "knife",
         PIPE: "pipe", HALL: "hall", STUDY: "study"}

V = lambda n: ('var', n)
C = lambda c: ('const', c)


def conj(*stmts):
    out = stmts[0]
    for s in stmts[1:]:
        out = product_dfa(out, s)
    return minimize(out)


def pow2(term, tag):
    """pow2(term): exists w. add(w,1) = term and term & w = 0."""
    w = f"W{tag}"
    s = conj(stmt_eq(('add', V(w), C(1)), term),
             stmt_eq(('and', term, V(w)), C(0)))
    return minimize(project(s, {w}))


def size_is(hvar, k, tag):
    """|hvar| = k via k disjoint power-of-two witnesses."""
    ps = [f"P{tag}{i}" for i in range(k)]
    parts = [pow2(V(p), f"{tag}{i}") for i, p in enumerate(ps)]
    for i in range(k):
        for j in range(i + 1, k):
            parts.append(stmt_eq(('and', V(ps[i]), V(ps[j])), C(0)))
    xor_term = V(ps[0])
    for p in ps[1:]:
        xor_term = ('xor', xor_term, p and V(p))
    parts.append(stmt_eq(xor_term, V(hvar)))
    return minimize(project(conj(*parts), set(ps)))


def in_hand(hvar, card):
    return stmt_eq(('and', V(hvar), C(card)), C(card))


def not_in_hand(hvar, card):
    return stmt_eq(('and', V(hvar), C(card)), C(0))


def hand_is(hvar, cards):
    return stmt_eq(V(hvar), C(cards))


def models(K):
    """Brute-force: which of the 64^3 deals does K accept?"""
    out = []
    for a_ in range(64):
        for b_ in range(64):
            for e_ in range(64):
                if accepts(K, {'A': a_, 'B': b_, 'E': e_}):
                    out.append((a_, b_, e_))
    return out


def ground_truth(pred):
    out = []
    for a_ in range(64):
        for b_ in range(64):
            for e_ in range(64):
                if pred(a_, b_, e_):
                    out.append((a_, b_, e_))
    return out


def report(K, label, pred):
    m = models(K)
    gt = ground_truth(pred)
    assert m == gt, f"{label}: automaton disagrees with brute force"
    print(f"{label}: canonical {K.n} states, "
          f"{len(m)} consistent deals (brute-force match)")
    return m


def judge(K, H, text):
    """One-sided judgment, both directions of a question."""
    print(f"    {text}: {'KNOWN TRUE' if entails(K, H) else 'unknown'}")


def _run():
    # ---- K0: the a-priori knowledge ---------------------------------
    partition = conj(
        stmt_eq(('xor', V('A'), ('xor', V('B'), V('E'))), C(FULL)),
        stmt_eq(('and', V('A'), V('B')), C(0)),
        stmt_eq(('and', V('A'), V('E')), C(0)),
        stmt_eq(('and', V('B'), V('E')), C(0)))
    sizes = conj(size_is('A', 2, 'a'), size_is('B', 1, 'b'))
    envelope = conj(pow2(('and', V('E'), C(3)), 'es'),
                    pow2(('and', V('E'), C(12)), 'ew'),
                    pow2(('and', V('E'), C(48)), 'er'))
    K0 = conj(partition, sizes, envelope)

    def pc(x):
        return bin(x).count('1')

    def pred0(a_, b_, e_):
        return (a_ ^ b_ ^ e_ == FULL and a_ & b_ == 0 and a_ & e_ == 0
                and b_ & e_ == 0 and pc(a_) == 2 and pc(b_) == 1
                and pc(e_ & 3) == 1 and pc(e_ & 12) == 1
                and pc(e_ & 48) == 1)

    report(K0, "K0 (partition + |A|=2 + |B|=1 + envelope categories)",
           pred0)

    # Derived, never asserted: the envelope holds exactly 3 cards
    judge(K0, size_is('E', 3, 'e3'), "|E| = 3 (derived from partition)")
    # And a non-fact stays unknown:
    judge(K0, in_hand('E', PLUM), "plum in envelope")

    # ---- Event 1: Alice passes on (plum, knife, hall) ---------------
    K1 = conj(K0, not_in_hand('A', PLUM | KNIFE | HALL))
    report(K1, "K1 = K0 + Alice holds none of {plum, knife, hall}",
           lambda a_, b_, e_: pred0(a_, b_, e_) and a_ & 22 == 0)

    # ---- Event 2: Bob passes on the same suggestion -----------------
    K2 = conj(K1, not_in_hand('B', PLUM | KNIFE | HALL))
    report(K2, "K2 = K1 + Bob holds none of {plum, knife, hall}",
           lambda a_, b_, e_: pred0(a_, b_, e_) and a_ & 22 == 0
           and b_ & 22 == 0)

    print("  deductions at K2:")
    judge(K2, in_hand('E', PLUM), "plum in envelope")
    judge(K2, in_hand('E', KNIFE), "knife in envelope")
    judge(K2, in_hand('E', HALL), "hall in envelope")
    judge(K2, hand_is('E', PLUM | KNIFE | HALL),
          "envelope = {plum, knife, hall} exactly")
    print("  one-sidedness at K2 (mustard is in A or B, but neither "
          "is knowable):")
    judge(K2, in_hand('A', MUSTARD), "mustard in Alice's hand")
    judge(K2, not_in_hand('A', MUSTARD), "mustard NOT in Alice's hand")
    judge(K2, in_hand('B', MUSTARD), "mustard in Bob's hand")
    judge(K2, not_in_hand('E', MUSTARD), "mustard NOT in envelope")

    # ---- Event 3: Bob shows the pipe --------------------------------
    K3 = conj(K2, in_hand('B', PIPE))
    m3 = report(K3, "K3 = K2 + Bob shows pipe",
                lambda a_, b_, e_: pred0(a_, b_, e_) and a_ & 22 == 0
                and b_ & 22 == 0 and b_ & PIPE)

    print("  deductions at K3 (everything is forced):")
    judge(K3, hand_is('A', MUSTARD | STUDY), "Alice = {mustard, study}")
    judge(K3, hand_is('B', PIPE), "Bob = {pipe}")
    judge(K3, hand_is('E', PLUM | KNIFE | HALL),
          "envelope = {plum, knife, hall}")
    assert len(m3) == 1
    a_, b_, e_ = m3[0]
    fmt = lambda h: "{" + ", ".join(NAMES[c] for c in NAMES if h & c) + "}"
    print(f"  unique consistent deal: A={fmt(a_)} B={fmt(b_)} "
          f"E={fmt(e_)}")
    print("  accusation: Professor Plum, in the hall, with the knife")

    # The test never lies in the other direction either:
    assert not entails(K2, hand_is('B', PIPE))
    print("all stages cross-validated against 262,144-deal brute force")


if __name__ == "__main__":
    _run()
