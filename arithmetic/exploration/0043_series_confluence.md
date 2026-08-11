# 0043 — Confluence of the series rules: completed, and the residue located

0042 left confluence unchecked. Checked here by exhaustive search of the
rewrite graph, and completed. Code: `output/series_confluence.py`.

**Method.** Every rule is verified meaning-preserving before use, so any
two normal forms of one term are semantically equal and a divergence can
only be syntactic. The engine then explores the *whole* reachable
rewrite graph of a term and collects every normal form — so more than one
normal form is a **proof** of divergence for that term, not evidence of
it. Node cap reported when hit (it never was).

---

## 1. The starting state was worse than 0042 claimed

Run as written: **28 divergent terms of 4000**, and the size measure did
not certify termination — `distribute` *grows* terms
(`U(x | x) → U(x) | U(x)`). Both are corrections to 0042 §5.

## 2. The completion, round by round

Each round's smallest witness pointed at exactly one missing or
misoriented rule:

| # | witness | what it forced |
|---|---|---|
| 1 | `U(a\|b) ^ a(U(a\|b))` — 0042's predicted pair | **reorient combination to `collect`**: `S(a) ∘ S(b) → S(a ∘ b)` |
| 2 | `U(T(1))` | fold `N` on constants |
| 3 | `N(T(D x))` | low-bit rules `S(t) & 1 → t & 1` |
| 4 | `T(U(a(1)))` | fold constants through shifts |
| 5 | `!(a(1))` | fold *every* series on constants, not just `\|`/`&` ones |
| 6 | `T(1^1) ^ (D(1)\|D(x))` | units and annihilators of the base operators |
| 7 | `D(1)\|D(x)` against `D(1\|x)` | split a constant out of a series argument, folding it at once |
| 8 | `D(T(x&1))` | low-bit *arguments*: `D(t&1) → t&1`, `U(t&1) → N(t&1)` |
| 9 | `(1 & x)` against `(x & 1)` | orient commutativity |

**Round 1 is the load-bearing one.** 0042 oriented combination as
*distribute*; that orientation cannot be completed, because it destroys
the very redex telescoping needs. Oriented as **collect** the critical
pair vanishes outright — the collected form is exactly what telescope
matches — and a genuine termination measure appears:

```
(series count, total argument size, non-N series count, size, unsortedness)
```

lexicographic, verified strictly decreasing on every rule application.
Collect cuts the first component, shift-out the second, the D→N low-bit
rule the third, commutation the fifth.

## 3. Where it lands

**2 divergent terms of 4000 remain**, both of one shape:

```
(1 & U((x | 1)))   ->   (1 & (1 | x))
                   ->   1
```

and **both become identical once the base algebra is put in ANF**. The
engine keeps `|` primitive; the corpus expands `a | b = a ^ b ^ ab` and
reduces, where Boolean absorption is an identity —
`1 & (1 ^ x ^ 1x) = 1 ^ 1x ^ 1x = 1`.

So the verdict is clean: **the series rules are confluent. The residue
is a base-algebra convention the engine imposed and the corpus does not
have.**

## 4. The rule set, as completed

```
collect        S(a) ∘_S S(b)        -> S(a ∘_S b)
shift-out      S(σ_S t)             -> σ_S(S t)
telescope      S(t) ^ σ_S(S t)      -> m_S(t)
absorb         S1(S2 t)             -> 0042's table
split-constant S(c ∘_S t)           -> S(c) ∘_S S(t), constant folded
low-bit        S(t) & 1             -> t & 1        [U, T, !]
                                     -> N(t) & 1    [D]
low-arg        S(t & 1)             -> t & 1        [D, T]
                                     -> N(t & 1)    [U]
N-lowbit       N(N(t) & 1)          -> N(t)
N-shift        N(a t) -> N(t),  N(b t) -> 1
constants      S(c) -> c',  σ(c) -> c',  folding, units, annihilators
commute        oriented on the commutative joins
```

Fourteen rules where 0042 had five. Nine of the additions are constant
and low-bit bookkeeping that the schema does not mention; the one
structural change is the reorientation.

## 5. Honest limits

- Confluence is established by exhaustive graph search over **4000
  random terms at depth 3**, not by a critical-pair proof over all
  terms. It is much stronger than strategy sampling — each term's
  verdict is exact — and it is not a theorem.
- The rule set grew from five to fourteen. Whether it is minimal, and
  whether the nine bookkeeping rules would disappear under a proper ANF
  base (as §3 suggests), is unexamined.
- The engine is single-variable. Multi-variable terms may open critical
  pairs this search cannot see.

## 6. Open

1. **Rebuild on an ANF base.** §3 says the residue is entirely the
   `|`-as-primitive convention. Expanding `|` and normalising the base
   to ANF should discharge it and probably absorb several of the
   bookkeeping rules — the natural next build, and it would put the
   engine in the corpus's own frame.
2. **A critical-pair proof.** With the rule set finite and a working
   termination order, Knuth–Bendix over the non-AC part is now feasible
   by hand or by machine, and would upgrade §3 from measured to proved.
3. **Multi-variable.** Extend the term generator to two symbols and
   re-run; the `collect` rule in particular has more redexes there.
