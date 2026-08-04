
This document contains reflections that may prove useful in determining how to test for monotonicity.

A function is non-monotonic (in a particular ordering / permutation of truth values) if increasing any input's value leads to a decrease in any output's value

I would need a way to detect "less than".
I would need a way to increment.

How do I detect "less than"?

Easiest way is to define an "ordering" or "less than" function. The ordering function takes two (maybe kind of?) inputs and returns 1 if the left has a value less than the right. We can then detect less than by supplying f + t + lessthan. Can easily reframe this to gt, gt/eq, lt/eq as necessary.

How do I increment?

We basically need to test every adjacent pair of inputs. So start from (0, 0, 0, ...) then increment each in sequence recursively til we get to (N, N, N, ...). To simplify things, we can define t as the "lagged" version of f (and reframe to less than or equal to instead of less than). Basically, t (:= lagged(f)) must be less than or equal to f at every step. Note that t will have len(inputs of f) * len(outputs of f) outputs because it must compute the full output of f for each lagged input. Note also that t and f get the same treatment here

```
                 all Xs must be 1 always
lt or eq > _ _ | X1
lt or eq > _ _ | X2
lt or eq > _ _ | X3
---------------+------
           ___ |      
           ___ |      
           ___ |      
           ^ ^
           t f
```

It's trivially easy to define a "tee" function under + to allow t and f to get the same inputs. It's even easier to define one under * which just looks like (i) -> (i, i). Then the above is expressed something like

input * tee + t + f

and the requirement is that this is equivalent to the constant () -> 1 (or just whatever constant we define)

How do I define equality in this framework? Equivalent to a constant would be very nice given the need for this to play nicely with set-truth definitions. It's easy enough to define it as () -> (0, 0, 0, 0, ...)

This thread is getting away from the title of this doc, so I'm moving it to [[2024-12-22 defining `true` and `for all inputs`]]
