
The composition generalization * mentioned in other docs is kind of like multiplication. First a little more generalization, as below we'll allow N possible output values of a given function:

```
f > ?   ?   ?   ?   ?   ?   |  ?? ?? ??
f > ?   ?   ?   ?   ?   ?   |  ?? ?? ??
f > ?   ?   ?   ?   ?   ?   |  ?? ?? ??
----------------------------|----------
f > Y0  Y1  Y2  Y3  Y4  Y5  |  ?  ?  ?
f > X0  X2  X2  X3  X4  X5  |  ?  ?  ?
f > W0  W3  W2  W3  W4  W5  |  ?  ?  ?
    ^   ^   ^   ^   ^   ^      ^  ^  ^
    t   t   t   t   t   t      t  t  t
```

Now we need another operator that acts kind of like "evaluating" in the sense of f(something, something, something). This other operator seems a little more like addition.

```
(a, b, c) => (d, e, f, z)
+
(g, h, i) => (j)

becomes

(d, e, f, a, b, c) => (j, z)
```

So roughly the outputs of the LHS "fill up" the inputs of the RHS to the greatest extent they can, and any remaining outputs get appended as new output values in the result. Inputs of the LHS are simply appended as new inputs.

This is kind of interesting. It introduces the idea of 0-output functions like `(a, b, c) => ()` that just add dummy indices.

In this system you "involve" two different "columns" of outputs to produce a new output by adding them to a new, "declared" function with the desired behavior. Something like `() => (a, b, c) + (d, e, f) => (g) yielding (a, b, c) => (g)`

This or something like it (haven't checked and it's 2 am) should satisfy associativity and might let * distribute over it (need to check).

If it does satisfy associativity, it makes the proof of distributivity over single-nesting super easy, considering

a * (b + c) = a * b + a * c = b * a + c * b = (b + c) * a

where a commutes with both b and c respectively (since the + operator is a generalization of single-nesting)



For + to be associative the following

```
(a, b, c) => (d, e) + (f, g, h) => (i, j)

produces

(f, *(a, b, c) => (d, e)) => (i, j)
```

```
(a, b, c) => (d, e, f) + (h) => (i)

produces

(*(a, b, c) => (d)) => (*(a, b, c) => (e, f), i)

(a, b, c) => (e, f, i)
```


```
x := (a b c) => (d e)
y := (f g) => (h)
z := (i j k) => (l)

(x + y) + z
d -> f
e -> g
(a b c) => (y(x(a b c)))
h -> k
(i j a b c) => ( z())


x + (y + z)
h -> k
d -> f
e -> g
```


Rank should be some constant which behaves in a predictable way under the operators. Ideally a * b produces rank(a) * rank(b) and same w/ +.

If rank is inputs - outputs, then `rank(a * b) = a.inputs * b.inputs - a.outputs * b.outputs` and `rank(a) * rank(b) = (a.inputs - a.outputs) * (b.inputs - b.outputs) = a.in * b.in - a.out * b.in - a.in * b.out + a.out * b.out` which only works if `a.out * b.out - a.out * b.in - a.in * b.out = a.out * b.out` so `2 * a.out * b.out = a.out * b.in + a.in * b.out`

Rank might be best represented as a complex number. If `rank(a) = a.in + i a.out` then `rank(a) * rank(b) = (a.in * b.in - a.out * b.out) + i (a.in * b.out + a.out * b.in)` which would need to be in an equivalence class with `(a.in * b.in) + i (a.out * b.out)`

fundamentally I'm looking for some f such that `f(rank(x), rank(y), *) = rank(x * y)`. f must be reducible to `f(a, b, *) = (re(a) * re(b)) + i (im(a) * im(b)) = ((a+a')/2 * (b+b')/2) + i ((a-a')/2 * (b-b')/2) = 1/4 (ab+ab'+a'b+a'b') + i/4 (ab-a'b-ab'+a'b')`

And the idea is the rank for addition should scale similarly. So in theory `f(rank(x), rank(y), +) = rank(x + y)` and we should do `f(a, b, +) = (re(a) + re(b)) + i (im(a) + im(b))`.

The * operator results in a difference of squares, something like (a.out * b.out) - (a.in * b.in). The + operator results in a straight ish sum, something like (a.out + b.out) - (a.in + b.in). This is the state today.

So what is rank(a * (b + c))?
`rank(a * (b+c)) = a.out * (b+c).out - a.in * (b+c).in`
`rank(a*b + a*c) = ((a*b).out + (a*c).out) - ((a*b).in + (a*c).in)`
`                = (a.out*b.out + a.out*c.out) - (a.in*b.in + a.in*b.in)`
`                = a.out (b.out + c.out) - a.in (b.in + b.in)`

Which since a can be arbitrary means it must be true b.X+c.X = (b+c).X which in general is not with the current metric.


Experimentally at least some functions pass for `(f1 * f2) + f3 = f1 * (f2 + f3)` and seem to only fail for size mismatches (or mismatched overflow counts - see [[additivity_check.py#^overflows-dont-match]] and [[additivity_check.py#^overflows-do-match]]).

`left outputs = f1.out * f2.out - min(f1.out * f2.out, f3.in) + f3.out`
`left inputs = f1.in * f2.in - min(f1.out * f2.out, f3.in) + f3.in`

`right outputs = f1.out * (f2.out + f3.out - min(f2.out, f3.in))`
`              = f1.out * f2.out + f1.out * f3.out - f1.out * min(f2.out, f3.in)`
`right inputs = f1.in * (f2.in + f3.in - min(f2.out, f3.in))`
`             = f1.in * f2.in + f1.in * f3.in - f1.in * min(f2.out, f3.in)`

Outputs:
`f1.out * f2.out - min(f1.out * f2.out, f3.in) + f3.out = f1.out * f2.out + f1.out * f3.out - f1.out * min(f2.out, f3.in)`
`- min(f1.out * f2.out, f3.in) + f3.out = f1.out * f3.out - f1.out * min(f2.out, f3.in)`

Inputs:
`f1.in * f2.in + f1.in * f3.in - f1.in * min(f2.out, f3.in) = f1.in * f2.in - min(f1.out * f2.out, f3.in) + f3.in`
`f1.in * f3.in - f1.in * min(f2.out, f3.in) = - min(f1.out * f2.out, f3.in) + f3.in`
`f1.in * (f3.in - min(f2.out, f3.in)) = -min(f1.out * f2.out, f3.in) + f3.in`
^inputs-and-outputs

Use the following script to generate test cases and insert into [[additivity_check.py#^mutual-associativity-hook]]
```python
def cond_output(f1_in, f2_in, f3_in, f1_out, f2_out, f3_out):
    return -min(f1_out * f2_out, f3_in) + f3_out == f1_out * f3_out - f1_out * min(f2_out, f3_in)

def cond_input(f1_in, f2_in, f3_in, f1_out, f2_out, f3_out):
    return f1_in * f3_in - f1_in * min(f2_out, f3_in) == -min(f1_out * f2_out, f3_in) + f3_in

import random

check_range = 5
while True:
    inputs = [random.randint(0, 5) for _ in range(6)]
    if cond_input(*inputs) and cond_output(*inputs):
        print(inputs)
        break
```

See [[additivity_check.py#^overflows-dont-match]] and [[additivity_check.py#^overflows-do-match]] - note that when the overflows match we seem to always get a match, and that when they don't we get very similar results.

The following script shows ~1.1% of the time we expect to find overflows matching w/ check_range == 100 but ~18% of the time w/ check_range == 5, so check_range reduces the probability of finding matching overflows
```python
def cond_output(f1_in, f2_in, f3_in, f1_out, f2_out, f3_out):
    return -min(f1_out * f2_out, f3_in) + f3_out == f1_out * f3_out - f1_out * min(f2_out, f3_in)

def cond_input(f1_in, f2_in, f3_in, f1_out, f2_out, f3_out):
    return f1_in * f3_in - f1_in * min(f2_out, f3_in) == -min(f1_out * f2_out, f3_in) + f3_in

import random

check_range = 100
are = 0
are_not = 0
for _ in range(10000):
    inputs = [random.randint(0, check_range) for _ in range(6)]
    if cond_input(*inputs) and cond_output(*inputs):
        are += 1
    else:
        are_not += 1

print(f'are {are} are_not {are_not}')
```



case 1 - `(f1 * f2) + f3`
case 2 - `f1 * (f2 + f3)`

So size mismatches are resolved when the following are true
`- min(f1.out * f2.out, f3.in) + f3.out = f1.out * f3.out - f1.out * min(f2.out, f3.in)`
`f1.in * f3.in - f1.in * min(f2.out, f3.in) = - min(f1.out * f2.out, f3.in) + f3.in`

Next question is what is the overflow on addition in each of the cases above. This conditional [[additivity_check.py#^add-dummy-indexes]] seems to cause the overflow issue to go away but does not affect the  /
zcdfffdds 1`

