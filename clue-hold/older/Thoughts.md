I wonder what turing machines are equivalent to the various functions?

Is the set of n-dimensional functions a group? Under what operation (can I use my composition operation?)? Still need to understand the relationship between elements and transformations
- elements and transformations illustrates a fundamental weakness of groups (maybe), which is that they can't (maybe) Represent the thing they act on. Consider the binary functions. The requirement of identity and inverse means that the nilary functions can't be included. Since nilary functions are the data elements, i.e. the thing the group elements act on, the group itself falls short in representing these. Note also that the nilary functions are essentially the zeros of the group.

One good way of constructing higher dim functions: Take an invertible function of any arity and dim d, then increment dim to d+1. Make one copy of the original table for each i up to d, replacing i with d+1. Nix any duplicate rows (which are rows with no i). New function is necessarily invertible. Seems probable the new function inherits some completeness properties too.

Question: is there a way for non-FC functions of dimension d to be complete up to dimension d' < d?