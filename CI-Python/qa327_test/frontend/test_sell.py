import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from datetime import date, timedelta
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the frontend of the sell function outlined as R4/sell
in A1_Testcase_Summary.md file.

The tests will only test the frontend portion of the program by patching the backend to return
the correct data base values.
"""

dateTime = date.today()
dateTime + timedelta(days=10)
future_date = dateTime.strftime("%Y\t%m%d")
format_date = dateTime.strftime("%Y-%m-%d")

test_user = User(
    email='test_sellerpage@test.com',
    name='test_sellerpage',
    password=generate_password_hash('test_sellerPage!2')
)

# Moch some sample tickets
test_tickets = [
    {'ticket_name': 'testTicket',
     'ticket_price': '15', 'num_tickets': '15',
     'ticket_date': format_date, 'ticket_owner': 'test_sellerpage@test.com'}
]

'''
login_pass is a decorator which logs in the user before each test
It contains tests to confirm that login was successful as well
'''


@patch('qa327.backend.get_user', return_value=test_user)
@patch('qa327.backend.get_all_tickets', return_value=test_tickets)
@patch('qa327.backend.login_user', return_value=test_user)
def login_pass(inner_function, self, *_):
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.login_user', return_value=test_user)
    def wrapped_inner(self, *_):
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_sellerpage@test.com")
        self.type("#password", "test_sellerPage!2")
        # click enter button
        self.click('input[type="submit"]')

        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/")
        return inner_function(self, *_)

    # return the wrapped version of the inner_function:
    wrapped_inner.__name__ = inner_function.__name__
    return wrapped_inner

class FrontEndSellFunctionTest(BaseCase):

    @login_pass
    def test_sell_name_regex(self, *_):

        # R4.1.1
        self.open(base_url) # Go to page with ticket sale ability

        # Fill in ticket information
        self.type("#sell_ticket_name", "   spaceTest") # test with space as first entry
        self.type("#sell_num_tickets", "15")
        self.type("#sell_ticket_price", "15")
        self.type("#sell_ticket_date", future_date) # use date that is ahead of todays date

        # Hit 'Post Ticket'
        self.click('input[id="sell_btn-submit"]')

        # Check for failed to sell ticket message
        self.assert_element("#sell_message")
        self.assert_text("Ticket name does not follow guideline", "#sell_message")

        self.open(base_url)  # Go to page with ticket sale ability

        # Fill in ticket information
        self.type("#sell_ticket_name", "@$$ @$$")  # non alphanumeric name
        self.type("#sell_num_tickets", "15")
        self.type("#sell_ticket_price", "15")
        self.type("#sell_ticket_date", future_date)  # use date that is ahead of todays date

        # Hit 'Post Ticket'
        self.click('input[id="sell_btn-submit"]')

        # Check for failed to sell ticket message
        self.assert_element("#sell_message")
        self.assert_text("Ticket name does not follow guideline", "#sell_message")

    @login_pass
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_sell_name_length(self, *_):
        # R4.2.1

        self.open(base_url)  # Go to page with ticket sale ability

        # Fill in ticket information
        self.type("#sell_ticket_name", "testTicket")
        # test name shorter than 60 characters
        self.type("#sell_num_tickets", "15")
        self.type("#sell_ticket_price", "15")
        self.type("#sell_ticket_date", future_date)  # use date that is ahead of todays date

        # Hit 'Post Ticket'
        self.click('input[id="sell_btn-submit"]')

        # Check for posted ticket in table and /sell was reached
        ticket_id = self.driver.find_element_by_id("testTicket%15%15%"
                            + format_date + "%test_sellerpage@test.com").text

        self.assertIn("testTicket", ticket_id)
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, base_url + "/sell")

    @login_pass
    def test_sell_name_length_long(self, *_):
        # R4.2.2

        self.open(base_url)  # Go to page with ticket sale ability

        # Fill in ticket information
        self.type("#sell_ticket_name", "This Ticket Name Will Be Longer Than 60,"
                                       " Characters and Will Fail for that Reason")
                                            # test name longer than 60 characters
        self.type("#sell_num_tickets", "15")
        self.type("#sell_ticket_price", "15")
        self.type("#sell_ticket_date", future_date)  # use date that is ahead of todays date

        # Hit 'Post Ticket'
        self.click('input[id="sell_btn-submit"]')

        # Check for failed to sell ticket message
        self.assert_element("#sell_message")
        self.assert_text("Ticket name does not follow guideline", "#sell_message")


    # def test_sell_qunatity_inside(self, *_):
    #     # R4.3.1
    #     pass
    #
    # def test_sell_qunatity_outside(self, *_):
    #     # R4.3.2
    #     pass
    #
    # def test_sell_price_inside(self, *_):
    #     # R4.4.1
    #     pass
    #
    # def test_sell_price_outside(self, *_):
    #     # R4.4.2
    #     pass
    #
    # def test_sell_date_proper(self, *_):
    #     # R4.5.1
    #     pass
    #
    # def test_sell_date_improper(self, *_):
    #     # R4.5.2
    #     pass
    #
    # def test_sell_date_not_exist(self, *_):
    #     # R4.5.3
    #     pass
    #
    # def test_sell_date_past(self, *_):
    #     # R4.5.4
    #     pass
    #
    # def test_sell_error_redirection(self, *_):
    #     # R4.6.1
    #     pass
    #
    # def test_sell_error_message(self, *_):
    #     # R4.6.2
    #     pass
    #
    # def test_sell_display_correct(self, *_):
    #     # R4.7.1
    #     pass
    #
    # def test_sell_display_duplicates(self, *_):
    #     # R4.7.2
    #     pass

