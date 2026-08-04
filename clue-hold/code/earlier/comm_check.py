from __future__ import annotations
import numpy as np
import functools



def num_to_base(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]



def num_to_base_padded(n, b, l):
    inter = num_to_base(n, b)
    return [0] * (l - len(inter)) + inter



class Operator:
    def __init__(self, output_col: list[int] = None, dim = 2, *, ary = None, callable = None):
        # len(output_col) = dim ** ary
        if ary is None:
            ary = np.log(len(output_col)) / np.log(float(dim))
            assert abs(round(ary) - ary) < 1e-8, f'bad dimension {dim} or outputs {len(output_col)}. Best guess at ary is {ary}'
        self.ary = int(round(ary))
        def recurse_inputs(prior, dim, add_ary):
            if add_ary <= 0:
                return prior
            inter = tuple(
                (d, *p)
                    for d in reversed(range(dim))
                        for p in prior)
            return recurse_inputs(inter, dim, add_ary - 1)

        self.dim = dim
        self.inputs = recurse_inputs([tuple([])], dim, self.ary)
        if output_col is None:
            output_col = tuple(callable(i) for i in self.inputs)
        self.output_col = output_col
        self.mapping = {inp: out for inp, out in zip(self.inputs, output_col)}

    def __str__(self):
        return f'dim {self.dim}\n' + '\n'.join(f'{inp} | {self.mapping[inp]}' for inp in self.inputs[::-1])

    def short(self) -> str:
        return str(self.output_col)

    @functools.cache
    def __call__(self, inputs) -> int:
        if len(inputs) != self.ary:
            raise ValueError(f'Expected {self.ary} got {len(inputs)} inputs to operator')
        return self.mapping[inputs]

    def test(self, other_left: Operator, comparator = lambda x : x, other_right: Operator = None):
        if not other_right:
            other_right = other_left
        if self.dim != other_left.dim:
            raise ValueError(f'Got incompatible dimensions testing two operators {self.dim}, {other_left.dim}')
        num_elems = self.ary * other_left.ary
        num_cases = self.dim ** num_elems
        for i in range(num_cases):
            raw = num_to_base(i, self.dim)
            left_padded = ([0] * (num_elems - len(raw)) + raw)[:num_elems]
            arr = np.reshape(left_padded, (self.ary, other_left.ary))
            res_self_other = self(tuple(
                other_right(tuple(arr[j, :]))
                    for j in range(self.ary))) if other_right.ary > 0 else self(tuple(other_right(tuple([])) for _ in range(self.ary)))
            res_other_self = other_left(tuple(
                self(tuple(arr[:, j]))
                    for j in range(other_left.ary))) if self.ary > 0 else other_left(tuple(self(tuple([])) for _ in range(other_left.ary)))
            if res_self_other != comparator(res_other_self):
                return False
        return True

    def for_each_fixed(self) -> list[Operator]:
        if self.ary == 0: return [lambda x : self(tuple([]))]
        if self.ary == 1: return [lambda x : self(tuple([x]))]
        res = list()
        adj_ary = self.ary - 1
        num_elems_raw = self.dim ** adj_ary
        for i in range(num_elems_raw):
            fixed_vals = num_to_base_padded(i, self.dim, adj_ary)
            for j in range(self.ary):
                output_col = tuple(self(tuple(fixed_vals[:j] + [k] + fixed_vals[j:])) for k in reversed(range(self.dim)))
                res.append(Operator(output_col))
        return res

    def all_fixed_matches(self, other: Operator):
        if self.dim != other.dim:
            raise ValueError(f'Got mismatched dim in all_fixed_matches {self.dim} {other.dim}')
        self_for_each_fixed = self.for_each_fixed()
        other_for_each_fixed = other.for_each_fixed()
        for a in self_for_each_fixed:
            for b in other_for_each_fixed:
                for i in range(self.dim):
                    # print('a bound for', a.bound_for)
                    # print('b bound for', b.bound_for)
                    # print('a(0)', a((0,)))
                    # print('a(i)', a((i,)))
                    # print('b(0)', b((0,)))
                    # print('b(i)', b((i,)))
                    # print()
                    if not (a((i,)) == b((i,))): return False
        return True



def tables_of_arys(arys: list[int], dim = 2) -> list[Operator]:
    res = []
    for ary in arys:
        len_output_col = dim ** ary
        num_possible_outputs = dim ** len_output_col
        for i in range(num_possible_outputs):
            raw = num_to_base(i, dim)
            left_padded = [0] * (len_output_col - len(raw)) + raw
            res.append(Operator(left_padded, dim))
    return res



tables = tables_of_arys([1,2,3,4], 2)

op_and = Operator((1,0,0,0))
op_or = Operator((1,1,1,0))
op_converse = Operator((1,1,0,1))
op_implication = Operator((1,0,1,1))
op_nand = Operator((0,1,1,1))
op_nor = Operator((0,0,0,1))
op_nxor = Operator((1,0,0,1))
op_xor = Operator((0,1,1,0))
op_nconverse = Operator((0,0,1,0))
op_nimplication = Operator((0,1,0,0))

# test_op = op_xor
test_op = Operator(
    # (1,1,1,0),
    (1,1,0,0,0,0,0,0),
    # (1,0,0,0,0,0,0,0)
    # (1,1,1,0,1,1,0,0),
    # ary = 2,
    # callable = lambda x : int(not any(x)) # lambda x : int(sum(x) > 1) # lambda x : (sum(x)+0) % 2
)

complement = Operator(
    (1,1,0,0,1,0,0,0)
)
complement_output = Operator(
    (0,0,0,1,0,0,1,1)
)
complement_input = Operator(
    (0,0,1,1,0,1,1,1)
)

# print(test_op)

# print(test_op.test(complement_input, other_right = complement_output))

for t in tables:
    if test_op.test(t):
        print()
        print(t)
        # print('and testing:', op_or.all_fixed_matches(t))
        # print()


