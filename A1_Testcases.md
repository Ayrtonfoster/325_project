# TestCases R5

## R5
### Test case R5.0.1 - /update[POST] The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character.
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_test_ticket_@69_XXx',
    quantity=10,
    price=10,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /update
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `Error: Alphanumeric characherts only`
-   open /logout (clean up)


### Test case R5.1 - /update[POST] The name of the ticket is no longer than 60 characters
#### R5.1.1 - Check if updating action passes with ticket names shorter than 60 characters
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=10,
    price=10,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /update
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `success`
-   open /logout (clean up)



#### R5.1.2 - Check if updating action passes with ticket names longer than 60 characters
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_MLG_test_ticket_69_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    quantity=10,
    price=10,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `error: Ticket name longer than 60 characters`
-   open /logout (clean up)

### Test case R5.2 - /update[POST] The quantity of the tickets has to be more than 0, and less than or equal to 100.
#### R5.2.1 - Check if "ticket quantity" inside of range is accepted by front end
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=10,
    price=10,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `success`
-   open /logout (clean up)



#### R5.2.2 -  Check if "ticket quantity" outside of range causes updating action failure
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=999,
    price=10,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `error: number of tickets is not between 0 and 100`
-   open /logout (clean up)

### Test case R5.3 - /update[POST] The quantity of the tickets has to be more than 0, and less than or equal to 100.
#### R5.3.1 - Check if "ticket price" inside of range is accepted by front end
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=10,
    price=20,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   enter test_ticket's price into element  `#update_price`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `success`
-   open /logout (clean up)



#### R5.3.2 - Check if "ticket price" outside of range causes updating action failure
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=20,
    price=2,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   enter test_ticket's price into element  `#update_price`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `error: ticket price not between 0 and 100`
-   open /logout (clean up)


### Test case R5.4 - /update[POST] Date must be given in the format YYYYMMDD 
#### R5.4.1 - Check if entered date using proper format is accepted by front end
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=10,
    price=20,
    date='20201101'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   enter test_ticket's price into element  `#update_price`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `success`
-   open /logout (clean up)



#### R5.4.2 - Check if entered date using improper format cause updating action failure
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=20,
    price=2,
    date='09092020'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   enter test_ticket's date into element  `#update_date`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `error: ticket date does not follow specified format`
-   open /logout (clean up)

#### R5.4.3 - Check if dates that match the format but do not exists(e.g. Nov 31st) cause selling action failure
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=20,
    price=2,
    date='20201573'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   enter test_ticket's date into element  `#update_date`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `error: ticket date does not exist`
-   open /logout (clean up)

#### R5.4.4 - Check if dates that have already passed cause updating action failure
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=20,
    price=2,
    date='14530523'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   enter test_ticket's date into element  `#update_date`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `error: ticket date is from the past`
-   open /logout (clean up)

### Test case R5.5 - /update[POST] The ticket of the given name must exist
#### R5.5.1 - Check if the system allows you to purchase a ticket that does not exist
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=10,
    price=20,
    date='20201101'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `error: A ticket under that name does not exist`
-   open /logout (clean up)



#### R5.5.2 - Check if the system allows you to purchase a ticket that exist
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=20,
    price=2,
    date='20201101'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   enter test_ticket's date into element  `#update_date`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `success`
-   open /logout (clean up)

### Test case R5.6 - /update[POST] For any errors, redirect back to / and show an error message
#### R5.6.1 - Check if when an error message is created a redirection to the / page occurs, and teh error message displays
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=10,
    price=20,
    date='20201101'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#update_name`
-   enter test_ticket's quantity into element  `#update_quantity`
-   click element  `#update_submit`
-   validate that the  `#update_message`  element shows  `error: A ticket under that name does not exist`
- validate we are on /
-   open /logout (clean up)

## R6
### Test case R6.0.1 - /buy[POST] The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character.
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_test_ticket_@69_XXx',
    quantity=10,
    price=10,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /buy
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `Error: Alphanumeric characherts only`
-   open /logout (clean up)


### Test case R6.1 - /update[POST] The name of the ticket is no longer than 60 characters
#### R6.1.1 - Check if updating action passes with ticket names shorter than 60 characters
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=10,
    price=10,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /buy
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `success`
-   open /logout (clean up)



#### R6.1.2 - Check if updating action passes with ticket names longer than 60 characters
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_MLG_test_ticket_69_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    quantity=10,
    price=10,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /buy
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `error: Ticket name longer than 60 characters`
-   open /logout (clean up)

### Test case R6.2 - /update[POST] The quantity of the tickets has to be more than 0, and less than or equal to 100.
#### R6.2.1 - Check if "ticket quantity" inside of range is accepted by front end
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=10,
    price=10,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /buy
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `success`
-   open /logout (clean up)



#### R6.2.2 -  Check if "ticket quantity" outside of range causes updating action failure
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=999,
    price=10,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /buy
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `error: number of tickets is not between 0 and 100`
-   open /logout (clean up)

### Test case R6.3 - /update[POST] The ticket name exists in the database and the quantity is more than the quantity requested to buy
#### R6.3.1 - Check if you can buy more tickets than what are available
Test Data:
```
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
    balance= 99999
)
```

```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=10,
    price=20,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /buy
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `error: you are attempting to purchase more tickets than what are available`
-   open /logout (clean up)



#### R5.3.2 - Check if you can buy less than the available amount
Test Data:
```
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
    balance= 99999
)
```
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=20,
    price=2,
    date='20200901'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /buy
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `success`
-   open /logout (clean up)


### Test case R6.4 - /update[POST] The user has more balance than the ticket price * quantity + service fee (35%) + tax (5%)
#### R6.4.1 - Check if you can buy tickets where the total comes to be more than what the user has in their balance
Test Data:
```
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
    balance= 100
)
```
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=10,
    price=20,
    date='20201101'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `error: You do not have nought money in you balance to buy these tickets`
-   open /logout (clean up)


### Test case R6.5 - /update[POST] The ticket of the given name must exist
#### R6.5.1 - Check if the system allows you to purchase a ticket that does not exist
Test Data:
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='xXX_MLG_test_ticket_69_XXx',
    quantity=10,
    price=20,
    date='20201101'
)
```
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `error`
-   open /logout (clean up)


## R7.1 - Logout will invalid the current session and redirect to the login page. After logout, the user shouldn't be able to access restricted pages.  

### Testcase R7.1.1 - Confirm after logout that user is redirected to the login page
Mocking:   
backend.get_user to authenticate user not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
/validate user is redirected to login  

### Testcase R7.1. - Confirm after logout that user succeed to access /login  
Mocking:   
backend.get_user to authenticate user not logged in  

Actions:
open /logout (invalidate any logged-in sessions that may exist))  
open /login  
validate users current page is /login  

### Testcase R7.1.3 - Confirm after logout that user succeed to access /register  
Mocking:   
backend.get_user to authenticate user not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
open /register  
validate users current page is /register  

### Testcase R7.1.4 - Confirm after logout that user fails to access /logout  
Mocking:   
backend.get_user to authenticate user is not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
open /register  
validate users current page is /register  

### Testcase R7.1.5 - Confirm after logout that user fails to access /  
Mocking:   
backend.get_user to authenticate user is not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
open /  
validate users is redirected to /login   

### Testcase R7.1.6 - Confirm after logout that user fails to access /sell  
Mocking:   
backend.get_user to authenticate user is not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
open /sell  
validate users is redirected to /login   

### Testcase R7.1.7 - Confirm after logout that user fails to access /update  
Mocking:   
backend.get_user to authenticate user is not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
open /update  
validate users is redirected to /login   

### Testcase R7.1.8 - Confirm after logout that user fails to access /buy   
Mocking:   
backend.get_user to authenticate user is not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
open /buy  
validate users is redirected to /login   

### Testcase R7.1.9 - Confirm after logout that user fails to access /\* any other urls
open /logout (invalidate any logged-in sessions that may exist))  
open /nonexistantpage  
validate a 404 error is returned  

## Testcase R8.1 - For any other requests except the ones above, the system should return a 404 error   

### Testcase R8.1.1 - Confirm that requested urls other than the listed requests (/, /login, /logout, /sell, /update, /buy) fail to be accessed and a 404 error is returned
Mocking:   
N/A  

Actions:  
open /nonexistentpage  
validate users is returned a 404 error  





