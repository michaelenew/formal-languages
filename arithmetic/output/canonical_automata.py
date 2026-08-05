"""Canonical symbolic addition: terms with free variables reduce to
canonical minimal automata.

The symbolic-convexity gap (0002 section "What this does not yet give"):
ground terms reduce by the carry recursion, but symbolic terms like
Addition(x, y) have no ground popcount to bound the recursion. This
module closes the gap for the addition fragment. The canonical form of a
statement is the minimal complete synchronous DFA of the relation it
denotes, read least-significant-bit first over one channel per free
variable:

  - Myhill-Nerode: the minimal complete DFA is unique, so the canonical
    form is unique -- the arithmetic analogue of ANF uniqueness.
  - Every compilation step carries an a-priori size bound readable off
    the term (intersection <= |A|*|B| states, projection <= 2^n,
    minimization shrinks), so the reduction is knowably terminating
    with no cleverness.
  - A statement is TRUE iff its canonical automaton is the universal
    one-state automaton -- the automatic-fragment analogue of "reduces
    to 0". Entailment K |= H is language containment, decided by
    emptiness of K intersected with the complement of H. The judgment
    stays one-sided: universal / not-universal, containment /
    no-containment.

Encoding: one letter of input is a *bit column* -- a dict mapping each
variable name (channel) to that variable's bit at the current position.
A word of columns, least significant position first, spells out one
value per channel; any amount of zero-padding is accepted (decode-based
languages), which is what makes projection of internal channels sound.
A column may carry more channels than an automaton knows: every
automaton reads only its own channels and ignores the rest, which is
what makes intersection over different variable sets work with no
alignment bookkeeping.

Base relations (each a hand-built DFA, correctness sampled in the
suite): exclusive-or, intersection, shift-fill-zero (2x), shift-fill-one
(2x+1), addition (the 2-state carry automaton -- the closed form of the
stabilizing series of 0002), trailing-ones (2 states), equality, and
equality-with-a-constant.

Terms are instances of the Term class hierarchy: Variable, Constant,
ShiftFillZero, ShiftFillOne, TrailingOnes, ExclusiveOr, Intersection,
Addition.  Run this file directly for the verification suite.
"""

from __future__ import annotations

from itertools import product as cartesian_product
from typing import Iterator


BitColumn = dict[str, int]
StateIndex = int
VariableAssignment = dict[str, int]

# Internal only: dicts are not hashable, so the transition table is
# keyed by a frozen snapshot of the column. Nothing outside the DFA
# class ever sees this type -- every boundary speaks dict columns.
_FrozenColumn = frozenset[tuple[str, int]]


def _frozen(column: BitColumn) -> _FrozenColumn:
    return frozenset(column.items())


def _all_columns_over(variable_names: tuple[str, ...]) -> list[BitColumn]:
    return [dict(zip(variable_names, bits))
            for bits in cartesian_product(
                (0, 1), repeat=len(variable_names))]


def _column_sort_key(column: BitColumn) -> tuple[tuple[str, int], ...]:
    return tuple(sorted(column.items()))


Transition = tuple[StateIndex, BitColumn, StateIndex]


class DFA:
    """A synchronous multi-channel DFA denoting a relation on numbers.

    Transitions may be partial; a missing transition is an implicit
    dead state. Channels are named by `variable_names`. All
    transforming methods return new automata; nothing mutates.
    """

    def __init__(self,
                 variable_names: tuple[str, ...],
                 state_count: int,
                 initial_state: StateIndex,
                 transitions: list[Transition],
                 accepting_states: frozenset[StateIndex]) -> None:
        self.variable_names: tuple[str, ...] = tuple(
            sorted(variable_names))
        self.state_count: int = state_count
        self.initial_state: StateIndex = initial_state
        self.accepting_states: frozenset[StateIndex] = frozenset(
            accepting_states)
        self._transition_table: dict[
            tuple[StateIndex, _FrozenColumn], StateIndex] = {
            (state, _frozen(column)): target
            for state, column, target in transitions}

    def alphabet(self) -> list[BitColumn]:
        """Every bit column over this automaton's own channels."""
        return _all_columns_over(self.variable_names)

    def transition_target(self, state: StateIndex,
                          column: BitColumn) -> StateIndex | None:
        """Follow one transition. The column may carry extra channels;
        only this automaton's own channels are read."""
        own_column: BitColumn = {
            name: column[name] for name in self.variable_names}
        return self._transition_table.get((state, _frozen(own_column)))

    def transitions(self) -> Iterator[Transition]:
        """Every stored transition, with its column as a dict."""
        for (state, frozen_column), target in (
                self._transition_table.items()):
            yield state, dict(frozen_column), target

    def completed(self) -> DFA:
        """The same relation with a total transition table (an explicit
        dead state absorbs every missing transition)."""
        alphabet = self.alphabet()
        if all(self.transition_target(state, column) is not None
               for state in range(self.state_count)
               for column in alphabet):
            return self
        dead_state: StateIndex = self.state_count
        transitions: list[Transition] = list(self.transitions())
        for state in range(self.state_count + 1):
            for column in alphabet:
                if (state == dead_state
                        or self.transition_target(state, column) is None):
                    transitions.append((state, column, dead_state))
        return DFA(self.variable_names, self.state_count + 1,
                   self.initial_state, transitions,
                   self.accepting_states)

    def complemented(self) -> DFA:
        """The complementary relation (all tuples this one rejects)."""
        total: DFA = self.completed()
        return DFA(total.variable_names, total.state_count,
                   total.initial_state, list(total.transitions()),
                   frozenset(range(total.state_count))
                   - total.accepting_states)

    def intersected_with(self, other: DFA) -> DFA:
        """Conjunction: run both automata in lockstep on shared
        columns. Each automaton reads its own channels; channels known
        to only one operand are unconstrained in the other. State
        bound: |self| * |other|, a priori."""
        joint_variables: tuple[str, ...] = tuple(sorted(
            set(self.variable_names) | set(other.variable_names)))
        pair_index: dict[tuple[StateIndex, StateIndex], StateIndex] = {
            (self.initial_state, other.initial_state): 0}
        pair_order: list[tuple[StateIndex, StateIndex]] = [
            (self.initial_state, other.initial_state)]
        transitions: list[Transition] = []
        current: StateIndex = 0
        while current < len(pair_order):
            self_state, other_state = pair_order[current]
            for column in _all_columns_over(joint_variables):
                self_target = self.transition_target(self_state, column)
                other_target = other.transition_target(other_state,
                                                       column)
                if self_target is None or other_target is None:
                    continue
                target_pair = (self_target, other_target)
                if target_pair not in pair_index:
                    pair_index[target_pair] = len(pair_order)
                    pair_order.append(target_pair)
                transitions.append(
                    (current, column, pair_index[target_pair]))
            current += 1
        accepting_states = frozenset(
            index for pair, index in pair_index.items()
            if pair[0] in self.accepting_states
            and pair[1] in other.accepting_states)
        return DFA(joint_variables, len(pair_order), 0, transitions,
                   accepting_states)

    def existentially_projected(self,
                                variables_to_remove: set[str]) -> DFA:
        """Existential quantification: forget the named channels.

        The removed channels' bits become nondeterministic guesses,
        fixed by the subset construction. Padding closure first: a
        state is made accepting if an accepting state is reachable from
        it via columns that are zero on every surviving channel (the
        removed channels may need more bits than the surviving word
        carries). State bound after determinization: 2^|self|."""
        surviving_variables: tuple[str, ...] = tuple(
            name for name in self.variable_names
            if name not in variables_to_remove)
        zero_successors: dict[StateIndex, set[StateIndex]] = {
            state: set() for state in range(self.state_count)}
        for state, column, target in self.transitions():
            if all(column[name] == 0 for name in surviving_variables):
                zero_successors[state].add(target)
        padding_closed_accepting: set[StateIndex] = set(
            self.accepting_states)
        newly_accepting: set[StateIndex] = set(padding_closed_accepting)
        while newly_accepting:
            newly_accepting = {
                state for state in range(self.state_count)
                if state not in padding_closed_accepting
                and zero_successors[state] & padding_closed_accepting}
            padding_closed_accepting |= newly_accepting
        guessing_successors: dict[
            tuple[StateIndex, _FrozenColumn], set[StateIndex]] = {}
        for state, column, target in self.transitions():
            surviving_column: BitColumn = {
                name: column[name] for name in surviving_variables}
            guessing_successors.setdefault(
                (state, _frozen(surviving_column)), set()).add(target)
        initial_subset: frozenset[StateIndex] = frozenset(
            [self.initial_state])
        subset_index: dict[frozenset[StateIndex], StateIndex] = {
            initial_subset: 0}
        subset_order: list[frozenset[StateIndex]] = [initial_subset]
        transitions: list[Transition] = []
        current: StateIndex = 0
        while current < len(subset_order):
            current_subset = subset_order[current]
            for column in _all_columns_over(surviving_variables):
                successor_subset = frozenset(
                    target for state in current_subset
                    for target in guessing_successors.get(
                        (state, _frozen(column)), ()))
                if not successor_subset:
                    continue
                if successor_subset not in subset_index:
                    subset_index[successor_subset] = len(subset_order)
                    subset_order.append(successor_subset)
                transitions.append(
                    (current, column, subset_index[successor_subset]))
            current += 1
        accepting_states = frozenset(
            index for subset, index in subset_index.items()
            if subset & padding_closed_accepting)
        return DFA(surviving_variables, len(subset_order), 0,
                   transitions, accepting_states)

    def minimized(self) -> DFA:
        """The canonical form: the unique minimal complete DFA
        (Myhill-Nerode), with states renamed in breadth-first order
        over sorted columns so that two canonical automata describe the
        same relation exactly when their fields are equal."""
        total: DFA = self.completed()
        sorted_alphabet: list[BitColumn] = sorted(
            total.alphabet(), key=_column_sort_key)
        reachable_states: set[StateIndex] = {total.initial_state}
        exploration_stack: list[StateIndex] = [total.initial_state]
        while exploration_stack:
            state = exploration_stack.pop()
            for column in sorted_alphabet:
                target = total.transition_target(state, column)
                assert target is not None
                if target not in reachable_states:
                    reachable_states.add(target)
                    exploration_stack.append(target)
        block_of: dict[StateIndex, int] = {
            state: int(state in total.accepting_states)
            for state in reachable_states}
        while True:
            signature_of: dict[StateIndex, tuple[int, ...]] = {}
            for state in reachable_states:
                targets = tuple(
                    block_of[total.transition_target(state, column)]
                    for column in sorted_alphabet)
                signature_of[state] = (block_of[state],) + targets
            block_index_of_signature: dict[tuple[int, ...], int] = {}
            for state in sorted(reachable_states):
                block_index_of_signature.setdefault(
                    signature_of[state], len(block_index_of_signature))
            refined_block_of: dict[StateIndex, int] = {
                state: block_index_of_signature[signature_of[state]]
                for state in reachable_states}
            if refined_block_of == block_of:
                break
            block_of = refined_block_of
        representative_of_block: dict[int, StateIndex] = {}
        for state in sorted(reachable_states):
            representative_of_block.setdefault(block_of[state], state)
        canonical_name_of_block: dict[int, StateIndex] = {
            block_of[total.initial_state]: 0}
        block_order: list[int] = [block_of[total.initial_state]]
        transitions: list[Transition] = []
        current: StateIndex = 0
        while current < len(block_order):
            block = block_order[current]
            representative = representative_of_block[block]
            for column in sorted_alphabet:
                target = total.transition_target(representative, column)
                assert target is not None
                target_block = block_of[target]
                if target_block not in canonical_name_of_block:
                    canonical_name_of_block[target_block] = len(
                        block_order)
                    block_order.append(target_block)
                transitions.append(
                    (current, column,
                     canonical_name_of_block[target_block]))
            current += 1
        canonical_accepting = frozenset(
            canonical_name_of_block[block_of[state]]
            for state in reachable_states
            if state in total.accepting_states)
        return DFA(total.variable_names, len(block_order), 0,
                   transitions, canonical_accepting)

    def describes_same_relation_as(self, other: DFA) -> bool:
        """Semantic equality by comparison of canonical forms -- the
        symbolic layer's 'reduce both and compare' test."""
        self_canonical: DFA = self.minimized()
        other_canonical: DFA = other.minimized()
        return (self_canonical.variable_names
                == other_canonical.variable_names
                and self_canonical.state_count
                == other_canonical.state_count
                and self_canonical._transition_table
                == other_canonical._transition_table
                and self_canonical.accepting_states
                == other_canonical.accepting_states)

    def is_empty(self) -> bool:
        """Does this automaton reject every tuple?"""
        successors_of: dict[StateIndex, set[StateIndex]] = {}
        for state, _column, target in self.transitions():
            successors_of.setdefault(state, set()).add(target)
        visited_states: set[StateIndex] = {self.initial_state}
        exploration_stack: list[StateIndex] = [self.initial_state]
        while exploration_stack:
            state = exploration_stack.pop()
            if state in self.accepting_states:
                return False
            for target in successors_of.get(state, ()):
                if target not in visited_states:
                    visited_states.add(target)
                    exploration_stack.append(target)
        return True

    def is_universal(self) -> bool:
        """Does this automaton accept every tuple? This is the
        'reduces to 0' verdict of the symbolic layer."""
        return self.complemented().is_empty()

    def entails(self, hypothesis: DFA) -> bool:
        """One-sided deduction: everything this relation (the
        knowledge) allows also satisfies the hypothesis. Decided by
        emptiness of knowledge intersected with the hypothesis's
        complement."""
        return self.intersected_with(
            hypothesis.complemented()).is_empty()

    def accepts_assignment(self,
                           assignment: VariableAssignment) -> bool:
        """Does this automaton accept the given values for its
        channels?"""
        column_count: int = max(
            [value.bit_length() for value in assignment.values()]
            + [1]) + 1
        state: StateIndex | None = self.initial_state
        for bit_position in range(column_count):
            column: BitColumn = {
                name: (assignment[name] >> bit_position) & 1
                for name in self.variable_names}
            if state is None:
                return False
            state = self.transition_target(state, column)
        return state in self.accepting_states


# ---------------------------------------------------------------------
# Base relation automata.  With dict columns these read as direct
# statements of the per-column logic: enumerate the bit combinations,
# keep the legal ones, name the states after what they remember.
# ---------------------------------------------------------------------

def relation_exclusive_or(left_variable: str, right_variable: str,
                          result_variable: str) -> DFA:
    """result = left ^ right (symmetric difference). Stateless."""
    transitions: list[Transition] = [
        (0, {left_variable: left_bit, right_variable: right_bit,
             result_variable: left_bit ^ right_bit}, 0)
        for left_bit in (0, 1) for right_bit in (0, 1)]
    return DFA((left_variable, right_variable, result_variable),
               1, 0, transitions, frozenset({0}))


def relation_intersection(left_variable: str, right_variable: str,
                          result_variable: str) -> DFA:
    """result = left & right (set intersection). Stateless."""
    transitions: list[Transition] = [
        (0, {left_variable: left_bit, right_variable: right_bit,
             result_variable: left_bit & right_bit}, 0)
        for left_bit in (0, 1) for right_bit in (0, 1)]
    return DFA((left_variable, right_variable, result_variable),
               1, 0, transitions, frozenset({0}))


def relation_addition(left_variable: str, right_variable: str,
                      result_variable: str) -> DFA:
    """result = left + right: the 2-state carry automaton -- the closed
    form of the stabilizing carry series (0002 Props 5/6). The state IS
    the carry bit; accept with no carry outstanding."""
    transitions: list[Transition] = []
    for carry_bit in (0, 1):
        for left_bit in (0, 1):
            for right_bit in (0, 1):
                next_carry: StateIndex = (
                    (left_bit & right_bit) | (left_bit & carry_bit)
                    | (right_bit & carry_bit))
                transitions.append((
                    carry_bit,
                    {left_variable: left_bit,
                     right_variable: right_bit,
                     result_variable: left_bit ^ right_bit ^ carry_bit},
                    next_carry))
    return DFA((left_variable, right_variable, result_variable),
               2, 0, transitions, frozenset({0}))


def relation_shift_fill_zero(input_variable: str,
                             output_variable: str) -> DFA:
    """output = 2 * input (the corpus's n0/inc; 0002's a).
    The state is the bit owed to the output channel."""
    transitions: list[Transition] = [
        (owed_bit,
         {input_variable: input_bit, output_variable: owed_bit},
         input_bit)
        for owed_bit in (0, 1) for input_bit in (0, 1)]
    return DFA((input_variable, output_variable), 2, 0, transitions,
               frozenset({0}))


def relation_shift_fill_one(input_variable: str,
                            output_variable: str) -> DFA:
    """output = 2 * input + 1 (the corpus's n1; 0002's b). The start
    state demands the output's low bit be 1, then behaves as
    shift-fill-zero."""
    start_state: StateIndex = 2
    transitions: list[Transition] = [
        (start_state,
         {input_variable: input_bit, output_variable: 1},
         input_bit)
        for input_bit in (0, 1)]
    transitions += [
        (owed_bit,
         {input_variable: input_bit, output_variable: owed_bit},
         input_bit)
        for owed_bit in (0, 1) for input_bit in (0, 1)]
    return DFA((input_variable, output_variable), 3, start_state,
               transitions, frozenset({0}))


def relation_trailing_ones(input_variable: str,
                           output_variable: str) -> DFA:
    """output = T(input), the trailing-ones mask: two states, inside /
    outside the trailing-ones region -- the closed form of the series
    x & b(x) & b(b(x)) & ... (0002 Prop 2; the corpus's $)."""
    outside_region: StateIndex = 0
    inside_region: StateIndex = 1
    transitions: list[Transition] = [
        (inside_region, {input_variable: 1, output_variable: 1},
         inside_region),
        (inside_region, {input_variable: 0, output_variable: 0},
         outside_region),
        (outside_region, {input_variable: 0, output_variable: 0},
         outside_region),
        (outside_region, {input_variable: 1, output_variable: 0},
         outside_region),
    ]
    return DFA((input_variable, output_variable), 2, inside_region,
               transitions, frozenset({0, 1}))


def relation_equality(input_variable: str,
                      output_variable: str) -> DFA:
    """output = input. Stateless."""
    transitions: list[Transition] = [
        (0, {input_variable: shared_bit, output_variable: shared_bit}, 0)
        for shared_bit in (0, 1)]
    return DFA((input_variable, output_variable), 1, 0, transitions,
               frozenset({0}))


def relation_constant(variable_name: str, constant_value: int) -> DFA:
    """variable = constant. States count matched bit positions; state i
    is accepting exactly when no 1-bits of the constant remain above."""
    bit_length: int = max(constant_value.bit_length(), 1)
    transitions: list[Transition] = [
        (bit_position,
         {variable_name: (constant_value >> bit_position) & 1},
         bit_position + 1)
        for bit_position in range(bit_length)]
    transitions.append((bit_length, {variable_name: 0}, bit_length))
    accepting_states = frozenset(
        bit_position for bit_position in range(bit_length + 1)
        if constant_value >> bit_position == 0)
    return DFA((variable_name,), bit_length + 1, 0, transitions,
               accepting_states)


# ---------------------------------------------------------------------
# Terms and their compilation
# ---------------------------------------------------------------------

INTERNAL_VARIABLE_PREFIX: str = "_"


def is_internal_variable(variable_name: str) -> bool:
    return variable_name.startswith(INTERNAL_VARIABLE_PREFIX)


class FreshVariableSource:
    """Supplies internal channel names, one per compiled term node."""

    def __init__(self) -> None:
        self.next_index: int = 0

    def fresh_variable_name(self) -> str:
        self.next_index += 1
        return f"{INTERNAL_VARIABLE_PREFIX}{self.next_index}"


class CompiledRelation:
    """The result of compiling a term: an automaton relating the term's
    free variables to a result channel."""

    def __init__(self, automaton: DFA,
                 result_variable_name: str) -> None:
        self.automaton: DFA = automaton
        self.result_variable_name: str = result_variable_name


class Term:
    """A term of the language. Subclasses: Variable, Constant,
    ShiftFillZero, ShiftFillOne, TrailingOnes, ExclusiveOr,
    Intersection, Addition."""

    def compiled(self,
                 fresh_source: FreshVariableSource) -> CompiledRelation:
        raise NotImplementedError

    def _compiled_through_base_relation(
            self,
            operand_relations: list[CompiledRelation],
            base_relation: DFA,
            result_variable_name: str) -> CompiledRelation:
        """Conjoin operand automata with a base relation, then project
        away the operands' internal result channels (eager projection
        keeps the channel count small at every step)."""
        combined: DFA = base_relation
        for operand_relation in operand_relations:
            combined = combined.intersected_with(
                operand_relation.automaton)
        internal_channels: set[str] = {
            operand_relation.result_variable_name
            for operand_relation in operand_relations
            if is_internal_variable(
                operand_relation.result_variable_name)}
        if internal_channels:
            combined = combined.existentially_projected(
                internal_channels)
        return CompiledRelation(combined.minimized(),
                                result_variable_name)


class Variable(Term):
    def __init__(self, variable_name: str) -> None:
        self.variable_name: str = variable_name

    def compiled(self,
                 fresh_source: FreshVariableSource) -> CompiledRelation:
        unconstrained = DFA(
            (self.variable_name,), 1, 0,
            [(0, {self.variable_name: bit}, 0) for bit in (0, 1)],
            frozenset({0}))
        return CompiledRelation(unconstrained, self.variable_name)


class Constant(Term):
    def __init__(self, value: int) -> None:
        self.value: int = value

    def compiled(self,
                 fresh_source: FreshVariableSource) -> CompiledRelation:
        result_variable_name: str = fresh_source.fresh_variable_name()
        return CompiledRelation(
            relation_constant(result_variable_name, self.value),
            result_variable_name)


class _UnaryTerm(Term):
    def __init__(self, operand: Term) -> None:
        self.operand: Term = operand

    def _base_relation(self, input_variable: str,
                       output_variable: str) -> DFA:
        raise NotImplementedError

    def compiled(self,
                 fresh_source: FreshVariableSource) -> CompiledRelation:
        operand_relation: CompiledRelation = self.operand.compiled(
            fresh_source)
        result_variable_name: str = fresh_source.fresh_variable_name()
        return self._compiled_through_base_relation(
            [operand_relation],
            self._base_relation(operand_relation.result_variable_name,
                                result_variable_name),
            result_variable_name)


class ShiftFillZero(_UnaryTerm):
    """2x -- the corpus's n0/inc, 0002's a."""

    def _base_relation(self, input_variable: str,
                       output_variable: str) -> DFA:
        return relation_shift_fill_zero(input_variable, output_variable)


class ShiftFillOne(_UnaryTerm):
    """2x + 1 -- the corpus's n1, 0002's b."""

    def _base_relation(self, input_variable: str,
                       output_variable: str) -> DFA:
        return relation_shift_fill_one(input_variable, output_variable)


class TrailingOnes(_UnaryTerm):
    """T(x) -- the corpus's $."""

    def _base_relation(self, input_variable: str,
                       output_variable: str) -> DFA:
        return relation_trailing_ones(input_variable, output_variable)


class _BinaryTerm(Term):
    def __init__(self, left_operand: Term, right_operand: Term) -> None:
        self.left_operand: Term = left_operand
        self.right_operand: Term = right_operand

    def _base_relation(self, left_variable: str, right_variable: str,
                       result_variable: str) -> DFA:
        raise NotImplementedError

    def compiled(self,
                 fresh_source: FreshVariableSource) -> CompiledRelation:
        left_relation: CompiledRelation = self.left_operand.compiled(
            fresh_source)
        right_relation: CompiledRelation = self.right_operand.compiled(
            fresh_source)
        result_variable_name: str = fresh_source.fresh_variable_name()
        return self._compiled_through_base_relation(
            [left_relation, right_relation],
            self._base_relation(left_relation.result_variable_name,
                                right_relation.result_variable_name,
                                result_variable_name),
            result_variable_name)


class ExclusiveOr(_BinaryTerm):
    def _base_relation(self, left_variable: str, right_variable: str,
                       result_variable: str) -> DFA:
        return relation_exclusive_or(left_variable, right_variable,
                                     result_variable)


class Intersection(_BinaryTerm):
    def _base_relation(self, left_variable: str, right_variable: str,
                       result_variable: str) -> DFA:
        return relation_intersection(left_variable, right_variable,
                                     result_variable)


class Addition(_BinaryTerm):
    def _base_relation(self, left_variable: str, right_variable: str,
                       result_variable: str) -> DFA:
        return relation_addition(left_variable, right_variable,
                                 result_variable)


def statement_of_equality(left_term: Term, right_term: Term) -> DFA:
    """The statement 'left_term = right_term' as a canonical automaton
    over the free variables. This is the symbolic H ^ HK substrate:
    equality is XOR reducing to 0, here realized as the equality
    relation on the two result channels with internals projected
    away."""
    fresh_source = FreshVariableSource()
    left_relation: CompiledRelation = left_term.compiled(fresh_source)
    right_relation: CompiledRelation = right_term.compiled(fresh_source)
    if (left_relation.result_variable_name
            == right_relation.result_variable_name):
        combined: DFA = left_relation.automaton.intersected_with(
            right_relation.automaton)
    else:
        combined = left_relation.automaton.intersected_with(
            right_relation.automaton).intersected_with(
            relation_equality(left_relation.result_variable_name,
                              right_relation.result_variable_name))
    internal_channels: set[str] = {
        name for name in (left_relation.result_variable_name,
                          right_relation.result_variable_name)
        if is_internal_variable(name)}
    if internal_channels:
        combined = combined.existentially_projected(internal_channels)
    return combined.minimized()


# ---------------------------------------------------------------------
# Verification suite
# ---------------------------------------------------------------------

def run_verification_suite(random_seed: int = 20260804) -> None:
    import random
    random_source = random.Random(random_seed)
    x_term, y_term, w_term, z_term = (
        Variable('x'), Variable('y'), Variable('w'), Variable('z'))

    # Base addition automaton against ground arithmetic
    addition_relation: DFA = relation_addition('x', 'y', 'z')
    for _ in range(2000):
        left_value = random_source.randrange(1 << 16)
        right_value = random_source.randrange(1 << 16)
        assert addition_relation.accepts_assignment(
            {'x': left_value, 'y': right_value,
             'z': left_value + right_value})
        assert not addition_relation.accepts_assignment(
            {'x': left_value, 'y': right_value,
             'z': left_value + right_value
             + random_source.randrange(1, 9)})
    print("base addition automaton: 2000 accept + 2000 reject "
          "samples  OK")

    # THE decisive test: successor two ways -> identical canonical
    # automaton. x ^ b(T(x)) (the stabilizing-series successor, 0002
    # Prop 3) vs x + 1: same canonical object, mechanically.
    successor_by_series: DFA = statement_of_equality(
        ExclusiveOr(x_term, ShiftFillOne(TrailingOnes(x_term))), z_term)
    successor_by_addition: DFA = statement_of_equality(
        Addition(x_term, Constant(1)), z_term)
    assert successor_by_series.describes_same_relation_as(
        successor_by_addition)
    print(f"successor via series == successor via addition of 1: "
          f"identical canonical automaton "
          f"({successor_by_series.state_count} states)  OK")

    # Laws of addition as universality (the 'reduces to 0' analogue)
    assert statement_of_equality(
        Addition(x_term, y_term),
        Addition(y_term, x_term)).is_universal()
    assert statement_of_equality(
        Addition(Addition(x_term, y_term), w_term),
        Addition(x_term, Addition(y_term, w_term))).is_universal()
    assert statement_of_equality(
        Addition(x_term, Constant(0)), x_term).is_universal()
    print("commutativity, associativity, unit: universal  OK")

    # Carry-save identity (clue/2026-06-21):
    # add(x^y^w, a(xy ^ xw ^ yw)) = x + y + w
    carry_save_left: Term = Addition(
        ExclusiveOr(x_term, ExclusiveOr(y_term, w_term)),
        ShiftFillZero(ExclusiveOr(
            Intersection(x_term, y_term),
            ExclusiveOr(Intersection(x_term, w_term),
                        Intersection(y_term, w_term)))))
    carry_save_right: Term = Addition(
        x_term, Addition(y_term, w_term))
    assert statement_of_equality(
        carry_save_left, carry_save_right).is_universal()
    print("carry-save identity: universal  OK")

    # One-sidedness: a non-law is not universal and not empty
    non_law: DFA = statement_of_equality(
        Addition(x_term, y_term), x_term)
    assert not non_law.is_universal() and not non_law.is_empty()
    print("x + y = x: neither universal nor empty (undecided as a "
          "law, satisfiable as a constraint)  OK")

    # Entailment, strict: y = 2x  entails  (exists w: y = w + w)
    knowledge: DFA = statement_of_equality(
        y_term, ShiftFillZero(x_term))
    hypothesis: DFA = statement_of_equality(
        y_term, Addition(w_term, w_term)).existentially_projected(
        {'w'}).minimized()
    assert knowledge.entails(hypothesis)
    assert not hypothesis.entails(knowledge)
    print("y = 2x entails (exists w: y = w + w), and not "
          "conversely  OK")

    # Multiplication by a constant stays in the fragment: z = 3x
    triple_statement: DFA = statement_of_equality(
        Addition(x_term, ShiftFillZero(x_term)), z_term)
    for _ in range(500):
        sample_value = random_source.randrange(1 << 24)
        assert triple_statement.accepts_assignment(
            {'x': sample_value, 'z': 3 * sample_value})
        assert not triple_statement.accepts_assignment(
            {'x': sample_value, 'z': 3 * sample_value + 1})
    print(f"z = 3x via x + 2x: 500 samples "
          f"({triple_statement.state_count} canonical states)  OK")

    # Canonical sizes (complete minimal automata, dead state included)
    for label, automaton in [
            ("z = x + y", addition_relation),
            ("z = x + 1", successor_by_addition),
            ("z = T(x)", statement_of_equality(
                TrailingOnes(x_term), z_term)),
            ("z = 3x", triple_statement)]:
        print(f"    canonical size  {label}: "
              f"{automaton.minimized().state_count} states")

    # Basis derivations (0008): the wiring-closure of {^, &, a} plus
    # constants generates the other primitives, and via Buechi-Bruyere
    # (the {+, V_2}-definable relations are exactly the 2-automatic
    # ones) the entire canonical layer.

    def union_term(left: Term, right: Term) -> Term:
        return ExclusiveOr(ExclusiveOr(left, right),
                           Intersection(left, right))

    # b from {a, ^, 1}
    assert statement_of_equality(
        ShiftFillOne(x_term),
        ExclusiveOr(ShiftFillZero(x_term), Constant(1))).is_universal()

    # T's graph, quantifier-free from {^, &, a, b, 1}:
    # z = T(x) <=> z is an all-ones prefix (z & b(z) = z), z lies
    # inside x, and the next position up (b(z) ^ z) is not in x.
    all_ones_prefix: DFA = statement_of_equality(
        Intersection(z_term, ShiftFillOne(z_term)), z_term)
    derived_trailing_ones: DFA = all_ones_prefix.intersected_with(
        statement_of_equality(Intersection(z_term, x_term), z_term)
    ).intersected_with(statement_of_equality(
        Intersection(ExclusiveOr(ShiftFillOne(z_term), z_term), x_term),
        Constant(0))).minimized()
    assert derived_trailing_ones.describes_same_relation_as(
        statement_of_equality(TrailingOnes(x_term), z_term))

    # Addition from {^, &, a} with one hidden carry wire whose defining
    # equation has a unique solution (bit 0 is 0, bit i+1 is determined
    # by bit i):  z = x + y  <=>
    #   exists C: C = a(xy or ((x^y) & C))  and  z = x ^ y ^ C
    carry_term: Term = Variable('Carry')
    derived_addition: DFA = statement_of_equality(
        carry_term,
        ShiftFillZero(union_term(
            Intersection(x_term, y_term),
            Intersection(ExclusiveOr(x_term, y_term), carry_term)))
    ).intersected_with(statement_of_equality(
        z_term, ExclusiveOr(ExclusiveOr(x_term, y_term), carry_term))
    ).existentially_projected({'Carry'}).minimized()
    assert derived_addition.describes_same_relation_as(
        addition_relation.minimized())

    # V_2 (lowest set bit) with one hidden mask wire, completing the
    # bridge to Buechi-Bruyere:  z = V_2(x)  <=>
    #   exists m: m all-ones prefix, z = b(m) ^ m, z inside x, m&x = 0
    mask_term: Term = Variable('Mask')
    derived_lowest_bit: DFA = statement_of_equality(
        Intersection(mask_term, ShiftFillOne(mask_term)), mask_term
    ).intersected_with(statement_of_equality(
        z_term, ExclusiveOr(ShiftFillOne(mask_term), mask_term))
    ).intersected_with(statement_of_equality(
        Intersection(z_term, x_term), z_term)
    ).intersected_with(statement_of_equality(
        Intersection(mask_term, x_term), Constant(0))
    ).existentially_projected({'Mask'}).minimized()
    for _ in range(1000):
        sample_value = random_source.randrange(1, 1 << 20)
        lowest_set_bit = sample_value & -sample_value
        assert derived_lowest_bit.accepts_assignment(
            {'x': sample_value, 'z': lowest_set_bit})
        assert not derived_lowest_bit.accepts_assignment(
            {'x': sample_value, 'z': lowest_set_bit << 1})
    assert not derived_lowest_bit.accepts_assignment({'x': 0, 'z': 0})
    print("basis derivations: b, T (quantifier-free), addition "
          "(one hidden wire), V_2 -- all from {^, &, a, constants}  OK")

    print("all checks passed")


if __name__ == "__main__":
    run_verification_suite()
