
By spot checking, AND distributes over some false preserving functions and does not distribute over some non false preserving functions. Test conjecture that AND distributes over all and only false preserving functions

Can check [[2025-02-06 what does AND distribute over.py]] - this is indeed the case.

False preservation is equivalent to commuting under * with FALSE:=() -> 0

So for some reason it seems that f * FALSE == FALSE * f <-> (a F b) AND c == (a AND c) F (b AND c)

What does distributing look like in terms of * ? For unary functions it implies f(t(a), t(b)) == t(f(a, b)). This is similar to distributivity, which is just saying f(t(a, c), t(b, c)) == t(f(a, b), c)

Note that for * combining two binary functions we get f(t(a, b), t(c, d)) == t(f(a, c), f(b, d)) for all combinations of a, b, c, d. We can take a subset of combinations. Take t:=AND and set d to 1. Then t(c, d) == c and we get f(AND(a, b), c) == AND(f(a, c), f(b, 1))

# Proof that AND distrib is sufficient for false preservation

If it's false preserving then f * FALSE == FALSE * f. Also AND is false preserving. If

AND(F(a, b), c) == F(AND(a, c), AND(b, c))

then

FALSE() * AND(F(a, b), c) == FALSE() * F(AND(a, c), AND(b, c))

and

AND(FALSE(), FALSE()) == FALSE() == FALSE() * F(AND(a, c), AND(b, c))

and since anything * FALSE() == FALSE(), we can sub in F(AND(a, c), AND(b, c)) * FALSE() for FALSE() and get

F(AND(a, c), AND(b, c)) * FALSE() == FALSE() * F(AND(a, c), AND(b, c))

and since we can choose any a, b, c, d to produce any combination of inputs to F, it must be true that F * FALSE == FALSE * F. In other words, AND distributing over F is sufficient to show F is false preserving.

Essential elements of the proof:
- AND is false preserving <-> AND * FALSE == FALSE * AND
- AND's outputs span the truth values
- anything * FALSE == FALSE


# (Attempting) Proof that AND distrib is necessary for false preservation

If F is false preserving then must it be true that AND distributes over it? Start by assuming F is false preserving...

FALSE() * F(a, b) == F(a, b) * FALSE()

without loss we can sub in a := AND(c, d) since AND spans all outputs

FALSE() * F(AND(c, d), b) == F(AND(c, d), b) * FALSE()

There's no inverse operation for FALSE * which makes it hard to generalize to indices other than 0, 0, 0, ...

it must be true that only the 0, 0 slot (as in the output of F(0, 0)) makes a difference. Is it possible to show that every other position doesn't affect AND distributivity?

So essentially in AND(F(a, b), c) == F(AND(a, c), AND(b, c)) (definition of distributive) it must be true that only when F(0, 0) comes up can a contradiction occur.

So statements like AND(F(0, 1), 1) == F(AND(0, 1), AND(0, 1)) must always hold true for every F (since they DON'T involve F(0, 0)). And the reason this holds true should be embedded in the properties of AND.

## Here's an interesting property: AND(a, 1) == a
Since AND(a, 1) == a,

AND(F(a, b), 1) == F(AND(a, 1), AND(b, 1)) --> F(a, b) == F(a, b)

Which trivially shows no contradiction can appear in this case.

But this property is not unique to AND (OR shares, so do a few others), so there must be another situation where where F(0, 0) doesn't come up...

## Searching for another interesting property (by brute force)...

For a := 0, b := 0, c := 0

`AND(F(0, 0), 0) == F(AND(0, 0), AND(0, 0))`
`0 == F(0, 0)`

i.e. if AND distributes over F, F must be false preserving. We knew this, but this is actually a neater way of showing it.

For a := 0, b := 0, c := 1

`AND(F(0, 0), 1) == F(AND(0, 1), AND(0, 1))`
`F(0, 0) == F(0, 0)`

i.e. This comes back to the known `AND(0, a) == a` property but also relies on AND(0, 1) == 0. This can be inverted (AND(1, 0) == 0) as well to show that **ONLY** AND distributes, since only AND has all 3 properties T(a, 1) == a, T(a, 0) == 0, and commutativity (technically by this logic we show that each reversal must be true - T(1, a) == a and T(0, a) == 0 - then back into commutativity from there).

## So the second interesting property is...

AND(0, 1) == F(0, 0) and AND(1, 0) == F(0, 0)

and in this case, F(0, 0) == 0, since by the above AND distrib is sufficient to show false preservation.

## This doesn't really

This proves that only AND can distribute, doesn't really prove that AND must distribute. Searching in higher dimensions (below) it appears there may be no general form of AND which distributes over all false preserving values

# Generalizing this

To distribute, AND in higher dimensions would need to satisfy

`AND(0, a) == AND(a, 0) == F(0, 0)`

And it must _at least_ be true that _no contradiction can occur_ when

`AND(F(a, b), 1) == F(AND(a, 1), AND(b, 1))`

So patterning after the above, if we define `AND(x, 1) := x` then this reduces to F(a, b) == F(a, b) from which no contradiction can occur. Any other definition will further limit which Fs are distributed over. E.g. if F were to have F(0, 2) := 1, this would mean `AND(1, 1) == 1 == F(AND(0, 1), AND(2, 1)) == F(0, AND(2, 1))`. This restriction on F's structure must be satisfied or a contradiction occurs, and since we hope for NO restriction on F, we prefer to avoid this.

What about 2 as an input? We hope that it will be true that for all false preserving F

`AND(F(a, b), 2) = F(AND(a, 2), AND(b, 2))`

Since we already know F(0, 0) == 0, we can derive AND(0, 2) == F(AND(0, 2), AND(0, 2)). This places a further restriction on F UNLESS we choose AND(0, 2) := 0. Any other choice restricts the value of F(n, n) (n != 0) to something specific. This holds for every AND(0, n).

What about AND(2, 2)? Again we hope that

`AND(F(a, b), 2) = F(AND(a, 2), AND(b, 2))`

For all a, b. We can therefore choose a := 2 and get

`AND(F(2, b), 2) = F(AND(2, 2), AND(b, 2))`

And without reducing further, it is clear that AND(2, 2) must be 0 to avoid restricting F further. Any other choice would mean we have a restriction on F(n, m) (n != 0), which is undesirable if we want AND to distribute over every false preserving F.

Since we have a free choice of a, we can show that AND(a, 2) must all also be 0.

This cannot exist simultaneously with the above AND(x, 1) := x without restricting F. In the case of a := 1, we get AND(F(1, b), 2) = F(AND(1, 2), AND(1, b)) -> 0 = F(2, b).



# Putting this on hold for a bit...

Since it seems like it's impossible to build generalized AND that distributes over all false-preserving operators, I'm going to go focus on some other things for a bit. This is still an interesting thread.

It seems from work to this point that the AND definition with the least restriction on the Fs over which it distributes is AND(1, x) := x, AND(a, x) := 1 (a != 1), AND(a, b) := AND(b, a)

Open questions are:
- What is the exhaustive list of properties F must have such that this AND distributes over it?
- What are the effects of each combinations of conflicting properties? Basically what properties of F can I preserve (false preserving and what else?) while defining one AND that distributes over them all. **This is still of interest - I only need one AND / XOR combo to make this work**
