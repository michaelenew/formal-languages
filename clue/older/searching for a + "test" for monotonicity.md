
Question of this document is whether it is possible to describe monotonicity as some relationship with another function (probably commutativity) under +

Using the definition of + from [[removing double casing on +]]

In order for the relation to be commutative, consider taking something like

1 | 1
2 | 2
3 | 2
4 | 2

And limit ourselves to just one output. Since the right side must be the output always, the function this would test must ONLY have 1s and 2s as its output in the subdomain of only 1s and 2s as inputs.

NOT RIGOROUS: seems like only the indentity will have the appropriate range. It's definitely possible that some fixed choice of function or functions would degenerate such that not all possible outputs would appear in any one test, but this seems like a less promising route than...



It's also possible that the function must test itself under this definition. BUT note that "commutativity" doesn't directly apply here as noted in [[defining "test" and "commute" for *]]. In order to define a meaningful test of a function with itself we would need to come up with some corollary of "transpose" in the * definition.

One thing that jumps to mind for the corollary of transpose is reversing the order. So something like (f + f)(X) = (f + f)(X[ ::-1 ])


