
If it's possible to construct an "if" or an "increment" function based on an arbitrary input function and for a specific arbitrary choice of input, then it must also be possible to construct every function.

XOR looks like

```
0 1 2 3 4 5 6 ...
1 0 1 2 3 4 5 ...
2 1 0 1 2 3 4 ...
3 2 1 0 1 2 3 ...
4 3 2 1 0 1 2 ...
...
```

AND looks like

```
0 0 0 0 ...
0 1 0 0 ...
0 0 2 0 ...
0 0 0 3 ...
...
```

and we have every nilary function to work with as well.

It is easy to "choose" an index using XOR as long we have every nilary. Simply (for input vector i) take

```
(i[0] XOR const_x) AND const_1
(i[1] XOR const_y) AND const_1
...
```

where each of the above terms evaluates to 1 i[x] are equal and 0 otherwise. We can then reduce all those terms to a single 1 or 0 by just ANDing them all together

Now to get an "increment" function, all we need is effectively an "add" function.

XOR is already essentially a "subtract" function. The problem with using raw XOR is that 0 0 results in 1 when it should result in MAX_VAL (whatever that is...). The problem seems to be that XOR as you go away from the main diagonal will never wrap back around to 0. In a sense it is "uninformed" about what the max truth value is, which means it cannot ever achieve a modulo situation without other inputs.

A reasonably elegant resolution to this tension would be if it's the user's choice. Basically your increment function depends on the max valued constant function you include in your logic. Something like "if i == 0 const_max, otherwise i XOR const_1"

*Note* it's trivially easy to get this to rephrase as "if i == const_max then const_max else i XOR const_1" if that helps.

# iff...

So we actually arrive at a situation wherein these two functions (in the presence of all nilary functions) are FC iff they can produce the function "if i == 0 const_max, otherwise i XOR const_1". If this subfunction can be constructed we have a machine to produce any function at all, and if it can't these aren't FC (by counterexample)

Let's start by trying to construct a non-degenerate function that maps i=0 to const_max

XOR(i, const_max) obviously does this.

Now let's try to get 0 and 1 to differ by more than a single increment.

something like (i XOR 2) AND 2 maps i=0 to 2 and i=1 to 0. Everything but 2 gets mapped to 0.

Here's something weird to think about...

If we allow const_max *plus one* then this solves our problem. We just take

```
(i[0] XOR const_x) AND const_max+1 ---
                                       \
(i[1] XOR const_y) AND const_max+1 ---- AND
                                          \
(i[2] XOR const_z) AND const_max+1 ------- AND
...                                          \
```

Which is `if <selected pattern> then const_max+1 else 0`

Then we take that and go `(if <selected pattern> then const_max+1 else 0) XOR 1`

# Putting a pin in an open question...

The result "AND, XOR, and all constants up to N are FC in N-1 logical values" is (probably) sufficient to solve finite games. If N-1 is finite then N is also finite.

Further implications of this construction might depend on whether it's FC in N logical values as well. For now we don't need to prove that.
