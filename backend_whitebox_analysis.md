# Backend White Box Analysis
## Ayrton Foster, Eric Leask, Matthew Kruzich, Francesco Marrato

### Method: ```backend.update_ticket()```
Chosen because patching was only required for the ```backend.get_ticket``` and was only used once. No need for 
complex patching of different values at different times as seen in ```update_balance()```
### Analysis: Block Coverage
block coverage was chosen because of how simple the ```backend.update_ticket()``` method is.
With only one if/else statement performing decision or even coverage testing does not make much of a difference.
The entire method is made up of 8 executable statements with only one decision changing the result of the return.

Block testing was completed by running the method with a test case for each block (a.k.a. when the if statement
 is True/False) and checking the result against what should be expected as a return. The two tests are as follows.
 
 1. Perform ```update_ticket()``` with valid ticket to return ```True``` and skip over the ```if``` statement found on line 118.
 Patch in ```get_ticket``` to return ```None```.
 2. Perform ```update_ticket()``` with invalid ticket to return ```None``` and go through the ```if``` statement found on line 118.
 Patch in ```get_ticket``` to return ```True```.

