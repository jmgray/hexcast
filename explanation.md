
Problem Statement
1. Every time you run the program, it should emit one 8-digit hexadecimal code;
2. It should emit every possible code before repeating;
3. It should not print "odd-looking" codes such as 0xAAAAAAAA or 0x01234567 or any commonly used words, phrases, or hexspeak such as 0xDEADBEEF;
4. Codes should be emitted in apparently random order.

At first glance this does not seem to be that difficult It is very straightforward to find a solution that will satisfy constraints 1,3 & 4.
However, at second glance it is clear the constraint 2 makes this a non-trivial problem. There are 2^32 possible codes (16^8 == 2^32) and we need to cycle through
them without repeating, and the order needs to appear random. To restate the problem: we need to find a random-seeming sequence of numbers through a list of 2^32 items.

My first thoughts revolved around finding a sequence along a 2D matrix, the implicit assumption being that if you can find a pattern you can scale up to higher dimensions.
There are various ways in which you can walk through a 2D matrix: Row-wise, column-wise, diagonally, even spirally. 
For a small matrix this gives you a pseudo-random walk but for any matric of any size the pattern reveals itself quickly.

One tactic you migt take would be to walk around the matrix taking larger steps. Instead of going to the next one in the list, jump two or three.
I visualized that on a matrix but realized that this is simply rotating through a list and to make sure all of the items are visited
the size of the rotation should ideally be co-prime to the size of the list.







Incrementing through a series of numbers should be easy so a first thought is to use some kind of visited list to track the progress 
but even if we used a high performant DB to store such a list it would still require a few billion rows. 

And they need to appear random. The key word here is `appear`, as it turned out.






