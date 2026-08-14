# 0065 — The reference tower and the fourth bucket

Thread 3, plus the user's holonomy-of-knowledge thesis made as
precise as the frame allows. Code: `output/the_reference_tower.py`.

---

## 1. Gauge-fixing works and costs exactly the tax

m liars plus a reference liar: every bit-relative-to-reference is
invariant and **exact** in every floor solution — the reference
converts all relative bits to definite values ("absolute in the
reference gauge") — and the system's floor stays exactly 1 bit: the
reference's own coin. Verified m = 1..4 with 1 and 2 references.

## 2. The tower never closes

Adding more references never reaches 0 bits. Each new reference has
no sheet of its own to stand on; the residual coin is conserved
under gauge-fixing. This is the frame's shape of **iterated
incompleteness**: add the axiom "the intended sheet is this one" and
the extended system has a fresh undecided sheet (PA → PA+Con(PA) →
…, as dynamics).

## 3. The four buckets

Toy: models = the hexagon's two global solutions, deck-swapped;
the language's observables = deck-invariant functions. Verified:

- a statement is **decided iff deck-invariant** (all 30 pairwise
  parities: same truth in both models);
- all 12 literals are **independent** (true in exactly one model),
  and the deck is a bijection pairing each independent statement
  with its dual in the other model — "the locus is its own dual,"
  now a computed bijection.

So the fourth bucket — *true, but inexpressibly so* — is: **truth on
the intended sheet, where "intended" is not deck-invariant and
therefore not a statement of the language.** Provable = true on
every sheet (deck-invariant truth); the Gödel sentence is a relative
bit read as if it were absolute.

The bleed-back question ("why does uncertainty come in from the
boundary?") inverts: the sheet-distinction only *exists* at the
boundary — the sheets agree at every finite stage (that is exactly
why both are consistent) — while the language's access is finite.
Nothing bleeds in; rather, a boundary degree of freedom casts a
shadow on finite syntax, and the shadow is the independent
statements. In arithmetic proper the deck is not Z₂ but the Cantor
space of consistent completions (each independent sentence is one
local double cover; Lindenbaum's tree iterates them), which rhymes
with the odometer's Haar-on-2^ω — stated as rhyme, not theorem.

## 4. Guarded loops carry no holonomy

`n := ¬a(n)` — an odd-negation loop *with depth* — has a one-point
core at every width: **depth kills holonomy**. A loop carries
holonomy only if it closes at the same level: depth-0 syntax (the
liar) or the boundary (read-back through h, 0054/0055). This is the
user's "every finite cycle is even," corrected and sharpened:
finite guarded travel always descends, so it cannot come back odd;
Gödel's diagonal sentence closes its loop *through the unbounded
proof-search* — through the boundary — and that is why the
obstruction is a cliff (0057): holonomy is a class, not a quantity;
no finite stage carries a fraction of a parity.

## Honest limits

- §3's logic mapping is a two-model toy; real arithmetic has
  continuum-many completions and the "intended sheet" (the standard
  model) is singled out semantically, not by symmetry — the
  deck-invariance criterion models *first-order expressibility*
  (provable = true in all models is the completeness theorem; the
  indefinability of standardness is compactness/overspill), cited
  not re-proved.
- §4 identifies Gödel's loop-closure with boundary read-back by the
  structure of Prov (Σ₁ search); the identification is an argument,
  not a formalized theorem in the frame.

## Open

1. Formalize "theory tier" in-frame: sentences as guarded objects,
   models as sheets of a co-guarded completion — can the four
   buckets be *computed* for a small essentially-undecidable system
   (e.g., the frame's own N-channel statements)?
2. The tower's limit: references indexed by ordinals (the frame's
   analogue of iterated consistency extensions) — does the residual
   coin survive every constructive limit?
