# Hexcast
This small project was created as an answer to the following interview question:


```
We’d like you to write us a program that:
Generates 8-digit hexadecimal codes to be used for 2FA.

The rules are as follows:
1. Every time you run the program, it should emit one 8-digit hexadecimal code;
2. It should emit every possible code before repeating;
3. It should not print "odd-looking" codes such as 0xAAAAAAAA or 0x01234567 or any commonly used words, phrases, or hexspeak such as 0xDEADBEEF;
4. Codes should be emitted in apparently random order.
```

The approach embodied in this code weas driven by two considerations:
* The program need to cycle through ~2^32 items without repeating.
* It must somehow persist it's state between runs.
* Item 4, `Codes should be emitted in apparently random order` implies that you must cycle through them cleverly






To run the program do the following:
1. create a virtual environment
2. Acquire the code to this project, `git pull` or download
3. `pip install -r requirements.txt`
4. Make sure the context in which the program runs has read/write privileges

* The program has several commands:
  * `python hexcast init` initializes the current run with default values, creating an `hfa.ini`
  * `python hexcast sequence` displays the list of numbers to be emitted on subsequent calls
  * `python hexcast` emits the next number in the sequence


 