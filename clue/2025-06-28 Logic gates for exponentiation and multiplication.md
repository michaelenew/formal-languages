


The mod 2 operator is simply `a := a&1`

The + operator is `a + b := a ^ b ^ INC(a&b)`

** Just thought of something - I can consider an infinite series of increments of a set to be a new elementary symbol. This may solve some problems

# Multiplication

Doing this is as iterative setwise multiplication

0 * A ^ 0, 1 * A ^ A

define !A to be the infinite series A ^ INC(A) ^ INC(INC(A)) ^ ...
    If !(AB), then
    ```
       1  A0   A1   A2   A3 ...
    1  1  A0   A1   A2   A3
    B0 B0 A0B0 A1B0 A2B0
    B1 B1 A0B1 A1B1 A2B1
    B2 B2 A0B2
    ...
    ```
    Would be (!A)(!B) - note everything appears once
    Then
    ```
          1    A0    B0   A0B0   A1   B1   A0B1
    1      1    A0    B0   A0B0   A1   B1   A0B1                     
    A0     A0   A0                                 
    B0                B0                         
    A0B0                                          
    A1                                          
    B1                                          
    A0B1                                          
    ```

    

Then c * A := !c & A where c := 0 or 1
    because !c is empty if c is 0 and every set if c is 1

So generally we want A + B. Iterate through elements of A

A[0] * B = !(A&1) & B
A[1] * B = !(A&2) & B
A[2] * B = !(A&4) & B
...

Add these together

`(!(A&1) & B) + (!(A&2) & B)`
`!(A&1) & B ^ !(A&2) & B ^ !(A&1) & B & !(A&2) & B)`

# Exponentiation

The logic gates for exponentiation 

NOTE: the logic gates for exponentiation should ideally make obvious the fact that INC(INC(INC(1))) is equal to 2 ** 2 (and so on for all powers)

Can I convert a number to a floating point representation? This would require taking the floored log... But floored log is really just "what's the largest component you have". It kind of already is in floating point representation come to think of it...


