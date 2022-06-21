
Problem Statement
1. Every time you run the program, it should emit one 8-digit hexadecimal code;
2. It should emit every possible code before repeating;
3. It should not print "odd-looking" codes such as 0xAAAAAAAA or 0x01234567 or any commonly used words, phrases, or hexspeak such as 0xDEADBEEF;
4. Codes should be emitted in apparently random order.

### TL;DR
* Treat the list of Hexadecimal numbers as a 16 x 8 vector space (matrix)
* Linearize this space into an array
* Pick a random starting point in the array
* Walk through the list by large steps mod the size of the list (steps are prime)
* Filter out any unwanted string using standard password validation techniques

### NTL;GD (Not too long; Gimme Details)

Apologies for the somewhat academic tone here. It's just what I do. :)

At first glance this does not seem to be that difficult It is very straightforward to find a solution that will satisfy constraints 1,3 & 4.
However, at second glance it is clear the constraint 2 makes this a non-trivial problem. There are 2^32 possible codes (16^8 == 2^32) and we need to cycle through
them without repeating, and the order needs to appear random. To restate the problem: we need to find a random-seeming sequence of numbers through a list of 2^32 items.

My first thoughts revolved around finding a sequence along a 2D matrix, the implicit assumption being that if you can find a pattern you can scale up to higher dimensions.
There are various ways in which you can walk through a 2D matrix: Row-wise, column-wise, diagonally, even spirally. 
For a small matrix this gives you a pseudo-random walk but for any matric of any size the pattern reveals itself quickly.

One tactic you might take would be to walk around the matrix taking larger steps. Instead of going to the next one in the list, jump two or three.
I visualized that on a matrix but realized that this is simply rotating through a list and to make sure all of the items are visited
the size of the rotation should ideally be co-prime to the size of the list. Simple prime numbers would work.

This approach would work but there were two challenges to solve: converting between a vector--
essenaitally a set of matrix coordinates into the matrix--and an index into the array, and back again.
I am sure there is a way to derive such a formula (it is likely on a blog somewhere too) but I simply experiemented on 2 and 3 dimensional arrays 
with a few digits to ferret out a strategy for higher dimensions.

For a two-dimensional matrix, assuming a (row,col) coordinate system,
it is well-known and very simple to get the index:<br> 
`index = current_row * SIZE_OF_ROW + current_col`<br>
and going from index to coordinate is only slghtly more difficult:<br> 
`row = Floor(index / SIZE_OF_ROW), col = index mod SIZE_OF_ROW`


Adding a 3rd dimension, and assuming sides are of equal length (cubic), we have the following:<br>
`index = x * (M_SIZE)^2 + y * (M_SIZE)^1 + z * (M_SIZE)^0`<sup>1</sup><br>
For example, with `M_SIZE=4` and a coordinate of `(2, 3, 3)` we would have:<br>
`2 * 16 + 3 * 4 + 3 * 1 = 47`


Now that is easily generalizable to:<br>
`index = v0 * t0 + v1 * t1 ... vn * 1` 
where `T = (m_size^(m_dim-1) + m_size^(m_dim-2) ... 1)`<br>
or `T=(s^(d-1) + s^(d-2) + ... 1)`<br>
or `V · T `


Of course, this all by way of research since we don't really need to calculate the index--it is inherent in simply positing the array itself.
What we need is a way to get from the `index` to the `Vector`. To do that we need to iterate over the index, using a `T` array as listed above.<br>

`v0 = Floor(index / t0)`
`v1 = Floor((index - v0*t0) / t1)`
...
`vn = Remaining - v(n-1) * t(n-1)`

With that, there is a way to get from index to vector and it is easy to get then from vector to a hex string. 
All that is needed to complete the problem is a suitable storage mechanism for persisting each interation and some filtering
and validating pieces to sidestep any unwanted hex strings. Voila.


Of course, I say that like the work is trivial, and true, I think the strategy is solid, but it must be constructed. 
And tested; if not thoroughly, at least enough to know that it basically works. There are certainly more efficient ways to get
this functionality and I am certain there are security holes in this. The only randomness is in the choice os starting index. 
I thought about randomizing the step or `leap` value, but that seemed too much for the goal at hand, whch was just to complete this asessment.









<sup>1 I suspect that the calculation for a non-cubic space would entail just a small modification but I don't know and did not care to explore the matter.</sup>




