import pytest
from faker import Faker
from seleniumbase import BaseCase
import selenium

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User, Ticket
from werkzeug.security import generate_password_hash, check_password_hash

# Moch a sample user
fake = Faker()
email = fake.email()
name = fake.name()
# Mock a sample user
test_user = User(
    email=email,
    name=name,
    password=generate_password_hash('test_Frontend!2'),
    balance=1000
)

# Moch some sample ticksets
test_tickets = [Ticket(
    id = 1234,
    ticket_name = "test ticket",
    num_tickets = 60,
    ticket_price = 25,
    ticket_date = "2021-06-23",
    ticket_owner = "Uncle Steve"
)]
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
        self.type("#email", email)
        self.type("#password", "test_Frontend!2")
        # click enter button
        self.click('input[type="submit"]')
        
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, "http://localhost:8081/")
        return inner_function(self, *_)
    # return the wrapped version of the inner_function:
    wrapped_inner.__name__ = inner_function.__name__
    return wrapped_inner
    
class BuyTest(BaseCase):
    #Constraint:
    #The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character.
    #Breaks if inputting a ticket that doesn't exist
    #Is not catching non-alphanum values in first/last index of string
    #Fixed regex
    """
        R6.0.1.1: Check if failure "ticket name" inputs against ticket name regex causes selling action failure
    """
    @login_pass
    def test_ticket_alphanumeric(self, *_):
        self.type("#buy_ticket_name", "ticket#") 
        self.type("#buy_num_tickets", "1" )
        self.click('input[id="buy_btn-submit"]')
        self.assert_text("Ticket name does not follow guideline", "#buy_message")
    """
        R6.0.1.2: Check if failure "ticket name" inputs against ticket name regex causes selling action failure
    """    
    @login_pass
    def test_ticket_spaces(self, *_):
        self.type("#buy_ticket_name", " ticket ")
        self.type("#buy_num_tickets", "1" )
        self.click('input[id="buy_btn-submit"]')
        self.assert_text("Ticket name does not follow guideline", "#buy_message")
    """
        R6.1.2: Check if selling action fails with ticket names longer than 60 characters
    """
    #The name of the ticket is no longer than 60 characters
    @login_pass
    def test_ticket_over_length(self, *_):
        self.type("#buy_ticket_name", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        self.type("#buy_num_tickets", "1" )
        self.click('input[id="buy_btn-submit"]')
        self.assert_text("Ticket name does not follow guideline", "#buy_message")
    """
        R6.2.2.1: Check if "ticket quantity" outside of range causes selling action failure
    """
    #The quantity of the tickets has to be more than 0, and less than or equal to 100.
    @login_pass
    def test_purchase_min(self, *_):
        self.type("#buy_ticket_name", test_tickets[0].ticket_name)
        self.type("#buy_num_tickets", "0" )
        self.click('input[id="buy_btn-submit"]')
        self.assert_text("Number of tickets outside of range", "#buy_message")
    """
        R6.2.2.2: Check if "ticket quantity" outside of range causes selling action failure
    """
    @login_pass    
    def test_purchase_max(self, *_):
        self.type("#buy_ticket_name", test_tickets[0].ticket_name)
        self.type("#buy_num_tickets", "101" )
        self.click('input[id="buy_btn-submit"]')
        self.assert_text("Number of tickets outside of range", "#buy_message")
    
   """
   R6.1.1: Check if selling action passes with ticket names shorter than 60 characters
   R6.2.1: Check if "ticket quantity" inside of range is accepted by front end
   R6.3.2: Check if you can buy less than the available amount
   """
    #The ticket name exists in the database and the quantity is more than the quantity requested to buy
    @login_pass 
    @patch('qa327.backend.get_ticket', return_value=test_tickets[0])
    @patch('qa327.backend.buy_tickets', return_value=True)
    def test_ticket_purchase_success(self, *_):
        purchase_num_tickets=5
        self.type("#buy_ticket_name", test_tickets[0].ticket_name)
        self.type("#buy_num_tickets", str(purchase_num_tickets) )
        self.click('input[id="buy_btn-submit"]')
        self.assert_text("", "#buy_message")
    
    """
    R6.3.1:Check if you can buy more tickets than what are available
    """
    @login_pass
    @patch('qa327.backend.get_ticket', return_value=test_tickets[0])
    def test_ticket_over_quantity(self, *_):
        self.type("#buy_ticket_name", test_tickets[0].ticket_name)
        self.type("#buy_num_tickets", "100" )
        self.click('input[id="buy_btn-submit"]')
        self.assert_text("Requested more than available tickets", "#buy_message")
    #Issue gertting Not a concert ticket, implying it did not find the ticket #testcase issue
    #Conditionals for error message were not if elif, were if if 
    
    
    #The user has more balance than the ticket price * quantity + service fee (35%) + tax (5%)
    @login_pass
    @patch('qa327.backend.get_ticket', return_value=test_tickets[0])
    def test_payment(self, *_):
        self.type("#buy_ticket_name", test_tickets[0].ticket_name)
        self.type("#buy_num_tickets", "50" )
        self.click('input[id="buy_btn-submit"]')
        self.assert_text("Not enough money in balance", "#buy_message")
        