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
### Prototype method/interactions diagram
![alt text](https://i.imgur.com/bWG3omE.png) 
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
| `ticket_info_sanitizer` | check all ticket entries against  outlined requirements and constraints|
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
### Test Organisation
Unit Tests: Based on the requirement sub-lists R1 to R8 with mirrored tests for both front and back end. Front end 
tests will use mocking for backend requirements and back end tests will use mocking for frontend tests. Back end tests will 
be based off the front end tests written in A1. A test partitioning system will be put inplace for all tests using HTML 
input boxes to reduce the number of tests required to be confident of its functionality

Integration Testing: Integration testing will begin with performing identical tests from sub-lists R1 to R8 without the 
use of mocking for front end or back end. These re-tests will identify any misalignment between requests made to the backend and the expected data to be returned.
Indepth test cases will also be created for the interactions between the ```/``` home page and the ```/buy, /sell, /update``` functions. ```/buy, /sell, /update```
integration testing is highlighted as these functions make up the majority of user interactions.

System Testing: System testing will be based on user stories, where test cases are created from paths and actions that are common to how the website should be used.
Malintent user stories will also be used for testing. Malintent test cases will consider the possibility of user attempting to miss use the website for mischievous purpose.
User story testing will be the most complex with multiple checks being made each time the website commits a new change to the screen. 

### Environment, Techniques, and Tools
Test will be automatically run using the ```pytest``` before each build is merged with the main code branch. 
Code repository badges such as 

![alt text](https://travis-ci.org/{{username}}/{{project_name}}.png?branch={{branch}})  (build status) 

and  

![alt text](https://camo.githubusercontent.com/3a5fbd250633413cd9a1a57ba65e09cb88ef5cf9d1d871fd2be4febb97e7a3b3/68747470733a2f2f63646e2e7261776769742e636f6d2f646272676e2f636f7665726167652d62616467652f6d61737465722f6578616d706c652e737667)  (build coverage)

 will be updated based on the test results and posted to the main page of the github repository, most likely 
on the ```README.md``` document. If possible (still un-researched) the test repository will be automatically ran 
directly from github on a schedule basis allowing testing to continue without direct supervision.

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