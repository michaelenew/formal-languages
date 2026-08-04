
When last I left this, I had two ideas for how to proceed:
- Try to define the operator f(a)=a+1 in terms of other operators. I had previously tried to define a+b and didn't have much luck
- Explore semantic minimality a little more. Right now A, 2A, !A are semantically completely distinct(irreducible symbols), but of course knowing any of them determines the others. The identity !A ^ 2!A ^ A reduces the semantic degrees of freedom by 1, leaving 2, but we need to get to 1. One idea was to incorporate f(A) := 2 ** A or f(A) := A+1 and find identities with that new operator (This might help if e.g. every trio of operators yields a new identity, then we'd introduce 1 dof but take away 3...).
    - A useful practical exploration could be to see what extra statements (if any) are determined with the introduction of the identity !A ^ 2!A ^ A

Recording some stuff not yet recorded here:
- Every ! has an inverse (as proven by the identity !A ^ 2!A ^ A -> A' ^ 2A' ^ !inv A' after symbol substitution !A := A' forcing A := !inv A')
- Every 2 has an inverse. !A ^ 2!A ^ A. B := 2A implying 2inv B = A. 2inv B ^ !B ^ 
- ! does not distribute over & in a nice and obvious way (though unproven if there's no distributive rule at all)


