
Start with the grid. All 0s. I'm trying to make an N-ary function T that commutes with the M-ary function F and I know that F is monotonic. Monotonic here means for _any_ chosen ordering of the truth values, an increase in input never results in a decrease in output.

```
f _ _ | _
------+---
f _ _ | _
f _ _ | _
  t t   t
```

NOTE: the answer is "yes". Every monotonic must preserve at least 1 truth value. But it's possible to have two monotonics, the first preserving 1 and the second preserving 0, but still not be FC. So the question I really need answered is more around whether there is an _indicative_ function that is always 
    - Maybe "a function commuting with NO constants" would be the condition? This guarantees there is one function that is non-monotonic. I can at least search for counterexamples:
        - AND, OR, NOT -> NOT commutes with no constants
        - AND, XOR, 1 -> 1 commutes with 1, AND and XOR commute with 0
            - These "test" as monotonics but aren't actually monotonic
            - Do these functions AVOID commuting with some specific function? Maybe I can narrow down the list further - "you're monotonic if you commute with a constant and you commute with < something else>"

Here's a way to observer monotonicity. Start with a graph at 0, F(0, 0, 0, ...). For each "next step" call the x axis 1 (sum of all inputs) and draw a line from the first point to each of the second. Then from each of those lines, for the next step (x axis 2) draw more lines to the values. This will create a big explosion of lines, all monotonically increasing.

Here's something quasi-orderly about this graph. If we ignore points that straddle the preserved constant, everything below the point F(preserved constant) must be less than or equal to the const and everything above it must be greater than or equal to it. This divides the graph into quadrants.
    This is true of every point - ignore the straddling points and it's divided into constants. It's interesting that for the preserved const it falls in a predictable way (i.e. on a particular curve) though
        Are there other predictable curves on which these divides must fall?
            I can create a sub-monotonic where I hold one input constant and vary the others. In the case where I hold one input constant at h and search for the constant preserved input g, the value of F must be in the range F(g) to F(h) inclusive and the input falls on the curve defined as F(h) := g + h * (num inputs - 1)
        Question: Is there a way to test for the preservation condition of a single "curve" using a single commutativity check? As in the first "curve" is hold nothing constant, put 0 then 1 then 2 then ... into all inputs.
            Doesn't seem like it. The commutativity must be local (must match everywhere), but the crossover property is global (just has to be true in one place)


So the graph of the first line would look something like this. The curve is f(x) = x ** (1 / arity) where arity is the arity of f

```
f(x)
|
|                    o
|           o
|      o
|   o
| o
+---------------------- sum of inputs
```

Then if I take one input, hold it at 0, I expect the crossover line to look like this. It's now the graph of f(x) = x ** (1 / (artiy-1))

```
f(x)
|
|               x    o
|       x   o
|    x o
|  xo
| x
+---------------------- sum of inputs
```

and if I take that same input and hold it at 10 instead of 0, I expect the crossover line to look like this (same slope as holding a constant 0 just offset horizontally). f(x) = (x - 10) ** (1 / (arity-1))

```
f(x)
|
|               x    o     z
|       x   o      z
|    x o        z
|  xo         z
| x          z
+---------------------- sum of inputs
```

The actual trace of the function must intersect each of these curves at least once.

What's really going on here is that each input is its own axis. What we're saying is that the function produces some path inside a N dimensional cube, but that eventually it must cross the straight line defined by (0, 0, 0, ...) and (1, 1, 1, ...). Take f(0, x). This "grows" on one wall of the 3d cube in which the parameterized function lives (a, b) -> (a, b, f(a, b)). If I now fix a:=0 and parameterize b -> (0, b, f(0, b)) then somewhere on the line (0, 0, 0) to (0, N, N) the curve will intersect it.
    Visualization help: this looks like a bunch of straight lines between various extrema of a cube. The lines always go from 0 to N in at least one dimension, so it's always some corner to another corner. The actual **SURFACE** (a, b, ..., f(a, b, ...)) always intersects all of these lines in at least 1 place.

It seems like this property of each sub-function preserving a constant is insufficient in isolation. I can simply create a function that is 0 everywhere that 0 or N is in the input (i.e. boundary locations) but choose the function to be any other shape elsewhere. For 4 truth values or more this gives me enough space to create a non-monotonic whose every sub-function preserves 0.


