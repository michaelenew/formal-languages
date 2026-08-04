# Associativity
Checking if the generalized composition operator is associative

```
f * t = f(
    t(x11, x12, x13, ...),
    t(x21, x22, x23, ...),
    t(x31, x32, x33, ...),
    ...
)

```


```
f > ?   ?   ?   ?   ?   ?   |  ??
----------------------------|-----
f > Y0  Y'  Y2  Y3  Y4  Y5  |  ?
f > X0  X'  X2  X3  X4  X5  |  ?
f > W0  W'  W2  W3  W4  W5  |  ?
    ^   ^   ^   ^   ^   ^      ^
    t   t   t   t   t   t      t
```

```
(f * g) * h =>

f(
    x1,
    x2,
    x3,
    ...
)

f(
    g(x11, x12, x13, ...),
    g(x21, x22, x23, ...),
    g(x31, x32, x33, ...),
    ...
)

f(
    g(
        x11,
        x12,
        x13,
        ...
    ),
    g(
        x21,
        x22,
        x23,
        ...
    ),
    g(
        x31,
        x32,
        x33,
        ...
    ),
    ...
)


f(
    g(
        h(x111, x112, x113, ...),
        h(x121, x122, x123, ...),
        h(x131, x132, x133, ...),
        ...
    ),
    g(
        h(x211, x212, x213, ...),
        h(x221, x222, x223, ...),
        h(x231, x232, x233, ...),
        ...
    ),
    g(
        h(x311, x312, x313, ...),
        h(x321, x322, x323, ...),
        h(x331, x332, x333, ...),
        ...
    ),
    ...
)
```


```
f * (g * h) =>

h(
    x1,
    x2,
    x3,
    ...
)

g(
    h(
        x11,
        x12,
        x13,
        ...
    ),
    h(
        x21,
        x22,
        x23,
        ...
    ),
    h(
        x31,
        x32,
        x33,
        ...
    ),
    ...
)

f(
    g(
        h(x111, x112, x113, ...),
        h(x121, x122, x123, ...),
        h(x131, x132, x133, ...),
        ...
    ),
    g(
        h(x211, x212, x213, ...),
        h(x221, x222, x223, ...),
        h(x231, x232, x233, ...),
        ...
    ),
    g(
        h(x311, x312, x313, ...),
        h(x321, x322, x323, ...),
        h(x331, x332, x333, ...),
        ...
    ),
    ...
)
```

It is associative

# Identity

Identity is already known - `x => x` is the identity. 

# Inverse

To define inverse, all the functions have to be of the same type. We'll accomplish this by letting every function be infinite-dimensional, but where any indices that are not mentioned are do-nothing indices.

We also need an ordering on the indices. Technically we can choose whatever ordering we want here, but we'll use the natural one (from above, basically we want the composition's inputs to follow the same order they appear in the full expansion so that `(f * g)(x11, x12, x13, ...) = f(g(y11, y12, y13, ...), ...)`). Letting the "sub"script denote the function's explicit indices, we can define
`f(xi) * g(yj)` becomes `(f * g)(xij)` where `ij` is ordered left-dominant.
- This ordering is a little weird since we're letting each dimension be infinite. Technically the i and j can apply only to explicit indices, nothing wrong with that, but it's still kind of an odd ordering. Might make sense to just claim the function, rather than accepting a tuple of inputs (i.e. map of int to input), accepts a map of tuple to input.

```
f > y3   y2   y1   |  z
-------------------|-----
    x31  x21  x11  |  
    x32  x22  x12  |  
    x33  x23  x13  |  
    ^    ^    ^       
    g    g    g       
```

The identity is the function wherein x11 == z no matter what inputs are provided.

Notes:
- If g is "or" it becomes impossible to back out x11. Proof is very simple: consider a case where x11 is 1, x12 is Y, and the output is 1. Then switch x11 to 0. The output of g doesn't change, so the output of the whole thing stays 1.
- This effect occurs for _any_ non-invertible (i.e. non-information-conserving) function of either g or f
- Conservative isn't enough to form a group either. All information in the left two columns is trash (unaffected in any way by the value of x11). The only value f receives that encodes any info about z11 is y1, but there are multiple configs of x1* that produce each y1 (and x11 must be different for each since it's conservative), so we can't back out what x11 was
- There needs to be some row-wise constraint on the system here to enable encoding of information about x1j, j > 1
    - Requiring functions to be either commutative or non-commutative encodes row-wise information
    - I already know that some noncommutative functions form commutative functions under some compositions, but this * is a very special type of composition that doesn't allow for index-wise nesting, so it's possible that this general composition is closed for noncommutative functions
    - I also know that commutative functions under _any_ composition are closed

Open question:
- If f and g are both commutative under * (i.e. `(f * f)(xij) = (f * f)(xji)` and same for g), does that imply `f * g = g * f`?
    - Assuming  that an inverse exists for all functions
    - if f * f is commutative, is f * g commutative with f?
    - f * g = h
    - f * g * f = h * f
    - g * f = f-1 * h * f
    - So they're in the same conjugacy class
    - Now my question was whether g * f is commutative with f
    - f * g * f = f * ( g * f ) = f * h = f * ( f-1 * h * f ) = f * f-1 * h * f = h * f
    - So yes
    - Now
    - f * g = h
    - f * g * f = h * f
    - f * g * f = f * h
    - f-1 * f * g * f = f-1 * f * h
    - g * f  = h = f * g
    - QED
    - I think my only assumption I used here was actually that f is commutative, right? Easy enough to test

Now back here

```
f > y3   y2   y1   |  z
-------------------|-----
f > x31  x21  x11  |  q1
f > x32  x22  x12  |  q2
f > x33  x23  x13  |  q3
    ^    ^    ^       ^
    g    g    g       g
    f    f    f       f
```

I know that this diagram must hold true assuming that both f and g are commutative (bottom row can be either f or g)

Question is, if f is conservative and commutes with itself, is there a g that is conservative and commutative such that f * g reduces to the identity?

For dimensionality d and arity a, there are d^a/d = d^(a-1) rows that produce a given output (for a conservative function). We need to distinguish between this many inputs to determine x11 based on the output of the function. Including commutativity means I can whittle down the right column to the d^(a-1) elements that could produce z

One thing that would help a lot would be to understand what this operation looks like on a truth table or graph.

```
xor:
----+--
0 0 | 0
0 1 | 1
1 0 | 1
1 1 | 0
```

g * xor
```
we chop the table of g * xor into little chunks
+-----+ +-----+ 
| 0 0 | | 0 0 | 
| 0 0 | | 0 1 | 
| 0 0 | | 1 0 | 
| 0 0 | | 1 1 | 
+-----+ +-----+
| 0 1 | | 0 0 | 
| 0 1 | | 0 1 | 
| 0 1 | | 1 0 | 
| 0 1 | | 1 1 | 
+-----+ +-----+
| 1 0 | | 0 0 | 
| 1 0 | | 0 1 | 
| 1 0 | | 1 0 | 
| 1 0 | | 1 1 | 
+-----+ +-----+
| 1 1 | | 0 0 | 
| 1 1 | | 0 1 | 
| 1 1 | | 1 0 | 
| 1 1 | | 1 1 | 
+-----+ +-----+ 
```

```
f > y2   y1   |  z
--------------|-----
f > x21  x11  |  q1
f > x22  x12  |  q2
    ...  ...  |  ...
    ^    ^       ^
    g    g       g
    
where f is xor and g is to be devised.

f > y2   y1   |  z
--------------|-----
f > 0    0    |  0
f > 0    0    |  0
    ...  ...  |  ...
    ^    ^       ^
    g    g       g

Here for f * g to reduce to the identity, g(0, 0, ..) must be 0
Now evaluate to

f > y2   y1   |  z
--------------|-----
f > 1    1    |  0
f > 0    0    |  0
    ...  ...  |  ...
    ^    ^       ^
    g    g       g

So g(0, 0, ...) = 1 for identity to hold but we already defined g(0, 0, ...) to be 0.
This is a contradiction.
Such an example must arise no matter the chosen f. Just cycle through any two inputs that produce the same output in the first row. Since the function is conservative, the x11 must be different, leading to a contradiction.
```

A system like this having an associative closed binary operation with an identity element is called a monoid (hey, found one)

Because we no longer need an inverse to hold, we can include the nil-ary operations as well, making the system completely self-contained

For next time:
I know that the * operator forms a monoid over the n-ary d-dimensional logical functions. One subset (is it a submonoid? could be b/c it has identity) of the n-ary d-dimensional logical functions is of commutative functions. Open questions:
- What's the relationship between * and element-wise composing? Element-wise composing determines functional completeness so that is still key
- Generation concepts in monoids? What's generated by the commutatives? Non-commutatives?
- what are the idempotents
- interesting - with the inclusion of nil-ary operators, the functions themselves are a map from the subset of nilary operators to that same subset... sort of since sets of operators aren't included in the monoid
- box operator where the right side is nilary is just a special case of calling the function with constant input (just a one valued truth table)
- the single composition operator kind of forms a monoid. Call .i the operator that embeds b into the ith parameter of a upon a .i b. Then a .i b .j c can be evaluated without regard for the internals of a, b, and c in the sense that (a .i b) .j c = a .i (b .j' c) where j' = i + j (infinite trailing dummy indices can be accounted for by truncating a to the max of i and its max nondummy index, and similar for b, and truncating c to max nondummy index)
- is commutativity an equivalence relation? ab=ba and ac=ca, then bc=cb? Not necessarily, but it does form a class. It's an implication relation, not an equivalence relation. 
- does single composition preserve any of Green's relations?
- can every index-wise composition be expressed as some generalized composition?
    - Can every index-wise composition be expressed as a generalized composition involving the index-wise composed elements?
        - Counterexamples below that there's no left element and no right element. Still need to check for sandwiches
    - Are there primes under the generalized composition
    - Seems plausible there might exist "selection" elements that do a similar job to index-wise composition under general composition, maybe something like a * s_i * b is equivalent to a \*i b
        - Counterexamples below to left and right versions. Can consider sandwiches

# Indexing
## diagonal indexing?
x_ij =>
00 => 0
10 => 1
01 => 2
20 => 3
11 => 4
02 => 5

area of prior triangle + how many elements have I traversed on the current hypotenuse?
side length of prior triangle = i + j => area = (i + j) (i + j + 1) / 2
steps taken on current hypotenuse = j

so x_ij = x_k where k = (i + j) (i + j + 1) / 2 + j
= (i^2 + ij + i + ji + j^2 + j) / 2 + j
= (i^2 + j^2 + 2ij + i + 3j) / 2

Does this work nicely with associativity?

(x_i * y_j) * z_k
s = ij = (i^2 + j^2 + 2ij + i + 3j) / 2
t = sk = (s + k) (s + k + 1) / 2 + k
\= ((i^2 + j^2 + 2ij + i + 3j) / 2 + k) ((i^2 + j^2 + 2ij + i + 3j) / 2 + k + 1) / 2 + k
\= i/4 + (3 i^2)/8 + i^3/4 + i^4/8 + (3 j)/4 + (5 i j)/4 + (5 i^2 j)/4 + (i^3 j)/2 + (11 j^2)/8 + (7 i j^2)/4 + (3 i^2 j^2)/4 + (3 j^3)/4 + (i j^3)/2 + j^4/8 + (3 k)/2 + (i k)/2 + (i^2 k)/2 + (3 j k)/2 + i j k + (j^2 k)/2 + k^2/2
^^^ wolfram alpha

x_i * (y_j * z_k)

q = jk = (j + k) (j + k + 1) / 2 + k = (j^2 + k^2 + 2jk + i + 3k) / 2
r = iq = (i + q) (i + q + 1) / 2 + q
\= (i + (j^2 + k^2 + 2jk + i + 3k) / 2) (i + (j^2 + k^2 + 2jk + i + 3k) / 2 + 1) / 2 + (j^2 + k^2 + 2jk + i + 3k) / 2
\= (5 i)/4 + (9 i^2)/8 + (3 j^2)/4 + (3 i j^2)/4 + j^4/8 + (9 k)/4 + (9 i k)/4 + (3 j k)/2 + (3 i j k)/2 + (3 j^2 k)/4 + (j^3 k)/2 + (15 k^2)/8 + (3 i k^2)/4 + (3 j k^2)/2 + (3 j^2 k^2)/4 + (3 k^3)/4 + (j k^3)/2 + k^4/8
^^^ wolfram alpha

So not working...

Pairing functions are a thing https://en.wikipedia.org/wiki/Pairing_function#:~:text=In%20mathematics%2C%20a%20pairing%20function,same%20cardinality%20as%20natural%20numbers. but there's no mention of making one of them associative

Precisely what I need is a pairing function f(i,j) => k so that f(f(i,j),k) = f(i,f(j,k))

and in general anything that maps evenly spaced discrete right triangles should be easy to modify into a pairing function.

defining that (0,0) = 0, can I find a function that works?
f(f(0,0),0) = 0 = f(0,f(0,0))
f(f(1,0),0) = f(1,f(0,0)) = f(1,0) => f(1,0) = 1 by invertibility
f(f(0,0),1) = f(0,f(0,1)) = f(0,1) => f(0,1) = 1
=><=

If defining (0,0) = 0 doesn't work, what does that say about defining (0,0) = 1?
f(f(0,0), 0) = f(0,f(0,0)) = f(1,0) = f(0,1)
=><=

which also applies to any non-zero number chosen for (0,0)

So there is no associative pairing function

# Selection 

Let's try to insert False into or.

a or false

```
0 | 0
1 | 1
```

yields the identity, so if an insertion exists it somehow composes to the inverse of a, implying a has an inverse (whether left or right is not clear). This seems unlikely because it would imply or and the identity are of the same order (Green's relations)

Consider OR from the right. Since * is associative, there is no loss of generality in assuming composition with only one function.
```
f > y3   y2   y1   |  z
-------------------|-----
    x31  x21  x11  |
    x32  x22  x12  |
    ^    ^    ^
    OR   OR   OR
```

This cannot exist by the non-invertibility of OR in its first operand. If OR is not invertible or "counting" in its first operand, then there is some configuration for all other elements constant that x11 changes but y1 does not.

This also cannot exist by the symmetry of OR. Consider the same situation as above where x11 == z and x12 != x11, then swap x11 and x12.

Consider something composing with OR from the left.

```
OR> y2   y1   |  z
--------------|-----
    x21  x11  |
    x22  x12  |
    x23  x13  |
    ^    ^
    g    g
```
We need to produce something such that x11 = z always. This is never going to be possible by the symmetry of OR. Consider any arrangement where x21 != x11 and x11 == z. By the definition of the operator, the interposition of x1: and x2: is a possible input, and since OR is symmetric in its operands we have z == x21 and x21 != x11, so no such function exists. The same logic also applies to any functions that are symmetric in any two non-dummy operands.

** not sure if there's any relation to non-invertibility of OR in this case **

So there's no way to define an 'insertion' of false into OR. It also implies there is no left or right element which produces the identity when multiplied with OR. Both of these statements apply to anything which is symmetric in any operand and potentially to anything non-invertible.

# On left and right generators
the constant functions behave strangely under Green's relations. Green's relations define reflexive and transitive ordering operators <= where it holds that if a<=b and b<=c then a<=c. The constant operators from the left or the right always produce the constant operators.

Interestingly, it's possible in higher dimensions to create the constant expressions. Consider two functions g and f both of which have nondummy indices and are composed as f * g. Then choose g which outputs only 1 and 2 while f only changes for 3 and 4 supplied as its operands. This clearly creates a situation where f will never change but neither function was constant to start.

```
f > y2   y1   |  z
--------------|-----
    x21  x11  |
    x22  x12  |
    x23  x13  |
    ^    ^
    g    g
```

Note that this argument doesn't apply to 2 dimensions since you can't have a function which outputs numbers in some non-full range (you need to create two ranges that are non-empty, but if you try to partition [0, 1] you get [0] and [1], where one of these would be used as the set of possible outputs of g - but of course this means g's output never changes i.e. it's constant)

Might make sense to include functions of all dimensions where lower dimensional functions are dummy on inputs greater than the "dimension" with output of some large dimension so that they don't compose strangely with lower dimensional functions (could also use -1 to indicate some unused indices; this will map fine).

This seems to mean that the constant functions are the smallest elements under ordering, since they must be equivalent to themselves under composition. One weird thing is that one generates itself on the left, but on the right each generates every constant function.



# Do certain elements have inverses?
https://en.wikipedia.org/wiki/Coxeter_group
Does XOR have an inverse?

idk try a 2x2
```
f > y2   y1   |  z
--------------|-----
    x21  x11  |
    x22  x12  |
    ^    ^
    g    g
```

If g is XOR the trouble comes b/c XOR is symmetric in its operands. You can switch x11 and x12 for x11 != x12, leaving y1 in place and therefore z unchanged.

If f is XOR, trouble comes back to symmetry. Choose x11 != x21 then flip x1: and x2:, leaving z unchanged but x11 changed.


Adding further constraints doesn't invalidate this argument. Why does it feel like it might?
Let's enforce that it must be commutative (let f be the unknown)

```
f > y2   y1   |  z
--------------|-----
f > x21  x11  |  w2
f > x22  x12  |  w1
    ^    ^       ^
    g    g       g
```

Consider x:: = 0. Then y: and w: are both 0 and z is 0, so g(0,0) is 0
consider x:: = 0 except x11 = 1. g(0,1) = 1 for this to be an inverse
consider x:: = 0 except x22 = 1. g(1,0) = 0 for this to be an inverse
consider x:: = 0 except x21 = 1. Then top row is f(1,0) => z=1 which is not an inverse, so contradiction

This is just the argument from above. It holds irrespective of commutativity...



