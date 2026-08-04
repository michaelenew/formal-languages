
The problem I'm facing is this.

In the original formulation, a setwise operator (e.g. xor) was related to the bitwise operator like this

```
Def set_op(A, B):
  Result = set()
  For elem in U:
    If bit_op(elem in A, elem in B) == 1:
      Result.add(elem)
```

Where this is all well defined because the bit op will only ever return 0 or 1

Since then, I've defined "contains" and "union" in terms of set operations, as well as 0 and 1 in terms of sets, which in theory means I can reformulate this to be a recursive definition.

The problem is two fold.

First, I've violated the natural assumption that the bit ops only output 0 or 1. This is the big one - what do I do when xor(a, b) == 5? The prior proposal was to allow multiple concepts of contains - you are "5 in" the set. This is more like "where in this set are you" than "are you in this set" - you are "in section 5".

Second, the definition for "contains" outputs the set containing only the element or the empty set, not 0 or 1.

The tension arises because i have assigned sets as numbers. Before, the bit operators were distinct from the set operators. Now it is not so clear.

A natural generalization to the above is to say that the result set is the union (or xor) of the elementwise contains operators, like this

```
Def set_op(A, B):
  Result = set()
  For elem in U:
    Result = Result union Set_op(A intersect {elem}, B intersect {elem})
```




The sections approach has some merit now. Each element exists in a section and goes to the resultant section.

```
Def set_op(A, B):
  Result=sectionset()
  For elem in U:
    a = Whereiselemin(A)
    b = Whereiselemin(B)
    Respos = elem_op(a,b)
    Result[respos].add(elem)
```

The question is how do things get into "higher" positions in the first place? And why?

(This was my original formulation - 3 actually means "in 0 and 1 positions" Because 3 = 2^0+2^1)


