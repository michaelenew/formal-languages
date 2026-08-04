
It is important that N-valued logic AND and XOR have a way to expand parenthesized terms. In 2-valued logic this takes the form of distributivity, so if we are to have generalized AND and XOR be a strict superset of the 2-valued truth tables, distributivity must still be the way we eliminate parentheses in N-valued logic.

This document explores what must be necessary for distributivity to hold in higher dimensional logics

# Next thing to do (distributivity)...

Distributivity is nice but 

Need to figure out if there's any distributive law for the generalized AND and XOR.

AND = lambda a, b : a if a == b else 0
XOR = lambda a, b : abs(a - b)

(a XOR b) AND c
(a AND c) XOR (b AND c)

try for 3, 4, 5

(a XOR b) AND c = (3 XOR 4) AND 5 = 1 AND 5 = 0
(a AND c) XOR (b AND c) = (1 AND 3) XOR (2 AND 3) = 0 XOR 0 = 0

make a and b the same but c different

(1 XOR 1) AND 2 = 0
(1 AND 2) XOR (1 AND 2) = 0

make c = b - a
and  a != c
and  b != c
c = 1, a = 2, b = 3

(2 XOR 3) AND 1 = 1
(2 XOR 1) AND (3 XOR 1) = 0

# Maybe try instead...

defining as below (modify AND a little bit)

AND = lambda a, b : min(a, b)
XOR = lambda a, b : abs(a - b)

and check for distributivity...

(a XOR b) AND c = min(abs(a - b), c)
(a AND c) XOR (b AND c) = abs(min(a - c) - min(b - c))

this clearly doesn't work if a != b but c is 0.

# Okay different approach

Next thing to try is to construct a function that behaves properly in 3 truth values.

We know that in 2 truth values AND distributes over XOR

What must be true about the missing elements up to 3 dimensions to distribute?

Seems like XOR can probably stay as-is - it just seems right.

XOR:
```
0 1 a
1 0 b
e d c
```

AND:
```
0 0 f
0 1 g
j i h
```

For inputs 0,0,2

(0 xor 0) And 2 = 0 and 2
(0 and 2) Xor (0 and 2)

If 0 and 2 := 2 then 2 xor 2 == 2; if f := 2 then c := 2
Otherwise, 0 and 2 must be 0; otherwise, f == 0

For inputs 2,0,0

(2 xor 0) And 0
(2 and 0) Xor (0 and 0) = (2 and 0) Xor 0

For inputs 1,1,2

(1 xor 1) And 2 = 0 and 2
(1 and 2) Xor (1 and 2)

1 and 2 is bound by the same condition as 0 and 2, so 1 and 2 == 0 and 2; g == f

for inputs 1, 2, 2

(1 xor 2) and 2
(1 xor 2) and (2 xor 2) = (1 xor 2) and 0

->
  no consistency problems if b == 0 or 1
  if b == 2 then j == h

For inputs 0,1,2

(0 xor 1) And 2 = 1 and 2 = g
(0 xor 2) And (1 xor 2) = 

For inputs 2,2,2

(2 xor 2) And 2
(2 and 2) Xor (2 and 2)

->
  If 2 xor 2 := 2, then 2 and 2 == 2 (unlikely)
  If 2 xor 2 := 0, then c and 2 == h xor h

## assume f == 0

XOR:
```
0 1 a
1 0 b
e d 0
```

AND:
```
0 0 0
0 1 0
j i h
```

then c == 0
g == 0

h xor h is always 0, so "c and 2" == 0
-> c == 0, so 0 and 2 == 0 (already knew this)

### assume a == 2

XOR:
```
0 1 2
1 0 b
e d 0
```

AND:
```
0 0 0
0 1 0
j i 0
```

for 1, 2, 0

(1 xor 2) and 0 == b and 0
(1 and 0) xor (2 and 0) == 0 xor j

if AND is commutative, j == 0 so "b and 0 == 0" -> no limit placed on b

for 1, 2, 1

(1 xor 2) and 1 == b and 1
(1 and 1) xor (1 and 2) == 1 xor 0 == 1

-> "b and 1 == 1"

-> if b == 2, then i == 1
   otherwise, b == 1

for inputs 0, 2, 2

(0 xor 2) and 2 == 2 and 2 == h
(0 and 2) and (2 and 2) == 0 and h == 0
    0 and h is always 0 irrespective of h

-> h == 0

#### Assume both are comm

XOR:
```
0 1 2
1 0 1
2 1 0
```

AND:
```
0 0 0
0 1 0
0 0 0
```

Since "b and 1 = 1", b == 1

Per [[2025-01-20 (1) 3-valued distributivity.py]] This is distributive.


# Now try to build a dim=4 extension

(assume commutativity off the bat)

XOR:
```
0 1 2 a
1 0 1 b
2 1 0 c
a b c d
```

AND:
```
0 0 0 h
0 1 0 i
0 0 0 j
h i j k
```

(a xor b) and c = (a and c) xor (b and c)

for 0, 0, 3
(0 xor 0) and 3 = 0 and 3 = h
(0 and 3) xor (0 and 3) = k xor k

## Assume a=3, b=2, c=1, d=0

XOR:
```
0 1 2 3
1 0 1 2
2 1 0 1
3 2 1 0
```

AND:
```
0 0 0 0
0 1 0 i
0 0 0 j
0 i j k
```

k xor k = 0 -> h = 0

for 0, 1, 3
(0 xor 1) and 3 = 1 and 3 = i
(0 and 3) xor (1 and 3) = 0 xor i
-> i = i (no information)

for 0, 2, 3
(0 xor 2) and 3 = 2 and 3 = j
(0 and 3) xor (2 and 3) = 0 xor j
-> j = 0 xor j = j (no information)


for 0, 3, 3
(0 xor 3) and 3 = 3 and 3 = k
(0 and 3) xor (3 and 3) = k xor 0 = k
-> k = k (no information)

for 1, 3, 3
(1 xor 3) and 3 = 2 and 3 = j
(1 and 3) xor (3 and 3) = i xor k
-> i xor k = j

## Never mind just brute force it...

Can check the output of the section [[2025-01-20 (1) 3-valued distributivity.py]] check_every_4() to find that there is exactly 1 definition of AND that distributes over the "feels right" generalized XOR defintion. See below:

Successful test for
  xor
    0 1 2 3
    1 0 1 2
    2 1 0 1
    3 2 1 0
  and
    0 0 0 0
    0 1 0 1
    0 0 0 0
    0 1 0 1

Also check the section check_6() to show that this pattern generalizes up to 6 dimensions (i.e. and is 1 if a and b are odd, otherwise 0)


