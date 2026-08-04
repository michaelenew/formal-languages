
# Thought: Can I express higher dimensions in 2 dimensions?

The 2 dimensional logic is relatively simple. I have some sets (symbols) that form terms (intersections). Terms get unioned together when I take A intersect B.

In theory I can define relationships between symbols, represented by meta-symbols. I can say things like

`X ^ ABC` and `Y ^ DEF` and `(X ^ Y) ^ <something>` where `<something>` describes how the symbols X and Y combine.

I could define special symbols for set sizes. It would be a single symbol defined such that (some operation) on every set and only sets of size N results in 0. This really feels like it needs sizes...

The operator that is 0 if exactly one of its inputs is 0 is AND. If I have known elemental sets. I don't have the idea of 0, just "in" or "out of" the set. So what I can do is define a condition: Define X as a set and Y as an elemental set.

A set X contains another set Y if XY (intersection is 0) BUT there's some symbol defined to represent the set containing just the set Y called Z where XZ ^ Z (Z is in X). The relationship between Y and Z is "meta" in a sense because I as the writer of the logic define and keep track of Z as the set containing the set Y, but this fact isn't really encoded in the logic anywhere.

Now if I have every elemental set, I can define the relevant meta symbols for "size 3". Just define new symbols for every set of size 3 (S3_i := A union B union C for each combination of elemental sets A, B, C) and define one set which contains all and only these new symbols, called S3. We also define a new symbol X1, which is the set containing just X. Then the check for if a set X is size 3 is simply S3X1 ^ X1.

# So basically

This is much less elegant than defining set sizes using higher dimensions, but it should work.

In practice, each combination of symbols gets a meta symbol. The relationships between meta symbols and their underlying symbol combinations have to be tracked outside of the truth statement (this is the biggest inelegancy). Also each meta symbol can have its own meta symbol. To track this in the real world we would make meta symbols implicit based on need and only instantiate one when it's relevant to the truth statement.

So usually we would end up with N parallel truth statements. It seems like a rarity you would ever want to track a symbol's interaction with a meta symbol (because they're defined to be disparate...). You would end up with something like

level 0: `A ^ B ^ ABC ^ ...`
and, in parallel
level 1 (meta): `A_meta ^ (AB ^ C)_meta ^ ...`

and we keep going with level 2 (meta meta) and so on. This is JUST A PRACTICAL THING since we rarely have non-meta and meta symbols interact. The "real" truth statement is much larger where we define every meta symbol to be disjoint with every non-meta symbol and union all levels together together.

Checking the truth of an assertion is then done in the usual way by checking if all terms cancel when we take A ^ AT.

# This is the make it work part

We make it work, make it good, make it fast, in that order. This makes it work.

TODO is to write this in code and check that it works. This is tractable and expressible and should be sufficient to solve the information problem in Clue.

Other TODO is figure out better ways to express this. Determination of size here is incredibly inelegant - build the union of "(number of elementary symbols) choose (size of set)" sets is pretty gruesome, even if it works.

# Maybe a problem...

The fact that the truth statement itself cannot be used to back out which sets are of size 3 is concerning. Basically a meta size set S will relate the same (disjoint to every non-meta set and every other meta set except those that are meta symbols of sets of size 3).

**Precise formulation**: Can we tell that, for elementary A and B, the meta set `{A ^ B} == {A ^ B ^ AB}` (adopting () means meta)? If we can then the gap should be bridged.

If A and B are elementary, `AB`. Meta tenets for `{A ^ B}`: `A{A ^ B}` and `B{A ^ B}`. Meta tenets for `{A ^ B ^ AB}`: `A{A ^ B ^ AB}` and `B{A ^ B ^ AB}` and `{A ^ B}{A ^ B ^ AB}`

Now I can do T:=`(AB) U (A{A ^ B}) U (B{A ^ B}) U A{A ^ B ^ AB} U B{A ^ B ^ AB} U {A ^ B}{A ^ B ^ AB}`

TODO for next time is expand this out and see if `T({A^B} ^ {A^B^AB}) ^ ({A^B} ^ {A^B^AB})` cancels to 0 terms (i.e. the relationship is encoded)

# Continuing (2025-03-22)

Based on `2025-03-22  meta symbols.py` the missing information to deduce that the meta symbols for `{A ^ B}` and `{A ^ B ^ AB}` are equal is:

`A&B&{A ^ A&B ^ B} ^ A&B&{A ^ B} ^ A&{A ^ A&B ^ B} ^ A&{A ^ B} ^ B&{A ^ A&B ^ B} ^ B&{A ^ B} ^ {A ^ A&B ^ B} ^ {A ^ B}`

Imma break this out a little bit.

```
  A&B&{A ^ A&B ^ B}
^ A&B&{A ^ B}
^ A&{A ^ A&B ^ B}
^ A&{A ^ B}
^ B&{A ^ A&B ^ B}
^ B&{A ^ B}
^ {A ^ A&B ^ B}
^ {A ^ B}
```

Factoring (U is the "universal set"):
`(A ^ B ^ A&B ^ U) & ({A ^ B} ^ {A ^ A&B ^ B})`

So this is "the inverse of A union B intersected with the meta sets of interest"

Here is a proof that {A ^ B} ^ {A ^ B ^ AB}:

```
  A&B&{A ^ A&B ^ B}&{A ^ B}
^ A&{A ^ A&B ^ B}&{A ^ B}
^ B&{A ^ A&B ^ B}&{A ^ B}
^ {A ^ A&B ^ B}
^ {A ^ B}
```

## Hmm...

Every statement has a minimal form. Therefore the minimal proof that `{A ^ A&B ^ B} ^ {A ^ B}` must be `{A ^ A&B ^ B} ^ {A ^ B}`. This means that every statement which shows `{A ^ A&B ^ B} ^ {A ^ B}` can be factored into `({A ^ A&B ^ B} ^ {A ^ B}) | residual`. It is therefore not possible to construct an inference that `({A ^ A&B ^ B} ^ {A ^ B})` without directly encoding this information, i.e. by encoding information without these symbols explicitly. Essentially it's not possible for anything related to the symbols A and B to matter here since the minimal form of the evidence (`{A ^ A&B ^ B} ^ {A ^ B}`) doesn't mention A or B.
