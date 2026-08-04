
The crux here is that you can represent a N-ary function f(a, b, c, ...) as a table within relational calculus with 3 columns - row, col, val.

# Building up the table
The most natural way to build up a table is to take a copy of the prior table and append either a 1 or a 0

```
0 | _
1 | _

Then

0 0 | _
1 0 | _
0 1 | _
1 1 | _

and so on
```

Last detail here. To further reduce the number of "kinds" of thing, it's possible to consider each row with an infinite tail of trailing 0s.

# Converting to r/c/v notation

Note that most of the row/col/val pairs are redundant (everything left of the | ). Note also that val is inferable based on row/col for the redundant table. Note as well that col doesn't need to be specified for the unique information (everything right of the | )

The redundant table `R` can be represented as the set of all rows and cols. The row indices range over 2^max(col index).

In the above expansion, for `R`, `R.v = floor(R.r / 2^R.c) % 2`, though it might be more convenient to try and find something without a floor in it and without a `mod 2` (since that will go away eventually)

# What's a composition

To insert the result of one function`T` into another `F`, join from `U.v` to `R.v`

I need to get the row of the combined function and pair that row calc with `F.v`.

## The row/col calculation problem
The _column_ associated with two input columns can be calculated via diagonalization.
```
F.c + T.c = Lateral

Area = 1 + 2 + 3 + 4 + ...
L =    2,  3,  4,  5,  ...

Area = (L-1)(L-1+1)/2 = L(L-1)/2

Then choose one or the other to add and
New.c = F.c + (F.c + T.c)(F.c + T.c - 1) / 2
```

This gives me _values_ and _columns_ for a particular input. Given these, how do I back out the row? The first value being a 1 adds 1. The second adds 2. The third adds 4. And so on adding 2^i each time.

```
0 | _       1 ^ 0


0 | _       2 ^ 1
1 | _


0 0 | _     3 ^ 2
1 0 | _
0 1 | _
1 1 | _

0 2
2 0
1 2
2 1
2 2

N^2 - (N-1)^2 = 2N - 1
```

## What does this look like
```
SELECT
    UF.v as v
    <something> as r
FROM UT, RT, UF, RF
WHERE
    UT.r = RT.r     -- Complete T
    UF.r = RT.r     -- Complete F
    UT.v = RF.v     -- Insertion
```


For the output:
row = sum(val * dim ^ col)
col = (F.col + T.col)(F.col + T.col - 1) / 2
val = floor(row / dim^col) % dim

For minimal information, R can just be the set of all pairs of indices. Row determines the sequence of values as val = floor(row / dim^col) % dim and col determines the value.

RT.col is vertical index
RF.col is horizontal index
resultant col = (RF.col + RT.col)(RF.col + RT.col - 1) / 2
resultant row = sum(RT.val * dim ^ ((RF.col + RT.col)(RF.col + RT.col - 1) / 2))
```
SELECT
    UF.v as v
    sum() as r
FROM UT, RT, UF, RF
WHERE
    UT.r = RT.r     -- Complete T
    UF.r = RT.r     -- Complete F
    UT.v = RF.v     -- Insertion
```


