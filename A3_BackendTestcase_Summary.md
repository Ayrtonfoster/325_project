# Summary of Backend Testcase Implementation :100:
A backend testcase for the Sell functionality was implemented. 

Since the frontend tests already ensured the form inputs were sanitized, there was only one partition to be tested: 
that where all the inputs are valid and the ticket is added to the database. For breadth, we decided to use a shotgun 
method to generate many random inputs within this partition. 

#### Precondition
- Server started

#### Actions
- Create random valid inputs for ticket sell form, as defined in R4
- Call backend sell_tickets method with these inputs, record return value

#### Postcondition
- return value from sell_tickets is True