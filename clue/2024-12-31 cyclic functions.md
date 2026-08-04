
If you think about function inputs as a graph, usually you MUST make this a DAG. Something like

A ----> C --
  \          \
    --> B ----> D

To avoid problems where the output of a function doesn't match have the same inputs

What happens when a function can loop back on itself though?


        -----> A
       |      /
        \    /
          --

             
In the simplest case, where the output is supplied directly to the input of the same function, this implies the index of A to which the output is supplied is identity

However, in more complex cases (e.g. below) where there are intervening functions it's interesting to think about...

A ---> B ----> C ---> output
       ^      /
        \    /
          --

and if B and C are (anti)commutative then this means I can reverse B and C then draw the same arrow (really some related arrow based on shuffling inputs). But this then also implies I can just draw a feed-forward arrow from B to C without reversing B and C's order. The feed-forward arrow might be trivial (i.e. it just says we feed the same thing from B to C as we already are) but it might be nontrivial (i.e. implies some further relation between the feed-forward index which is not at first glance obvious)



Another thought: And if B and C are monotonic then it seems like this would actually force the index to be the identity? Is that right? When I increment the input index, the output must stay the same or increase. But if I increment the output, the input must increase. Since I cannot effect a change in output without a change in input and I must have an output for each input, every input change must therefore correspond to a change in the output. Then by the pidgeon hole principle and limitation of montonicity I must have an output "vector" that starts at 0 and increments with each change. With shared feedback loops (i.e. output goes to 2+ inputs) this implies a limitation to the inputs of the function, which then allows for 2+ inputs to work


