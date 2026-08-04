from __future__ import annotations
from dataclasses import dataclass
import itertools
from typing import Callable, Iterable


'''
The purpose of this script is to check which (anti)commutativities can or cannot be obtained by composing
functions.

This relates to the open question of whether there exists a clear test for monotonicity. Commutativities
that cannot be obtained may provide some clue as to why monotonics do not have an obvious test.

This also relates to the question (almost just rephrasing the above) of the degree of functional completeness
proven by a set of functions having no (anti)commutativities

This script is incomplete. It is fairly trivial to see that 
'''

def test(t: Test, f: Test, vals):
    for x_raw in itertools.product(*([vals] * (t.dim * f.dim))):
        iter_x = iter(x_raw)
        x1 = tuple(tuple(itertools.islice(iter_x, t.dim)) for _ in range(f.dim))
        z1 = f(tuple(t(x) for x in x1))
        x2 = zip(*x1)
        z2 = t(tuple(f(x) for x in x2))
        if z1 != z2: return False
    return True

@dataclass
class Test:
    name: str
    test: Callable
    dim: int

    def __call__(self, tup):
        return self.test(tup)




######## dim 0
false = Test(
    name = 'false',
    test = lambda x : 0,
    dim = 0,
)

true = Test(
    name = 'true',
    test = lambda x : 1,
    dim = 0,
)



####### dim 1
ident = Test(
    name = 'ident',
    test = lambda x : {
        (0,): 0,
        (1,): 1,
    }[x],
    dim = 1,
)

not_ = Test(
    name = 'not',
    test = lambda x : {
        (0,): 1,
        (1,): 0,
    }[x],
    dim = 1,
)


####### dim 2
and_ = Test(
    name='and',
    test=lambda x: {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1}[x],
    dim=2,
)

not_implication = Test(
    name='not_implication',
    test=lambda x: {(0, 0): 0, (0, 1): 0, (1, 0): 1, (1, 1): 0}[x],
    dim=2,
)

not_converse = Test(
    name='not_converse',
    test=lambda x: {(0, 0): 0, (0, 1): 1, (1, 0): 0, (1, 1): 0}[x],
    dim=2,
)

xor = Test(
    name='xor',
    test=lambda x: {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0}[x],
    dim=2,
)

or_ = Test(
    name='or',
    test=lambda x: {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 1}[x],
    dim=2,
)

nor = Test(
    name='nor',
    test=lambda x: {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 0}[x],
    dim=2,
)

xnor = Test(
    name='xnor',
    test=lambda x: {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 1}[x],
    dim=2,
)

converse = Test(
    name='converse',
    test=lambda x: {(0, 0): 1, (0, 1): 0, (1, 0): 1, (1, 1): 1}[x],
    dim=2,
)

implication = Test(
    name='implication',
    test=lambda x: {(0, 0): 1, (0, 1): 1, (1, 0): 0, (1, 1): 1}[x],
    dim=2,
)

nand = Test(
    name='nand',
    test=lambda x: {(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 0}[x],
    dim=2,
)



def compose(*tests: Test, dim: int, depth: int = 10) -> Iterable[Test]:
    '''
    This function composes the provided tuple of Test objects to the specified depth and returns
    a Test for each composition
    '''


    for test in tests:
        test()

    # list of all compositions
    funcs: list[Test] = []

    for func in funcs:
        # for this func, build every possilbe set of inputs
        for i in range(func.dim):
            # what input am I giving this index?

        


