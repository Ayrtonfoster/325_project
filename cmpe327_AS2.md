# CMPE327 AS2 Group X
#### Ayrton Foster, Eric Leask, Franc Marrato, Matthew Kruzich
## Project Structure
### Overview
The architecture can be split into frontend, backend, and database. The frontend contains one function per http route 
for handling of its logic. The frontend will enforce constraints related to user input, such as format of form fields, 
and handle HTML serving. In the case where website behaviour depends on reading or writing to the database, the 
frontend will make a call to the backend, which will handle database access. The backend will enforce any constraints 
on consistency of objects in database. There are two classes of objects in the database: Users and Tickets.
### Method Outlines
#### Frontend
| Function Name | Function Description | 
| ---: | :--- |
| `authenticate` | decorator to redirect to login page if client is not logged in |
| `login_redirect` | decorator to redirect to homepage if client is logged in |
| `check_user_format` | helper function to check login and register form inputs against formatting requirements |
| `register_get` | serve registration page |
| `register_post` | register a new user |
| `login_get` | serve login page |
| `login_post` | login existing user |
| `profile` | serve user homepage |
| `logout` | logout user session |
| `sell_tickets` | user function to put tickets up for sale |
| `buy_tickets` | user function to buy tickets, if they exist |
| `update_tickets` | user function to modify tickets they are selling |
#### Backend
| Function Name | Function Description | 
| ---: | :--- |
| `get_user` | retrieve user object from database |
| `login_user` | check that email + password combination is valid |
| `post_tickets` | add tickets to the database |
| `get_all_tickets` | return full list of tickets in database |
| `buy_tickets` | remove tickets from database, if they exist |
| `get_ticket` | retrieve ticket object from the database |
| `update_tickets` | modify a ticket in the database, if it exists |
| `update_balance` | if user exists, subtract amount from user balance |
| `register_user` | add user to database |
### Class Outlines
Classes are used to represent database objects in object-oriented fashion. Attributes represent underlying SQL 
relations.
#### Model
| Class Name | Attributes |
| ---: | :--- |
| User | id, email, password, name, balance |
| Ticket | id, ticket_name, num_tickets, ticket_price, ticket_date |





## Style Guide
PEP:8 is the chosen style and syntax that will be followed by the developers of this project. It was chosen because of 
its wide use and non-specificity towards any corporations. Developers have setup their IDE's to perform automatic 
formatting inspections where error will be highlighted. The use of a defined style guide will speed up debugging, 
increasing clarity, and reducing time required for code inspections.

A link to the full style guide outline can be found here: https://www.python.org/dev/peps/pep-0008/ 
## Test Plan
### Test Organization
Unit Tests: Based on the requirement sub-lists R1 to R8 with mirrored tests for both front and back end. Front end 
tests will use mocking for backend requirements and vise-versa.
 
unit tests based on R groupings, integration tests based around the buy sell features, system testing using user 
stories
### Tools and Techniques
Automated tests will be run using the ```pytest``` command prior to each commit. The automated tests will be pulled 
from ```qa327_test``` folder which will be organized as outlined in "Test Organization".

### Environments

### Responsibilities
Team members will be responsible for test cases related to the functionalities they implemented. Dynamic pair 
programming was used, with Eric + Matt implementing login, registration, and redirect functions; and Ayrton and Franc 
implementing homepage and buy, sell, and update ticket functions.
#### Unit Testing
| Unit Test Cases | Contact |
| --- | --- |
| R1, R2, R7, R8 | Eric + Matt |
| R3, R4, R5, R6 | Ayrton + Franc |
#### Integration Testing
| Integration Test Cases | Contact |
| --- | --- |
| login, registration, logout, redirect | Eric + Matt |
| homepage, buy, sell, and update | Ayrton + Franc |
#### System Testing
The full team will be jointly involved in resolving system testcase issues, as these will require an understanding of 
the full design.

### Budget Management