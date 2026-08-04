
# Purpose

This file just checks for associativity of AND and XOR.

Check [[2025-01-20 (2) associativity of XOR AND.py]] for script.

The gist is the distributive XOR definition isn't associative. Then we go on a search for associative xor definitions

The most promising XOR definition (works to dim 100 at least) is


0 1 2 3
1 0 2 3
2 2 2 3
3 3 3 3


aka


def XOR(a, b) -> int:
    if a < 2 and b < 2:
        return (a + b) % 2
    return max(a, b)


# Next steps

Next steps are to perform another search for commutative, distributive, and associative AND extensions with this XOR definition.
