import pytest
from faker import Faker
from datetime import date, timedelta
from seleniumbase import BaseCase
import selenium


import time
from q325_test.conftest import base_url
from unittest.mock import patch
from q325.models import db, User, Ticket
from werkzeug.security import generate_password_hash, check_password_hash


dateTime = date.today()
dateTime = dateTime + timedelta(days=10)
future_date = dateTime.strftime("%Y\t%m%d")
format_date = dateTime.strftime("%Y-%m-%d")


# Moch a sample user
fake = Faker()
email = fake.email()
name = fake.name()
# Mock a sample user
test_user = User(
    email = "UncleSteve@email.com",
    name='test_sellerpage',
    password=generate_password_hash('test_Frontend!2'),
    balance=5000
)


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
        self.type("#email", "UncleSteve@email.com")
        self.type("#password", "test_Frontend!2")
        # click enter button
        self.click('input[type="submit"]')
        
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/")
        return inner_function(self, *_)
    # return the wrapped version of the inner_function:
    wrapped_inner.__name__ = inner_function.__name__
    return wrapped_inner

class FrontEndUpdateFunctionTest(BaseCase):

    #@patch('q325.backend.get_user', return_value=test_user)
    #@patch('q325.backend.get_all_tickets', return_value=test_tickets)
    #@patch('q325.backend.login_user', return_value=test_user)
    @login_pass
    def test_update_name_regex(self, *_):
        """
        R5.0.1: Check if bad ticket name fails
        R5.1.1: Check if ticket name shorter than 60 works
        R5.1.2: Check if ticket name longer than 60 fails
        R5.5.2: Check if the system allows you to purchase a ticket that exist
        """

        self.type("#update_ticket_name", "testfrontend@test.com")
        self.type("#update_num_tickets", "22")
        self.type("#update_ticket_price", "44")
        self.type("#update_ticket_date",  future_date)
        self.click('input[id="update_btn-submit"]')

        self.assert_element("#update_message")
        self.assert_text("Ticket name does not follow guideline", "#update_message")


        self.type("#update_ticket_name", "bbbbbbbbbbbbbbbbbbbbbbbbbbboooooooooooooooooooooooobbbbbbbbbbbbbbbbbbbbbbbbb")
        self.type("#update_num_tickets", "22")
        self.type("#update_ticket_price", "44")
        self.type("#update_ticket_date",  future_date)
        self.click('input[id="update_btn-submit"]')

        self.assert_element("#update_message")
        self.assert_text("Ticket name does not follow guideline", "#update_message")


        self.type("#update_ticket_name", "testTicket")
        self.type("#update_num_tickets", "15")
        self.type("#update_ticket_price", "15")
        self.type("#update_ticket_date",  future_date)

        self.click('input[id="update_btn-submit"]')

        time.sleep(10)

        ticket_id = self.driver.find_element_by_id("testTicket%15%15%" 
                            + format_date + "%test_sellerpage@test.com").text

        self.assertIn("testTicket", ticket_id)
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, base_url + "/update")

    @login_pass
    def test_valid_input(self, *_):
        """
        R5.2.1: Check if "ticket quantity" inside of range is accepted by front end
        R5.3.1: Check if "ticket price" inside of range is accepted by front end
        R5.4.1: Check if entered date using proper format is accepted by front end
        """
    
        self.type("#update_ticket_name", "testTicket")
        self.type("#update_num_tickets", "15")
        self.type("#update_ticket_price", "15")
        self.type("#update_ticket_date",  future_date)

        self.click('input[id="update_btn-submit"]')

        time.sleep(10)

        ticket_id = self.driver.find_element_by_id("testTicket%15%15%" 
                            + format_date + "%test_sellerpage@test.com").text

        self.assertIn("testTicket", ticket_id)
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, base_url + "/update")

    @login_pass
    def test_update_ticket_num_regex(self, *_):
        """
        R5.2.2: Check if "ticket quantity" outside of range causes updating action failure
        """

        self.type("#update_ticket_name", "testTicket")
        self.type("#update_num_tickets", "-20")
        self.type("#update_ticket_price", "44")
        self.type("#update_ticket_date",  future_date)
        self.click('input[id="update_btn-submit"]')

        self.assert_element("#update_message")
        self.assert_text("Number of tickets outside of range", "#update_message")


        self.type("#update_ticket_name", "testTicket")
        self.type("#update_num_tickets", "120")
        self.type("#update_ticket_price", "44")
        self.type("#update_ticket_date",  future_date)
        self.click('input[id="update_btn-submit"]')

        self.assert_element("#update_message")
        self.assert_text("Number of tickets outside of range", "#update_message")


    @login_pass
    def test_update_ticket_price_regex(self, *_):
        """
        R5.3.2: Check if "ticket price" outside of range causes updating action failure
        """

        self.type("#update_ticket_name", "testTicket")
        self.type("#update_num_tickets", "20")
        self.type("#update_ticket_price", "5")
        self.type("#update_ticket_date",  future_date)
        self.click('input[id="update_btn-submit"]')

        self.assert_element("#update_message")
        self.assert_text("Ticket price outside of range", "#update_message")


        self.type("#update_ticket_name", "testTicket")
        self.type("#update_num_tickets", "20")
        self.type("#update_ticket_price", "210")
        self.type("#update_ticket_date",  future_date)
        self.click('input[id="update_btn-submit"]')

        self.assert_element("#update_message")
        self.assert_text("Ticket price outside of range", "#update_message")


    @login_pass
    def test_update_ticket_date_regex(self, *_):
        """
        R5.4.4: Check if dates that have already passed cause updating action failure
        R5.6.1: Check if when an error message is created a redirection to the / page occurs
        """

        self.type("#update_ticket_name", "testTicket")
        self.type("#update_num_tickets", "50")
        self.type("#update_ticket_price", "50")
        self.type("#update_ticket_date",  "1998\t1231")
        self.click('input[id="update_btn-submit"]')


        # Check for signs that index.html was loaded
        self.assert_element("#update_message")
        self.assert_element("#welcome-header")
        self.assert_element("#account-balance")
        self.assert_element("#sell_header")
        self.assert_element("#buy_header")
        self.assert_text("Date entered not valid", "#update_message")