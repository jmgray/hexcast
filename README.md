# Hexcast
In my travels through the sea of technology that encompasses us all I recently happened upon an interesting programming challenge. This small project was created as an attempt to solve it. Said challenge: 


```
Write a program that generates 8-digit hexadecimal codes

The rules are as follows:
1. Every time you run the program, it should emit one 8-digit hexadecimal code;
2. It should emit every possible code before repeating;
3. It should not print "odd-looking" codes such as 0xAAAAAAAA or 0x01234567 
   or any commonly used words, phrases, or hexspeak such as 0xDEADBEEF;
4. Codes should be emitted in apparently random order.
```

The approach embodied in this code was driven by several considerations:
* The program needs to cycle through ~2<sup>32</sup> items without repeating.
* It must somehow persist it's state between runs.
* Item 4, `Codes should be emitted in apparently random order` implies that you must cycle through them cleverly.

A fuller explanation of this program is in `explanation.md`

To run the program do the following:
1. create a virtual environment
2. Acquire the code to this project, either `git clone` or download it
3. `pip install -r requirements.txt`
4. Make sure the context in which the program runs has write privileges. It uses an `ini` file.

* The program has several commands:
  * `python hexcast init` initializes the current run with default values, creating an `hfa.ini`
  * `python hexcast sequence` displays the list of numbers to be emitted on subsequent calls. This works for a total element size of 1000 or less.
  * `python hexcast` emits the next number in the sequence

#### Default Example
On the command line type the following:<br>
`python hexcast init`<br>

This initializes the default ini with the following, full details of which are in the `example.hfa.ini` file. Suffice to say it creates parameters to use a 4 x 2 matrix. This will contain 16 elements which will be "randomly" traversed:
```
[CYCLE]
size = 4
dimension = 2
leap = 7
index = 3
nth = 0
validate = false
start_index = 3
```
Invoke the program a few times to display numbers within the matrix sequence:
```
python hexcast
22
python hexcast
01
python hexcast
20
```
Typing the following displays the sequence in which values will be displayed:<br>
`python hexcast sequence`<br>
`{'03': 3, '22': 10, '01': 1, '20': 8, '33': 15, '12': 6, '31': 13, '10': 4, '23': 11, '02': 2, '21': 9, '00': 0, '13': 7, '32': 14, '11': 5, '30': 12}`
Each element in this represents an item in the sequence. Each key is the number emitted (which is really just a 2D vector) and each value is the index within the list that corresponds to that item. See `explanation.md` for more details. If you don't see the above, then something is off.


You can initialize the program to a different vector space by providing parameters for the vector size adn the matrix dimension. This command sets up a 3D matrix with 6 nodes per side, so 6^3 or 216 elements:<br>
`python hexcast init 6 3`

Each call shows 3D vectors whose digits are all `0-5`:<br>
```
python hexcast
193
python hexcast
434
python hexcast
205
```
If you invoke it 216 times you will wind up at the beginning of the list.

### Hexadecimal output
To initialize the program to display random hexadecmial numbers type:<br>
`python hexcast init 16 8`

Now, you can display random hexadecimal numbers all day long:<br>
```
python hexcast
5C1CF369c

python hexcast
BE4F8ED6

python hexcast
20822A43
```
If you are able to type this about `4,000,000,000` more times you will see `5C1CF369` again. I have not actually done this. :)


I should state that I spent about a half a day pondering how to approach this problem 
and about another 2 days sporadically reassessing, creating and testing the system. Aside from some mechanical issues, 
such as looking for easy ways to extract hunks of arrays, and getting `sympy` to quickly find large primes,
I did not do any research in solving this. When I had resolved to follow this strategy, I gave the problem to a friend, 
who found a solution in 20 minutes using a reversible encryption technique, something I don't know much about but probably should learn.
We use what we know. :)
