"""What is actually primitive, and what every operator does to a bitstring.

Three eliminations, verified, then a worked example of every surviving
operator with its expansion written out beside it.

  constants  -- a constant is an `a`/`b` chain over `0`: reading n's
                binary MSB-first, `a` for a 0 bit and `b` for a 1 bit.
                So `0` is the only constant needed. Equivalently `1`
                with `a` and `^`, since `b(t) = a(t) ^ 1`; that basis is
                smaller because `0 = 1 ^ 1`.
  Ω          -- `N(b(0))`. The universe comes out of the one operator
                that manufactures it.
  measures   -- `lowset` and `lowzero` are not primitive operations.
                Each is its own telescoping (`lowset(t) = U(t) ^ a(U t)`)
                and they are each other under complement. They must
                still be *symbols* in the rewrite system, though --
                telescope exists to package that pattern into an atom no
                rule can reopen, and expanding it makes the rule the
                identity. Algebra signature and rewrite signature are
                different lists.

Leaving eight primitive operations: `1`, `a`, `^`, `&`, `!`, `U`, `T`,
`N`.

Run directly for the verification suite.
"""

from __future__ import annotations

WIDTH = 8
MASK = (1 << WIDTH) - 1

a = lambda v: (v << 1) & MASK
b = lambda v: ((v << 1) | 1) & MASK
N = lambda v: 0 if v == 0 else MASK

bits = lambda v: format(v & MASK, f"0{WIDTH}b")


def series(join, step, value):
    """`x ∘ σ(x) ∘ σ²(x) ∘ …`, and the terms it went through."""
    combine = {"^": lambda p, q: p ^ q, "|": lambda p, q: p | q,
               "&": lambda p, q: p & q}[join]
    total, lifted, terms = value, value, [value]
    while True:
        lifted = step(lifted)
        nxt = combine(total, lifted)
        terms.append(lifted)
        if nxt == total and lifted in (0, MASK):
            return total, terms[:-1]
        total = nxt


bang = lambda v: series("^", a, v)[0]
up = lambda v: series("|", a, v)[0]
trail = lambda v: series("&", b, v)[0]


# ---------------------------------------------------------------------
# 1. constants are chains
# ---------------------------------------------------------------------

def chain_over_zero(value: int) -> str:
    """The `a`/`b` word that builds `value` from `0`, as a term."""
    term = "0"
    for bit in format(value, "b").lstrip("0") or "":
        term = f"{'b' if bit == '1' else 'a'}({term})"
    return term


def evaluate_chain(term: str) -> int:
    value = 0
    for symbol in reversed([piece for piece in term.replace(")", "")
                            .split("(") if piece in ("a", "b")]):
        value = a(value) if symbol == "a" else b(value)
    return value


def verify_constants_are_chains() -> None:
    for value in range(1 << WIDTH):
        assert evaluate_chain(chain_over_zero(value)) == value, value
    print(f"  every constant in [0, {1 << WIDTH}) is an a/b chain over 0")
    for value in (0, 1, 2, 3, 44, MASK):
        print(f"    {value:<4} {bits(value)}   {chain_over_zero(value)}")
    print()
    print("  b^k(0) = 2^k - 1:")
    value, run = 0, []
    for _ in range(5):
        run.append(f"{value}")
        value = b(value)
    print(f"    {' -> '.join(run)}   (b of each)")


def verify_the_smaller_basis() -> None:
    """`{1, a, ^}`: `b` is derived, and `0` comes free."""
    for value in range(1 << WIDTH):
        assert b(value) == a(value) ^ 1, value
    print("  b(t) = a(t) ^ 1                for every t -- b is derived")
    assert (1 ^ 1) == 0
    print("  0 = 1 ^ 1                      -- 0 is derived")
    for value in range(1 << WIDTH):
        total, power = 0, 1
        for index in range(WIDTH):
            if value >> index & 1:
                total ^= power
            power = a(power)
        assert total == value, value
    print(f"  every constant is a ^-sum of a^k(1)")
    print("  so the smaller basis is {1, a, ^}; {0, a, b} also works but")
    print("  needs b primitive, and 0 = 1 ^ 1 makes the first strictly")
    print("  smaller.")


def verify_omega_comes_from_N() -> None:
    assert N(b(0)) == MASK
    chain = 0
    for _ in range(WIDTH):
        chain = b(chain)
    assert chain == MASK
    print(f"  Ω = N(b(0)) = {bits(N(b(0)))}      width-independent")
    print(f"  Ω = b^{WIDTH}(0) = {bits(chain)}    needs the width")
    print("  N is what makes the universe without knowing how wide it is.")


def verify_measures_are_telescopings() -> None:
    for value in range(1 << (WIDTH - 1)):
        assert (bang(value) ^ a(bang(value))) == value, value
        assert (up(value) ^ a(up(value))) == (value & -value), value
        assert (trail(value) ^ b(trail(value))) == \
            ((MASK ^ value) & -(MASK ^ value)), value
    print("  !(t) ^ a(!t)  =  t                     the argument itself")
    print("  U(t) ^ a(U t) =  lowest set bit of t")
    print("  T(t) ^ b(T t) =  lowest zero bit of t")
    print()
    # complement is available once Ω is: ¬t = t ^ N(b 0)
    for value in range(1 << (WIDTH - 1)):
        complement = value ^ MASK
        assert (trail(complement) ^ b(trail(complement))) == \
            (value & -value), value
    print()
    print("  and the two are each other under complement (0041's `T` is")
    print("  `U` dualised, again):")
    print("    lowset(t) = lowzero(t ^ Ω),  with  Ω = N(b(0))")
    print()
    print("  So no measure is a primitive OPERATION. But each must stay a")
    print("  SYMBOL in the rewrite system: telescope's whole job is to")
    print("  package that pattern into an atom no rule can reopen. Expand")
    print("  `lowset` back to `U(t) ^ a(U t)` and telescope becomes the")
    print("  identity rewrite, and the series count stops falling.")
    print("  Algebra signature and rewrite signature are not the same list.")


# ---------------------------------------------------------------------
# 2. every operator on a bitstring
# ---------------------------------------------------------------------

X = 0b00101100      # 44
Y = 0b00011010      # 26
Z = 0b00010111      # 23, chosen for its trailing ones


def show_elementary() -> None:
    print(f"  x = {bits(X)}        y = {bits(Y)}")
    print()
    rows = [
        ("a(x)", "x << 1, fills a 0", a(X)),
        ("b(x)", "x << 1, fills a 1   [= a(x) ^ 1]", b(X)),
        ("x ^ y", "symmetric difference", X ^ Y),
        ("x & y", "intersection", X & Y),
        ("x | y", "= x ^ y ^ xy, derived", X ^ Y ^ (X & Y)),
    ]
    for name, note, value in rows:
        print(f"    {name:<8} {bits(value)}   {note}")


def show_compound() -> None:
    for label, value, join, step, symbol, result in [
            ("!", X, "^", a, "^", bang(X)),
            ("U", X, "|", a, "|", up(X)),
            ("T", Z, "&", b, "&", trail(Z))]:
        total, terms = series(join, step, value)
        assert total == result
        shift = "a" if step is a else "b"
        print(f"    {label}({bits(value)}) = {bits(result)}")
        print(f"      expanded:  x {symbol} {shift}(x) {symbol} "
              f"{shift}²(x) {symbol} …")
        for index, term in enumerate(terms):
            arrow = "  " if index else "  "
            print(f"      {arrow}{'' if index else ' '}"
                  f"{symbol if index else ' '} {bits(term)}"
                  f"{'   (x)' if index == 0 else ''}")
        print(f"        = {bits(result)}")
        print()
    print(f"    N({bits(X)}) = {bits(N(X))}   N({bits(0)}) = {bits(N(0))}")
    print("      expanded:  NOTHING. `N` is the one operator with no")
    print("      expansion in the schema -- 0045 §4: every a/b operator")
    print("      is LSB-causal and N is not, so no series over a or b")
    print("      builds it. It is primitive, and it is the language's")
    print("      only downward channel.")


def show_measures() -> None:
    print(f"  on x = {bits(X)}")
    print(f"    !(x) ^ a(!x)  = {bits(bang(X) ^ a(bang(X)))}   = x")
    print(f"    U(x) ^ a(U x) = {bits(up(X) ^ a(up(X)))}   lowest set bit")
    print(f"  on z = {bits(Z)}")
    print(f"    T(z) ^ b(T z) = {bits(trail(Z) ^ b(trail(Z)))}"
          f"   lowest zero bit")


def run_verification_suite() -> None:
    sections = [
        ("Constants are `a`/`b` chains over 0", verify_constants_are_chains),
        ("The smaller basis: {1, a, ^}", verify_the_smaller_basis),
        ("Ω comes from N", verify_omega_comes_from_N),
        ("The measures are telescopings, not symbols",
         verify_measures_are_telescopings),
        ("The elementary operators on a bitstring", show_elementary),
        ("The compound operators, with expansions", show_compound),
        ("The measures on a bitstring", show_measures),
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
