
The monotonic functions from Post's functional completeness function need to be generalized.

In particular, monotonicity requires determining an order of the inputs which is considered ascending. The choice of order does not matter in 2 valued logic but does matter in higher valued logic. The choice only matters as long as it causes the cycle of the ordering to be different (and not simply in reversed order)

The simplest case where this matters is in 4 dimensions where you can permute 1 2 3 4 and 1 3 2 4 to get different cases. Each of these present a different monotonicity condition.

To see that this is the case, consider the functions

1 | 2
2 | 2
3 | 2
4 | 3

vs

1 | 3
2 | 3
3 | 3
4 | 2

The first is monotonic in the ordering 1 2 3 4 but not 1 3 2 4, and the second is monotonic in the ordering 1 3 2 4 but not 1 2 3 4. Every monotonicity ordering is preserved when composing two functions with that monotonicity, therefore every ordering must be violated by at least one function for the set to be functionally complete.
