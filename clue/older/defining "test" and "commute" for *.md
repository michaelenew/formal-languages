
Just now I got confused about what commutativity meant for * because I remembered that * commutativity of a function with itself implies linearity (in the Post's theorem sense). But of course a * a = a * a always so why is that special...

The point is that we actually TRANSPOSE ([[defining input transpose by * and +]]) the inputs and check for commutativity that way. So we're not actually checking for true commutativity, it's just something adjacent to commutativity.


b > ?   ?   ?   |  ??
----------------|-----
b > Y0  Y1  Y2  |  ?
b > X0  X1  X2  |  ?
b > W0  W1  W2  |  ?
    ^   ^   ^      ^
    a   a   a      c


Here what we're really saying is that (a * b)(X) = (b * a)(X^T). When a=b, this becomes (a * a)(X^T) = (a * a)(X) but when X is 0 or 1 dimension this (effectively) becomes (a * b)(X) = (b * a)(X)

This distinction doesn't matter at all for functions of arity 0 or 1 (which all other tests of interest in 2 valued logic are) because this is actually equivalent to true commutativity. For this reason it's easy to miss and we should probably choose a different term for it.

I think I use the term "test" everywhere else, so I'm going to continue using that even though it's a bit of an odd term. Will revisit this later.
