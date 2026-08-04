
Here's a way to construct symbols / numbers:

numbers are defined as sum(2 ** n for n in set)

0 := {}
1 := {0}
2 := {1}
3 := {0,1}
4 := {2}
...

This is important because it creates a natural "canonical set of size N". In particular, the first set of size N is 2 ** N - 1 and we can label this as the canonical set of that size.

The size operator would then not be the increment operator defined previously. The size operator would be

```
0 1 1 2 1 2 2 3 1 2 2 3 2 
```

This natural size is the Hamming Weight, and it has no known closed-form algebraic solution as far as I can tell.

Does this size operator distribute over ^ and &?

try

`size(2) ^ size(3) = size({1}) ^ size({0, 1}) = 1 ^ 2 = {0} ^ {1} = {0, 1} = 3`
`size(2 ^ 3) = size({1} ^ {0, 1}) = size({0}) = 1`

so not over ^.

`size(2) & size(3) = size({1}) & size({0, 1}) = 1 & 2 = {0} & {1} = {} = 0`
`size(2 & 3) = size({1} & {0, 1}) = size({1}) = 1`

# Integer Addition in these operators

Addition of the integer sets is defined as a ^ b ^ inc(a&b) (adapted from standard binary addition)

# The set containing A is...

0 := {}
The set containing 0 is 1
The set containing 1 is 2
And in general the set containing N is 2 ** N

So when I have a symbolic set I need to find a way to take 2 ** A





# 2025-05-14
XOR(A,B) = 2 ** XOR(LOG2(A), LOG2(B))
AND(A,B) = 2 ** AND(LOG2(A), LOG2(B))
2A = 2 ** PLUS1(LOG2(A))



# 2025-06-10 - obvious truths about size operator
S(XOR(A, B)) ^ (S(A) + S(B))    iff.  AB

Therefore

S(A ^ B) ^ (S(A) ^ S(B) ^ INC(S(A)S(B))) ^ AB

Letting B := A

S(0) ^ S(A) ^ S(A) ^ INC(S(A)) ^ A

implying INC(S(A)) ^ A

S(0) ^ 0
S(1) ^ 1
S(2) ^ 2
...


