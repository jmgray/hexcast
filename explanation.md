
#### Problem Statement
1. Every time you run the program, it should emit one 8-digit hexadecimal code
2. It should emit every possible code before repeating
3. It should not print "odd-looking" codes such as `0xAAAAAAAA` or `0x01234567` or any commonly used words, phrases, or hexspeak such as `0xDEADBEEF`;
4. Codes should be emitted in apparently random order.

#### TL;DR
* Treat the list of Hexadecimal numbers as a 16 x 8 vector space (matrix)
* Linearize this space into an array
* Pick a random starting point in the array
* Walk through the list by large steps mod the size of the list (steps are prime)
* Filter out any unwanted string using standard password validation techniques

#### NTL;GD (Not too long; Gimme Details)

Apologies for the somewhat academic tone here. It's just what I do. :)

At first glance this does not seem to be that difficult. It is very straightforward to find a solution that will satisfy constraints `1`,`3` & `4`.
However, at second glance it is clear the constraint `2` makes this a non-trivial problem. There are 2^32 possible codes (16^8 == 2^32) and we need to cycle through
them without repeating, and the order needs to appear random. To restate the problem: we need to find a random-seeming sequence of numbers through a list of 2^32 items.

My first thoughts revolved around finding a sequence along a 2D matrix, the implicit assumption being that if you can find a pattern in 2D, you can scale up to higher dimensions.
There are various ways in which you can walk through a 2D matrix: Row-wise, column-wise, diagonally, even spirally. 
For a small matrix this gives you a pseudo-random walk but for a matrix of any size the pattern reveals itself quickly.


One tactic you might take would be to walk around the matrix taking larger steps. Instead of going to the next one in whatever your traversal mechanism is, jump two or three,or more places instead. I visualized that on a matrix but realized quickly that converting the matrix to a simple list makes this a tractable problem. With data in a linear format, this becomes a problem of rotating through the list. To make sure all of the items are visited, the size of the rotation--the step or "leap"--should ideally be co-prime to the size of the list. Simple prime numbers should work.


This approach should work but there were two challenges to solve. Actually only one but I am going to go about it in a roundabout way so it feels like two: We need to convert an index from our proposed linear array to a vector--semantically, a set of matrix coordinates into the matrix, and to do do _that_ it is easiest to go the other way first. I.e., from a vector to an index.

 
I am sure there is a way to derive such a formula (it is likely on a blog somewhere too) but I simply experimented on 2 and 3 dimensional arrays 
with a few digits to ferret out a closed form for higher dimensions.


For a two-dimensional matrix, assuming a (row,col) coordinate system, it is well-known and very simple to get the index:<br> 
`index = current_row * SIZE_OF_ROW + current_col`<br>
and going from index to coordinate is only slghtly more difficult:<br> 
`row = Floor(index / SIZE_OF_ROW), col = index mod SIZE_OF_ROW`


Adding a 3rd dimension, and assuming sides are of equal length (cubic), we have the following:<br>
`index = x * (M_SIZE)^2 + y * (M_SIZE)^1 + z * (M_SIZE)^0`<sup>1</sup><br>
For example, with `M_SIZE=4` and a coordinate of `(2, 3, 3)` we would have:<br>
`2 * 16 + 3 * 4 + 3 * 1 = 47`


That is easily generalizable to:<br>
`index = v0 * t0 + v1 * t1 ... vn * 1` 
where `T = (M_SIZE^(M_DIM-1) + M_SIZE^(M_DIM-2) ... 1)`<br>
or `T=(s^(d-1) + s^(d-2) + ... 1)`<br>
or `V · T `


Of course, this all by way of research since we don't really need to calculate the index--it is inherent in simply positing the array itself.
Our indexc to vector convesion can be done by reversing the process by which we got the index value above; basically a series of divisions and "remaindings". We will iterate over the index, using a `T` array as listed above.<sup>2</sup<br>

`v0 = Floor(index / t0)`<br>
`v1 = Floor((index - v0*t0) / t1)`<br>
...<br>
`vn = Remaining - v(n-1) * t(n-1)`<br>

With that, there is a way to get from index to vector and it is easy to get then from vector to a hex string. 
All that is needed to complete the problem is a suitable storage mechanism for persisting each interation and some filtering
and validating pieces to sidestep any unwanted hex strings. Voila. We have `Hexcast`


Of course, I say that like the work is trivial, but it is not. Nonetheless, the strategy seems solid adn now begins the construction.
And testing; if not thoroughly, at least enough to know that it basically works. There are certainly more efficient ways to get
this functionality and I am certain there are security holes in this. The only randomness at all is in the choice of starting index. 
I thought about randomizing the step (`leap`) value, but that seemed too much for the goal at hand, which was just to complete this asessment.

#### Filters
The problem instructs that _odd-looking_ and obviously readable string should be avoided. This is what a normal person would say (i.e., someone who does not spend time thinking about effective ways to optimize algorithms just for fun) but it needs to be more precise to be useful in a program. `Hexcat` uses three filters to detect unacceptable string:
 
* `HexSpeakFilter` compares the calculated string to a canned list of invalid hex snippets. These are found in `hslist.txt`
* `MinimumUniqueDigitsFilter` verifies that the string contains at least 4 unique digits. This is meant to catch things like `AAAAABC`
* `SequenceHexDigitsFilter` examines the string for number sequences. It enforces the following conditions:
   * No sequence of 3 digits may be repeated anywhere in the string. So, bad: `ABCABCDE`, `02FAB02F`, good: `ABDABCDE`, `02FAB12F`
   * No sequence of 2 digits may be repeated more than twice anywhere in the string: bad: `A121212B`, `C5C5C543`, good: `A121B212`, `C53C5C54`
   * No consecutive sequence may be more than 3 digits: bad: `AAAAABCD`, `F1234EF`, good: `AAAADBCC`, `F12E42F`
 
There could of course be many other variations on this theme that better target unusable strings but these seemed to suffice for this problem. 
 
            

 
 
<sup>1 I suspect that the calculation for a non-cubic space would entail just a small modification but I don't know it and did not care to explore the matter for this work. Perhaps you will!</sup>


<sup>2</sup `T` stands for Tiers in the nomenclature of this program. Since we are ultimately dealing eith 8 dimensions it is not really precise to speak of "Tiers", but it is succinct and visually appealing. 


 

