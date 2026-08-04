from __future__ import annotations
import logging
import uuid
import functools
import itertools
from typing import Callable, Iterable, Iterator
'''
Trying the first thing mentioned in [[2024-12-29 Next things to try]]. We explore the extent to which
natural extensions of XOR and AND are FC in higher dimensional logic
'''

# logging.getLogger().setLevel(logging.DEBUG)

uuids = itertools.count()
def get_uuid() -> str:
    return str(next(uuids))

class Function:
    def __init__(self, input_slots: tuple[None | Function], function: Callable, name: str):
        logging.debug(f'Initializing Function with {list(map(str, input_slots))=} {function=}')
        self.input_slots = input_slots
        self.function = function
        self.name = name

        self.evaluations: dict[str, int] = dict()

    def __hash__(self):
        return hash(self.show())

    def __eq__(self, other: Function):
        return self.show() == other.show()
    
    def __str__(self):
        return self.show()

    def show(self) -> str:
        _, call = self._eval_with(itertools.count(), get_uuid())
        return call

    def descendents(self) -> set[Function]:
        return {self, *(
            descendent
            for slot in filter(lambda x : x, self.input_slots)
            for descendent in slot.descendents()
        )}
    
    def partial_arity(self) -> int:
        return sum(1 for slot in self.input_slots if slot is None)

    def arity(self):
        return len(self.remaining_inputs())
    
    def deep_copy_with_injections(self,
            injections: dict[tuple[Function, int], Function],
            already_deep_copied: dict[Function, Function] = None) -> Function:
        '''
        injections:
            In the key tuple, the Function is the function to replace and the int on the input is the index in input_slots to replace
            The value Function is the Function to insert at that slot

        already_deep_copied:
            implementation detail to avoid double-copying a function that injects its output twice
        '''
        already_deep_copied = already_deep_copied or dict()
        def get(key: tuple[Function, int], default: Function):
            if key in injections:
                return injections[key]
            if default is None:
                return None
            if default in already_deep_copied:
                return already_deep_copied[default]
            logging.debug(f'  I am deep copying to make a child of {self=} {default=}')
            already_deep_copied[self] = default.deep_copy_with_injections(injections, already_deep_copied)
            return already_deep_copied[self]

        return Function(
            input_slots = tuple(
                get((self, i), slot) # injections.get((self, i), slot)
                for i, slot in enumerate(self.input_slots)
            ),
            function = self.function,
            name = self.name,
        )

    def remaining_inputs(self) -> set[tuple[Function, int]]:
        return {
            (descendent, index)
            for descendent in self.descendents()
            for index, val in enumerate(descendent.input_slots)
            if val is None
        }

    def with_possible_inputs(self, other: Function, min_arity = 0, max_arity: int = 4) -> Iterable[Function]:
        # result_arity == self.arity() + other.arity() - take_count
        # and min_arity <= result_arity < max_arity
        # where take_count is the number of indexes into which we inject other's value
        # therefore
        # min_arity <= self.arity() + other.arity() - take_count < max_arity
        # self.arity() + other.arity() - max_arity < take_count
        # take_count > self.arity() + other.arity() - max_arity
        # take_count <= self.arity() + other.arity() - min_arity
        min_take_count = self.arity() + other.arity() - max_arity + 1
        max_take_count = self.arity() + other.arity() - min_arity + 1

        # the output of other is the input to 0 or more remaining inputs
        remaining_input_combinations = (
            combo
            for take_count in range(max(0, min_take_count), max(0, max_take_count))
            for combo in itertools.combinations(self.remaining_inputs(), take_count)
        )

        for combo in remaining_input_combinations:
            func = self.deep_copy_with_injections(dict((c, other) for c in combo))
            expected_arity = self.arity() + other.arity() - len(combo)
            arity = func.arity()
            if expected_arity != arity:
                replacements = [(c[0].show(), c[1]) for c in combo]
                raise ValueError(
                    f'Unexpected arity {arity}, expected {expected_arity} based on {replacements=}'
                    + f' composing {self.show()=} and {other.show()=} producing {func.show()}'
                )
            if not (min_arity <= arity and max_arity > arity):
                raise ValueError(f'This should not be possible! {func.show()} had arity {arity} not between {min_arity} and {max_arity}')

            yield func

    def _eval_with(self, additional_inputs: Iterator[int], evaluation_id: str) -> tuple[int, str]:
        if evaluation_id in self.evaluations:
            # We've evaluated this function for this call, so we short-circuit and return the known existing value
            # importantly, this SKIPS taking more values from additional_inputs
            return self.evaluations[evaluation_id]

        iter_count = [0]
        def _next(iterable: Iterator[int]) -> int:
            val = next(iterable)
            iter_count[0] = iter_count[0] + 1
            return val

        evaluations = list(
            [_next(additional_inputs)] * 2 if slot is None else slot._eval_with(additional_inputs, evaluation_id)
            for slot in self.input_slots
        )
        if iter_count[0] != self.partial_arity():
            print(f'  Incorrect pull count {self.name} {id(self)} pulled {iter_count} inputs but expected {self.partial_arity()}')
            print(f'    {self}')
        inputs, captures = list(zip(*evaluations)) or [(), ()]
        self.evaluations[evaluation_id] = (
            self.function(*inputs),
            f'{self.name}({", ".join(map(str, captures))})'
        )
        return self.evaluations[evaluation_id]
    
    def eval_with(self, additional_inputs: Iterator[str]) -> int:
        a = list(additional_inputs)
        print(f'      Calling {self} with {a} which has arity {self.arity()} and inputs {[(str(a), b) for a, b in self.remaining_inputs()]}')
        print(f'        {self.partial_arity()=} and {list(map(Function.partial_arity, self.descendents()))=}')
        print(f'        {list(map(str, self.descendents()))}')
        additional_inputs = iter(a)
        result, _ = self._eval_with(additional_inputs, get_uuid())
        return result

    def truth_table_outputs(self, left_hand_side: list[tuple[int]]) -> tuple[int]:
        if len(left_hand_side[0]) != self.arity():
            raise ValueError('Bad truth table supplied')
        return tuple(
            self.eval_with(iter(input_tuple))
            for input_tuple in left_hand_side
        )



DIMENSION = 3



# input_pairs is the left side of the truth table of a single binary function in DIMENSION-valued logic
input_pairs: list[tuple[int, int]] = list()
for i in range(DIMENSION):
    for j in range(DIMENSION):
        input_pairs.append((i, j))

# outputs is every possible right side of the truth table for a single binary function in DIMENSION-valued logic
outputs = set(itertools.product(list(range(DIMENSION)), repeat = len(input_pairs)))
remove_output = lambda x : outputs.remove(x) if x in outputs else None

print(f'{len(input_pairs)=}, {len(outputs)=}')

AND = Function([None] * 2, lambda a, b : a if a == b else 0, 'AND')
XOR = Function([None] * 2, lambda a, b : abs(a - b), 'XOR')
C1 = Function([], lambda : 1, 'C1')
IDENTITY = Function([None], lambda x : x, 'I')


'''
# Repro case for a bug wherein we weren't recursively copying when adding functions
a = AND.deep_copy_with_injections({
    (AND, 1): AND,
})
inner_and = a.input_slots[1]
print(f'{a==inner_and=}')
b = a.deep_copy_with_injections({
    (inner_and, 0): AND,
    (inner_and, 1): AND,
})
print(AND.show(), id(AND))
print(a.show(), id(a))
print(b.show(), id(b))

import sys
sys.exit(0)
'''

'''
Okay so this code is pretty bad - side effects everywhere and hard to use. Here's the guide:

If you don't do a .with_possible_inputs(IDENTITY) then it's not possible to duplicate an input into the same function.
Basically always do a .with_possible_inputs(IDENTITY) right before checking the truth tables. You MUST do this even if
not allowing the identity as a composed function.

The Function class behaves like a node in a circuit diagram. It is evaluated once per call then its output can
be duplicated into multiple downstream nodes

Each .with_possible_inputs(...) call adds a single "node" to the circuit diagram everywhere there is space upstream
'''

for terminal_func in (AND, XOR):
    for composed_with_ident in terminal_func.with_possible_inputs(IDENTITY, 2, 3):
        remove_output(terminal_func.truth_table_outputs(input_pairs))

    for second_composed in (f for other in (AND, XOR, C1) for f in terminal_func.with_possible_inputs(other)):
        print('  second', second_composed.show())
        for composed_with_ident in second_composed.with_possible_inputs(IDENTITY, 2, 3):
            print('    with_ident', composed_with_ident.show())
            to_remove = composed_with_ident.truth_table_outputs(input_pairs)
            remove_output(to_remove)

    print('### ON TO THIRD ###')

    for second_composed in (f for other in (AND, XOR, C1) for f in terminal_func.with_possible_inputs(other)):
        print('  second', second_composed.show())
        for third_composed in (f for other in (AND, XOR, C1) for f in second_composed.with_possible_inputs(other)):
            print('    third', third_composed.show())
            for composed_with_ident in third_composed.with_possible_inputs(IDENTITY, 2, 3):
                print('      with_ident', composed_with_ident.show())
                to_remove = composed_with_ident.truth_table_outputs(input_pairs)
                remove_output(to_remove)




print(f'{len(outputs)=}')
