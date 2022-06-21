# Hexcast
This small project was created as an answer to the following interview question:


```
We’d like you to write us a program that:
Generates 8-digit hexadecimal codes to be used for 2FA.

The rules are as follows:
1. Every time you run the program, it should emit one 8-digit hexadecimal code;
2. It should emit every possible code before repeating;
3. It should not print "odd-looking" codes such as 0xAAAAAAAA or 0x01234567 
   or any commonly used words, phrases, or hexspeak such as 0xDEADBEEF;
4. Codes should be emitted in apparently random order.
```

The approach embodied in this code was driven by several considerations:
* The program needs to cycle through ~2^32 items without repeating.
* It must somehow persist it's state between runs.
* Item 4, `Codes should be emitted in apparently random order` implies that you must cycle through them cleverly.

To run the program do the following:
1. create a virtual environment
2. Acquire the code to this project, either `git clone` or download it
3. `pip install -r requirements.txt`
4. Make sure the context in which the program runs has write privileges. It uses an `ini` file.

* The program has several commands:
  * `python hexcast init` initializes the current run with default values, creating an `hfa.ini`
  * `python hexcast sequence` displays the list of numbers to be emitted on subsequent calls. This works for a total element size of 1000 or less.
  * `python hexcast` emits the next number in the sequence

A fuller explanation of this program is in `explanation.md`


I should state that I spent about a half a day pondering how to approach this problem 
and about another 2 days creating and testing the system. Aside from some mechanical issues, 
such as looking for easy ways to extract chunks of arrays, and getting `sympy` to quickly find large primes,
I did not do any research in solving this.
When I had resolved to follow this strategy, I gave the problem to a friend, 
who found a solution in 20 minutes using a reversible encryption technique, something I don't know much about but probably should learn.
We use what we know. :)
