
What we want to do in this doc is eliminate the casing where the + operator behaves differently based on whether the left outputs are > the right inputs or not. Right now the resultant size of the function looks like:

diff=max(l2-r1, 0)
(l1 | r1) + (l2 | r2) -> (l1+l2-r1 | r1-l2+r2)

But we'd like to not have the resultant size be cased with the max() function.

important is:
- There must still be an identity and it should be unique (currently () -> () is the ident)



Right now we can look at the the inputs by lining the left and right up like so:

_ _ _ _ _|_ _ _
          _ _ _ _ _|_ _ _

and in the other case where left outputs exceed right inputs:

_ _ _ _|_ _ _ _
        _ _|_ _ _


in this world everything input and outputs are inherently finite. No adding dummy indices and keeping the "same" function

but actually adding identity indices is fine... as long as we shuffle the order so that appending always adds to the end furthest from the |

It's convenient for everything to be written the same direction, so we can do

| _ _ _ _ _
> _ _ _ _ _ _ _
(+)
| _ _ _
> _ _

So that when the left outputs are too long, I can extend with IDENTITY indices on both the inputs and outputs like so:

| _ _ _ _ _
> _ _ _ _ _ _ _
(+)
| _ _ _ i i i i
> _ _ i i i i i

Which is natural, eliminates the double casing, and lets us conceptualize all functions as having infinite inputs and outputs (just only some are important)

and in this conceptual infinitization, () -> () is the same as every identity, which is I guess worth noting because now * and + share the same identity

() -> () is no longer a null for * though, which is also worth noting.

The way to think about this is that every unspecified output value just matches the input value at the same index




Is it associative?


| _ _ _ _ _ _ _ i
> _ _ _ _ _ _ _ i
(+)
| _ _ _ _ _ _ _ i
> _ _ i i i i i i
(+)
| _ _ _ _ _ _ _ i
> _ _ _ _ i i i i


call above f+g+h

(f+g)+h >0 = (g[f[f's inputs]]) + h[h's inputs] >0 = h[g[f[f's inputs]]] >0

f+(g+h) >0 = f[f's inputs] + (h[g[g's inputs]]) >0 = h[g[f[f's inputs]]] >0

and repeat for all indices. Or just like ya know get rid of the index bit and it's just normal composition of vector functions





Q: Does this help me describe monotonicity as commutativity under + with some function?
[[searching for a + "test" for monotonicity]]
