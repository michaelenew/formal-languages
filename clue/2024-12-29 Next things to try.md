This document records useful tractable problems to explore next.

# First

check whether generalizations of XOR and AND are functionally complete. The natural expansions would be

XOR := abs(a - b)

And

AND := a if a==b else 0

Of course including the constant TRUE (and maybe others) to achieve FC

Notably, the extension of OR here would be OR := a if a == b else abs(a - b). This extensions preserves the relation from 2-valued logic that `A XOR B XOR (A AND B) == A OR B`

# Second

try and understand which, if any besides the nilaries, functions cannot compose to the identity. In 2 valued logic it seems like every function in isolation can compose to the identity. This is useful in figuring out which commutativities can be gained
