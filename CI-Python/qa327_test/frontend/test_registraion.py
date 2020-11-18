import pytest
from seleniumbase import BaseCase
from flask import render_template, request, session, redirect

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the frontend homepage.

The tests will only test the frontend portion of the program, by patching the backend to return
specfic values. For example:

@patch('qa327.backend.get_user', return_value=test_user)

Will patch the backend get_user function (within the scope of the current test case)
so that it return 'test_user' instance below rather than reading
the user from the database.

Annotate @patch before unit tests can mock backend methods (for that testing function)
"""

# Moch a sample user
test_user = User(
    email='testfrontend@test.com',
    name='test0',
    password=generate_password_hash('test_Frontend!2')
)

# Moch some sample ticksets
test_tickets = [
    {'name': 't1', 'price': '100'}
]


class FrontEndHomePageTest(BaseCase):

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_success(self, *_):
        """
        This is a sample front end unit test to login to home page
        and verify if the tickets are correctly listed.
        """
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "test_Frontend!2")
        # click enter button
        self.click('input[type="submit"]')
        
        # after clicking on the browser (the line above)
        # the front-end code is activated 
        # and tries to call get_user function.
        # The get_user function is supposed to read data from database
        # and return the value. However, here we only want to test the
        # front-end, without running the backend logics. 
        # so we patch the backend to return a specific user instance, 
        # rather than running that program. (see @ annotations above)
        
        
        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test0", "#welcome-header")


    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_password_failed(self, *_):
        """ Login and verify if the tickets are correctly listed."""
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "testfrontend@test.com")
        self.type("#password", "wrong_password")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email/password format is incorrect.", "#message")


    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_registration_inaccessible(self, *_):
        """
        R2.0.1: Check that re-registration is bypassed for a user that is already logged in
        """
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "test_Frontend!2")
        # click enter button
        self.click('input[type="submit"]')
        
        # open home page
        self.open(base_url)

        # try to open register page
        self.open(base_url + '/register')   

        # Check if / page is opened for logged in user
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/")


    def test_registration_accessible(self, *_):
        """
        R2.1.1: Check that rregistration is accessible for a user that is not logged in
        """
        # try to open register page
        self.open(base_url + '/register')   

        # Check if / page is opened for logged in user
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/register")


    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_page_elements(self, *_):
        """
        R2.2.1: Check that "email", "user name", "password", and "password2" elements are present in 
                login page and that they are all form text inputs
        """

        # open login page
        self.open(base_url + '/register')
        self.assert_element("#email")
        self.assert_element("#name")
        self.assert_element("#password")
        self.assert_element("#password2")


    def test_with_empty_fields(self, *_):
        """
        R2.4.1: Test email cannot be empty
        R2.4.2: Test password cannot be empty
        R2.6.1: Test username cannot be empty
        """

        self.open(base_url + '/register')    

        # fill empty email
        self.type("#email", "")
        self.type("#name", "test0")        
        self.type("#password", "test_Frontend!2")        
        self.type("#password2", "test_Frontend!2")

        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Email format is incorrect.", "#message")


        # fill empty password
        self.type("#email", "test_frontend@test.com")
        self.type("#name", "test0")        
        self.type("#password", "")        
        self.type("#password2", "")

        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Password format is incorrect.", "#message")   


        # fill empty username
        self.type("#email", "test_frontend6@test.com")
        self.type("#name", "")        
        self.type("#password", "#Pasta123")        
        self.type("#password2", "#Pasta123")

        # click enter button
        self.click('input[type="submit"]')
        
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Name format is incorrect.", "#message")

    
    def test_valid_entries(self, *_):
        """
        R2.4.3: Test whether valid emails pass formatting checks
        R2.4.5: Test whether valid passowrd inputs pass formating checks
        """
        self.open(base_url + '/register')    

        # fill empty email
        self.type("#email", "test_frontend@test.com")
        self.type("#name", "test0")        
        self.type("#password", "test_Frontend!2")        
        self.type("#password2", "test_Frontend!2")

        # click enter button
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)


    def test_invalid_entries(self, *_):
        """
        R2.4.4: Check if failure of "email" input against RFC 5322 fails to register
        """
        self.open(base_url + '/register')    

        # fill empty email
        self.type("#email", "Abc.example.com")
        self.type("#name", "test0")        
        self.type("#password", "test_Frontend!2")        
        self.type("#password2", "test_Frontend!2")

        # click enter button
        self.click('input[type="submit"]')

        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Email format is incorrect.", "#message")



    def test_invalid_password(self, *_):
        """
        R2.4.6: Check if failure of "password" inputs against password regex fails registration
        """
        self.open(base_url + '/register')    

        # fill empty email
        self.type("#email", "test_frontend6@test.com")
        self.type("#name", "test0")        
        self.type("#password", "test")        
        self.type("#password2", "test")

        # click enter button
        self.click('input[type="submit"]')
        
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Password format is incorrect.", "#message")


    def test_matching_password(self, *_):
        """
        R2.5.1: Check if password and password2 different fails to register
        """
        self.open(base_url + '/register')    

        # fill empty email
        self.type("#email", "test_frontend6@test.com")
        self.type("#name", "tester0")        
        self.type("#password", "#Pasta123")        
        self.type("#password2", "#Pasta1234")

        # click enter button
        self.click('input[type="submit"]')
        
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Confirm Password format is incorrect.", "#message")


    def test_invalid_username(self, *_):
        """
        R2.6.2: Check username alphanumeric only	
        R2.6.3: Check no space at start	
        R2.6.4: Check no space at end	
        R2.7.1: Check username too short
        R2.7.2: Check username too long
        """
        self.open(base_url + '/register')    

        # fill non alphanumeric username
        self.type("#email", "test_frontend6@test.com")
        self.type("#name", "-!?")        
        self.type("#password", "#Pasta123")        
        self.type("#password2", "#Pasta123")

        # click enter button
        self.click('input[type="submit"]')
        
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Name format is incorrect.", "#message")

        
        # fill username starting with space
        self.type("#email", "test_frontend6@test.com")
        self.type("#name", " aaaaaaaaa")        
        self.type("#password", "#Pasta123")        
        self.type("#password2", "#Pasta123")

        # click enter button
        self.click('input[type="submit"]')
        
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Name format is incorrect.", "#message")


        # fill username ending with space
        self.type("#email", "test_frontend6@test.com")
        self.type("#name", "aaaaaaaa ")        
        self.type("#password", "#Pasta123")        
        self.type("#password2", "#Pasta123")

        # click enter button
        self.click('input[type="submit"]')
        
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Name format is incorrect.", "#message")


        # fill too short username
        self.type("#email", "test_frontend76@test.com")
        self.type("#name", "a")        
        self.type("#password", "#Pasta123")        
        self.type("#password2", "#Pasta123")

        # click enter button
        self.click('input[type="submit"]')
        
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Name format is incorrect.", "#message")


        # fill too long username
        self.type("#email", "test_frontend76@test.com")
        self.type("#name", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")        
        self.type("#password", "#Pasta123")        
        self.type("#password2", "#Pasta123")

        # click enter button
        self.click('input[type="submit"]')
        
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Name format is incorrect.", "#message")



    def test_duplicate_emails(self, *_):
        """
        R2.4.3: Check to ensure you can't create a second account with same email
        """
        self.open(base_url + '/register')    

        # fill empty email
        self.type("#email", "test_frontend76@test.com")
        self.type("#name", "aaaaaaaa")        
        self.type("#password", "#Pasta123")        
        self.type("#password2", "#Pasta123")

        # click enter button
        self.click('input[type="submit"]')
        
        self.open(base_url + '/register')    

        # fill empty email
        self.type("#email", "test_frontend76@test.com")
        self.type("#name", "bbbbbbbbbb")        
        self.type("#password", "#Pasta12")        
        self.type("#password2", "#Pasta12")

        # click enter button
        self.click('input[type="submit"]')

        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("This email is already in use", "#message")


    def test_register_login(self, *_):
        """
        R2.10.1: Test if you can register then login with that account
        """
        self.open(base_url + '/register')    

        # fill empty email
        self.type("#email", "test_frontend76@test.com")
        self.type("#name", "bob")        
        self.type("#password", "#Pasta123")        
        self.type("#password2", "#Pasta123")

        # click enter button
        self.click('input[type="submit"]')
        
        self.open(base_url + '/login')   

        self.type("#email", "test_frontend76@test.com")
        self.type("#password", "#Pasta123")

        # click enter button
        self.click('input[type="submit"]')
        
        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome bob", "#welcome-header")