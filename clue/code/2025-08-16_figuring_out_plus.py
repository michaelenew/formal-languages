
import itertools
from models.Statement import Statement, Symbol

a = Symbol('A', True).statement()
b = Symbol('B', True).statement()
c = Symbol('C', True).statement()

# This expression returns 1 if the popcount of a, b, c is 2 or 3 and 0 if the popcount is 0 or 1
# This is equivalent to the second least significant figure in the SUM of a, b, c
true = Statement() | (a&b) | (a&c) | (b&c)

# I'm having the computer figure out the actual form of the second LSF because I'm lazy
print('Seconds lsf, 3 symbols')
print('Term lengths:', sorted({len(term) for term in true.terms}))
print(true)
print()



d = Symbol('D', True).statement()
e = Symbol('E', True).statement()
f = Symbol('F', True).statement()

symbols = [a, b, c, d, e, f]
true = Statement()

# True if any 2 or 3 are true
for i, symbol1 in enumerate(symbols):
    for j, symbol2 in enumerate(symbols[i+1:], start = i+1):
        true = true | (symbol1 & symbol2)
        for k, symbol3 in enumerate(symbols[j+1:], start = j+1):
            true = true | (symbol1 & symbol2 & symbol3)

# But not if any 4 or 5 are true
for i, symbol1 in enumerate(symbols):
    for j, symbol2 in enumerate(symbols[i+1:], start = i+1):
        for k, symbol3 in enumerate(symbols[j+1:], start = j+1):
            for l, symbol4 in enumerate(symbols[k+1:], start = k+1):
                true = true & (Statement.full() ^ (symbol1 & symbol2 & symbol3 & symbol4))
                for m, symbol5 in enumerate(symbols[l+1:], start = l+1):
                    true = true & (Statement.full() ^ (symbol1 & symbol2 & symbol3 & symbol4 & symbol5))

# But yes if any 6 or 7 are true
for i, symbol1 in enumerate(symbols):
    for j, symbol2 in enumerate(symbols[i+1:], start = i+1):
        for k, symbol3 in enumerate(symbols[j+1:], start = j+1):
            for l, symbol4 in enumerate(symbols[k+1:], start = k+1):
                for m, symbol5 in enumerate(symbols[l+1:], start = l+1):
                    for n, symbol6 in enumerate(symbols[m+1:], start = m+1):
                        true = true | (symbol1 & symbol2 & symbol3 & symbol4 & symbol5 & symbol6)
                        for o, symbol7 in enumerate(symbols[n+1:], start = n+1):
                            true = true | (symbol1 & symbol2 & symbol3 & symbol4 & symbol5 & symbol6 & symbol7)


print(f'Second lsf, {len(symbols)} symbols')
print('Term lengths:', sorted({len(term) for term in true.terms}))
print(true)
print()





g = Symbol('G', True).statement()
h = Symbol('H', True).statement()
i = Symbol('I', True).statement()

symbols = [a, b, c, d, e, f, g, h, i]
true = Statement()

# True if any 2 or 3 are true
for i, symbol1 in enumerate(symbols):
    for j, symbol2 in enumerate(symbols[i+1:], start = i+1):
        true = true | (symbol1 & symbol2)
        for k, symbol3 in enumerate(symbols[j+1:], start = j+1):
            true = true | (symbol1 & symbol2 & symbol3)

# But not if any 4 or 5 are true
for i, symbol1 in enumerate(symbols):
    for j, symbol2 in enumerate(symbols[i+1:], start = i+1):
        for k, symbol3 in enumerate(symbols[j+1:], start = j+1):
            for l, symbol4 in enumerate(symbols[k+1:], start = k+1):
                true = true & (Statement.full() ^ (symbol1 & symbol2 & symbol3 & symbol4))
                for m, symbol5 in enumerate(symbols[l+1:], start = l+1):
                    true = true & (Statement.full() ^ (symbol1 & symbol2 & symbol3 & symbol4 & symbol5))

# But yes if any 6 or 7 are true
for i, symbol1 in enumerate(symbols):
    for j, symbol2 in enumerate(symbols[i+1:], start = i+1):
        for k, symbol3 in enumerate(symbols[j+1:], start = j+1):
            for l, symbol4 in enumerate(symbols[k+1:], start = k+1):
                for m, symbol5 in enumerate(symbols[l+1:], start = l+1):
                    for n, symbol6 in enumerate(symbols[m+1:], start = m+1):
                        true = true | (symbol1 & symbol2 & symbol3 & symbol4 & symbol5 & symbol6)
                        for o, symbol7 in enumerate(symbols[n+1:], start = n+1):
                            true = true | (symbol1 & symbol2 & symbol3 & symbol4 & symbol5 & symbol6 & symbol7)

# But no if any 8 or 9 are true
for i, symbol1 in enumerate(symbols):
    for j, symbol2 in enumerate(symbols[i+1:], start = i+1):
        for k, symbol3 in enumerate(symbols[j+1:], start = j+1):
            for l, symbol4 in enumerate(symbols[k+1:], start = k+1):
                for m, symbol5 in enumerate(symbols[l+1:], start = l+1):
                    for n, symbol6 in enumerate(symbols[m+1:], start = m+1):
                        for o, symbol7 in enumerate(symbols[n+1:], start = n+1):
                            for p, symbol8 in enumerate(symbols[o+1:], start = o+1):
                                true = true & (Statement.full() ^ (symbol1 & symbol2 & symbol3 & symbol4 & symbol5 & symbol6 & symbol7 & symbol8))
                                for q, symbol9 in enumerate(symbols[p+1:], start = p+1):
                                    true = true & (Statement.full() ^ (symbol1 & symbol2 & symbol3 & symbol4 & symbol5 & symbol6 & symbol7 & symbol8 & symbol9))


print(f'Second lsf, {len(symbols)} symbols')
print('Term lengths:', sorted({len(term) for term in true.terms}))
print(true)
print()





### Third LSF

true = Statement()

# True if any 4, 5, 6, or 7 are true
for i, symbol1 in enumerate(symbols):
    for j, symbol2 in enumerate(symbols[i+1:], start = i+1):
        for k, symbol3 in enumerate(symbols[j+1:], start = j+1):
            for l, symbol4 in enumerate(symbols[k+1:], start = k+1):
                true = true | (symbol1 & symbol2 & symbol3 & symbol4)
                for m, symbol5 in enumerate(symbols[l+1:], start = l+1):
                    true = true | (symbol1 & symbol2 & symbol3 & symbol4 & symbol5)
                    for n, symbol6 in enumerate(symbols[m+1:], start = m+1):
                        true = true | (symbol1 & symbol2 & symbol3 & symbol4 & symbol5 & symbol6)
                        for o, symbol7 in enumerate(symbols[n+1:], start = n+1):
                            true = true | (symbol1 & symbol2 & symbol3 & symbol4 & symbol5 & symbol6 & symbol7)

# But no if any 8 or 9 are true
for i, symbol1 in enumerate(symbols):
    for j, symbol2 in enumerate(symbols[i+1:], start = i+1):
        for k, symbol3 in enumerate(symbols[j+1:], start = j+1):
            for l, symbol4 in enumerate(symbols[k+1:], start = k+1):
                for m, symbol5 in enumerate(symbols[l+1:], start = l+1):
                    for n, symbol6 in enumerate(symbols[m+1:], start = m+1):
                        for o, symbol7 in enumerate(symbols[n+1:], start = n+1):
                            for p, symbol8 in enumerate(symbols[o+1:], start = o+1):
                                true = true & (Statement.full() ^ (symbol1 & symbol2 & symbol3 & symbol4 & symbol5 & symbol6 & symbol7 & symbol8))
                                for q, symbol9 in enumerate(symbols[p+1:], start = p+1):
                                    true = true & (Statement.full() ^ (symbol1 & symbol2 & symbol3 & symbol4 & symbol5 & symbol6 & symbol7 & symbol8 & symbol9))


print(f'Third lsf, {len(symbols)} symbols')
print('Term lengths:', sorted({len(term) for term in true.terms}))
print(true)
print()




def every(num: int, elements: list[Statement]) -> Statement:
    all_terms = Statement.empty()
    for combo in itertools.combinations(elements, num):
        this_term = Statement.full()
        for elem in combo:
            this_term = this_term & elem
        all_terms = all_terms ^ this_term
    return all_terms

addition_grid: list[list[Statement]] = list()

for i in range(7):
    column: list[Statement] = list()
    a = Symbol(f'a{i}').statement()
    b = Symbol(f'b{i}').statement()
    column.append(a)
    column.append(b)

    for j, prior_column in enumerate(addition_grid[::-1]):
        every_num = 2 ** (j+1)
        column.append(every(every_num, prior_column))

    addition_grid.append(column)

print('Addition grid last term')
for elem in addition_grid[-1]:
    print()
    print('Term lengths:', sorted({len(term) for term in elem.terms}))
    print(str(elem))




### So at some point in the past I realized that it's NEVER POSSIBLE to have carry at more than 1 place ahead.
### This is because it requires at least 4 elements to get out to 2 places ahead, but we only ever have a max
### of 3 values in any prior column.

### This elates and devastates me. Anyway, at least we've come to it from a practical perspective so there's
### little chance of error.




### Now let's figure out what the terms actually are. Seems likely it's just the union of all prior symbols.
# last_carry = addition_grid[-1][2]
# symbols = {symbol for term in last_carry.terms for symbol in term}
# union_of_all = Statement.empty()
# for symbol in symbols:
#     union_of_all = union_of_all | symbol.statement()

# print(union_of_all)
# print(last_carry)
# print(union_of_all == last_carry)


### Lol not even close.

# carry[n] =
#    a[n-1] & b[n-1]
#    ^ (a[n-1] ^ b[n-1]) & carry[n-1]

# =
#    a[n-1] & b[n-1]
#    ^ (a[n-1] ^ b[n-1]) & (
#           a[n-2] & b[n-2]
#           ^ (a[n-2] ^ b[n-2]) & carry[n-2]
#      )


