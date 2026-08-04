from __future__ import annotations
from functools import cache
import itertools
from pylab import figure


'''
any functionally complete operator can be used to define a metric; just 
    compose a and b until the effect is 0s on the diag then take the size of all non-zero elements

If I have an associative operator over which I can define a metric, every statement I make tells me
    much more about the system
    if a@b@c@d=0, this implies size(a@b@c@d)+size(0)=size(0)
    and by the triangle rule size(a) + size(b@c@d) = size(0)
    assuming the metric is defined (a,b)=size(a@b)

If I have a commutative operator over which I can define a metric, I learn even more
'''


# Operator class keeps the code below clean
class Operator:
    def __init__(self, o, symbol = ''):
        self.o = o
        self.symbol = symbol
        self.dim = len(o)

    def __call__(self, set1, set2):
        if type(set1) is tuple:
            return tuple(self.o[i][j] for i, j in zip(set1, set2))
        elif type(set1) is str and self.is_commutative():
            return f'({self.symbol.join(sorted([set1, set2]))})'
        elif type(set1) is str:
            return f'({set1}{self.o.symbol}{set2})'
        elif type(set1) is int:
            return self.o[set1][set2]
        raise ValueError(f'bad type {type(set1)} passed to operator')

    def __str__(self):
        return '\n'.join(map(str, self.o))

    def size_repr_rows(self):
        rows = [[0] * (self.dim ** 2) for _ in range(self.dim)]
        for i, r in enumerate(self.o):
            for j, item in enumerate(r):
                rows[item][i * self.dim + j] += 1
        return rows


    def left_identity(self):
        return self._identity(self.o)
    
    def right_identity(self):
        return self._identity(tuple(zip(*self.o)))

    @staticmethod
    def _identity(o):
        try:
            return o.index((0,1,2,3))
        except ValueError:
            return None

    # calculates the total sets "reachable" from the base sets using just supplied operators
    # basically a breadth-first-search on the tree where nodes are sets and edges are operators w/ a base set
    @staticmethod
    def determine_span(every_operator: list[Operator], base_sets: list[tuple]):
        traversed = set()
        pending = set(base_sets)
        while len(pending):
            prior_pending = pending
            pending = set()
            for p in prior_pending:
                for b in base_sets:
                    for o in every_operator:
                        for l in (lambda o, p, b : o(p, b), lambda o, p, b : o(b, p)):
                            to_set = l(o, p, b)
                            if to_set not in traversed: pending.add(to_set)
            traversed = traversed.union(prior_pending)
        return len(traversed)

    def span(self, base_sets):
        return self.determine_span((self,), base_sets)

    def calc_composition(self, other, fun):
        l = len(self.o)
        base = [[[None] * l for _ in range(l)] for _ in range(l)]
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    base[i][j][k] = fun(self, other, (i,), (j,), (k,))[0]
        return tuple(tuple(tuple(b) for b in a) for a in base)

    def check_equivalence(self, other, fun1, fun2):
        return self.calc_composition(other, fun1) == self.calc_composition(other, fun2)

    def distributes_over(self, other):
        return self.check_equivalence(
                other,
                lambda self, other, i, j, k : self(other(i, j), k),
                lambda self, other, i, j, k : other(self(i, k), self(j, k)))

    def reverse_distributes_over(self, other):
        return self.check_equivalence(
                other,
                lambda self, other, i, j, k : self(other(i, j), k),
                lambda self, other, i, j, k : self(other(i, k), other(j, k)))

    def is_associative(self, other = None):
        return self.check_equivalence(
                other or self,
                lambda self, other, i, j, k : self(other(i, j), k),
                lambda self, other, i, j, k : other(i, self(j, k)))

    def is_reverse_associative(self, other = None):
        return self.check_equivalence(
                other or self,
                lambda self, other, i, j, k : self(other(i, j), k),
                lambda self, other, i, j, k : self(i, other(j, k)))

    def zero_diag(self):
        return all(self.o[i][i] == 0 for i in range(self.dim))

    @cache
    def is_commutative(self):
        return all(self.o[i][j] == self.o[j][i] for i in range(len(self.o)) for j in range(len(self.o)))

    def vis_iter(self, num):
        start = tuple(range(4))
        working = start
        print(working)
        for _ in range(num):
            working = self(working, start)
            print(working)

    def vis_composition(self, other, title, fun):
        fig = figure()
        ax = fig.add_subplot(projection = '3d')
        ax.set_title(title)

        comp = self.calc_composition(other, fun)

        a = list()
        b = list()
        c = list()
        v = list()
        color = list()

        for i, vi in enumerate(comp):
            for j, vj in enumerate(vi):
                for k, vk in enumerate(vj):
                    a.append(i)
                    b.append(j)
                    c.append(k)
                    v.append(vk)
                    color.append(['g', 'y', 'tab:orange', 'r'][vk])

        ax.scatter(
                a,
                b,
                c,
                color = color)
        '''
        ax.text(
                a,
                b,
                c,
                v,
                size = 20,
                zorder = 1,
                color = 'k')
        '''

        ax.set_xlabel('A')
        ax.set_ylabel('B')
        ax.set_zlabel('C')

def calc_operators(base_sets):
    basic_operators = (
        (
            (0, 1, 2, 3),
            (1, 2, 3, 0),
            (2, 3, 0, 1),
            (3, 0, 1, 2),
        ),
        (
            (0, 1, 2, 3),
            (1, 0, 3, 2),
            (2, 3, 1, 0),
            (3, 2, 0, 1),
        ),
        (
            (0, 1, 2, 3),
            (1, 3, 0, 2),
            (2, 0, 3, 1),
            (3, 2, 1, 0),
        ),
        (
            (0, 1, 2, 3),
            (1, 0, 3, 2),
            (2, 3, 0, 1),
            (3, 2, 1, 0),
        ),
    )

    results = list()

    # find operators by permutation of rows and columns
    # seems to miss some, need to investigate why
    for basic_operator in basic_operators:
        all_operators = set()
        for p1 in itertools.permutations(tuple(range(4))):
            inter = tuple(zip(*(basic_operator[i] for i in p1)))
            for p2 in itertools.permutations(tuple(range(4))):
                all_operators.add(tuple(zip(*(inter[i] for i in p2))))
                '''
                print(p1, p2)
                print()
                print('\n'.join(map(str, zip(*inter))))
                print()
                print('\n'.join(map(str, tuple(zip(*(inter[i] for i in p2))))))
                input()
                '''

        for raw in all_operators:
            o = Operator(raw)
            results.append({
                'operator': o,
                'reduced': basic_operator,
                'raw': raw,
                'span': o.span(base_sets),
                'left_identity': o.left_identity(),
                'right_identity': o.right_identity(),
                'is_associative': o.is_associative(),
                'zero_diag': o.zero_diag(),
            })
    return results

def calc_heuristic(raw, fun, show = lambda x : False):
    res = {}
    for r in raw:
        a = fun(r)
        if a not in res: res[a] = 0
        if show(a): print(r['raw'])
        res[a] += 1
    return res

def analyze_heuristics(base_sets):
    results = calc_operators(base_sets)
    import json
    for key in ('span', 'left_identity', 'right_identity', 'is_associative', 'reduced', 'zero_diag'):
        print(key, json.dumps(calc_heuristic(results, lambda x : str(x[key])), indent = 2), '\n\n')

    print('span, left, and right ident', json.dumps(calc_heuristic(results, lambda x : x['span'] == 256 and None not in {x['left_identity'], x['right_identity']}), indent = 2), '\n\n')
    print('span and left ident', json.dumps(calc_heuristic(results, lambda x : x['span'] == 256 and x['left_identity'] is not None, show = lambda x : x), indent = 2), '\n\n')
    print('span and right ident', json.dumps(calc_heuristic(results, lambda x : x['span'] == 256 and x['right_identity'] is not None, show = lambda x : x), indent = 2), '\n\n')
    print('l and r ident', json.dumps(calc_heuristic(results, lambda x : None not in {x['left_identity'], x['right_identity']}, show = lambda x : x), indent = 2), '\n\n')
    print('span and associative', json.dumps(calc_heuristic(results, lambda x : x['span'] == 256 and x['is_associative']), indent = 2), '\n\n')
    print('span and zero_diag', json.dumps(calc_heuristic(results, lambda x : x['span'] == 256 and x['zero_diag'], lambda x : x), indent = 2), '\n\n')

def analyze_interesting(of_interest, base_sets):
    # interesting defined as invertible operators with identity of 0

    # a relationship similar to a null element:
    # (A $ 3) @ A = 3
    # (A $ B) @ (A $ B) = 3

    print('span:', Operator.determine_span(
        of_interest,
        base_sets
    ))

    def check_prop(name):
        for a in of_interest:
            for b in of_interest:
                print(a.symbol, name, b.symbol, ':', getattr(a, name)(b))
        print()

    check_prop('distributes_over')
    check_prop('reverse_distributes_over')
    check_prop('is_associative')
    check_prop('is_reverse_associative')

    for i, elem in enumerate(of_interest):
        print('elem', i, ':')
        elem.vis_iter(4)

    # of_interest[0].vis_composition(of_interest[1], r'(A @ B) $ C', lambda self, other, i, j, k : self(other(i, j), k))
    # of_interest[1].vis_composition(of_interest[0], r'(A $ B) @ C', lambda self, other, i, j, k : self(other(i, j), k))
    # of_interest[0].vis_composition(of_interest[1], r'(A \$ C) @ (B \$ C)', lambda self, other, i, j, k : self(other(i, k), other(j, k)))
    # of_interest[1].vis_composition(of_interest[0], r'(A @ C) $ (B @ C)', lambda self, other, i, j, k : self(other(i, k), other(j, k)))

    # pyplot.show()
    return

def iter_compose(iterations, operators, base_sets):
    # operate on (0,1,2,3) to test
    all_expressions = dict(base_sets)
    for _ in range(iterations):
        l = list(all_expressions.keys())
        for e1 in l:
            for e2 in l:
                for o in operators:
                    new_e = f'({o.symbol.join(sorted([e1, e2]))})' # can sort b/c operators are commutative
                    all_expressions[new_e] = o(all_expressions[e1], all_expressions[e2])
    return all_expressions

def search_for_weak_identities(of_interest):
    '''
        1
        a
    ab  abc ac
    b   bc  c
    '''
    base_sets = {
        '1': (1,1,1,1,1,1,1,1),
        'A': (0,1,1,1,1,0,0,0),
        'B': (0,0,0,1,0,1,1,0),
        'C': (0,0,0,1,1,0,1,1),
        # '0': (0,0,0,0),
    }

    a = iter_compose(3, of_interest, base_sets)

    # print('\n'.join(map(str, a.items())))

    res = {}
    for item in a.items():
        if not ('A' in item[0] and 'B' in item[0] and 'C' in item[0]): continue
        if str(item[1]) not in res: res[str(item[1])] = []
        res[str(item[1])].append(item[0])

    import json
    print(json.dumps(res, indent = 2))

    '''
    identities for A,B,C all composed only of type 1 and 0 elemeents:
    ((C@B)$A) = ((C$A)@B) # basically just treat (operator set) as a unit and can then commute
    ((1$A)$(B$C)) = ((1$B)$(A$C)) = ((1$C)$(A$B))
    ((A@A)@(B@C)) = ((A@B)@(A@C))
    ((A$A)$(B$C)) = ((A$B)$(A$C))

    "(0, 1, 1, 0, 3, 1, 2, 1)"
        "((B@C)$A)", 
        "((A$C)@B)",
        B @C $A
        C @B $A
        A $C @B
        C $A @B


    "(0, 1, 1, 0, 3, 1, 3, 1)"
        "((A@B)$C)",
        A @B $C
        B @A $C

    '''

def iter_compose_general(iterations, operators):

    binder = lambda o, f1, f2 : lambda i, j, k : o(f1(i, j, k), f2(i, j, k))
    expr = lambda fun : fun('A', 'B', 'C')
    all_expressions = {
        'A': lambda i, j, k : i,
        'B': lambda i, j, k : j,
        'C': lambda i, j, k : k,
    }

    for _ in range(iterations):
        print(len(all_expressions))
        l = list(all_expressions.keys())
        for e1 in l:
            for e2 in l:
                for o in operators:
                    # print(_, e1, e2, o.symbol)
                    # print(expr(all_expressions[e2]))
                    b = binder(o, all_expressions[e1], all_expressions[e2])
                    e = expr(b)
                    if e in all_expressions: continue
                    all_expressions[e] = b

    return all_expressions

def search_for_equivalent_forms(of_interest):
    # use iter_compose_general to analyze equivalent expressions in search of rules for eliminating parentheses
    a = iter_compose_general(3, of_interest)
    res = {}
    for item in a.items():
        if not ('A' in item[0] and 'B' in item[0] and 'C' in item[0]): continue
        arr = tuple(tuple(tuple(item[1](i,j,k) for k in range(4)) for j in range(4)) for i in range(4))
        if str(arr) not in res: res[str(arr)] = []
        res[str(arr)].append(item[0])

    import json
    print(json.dumps(res, indent = 2))

    # "(((0, 1, 2, 3), (3, 2, 1, 0), (3, 2, 1, 0), (0, 1, 2, 3)), ((3, 2, 1, 0), (1, 3, 0, 2), (3, 2, 1, 0), (2, 0, 3, 1)), ((3, 2, 1, 0), (3, 2, 1, 0), (3, 2, 1, 0), (3, 2, 1, 0)), ((0, 1, 2, 3), (2, 0, 3, 1), (3, 2, 1, 0), (2, 0, 3, 1)))": [
    #     "(((A@B)$(B$C))$A)",
    #     "(((A$C)$(A@B))$B)",
    #     "(((A$B)$(A@B))$C)",
    #     "(((B$C)$A)$(A@B))",
    #     "(((A$C)$B)$(A@B))",
    #     "(((A$B)$C)$(A@B))",
    #     "(((A@B)$C)$(A$B))",
    #     "(((A@B)$B)$(A$C))",
    #     "(((A@B)$A)$(B$C))"
    # "(((0, 1, 2, 3), (1, 2, 3, 0), (2, 3, 0, 1), (3, 0, 1, 2)), ((2, 1, 2, 1), (3, 2, 3, 2), (0, 3, 0, 3), (1, 0, 1, 0)), ((0, 3, 0, 3), (1, 0, 1, 0), (2, 1, 2, 1), (3, 2, 3, 2)), ((2, 3, 0, 1), (3, 0, 1, 2), (0, 1, 2, 3), (1, 2, 3, 0)))": [
    #     "(((A$C)@(A$C))@((B@C)@(C@C)))",
    #     "(((A$C)@(B@C))@((A$C)@(C@C)))"
    #   ],
    # "(((0, 0, 1, 1), (1, 2, 3, 0), (2, 3, 2, 3), (3, 1, 0, 2)), ((2, 0, 1, 3), (3, 2, 3, 2), (0, 3, 2, 1), (1, 1, 0, 0)), ((0, 0, 1, 1), (1, 2, 3, 0), (2, 3, 2, 3), (3, 1, 0, 2)), ((2, 0, 1, 3), (3, 2, 3, 2), (0, 3, 2, 1), (1, 1, 0, 0)))": [
    #     "(((A@C)$(C$C))@((A@C)@(B$C)))",
    #     "(((A$C)$(C$C))@((A$C)@(B$C)))"
    #   ],
    # "(((0, 2, 1, 1), (3, 1, 0, 0), (3, 1, 0, 0), (0, 2, 1, 1)), ((1, 3, 2, 2), (0, 2, 1, 1), (0, 2, 1, 1), (1, 3, 2, 2)), ((2, 0, 3, 3), (1, 3, 2, 2), (1, 3, 2, 2), (2, 0, 3, 3)), ((3, 1, 0, 0), (2, 0, 3, 3), (2, 0, 3, 3), (3, 1, 0, 0)))": [
    #     "(((A@C)@(B$B))@((C$C)@(C@C)))",
    #     "(((A@C)@(B$B))@((C$C)$(C@C)))",
    #     "(((A@C)@(C@C))@((B$B)@(C$C)))",
    #     "(((A@C)@(C$C))@((B$B)@(C@C)))",
    #     "(((A@C)@(C$C))@((B$B)$(C@C)))"
    #   ],

    # analyze_interesting(
    #     of_interest,
    #     (
    #         (1,1,1,1),
    #         (0,2,2,0),
    #         (0,0,3,3),
    #     )
    # )
    return

'''
of_interest = (
    Operator(( # A @ A @ A @ A = 0; (i + j) % 4
        (0, 1, 2, 3),
        (1, 2, 3, 0),
        (2, 3, 0, 1),
        (3, 0, 1, 2),
    ), '@'),
    Operator(( # flipped: 2, 1, unflipped: 3
        (0, 1, 2, 3),
        (1, 0, 3, 2),
        (2, 3, 1, 0),
        (3, 2, 0, 1),
    ), '|'),
    Operator(( # A $ A $ A $ A = 0; (i + j + ij)
        (0, 1, 2, 3),
        (1, 3, 0, 2),
        (2, 0, 3, 1),
        (3, 2, 1, 0),
    ), '$'),
    # Operator((
    #     (0, 1, 2, 3),
    #     (1, 0, 3, 2),
    #     (2, 3, 0, 1),
    #     (3, 2, 1, 0),
    # ), '~'),
)
# @ and $ span 0,1
# $ and | span 0,2
# @ and | span 0,3
# $ and | span 1,3
# @ and | span 1,2
# @ and | span 2,3, as do @ and $ and ~, as do $ and ~ and |
# $ and | span
# (1,1,1,1),
# (0,2,2,0),
# (0,0,3,3),
# is there some set of base sets that only spans w/ all 4 operators?

base = [[1] * (of_interest[0].dim ** 2)]
for o in of_interest[:-1]:
    base += o.size_repr_rows()

oi_rows = of_interest[-1].size_repr_rows()
import numpy as np
for o in oi_rows:
    print(np.linalg.matrix_rank(base + [o]))

sum_row = [a + b for a, b in zip(oi_rows[0], oi_rows[-1])]
print(np.linalg.matrix_rank(base + [sum_row]))
'''


analyze_heuristics((
    (0,0,0,0),
    (1,1,0,0),
    (0,1,1,0),
    (1,1,1,1),
))



'''
print(len(calc_operators((
    (0,0,0,0),
    (1,1,0,0),
    (0,1,1,0),
    (1,1,1,1),
))))
'''