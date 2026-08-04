https://www.sfu.ca/~jeffpell/papers/PostPellMartin.pdf

Rough outline:

Define several classes of truth function:
- Those which preserve uniform inputs (e.g. f,f,f,f -> f)
- Those which can be expressed as f(**x**) = ((0|1)+x1+x2+...) mod 2
- Those for which **x** >= **y** implies f(**x**) >= f(**y**)
    - Here, >= is defined as all(xi >= yi for xi, yi in zip(**x**, **y**)) where T > F
    - Note that this definition can be reversed as well, leading to a concept of "equality" wherein **x** and **y** are "equal" when **x** >= **y** and **x** <= **y**
- Those for which f(**x**) = -f(-**x**) where - is element-wise negation

The crux is twofold:

First, any combination involving functions lacking each property can be used to construct a known set of functionally complete operators. Thus it is sufficient to have one operator lacking each property.

Second, that any composition wherein all elementary functions have property X must also exhibit property X. Furthermore, there is a truth table each which lacks each property above (but does not lack the others). Thus it is necessary to have one operator lacking each property.

Funny: with 2 truth values, "monotonic" is always either true preserving or false preserving

_____

Four classes that extend:
- uniform preserving -> (a,a,a,a) -> a
- linear -> (a x1 + b x2 + ...) mod dim
- monotonic -> **x** >= **y** implies f(**x**) >= f(**y**)
    - Do we just use 0 < 1 < 2 < ... or do we need to include all arrangements?
- Self-dual -> f(**x**) = -f(-**x**)
    - Need a concept of negation; probably use x -> (x+dim/2) mod dim

Don't need to sweat the details of each choice above, just try to prove sufficiency of any one combination and then pare down until we can show necessity

# Extension

N valued logic of functions is a subset of N valued collections of sets in the sense that only certain input schemes apply to set logic. Basically if part of the input of A is 1, then all of A is 1. Thus if an operator collection is functionally complete for N valued logic functions, it is maximally expressive on sets.

Note that maximally expressive actually also implies functional completeness. We can always "pare down" With a maximally expressive operator collection to the units then build back up to form any set at all that we want.



On extending

Abstraction of self-dual and identities:

Take any unary operator z
The property of f that f(z(x1), z(x2), ...) = z(f(x1, x2, ...)) must extend to any composition of f (or other methods having this property)

The 1 ident function is where z(x)=1
The 0 ident is z(x)=0
The self dual is z(x)=-x

2d version?
z(f(x1, x2, ...), f(y1, y2, ...)) = f(z(x1, y1), z(x2, y2), ...)
Can this account for linear or monotonic?

Classes of function that should propagate upward:
Identity preserving
Exclusionary
Linears

syntax for implied comprehension:
```
f([t(y[i,:]) for i in dim(f)]) := f(t(y[,:]))
f([t(y[:,i]) for i in dim(f)]) := f(t(y[:,]))
```

define testing functions:
```
f is a function
f:(x:[N])->x[1]

and t is a test we want to apply
t:(x:[M])->x[1]

Then f satisfies t if for every y:x[M,N]
    f(t(y[,:])) == t(f(y[:,]))
```

Note that "f satisfies t" implies "t satisfies f" by symmetry

visualization:
```
t > _  _  _  _  _  _  |  X
----------------------|-----
t > _  _  _  _  _  _  |  _
t > _  _  _  _  _  _  |  _
t > _  _  _  _  _  _  |  _
t > _  _  _  _  _  _  |  _
    ^  ^  ^  ^  ^  ^  |  ^
    f  f  f  f  f  f     f
```
Put any values in the main rectangle, then apply the functions along the axis indicated. If both methods give you the same result no matter what you pick, then f satisfies t <-> t satisfies f

Example:  `t:(x[0])->x[1]`  function test is the same as "constant input gives same output"
```
test becomes:
f([t(), t(), t(), ...]) == t()
so every input is obviously the same as every output
```

Observation: every function satisfies the identity (member of `(x[1])->x[1]`)

For any set of functions f1, f2, f3..., if all satisfy t, their composition also satisfies t:
```
f([fi([a,b,c]), fj([d]), fk([e,g]), h, i, ...])

rewrite any constants as the identity, which as noted is guaranteed to satisfy t:

f([fi([a,b,c]), fj([d]), fk([e,g]), I(h), I(i), ...])

now the question is whether

f'([a,b,c,d,...]) := f([f1([a,b,c]), f2([d]), f3([e,g]), I(h), I(i), ...])

also necessarily satisfies t.

so for any x:[3,dim(t)], f1(t(x[,:])) == t(f1(x[:,]))

observation: every contiguous 

visualization from before:

t > _  _  _  _  _  _  |  Z
----------------------|-----
t > _  _  _  _  _  _  |  _   - a
t > _  _  _  _  _  _  |  _   - b
t > _  _  _  _  _  _  |  _   - c  _Y1_ here and above are params of f1

t > _  _  _  _  _  _  |  _   - d  _Y2_ params of f2

t > _  _  _  _  _  _  |  _   - e
t > _  _  _  _  _  _  |  _   - g  _Y3_ params of f3

t > _  _  _  _  _  _  |  _   - h  _Y4_ params of firtst I

    ^  ^  ^  ^  ^  ^  |  ^
    f  f  f  f  f  f     f

now t hasn't changed at all, and I know that there exists a function (which is f1) that makes those top 3 rows consistent.
in the smaller table, X1 = t(f1(x1[,:])) = f1(t(x1[:,]))

Take some bunch of tables which satisfies t. Calculate their "Z" values. These "Z" values are then the values of t(fi(xi[:,])) = fi(t(xi[,:])) which we can input to f to retrieve the original function. Therefore, X = f([Y1, Y2, ...]). By definition, this is also equal to f'([a, b, c, ...])

Y1 = f1(t(X1[,:])) = t(f1(X1[:,]))
Y2 = f2(t(X2[,:])) = t(f1(X2[:,]))
...

X = [X1, X2, ...]
Y = [t(X1), t(X2), ...]
  = t(X[,:])

x = [a, b, c, ...]
y = [t(a), t(b), ...]
  = t(x[:,])

x = [*x1, ...]
Y = [f1(t(x1[:,])), f2(t(x2[:,])), ...]
  = [t(f1(x1[,:])), t(f2(x2[,:])), ...]
  = t([f1(x1[,:]), f2(x2[,:]), ...])
  = t([])
by the definition:
    t(f1(x1[,:])) = t(X1)


by definition, f(X) = f'(x)

All that logic is summed up in the following algebra with definitions x := [a,b,c,...] and X := [f1([a,b,c]), ...] = [Y1, Y2, ...]

f' is chosen such that

Z   = f'(t(x[,:]))

and by the fact that f satisfies t

Z   = f(Y)
    = f(t(X[,:]))             # this is "f(right column of original matrix)"
    = t(f(X[:,]))             # this is "t(top row of original matrix)"
    = t(f'(x[:,]))            # this is "t(top row of exploded matrix)"

for sure: just because f satisfies t doesn't mean f' has the property in the presence of random f1, f2, ...
    e.g. f 

why does this proof only work for if fi satisfy t?
try for const false fi, const true t:
    f satisfies t if (true, true, ...) -> true
    every other input is free
    1 -> fine, X can have lots of values. Right col is const true. equals true
    2 -> not fine, this is now false.


like this?
    let f = f1(f2(a,b,c), d, f3(f4(e)), ...)
        where each of a, b, c, ... are arrays of dim(t) values
    where fi all satisfy t
    then t(f)
        = t(f1(f2(a,b,c), d, f3(f4(e)), ...))
        = f1(t(f2(a,b,c)), t(d), t(f3(f4(e))), ...)
        = f1(f2(t(a), t(b), t(c)), t(d), f3(t(f4(e))), ...)
        = f1(f2(t(a), t(b), t(c)), t(d), f3(f4(t(e))), ...)

    therefore applying t to each input parameter yields the same result as applying t to f directly

by induction for a test t:
    the identity function satisfies every function, therefore satisfies t
    call depth of embedding starting at the outermost function call and
        increasing by 1 for each step deeper into the call stack
    then for a function f at depth N which satisfies t
        and with composed functions fi
        invocation can be written f(f1(...), f2(...), ...)
    then if f satisfies t:
        t(f(f1(...), f2(...), ...))
        = f(t(f1(...)), t(f2(...)), ...)
    thus if f satisfies t, the expression with t at depth of embedding N
        can be rewritten to have t at depth of embedding N+1 and vice versa
    basically:
        - assuming all composed functions satisfy t, any invocation
            with t at depth N has an equivalent form with t at depth
            N+1
        - if all parameters at depth 0 (i.e. inputs) have t applied to them,
            then the depth of embedding of t can be made arbitrarily high,
            in particular it can be made equal to the depth of embedding
            of the parameters
        - since "depth of embedding equal to the depth of parameters" indicates
            that each parameter is individually wrapped in t, and since this is
            and equivalent form to t wrapping the outermost call, this proves that
            any function composed entirely of constituents satisfying t must
            also satisfy t

```

Observations:
- If t is exlusionary, any function satisfying t must be exlusionary
- If t is linear, there are definitely functions satisfying it that are linear
- If t is preservative, any function satisfying t must be preservative (make x all one value to see why)
- If f is monotonic, there are tests it satisfies that are also monotonic
- Preservative has a minimal dimension that we care about - 0 in this case

Question: what is it about a test that precludes functional completeness?
If the test is not functionally complete in isolation, is it possible for a composition of fs satisfying it to be functionally complete?

Observation: if t is functionally complete, every possible arrangement of dim(t) must appear in the right column (but this is also true if t is non exclusionary)

And if f satisfies t, f(t(x)) = t(f(x))

What about exploding a function g(x)=f(t(x)) with dim(g) = dim(f) * dim(t). Seems like if g is complete, f and t are both complete?

If g is complete I can choose any random x and Z, then make a map between them

Also, if g is a composition of f and t, g satisfies both f and t



Where I'm at: If some collection of fs satisfies any one t, any composition of those fs will also satisfy t. This means that if satisfying t precludes any truth table at all, the collection of fs is not functionally complete.
So: pick a truth table, ask yourself if satisfying t precludes that table (is this the same as that table \[not] satisfying t?). If so, and all your functions satisfy t, your fs are not complete.
Question: what is the indicator that t precludes any particular table?
    in the case of "false" - a "candidate" table is precluded if it has "true" as its f,f,f,f... row
    but this is the same thing as "not satisfying false"
    so if all fs satisfy false, and false fails to satisfy any particular table in the infinite world of possible tables, then the fs cannot possibly be complete?
    In summary: satisfying t precludes "reaching" any function t does not satisfy?
        rephrased: if fs all satisfy t, everything fs can construct through composition must also satisfy t
hypothesis: no single t except the identity satisfies every function
    maybe proof: nothing can satisfy both "false" and "not"?
if that's true:
    a solo complete function must not satisfy anything but the identity
funny observation: this is consistent with the trivial statement "f can always compose to form f" because f satisfying t implies t satisfies f

Observation: each test has a set of functions it matches. Each f then can only reach the intersection of its satisfied tests' matched functions. A collection of fs is complete when the intersection of "cannot reach" Is empty. This implies that two functions' collective span is never more than the union of their individual spans.

Question: how can I tell when a particular function satisfies no tests in finite time?
Maybe there's a finite subset of tests? "If f satisfies this basic t, it can't possibly satisfy all these other ts"
Maybe only have to check tests up to dim(f)?
Note that tests corresponding to posts original true preserving (true), false preserving (false), and self dual (not) are all linear in their minimal dimension. Maybe we only have to check the linear tests?

Question: what's the relationship between intertibility and linearity? In ordinary logic, xor and nxor are the only two invertible functions and the only two full rank linear functions.
Seems reasonably clear that a linear function all of whose coeffs (except the constant) are mutually prime with the number of truth values is invertible
A tractable rephrasing of invertible would be that every result appears holding all but one index constant and cycling through all values on that one index.
  Basically, pick any combo of inputs for all but one index. Then check if all truth values appear in the free index and the result. Iff for every free index and combo of inputs this holds true, f is invertible.
  This also shows that linearity is not necessary for invertibility in higher dimensions. Basically pick one of the fixed indices and pick any 3 truth values for that fixed index. For linearity to hold, the result values would need to be on the same cycle in the free index (linearity induces cycling in this way), but we can satisfy the above without that being true.
  In fact, this makes it seem like it's only "polynomial" functions of degree less than the number of truth values that are invertible (assuming every cycle is achievable via a polynomial on mod # of truth values) (there are (num truth values-1)! Cycles and order of (num truth values)^(num truth values) polynomials, so this seems plausible)




Question: if f is part of a collection of functions and f satisfies t, can including t in the "mix" of functions possibly increase the functional range of the set of functions?
Or vice versa - must it increase the functional range? (no, this would imply no function can match itself, which is not true)



Question: if f satisfies any t (excluding identity?), does that imply that f satisfies f?



Question: if f satisfies t, does that imply that f is composable from t? Definitely not - consider true / false tests - these can't possibly compose to higher dimensions but match a fair number of complex fs
However, I might be able to construct a



Question: How many degrees of freedom does a particular function have?
e.g. "true" has 0 even if it has a bunch of params - f(a,b,c,...) -> 1 you can close your eyes and tell me what f is
dummy indices can obviously be removed
can I "split" a single "full rank" index into two indices?
e.g.
```
0 | 0
1 | 1
```
can I then split to
```
0 0 | 0
0 1 | 1
1 0 | 0
1 1 | 1
```
"I give you the first param, can you exclude any outputs?"



Question: does f always satisfy f?
f(f(x)) = f(f(x))
Except one f is vertical and one is horizontal so it's more like f(f(x)^T) ?= f(f(x^T)^T)
Ie collapse index 1 then 2 ?= collapse index 2 then 1
Note: can add a ^T outside either without modifying meaning
f satisfies I and I satisfies f
And obviously I(f(x)) = I(f(x)^T)^T = f(I(x^T)^T) for x being dim(f) x 1
Answer: no, by counterexample (python script)

Question: under what circumstances does f satisfy f?


Next question:

question: if f and g both satisfy t, does f satisfy g?
```
f(t(y[,:])) == t(f(y[:,])) for random y:[]
g(t(z[,:])) == t(g(z[:,])) for random z

f(g(x[,:])) ?= g(f(x[:,])) for random x[dim()]

answer: no, by counterexample ()->1, ()->0, (x)->x
```



# Fresh thoughts
In Post's original proof, he lays out 5 classes of function.
True preserving and false preserving are both tested by the linear () -> 0 and () -> 1 resp.
    These tests are both linear in 0 dimensions
Self-dual is tested by (x) -> ~x
    This test linear in 1 dimension
    The only other non-trivial test in dimension is the identity: (x) -> x
Monotonic are always (with 2 truth values) true-preserving or false-preserving (or both).

This leaves linear. Hypothesis is that linear functions are always tested by linear functions
    and by example, it seems that they are tested in particular by those with the same offset
    this would imply that dissatisfying every non-identity linear test is sufficient
    and seems pretty obviously true. If f is linear, the right column of f test f will have each main block value times coeffs\[col_ind]. Then on the second phase, that value gets multiplied again by coeffs\[row_ind], so we end up with coeffs\[col_ind] * coeffs\[row_ind] * val. Then going the other way, it's obvious we end up with the same expression.

So for 2 valued logic, at least, we have the much simpler phrasing of the test:
"a set of functions is complete if it dissatisfies every linear test at least once"
and, for a solitary function, it is sufficient to check true, false, not, and itself.




Illustrative question: what truth tables does satisfying t PRECLUDE?
- Similar line of reasoning to posts original proof
- Answer is anything t doesn't satisfy
- Good example are the preservatives
    - F satisfies t means f preserves something
    - Preserving something means any truth table that doesn't preserve is unreachable
    - What's the condition for not being preservative? Not satisfying t
    - Therefore if a table doesn't satisfy t it is unreachable by any f or combo of fs satisfying t

Next question: is g satisfying every test f satisfies enough to guarantee f can reach g through composition?

Related: does g satisfying every test satisfying f guarantee f satisfies every test satisfying g? (If answer to above is yes, this would imply f and g have the same composite range)

Is satisfying every test a preserved property? Yes

Is dissatisfying a test a preserved property? No, can't be (fn complete sets can compose to any fn)

"I have some fn satisfying all my tests, can that fn compose to reach me?"



Question: does commuting with anything but the identity preclude composing to the identity? Identity commutes with everything (and is the only fn to do so), so composing to the identity would require testing only the identity if the statement "a group of functions composes to another iff they collectively satisfy all of its tests" is true. This is a more tractable case study on feasibility of that conjecture
- and and or both compose to the identity immediately
- Wrong direction - identity cannot compose to anything bc it always commutes with something. This case study does support the conjecture
- In fact every f tests a subset of the identity's tests, so every f should compose to the identity. Obviously the constant functions don't compose to the identity


Is at least one of every testing pair linear?
- promising lead: if every fn can be expressed as a nested modular expression, but linears can be expressed with only one modulo basis
    - ((a%m)%n) and what is its relation to a%n
    - a%m=(a+n%m*a//m)%m

Exercise: given an t, try to build out a f that satisfies it. The crux appears to be that once you choose the output for a particular input of f (e.g. 0,1,0 -> 1), this gets "tied" to some other input (if t is "NOT", then 0,1,0 gets tied to 1,0,1).
Observation: for NOT, an input array X is tied to the elementwise application of NOT on X
e.g. 0,1,0,1 -> 1 ties the input 1,0,1,0 to being 0

From the matrix representation of commutative test, this is roughly equivalent to "bringing the top row down". Below, Y gets "linked" to X through application of t
```
f > X0  X1  X2  X3  X4  X5  |  _
----------------------------|-----
f > Y0  Y1  Y2  Y3  Y4  Y5  |  _  
    ^   ^   ^   ^   ^   ^
    t   t   t   t   t   t
```

Can we generate a similar pattern with higher order t? Below, maybe ZY gets linked with XY and/or ZX? How does the output change as a result?
```
f > X0  X1  X2  X3  X4  X5  |  X'
----------------------------|-----
f > Y0  Y1  Y2  Y3  Y4  Y5  |  Y'  
f > Z0  Z1  Z2  Z3  Z4  Z5  |  Z'  
    ^   ^   ^   ^   ^   ^      ^
    t   t   t   t   t   t      t
```

I interpose X and Y, X' and Y' must be already defined, so it better be true the t(Z', X') = Y' if t(Z', Y') = X'

Seems like t must always satisfy the property that each of its inputs and outputs must be interposable. Does f also have to satisfy that property?
- T doesn't actually have to satisfy this property UNLESS f also satisfies it. Basically the top right value is knowable upon interpolation iff indices of f interpose with results of f.
- Note that interposition of each index with the result means each index also interposes with other indices
- If ANY two indices interpose on f, then no change happens to inputs of t
- What are all the eigen transformations of f? Seems if a transformation doesn't affect f in the main matrix and doesn't affect f on the top, then it's not possible for such a transformation to change the result of a test

```
interposition of two indices of f:

f > X0  X1  X2  X3  X4  X5  |  X'
----------------------------|-----
f > Y0  Y1  Y2  Y3  Y4  Y5  |  Y'  
f > Z0  Z1  Z2  Z3  Z4  Z5  |  Z'  
f > W0  W1  W2  W3  W4  W5  |  W'  
    ^   ^   ^   ^   ^   ^      ^
    t   t   t   t   t   t      t


f > X0  X'  X2  X3  X4  X5  |  ?
----------------------------|-----
f > Y0  Y'  Y2  Y3  Y4  Y5  |  ?  
f > Z0  Z'  Z2  Z3  Z4  Z5  |  ?  
f > W0  W'  W2  W3  W4  W5  |  ?  
    ^   ^   ^   ^   ^   ^      ^
    t   t   t   t   t   t      t

interesting: if f satisfies t, then I can repeat the process of calculating the rhs and substituting it into the index. This process has to form a cycle since there are a finite number of right hand columns. At first glance seems like the cycle is at most dim^3 in length, but if all 3 cycles were dim in length, the cycle would be dim  elements long. Max length seems to be the product of the superset of primes of (dim, dim-1, dim-2) - e.g. if top row had a cycle of 5, mid row had a cycle of 4, bottom row had a cycle of 3, then 5*4*3 is max length of cycle?
Can narrow this down further because top right can have no more than dim iterations between the same output.

Can divide each index (for other indices fixed) into cycles, defined by the process where we take the output, sub into the index, then repeat until we get see a value we've seen before.
e.g. 0 -> 3 -> 4 -> 1 -> 0
Can we have cycles with a tail, where the repeated value is not the first we choose?
e.g. 0 -> 3 -> 4 -> 3
Tailed cycles will occur if the outputs for this fixed index do not span every possible input (implication is that two inputs yield same output). Otherwise, the cycles partition the entire set of possible values.


f(X0, X', X2, X3, X4, X5) = t(
    f(W0, W', W2, W3, W4, W5),
    f(Z0, Z', Z2, Z3, Z4, Z5),
    f(Y0, Y', Y2, Y3, Y4, Y5)
)

f > ?   ?   ?   ?   ?   ?   |  ??
----------------------------|-----
f > Y0  Y'  Y2  Y3  Y4  Y5  |  ?
f > X0  X'  X2  X3  X4  X5  |  ?
f > W0  W'  W2  W3  W4  W5  |  ?
    ^   ^   ^   ^   ^   ^      ^
    t   t   t   t   t   t      t
```

Consider that changing one index effects some delta in the overall result f(t()) %dim. If I change one index, that gives me

```
starting from

f(X0, t(W1, Z1, X1), X2, X3, X4, X5)
=
t(W', f(Z0, Z1, Z2, Z3, Z4, Z5), Y')

and

f(X0, t(W1, Z1 + N, X1), X2, X3, X4, X5)
=
t(W', f(Z0, Z1 + N, Z2, Z3, Z4, Z5), Y')

where the delta is 
(
    f(X0, t(W1, Z1 + N, X1), X2, X3, X4, X5)
    - f(X0, t(W1, Z1, X1), X2, X3, X4, X5)
) % dim = (
    t(W', f(Z0, Z1 + N, Z2, Z3, Z4, Z5), Y')
    - t(W', f(Z0, Z1, Z2, Z3, Z4, Z5), Y')
) % dim

rearranging, we get
(
    f(X0, t(W1, Z1 + N, X1), X2, X3, X4, X5)
    + t(W', f(Z0, Z1, Z2, Z3, Z4, Z5), Y')
) % dim = (
    t(W', f(Z0, Z1 + N, Z2, Z3, Z4, Z5), Y')
    + f(X0, t(W1, Z1, X1), X2, X3, X4, X5)
) % dim

subbing in 
(
    f(X0, t(W1, Z1 + N, X1), X2, X3, X4, X5)
    + f(X0, t(W1, Z1, X1), X2, X3, X4, X5)
) % dim = (
    t(W', f(Z0, Z1 + N, Z2, Z3, Z4, Z5), Y')
    + t(W', f(Z0, Z1, Z2, Z3, Z4, Z5), Y')
) % dim


can boil down to f(t(x+N)) = t(f(x+N))
since we're now working with one variable
and the above becomes
f(t(x)) = t(f(x))
f(t(x+N)) = t(f(x+N))

if x+N is on f's cycle in that index, then it must reachable by composing fs like f(f(f(f(...f(x)))))

#### checking for linear f:
assume f's free index can be expressed as a linear fn: f(y) = ay + b
then by definition (since t commutes over f)
a t(x) + b = t(ax + b)
(this is the definition of t being linear lol) and 
a t(x+N) + b = t(a*(x+N) + b)

notice that NO MATTER WHAT,
    (t(ax + b) - b) / a
MUST BE AN INTEGER
but a can be ANY INTEGER
what this really means is that if fractional part is frac()
    ** main property of frac is that frac(g+h) = frac(frac(g)+frac(h))
    frac(t(ax + b) / a) = frac(b / a)
which means that if I increment b to b+d (for delta)
    frac(t(ax + b+d) / a) = frac((b+d) / a)
    frac(t(ax + b+d) / a) = frac(frac(b/a) + frac(d/a))
but frac(b/a) = frac(t(a(x+N) + b) / a) so
    frac(t(ax + b+d) / a)
    = frac(frac(t(ax + b) / a) + frac(d/a))
so there's an integer difference like this:
    frac(t(ax + b+d) / a) + M
    = frac(t(ax + b) / a) + frac(d/a)
and rearranging
    frac(t(ax + b+d) / a) - frac(d/a)
    = frac(t(ax + b) / a) - M
then
    frac(t(ax + b+d) / a - d/a)
    = frac(t(ax + b) / a - M)
    = frac(t(ax + b) / a)         // b/c integer doesn't affect frac()
so
    frac(t(ax + b+d) / a - d/a) = frac(t(ax + b) / a)
and
    frac(t(ax + b+d) / a - t(ax + b) / a - d/a) = 0
and
    frac((t(ax + b+d) - t(ax + b) - d) / a) = 0
this just tells me that t(ax + b+d) - t(ax + b) is d + an integer multiple of 1
    ** another property of frac is that is is just "mod 1"
    This line of reasoning might still hold if we choose "mod foo"

original statement was:
    a t(x) + b = t(ax + b)
and let mQ(x) be defined as x % Q, then it's true that
    mQ(a t(x) + b) = mQ(t(ax + b))
    mQ(t(x)) = mQ((t(ax + b) - b) / a)
    mQ(t(x)) = mQ(t(ax + b) / a - b/a)
    mQ(t(x)) = mQ(t(ax + b) / a) - mQ(b/a)   [name: eq570]
now increment b by d
    mQ(t(x)) = mQ(t(ax + b+d) / a) - mQ((b+d)/a)
    mQ(t(x)) = mQ(t(ax + b+d) / a) - mQ(b/a) - mQ(d/a)
and subtract in eq570
    0 = mQ(t(ax + b+d) / a)
        - mQ(b/a)
        - mQ(d/a)
        - mQ(t(ax + b) / a)
        + mQ(b/a)
    0 = mQ(t(ax + b + d) / a) - mQ(t(ax + b) / a) - mQ(d/a)
    0 = mQ((t(ax + b + d) - t(ax + b) - d) / a))
    0 = mQ(t(ax + b + d) - t(ax + b) - d))
finally:
    mQ(t(ax + b) + d) = mQ(t(ax + b + d))
which is the definition (under mod) of t being linear in b



A lemma:
If t is linear in b, then
    mQ(t(ax + b) + d) = mQ(t(ax + b + d))
and I can write 
    t((a+d)x + b) = t(ax + (b+dx))
replace dx with d'
    mQ(t((a+d)x + b)) = mQ(t(ax + b + d')) = mQ(t(ax + b) + d')
so
    mQ(t(ax + b + d')) = mQ(t(ax + b) + d')
    mQ(t(ax + b + dx)) = mQ(t(ax + b) + dx)
    mQ(t((a+d)x + b)) = mQ(t(ax + b) + dx)       [name: eq599]

Another way to think about it is t(ax+b)=t(0)+ax+b


Do a similar argument for a, start from eq570:
    mQ(t(x)) = mQ(t(ax + b) / a) - mQ(b/a)
and increment a by d:
    mQ(t(x)) = mQ(t((a+d)x + b) / (a+d)) - mQ(b/(a+d))
subtract in eq570:
    0 = mQ(t((a+d)x + b) / (a+d)) - mQ(b/(a+d))
        - mQ(t(ax + b) / a) + mQ(b/a)
multiply through by (a+d) * a:
    0 = mQ(a * t((a+d)x + b)) - mQ(ab)
        - mQ(t(ax + b) * (a+d)) + mQ(b*(a+d))
    0 = mQ(a * t((a+d)x + b)) - mQ(ab)
        - mQ(t(ax + b) * (a+d)) + mQ(ba) + mQ(bd)
    0 = mQ(a * t((a+d)x + b)) - mQ(t(ax + b) * (a+d)) + mQ(bd)
    0 = mQ(a * t((a+d)x + b) - t(ax + b) * (a+d) + bd)
    0 = mQ(a * t((a+d)x + b) - a * t(ax + b) - d * t(ax + b) + bd)
    0 = mQ(
        a * (t((a+d)x + b) - t(ax + b))
        - d * (t(ax + b) + b))
    )
and since mQ(t((a+d)x + b)) = mQ(t(ax + b) + dx) by eq599 above
    0 = mQ(
        a * (t(ax + b) + dx - t(ax + b))
        - d * (t(ax + b) + b))
    )
    0 = mQ(adx - d * (t(ax + b) + b)))
    0 = mQ(d * (ax - t(ax + b) - b))
    0 = mQ(t(ax + b) - ax - b)
    mQ(ax + b) = mQ(t(ax + b))

so f(y) = mQ(ay + b) implies t(ax + b) = mQ(ax + b) or t(f(x)) = f(x)

IMPORTANT: THIS LOOKS LIKE t=I, BUT ONLY APPLIES OVER THE RANGE OF f

At the start of the argument, we fixed all of f's indices except one and assumed that index was linear, and did similarly for t. Since we can choose any index to be free on f or t, this means that if any index on f or t is linear, and f commutes with t, every index of f and t is linear, and moreover is expressible by the same linear function (if f(y) = ay + b implies t(x) = ax + b, and each index of f must match all indices of t, and all indices of t must match each index of f, then every index of t and f is ax + b).

To handle the fact that every index contributes to the result, note that the above equations are all mQ. Basically, this implies that the sum of other indices gets lumped in then modded out to some constant, offsetting on both sides by the same amount mQ. This might imply that the ultimate value of f(t(...), t(...), ...) is a straight sum of every index like so: a*t(...)+b + a*t(...)+b + ...

note that the NOT function is f(x) = x+1 OR f(x) = -x on m2
```


active question - if two fns commute, is one of them linear?

Something weird:
The only binary two valued functions that commute with NOT are themselves defined in terms of NOT:
- A . B = NOT A
- A . B = NOT B
Three valued functions can be
- F(a,b,c)=(a+b+c)%2
Lesson being we can basically "not" and odd number of inputs and sum them up. This is in line with the above; for a fixed a and b, c behaves like "not"
More precisely:
```
NOT = ax + b = x + 1
---
g1(a) = f(a, 1, 1) = (a + 1 + 1) % 2
g1(0) = 2 % 2 = 0
g1(a) = g(0) + ax + b = 0 + x + 1 = x + 1 = NOT
---
g2(a) = f(a, 1, 0) = (a + 0 + 1) % 2
g2(0) = 1 % 2 = 1
g2(a) = g(0) + ax + b = 1 + x + 1 = x + 2 = x = I
---
basically, all that is important about the above is that g1 and g2 both work element-wise to satisfy NOT. NOT is kind of a lame example because I is the only other unary two valued function
```

Easy question: do OR and AND have this element-wise linearity?
What's interesting is that everything on 2 truth values has element-wise linearity. Holding all but one place constant, you only have F,F F,T T,F T,T as possible outcomes. You can always define this as 0, x, x+1, or 1 respectively.
Same is actually true for 3 truth values, since it's impossible to arrange 3 elements to be non-cyclic and non-anti-cyclic

So we have established element-wise linearity for all 2-valued functions, and each index (with other indices frozen) can have one of 4 different linear representations (mod 2) - x, x+1, 1, or 0. Now the question we need to answer is whether testing pairs in 2 dimensions all satisfy f(x) = f(0) + t(x) or whether there are exceptions.

Reminder for next time: python script seems to be showing f and t pairs that contradict the element wise linearity result above. Need to check some examples by hand

# What testing functions represent the 5 classes of Post?
true-preserving is T
false-preserving is F
self-dual is NOT

Counting functions
- One counting function is XOR. What commutes with XOR? Itself
- NXOR is counting. What commutes with NXOR? Itself
- Ary 3 counting functions are both commutative with themselves
- By the nature of counting functions, all counting functions self-commute (can be defined in terms of mod operators)

Monotonic functions
- 0,0,0,1 is monotonic, commutes with itself
- 0,0,1,1 is just identity
- 0,1,1,1 is monotonic, commutes with itself
- 0,0,0,0,0,1,1,1 is monotonic, but only commutes with identity up to ary 4
    - The related 0,0,0,1,1,1,1,1 seems to not commute with anything as well
    - Neither of these are actually monotonic though, I got the definition of monotonic wrong
- 0,0,0,0,0,0,0,1 is monotonic and commutes with itself (and some other random things)
    - The related 0,1,1,1,1,1,1,1 commutes with itself too
- 0,0,0,1,0,1,1,1 is monotonic and the only interesting function up to arity 4 it commutes with is NOT
    - Not surprising, it is also self-dual
    - Also commutes with T and F, again not surprising since it preserves T and F
- 0,0,1,1,0,1,1,1 is monotonic and again only commutes with T, F, and I

If a function is non-true-preserving, it can be monotonic iff it is F
If a function is non-false-preserving, it can be monotonic iff it is T
Both T and F commute with themselves (i.e. are counting?)

If I satisfy non-counting, non-F-preserving, and non-T-preserving, that means I have at least one function that is non-constant that 

```
                   T  F  Other
Commutes w/ self | Y  Y            if Y, 
Commutes w/ T    | Y  N
Commutes w/ F    | N  Y
Commutes w/ NOT  | N  N
Is monotonic     | Y  Y
```

Let's try it. What's a function that is monotonic but is not counting?
- 0,0,1,1 and 0,1,0,1 and 0,0,0,0 and 1,1,1,1 are the only 2d monotonics, but all are counting
- 0,0,1,1,0,1,1,1 might be one of the simplest...

```
(0, 0, 0) | 0
(0, 0, 1) | 0
(0, 1, 0) | 1
(0, 1, 1) | 1
(1, 0, 0) | 0
(1, 0, 1) | 1
(1, 1, 0) | 1
(1, 1, 1) | 1
```

F in second position yields 0,0,0,1, which is AND
Can't seem to form NOT...
- Would need a row with an input position i where the row output is (NOT i) and inverting the one index inverts the output. There are finitely many cases to check, and none of them work
- Monotonics actually seem specifically antithetical to forming NOT. Monotonics are defined by varying one index at a time, and assert that the changing of a T to F in one index can never result in a change from F to T in the output. Therefore, if all functions are monotonic, it's never possible to form NOT
    - Interesting that there's not an obvious commutativity relation for monotonics then...
    - Monotonics seem intrinsically related to this idea of allowing negation of an input

What's a better way of thinking about monotonics? In the below diagram, "counting" means that no two connected nodes have the same value. Monotonic means that no higher node has a 0 while a lower has a 1. True preserving means top node has a 1. False preserving means bottom has a 0. Self dual means that nodes that land in the same place upon 180 deg rotation have opposite values
```
        (1,1,1)
       /   |   \
     /     |     \
(0,1,1) (1,0,1) (1,1,0)
   | \   /   \   / |
   |   X       X   |
   | /   \   /   \ |
(0,0,1) (0,1,0) (1,0,0)
     \     |     /
       \   |   /
        (0,0,0)
```

Is there a way of defining an "inverted" commutativity relation that does test for monotonics specifically (since monotonics seem tied to inversion)? Maybe try anticommutativity. Anticommutativity might not have merit here. 0,0,1,1,0,1,1,1 does not anticommute with anything up to arity 4

The generalizable form of "anticommutativity" would be something like a * b = f(b * a) where f is NOT (but in general can be any unary function)
- There might be an opportunity to simplify conditions here. There are 4 unary function (I, NOT, F, T) in 2 valued logic, and it therefore might be possible to, instead of insisting there's some "special" reason we test T, F, NOT, that in fact we are always testing if a function commutes w/ itself and we just vary f
    - However, it's not immediately clear that w/ NOT is the same thing as NOT commutes w/ self

interesting that NOT is a function that cannot be composed without a non-monotonic and f = NOT is (maybe) used in determining anticommutativity

XOR anticommutes with NXOR and NOT and some weird operators like 10010110

AND doesn't anticommute with anything up to arity 4





A function that is both non-true preserving and non-false preserving cannot be monotonic. I.e. a monotonic is always at least one of true or false preserving.


Let's test a very simple monotonic 0,1,1,1,1,1,1,1

```
b > ?   ?   ?   |  ??
----------------|-----
b > Y0  Y1  Y2  |  ?
b > X0  X1  X2  |  ?
b > W0  W1  W2  |  ?
    ^   ^   ^      ^
    a   a   a      c


(0, 0, 0) | 0
(0, 0, 1) | 1
(0, 1, 0) | 1
(0, 1, 1) | 1
(1, 0, 0) | 1
(1, 0, 1) | 1
(1, 1, 0) | 1
(1, 1, 1) | 1
```


Must be true that c(0) = b(a(0)) = a(0), similarly c(1) = a(1)
When top row goes 0,0,0 to 0,0,1, then ?? changes from 0 to 1
Assume a(0) = 0
- Then c(0) = 0
- Change Y2 to 1, then c(0,0,1) = b(0,0,a(0,0,1))
    - Forces c(0,0,1) = a(0,0,1)
- Change Y1 to 1, then c(0,0,1) = b(0,a(0,0,1),0)
    - Again forces c(0,0,1) = a(0,0,1)
- Change X2 to 1, then c(0,1,0) = b(0,0,a(0,1,0))
    - Forces c(0,1,0) = a(0,1,0)
- Change X1 to 1, then c(0,1,0) = b(0,a(0,1,0),0)
    - Again forces c(0,1,0) = a(0,1,0)
- Can extend to c(1,0,0) = a(1,0,0) without contradiction
Set Y2 to 1
- Set X2 to 1, then c(0,1,1) = b(0,0,a(0,1,1))
    - Forces c(0,1,1) = a(0,1,1)
Can extend to show that c = a without contradiction

Something interesting seems to happen at the boundary of b that forces equivalence relations between a and c. If a can produce both 0 and 1, then choose some position of b (middle rows) that is poised to change output for some increment of some index. Then, you can change whatever value in the column poised to change b's output and derive relations like b(..., a(...), ...) = c(..., 0, ...) and b(..., a(...), ...) = c(..., 1, ...) for each index of c. c's inputs are all known, and we're assuming b is at a boundary. You can also choose values of a such that b is (top row) is poised to change, then ascertain c(...) = 0 and c(...) = 1, 


One thought: take b = 0,0,1,1,0,1,1,1, now the question is whether there exist any two functions a and c such that a * b = b * c

```
b > ?   ?   ?   |  ??
----------------|-----
b > Y0  Y1  Y2  |  ?
b > X0  X1  X2  |  ?
b > W0  W1  W2  |  ?
    ^   ^   ^      ^
    a   a   a      c


(0, 0, 0) | 0
(0, 0, 1) | 0
(0, 1, 0) | 1
(0, 1, 1) | 1
(1, 0, 0) | 0
(1, 0, 1) | 1
(1, 1, 0) | 1
(1, 1, 1) | 1
```

Must be true that c(0) = b(a(0)) = a(0), similarly c(1) = a(1)
When top row goes 0,0,1 to 0,1,1, then ?? changes from 0 to 1
Assume a(0) = 0
- then c(0) = 0
- ?? is 0 for 0
- 


if the square inputs are non-decreasing, then c's inputs are also non-decreasing. Similarly, if a's outputs are non-decreasing, then ?? is also non-decreasing. I guess the question is where does the contradiction arise... 





Maybe another way of tackling monotonics is to embed them in N-space?
```
001 - - - - -101
| \           | \
|   011 - - - - -111
|   |         |   |
|   |    x    |   |
|   |         |   |
000 | - - - -100  |
  \ |           \ |
    010 - - - - -110
```

Monotonic means no move up, to the right, or forward can result in an output going from 1 to 0. Self-dual means that the output for input x maps to the same output as input 1-x. Counting means no two adjacent edges have the same value. True and false preserving are obvious.




It is pretty easy to find _necessary_ testable conditions for nonmonotonics, but not _sufficient_ conditions. Monotonics necessarily are true-preserving or false-preserving, or both if non-constant, so non-monotonicity can be shown if a function is (non-true-preserving and not FALSE) or (non-false-preserving and not TRUE) or (non-true-preserving and non-false-preserving), but then there are non-monotonics that still satisfy this relation. But monotonicity itself seems hard to establish from the "outside" in some way...





(0,0,0,0,0,0,0,1) commutes with AND
AND commutes with AND
OR commutes with OR
