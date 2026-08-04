One good way of constructing higher dim functions: Take an invertible function of any arity and dim d, then increment dim to d+1. Make one copy of the original table for each i up to d, replacing i with d+1. Nix any duplicate rows (which are rows with no i). New function is necessarily invertible. Seems probable the new function inherits some completeness properties too.

What does this look like for xor?

```
0 0 | 0
0 1 | 1
1 0 | 1
1 1 | 0
```
becomes
```
0 0 | 0
0 1 | 1
1 0 | 1
1 1 | 0

2 2 | 2
2 1 | 1
1 2 | 1
1 1 | 2

0 0 | 0
0 2 | 2
2 0 | 2
2 2 | 0
```

\* only "works" if constancy holds for the function

Are there other extensions that "work" for other inheriting conditions?
