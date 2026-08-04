
Working from prior doc shows that it's not possible to define meta sets with just 2 truth values. Work from other docs hit a bit of a snag trying to create fully FC operators in higher dimensions.

An interesting idea is to create a set of operators in higher truth dimensions that are specifically designed to encode the "meta" set operation. In particular, it should be easy to define a unary increment operator like `x -> x + 1` as the "make this set a meta set" operation, then extensions of AND and XOR for each truth dimension so that we can make statements about the higher dimensions.

Insight: previously, I was trying to define an operator with 1 output like this:
```
0 1 2 3 ...
1 0 1 2
2 1 0 1
3 2 1 0
...
```
but this has a problem in my current framing. For what I need, I want a statement to be able to include both the meta set and the set itself. Both of them can be empty after all. Therefore my output of XOR must be able to encode "both / neither / one / the other" of these are present.

Two ways of encoding this information:
- Can encode it in the integers directly. 0 is none are present, 1 is 1 is present, 2 is 2 is present, 3 is 1 and 2 are present, and so on. This is just taking the binary array of 0s (no present) and 1s (present) and treating it like a binary integer
- Can produce an output of an array of 1s and 0s

Pretty clear to see these are the same approach. Let's encode them with numbers because I like having it laid out like above.

XOR (preserved property is "output includes iff exactly 1 input includes")
```
0 1 2
1 0 3
2 3 0
3 2 1 0
4 5 6 7 0
5 4 7 6 1 0
```

AND (preserved property is "output includes iff both inputs include")
```
0 0 0
0 1 0
0 0 2
0 1 2 3
0 0 0 0 4
0 1 0 0 4 5
```

Easiest way to think of this is that the inputs are actually a set of integers. Start with {}, {0}, {1}, {0, 1}, {2}, {0, 2}, {1, 2}, {0, 1, 2}, ... and the number representing that set is then sum(2 ** x for x in set). In this framing, the outputs in each cell are simply input_set_1 XOR/AND input_set_2.

There also needs to be a meta operator which maps a set to its increment. This is a unary operator. The simplest version of this operator is

INC
```
1 2 3 4 ...
```

So that INC {} := {0}, {0} := {1}, {1} := {0, 1}, ...

This should have a tendency (though not a guarantee) that `INC(a AND b) == INC(a) AND INC(b)` and `INC(a XOR b) == INC(a) XOR INC(b)`. In general where a and b match up, the operator behaves the same. We get into hot water though with something like a3:=a{0,1} and a5:=a{0,2}. The INC(a5) := a6 := a{1, 2} and INC(a3) := a4 := a{2}. a{2} XOR a{1, 2} == a{1} == a2 while INC(a{0,1} XOR a{0,2}) == INC(a{1,2}) == INC(a6) == a7

What has a nicer relationship is incrementing each _existing_ element in the existence set. E.g. we take {0, 1, 5} and map it to {1, 2, 6}. This must distribute over both AND and XOR.

This would look like
```
0 2 4 6 8 ...
```
Where each element is 2x the input. This is effectively just a binary integer bitshift if you take a binary array representation of the containment set.

INC only works on the containment set. The containment set cardinality starts at {} (for "0") and becomes {0} (for "1") when a set is represented.

All reasoning is essentially the same in this model as the prior model because we have preserved the essential properties of AND and XOR. We take hypothesis ^ (true & hypothesis) to see if a hypothesis is true.

Can this represent a set containing many sets? Because INC distributes over AND and XOR, trying to represent the set {A, B} will become INC(A) | INC(B) == INC(A) ^ INC(B) ^ INC(A)&INC(B). This is equivalent to INC(A | B), which is {A | B}. Not a good representation of {A, B}.

But I do have a new set of operators to play with. These should be close to functionally complete or functionally complete (with constants? at least const 1). It might be possible to just construct from a known set of elements the operator that always maps their union (or XOR combination since they are necessarily disjoint) to their size. Basically we'd wind up with a map such that `INC(a XOR b) -> map -> 2` (which is saying there are no elements in a XOR b at level 2). We also need to know `INC(a AND b) -> map -> 0`

To encode size I could just say that repeated INC'ing corresponds to the size of the set. Essentially I end up with
- `INC(A)`
- `INC(INC(A | B))`
- `INC(INC(INC(A | B | C)))`
- ...

(where size 0 is defined just by the un-incremented set A)

Basically the Nth INC of a set is empty iff that set has size N. Now there's a question of whether I can express "is of size 1 or 2 or 3".

INTERESTING: the multiple INC approach actually defines "a superset of this is of size N". If I take INC(INC(A | B)) then INC(INC(A)) will necessarily be empty as well. This means that 

It's a bit neater to construct a true map though. This allows us to define multiple levels of containment where we just map `INC(set) -> map -> set size`. Call MAP * INC := SIZE, then SIZE(a1) ^ {1}, ... but 1 is not a symbol. I can define 1 to be a symbol. Maybe I can also define the empty set at order 1 to be "size 1". The empty set at order 1 is (I think) not achievable by any other means.

## Idea for sizes

One way to encode sizes might be to define a "canonical set of size N" for each size we're interested in. Then, we could just say `INC(A) ^ INC(N)`. What this amounts to is a framework wherein a particular size (say INC(3)) is inside INC(A) when A is that size and is otherwise not in A.

> A general insight: I think it's necessary to make the size representation a positive assertion like this. Basically "something IS inside the set" not "something IS NOT inside the set". This is because if the size is defined in the negative then I end up taking the union of those sets, which means that the union of 2 sets must be the same size as each set individually (not correct behavior for set sizes in general).

This particualar idea seems to have some merit. If I want to say "A is size 1 or 2" then I write `INC(A) ^ INC(A)&(INC(1) | INC(2))`.

So what happens when I want to write "A is size 0 or 1"? `INC(A) ^ INC(A)&(INC(0) | INC(1))`. The canonical set of size 0 is already defined - the empty set. Unfortunately INC(0) := 0. It can still have its own symbol though (call it 0), it just so happens to be true that `0`. Could probably also define some kind of realtionship between canonically sized sets like `0 | 1 ^ 1` and `1 | 2 ^ 2` and so on. There's probably a clean way to express addition and multiplication in a similar way.

What happens when I want to say "A is not empty"? `INC(A)&INC(0)`.

`INC({})` is a 0-term statement, so it's also the empty set. For this reason I cannot define "the canonical set of size 0" to be "the empty set" (which is weird...). I probably have to define `INC(every known truth) ^ INC(0)`. Then all my statements get added as `true | (INC(statement) ^ INC(0))`.

I need to make sure truths of size operations are encoded as well. E.g. if `INC(A^AB) ^ INC(2)` and `INC(B^AB) ^ INC(4)` then it should be true that `INC(A ^ B) ^ INC(6)`.

```
INC(A^AB) ^ INC(2) ^ INC(B^AB) ^ INC(4) ^ (INC(A^AB) ^ INC(2))(INC(B^AB) ^ INC(4))

INC(A^AB) ^ INC(2) ^ INC(B^AB) ^ INC(4) ^ INC(A^AB)INC(B^AB) ^ INC(2)INC(B^AB) ^ INC(A^AB)INC(4) ^ INC(2)INC(4)

INC(A) ^ INC(AB) ^ INC(2) ^ INC(B) ^ INC(AB) ^ INC(4) ^ INC(2B) ^ INC(2AB) ^ INC(4A) ^ INC(4AB) ^ INC(2 4)

INC(A) ^ INC(B) ^ INC(2B) ^ INC(2AB) ^ INC(4A) ^ INC(4AB) ^ INC(2 4) ^ INC(2) ^ INC(4)

INC(A) ^ INC(B)
    ^ INC(2B) ^ INC(2AB) ^ INC(2)
    ^ INC(4AB) ^ INC(4) ^ INC(4A)
    ^ INC(2 4)
```

then it should also be true that `INC(A ^ B) ^ INC(6)`, so that `INC(A ^ B) ^ INC(6) ^ (INC(A ^ B) ^ INC(6)) (<above>)` is empty:

```
INC(A) ^ INC(B) ^ INC(6) ^ (INC(A) ^ INC(B) ^ INC(6))&(
    INC(A) ^ INC(B)
        ^ INC(2B) ^ INC(2AB) ^ INC(2)
        ^ INC(4AB) ^ INC(4) ^ INC(4A)
        ^ INC(2 4)
)

INC(A ^ B ^ 6 ^ (
    (A ^ B ^ 6)&(A ^ B)
        ^ (A ^ B ^ 6)&(2B ^ 2AB ^ 2)
        ^ (A ^ B ^ 6)&(4AB ^ 4 ^ 4A)
        ^ (A ^ B ^ 6)&2&4
))

INC(A ^ B ^ 6 ^ (
    A ^ B ^ A6 ^ B6
        ^ 2A ^ 2AB ^ 26B ^ 26AB ^ 26
        ^ 4B ^ 4AB ^ 46AB ^ 46 ^ 46A
        ^ 24A ^ 24B ^ 246
))

INC(6 ^ (
    A6 ^ B6
    ^ 2A ^ 2AB ^ 26B ^ 26AB ^ 26
    ^ 4B ^ 4AB ^ 46AB ^ 46 ^ 46A
    ^ 24A ^ 24B ^ 246
))

```


# Weird extension idea...

The extension above looks like "take the symbolic set {0, 1, 2, ...} paired with a 0/1 (in or out) and turn the 0/1 into a set itself like {0, 1, 2, ...}, applying the same operators to it". What if we extend this pattern? idk why we would need to right now, but it lets us encode theoretically arbitrary amounts of information. Each step can be thought of as "where does the last step exist?"

## Here's a way of framing the extension

We started with representation of 2 truth values of either i0 := {} or i1 := {0}. The former is 0 and the latter is 1 (computed as sum(2 ** n for n in set)). All we have done is allow more SYMBOLS in the truth values. Then we take the set-wise XOR or AND of the inputs to achieve the output. BUT, typically when we take XOR or AND we're taking it for one "tile". In this case we're actually taking the XOR or AND of an entire collection of tiles (set boundaries defined by the symbols 0, 1, 2, ...). For XOR the second order symbol (0, 1, 2, ...) represents a TERM and for AND the symbol represents a SYMBOL (yes, it's weird just think about it for a second).

So the first extension was going from taking 0s and 1s as inputs (symbols) (truth table for 1 tile) and outputting a whole collection of tiles (a statement) and we did this by allowing the input to become the output concept in the original framing. More precisely:

- For AND, we went from taking {} and {0} as inputs to taking 
- For XOR, we went from taking {} and {0} (where 0 is just a symbol) as inputs to taking an arbitrary collection of terms (whose precise formulation is stood in for by the symbols 0, 1, 2, ...). The truth table went from taking Symbol(0) and outputting Symbol(0), corresponding to a Statement(0, 1, 2, 3, ...), to taking Statement(0, 1, 2, 3, ...) as input and output, corresponding to a
    - Statement(Statement(0, 1, ...), Statement(...), ...) where each inner term gets eliminated if it exactly exists in the other meta-statement? Probably implementing this in code will help to clarify. Start with the single Symbol of "0". Write XOR and AND in terms of the empty set and the set containing 0. Build Term and Statement from XOR and AND. See what abstraction opportunities emerge.

So a natural question is "how do we allow this 'second order' framing w/ collections of statemnets"
