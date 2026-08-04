Prove that AND, OR, and NOT are functionally complete.

If they are not FC, by definition there is some f(a, b, c, ...) that cannot be expressed as compose(AND, OR, NOT)(a, b, c, ...)

There can be no function that commutes with each of AND, OR, NOT but not f, because compositions inherit commutativity

# Case study
I want to check what functions commute with AND and OR, then check what functions AND and OR can compose to.

Everything must commute with [0], [1], and I because these are all the identity

AND commutes with F, T, AND
OR commutes with F, T, OR
So limitation is targets MUST commute with {T, F}

IMPL commutes with T
CONV commutes with T
NAND commutes with none
NOR commutes with none
XOR commutes with XOR, F
NXOR commutes with NXOR, T
NCONV commutes with F
NIMPL commutes with F


## So if I'm right...
Then AND and OR can compose to none of the above?
IMPL should* compose to NXOR and CONV
IMPL should not compose to NCONV, NIMPL
XOR and NXOR should* be FC

\* for now, should is "maybe can" because I don't have a way to prove that _nothing_ tests a function, only a way to prove _something_ tests a function (by example)

CONV(p, q) ?= IMPL(q, IMPL(p, q))      # verified in Python

## These don't check...
The original theorem (Post's) requires that 5 categories be satisfied by the set of functions - non-true-preserving, non-false-preserving, non-monotonic, non-self-dual, non-linear (non-"counting"). The first few functions (F, T, NOT) correspond to 3 of these categories and one of the categories is redundant (monotonic) in a 2 valued logic. The only uncovered category by these first few checks, then, is non-linear functions.

So what does the internal structure of a linear function mean about what tests it?

Let's try a few examples
```
f(a,b,c) = (a+b+c+1) % 2    checked by NOT, NOT(x[0]), NOT(x[1]), NOT(x[2]), x[1], x[0], x[2], sum(1 + any 3 of x) | len(x) in {3,4}, 

f(a,b) = (a+b+1) % 2 checked by 1, NXOR (itself), sum(x) % 2 | len(x) in {3}
```

In 2 dimensions, you have either an even or odd number of considered indices for linear functions. All linear functions are of the form sum(x + (1 or 0)) % 2.
- If a function has an even number of considered indices, it must be either true preserving or false preserving since sum(x) % 2 is always 0 for all 0s or all 1s as input.
- If a function has an odd number of considered indices, it must be self-dual because sum(x) must have opposite parity of sum(not x).
- So linear functions in 2 valued logic are in a sense also redundant
    - Except the theorem says _not_ in any of the groups, so it's conceivable you have 2 different linear functions, one of which is self-dual and one of which is true-preserving, but are still not FC because they preserve linearity
    - It's also possible to have a true-preserving function that's nonlinear obviously
    - The argument that self-dual functions are always either true or false preserving and therefore not necessary to check hits a similar issue actually - we can have two self-dual functions, one true-preserving and one false-preserving, which are not FC because they still preserve self-duality

### Does it make sense...
There seems to be this tendency for linear functions to test linear functions. What linear functions test which? What's the pattern and can I define multiple kinds of linear function that differentiate between the NOT kind of linearity and other kinds?

# IDK random stuff
Commuting with self might be related to some symmetry in the operands

# For next time

Function commutativity is easy to visualize for functions of 2 inputs, but harder to visualize for more. One way to build a visualization would be to consider the array of inputs to one function mapped to the integers as one axis, then the array of inputs to the second function as the second axis, with the output in a third axis. Questions that need to be answered:
- What does functional commutativity look like here?
- Is there a natural way to go from the 2d graph of each of f and g to the 3d graph of f compose g (g compose f)

