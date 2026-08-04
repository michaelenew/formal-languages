import itertools
import typing
from termcolor import colored



'''
The purpose of this document is to search for associative, distributive, commutative, and
(in the presence of all nilary functions) FC
AND and XOR extensions.

The key property of XOR that we are interested in examining are a ^ a := 0. XOR is the only
binary commutative function that has this property, which is why we search here for XOR
extensions and no other pairing with AND.

The key property of AND we want is that it is distributive over XOR. AND is the only binary
commutative function that distributes over AND in 2 truth values, which is why we search here
for AND extenions only.

The key properties of XOR and AND are that they are that they maintain all their properties
in every dimension. This means that the result value N cannot appear before the Nth row/col
of each function.

Observations that guide this search:
- To be FC, it is necessary that at least one of the extensions at dimension N includes the
  value N (e.g. the 3rd row [index 2] must contain the value 2)
- There must always be a way to increment to the max output truth value
    - To be FC over N->N dimensions in N dimensions, at least one of the pair must contain the truth
      value N in a row/col that is _not_ (N, N). E.g. N=3 appears at (3, 2).
    - To be FC over N->N-1 (meaning N inputs N-1 outputs) dimensions in N dimensions, at least one of
      the pair must NOT have N in the (N, N) slot
    - To be FC over N-1->N-1 dimensions in N dimensions, every
'''


def print_table(prefix: str, table: list[list[int]]):
    for row in table:
        print(
            prefix
            + ' '.join(
                colored(elem, {0: 'green', 1: 'yellow', 2: 'red', 3: 'magenta'}.get(elem, 'white'))
                for elem in row
            )
        )

def is_associative(f, dim: int) -> bool:
    left_parentheses = lambda a, b, c : f(f(a, b), c)
    right_parentheses = lambda a, b, c : f(a, f(b, c))

    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                if left_parentheses(a, b, c) != right_parentheses(a, b, c):
                    return False
    return True


def is_distributive(addition_like, multiplication_like, dim: int) -> bool:
    # Undistributed looks like (a + b) * c
    undistributed = lambda a, b, c : multiplication_like(addition_like(a, b), c)

    # Distributed looks like a * c + b * c
    distributed = lambda a, b, c : addition_like(multiplication_like(a, c), multiplication_like(b, c))

    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                if undistributed(a, b, c) != distributed(a, b, c):
                    return False
    return True



def every_possible_extension(table: list[list[int]]) -> typing.Iterable[list[list[int]]]:
    dim = len(table) + 1
    for extension_spec in itertools.product(range(dim), repeat = dim):
        # if dim - 1 not in extension_spec:
        #     continue
        a = [
            list(existing) + [extension_spec[i]]
            for i, existing in enumerate(table)
        ] + [extension_spec]
        # print_table('', a)
        # print()
        yield a


def enumerate_pairs():
    XOR = [
        [0, 1],
        [1, 0],
    ]
    AND = [
        [0, 0],
        [0, 1],
    ]

    all_pairs = [[AND, XOR]]
    new_pairs = []
    dim = 2

    while True:
        if len(all_pairs) == 0:
            print('Terminated at dim', dim)
            break
        dim += 1
        for and_extension, xor_extension in all_pairs:
            for associative_xor in filter(
                lambda table : (
                    table[dim-1][dim-1] == 0
                    and
                    is_associative(lambda a, b : table[a][b], dim)
                ),
                every_possible_extension(xor_extension),
            ):
                for assoc_distrib_and in filter(
                    lambda table : (
                        dim-1 in table[-1][:-1]
                        and
                        is_associative(lambda a, b : table[a][b], dim)
                        and
                        is_distributive(
                            lambda a, b : associative_xor[a][b],
                            lambda a, b : table[a][b],
                            dim,
                        )
                    ),
                    every_possible_extension(and_extension),
                ):
                    # Search terminates immediately, there are no extensions satisfying this requirement
                    # If neither extension can produce the new value with at least 1 input less than the value
                    # then it's not possible to map e.g. (N-1, N-1) to N w/o making the whole function constant
                    # if dim-1 not in associative_xor[-1][:-1] and dim-1 not in assoc_distrib_and[-1][:-1]:
                    #     continue
                    print_table('AND ', assoc_distrib_and)
                    print()
                    print_table('XOR ', associative_xor)
                    print()
                    print()
                    print()
                    new_pairs.append([assoc_distrib_and, associative_xor])

        all_pairs = new_pairs
        new_pairs = []


enumerate_pairs()
