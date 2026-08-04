
My aim is to construct a way to construct a system capable of representing the concept of "Alice has 5 cards in her hand". I have discovered the following properties that may be useful:

- A representation of the integers in terms of sets. Using "increment", "xor" (extended), and "and" I can define addition in a closed form as a + b := a xor b xor inc(a and b)

I have the following possible avenues to explore:

- Can I define multiplication and exponentiation using elementary set operations? This would be useful because, in the set-wise formulation of the integers, "the set containing A" is 2 ** A
- The original versions of XOR and AND that 
