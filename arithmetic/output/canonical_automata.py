"""Canonical symbolic addition: terms with free variables reduce to
canonical minimal automata.

The symbolic-convexity gap (0002 section "What this does not yet give"):
ground terms reduce by the carry recursion, but symbolic terms like
Addition(x, y) have no ground popcount to bound the recursion. This
module closes the gap for the addition fragment. The canonical form of a
statement is the minimal complete synchronous DFA of the relation it
denotes, read least-significant-bit first over one track per free
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

Encoding: a tuple of finite sets (numbers) is a word over bit columns,
one bit per track per letter, letter index i giving bit i of every
track; any amount of zero-padding is accepted (decode-based languages),
which is what makes projection of internal tracks sound.

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


BitColumn = tuple[int, ...]
StateIndex = int
TransitionTable = dict[tuple[StateIndex, BitColumn], StateIndex]
VariableAssignment = dict[str, int]


def _column_projection(column: BitColumn,
                       source_variables: tuple[str, ...],
                       target_variables: tuple[str, ...]) -> BitColumn:
    """Restrict a bit column to the named target tracks."""
    position_of: dict[str, int] = {
        name: position for position, name in enumerate(source_variables)}
    return tuple(column[position_of[name]] for name in target_variables)


class DFA:
    """A synchronous multi-track DFA denoting a relation on numbers.

    Transitions may be partial; a missing transition is an implicit dead
    state. Tracks are named by `variable_names` (kept sorted), and each
    letter of the alphabet is one bit column aligned with those names.
    All transforming methods return new automata; nothing mutates.
    """

    def __init__(self,
                 variable_names: tuple[str, ...],
                 state_count: int,
                 initial_state: StateIndex,
                 transition_table: TransitionTable,
                 accepting_states: frozenset[StateIndex]) -> None:
        self.variable_names: tuple[str, ...] = tuple(variable_names)
        self.state_count: int = state_count
        self.initial_state: StateIndex = initial_state
        self.transition_table: TransitionTable = transition_table
        self.accepting_states: frozenset[StateIndex] = (
            frozenset(accepting_states))

    def alphabet(self) -> list[BitColumn]:
        """Every bit column over this automaton's tracks."""
        return list(cartesian_product(
            (0, 1), repeat=len(self.variable_names)))

    def completed(self) -> DFA:
        """The same relation with a total transition table (an explicit
        dead state absorbs every missing transition)."""
        alphabet = self.alphabet()
        if all((state, column) in self.transition_table
               for state in range(self.state_count) for column in alphabet):
            return self
        transition_table: TransitionTable = dict(self.transition_table)
        dead_state: StateIndex = self.state_count
        for state in range(self.state_count + 1):
            for column in alphabet:
                transition_table.setdefault((state, column), dead_state)
        return DFA(self.variable_names, self.state_count + 1,
                   self.initial_state, transition_table,
                   self.accepting_states)

    def complemented(self) -> DFA:
        """The complementary relation (all tuples this one rejects)."""
        total: DFA = self.completed()
        return DFA(total.variable_names, total.state_count,
                   total.initial_state, total.transition_table,
                   frozenset(range(total.state_count))
                   - total.accepting_states)

    def intersected_with(self, other: DFA) -> DFA:
        """Conjunction: run both automata in lockstep. Tracks appearing
        in only one operand are unconstrained in the other
        (cylindrification). State bound: |self| * |other|, a priori."""
        joint_variables: tuple[str, ...] = tuple(sorted(
            set(self.variable_names) | set(other.variable_names)))
        joint_alphabet = list(cartesian_product(
            (0, 1), repeat=len(joint_variables)))
        pair_index: dict[tuple[StateIndex, StateIndex], StateIndex] = {
            (self.initial_state, other.initial_state): 0}
        pair_order: list[tuple[StateIndex, StateIndex]] = [
            (self.initial_state, other.initial_state)]
        transition_table: TransitionTable = {}
        current: StateIndex = 0
        while current < len(pair_order):
            self_state, other_state = pair_order[current]
            for column in joint_alphabet:
                self_target = self.transition_table.get(
                    (self_state, _column_projection(
                        column, joint_variables, self.variable_names)))
                other_target = other.transition_table.get(
                    (other_state, _column_projection(
                        column, joint_variables, other.variable_names)))
                if self_target is None or other_target is None:
                    continue
                if (self_target, other_target) not in pair_index:
                    pair_index[(self_target, other_target)] = len(pair_order)
                    pair_order.append((self_target, other_target))
                transition_table[(current, column)] = (
                    pair_index[(self_target, other_target)])
            current += 1
        accepting_states = frozenset(
            index for pair, index in pair_index.items()
            if pair[0] in self.accepting_states
            and pair[1] in other.accepting_states)
        return DFA(joint_variables, len(pair_order), 0,
                   transition_table, accepting_states)

    def existentially_projected(self,
                                variables_to_remove: set[str]) -> DFA:
        """Existential quantification: forget the named tracks.

        The removed tracks' bits become nondeterministic guesses, fixed
        by the subset construction. Padding closure first: a state is
        made accepting if an accepting state is reachable from it via
        columns that are zero on every surviving track (the removed
        tracks may need more bits than the surviving word carries).
        State bound after determinization: 2^|self|, a priori."""
        surviving_variables: tuple[str, ...] = tuple(
            name for name in self.variable_names
            if name not in variables_to_remove)
        zero_successors: dict[StateIndex, set[StateIndex]] = {
            state: set() for state in range(self.state_count)}
        for (state, column), target in self.transition_table.items():
            surviving_bits = _column_projection(
                column, self.variable_names, surviving_variables)
            if all(bit == 0 for bit in surviving_bits):
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
        nondeterministic_transitions: dict[
            tuple[StateIndex, BitColumn], set[StateIndex]] = {}
        for (state, column), target in self.transition_table.items():
            surviving_bits = _column_projection(
                column, self.variable_names, surviving_variables)
            nondeterministic_transitions.setdefault(
                (state, surviving_bits), set()).add(target)
        surviving_alphabet = list(cartesian_product(
            (0, 1), repeat=len(surviving_variables)))
        initial_subset: frozenset[StateIndex] = frozenset(
            [self.initial_state])
        subset_index: dict[frozenset[StateIndex], StateIndex] = {
            initial_subset: 0}
        subset_order: list[frozenset[StateIndex]] = [initial_subset]
        transition_table: TransitionTable = {}
        current: StateIndex = 0
        while current < len(subset_order):
            current_subset = subset_order[current]
            for column in surviving_alphabet:
                successor_subset = frozenset(
                    target for state in current_subset
                    for target in nondeterministic_transitions.get(
                        (state, column), ()))
                if not successor_subset:
                    continue
                if successor_subset not in subset_index:
                    subset_index[successor_subset] = len(subset_order)
                    subset_order.append(successor_subset)
                transition_table[(current, column)] = (
                    subset_index[successor_subset])
            current += 1
        accepting_states = frozenset(
            index for subset, index in subset_index.items()
            if subset & padding_closed_accepting)
        return DFA(surviving_variables, len(subset_order), 0,
                   transition_table, accepting_states)

    def minimized(self) -> DFA:
        """The canonical form: the unique minimal complete DFA
        (Myhill-Nerode), with states renamed in breadth-first order over
        sorted columns so that two canonical automata describe the same
        relation exactly when their fields are equal."""
        total: DFA = self.completed()
        sorted_alphabet = sorted(total.alphabet())
        reachable_states: set[StateIndex] = {total.initial_state}
        exploration_stack: list[StateIndex] = [total.initial_state]
        while exploration_stack:
            state = exploration_stack.pop()
            for column in sorted_alphabet:
                target = total.transition_table[(state, column)]
                if target not in reachable_states:
                    reachable_states.add(target)
                    exploration_stack.append(target)
        block_of: dict[StateIndex, int] = {
            state: int(state in total.accepting_states)
            for state in reachable_states}
        while True:
            signature_of: dict[StateIndex, tuple[int, ...]] = {
                state: (block_of[state],) + tuple(
                    block_of[total.transition_table[(state, column)]]
                    for column in sorted_alphabet)
                for state in reachable_states}
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
        canonical_name_of_block: dict[int, StateIndex] = {
            block_of[total.initial_state]: 0}
        block_order: list[int] = [block_of[total.initial_state]]
        canonical_transitions: TransitionTable = {}
        current: StateIndex = 0
        while current < len(block_order):
            block = block_order[current]
            representative = next(
                state for state in reachable_states
                if block_of[state] == block)
            for column in sorted_alphabet:
                target_block = block_of[
                    total.transition_table[(representative, column)]]
                if target_block not in canonical_name_of_block:
                    canonical_name_of_block[target_block] = (
                        len(block_order))
                    block_order.append(target_block)
                canonical_transitions[(current, column)] = (
                    canonical_name_of_block[target_block])
            current += 1
        canonical_accepting = frozenset(
            canonical_name_of_block[block_of[state]]
            for state in reachable_states
            if state in total.accepting_states)
        return DFA(total.variable_names, len(block_order), 0,
                   canonical_transitions, canonical_accepting)

    def describes_same_relation_as(self, other: DFA) -> bool:
        """Semantic equality by comparison of canonical forms -- the
        symbolic layer's 'reduce both and compare' test."""
        self_canonical: DFA = self.minimized()
        other_canonical: DFA = other.minimized()
        return (self_canonical.variable_names
                == other_canonical.variable_names
                and self_canonical.state_count
                == other_canonical.state_count
                and self_canonical.transition_table
                == other_canonical.transition_table
                and self_canonical.accepting_states
                == other_canonical.accepting_states)

    def is_empty(self) -> bool:
        """Does this automaton reject every tuple?"""
        visited_states: set[StateIndex] = {self.initial_state}
        exploration_stack: list[StateIndex] = [self.initial_state]
        while exploration_stack:
            state = exploration_stack.pop()
            if state in self.accepting_states:
                return False
            for column in self.alphabet():
                target = self.transition_table.get((state, column))
                if target is not None and target not in visited_states:
                    visited_states.add(target)
                    exploration_stack.append(target)
        return self.initial_state not in self.accepting_states

    def is_universal(self) -> bool:
        """Does this automaton accept every tuple? This is the
        'reduces to 0' verdict of the symbolic layer."""
        return self.complemented().is_empty()

    def entails(self, hypothesis: DFA) -> bool:
        """One-sided deduction: everything this relation (the knowledge)
        allows also satisfies the hypothesis. Decided by emptiness of
        knowledge intersected with the hypothesis's complement -- the
        KH ^ H test with the complement on the knowledge side's dual."""
        return self.intersected_with(
            hypothesis.complemented()).is_empty()

    def accepts_assignment(self,
                           assignment: VariableAssignment) -> bool:
        """Does this automaton accept the given values for its tracks?"""
        column_count: int = max(
            [value.bit_length() for value in assignment.values()]
            + [1]) + 1
        state: StateIndex | None = self.initial_state
        for bit_position in range(column_count):
            column: BitColumn = tuple(
                (assignment[name] >> bit_position) & 1
                for name in self.variable_names)
            state = self.transition_table.get((state, column))
            if state is None:
                return False
        return state in self.accepting_states


# ---------------------------------------------------------------------
# Base relation automata
# ---------------------------------------------------------------------

def _two_track_relation(
        input_variable: str,
        output_variable: str,
        table: dict[tuple[StateIndex, int, int], StateIndex],
        state_count: int,
        initial_state: StateIndex,
        accepting_states: frozenset[StateIndex]) -> DFA:
    """Build a 2-track DFA from (state, input_bit, output_bit) rows,
    aligning the letter order with the sorted track names."""
    variable_names: tuple[str, ...] = tuple(
        sorted((input_variable, output_variable)))
    tracks_are_flipped: bool = variable_names != (
        input_variable, output_variable)
    transition_table: TransitionTable = {}
    for (state, input_bit, output_bit), target in table.items():
        column: BitColumn = ((output_bit, input_bit)
                             if tracks_are_flipped
                             else (input_bit, output_bit))
        transition_table[(state, column)] = target
    return DFA(variable_names, state_count, initial_state,
               transition_table, accepting_states)


def _three_track_bitwise_relation(
        left_variable: str, right_variable: str, result_variable: str,
        result_bit_of) -> DFA:
    """One-state DFA for a bitwise law result = f(left, right)."""
    variable_names: tuple[str, ...] = tuple(
        sorted((left_variable, right_variable, result_variable)))
    position_of: dict[str, int] = {
        name: position for position, name in enumerate(variable_names)}
    transition_table: TransitionTable = {}
    for column in cartesian_product((0, 1), repeat=3):
        left_bit = column[position_of[left_variable]]
        right_bit = column[position_of[right_variable]]
        result_bit = column[position_of[result_variable]]
        if result_bit == result_bit_of(left_bit, right_bit):
            transition_table[(0, column)] = 0
    return DFA(variable_names, 1, 0, transition_table, frozenset({0}))


def relation_exclusive_or(left_variable: str, right_variable: str,
                          result_variable: str) -> DFA:
    """result = left ^ right (symmetric difference)."""
    return _three_track_bitwise_relation(
        left_variable, right_variable, result_variable,
        lambda left_bit, right_bit: left_bit ^ right_bit)


def relation_intersection(left_variable: str, right_variable: str,
                          result_variable: str) -> DFA:
    """result = left & right (set intersection)."""
    return _three_track_bitwise_relation(
        left_variable, right_variable, result_variable,
        lambda left_bit, right_bit: left_bit & right_bit)


def relation_addition(left_variable: str, right_variable: str,
                      result_variable: str) -> DFA:
    """result = left + right: the 2-state carry automaton -- the closed
    form of the stabilizing carry series (0002 Props 5/6)."""
    variable_names: tuple[str, ...] = tuple(
        sorted((left_variable, right_variable, result_variable)))
    position_of: dict[str, int] = {
        name: position for position, name in enumerate(variable_names)}
    transition_table: TransitionTable = {}
    for carry_bit in (0, 1):
        for column in cartesian_product((0, 1), repeat=3):
            left_bit = column[position_of[left_variable]]
            right_bit = column[position_of[right_variable]]
            result_bit = column[position_of[result_variable]]
            if result_bit == left_bit ^ right_bit ^ carry_bit:
                next_carry: StateIndex = (
                    (left_bit & right_bit) | (left_bit & carry_bit)
                    | (right_bit & carry_bit))
                transition_table[(carry_bit, column)] = next_carry
    return DFA(variable_names, 2, 0, transition_table, frozenset({0}))


def relation_shift_fill_zero(input_variable: str,
                             output_variable: str) -> DFA:
    """output = 2 * input (the corpus's n0/inc; 0002's a).
    State = the bit owed to the output track."""
    table: dict[tuple[StateIndex, int, int], StateIndex] = {}
    for owed_bit in (0, 1):
        for input_bit in (0, 1):
            table[(owed_bit, input_bit, owed_bit)] = input_bit
    return _two_track_relation(input_variable, output_variable, table,
                               2, 0, frozenset({0}))


def relation_shift_fill_one(input_variable: str,
                            output_variable: str) -> DFA:
    """output = 2 * input + 1 (the corpus's n1; 0002's b). The start
    state demands the output's low bit be 1, then behaves as
    shift-fill-zero."""
    start_state: StateIndex = 2
    table: dict[tuple[StateIndex, int, int], StateIndex] = {}
    for input_bit in (0, 1):
        table[(start_state, input_bit, 1)] = input_bit
        for owed_bit in (0, 1):
            table[(owed_bit, input_bit, owed_bit)] = input_bit
    return _two_track_relation(input_variable, output_variable, table,
                               3, start_state, frozenset({0}))


def relation_trailing_ones(input_variable: str,
                           output_variable: str) -> DFA:
    """output = T(input), the trailing-ones mask: 2 states (inside /
    outside the trailing-ones region) -- the closed form of the series
    x & b(x) & b(b(x)) & ... (0002 Prop 2; the corpus's $)."""
    inside_region: StateIndex = 1
    outside_region: StateIndex = 0
    table: dict[tuple[StateIndex, int, int], StateIndex] = {
        (inside_region, 1, 1): inside_region,
        (inside_region, 0, 0): outside_region,
        (outside_region, 0, 0): outside_region,
        (outside_region, 1, 0): outside_region,
    }
    return _two_track_relation(input_variable, output_variable, table,
                               2, inside_region, frozenset({0, 1}))


def relation_equality(input_variable: str,
                      output_variable: str) -> DFA:
    """output = input."""
    table: dict[tuple[StateIndex, int, int], StateIndex] = {
        (0, 0, 0): 0, (0, 1, 1): 0}
    return _two_track_relation(input_variable, output_variable, table,
                               1, 0, frozenset({0}))


def relation_constant(variable_name: str, constant_value: int) -> DFA:
    """variable = constant. States count matched bit positions; state i
    is accepting exactly when no 1-bits of the constant remain above."""
    bit_length: int = max(constant_value.bit_length(), 1)
    transition_table: TransitionTable = {}
    for bit_position in range(bit_length):
        expected_bit: int = (constant_value >> bit_position) & 1
        transition_table[(bit_position, (expected_bit,))] = (
            bit_position + 1)
    transition_table[(bit_length, (0,))] = bit_length
    accepting_states = frozenset(
        bit_position for bit_position in range(bit_length + 1)
        if constant_value >> bit_position == 0)
    return DFA((variable_name,), bit_length + 1, 0, transition_table,
               accepting_states)


# ---------------------------------------------------------------------
# Terms and their compilation
# ---------------------------------------------------------------------

INTERNAL_VARIABLE_PREFIX: str = "_"


def is_internal_variable(variable_name: str) -> bool:
    return variable_name.startswith(INTERNAL_VARIABLE_PREFIX)


class FreshVariableSource:
    """Supplies internal track names, one per compiled term node."""

    def __init__(self) -> None:
        self.next_index: int = 0

    def fresh_variable_name(self) -> str:
        self.next_index += 1
        return f"{INTERNAL_VARIABLE_PREFIX}{self.next_index}"


class CompiledRelation:
    """The result of compiling a term: an automaton relating the term's
    free variables to a result track."""

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
        away the operands' internal result tracks (eager projection
        keeps the track count small at every step)."""
        combined: DFA = base_relation
        for operand_relation in operand_relations:
            combined = combined.intersected_with(
                operand_relation.automaton)
        internal_tracks: set[str] = {
            operand_relation.result_variable_name
            for operand_relation in operand_relations
            if is_internal_variable(
                operand_relation.result_variable_name)}
        if internal_tracks:
            combined = combined.existentially_projected(internal_tracks)
        return CompiledRelation(combined.minimized(),
                                result_variable_name)


class Variable(Term):
    def __init__(self, variable_name: str) -> None:
        self.variable_name: str = variable_name

    def compiled(self,
                 fresh_source: FreshVariableSource) -> CompiledRelation:
        unconstrained = DFA(
            (self.variable_name,), 1, 0,
            {(0, (0,)): 0, (0, (1,)): 0}, frozenset({0}))
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
    relation on the two result tracks with internals projected away."""
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
    internal_tracks: set[str] = {
        name for name in (left_relation.result_variable_name,
                          right_relation.result_variable_name)
        if is_internal_variable(name)}
    if internal_tracks:
        combined = combined.existentially_projected(internal_tracks)
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

    print("all checks passed")


if __name__ == "__main__":
    run_verification_suite()
