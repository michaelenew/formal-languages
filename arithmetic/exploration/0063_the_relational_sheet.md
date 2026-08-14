# 0063 — The relational sheet: absolute parity is gauge, relative parity is physical

The user read 0062's T^k = ¬ two ways: "N moves pins your belief at
½, but 2N moves pins it as 'whatever I see now'"; and "observation
parity splits the universe into a self-dual pair — exactly two
consistent states of the rest you can't see, even for yourself."
Both verified, with one correction of scope and one upgrade from
"can't see" to "gauge". Code: `output/the_relational_sheet.py`.

---

## 1. N moves pin ½; 2N moves pin nothing — exactly

Any stationary belief is invariant under every power of T, in
particular under T^k = complement — so it is complement-symmetric and
**every channel's marginal is exactly ½**. The forced coin comes
entirely from the odd power. Invariance under T^{2k} = id is vacuous:
a point mass ("whatever I see now") survives 2k moves unchanged.
Verified k = 3, 5 over random rational stationary mixtures.

## 2. Observation has a parity

Reading channel j from channel i through the constraint chain
complements once per hop: on the double cover (verified on both
lifted solutions, k = 3, 5), **even paths read the value, odd paths
its dual** — 0-hop and 2-hop observation are the same observation;
1-hop is the other one. What oscillates at successive encounters is
path parity, always between the same two values. The bipartition of
the cover *is* this parity.

## 3. The sheet is relational

Two liars jointly (0062's diagonal deck group — the individual flip
is not a power of the joint traversal, verified):

| observable | status |
|---|---|
| either liar's own value | marginal ½, forced — **gauge** |
| XOR of the two | invariant under the dynamics, **exact** in every floor solution |
| total floor entropy | 1 bit (the shared coin), not 2 |

Two triangles: "do their constant worlds agree" is invariant under
the joint dynamics; "which world is mine" is not. So the upgrade of
the user's phrasing: the two dual states of the rest of the universe
are not merely *unseen* — the absolute sheet is **gauge** (no
observable of the dynamics refers to it), while every *relative*
sheet between subsystems is a free, exact, agreed-upon observable.
You cannot know which of the two dual worlds you are in, and everyone
agrees about every difference. This is the frame's version of the
neutron-interferometry fact: a 2π rotation of the whole universe is
invisible; a 2π rotation of one arm relative to the other shifts the
fringes.

## 4. "Exactly two" is the Z₂ case

Two odometers jointly: the difference (a − b) mod 2^w is invariant
and exact; each absolute position is forced-uniform (w bits of
compulsory noise); the deck group is Z_{2^w}. So "everything is its
own dual" is the holonomy-Z₂ case of a graded law: **everything is
its own d-fold echo** — d consistent unobservable positions of the
rest of the world, with all differences shared and exact. The dual
pair dominates because the cheapest paradox has period 2.

## Physics registration (context, from the conversation)

The user's speculation instantiates known structure at three scales:
exchange parity (spin–statistics: odd/even permutations act as ∓1;
the two sectors are the boson/fermion split); univalence and
fermion-parity superselection ("splits the universe in two" is the
superselection sector structure; the 2π-rotation sign was measured
relationally in neutron interferometry, 1975); and Majorana pairs
(one occupation bit shared by two separated sites, invisible to
either — "two consistent states of the rest you can't see" is the
topological qubit). In 2+1 dimensions the parity of interaction
order enriches to the full braid word (anyons) — the native home of
the knot counter, where *more* than parity is physical.

## Honest limits

- All checks exhaustive/exact at stated sizes; §1's claim uses
  stationarity = invariance under T (hence all powers) — beliefs
  required to be consistent only with T^{2k} genuinely are
  unconstrained, which is the user's point stated operationally.
- The gauge language is an identification, not extra mathematics:
  "gauge" = the orbit of the deck action on solutions; "observable"
  = deck-invariant function. The physics registrations are context.

## Open

1. **Gauging the sheet.** If the absolute sheet is gauge, the frame
   should admit a gauge-fixing story: adding one reference channel
   ("the vacuum's sheet") that converts relative bits to absolute
   ones — and the cost of the reference should be exactly the 1-bit
   tax, paid once per world. Checkable.
2. **The braid enrichment.** The frame's traversals commute (cyclic
   deck groups). A frame variant where two traversals do *not*
   commute (braided rather than cyclic holonomy) would be the
   arithmetic analogue of anyons — and 0060's causal-conjugacy
   theorem says it cannot come from single-channel causal maps, so
   it needs at least two interacting channels. Where exactly does
   the frame's commutativity break?
