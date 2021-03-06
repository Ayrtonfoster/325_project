import pytest
import numpy as np
from faker import Faker
from seleniumbase import BaseCase

from q325_test.conftest import base_url
from unittest.mock import patch
from q325.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the frontend login page.
"""

fake = Faker()
email = fake.email()
name = fake.name()
# Mock a sample user
test_user = User(
    email=email,
    name=name,
    password=generate_password_hash('test_Frontend!2')
)

# Moch some sample ticksets
test_tickets = [
    {'name': 't1', 'price': '100'}]

class FrontEndLoginFunctionTest(BaseCase):

    def test_show_login_not(self, *_):
        """
        R1.1.1: Check if the default page before login is /login
        """
        self.open(base_url) # open login page

        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/login")
        self.assert_element("#login_title") # Had to create a title for H1 in login
        self.assert_text("Log In", "#login_title") # check if 'Log In' is visible

    def test_login_return_home(self, *_):
        """
        R1.1.2: Check if the home page '/' is inaccessible when not logged in
        """
        # Attempt to open home page (not logged in)
        self.open(base_url + '/')

        # Check if returned to /login page
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/login")
        self.assert_element("#login_title")  # Had to create a title for H1 in login
        self.assert_text("Log In", "#login_title")  # check if 'Log In' is visible

    def test_login_default_message(self, *_):
        """
        R1.2.1: Check if the startup page /login contains the message 'please login' on initial open
        """

        self.open(base_url + '/login')  # open login page

        self.assert_element("#message")  # check for default 'Please login' message
        self.assert_text("Please login", "#message")

    @patch('q325.backend.get_user', return_value=test_user)
    @patch('q325.backend.get_all_tickets', return_value=test_tickets)
    @patch('q325.backend.login_user', return_value=test_user)
    def test_login_redirect_pass(self, *_):
        """
        R1.3.1: If the user is logged in redirect to / 'home' page
        R1.5.1: The login form is submitted and requests / 'home' page
        R1.8.1: Check if a correct password returns a True/Pass value when login is requested
        R1.10.1: If email and password are correct and a login request is made, redirect to / 'home'
        """

        self.open(base_url + '/login')  # go to login page for initial log in

        # fill in login information (correctly)
        self.type("#email", email)
        self.type("#password", "test_Frontend!2")
        # click enter button
        self.click('input[type="submit"]')

        # Check if / page is opened for logged in user
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/")

        self.open(base_url + '/login')  # attempt to go back to /login without signing out

        # Check if / page is opened for logged in user
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/")

    def test_login_redirect_fail(self, *_):
        """
        R1.3.2: When the login post fails test that the webpage does not perform a redirects to / 'home'
        R1.5.2: When a login post fails a redirection to /login is performed
        """

        self.open(base_url + '/login')  # go to login page for initial log in

        # fill in login information (improperly)
        self.type("#email", email)
        self.type("#password", "wrong_password")
        # click enter button
        self.click('input[type="submit"]')

        # check if redirection to /login occurs when failed login post occurs
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/login")

    def test_login_fields(self, *_):
        """
        R1.4.1: Check if the login page includes the minimum fields of email and password
        """

        self.open(base_url + '/login')  # go to login page

        # check if email and password fields exist
        self.assert_element("#email")
        self.assert_element("#password")

    def test_login_empty_fields(self, *_):
        """
        R1.6.1: Check if login does not succeed when the fields are empty
        """

        self.open(base_url + '/login')  # go to login page for initial log in

        # Attempt login with empty fields
        self.type("#email", "")
        self.type("#password", "")

        # Submit login attempt with empty fields
        self.click('input[type="submit"]')

        # Check if login does not work
        self.assert_element("#message")  # check for default 'Please login' message
        self.assert_text("Please login", "#message")

        # Check if we are still on the /login page
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/login")

    def test_login_email_RFC5322(self, *_):
        """
        R1.7.1: Email inputs are checked against RFC 5322 Regex
        R1.7.2: Email inputs checked against RFC 5322 Standard throw error_messages when not met
        """

        # List of first characters that could cause failure of RFC 5322
        false_char = ['.','@','  ','..']

        self.open(base_url + '/login')  # go to login page for initial log in

        # Attempt login with bad email
        self.type("#email", str(np.random.choice(false_char))+email)
        self.type("#password", "test_Frontend!2")

        # Submit login attempt with porr email field
        self.click('input[type="submit"]')

        # Check if we are still on the /login page
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/login")

        self.assert_element("#message")  # check for error_message for bad email
        self.assert_text("email/password format is incorrect.")


    def test_login_password_fail(self, *_):
        """
        R1.8.2: Test if 'bad' password that do not meet the password criteria throw a login error
        """
        # R1.8.2
        self.open(base_url + '/login')  # go to login page for initial log in

        self.type("#email", email)
        self.type("#password", "Sh0r!") # attempt password that is too short
        self.click('input[type="submit"]')

        self.assert_element("#message")  # check for error_message for bad password
        self.assert_text("email/password format is incorrect.")

        self.type("#email", email)
        self.type("#password", "N0LOWER&")  # attempt password with no lower case
        self.click('input[type="submit"]')

        self.assert_element("#message")  # check for error_message for bad password
        self.assert_text("email/password format is incorrect.")

        self.type("#email", email)
        self.type("#password", "n0upper!")  # attempt password with no upper case
        self.click('input[type="submit"]')

        self.assert_element("#message")  # check for error_message for bad password
        self.assert_text("email/password format is incorrect.")

        self.type("#email", email)
        self.type("#password", "n0Special")  # attempt password with no special characters
        self.click('input[type="submit"]')

        self.assert_element("#message")  # check for error_message for bad password
        self.assert_text("email/password format is incorrect.")

    def test_login_formating_errors(self, *_):
        """
        R1.9.1: Check if the /login page is rendered for any formatting errors and message is displayed
        R1.9.2: Check if pop-up message reads "email/password" os shown on /login after error_message is thrown
        R1.11.1: If email or password are incorrect redirect to /login
        R1.11.2: Check if pop-up message reads "email/password" os shown on /login after error_message is thrown
        """

        self.open(base_url + '/login')  # go to login page for initial log in

        # Bad email
        self.type("#email", "invalid_user@test.com")
        self.type("#password", "test_Frontend!2")
        self.click('input[type="submit"]')
        # check if /login page is requested
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/login")
        # check if message is shown
        self.assert_element("#message")
        self.assert_text("login failed")

        # Bad password
        self.type("#email", email)
        self.type("#password", "wrong_password")
        self.click('input[type="submit"]')
        # check if /login page is requested
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/login")
        # check if message is shown
        self.assert_element("#message")
        self.assert_text("email/password format is incorrect.")

