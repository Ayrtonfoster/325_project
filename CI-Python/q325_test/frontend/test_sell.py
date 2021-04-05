import pytest
from selenium.webdriver.common.by import By
from seleniumbase import BaseCase

from q325_test.conftest import base_url
from unittest.mock import patch
from datetime import date, timedelta
from q325.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the frontend of the sell function outlined as R4/sell
in A1_Testcase_Summary.md file.

The tests will only test the frontend portion of the program by patching the backend to return
the correct data base values.
"""

dateTime = date.today()
dateTime = dateTime + timedelta(days=10)
future_date = dateTime.strftime("%Y-%m-%d")
format_date = dateTime.strftime("%Y-%m-%d")
past = dateTime - timedelta(days=45)
past_date = past.strftime("%Y-%m-%d")


test_user = User(
    email='test_sellerpage@test.com',
    name='test_sellerpage',
    password=generate_password_hash('test_sellerPage!2')
)

# Moch some sample tickets
test_tickets = [
    {'ticket_name': 'testTicket',
     'ticket_price': '15', 'num_tickets': '15',
     'ticket_date': format_date, 'ticket_owner': 'test_sellerpage@test.com'},
    {'ticket_name': 'ticket_info_correct',
     'ticket_price': '35', 'num_tickets': '80',
     'ticket_date': format_date, 'ticket_owner': 'test_sellerpage@test.com'}
]

'''
login_pass is a decorator which logs in the user before each test
It contains tests to confirm that login was successful as well
'''


@patch('q325.backend.get_user', return_value=test_user)
@patch('q325.backend.get_all_tickets', return_value=test_tickets)
@patch('q325.backend.login_user', return_value=test_user)
def login_pass(inner_function, self, *_):
    @patch('q325.backend.get_user', return_value=test_user)
    @patch('q325.backend.get_all_tickets', return_value=test_tickets)
    @patch('q325.backend.login_user', return_value=test_user)
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
        """
        R4.1.1: Check if the ticket name regex throws an
        error when a ticket name does not follow the guide lines
        """

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
    @patch('q325.backend.get_all_tickets', return_value=test_tickets)
    def test_sell_name_length(self, *_):
        """
        R4.2.1: Check if selling action passes with ticket
        names shorter than 60 characters
        """

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
        """
        R4.2.2: Check if selling action passes with ticket
        names longer than 60 characters
        """

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

    @login_pass
    @patch('q325.backend.get_all_tickets', return_value=test_tickets)
    def test_sell_quantity_inside(self, *_):
        """
        R4.3.1: Check if ticket quantity inside of range
        is accepted by frontend (1-100)
        """

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
    def test_sell_quantity_outside(self, *_):
        """
        R4.3.2: Check if ticket quantity outside of range is
        accepted by frontend (1-100)
        """
        self.open(base_url)  # Go to page with ticket sale ability

        # Fill in ticket information
        self.type("#sell_ticket_name", "too many tickets")
        self.type("#sell_num_tickets", "200") # Tickets more than 100
        self.type("#sell_ticket_price", "15")
        self.type("#sell_ticket_date", future_date)  # use date that is ahead of todays date

        # Hit 'Post Ticket'
        self.click('input[id="sell_btn-submit"]')

        # Check for failed to sell ticket message
        self.assert_element("#sell_message")
        self.assert_text("Number of tickets outside of range", "#sell_message")

    @login_pass
    @patch('q325.backend.get_all_tickets', return_value=test_tickets)
    def test_sell_price_inside(self, *_):
        """
        R4.4.1: Check if ticket price inside of range is
        accepted by front end (10-100)
        """

        self.open(base_url)  # Go to page with ticket sale ability

        # Fill in ticket information
        self.type("#sell_ticket_name", "testTicket")
        # test name shorter than 60 characters
        self.type("#sell_num_tickets", "15")
        # In range # of tickets to sell
        self.type("#sell_ticket_price", "15")
        # In range ticket price
        self.type("#sell_ticket_date", future_date)  # use date that is ahead of todays date

        # Hit 'Post Ticket'
        self.click('input[id="sell_btn-submit"]')

        # Check for posted ticket in table and /sell was reached
        ticket_id = self.driver.find_element_by_id("testTicket%15%15%"
                                                   + format_date + "%test_sellerpage@test.com").text

        self.assertIn("testTicket", ticket_id)
        # check if url is /sell Post request from index.html
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, base_url + "/sell")

    @login_pass
    def test_sell_price_outside(self, *_):
        """
        R4.4.2: Check if ticket price outside of range is
        accepted by front end (10-100)
        """

        self.open(base_url)  # Go to page with ticket sale ability

        # Fill in ticket information
        self.type("#sell_ticket_name", "too many tickets")
        self.type("#sell_num_tickets", "15")
        self.type("#sell_ticket_price", "1500") # price outside of range
        self.type("#sell_ticket_date", future_date)  # use date that is ahead of todays date

        # Hit 'Post Ticket'
        self.click('input[id="sell_btn-submit"]')

        # Check for failed to sell ticket message
        self.assert_element("#sell_message")
        self.assert_text("Ticket price outside of range", "#sell_message")

    @login_pass
    @patch('q325.backend.get_all_tickets', return_value=test_tickets)
    def test_sell_date_proper(self, *_):
        """
        R4.5.1: Check if dates entered using proper format are
        accepted by frontend (yyyy-mm-dd)
        """

        self.open(base_url)  # Go to page with ticket sale ability

        # Fill in ticket information
        self.type("#sell_ticket_name", "testTicket")
        # test name shorter than 60 characters
        self.type("#sell_num_tickets", "15")
        # In range # of tickets to sell
        self.type("#sell_ticket_price", "15")
        # In range ticket price
        self.type("#sell_ticket_date", future_date)
        # using properly formatted date
        # use date that is ahead of todays date

        # Hit 'Post Ticket'
        self.click('input[id="sell_btn-submit"]')

        # Check for posted ticket in table and /sell was reached
        ticket_id = self.driver.find_element_by_id("testTicket%15%15%"
                                                   + format_date + "%test_sellerpage@test.com").text

        self.assertIn(format_date, ticket_id)
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, base_url + "/sell")

    @login_pass
    def test_sell_date_past(self, *_):
        """
        R4.5.4: Check if dates entered that are in the past
        (before today) cause selling action failure
        """
        self.open(base_url)  # Go to page with ticket sale ability

        # Fill in ticket information
        self.type("#sell_ticket_name", "date in past")
        self.type("#sell_num_tickets", "15")
        self.type("#sell_ticket_price", "15")
        self.type("#sell_ticket_date", past_date)  # date is in past

        # Hit 'Post Ticket'
        self.click('input[id="sell_btn-submit"]')

        # Check for failed to sell ticket message
        self.assert_element("#sell_message")
        self.assert_text("Date entered not valid", "#sell_message")

    @login_pass
    def test_sell_error_redirection(self, *_):
        """
        R4.6.1: Check if when an error message occurs a redirection
        to the index.html template occurs
        R4.6.2: Check if when an error message is created the message
        is displayed when the redirection to the index.html template occurs
        """
        self.open(base_url)  # Go to page with ticket sale ability

        # Fill in ticket information
        self.type("#sell_ticket_name", "$WrongName***") # Incorrect Name
        self.type("#sell_num_tickets", "1500") # Out of range ticket numbers
        self.type("#sell_ticket_price", "1500")  # Price outside of range
        self.type("#sell_ticket_date", past_date)  # Date is from past

        # Hit 'Post Ticket'
        self.click('input[id="sell_btn-submit"]')

        # Check for signs that index.html was loaded
        self.assert_element("#welcome-header")
        self.assert_element("#account-balance")
        self.assert_element("#sell_header")
        self.assert_element("#buy_header")
        # Check for failed to sell ticket message
        self.assert_element("#sell_message")
        self.assert_text("Ticket name does not follow guideline", "#sell_message")

    @login_pass
    @patch('q325.backend.get_all_tickets', return_value=test_tickets)
    def test_sell_display_correct(self, *_):
        """
        R4.7.1: Check if a correctly added ticket and its information is displayed
        on the / page of the user
        """

        self.open(base_url)  # Go to page with ticket sale ability

        # Fill in ticket information
        self.type("#sell_ticket_name", "ticket_info_correct")
        # test name shorter than 60 characters
        self.type("#sell_num_tickets", "80")
        # In range # of tickets to sell
        self.type("#sell_ticket_price", "35")
        # In range ticket price
        self.type("#sell_ticket_date", future_date)
        # using properly formatted date
        # use date that is ahead of todays date

        # Hit 'Post Ticket'
        self.click('input[id="sell_btn-submit"]')

        # Check for posted ticket in table and /sell was reached
        ticket_id = self.driver.find_element_by_id("ticket_info_correct%35%80%"
                                                   + format_date + "%test_sellerpage@test.com").text

        # Check that all relevant info is posted to the selling table
        self.assertIn(format_date, ticket_id)
        self.assertIn("80", ticket_id)
        self.assertIn("35", ticket_id)
        self.assertIn("ticket_info_correct", ticket_id)
        self.assertIn("test_sellerpage@test.com", ticket_id)
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, base_url + "/sell")

    @login_pass
    @patch('q325.backend.get_all_tickets', return_value=test_tickets)
    def test_sell_display_duplicates(self, *_):
        """
        R4.7.2: Check if the correct number of tickets (table entries)
        is presented in the ticket list and bottom of / page of user
        """

        self.open(base_url)  # Go to page with ticket sale ability

        # Fill in ticket information Ticket #1
        self.type("#sell_ticket_name", "ticket_info_correct")
        self.type("#sell_num_tickets", "80")
        self.type("#sell_ticket_price", "35")
        self.type("#sell_ticket_date", future_date)

        # Hit 'Post Ticket'
        self.click('input[id="sell_btn-submit"]')

        # Fill in ticket information Ticket #2
        self.type("#sell_ticket_name", "testTicket")
        self.type("#sell_num_tickets", "15")
        self.type("#sell_ticket_price", "15")
        self.type("#sell_ticket_date", future_date)

        # Hit 'Post Ticket'
        self.click('input[id="sell_btn-submit"]')

        table_entries = self.driver.find_element_by_id("ticket_table")
        rows = table_entries.find_elements(By.TAG_NAME, "tr")
        if(len(rows) == 3):
            pass
        else:
            raise ValueError("Looking for 2 table entries got: " + str(len(table_entries)))


