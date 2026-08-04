from __future__ import annotations

import itertools
from random import Random



class Fun:
    def __init__(self,
            inputs: int,
            outputs: int,
            fun: callable,
            debug: bool = False,):

        self.inputs = inputs
        self.outputs = outputs
        self.fun = fun
        self.debug = debug

        if debug:
            print(f'Initializing Fun with {inputs} {outputs}')

    def __call__(self, *args) -> tuple:
        return self.fun(*args)

    def __add__(self, other: Fun) -> Fun:
        # if other.inputs < self.outputs:
        #     # ^add-dummy-indexes
        #     other = Fun(
        #         inputs = self.outputs - other.inputs,
        #         outputs = 0,
        #         fun = lambda *args : tuple(),
        #     ) + other
        def new_callable(*args) -> tuple:
            self_inputs_from_new = args[-self.inputs:] if self.inputs != 0 else []
            other_inputs_from_new = args[:-len(self_inputs_from_new)] if self.inputs != 0 else args

            self_res = self(*self_inputs_from_new)
            other_inputs_from_self = self_res[-other.inputs:] if other.inputs != 0 else []
            outputs_from_self = self_res[:-other.inputs] if other.inputs != 0 else self_res

            outputs_from_other = other(*other_inputs_from_new, *other_inputs_from_self)

            # The following do not work on this line
            # (*outputs_from_self, *(outputs_from_other[::-1]))
            # (*outputs_from_self[::-1], *(outputs_from_other))
            # (*(outputs_from_self[::-1]), *(outputs_from_other[::-1]))
            # (*(outputs_from_other[::-1]), *(outputs_from_self[::-1]))
            # (*(outputs_from_other), *(outputs_from_self[::-1]))
            # (*(outputs_from_other[::-1]), *(outputs_from_self))
            # (*(outputs_from_other), *(outputs_from_self))
            # outputs_from_other
            return (*outputs_from_self, *outputs_from_other)
        
        ret = Fun(
            inputs = self.inputs + other.inputs - min(self.outputs, other.inputs),
            outputs = other.outputs + self.outputs - min(self.outputs, other.inputs),
            fun = new_callable,
            debug = self.debug and other.debug,
        )

        if self.debug:
            into_inputs = min(self.outputs, other.inputs)
            print(f'  From addition overflow is {into_inputs} + {self.outputs - into_inputs} = {self.outputs}')

        return ret
    
    def __mul__(self, other: Fun) -> Fun:
        def new_callable(*args) -> tuple:
            self_results = [
                self(*args[i * self.inputs : (i+1) * self.inputs])
                    for i in range(0, other.inputs)]
            other_results = [
                other(*other_inputs)
                    for other_inputs in zip(*self_results)]
            
            # IMPORTANT: the following are all associative on this line
            #     AND don't affect mutual associativity
            # tuple(e for result in other_results for e in result)
            # tuple(e for result in zip(*other_results) for e in result)
            # tuple(e for result in zip(*other_results[::-1]) for e in result[::-1])
            
            # BUT the following violates the identity unit tests and mismatches outputs...
            # tuple(e for result in other_results[::-1] for e in result[::-1])
            return tuple(e for result in other_results for e in result)

        return Fun(
            inputs = self.inputs * other.inputs,
            outputs = self.outputs * other.outputs,
            fun = new_callable,
            debug = self.debug and other.debug,
        )
    
    @classmethod
    def test_multiplication(cls):
        identity = Fun(1, 1, lambda x : (x,))
        not_ = Fun(1, 1, lambda x : ((x + 1) % 2,))
        xor = Fun(2, 1, lambda x, y : ((x + y) % 2,))
        and_or = Fun(2, 2, lambda x, y : (min(x, y), max(x, y)))

        assert identity(1) == (1,)
        assert not_(1) == (0,)
        assert xor(1, 1) == (0,)
        assert and_or(4, 1) == (1, 4)

        assert (identity * not_)(1) == not_(1)
        assert (xor * identity)(0, 1) == xor(0, 1)
        assert (identity * and_or)(3, 9) == and_or(3, 9)
        assert (and_or * identity)(5, 7) == and_or(5, 7)

        and_or_2 = and_or * and_or
        assert and_or_2(1,2,3,4) == (1, 3, 2, 4)

    @classmethod
    def test_addition(cls):
        # return # short circuit to rapid iterate on __add__
        f1 = Fun(0, 1, lambda : (2,))
        f2 = Fun(1, 1, lambda x : (x,))
        f3 = Fun(2, 1, lambda x, y : (x + y,))
        f4 = Fun(1, 2, lambda x : (x, x))
        f5 = Fun(2, 2, lambda x, y : (x, y))

        assert f1() == (2,)
        assert f2(1) == (1,)
        assert f3(2, 2) == (4,)
        assert f4(3) == (3, 3)

        f11 = f1 + f1
        assert f11.inputs == 0
        assert f11.outputs == 2
        assert f11() == (2, 2)

        f12 = f1 + f2
        assert f12.inputs == 0
        assert f12.outputs == 1
        assert f12() == (2,)

        f13 = f1 + f3
        assert f13.inputs == 1
        assert f13.outputs == 1
        assert f13(6) == (8,)

        f14 = f1 + f4
        assert f14.inputs == 0
        assert f14.outputs == 2
        assert f14() == (2, 2)

        f21 = f2 + f1
        assert f21.inputs == 1
        assert f21.outputs == 2
        assert f21(3) == (3, 2)

        f33 = f3 + f3
        assert f33.inputs == 3
        assert f33.outputs == 1
        assert f33(1, 2, 3) == (6,)

        f34 = f3 + f4
        assert f34.inputs == 2
        assert f34.outputs == 2
        assert f34(4,5) == (9, 9)

        f35 = f3 + f5
        assert f35.inputs == 3
        assert f35.outputs == 2
        assert f35(3,4,5) == (3, 9)
    


class RandFun(Fun):
    def __init__(self,
            inputs: int,
            outputs: int,
            seed: int,
            dim: int,
            debug: bool = False,):

        def rand_result(*args):
            r = Random(seed + hash(args))
            return tuple(r.randint(0, dim) for _ in range(outputs))

        Fun.__init__(self, inputs, outputs, rand_result, debug)

    @classmethod
    def test(cls):
        # basic cases - two identical nilary functions produce the same result, non-identical don't produce identical results
        assert RandFun(0, 10, 0, 100)() == RandFun(0, 10, 0, 100)()
        assert RandFun(0, 10, 1, 100)() == RandFun(0, 10, 1, 100)()
        assert RandFun(0, 10, 0, 100)() != RandFun(0, 10, 1, 100)()

        # testing that multiple calls on the same RandFun produce the same result
        rf = RandFun(0, 10, 0, 100)
        rf()
        assert rf() == RandFun(0, 10, 0, 100)()

        # testing arity > 0 works
        assert RandFun(4, 10, 2, 100)(1,2,3,4) == RandFun(4, 10, 2, 100)(1,2,3,4)



seeds = itertools.count()
dim = 4

def test_equality(res1: Fun, res2: Fun):
    if res1.inputs != res2.inputs or res1.outputs != res2.outputs:
        print('in/out size misaligned')
        return False

    for i in range(10):
        check = RandFun(0, max(res1.inputs, res2.inputs), i, dim)
        first = (check + res1)()
        second = (check + res2)()
        if first != second:
            print(f'found mismatched outputs {first} {second}')
        else:
            print(f'pass {first} {second}')


def additive_associativity():
    def test_addition_associativity(f1: Fun, f2: Fun, f3: Fun):
        res1 = (f1 + f2) + f3
        res2 = f1 + (f2 + f3)
        return test_equality(res1, res2)

    # All pass
    print('\n\nADDITIVE ASSOCIATIVITY')
    test_addition_associativity(
        RandFun(2, 5, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(5, 2, next(seeds), dim, True),
    )

    test_addition_associativity(
        RandFun(3, 1, next(seeds), dim, True),
        RandFun(4, 4, next(seeds), dim, True),
        RandFun(2, 2, next(seeds), dim, True),
    )

    test_addition_associativity(
        RandFun(2, 3, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(4, 1, next(seeds), dim, True),
    )

def multiplicative_associativity():
    def test_multiplication_associativity(f1: Fun, f2: Fun, f3: Fun):
        res1 = (f1 * f2) * f3
        res2 = f1 * (f2 * f3)
        return test_equality(res1, res2)

    # All pass
    print('\n\nMULTIPLICATIVE ASSOCIATIVITY')
    test_multiplication_associativity(
        RandFun(2, 5, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(5, 2, next(seeds), dim, True),
    )

    test_multiplication_associativity(
        RandFun(3, 1, next(seeds), dim, True),
        RandFun(4, 4, next(seeds), dim, True),
        RandFun(2, 2, next(seeds), dim, True),
    )

    test_multiplication_associativity(
        RandFun(2, 3, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(4, 1, next(seeds), dim, True),
    )

def mutual_associativity():
    def test_mutual_associativity(f1: Fun, f2: Fun, f3: Fun):
        res1 = (f1 + f2) * f3
        res2 = f1 + (f2 * f3)
        return test_equality(res1, res2)

    # All fail due to size mismatches
    print('\n\nMUTUAL ASSOCIATIVITY')
    test_mutual_associativity(
        RandFun(2, 5, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(5, 2, next(seeds), dim, True),
    )

    test_mutual_associativity(
        RandFun(3, 1, next(seeds), dim, True),
        RandFun(4, 4, next(seeds), dim, True),
        RandFun(2, 2, next(seeds), dim, True),
    )

    test_mutual_associativity(
        RandFun(2, 3, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(4, 1, next(seeds), dim, True),
    )

def mutual_associativity_2():
    def test_mutual_associativity_2(f1: Fun, f2: Fun, f3: Fun):
        res1 = (f1 * f2) + f3
        res2 = f1 * (f2 + f3)
        return test_equality(res1, res2)

    # Some pass...?
    # ^mutual-associativity-hook
    print('\n\nMUTUAL ASSOCIATIVITY 2')

    # Fails due to size mismatch
    test_mutual_associativity_2(
        RandFun(2, 5, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(5, 2, next(seeds), dim, True),
    )

    # PASSES?!
    # Notice that the overflow sizes match here
    # ^overflows-do-match
    '''
    Initializing Fun with 2 1
    Initializing Fun with 4 3
    Initializing Fun with 1 5
    Initializing Fun with 8 3
        From addition overflow is 1 + 2 = 3
    Initializing Fun with 8 7
        From addition overflow is 1 + 2 = 3
    Initializing Fun with 4 7
    Initializing Fun with 8 7
    pass (3, 0, 2, 2, 3, 3, 2) (3, 0, 2, 2, 3, 3, 2)
    pass (0, 0, 2, 2, 3, 2, 3) (0, 0, 2, 2, 3, 2, 3)
    pass (4, 2, 2, 2, 3, 3, 2) (4, 2, 2, 2, 3, 3, 2)
    pass (4, 0, 0, 2, 0, 1, 2) (4, 0, 0, 2, 0, 1, 2)
    pass (0, 4, 0, 2, 0, 1, 2) (0, 4, 0, 2, 0, 1, 2)
    pass (3, 2, 2, 2, 3, 3, 2) (3, 2, 2, 2, 3, 3, 2)
    pass (2, 0, 3, 3, 0, 0, 2) (2, 0, 3, 3, 0, 0, 2)
    pass (4, 1, 3, 3, 0, 0, 2) (4, 1, 3, 3, 0, 0, 2)
    pass (3, 3, 0, 4, 0, 3, 0) (3, 3, 0, 4, 0, 3, 0)
    pass (1, 4, 2, 2, 3, 2, 3) (1, 4, 2, 2, 3, 2, 3)
    '''
    test_mutual_associativity_2(
        RandFun(3, 1, next(seeds), dim, True),
        RandFun(4, 4, next(seeds), dim, True),
        RandFun(2, 2, next(seeds), dim, True),
    )

    # Fails due to size mismatch
    test_mutual_associativity_2(
        RandFun(2, 3, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(4, 1, next(seeds), dim, True),
    )

    # Using a brute force approach to find some that don't fail the size check
    
    # [0, 2, 2, 3, 4, 2]
    # Fails due to output mismatch
    # Read this. It's weird. Numbers coming back the same each time is probably because whole function is nilary
    # Problem is that left and right look way
    # more similar than I'd expect (11 / 13 positions match). Can also try with different seeds, but index
    # 3 and 6 are always the only mismatched indices
    #
    # Consider that this is a bug in the code (or operator definition) related to handling nilary functions
    '''
    found mismatched outputs (2, 1, 2, 0, 3, 4, 4, 0, 2, 3, 0, 1) (2, 1, 3, 0, 3, 4, 4, 2, 2, 3, 0, 1)
    found mismatched outputs (2, 1, 2, 0, 3, 4, 4, 0, 2, 3, 0, 1) (2, 1, 3, 0, 3, 4, 4, 2, 2, 3, 0, 1)
    found mismatched outputs (2, 1, 2, 0, 3, 4, 4, 0, 2, 3, 0, 1) (2, 1, 3, 0, 3, 4, 4, 2, 2, 3, 0, 1)
    found mismatched outputs (2, 1, 2, 0, 3, 4, 4, 0, 2, 3, 0, 1) (2, 1, 3, 0, 3, 4, 4, 2, 2, 3, 0, 1)
    found mismatched outputs (2, 1, 2, 0, 3, 4, 4, 0, 2, 3, 0, 1) (2, 1, 3, 0, 3, 4, 4, 2, 2, 3, 0, 1)
    found mismatched outputs (2, 1, 2, 0, 3, 4, 4, 0, 2, 3, 0, 1) (2, 1, 3, 0, 3, 4, 4, 2, 2, 3, 0, 1)
    found mismatched outputs (2, 1, 2, 0, 3, 4, 4, 0, 2, 3, 0, 1) (2, 1, 3, 0, 3, 4, 4, 2, 2, 3, 0, 1)
    found mismatched outputs (2, 1, 2, 0, 3, 4, 4, 0, 2, 3, 0, 1) (2, 1, 3, 0, 3, 4, 4, 2, 2, 3, 0, 1)
    found mismatched outputs (2, 1, 2, 0, 3, 4, 4, 0, 2, 3, 0, 1) (2, 1, 3, 0, 3, 4, 4, 2, 2, 3, 0, 1)
    found mismatched outputs (2, 1, 2, 0, 3, 4, 4, 0, 2, 3, 0, 1) (2, 1, 3, 0, 3, 4, 4, 2, 2, 3, 0, 1)
    '''
    test_mutual_associativity_2(
        RandFun(0, 3, next(seeds), dim, True),
        RandFun(2, 4, next(seeds), dim, True),
        RandFun(2, 2, next(seeds), dim, True),
    )

    # [2, 4, 1, 1, 3, 5]
    # passes
    test_mutual_associativity_2(
        RandFun(2, 1, next(seeds), dim, True),
        RandFun(4, 3, next(seeds), dim, True),
        RandFun(1, 5, next(seeds), dim, True),
    )

    # [5, 1, 0, 0, 2, 0]
    # Passes because result is 0 0 function
    test_mutual_associativity_2(
        RandFun(5, 0, next(seeds), dim, True),
        RandFun(1, 2, next(seeds), dim, True),
        RandFun(0, 0, next(seeds), dim, True),
    )

    # [3, 3, 1, 2, 4, 1]
    # Similar case to above, but this one is more interesting because it produces a non-nilary function
    # Notice that again most lines are closely matched and some happen to coincide
    # Also notice that the addition overflows don't match here
    # ^overflows-dont-match
    '''
    Initializing Fun with 3 2
    Initializing Fun with 3 4
    Initializing Fun with 1 1
    Initializing Fun with 9 8
        From addition overflow is 1 + 7 = 8
    Initializing Fun with 9 8
        From addition overflow is 1 + 3 = 4
    Initializing Fun with 3 4
    Initializing Fun with 9 8
    found mismatched outputs (2, 2, 0, 2, 1, 1, 1, 4) (2, 2, 0, 4, 1, 1, 1, 4)
    found mismatched outputs (4, 3, 0, 3, 4, 1, 2, 4) (4, 3, 0, 2, 4, 1, 2, 4)
    found mismatched outputs (0, 3, 0, 3, 4, 1, 0, 1) (0, 3, 0, 2, 4, 1, 0, 1)
    found mismatched outputs (3, 2, 1, 1, 0, 4, 1, 2) (3, 2, 1, 0, 0, 4, 1, 2)
    pass (3, 4, 1, 4, 1, 0, 2, 4) (3, 4, 1, 4, 1, 0, 2, 4)
    found mismatched outputs (4, 2, 0, 2, 3, 4, 3, 2) (4, 2, 0, 4, 3, 4, 3, 2)
    pass (3, 1, 3, 4, 0, 0, 0, 4) (3, 1, 3, 4, 0, 0, 0, 4)
    found mismatched outputs (4, 3, 3, 0, 0, 1, 0, 0) (4, 3, 3, 1, 0, 1, 0, 0)
    found mismatched outputs (4, 1, 0, 2, 0, 3, 2, 4) (4, 1, 0, 4, 0, 3, 2, 4)
    found mismatched outputs (3, 3, 3, 1, 0, 0, 4, 1) (3, 3, 3, 0, 0, 0, 4, 1)
    '''
    test_mutual_associativity_2(
        RandFun(3, 2, next(seeds), dim, True),
        RandFun(3, 4, next(seeds), dim, True),
        RandFun(1, 1, next(seeds), dim, True),
    )


def distributivity_mul_over_add():
    def test_right_distributivity_mul_over_add(f1: Fun, f2: Fun, f3: Fun):
        res1 = (f1 + f2) * f3
        res2 = (f1 * f3) + (f2 * f3)
        return test_equality(res1, res2)

    def test_left_distributivity_mul_over_add(f1: Fun, f2: Fun, f3: Fun):
        res1 = f3 * (f1 + f2)
        res2 = (f3 * f1) + (f3 * f2)
        return test_equality(res1, res2)

    # All fail. Size mismatches and output mismatches
    print('\n\nDISTRIBUTIVITY MUL OVER ADD')
    test_right_distributivity_mul_over_add(
        RandFun(2, 5, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(5, 2, next(seeds), dim, True),
    )

    test_right_distributivity_mul_over_add(
        RandFun(3, 1, next(seeds), dim, True),
        RandFun(4, 4, next(seeds), dim, True),
        RandFun(2, 2, next(seeds), dim, True),
    )

    test_right_distributivity_mul_over_add(
        RandFun(2, 3, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(4, 1, next(seeds), dim, True),
    )

    test_left_distributivity_mul_over_add(
        RandFun(2, 5, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(5, 2, next(seeds), dim, True),
    )

    test_left_distributivity_mul_over_add(
        RandFun(3, 1, next(seeds), dim, True),
        RandFun(4, 4, next(seeds), dim, True),
        RandFun(2, 2, next(seeds), dim, True),
    )

    test_left_distributivity_mul_over_add(
        RandFun(2, 3, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(4, 1, next(seeds), dim, True),
    )

def distributivity_add_over_mul():
    def test_right_distributivity_add_over_mul(f1: Fun, f2: Fun, f3: Fun):
        res1 = (f1 * f2) + f3
        res2 = (f1 + f3) * (f2 + f3)
        return test_equality(res1, res2)

    def test_left_distributivity_add_over_mul(f1: Fun, f2: Fun, f3: Fun):
        res1 = f3 + (f1 * f2)
        res2 = (f3 + f1) * (f3 + f2)
        return test_equality(res1, res2)

    # All fail. Size mismatches and output mismatches
    print('\n\nDISTRIBUTIVITY ADD OVER MUL')
    test_right_distributivity_add_over_mul(
        RandFun(2, 5, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(5, 2, next(seeds), dim, True),
    )

    test_right_distributivity_add_over_mul(
        RandFun(3, 1, next(seeds), dim, True),
        RandFun(4, 4, next(seeds), dim, True),
        RandFun(2, 2, next(seeds), dim, True),
    )

    test_right_distributivity_add_over_mul(
        RandFun(2, 3, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(4, 1, next(seeds), dim, True),
    )

    test_left_distributivity_add_over_mul(
        RandFun(2, 5, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(5, 2, next(seeds), dim, True),
    )

    test_left_distributivity_add_over_mul(
        RandFun(3, 1, next(seeds), dim, True),
        RandFun(4, 4, next(seeds), dim, True),
        RandFun(2, 2, next(seeds), dim, True),
    )

    test_left_distributivity_add_over_mul(
        RandFun(2, 3, next(seeds), dim, True),
        RandFun(1, 3, next(seeds), dim, True),
        RandFun(4, 1, next(seeds), dim, True),
    )

# Unit tests. Make sure we haven't broken the basic contracts
Fun.test_addition()
Fun.test_multiplication()
RandFun.test()

# other tests
additive_associativity()
multiplicative_associativity()
mutual_associativity()
mutual_associativity_2()
# distributivity_mul_over_add()
# distributivity_add_over_mul()

















