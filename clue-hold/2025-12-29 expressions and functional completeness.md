
If we have 2 syntaxes for expressing a single underlying semantic object, e.g. an expression in terms of AND/OR/NOT and XOR/AND/TRUE, they "admit the same semantics"

2 ways of saying this same thing:

1. There exists a way to rewrite the first system to the second: AND -> f(XOR, AND, TRUE), OR -> f(XOR, AND, TRUE), NOT -> f(XOR, AND, TRUE); and going in the opposite direction: XOR -> f(AND, OR, NOT), etc
2. Both of these systems of operators are functionally complete

These two statements seem totally disparate but in this context mean exactly the same thing. This is striking and it's why I'm making a new document for this thought.

Bringing in the relationship of functional completeness with commutativity in certain situations, it seems like there's some chance to build a bridge here but I cannot quite see it yet.
