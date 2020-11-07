# CMPE327 AS2 Group X
#### Ayrton Foster, Eric Leask, Franc Marrato, Matthew Kruzich
## Project Structure
### Overview
The architecture can be split into frontend, backend, and database. The frontend contains one function per http route 
for handling of its logic. The frontend will enforce constraints related to user input, such as format of form fields, 
and handle HTML serving. In the case where website behaviour depends on reading or writing to the database, the 
frontend will make a call to the backend, which will handle database access. The backend will enforce any constraints 
on consistency of objects in database. There are two classes of objects in the database: Users and Tickets.
### Method Outline

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

- Environments
- Responsibilities
- Budget Management