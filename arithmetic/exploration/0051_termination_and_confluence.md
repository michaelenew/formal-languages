# 0051 — Expand-and-cancel: terminates? No. Confluent? No. Both are theorems.

Asked: check termination and confluence of 0050's expand-and-cancel,
hard proof, computationally verified. Both fail, each with a finite
machine-checked certificate, and each failure is structural rather than
a defect — non-termination is the ineliminability of the series names,
and non-confluence is `N`'s missing fixpoint law, made local. The audit
also caught one unsound rule and two missing ones that 0048–0050's
sampling never touched. Code: `output/termination_and_confluence.py`.

---

## 1. The inner loop terminates — a real reduction order

The local rules (0048's set, `collect` and `telescope` deleted). A
counting measure **provably cannot work**, and the reason is worth
keeping: `shift-out` on the `b` shift rewrites

```
S(b t)  →  b(S t)  =  a(S t) ^ 1
```

a one-atom pattern into a **two-monomial polynomial**, so every sibling
atom in the monomial is duplicated and any global count can grow. (0043,
0044 and 0048 all reported measured termination with counting measures;
their samples happened not to put `shift-out`'s b-case under a product.
The violation is exhibited in code.)

A **multiplicative interpretation** absorbs duplication natively:

```
W(polynomial) = Σ monomial weights          (0 for `0`)
M(monomial)   = Π atom weights              (1 for `Ω`)
w(x) = w(1)   = 2
w(a(P))       = 2·(W(P) + 1)
w(S(P))       = 2·K^(W(P)+1)     series and measures
w(N(P))       =    K^(W(P)+1)                        K = 2048
```

A monomial is a *product*, so replacing an atom of weight `w` by a
polynomial of weight `< w` shrinks the monomial regardless of what
multiplies it, and XOR cancellations only remove more. Every constructor
is strictly monotone, so the per-rule root inequalities are the whole
proof. Each is an instance of "K^linear beats linear":

| rule | root inequality |
|---|---|
| settle, unit | `2K^(n+1) > B₀` — the largest emitted constant weighs 241 |
| absorb | exponents: `2K^(n+1)+1 > 2n+2` |
| shift-out (a and b cases) | `2K^(2n+3) > 2(2K^(n+1)+1) + 2` |
| confine | `2K^(n+1) > K^(n+1)` and `> n` |
| low-bit | `2K^(n+1) > n+1`; masked monomial dies: `M ≥ 4 > 2` |
| N-see-through | `K^(2n+3) > K^(n+1)` |
| N-absorb, contain | a monomial loses a factor `≥ 2` |

All checked exactly for `n = 0..600` (beyond which each is monotone),
and the full inequality is audited on every sampled rule application
whose weight is computable (weights are towers for nested series; the
towers are skipped and counted). **The inner loop terminates from every
term.**

## 2. The inner loop is not confluent — and the audit caught an unsound rule

Because L terminates, its complete normal-form set is computable
*exactly*, so "two distinct normal forms" is a finite decidable
certificate. Smallest one found:

```
1x | U(1x)   -->*   N(1x)
1x | U(1x)   -->*   N(1x) ^ 1x ^ N(1x)·1x
```

both irreducible, both the same set. By Newman's lemma a terminating
system with a non-unique normal form fails local confluence. **L is
terminating and not confluent.**

The second form should reduce — it is `1x | N(1x)`, and `1x` vanishes
wherever `N(1x)` does — but 0048's port of `N-absorb` tests the sibling
monomial's atoms one at a time against the guard's argument, and dropped
0044's `inside` clause that catches the sibling equalling the argument
as a whole monomial.

**Correction to 0048, methodological.** Its harness never tested this:
`verify_what_is_still_not_identified` filtered with
`if capped or len(forms) != 1: continue`, silently dropping every
divergent term. 0048 §5's "0 unsound identifications" was measured on
the survivors only.

**Correction to 0048, a real bug.** The same exhaustive scan found a
divergent pair that was *not* semantically equal, which is worse than
non-confluence — and replaying steps found the culprit:

```
shipped:   T(lowzero t)  →  lowzero(t & 1)      UNSOUND at t = Ω
true law:  T(lowzero t)  =  lowzero(t) & 1
```

The absorb table's `low` flag masks the *argument*; this law needs the
mask *outside*, which the table cannot express. `lowzero(Ω) = ∅` so the
left side is `0`, while `lowzero(Ω&1) = a(1)`. The entry is removed (the
neighbouring three measure-absorb entries were re-audited against the
decision procedure and are sound; `T(lowset t) → lowset(t&1)` survives
only because `lowset(t&1) = t&1 = lowset(t)&1` — an accident of `lowset`
that `lowzero` does not share). Found by the confluence audit, exactly
as 0044's unsound rule was found by the divergence search: **the
confluence check is the strongest bug-finder this workstream has.**

## 3. Expansion does not terminate: one infinite path, no strategy escapes

```
X_k  =  x ^ a(x) ^ … ^ a^(k-1)(x) ^ a^k(!(x))
```

Machine-checked for `k = 0..40`: `X_k` has **no local redex and exactly
one expansion**, and that expansion is `X_{k+1}`; sizes strictly
increase. The induction is one line — `X_k`'s only operator atom is the
`!` under `a^k`, whose argument `x` fires nothing, and its unique
unfolding is `X_{k+1}`. The reduction graph of `!(x)` is a single
infinite path: non-termination with **no choice anywhere**, so no
strategy avoids it.

## 4. Worse: there are no normal forms to reach

Weak normalization fails too, and the proof is the corpus's own locality
argument (0002 Prop 4) promoted to the whole system.

- **Every series-free, N-free term is d-local** — output bit `i`
  depends only on input bits in `[i−d, i]`, `d` = the term's `a`-depth.
  Structural induction (`x`, `1`: 0; `^`,`&`: max; `a`: +1);
  machine-checked on 7.6 million window checks at width 11.
- **No series or measure is d-local for any d** — witness pairs for
  each of `!`, `U`, `T`, `N`, `lowset`, `lowzero` at every `d ≤ 8`:
  inputs agreeing on the whole window whose outputs differ at bit `i`.
- **N-guards do not help**: on the family `x_r = 1<<r` every guard flag
  `N(P(x_r))` is eventually constant (each monomial of a flat `P` is a
  constant mask times at most one shifted copy of a single bit —
  machine-checked), so a flat-plus-guards term agrees with one local
  function on a tail of the family, and `U` separates `x_p` from `x_q`
  inside a shared window there.

Any normal form is flat-plus-guards (every series atom outside an `N`
argument is expandable, by construction). So **`U(x)` has no normal
form at all** — nothing in its reduction graph is irreducible. The same
holds for `!` and `T`. Expand-and-cancel is not weakly normalizing,
*necessarily*: the series names denote non-local operators and normal
forms can only say local things. Non-termination is the statement that
`U`, `!`, `T` are irredundant — 0042 §1's collapse read as a rewriting
theorem.

## 5. Expand-and-cancel is not confluent — the certificate

```
!(x&1)  --confine-->  N(x&1)
!(x&1)  --expand--->  x&1 ^ a(!(x&1))  -->L*  x&1 ^ a(N(x&1))
```

Machine-checked: both results irreducible (no local rule, no expansion —
`N` has no unfolding and nothing beneath it is reachable), distinct, and
equal at every width. A finite counterexample to confluence.

**The diagnosis is exact.** `confine` knows `!(p) = N(p)` on a one-bit
`p`; expansion can unfold `!` but not `N` — `N` is the one operator with
no fixpoint law (0042 §3). Once one copy of the redex is confined and
another expanded, nothing chases the `a(N(…))` tail back down. The
failure of confluence *is* the failure of `N` to have an expansion, made
local. 0047 found the same operator to be the machine's guard; this is
the sentence form of that fact: **`N` is where determinism dies.**

## 6. Knuth–Bendix on the wreckage: two missing rules, surfaced not guessed

Orienting the certificate's join by §1's order gives

```
N-fold        C·p ^ C·a(N p)  →  C·N(p)        [p confined to bit 0]
```

— which is a real law: a one-bit `p` propagates through `N` exactly as a
`^` series would, so `N` restricted to bit-0 arguments has the fixpoint
`N(p) = p ^ a(N p)`. The schema could not give `N` an *expansion*;
completion hands it a *contraction*, on the one domain where it has one.
(The common factor `C` is 0050's telescope lesson again: ANF distributes
products, so the pattern is monomial families, not atoms.)

The peak census surfaced a second, independent family with no `N` in it:
expanding a measure on a constant manufactures products of disjoint
shifted constants — `a(a(1))·a(1)` — that denote `0` and that no rule
removes. Hence

```
annihilate    m  →  0     [m has a finite support bound and its known
                           prefix across that bound is all zero]
```

generalizing `low-bit`'s prefix case from mask-1 monomials to any
bounded monomial. Both rules are machine-checked meaning-preserving and
both fit §1's reduction order (a monomial pair becomes one lighter
monomial; a monomial disappears).

Census, bounded join search: **before repair 46 of 471 peaks unjoined;
after, 23 of 477** — and the certificate peak and the stuck-truth
example below both heal. Completion is *not* run to closure: the remaining unjoined
peaks are reported, a bounded search proves nothing about them, and the
repaired system's confluence is a conjecture. The theorem is the
negative one.

## 7. What non-confluence means: the procedure must be a search

Every rule preserves meaning and `0` is irreducible, so **reaching `0`
on any path is a proof**. Non-confluence means the converse discipline
is impossible:

```
!(x&1) ^ N(x&1)        a TRUE statement (≡ 0)
  --confine-->  0                      in one step
  --expand--->  …  -->  x&1 ^ a(N(x&1)) ^ N(x&1)    irreducible, ≠ 0
```

A true statement can reduce to a stuck nonzero term. So "normalize and
read off the answer" is not a decision procedure here — "search for 0"
is, and 0050's `decides` (any-path-to-zero, capped searches kept) is
forced, not a convenience. This also retro-justifies 0050's
capped-search correction from first principles.

## 8. Honest limits

- §1 is a proof (interpretation + per-rule root inequalities), with the
  grid `n ≤ 600` checked exactly and monotonicity beyond it immediate;
  the exact audit skips weight-towers (nested series) and says so.
- §2's and §5's certificates are exact and decisive. The *diagnosis*
  sentences (which clause is missing, why `N` is the cause) are
  argued, not proved — but §6's repairs healing exactly those peaks is
  strong evidence the diagnosis is right.
- §4's flag-settling lemma is machine-checked on flat guard arguments;
  the nested-guard case is argued by induction in prose, not verified
  separately.
- §6's census is a bounded search on sampled peaks: "23 unjoined" means
  not joined *within budget*, nothing more. No confluence claim is made
  for the repaired system.
- Everything is single- and two-variable, widths ≤ 24, and soundness
  checks go through 0047's verified-not-proved decision procedure.

## 9. Open

1. **Run completion to closure.** N-fold and annihilate are rounds one
   and two. The remaining unjoined peaks (absorb-vs-expand,
   expand-vs-expand around `!`/`U` products) are the next critical
   pairs; whether the process stabilizes at a finite rule set is
   exactly the question "is truth-search normalizable away from `N`".
2. **Confluence of the N-free fragment.** Every ingredient of §5's
   certificate needs an N-minting rule. Conjecture: L+E restricted to
   N-free terms with N-minting rules removed is confluent. The census
   machinery is ready to test it.
3. **The N-fold domain.** `N(p) = p ^ a(N p)` holds on bit-0-confined
   `p`. The general `N(t)` has no fixpoint in the signature — but 0047
   §3 decided `N` by carrying one emission flag per guard. Whether that
   flag can be internalized as a *bounded family* of N-folds (one per
   known-prefix position) is the sentence-form version of the guard,
   and would say precisely how much of `N` rewriting can recover.
4. **Weight-aware search.** §1's order gives a principled priority for
   `decides`: prefer steps that shrink the interpretation. Whether that
   search is complete for truth on the repaired system is open and now
   measurable.
