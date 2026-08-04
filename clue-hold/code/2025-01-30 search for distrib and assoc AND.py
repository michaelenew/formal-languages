
import itertools
import typing
from termcolor import colored


# The goal of this script is to search for an AND extension that is commutative, distributive, and associative with
# the following XOR extension. Read more about why this XOR extension in [[2025-01-20 (2) Assoc of AND XOR]]

def XOR(a, b) -> int:
    if a < 2 and b < 2:
        return (a + b) % 2
    return max(a, b)


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


def find_dim_3_extensions():
    DIM = 3

    for and_spec in itertools.product(range(DIM), repeat = DIM):
        table = [
            [0, 0, and_spec[0]],
            [0, 1, and_spec[1]],
            and_spec,
        ]
        and_extension = lambda a, b : table[a][b]

        if is_associative(and_extension, DIM) and is_distributive(XOR, and_extension, DIM):
            print_table('', table)
            print()

    '''
    Only one that pops up is
    0 0 2
    0 1 2
    2 2 2
    '''


def find_dim_4_extensions():
    DIM = 4

    for and_spec in itertools.product(range(DIM), repeat = DIM):
        table = [
            [0, 0, 2, and_spec[0]],
            [0, 1, 2, and_spec[1]],
            [2, 2, 2, and_spec[2]],
            and_spec,
        ]
        and_extension = lambda a, b : table[a][b]

        if is_associative(and_extension, DIM) and is_distributive(XOR, and_extension, DIM):
            print_table('', table)
            print()

    '''
    Three pop up
    0 0 2 2
    0 1 2 2
    2 2 2 2
    2 2 2 2

    0 0 2 2
    0 1 2 2
    2 2 2 2
    2 2 2 3

    0 0 2 3
    0 1 2 3
    2 2 2 3
    3 3 3 3
    '''


def find_dim_5_extensions():
    DIM = 5

    print('For all 2s')
    for and_spec in itertools.product(range(DIM), repeat = DIM):
        table = [
            [0, 0, 2, 2, and_spec[0]],
            [0, 1, 2, 2, and_spec[1]],
            [2, 2, 2, 2, and_spec[2]],
            [2, 2, 2, 2, and_spec[3]],
            and_spec,
        ]
        and_extension = lambda a, b : table[a][b]

        if is_associative(and_extension, DIM) and is_distributive(XOR, and_extension, DIM):
            print_table('', table)
            print()

    print('For all 2s and one 3')
    for and_spec in itertools.product(range(DIM), repeat = DIM):
        table = [
            [0, 0, 2, 2, and_spec[0]],
            [0, 1, 2, 2, and_spec[1]],
            [2, 2, 2, 2, and_spec[2]],
            [2, 2, 2, 3, and_spec[3]],
            and_spec,
        ]
        and_extension = lambda a, b : table[a][b]

        if is_associative(and_extension, DIM) and is_distributive(XOR, and_extension, DIM):
            print_table('', table)
            print()

    print('For all 3s')
    for and_spec in itertools.product(range(DIM), repeat = DIM):
        table = [
            [0, 0, 2, 3, and_spec[0]],
            [0, 1, 2, 3, and_spec[1]],
            [2, 2, 2, 3, and_spec[2]],
            [3, 3, 3, 3, and_spec[3]],
            and_spec,
        ]
        and_extension = lambda a, b : table[a][b]

        if is_associative(and_extension, DIM) and is_distributive(XOR, and_extension, DIM):
            print_table('', table)
            print()


def every_possible_extension(table: list[list[int]]) -> typing.Iterable[list[list[int]]]:
    dim = len(table) + 1
    for and_spec in itertools.product(range(dim), repeat = dim):
        # if dim - 1 not in and_spec:
        #     continue
        a = [
            list(existing) + [and_spec[i]]
            for i, existing in enumerate(table)
        ] + [and_spec]
        # print_table('', a)
        # print()
        yield a


def enumerate_pairs():
    AND = [
        [0, 0],
        [0, 1],
    ]
    XOR = [
        [0, 1],
        [1, 0],
    ]

    all_pairs = [[AND, XOR]]
    new_pairs = []
    dim = 2

    while True:
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
                        dim-1 in table[-1]
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
