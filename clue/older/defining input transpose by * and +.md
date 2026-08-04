
This document tries to define "transpose" as mentioned in [[defining "test" and "commute" for *]] in terms of + and/or \*

For \* the first thing to remember is that we have to have a well-defined order of inputs in the final function. A property that (probably) would be nice to preserver is that in the matrix-input definition the reversal of order allows a map from the original matrix indices like `(a, b) -> (b, a)`, so essentially we want a transformation (call it `$ T`) such that if the following is true, we can say "t tests f (under * )"

input --($ T)--> x
    \              \
  (f * t)        (t * f)
      \              \
        y --($ T)--> output

In other words, t tests f iff $ T is "antilinear" over f * t for all inputs

input + (f * t) $ T = input $ T + (f * t)

# Trying w/ * ($ := * )

If * can be used to define the transpose, then we have to apply (* T) to some nil-ary function and get out the opposite order of outputs

T >  x4 |  y4
T >  x3 |  y3
T >  x2 |  y2
T >  x1 |  y1
--------+-----
     ^
     (inputs are nil-ary)

It's clear that the only way this can happen is by reframing how we think about the order of outputs from the * operator - as in, by default, they are transposed. As in the inputs () -> (x1, x2, x3, x4) * (y) -> (y) := (x4, x3, x2, x1). Reframing in this way is reasonably elegant because I then can remove the need for an additional operator and all results on single- and 0-output functions still apply.

It does have the problem that there cannot be a true identity without double-application (you must do a * I * I to get back to a), BUT if * is still associative then it MUST be true by closure of * that (I * I) is in the same set. In other words (and this is weird) the operator we were calling "I" before is NOT the identity, it is in some sense I = (the actual identity) ^ (1/2) and the identity would then be defined as (I * I). This is kind of weird, but it gives a sense in which we apply "half" of an operator (TODO: add a link to a doc?). This is kind of like "drilling in", in the sense that all the other work in this document where we talk about a t or an f there is a corresponding t' or f' as t' = (t * I) or f' = (f * I). What I'm getting at is this gives every function an evil twin (except functions with < 2 outputs because reversing the order of a sequence of length 0 or 1 gives the same output)

Future me: This thought on evil twins is incomplete and might have promise... but I'm going to work on + for a while now and see if something jumps out.

# Trying w/ + ( $ := + )

The + operator seems naturally suited to the task of reordering inputs. What is important for this function (call it r) is that it has the following relationship with the function that takes the 2d inputs of * (call them i, j) and returns the output ordering (call it o) and reorders them such that

r(f(i, j)) = f(j, i)

It's also pretty easy to see that when f * t is single-output (or any other case where T * h = h * T) t tests f iff they are "antilinear":

input + (f * t) + T = input + (f * t)
input + T + (t * f) = (input + T) + (t * f)
-> (input + T) + (t * f) = input + (f * t)


