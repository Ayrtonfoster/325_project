# A3 Failure Report
## Contributers
•	Ayrton Foster

•	Francesco Marrato

•	Eric Leask
 
•	Matthew Kruzich

## R1 /Login | Failure Report

| Test Name                             | Test Function                                                                       | Error in Output                                                            | Cause of Error                                                                            | Solution                                                      |
|---------------------------------------|-------------------------------------------------------------------------------------|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| test_show_login_not: R1.1.1           | Check if the default page before login is /login                                    | Check if the deselenium.common.exceptions.NoSuchElementException: Message: | Login page had no id tag for title                                                        | Gave the login.html page an id for its title (id=login_title) |
| test_login_redirect_pass: R1.5.1      | Check if the post request submitted requests to / upon login success                | Redundant                                                                  | No Error                                                                                  | Combined with test R1.3.1                                     |
| test_login_redirect_pass: R1.8.1      | Check if a correct password returns a True/Pass value when login is requested       | Redundant                                                                  | No Error                                                                                  | Combined with test R1.3.1                                     |
| test_login_redirect_pass: R1.10.1     | If email and password are correct and a login request is made, redirect to / 'home' | Redundant                                                                  | No Error                                                                                  | Combined with test R1.3.1                                     |
| test_login_redirect_fail: R1.5.2      | When a login post fails a redirection to /login is performed                        | Redundant                                                                  | No Error                                                                                  | Combined with test R1.3.2                                     |
| test_login_email_RFC5322: R1.7.1      | Email inputs are checked against RFC 5322 regex                                     | Invalid Test                                                               | Selenium Base cannot explicitly confirm that a RFC 5322  REGEX is used                    | Rolled into test R1.7.2                                       |
| test_login_formating_errors: R1.9.2   | Check if 'pop-up' message is shown on /login page if error_message has ben thrown   | Invalid Test                                                               | When originally outlined error messages were thought to generate a 'pop-up' style message | Rolled into test R1.9.1                                       |
| test_login_formatting_errors: R1.11.2 | Check if 'pop-up' message is shown on /login page if error_message has been thrown  | Invalid Test                                                               | When originally outlined error messages were thought to generate a 'pop-up' style message | Rolled into test R1.11.1                                      |

## R2 /Register | Failure Report

| Test Name                             | Test Function                                                                       | Error in Output                                                            | Cause of Error                                                                            | Solution                                                      |
|---------------------------------------|-------------------------------------------------------------------------------------|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| check_re-registration_is_bypassed: R2.0.1           | Make sure users don't have to re-register if they have already logged in                                            | Redundant          | No Error                                                       | Combined with test R1.3.2 |
| test_redirect_to_registration: R2.1.1      | Check that user registration page is served to a user that is not logged in                | Redundant                                                                  | No Error                                                                                  | Combined with test R1.3.2                                     |
| test_submit_button_exists: R2.3.1      | Check that there is a submit button for registration       | Redundant                                                                  | No Error                                                                                  | Rolled into R.2.1                                     |
| Check user created properly: R2.7.2     | Check if username is too short when registering | Valid Username                                                                  | Code checking whether username is too shirt or too long implemented incorrectly                                                                                  | Fixed logic for username length check                                   |
| Check user created properly: R2.10.1     | Check to ensure user created successfully and can login | Redundant                                                                  | No Error                                                                                  | Combined with test R1.3.1                                     |

   

## R3 / | Failure Report
## R4 /Sell | Failure Report

- To be completed at a later date
## R5 /Update | Failure Report

- To be completed at a later date
## R6 /Buy | Failure Report

- To be completed at a later date
## R7 /Logout | Failure Report
## R8 /* | Failure Report