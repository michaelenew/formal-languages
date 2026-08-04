
With 2 truth values, XOR cancels like a ^ a := 0. This is an interesting property and is important to minimal form.

It's also possible to have minimal form (especially in higher truth dimensions) with multiple cancelation. This would look like (in general) a ^ a ^ ... ^ a disappears for some other count of a. A naive description where the number of terms is the truth dimensionality presents obvious issues, and it is the purpose of this document to represent this idea in a less impossible way (or demonstrate no such representation exists)

The essential properties with 2 truth values:

- 0 ^ a := a
- a ^ a := 0

We would need to preserve this over every domain. In other words, if when generalized I restrict my truth value dimension to 2, these properties as written must hold. Beyond 2 dimensions, I get to manipulate the definition.

If we try to generalize with more a terms, we end up with a ^ a ^ a := 0 in 3 dimensions. This breaks the 2d definition, where a ^ a ^ a == a ^ 0 == a, so there is at least 1 number where this breaks.

What if instead all we wanted to preserve was a ^ a ^ a := a? The number of terms such that a ^ ... ^ a := a must be variable length based on a known truth dimension. The LCM of the first (dim) natural numbers should be the smallest possible "period number" (closed form given by the second Chebyshev formula according to https://math.stackexchange.com/questions/659799/lcm-of-first-n-natural-numbers)


[]()