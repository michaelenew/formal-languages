# 0031 — The decision/counting split: where the eigenframe program stops, and what survives

Directive: proceed at pace until something proves impossible or
intractable. Something did. This note records the impossibility, its
witnesses, and the exact boundary it draws. Machine checks:
`output/polymorphism_frames.py`; the subclass map figure is updated
with the two falsifier rows.

## 1. The experiment the audit selected

0030's audit pointed at the polymorphism ↔ frame correspondence:
Schaefer's three nontrivial tractable classes are affine, Horn
(min-closed), and bijunctive (median-closed). The affine class had a
frame cure (GL(n,2), 0030). The deciding question: do the other two?

Two succinct families, both machine-checked to lie in their classes
and both given working polynomial deciders, cross-checked against
brute force on the full deduction grid:

- **Independent sets of a cycle-plus-matching graph** (2-CNF;
  median-closed by 500-triple check; full literal grid by
  implication-graph closure).
- **A bipartite implication system** (definite Horn with singleton
  bodies; min-closed by 500-pair check; full grid by unit
  propagation).

## 2. The measurement

Every frame of the taxonomy, three sizes, same statements:

    independent sets      n   minterm    ANF    dual   Walsh   OBDD    FDD  negFDD
                         12       220    920     105    3526     66    145      98
                         16      1156  10936     439   60103    176    589     265
                         20      5620 133508    2217 1000171    384   3162     869

    implications         12       226    397     305    3286     91    251     107
                         16      1230   3357    2773   58017    302   1146     381
                         20      8410  23193   10001  524288    701   4916     886

**Every frame grows by more than 2× per step on both families**
(asserted). Parameter probes fail: best of 6 random orders 101, best
of 6 random GL(n,2) maps 304, moment diagram 152 — against 66 in the
natural order at n = 12. Honesty note: random probes cannot exhaust
the GL orbit; the structural point is that these families carry no
linear structure to eliminate (0030's affine family *supplied* its
curing map; nothing here does). For the independent-set shape,
OBDD hardness in every order is the cutwidth/pathwidth theorem for
expander-like graphs (cited), and the knowledge-compilation map's
non-linear targets — DNNF and everything below it (Darwiche–Marquis)
— carry exponential expander lower bounds in the literature
(Bova–Capelli–Mengel–Slivovsky). This is not a missing-frame
problem: linear and non-linear canonical representation classes
fail together.

## 3. The impossibility

> **Portfolio optimality is false for the decision task.** Two of
> Schaefer's three nontrivial tractable classes are decided in
> polynomial time by formula-side closure algorithms (implication
> closure, unit propagation) that never hold any canonical
> solution-space object — while their solution spaces have no home
> in any frame of the completed taxonomy. Deciding is strictly
> cheaper than representing.

This is 0020's B1 break (PPSZ decides without canonicalising)
upgraded from an algorithmic curiosity to a structural fact: it is
witnessed by *natural subclasses* — two-thirds of the tractable
Boolean CSP world — not by a clever SAT solver. The proof sketch's
step "best possible = run all N frame canonicalisations in parallel"
cannot be repaired by adding frames: the pool theorem (0030) closes
the linear kinds, and the cited compilation-map lower bounds close
the non-linear ones. As a route to P ≠ NP through decision
complexity, the eigenframe program is blocked here. This is the
impossibility the pace was set to find.

## 4. What survives — and it is not nothing

The boundary is exactly the **counting line**:

- Counting independent sets of cubic graphs is **#P-complete**
  (Greenhill). Any frame compilation yields the model count for
  free (that is what canonical objects do). So no frame *could* be
  small on the median-closed family without collapsing #P — the
  all-frames blow-up sits precisely on a real hardness boundary,
  which is evidence the frame sizes are *measuring* something true.
- The polynomial deciders answer entailment queries but cannot
  count: implication closure never knows how many independent sets
  there are.
- The Clue solver's actual task in this thread was always
  deduction **with counting** (the verdict grid *plus* exact deal
  counts, 0010): that task is the frame program's native home.

So the program bifurcates:

> **For bare decision**: frames are not optimal; formula-side
> closure algorithms genuinely escape representations. No P ≠ NP
> route here.
>
> **For deduction-with-counting / compilation**: the frame theory
> stands intact — finiteness (pool theorem), the flow matrix, the
> subclass map, and the portfolio question, now sharply posed:
> *is the frame portfolio optimal for model counting?* The measured
> evidence is consistent with yes: every counting-tractable
> subclass met has a frame home, and both frameless subclasses have
> #P-complete counting.

## 5. Status of the program after 0031

- Finiteness of kinds: machine theorem at one coordinate, three
  assumptions isolated (0030) — intact.
- Flow matrix and subclass escape map: complete, now including the
  two falsifier rows — intact as a theory of representation cost.
- Portfolio optimality: **refuted for decision** (this note);
  **open and sharpened for counting** — the surviving conjecture:
  a subclass has a polynomial frame home in the completed taxonomy
  iff its model-counting problem is polynomial.
- Immediate tests of the surviving conjecture: (a) find a
  counting-tractable class and verify a frame home — spanning trees
  (Kirchhoff/matrix-tree: counting poly!) as solution spaces?
  perfect matchings of planar graphs (FKT: poly counting) — do
  planar-matching indicator families have small frames? (b) the
  reverse direction: a frame-homed family whose counting is hard
  would refute it instantly.
