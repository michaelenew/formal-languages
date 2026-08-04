
All of the work in this section relating to Post's FC theorem and generalizing the tests for true-preserving, false-preserving, linear, and self-dual is easily approached in a framework where functions have N inputs and 1 output. Furthermore, this only involved the * operator.

Allowing inclusion of more than one output (allowing N inputs and M outputs) is in search of another operator that will allow us to more easily approach the last of Post's 5 conditions - monotonicity.

One attempt at finding such an operator is the + defined in [[Additive (+) operator]]. We want + to do two things:

- Be associative. 
- Be inclusive of function _evaluation_.

We want to be able to compose a bunch of functions that look like () -> (1) like (f + g + h + ...) then apply that to some complex function as an "evaluation" of that function. This means we can now define "evaluation" in the framework of this generalized function composition operation. It also means we must have a concept of "multiple outputs" since we must encode arbitrarily many values to be used to evaluate whatever function, e.g. (f + g + h + ...) must look like () -> (1, 2, 0, ...). This means that everything we ever want to do with our function is within the closure of our framework
