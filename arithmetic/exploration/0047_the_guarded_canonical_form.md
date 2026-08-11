# 0047 — The guarded canonical form: it exists, and the wall is elsewhere

The target: a canonical form sound and complete for *true* statements —
terms denoting the empty set — allowed to be sloppy about which nonempty
set a false statement denotes, so that whatever is undecidable gets
pushed out of the true class.

Short version. The guard buys nothing on the decision side, because `^`
turns every equality question into a zero question. But the question it
leaves is **decidable**, the guarded form **exists**, and `N` is exactly
the guard. What the exercise finds is not a wall of undecidability but
two other things: the current rule set is both incomplete *and* unsound
outside the width it was measured at, and the canonical object is not a
term. Code: `output/guarded_canonical_form.py`.

---

## 1. The guard does not shrink the problem

```
E1 = E2   iff   E1 ^ E2 = 0
```

`^` is in the signature, so a procedure recognising exactly the true
statements *is* a decision procedure for the word problem. There is no
smaller problem hiding behind "only the true ones". 200 random pairs:
`equal(p, q)` and `decide_zero(p ^ q)` never disagree.

What the guard **can** weaken is the *output*. A zero test owes nothing
to the nonzero terms and need not put them in any normal form at all.
That is the only sense in which "guarded" is a real weakening, and §4 is
what it buys.

## 2. The invariant is not LSB-causality. It is bounded state.

0045 §4 found every operator but `N` is LSB-causal — bit *i* of the
output depends only on bits ≤ *i* of the input. That is necessary and it
is not what decides. The property that decides is that the state carried
between positions is **finite**:

| node | state | output |
|---|---|---|
| `x` | none | input bit |
| `Ω` | none | `1` |
| `n` | position counter, capped at `n.bit_length()` | `(n >> pos) & 1` |
| `a` | 1 bit (delay) | previous child output |
| `^`, `&` | none | pointwise |
| `!` | 1 bit — parity so far | `parity ^ t` |
| `U` | 1 bit — seen a 1 | `seen \| t` |
| `T` | 1 bit — all 1s so far | `alive & t` |
| `lowset` | 1 bit — seen a 1 | `t & ¬seen` |
| `lowzero` | 1 bit — all 1s so far | `alive & ¬t` |
| `N` | **not finite state** | — |

So an `N`-free term is a finite Mealy transducer read LSB upward, and
"is it identically 0" is **reachability**: no reachable state emits a 1.
Verified against the straight recursive interpreter — 24000 runs over
4000 random terms in two free variables, bit for bit.

Reachable state counts stay small: 2 for each operator alone, 3 for
`!(U(T(a(x))))`.

## 3. `N` is the guard, and the guard is all it costs

`N`'s bit 0 is the OR of every input bit, so no bounded state read from
the LSB can produce it. Fix each `N` subterm to `0` or to `Ω` and what
remains is finite-state. The guess is discharged inside the same run:
alongside the machine state, carry one flag per `N` argument recording
whether it has emitted a 1 yet, plus one for the root. After the input's
finite support the term can still emit, so each reachable configuration
is closed under a tail of zeros until nothing moves. A guard is
*consistent* when the settled flags match it, and the term is refuted
when some consistent configuration has the root flag set.

Cost: 2^k reachability sweeps for k distinct `N` subterms. Against
exhaustive evaluation on 1500 random terms — 155 decided empty, 1345
refuted — every refutation carries an input that evaluates nonzero, and
no term called empty is nonzero under brute force at width 11.

The rules 0038 and 0042 found by hand come out of the guard alone; the
procedure has no rule for `N` at all:

```
N(x) ^ N(x)       N(N x) ^ N(x)     N(a x) ^ N(x)
N(b x) ^ Ω        N(U x) ^ N(x)     N(T x) ^ N(x&1)      all TRUE
```

## 4. The guarded canonical form

```
term  ↦  { (guard, minimal Mealy machine under that guard)
           : guard consistent, i.e. realised by some input }
```

Minimisation is reachable-then-refine, renumbered breadth-first, so the
machine is a canonical tuple — equal functions give equal tuples. And:

> **the statement holds iff every entry is the zero machine.**

600 random terms: this and the §3 decision procedure never disagree.

Seven pairs, checked both ways — semantic equality and machine identity
give the same verdict every time:

```
!(t) ^ a(!t)   =  t                       machines match
U(t) ^ a(U t)  =  lowset(t)               machines match
T(t) ^ b(T t)  =  lowzero(t)              machines match
lowset(t)      =  lowzero(t ^ Ω)          machines match
T(x) & U(x)    =  T(x) & x                machines match
U(x) ^ U(a x)  ≠  lowset(x) ^ x U(a x)    machines differ
!(U x)         ≠  lowset(x)               machines differ
```

**This is the answer to the question as asked, and it is a positive
one.** At the 0046 signature there is a guarded canonical form, it is
sound and complete for truth, and nothing is undecidable. The price is
in §7.

## 5. What breaks in the existing primitives — two different defects

Running 0044/0045's rewrite engine against the unbounded decision
procedure, on 836 terms from both of its generators, separates two
failures that look alike and are not:

**WIDTH-BOUND — the rules identify too much.** 30 of 836 normal forms
do not mean what the term meant.

```
a(Ω)   ->   510          at WIDTH = 9
!(Ω)   ->   341
U(a 1) ->   510
```

`fold` evaluates a constant argument inside a fixed width. Unboundedly
`a(Ω) = Ω ^ 1`, which is *cofinite* and is not any finite constant; 510
is its truncation to the window the engine happens to use. **These
rewrites are sound at width 9 and at no other width.** That is a defect
in 0043–0046, not in the objection to them, and §6 is the repair.

**INCOMPLETE — the rules identify too little.** 3 of 836 terms are
identically empty and do not normalise to `0`; 92 pairs mean the same at
every width and reach different normal forms. As named laws, each true
at every width and each missed:

| law | normal forms reached |
|---|---|
| `b(x) = a(x) ^ 1` — 0046 §1 | `b(x)` vs `1 ^ a(x)` |
| `T(a x) = 0` — `T` dies on an even argument | `T(a(x))` vs `0` |
| `U(b x) = Ω` — `U` saturates on an odd one | `U(b(x))` vs `Ω` |
| `N(x&1) = !(x&1)` | `N(x&1)` vs `!(x&1)` |
| `a(Ω ^ x) · b(x) = 0` — complementary shifts | `a(Ω^x)b(x)` vs `0` |
| `7 = 1 ^ 6` | `7` vs `1 ^ 6` |

Six of six. These are not near-misses of existing rules. Each needs a
fact the rule language cannot state: what bit 0 of an argument is, that
two atoms are complementary, that `b` is not primitive, that two
constants are one constant.

**A correction to 0044.** That last row is a claim from 0044's own
census, which listed `fold-of-two-constants` among the rules "gone —
building an ANF polynomial already does them". It is not gone. A
constant is a monomial with no atoms and `xor` is symmetric difference
on monomials, so two constants with *different* masks are two monomials
and stay two:

```
engine.xor(const 1, const 6)  ->  `1 ^ 6`   2 monomials, 0 rewrites
                                  const 7   ->  `7`, 1 monomial
```

ANF absorbs folding only when the masks are equal, where cancellation
does it. The census overstated the representation.

## 6. The new primitive: constants are lassos

The two defects have one cause. **The constants of this language are not
closed under its own operators.** `U` of any nonzero finite set is
cofinite; `!` of the universe alternates forever. An `int` cannot hold
either, and a width-`W` int silently truncates it — which is exactly
`fold`'s unsoundness.

Every closed term is a machine with no input, so its run is a **lasso**:

```
0          0(0)^ω        finite
1          1(0)^ω        finite
Ω          ε(1)^ω        not a finite constant
a(Ω)       0(1)^ω        not a finite constant
!(Ω)       ε(10)^ω       not a finite constant
U(a 1)     01(1)^ω       not a finite constant
!(1)       1(1)^ω        not a finite constant
lowset(Ω)  1(0)^ω        finite
N(b 0)     1(1)^ω        not a finite constant
```

So the answer to "is a new primitive necessary in the language of the
canonicalisation" is **yes, and it is not an operation**. 0046's eight
still generate everything. What has to change is the *constant*: the
closure of `{0, 1}` under the signature is the ultimately periodic sets,
and the rewrite system's constants must be written as `(prefix)(cycle)^ω`
rather than as integers.

That is 0046 §2's split arriving a second time — a symbol canonicality
needs that the algebra does not — and it now has two members: the
measures, and the lasso constants.

## 7. Where the wall actually is

Not undecidability. Two other places.

**Canonicity leaves the term language.** The canonical object of §4 is a
minimal machine. The rewrite system cannot reach it because a normal
form is a term and the equivalence classes are not term-shaped — `7` and
`1 ^ 6` are one machine and two normal forms. Any complete term-level
canonical form would have to be at least as expressive as the minimal
machine, which is what §6's lasso constants begin to concede.

**The frontier is bounded state, and `N` is not on it.** Residual counts
of two-input functions, read LSB upward, tails of 5 bits:

| prefix read | `x ^ y` | `x + y` | `x * y` |
|---|---|---|---|
| 0 | 1 | 1 | 1 |
| 1 | 1 | 2 | 4 |
| 2 | 1 | 2 | 16 |
| 3 | 1 | 2 | 64 |
| 4 | 1 | 2 | 256 |
| 5 | 1 | 2 | 1024 |
| 6 | 1 | 2 | 4096 |

`x ^ y` needs one state; `x + y` needs two — the carry — and **addition
is therefore free**, a finite-state operator the corpus does not have
and could take at no cost to any of this. `x * y` is LSB-causal, so
0045 §4's test passes it, and its state count multiplies by four with
every further bit read.

So the wall is: a term must not need to remember an unbounded amount
about the prefix it has read. Every operator in the 0046 basis stays
under that line. Variable-by-variable multiplication crosses it, and a
decision procedure of this shape stops existing there.

*Context, not measured here:* this is the shape of the classical
boundary — monadic second-order theory of `(ℕ, succ)` is decidable
(Büchi), and of `(ℕ, +, ·)` is not. The signature sits on the decidable
side, and the residual table is a measurement of why, not a proof of the
theorem.

## 8. Honest limits

- The decision procedure is **verified, not proved**. Its delicate parts
  are the zero-tail closure and the guard-consistency check; both are
  supported by 1500-term agreement with brute force and by 600-term
  agreement between two independent routes (`decide_zero` and
  `guarded_canonical_form`), not by an argument.
- Brute force can only refute "empty at every width" at *one* width, so
  §3's second column bounds the error in one direction only. The
  agreement in the other direction — every refutation carries a
  witnessed input — is exact.
- The head-to-head in §5 is single-variable, because the engine is.
  Machines here handle several variables and the two-variable claims are
  only in §2 and §7.
- `Machine` shares identical subterms, so guards are per *distinct* `N`
  subterm. Correct — `N` is a function — but it means the guard count is
  a property of the term's DAG, not its tree.
- §6's lasso repair is stated and its need is measured; the rewrite
  system has **not** been rebuilt over lasso constants. That is the next
  piece of work, not a result here.

## 9. Open

1. **Rebuild `fold` over lassos.** The immediate consequence of §5–§6,
   and the only way the existing rule set becomes width-independent. It
   should also discharge `7 = 1 ^ 6` for free.
2. **How far can rules go before the machine is needed?** §5's six laws
   are all rule-shaped — bit-0 knowledge, complementary atoms, `b`
   elimination. Adding them shrinks the gap without closing it. Knowing
   *which* identities are unreachable by any finite rule set over this
   signature is the sharp form of §7's first wall.
3. **Take addition.** §7 says `+` costs one bit of state. The corpus has
   never had it, and 0034–0036's counted tier is exactly where it would
   land.
4. **What does the guard count measure?** 2^k sweeps for k `N`
   subterms, and 0045 §4 called `N` the language's one downward channel.
   Whether k is ever forced to be large — or whether `N` subterms can be
   merged the way the machine merges states — is untouched.
