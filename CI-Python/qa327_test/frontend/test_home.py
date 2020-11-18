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
    balance=5000
)

# Moch some sample ticksets
test_tickets = [Ticket(
    id = 1234,
    ticket_name = "test_ticket",
    num_tickets = 20,
    ticket_price = 10,
    ticket_date = "2021-06-23",
    ticket_owner = "Uncle Steve"
)]


#Unit Tests require the a user to login to the system
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
    

class MainPageTest(BaseCase):
    #If the user is not logged in, redirect to login page
    def test_redirect_login(self, *_):
        # open index page
        self.open(base_url + '/')
        self.assert_element("#login_title")
        self.assert_text("Log In", "#login_title") 
    #This page shows a header 'Hi {}'.format(user.name)
    @login_pass
    def test_main_header(self, *_):
        self.assert_element("#welcome-header")
        self.assert_text("Welcome " + test_user.name, "#welcome-header")  
    #This page shows user balance.
    @login_pass
    def test_user_balance(self, *_):
        self.assert_element("#account-balance")
        self.assert_text("Your balance is: " + str(test_user.balance) + " !", "#account-balance")
    #This page shows a logout link, pointing to /logout
    @login_pass
    def test_logout_visual(self, *_):
        self.assert_element("#logout")
        self.assert_text("logout", "#logout")  

    #This page lists all available tickets. Information including the quantity of each ticket, the owner's email, and the price, for tickets that are not expired.
    @login_pass
    def test_ticket_list(self, *_):
        self.assert_element("#tickets")
        ticket_info = self.driver.find_element_by_('tickets').text
        for ticket in test_tickets:
            self.assertIn(ticket.ticket_name,ticket_info )
            self.assertIn(ticket.num_tickets,ticket_info)
            self.assertIn(ticket.ticket_price,ticket_info)
            self.assertIn(ticket.ticket_date,ticket_info)
            self.assertIn(ticket.ticket_owner,ticket_info)
        
    #This page contains a form that a user can submit new tickets for sell. Fields: name, quantity, price, expiration date
    @login_pass
    def test_sell_form_visuals(self, *_):
        self.assert_element("#sell_message")
        self.assert_element("#ticket_name")
        self.assert_element("#num_tickets")
        self.assert_element("#ticket_price")
        self.assert_element("#ticket_date")
        self.assert_element("#btn-submit") 

    #This page contains a form that a user can buy new tickets. Fields: name, quantity
    @login_pass
    def test_buy_form_visuals(self, *_):
        pass
    #This page contains a form that a user can update existing tickets. Fields: name, quantity, price, expiration date
    @login_pass
    def test_update_form_visuals(self, *_):
        pass
    #The ticket-selling form can be posted to /sell
    @login_pass
    def test_sell_post(self, *_):
        pass
    #The ticket-buying form can be posted to /buy
    @login_pass
    def test_buy_post(self, *_):
        pass
    #The ticket-update form can be posted to /update
    @login_pass
    def test_update_post(self, *_):
        pass
