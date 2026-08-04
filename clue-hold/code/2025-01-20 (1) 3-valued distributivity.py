
def test_3():
    print('Testing for dim=3')

    XOR = lambda a, b : (
        (0, 1, 2),
        (1, 0, 1),
        (2, 1, 0),
    )[a][b]
    AND = lambda a, b : (
        (0, 0, 0),
        (0, 1, 0),
        (0, 0, 0),
    )[a][b]

    undistributed = lambda a, b, c : AND(XOR(a, b), c)
    distributed = lambda a, b, c : XOR(AND(a, c), AND(b, c))

    for a in range(3):
        for b in range(3):
            for c in range(3):
                if distributed(a, b, c) != undistributed(a, b, c):
                    print(f'Mismatch at {a} {b} {c} = {distributed(a, b, c)} / {undistributed(a, b, c)}')



def test_4():
    print('Testing for dim=4')

    XOR = lambda a, b : (
    (0, 1, 2, 3),
    (1, 0, 1, 2),
    (2, 1, 0, 1),
    (3, 2, 1, 0),
    )[a][b]
    AND = lambda a, b : (
    (0, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 0, 0),
    (0, 0, 0, 0),
    )[a][b]

    undistributed = lambda a, b, c : AND(XOR(a, b), c)
    distributed = lambda a, b, c : XOR(AND(a, c), AND(b, c))

    for a in range(4):
        for b in range(4):
            for c in range(4):
                if distributed(a, b, c) != undistributed(a, b, c):
                    print(f'Mismatch at {a} {b} {c} = {distributed(a, b, c)} / {undistributed(a, b, c)}')




def test_every_4():
    print('Testing every possibility for dim=4')

    def test(distributed, undistributed) -> bool:
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    if distributed(a, b, c) != undistributed(a, b, c):
                        return False
        return True

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
        

    i = 0
    for num_0 in range(4):
        for num_1 in range(4):
            for num_2 in range(4):
                for num_3 in range(4):
                    for num_4 in range(4):
                        for num_5 in range(4):
                            for num_6 in range(4):
                                for num_7 in range(4):
                                    if i % 10000 == 0:
                                        print(f'On iteration {i}')
                                    i += 1
                                    xor_table = (
                                        (0, 1, 2, num_0),
                                        (1, 0, 1, num_1),
                                        (2, 1, 0, num_2),
                                        (num_0, num_1, num_2, num_3),
                                    )
                                    XOR = lambda a, b : xor_table[a][b]
                                    and_table = (
                                        (0, 0, 0, num_4),
                                        (0, 1, 0, num_5),
                                        (0, 0, 0, num_6),
                                        (num_4, num_5, num_6, num_7),
                                    )
                                    AND = lambda a, b : and_table[a][b]

                                    undistributed = lambda a, b, c : AND(XOR(a, b), c)
                                    distributed = lambda a, b, c : XOR(AND(a, c), AND(b, c))

                                    if test(distributed, undistributed):
                                        print('Successful test for')
                                        print('  xor')
                                        print_table('    ', xor_table)
                                        print('  and')
                                        print_table('    ', and_table)




def test_6():
    print('Testing generalized dim=6')

    XOR = lambda a, b : (
    (0, 1, 2, 3, 4, 5),
    (1, 0, 1, 2, 3, 4),
    (2, 1, 0, 1, 2, 3),
    (3, 2, 1, 0, 1, 2),
    (4, 3, 2, 1, 0, 1),
    (5, 4, 3, 2, 1, 0)
    )[a][b]
    AND = lambda a, b : (
    (0, 0, 0, 0, 0, 0),
    (0, 1, 0, 1, 0, 1),
    (0, 0, 0, 0, 0, 0),
    (0, 1, 0, 1, 0, 1),
    (0, 0, 0, 0, 0, 0),
    (0, 1, 0, 1, 0, 1),
    )[a][b]

    undistributed = lambda a, b, c : AND(XOR(a, b), c)
    distributed = lambda a, b, c : XOR(AND(a, c), AND(b, c))

    for a in range(6):
        for b in range(6):
            for c in range(6):
                if distributed(a, b, c) != undistributed(a, b, c):
                    print(f'Mismatch at {a} {b} {c} = {distributed(a, b, c)} / {undistributed(a, b, c)}')


if __name__ == '__main__':
    # test_3()
    # test_4()
    # test_every_4()
    test_6()
