import itertools
import typing
from termcolor import colored



def print_table(prefix: str, table: list[list[int]]):
    for row in table:
        print(
            prefix
            + ' '.join(
                colored(elem, {0: 'green', 1: 'yellow', 2: 'red', 3: 'magenta'}.get(elem, 'white'))
                for elem in row
            )
        )


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
    for extension_spec in itertools.product(range(dim), repeat = 2 * dim - 1):
        a = [
            list(existing) + [extension_spec[i]]
            for i, existing in enumerate(table)
        ] + [list(extension_spec[dim-1:])]
        yield a



def check_false_preserving_AND_distributivity():
    false_preserving = every_possible_extension([[0]])
    non_false_preserving = every_possible_extension([[1]])
    AND = lambda a, b: [
        [0, 0],
        [0, 1],
    ][a][b]

    for fp in false_preserving:
        if is_distributive(lambda a, b: fp[a][b], AND, 2):
            print_table('FALSE PRESERVING ', fp)
        else:
            print_table('false preserving does not distribute ', fp)
        print()

    for nfp in non_false_preserving:
        if is_distributive(lambda a, b: nfp[a][b], AND, 2):
            print_table('NON FALSE PRESERVING ', nfp)
        else:
            print_table('non false preserving does not distribute ', nfp)
        print()


