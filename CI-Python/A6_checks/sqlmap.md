| Test Name                             | Test Function                                                                       | Error in Output                                                            | Cause of Error                                                                            | Solution                                                      |
|---------------------------------------|-------------------------------------------------------------------------------------|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| test_show_login_not: R1.1.1           | Check if the default page before login is /login                                    | Check if the deselenium.common.exceptions.NoSuchElementException: Message: | Login page had no id tag for title                                                        | Gave the login.html page an id for its title (id=login_title) |
| test_login_redirect_pass: R1.5.1      | Check if the post request submitted requests to / upon login success                | Redundant 