from __future__ import annotations
from dataclasses import dataclass
import itertools
from typing import Callable

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

negate = Test(
    name = 'not',
    test = lambda x : int(not x[0]),
    dim = 1,
)

ident = Test(
    name = 'ident',
    test = lambda x : x[0],
    dim = 1,
)

xor = Test(
    name = 'xor',
    test = lambda x : int(x[0] != x[1]),
    dim = 2,
)

nxor = Test(
    name = 'nxor',
    test = lambda x : int(x[0] == x[1]),
    dim = 2,
)

nand = Test(
    name = 'nand',
    test = lambda x : int(not (x[0] and x[1])),
    dim = 2,
)

nor = Test(
    name = 'nor',
    test = lambda x : int(not (x[0] or x[1])),
    dim = 2,
)

or_ = Test(
    name = 'or',
    test = lambda x : int(x[0] or x[1]),
    dim = 2,
)

and_ = Test(
    name = 'and',
    test = lambda x : int(x[0] and x[1]),
    dim = 2,
)

implication = Test(
    name = 'implication',
    test = lambda x : int(not (x[0] and not x[1])),
    dim = 2,
)

linear3 = Test(
    name = 'linear3',
    test = lambda x : sum(x) % 2,
    dim = 3,
)

linear3p1 = Test(
    name = 'linear3p1',
    test = lambda x : (sum(x) + 1) % 2,
    dim = 3,
)

linear4 = Test(
    name = 'linear4',
    test = lambda x : sum(x) % 2,
    dim = 4,
)

linear4p1 = Test(
    name = 'linear4p1',
    test = lambda x : (sum(x) + 1) % 2,
    dim = 4,
)

linear5 = Test(
    name = 'linear5',
    test = lambda x : sum(x) % 2,
    dim = 5,
)

linear5p1 = Test(
    name = 'linear5p1',
    test = lambda x : (sum(x) + 1) % 2,
    dim = 5,
)

monotonic3_2 = Test(
    name = 'monotonic3_2',
    test = lambda x : int(sum(x) > 2),
    dim = 3,
)

monotonic4_2 = Test(
    name = 'monotonic4_2',
    test = lambda x : int(sum(x) > 2),
    dim = 4,
)

# rando = Test(
#     name = 'rando',
#     dim = 3,
#     test = lambda a : tuple([
#         (
#             (3,1,2,1),
#             (3,3,2,2),
#             (0,0,2,1),
#             (0,1,2,3),
#         ),
#         (
#             (2,2,1,3),
#             (0,1,2,0),
#             (0,1,1,0),
#             (2,2,2,3),
#         ),
#         (
#             (2,0,0,0),
#             (3,1,1,0),
#             (1,1,2,1),
#             (0,0,0,2),
#         ),
#         (
#             (3,2,1,0),
#             (3,1,2,0),
#             (1,1,0,1),
#             (0,2,0,2),
#         ),
#     ])[a[0]][a[1]][a[2]],
# )

tested = and_
for fun in (false, true, negate, ident, xor, nxor, nand, nor, or_, and_,
        implication, linear3, linear3p1, linear4, linear4p1, monotonic3_2,
        monotonic4_2, linear5, linear5p1):
    print(
        test(
            fun,
            tested,
            (0, 1),
        ),
        fun.name,
        tested.name,
    )

'''
Observations:
    nand and nor don't match anything except ident
    not, xor, or, and, nxor, false, true all match themselves
    rando and implication match true but not themselves

same result on reversal of order of params means f always matches f (generalization of commutativity)
    wait but nand does not match itself...
    neither does nor and they're both "commutative"

linear always matches itself?
'''
