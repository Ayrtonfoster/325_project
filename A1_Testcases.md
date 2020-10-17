
##R7.1 - Logout will invalid the current session and redirect to the login page. After logout, the user shouldn't be able to access restricted pages.  

###Testcase R7.1.1 - Confirm after logout that user is redirected to the login page
Mocking:   
backend.get_user to authenticate user not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
/validate user is redirected to login  

###Testcase R7.1. - Confirm after logout that user succeed to access /login  
Mocking:   
backend.get_user to authenticate user not logged in  

Actions:
open /logout (invalidate any logged-in sessions that may exist))  
open /login  
validate users current page is /login  

###Testcase R7.1.3 - Confirm after logout that user succeed to access /register  
Mocking:   
backend.get_user to authenticate user not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
open /register  
validate users current page is /register  

###Testcase R7.1.4 - Confirm after logout that user fails to access /logout  
Mocking:   
backend.get_user to authenticate user is not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
open /register  
validate users current page is /register  

###Testcase R7.1.5 - Confirm after logout that user fails to access /  
Mocking:   
backend.get_user to authenticate user is not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
open /  
validate users is redirected to /login   

###Testcase R7.1.6 - Confirm after logout that user fails to access /sell  
Mocking:   
backend.get_user to authenticate user is not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
open /sell  
validate users is redirected to /login   

###Testcase R7.1.7 - Confirm after logout that user fails to access /update  
Mocking:   
backend.get_user to authenticate user is not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
open /update  
validate users is redirected to /login   

###Testcase R7.1.8 - Confirm after logout that user fails to access /buy  
Mocking:   
backend.get_user to authenticate user is not logged in  

Actions:  
open /logout (invalidate any logged-in sessions that may exist))  
open /buy  
validate users is redirected to /login   

###Testcase R7.1.9 - Confirm after logout that user fails to access /\* any other urls    
open /logout (invalidate any logged-in sessions that may exist))  
open /nonexistantpage  
validate a 404 error is returned  




