
from termcolor import colored
def print_table(prefix: str, table: list[list[int]]):
    for row in table:
        print(
            prefix
            + ' '.join(
                colored(elem, {0: 'green', 1: 'yellow', 2: 'red', 3: 'magenta'}[elem])
                for elem in row
            )
        )
        
def test_xor_and():
    XOR = lambda a, b : abs(a - b)
    AND = lambda a, b : (
        (0, 0, 0, 0, 0, 0),
        (0, 1, 0, 1, 0, 1),
        (0, 0, 0, 0, 0, 0),
        (0, 1, 0, 1, 0, 1),
        (0, 0, 0, 0, 0, 0),
        (0, 1, 0, 1, 0, 1),
    )[a][b]


    for a in range(6):
        for b in range(6):
            for c in range(6):
                if AND(AND(a, b), c) != AND(a, AND(b, c)):
                    print(f'and failed on {a}, {b}, {c}')
                if XOR(XOR(a, b), c) != XOR(a, XOR(b, c)):
                    print(f'xor failed on {a}, {b}, {c} with', XOR(XOR(a, b), c), XOR(a, XOR(b, c)))


def try_every_xor_3():
    DIM = 3
    def does_associate(fun):
        for a in range(DIM):
            for b in range(DIM):
                for c in range(DIM):
                    if fun(fun(a, b), c) != fun(a, fun(b, c)):
                        return False
        return True

    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                xor_table = (
                    (0, 1, a),
                    (1, 0, b),
                    (a, b, c),
                )
                XOR = lambda a, b : xor_table[a][b]
                if does_associate(XOR):
                    print('Found one')
                    print_table('', xor_table)



def try_each_xor_4():
    '''
    There are only 4 functions that distribute in 3 dimensions:

    Found one
    0 1 0
    1 0 1
    0 1 0
    Found one
    0 1 0
    1 0 1
    0 1 2
    Found one
    0 1 1
    1 0 0
    1 0 0
    Found one
    0 1 2
    1 0 2
    2 2 2
    '''


    DIM = 4
    def does_associate(fun):
        for a in range(DIM):
            for b in range(DIM):
                for c in range(DIM):
                    if fun(fun(a, b), c) != fun(a, fun(b, c)):
                        return False
        return True

    print('\nbreak')
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    xor_table = (
                        (0, 1, 0, a),
                        (1, 0, 1, b),
                        (0, 1, 0, c),
                        (a, b, c, d),
                    )
                    XOR = lambda a, b : xor_table[a][b]
                    if does_associate(XOR):
                        print('Found one')
                        print_table('', xor_table)

    print('\nbreak')
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    xor_table = (
                        (0, 1, 0, a),
                        (1, 0, 1, b),
                        (0, 1, 2, c),
                        (a, b, c, d),
                    )
                    XOR = lambda a, b : xor_table[a][b]
                    if does_associate(XOR):
                        print('Found one')
                        print_table('', xor_table)

    print('\nbreak')
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    xor_table = (
                        (0, 1, 1, a),
                        (1, 0, 0, b),
                        (1, 0, 0, c),
                        (a, b, c, d),
                    )
                    XOR = lambda a, b : xor_table[a][b]
                    if does_associate(XOR):
                        print('Found one')
                        print_table('', xor_table)

    print('\nbreak')
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    xor_table = (
                        (0, 1, 2, a),
                        (1, 0, 2, b),
                        (2, 2, 2, c),
                        (a, b, c, d),
                    )
                    XOR = lambda a, b : xor_table[a][b]
                    if does_associate(XOR):
                        print('Found one')
                        print_table('', xor_table)



def test_promising_xor():
    '''
    One of the 4s that works is
    0 1 2 3
    1 0 2 3
    2 2 2 3
    3 3 3 3

    This looks like the cleanest pattern to try to replicate. Checking its associativity in 5+ dims
    '''


    DIM = 100
    def does_associate(fun):
        for a in range(DIM):
            for b in range(DIM):
                for c in range(DIM):
                    if fun(fun(a, b), c) != fun(a, fun(b, c)):
                        return False
        return True

    def XOR(a, b) -> int:
        if a < 2 and b < 2:
            return (a + b) % 2
        return max(a, b)

    print(does_associate(XOR))



if __name__ == '__main__':
    # test_xor_and()
    # try_every_xor_3()
    # try_each_xor_4()
    test_promising_xor()
