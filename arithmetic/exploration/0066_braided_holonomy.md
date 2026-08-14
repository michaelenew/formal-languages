# 0066 — Braided holonomy: where the frame's commutativity breaks

Thread 4. Every paradox through 0063 had cyclic holonomy, and 0060
proved a single causal channel can produce nothing else. The door
is the *second loop through a shared channel*. Code:
`output/braided_holonomy.py`.

---

## 1. The group tax

Two reference loops with monodromies σ, τ on a shared fiber;
revision picks a loop at random. Verified by exact elimination: the
stationary space is exactly the mixtures of uniforms on the orbits
of the **generated group** ⟨σ,τ⟩, so the tax law generalizes
verbatim:

```
forced entropy = log₂(smallest orbit of ⟨σ, τ⟩)
```

σ=(01), τ=(12) on a 3-valued channel: ⟨σ,τ⟩ = S₃, transitive —
**tax = log₂3 ≈ 1.585 bits**, Haar on a nonabelian group's orbit.
The first non-cyclic coin.

## 2. Order becomes observable

Audit loop A then B versus B then A: the results differ by the
commutator [σ,τ] — for the S₃ pair, a 3-cycle: a deterministic,
state-independent discrepancy. For every abelian pair (all systems
of 0059–0063) the residue is the identity: parity was the *only*
path-memory. Noncommuting loops remember the **word** of the
traversal, not just its length mod 2 — path-dependence beyond
parity, the permutation shadow of braiding. (True anyonic braiding
adds phases on top — the amplitude level of this, as 0059 §5's cat
states were to the liar.)

## 3. Where binary fails and braiding begins

All monodromies of a 1-bit fiber commute (S₂ is abelian): **no pair
of binary loops can braid**. A shared 2-bit channel suffices: swap
and flip generate D₄ (order 8), noncommuting. So the exact door:
braiding enters with the second loop through one shared
multi-valued channel — never earlier, by 0060's cyclic theorem for
single causal channels.

## Honest limits

- The two-loop "revision" is a Markov chain (random loop choice),
  the natural multi-loop extension of the deterministic revision
  map; the stationary characterization is verified by exact
  elimination in every case shown.
- "Permutation shadow of braiding" is a structural statement (S_n
  vs B_n); no claim that the frame realizes anyonic *statistics* —
  that needs the amplitude level.

## Open

1. Express the S₃ pair as genuine frame syntax (two definition
   loops sharing a 2-bit channel with `^`, `&`, `a` bodies) and
   re-run the census: how common is braiding among random two-loop
   systems?
2. The amplitude enrichment: quantize the two-loop system (unitary
   per loop) — the invariant states of noncommuting unitaries are
   the frame's first non-abelian "anyon" sector; does the
   zero-entropy buy-back (0059 §5) survive noncommutativity, and
   what replaces the cat state? (Common eigenvectors need not
   exist — the first candidate for a paradox whose quantum tax is
   *not* zero.)
