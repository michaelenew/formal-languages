from __future__ import annotations


class Symbol:
    def __init__(self, symbol: str, is_elementary: bool = None):
        if is_elementary is None:
            is_elementary = symbol == symbol.upper()
        self.symbol = symbol.upper() if is_elementary else symbol.lower()
        self.is_elementary = is_elementary

    def __str__(self) -> str:
        return self.symbol
    
    def __hash__(self):
        return hash(self.symbol)

    def __eq__(self, other: Symbol):
        return str(self) == str(other)
    
    def __xor__(self, other: Symbol | Statement) -> Statement:
        if type(other) is Symbol:
            other = other.statement()
        return self.statement() ^ other

    def __and__(self, other: Symbol | Statement) -> Statement:
        if type(other) is Symbol:
            other = other.statement()
        return self.statement() & other

    def __or__(self, other: Symbol | Statement) -> Statement:
        if type(other) is Symbol:
            other = other.statement()
        return self.statement() | other

    def __rxor__(self, other: Symbol | Statement) -> Statement:
        return self ^ other

    def __rand__(self, other: Symbol | Statement) -> Statement:
        return self & other

    def __ror__(self, other: Symbol | Statement) -> Statement:
        return self | other

    def statement(self) -> Statement:
        return Statement(frozenset({
            frozenset({self}),
        }))
    
    @classmethod
    def element(cls, symbol: str) -> Symbol:
        return cls(symbol, True)



class Statement:
    def __init__(self, terms: frozenset[frozenset[Symbol]] = frozenset()):
        self.terms = terms

    def __hash__(self):
        return hash(self.terms)
    
    def __eq__(self, other: Statement):
        return self.terms == other.terms

    def symbols(self) -> frozenset[Symbol]:
        return frozenset(
            sym
            for term in self.terms
            for sym in term
        )

    def elementary_universe(self) -> Statement:
        '''
        Returns the union of every element in the statement
        '''
        universe_set = Statement.empty()
        for symbol in self.symbols():
            if symbol.is_elementary:
                universe_set |= symbol.statement()
        return universe_set

    def symbolic_universe(self) -> Statement:
        '''
        Returns the union of every symbol in the statement
        '''
        universe_set = Statement.empty()
        for symbol in self.symbols():
            universe_set |= symbol.statement()
        return universe_set

    def __eq__(self, other: Statement) -> bool:
        return self.terms == other.terms

    def __xor__(self, other: Statement) -> Statement:
        return Statement(self.terms.union(other.terms) - self.terms.intersection(other.terms))

    def __and__(self, other: Statement) -> Statement:
        terms = set()
        for self_term in self.terms:
            for other_term in other.terms:
                term = self_term.union(other_term)
                if term in terms:
                    terms.remove(term)
                else:
                    terms.add(term)
        return Statement(terms)

    def __or__(self, other: Statement) -> Statement:
        return self ^ other ^ self & other

    def __str__(self) -> str:
        return ' ^ '.join(sorted(
            '&'.join(sorted(map(str, term))) or '1'
            for term in self.terms
        ))

    @classmethod
    def empty(cls) -> Statement:
        return Statement(frozenset())
    
    @classmethod
    def full(cls) -> Statement:
        return Statement(frozenset({frozenset({})}))

    @classmethod
    def symbolic(self, symbol: Symbol) -> Statement:
        return symbol.statement()

    def with_symbol(self, symbol: Symbol) -> Statement:
        if symbol.is_elementary:
            # elements are disjoint from every other element
            return self | (symbol.statement() & self.elementary_universe())
        return self

    def meta(self) -> Statement:
        # meta symbols are always elementary
        return Symbol('{' + str(self) + '}', True)

    @staticmethod
    def test():
        a = Symbol('a').statement()
        b = Symbol('b').statement()

        assert (a ^ a).terms == frozenset()

        assert (a ^ b ^ a).terms == frozenset({
            frozenset({Symbol('b')}),
        })

        assert (a ^ b).terms == frozenset({
            frozenset({Symbol('a')}),
            frozenset({Symbol('b')}),
        })

        assert (a & b).terms == frozenset({
            frozenset({Symbol('a'), Symbol('b')}),
        })

        assert (a ^ b ^ (a & b)).terms == frozenset({
            frozenset({Symbol('a')}),
            frozenset({Symbol('b')}),
            frozenset({Symbol('a'), Symbol('b')})
        })

        # Check operator precedence
        assert a ^ b ^ (a & b) == a ^ b ^ a & b
        assert a ^ b ^ (a & b) == a & b ^ a ^ b

        # Checking distributivity
        assert ((a ^ b ^ a&b) & a).terms == frozenset({
            frozenset({Symbol('a')}),
        })

        assert ((a ^ b ^ a&b) & (a & b)).terms == frozenset({
            frozenset({Symbol('a'), Symbol('b')}),
        })

        assert ((a ^ b ^ a&b) & (a ^ b)).terms == frozenset({
            frozenset({Symbol('a')}),
            frozenset({Symbol('b')}),
        })


if __name__ == '__main__':
    Statement.test()
