
This doc deals with defining testing conditions fully within the context of the framework. Statements of import have been written like `a equal b for all inputs`, but only a and b are defined, not "equals" or "for all inputs"

From the backlink in [[2024-12-22 what do I need for monotonic]]: Equivalent to a constant would be very nice given the need for this to play nicely with set-truth definitions. It's easy enough to define it as () -> (0, 0, 0, 0, ...)

Previously when defining * we left the definition as

input + (f * t) = input + transpose + (t * f)
_for all inputs_

but "=" is not well-defined in this framework. It would be more convenient to define a "true" function and find a relation which is true in the above case and false otherwise.

The "=" function is easy enough to define as (i, j) -> {i=j: 0, otherwise: 1}, so that the expression would be 

`input + (f * t) + input + transpose + (t * f) + eq`

Now we also don't have a definition of "for all inputs". It's easy enough to define a nilary function "V" which enumerates every permutation of outputs which we feed to f as (V + f + f + f + f + ...), but then (f + f + f + f + ...) should be expressible as

`(f * tee(len(f)))`

where

```
tee(j) := (i) -> (i, i, i, ...)
                 |--j times--|
```

so the whole thing gets written as

`V + (f * t * tee) + V + T + (t * f * tee) + eq`


