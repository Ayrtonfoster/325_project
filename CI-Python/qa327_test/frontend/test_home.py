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
    ticket_name = "test ticket",
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
    
    def test_redirect_login(self, *_):
        """
        R3.0.1: Check user not logged in redirect to /login
        """
        # open / page
        self.open(base_url + '/')
        self.assert_element("#login_title")
        self.assert_text("Log In", "#login_title") 
    
    @login_pass
    def test_main_header(self, *_):
        """
        R3.1.1: Check element present containing welcome message "Hi {user.name}"
        """
        self.assert_element("#welcome-header")
        self.assert_text("Welcome " + test_user.name, "#welcome-header")  
    @login_pass
    def test_user_balance(self, *_):
        """
        R3.2.1: Check element present containing user balance
        """
        self.assert_element("#account-balance")
        self.assert_text("Your balance is: " + str(test_user.balance) + " !", "#account-balance")
    
    @login_pass
    def test_logout_visual(self, *_):
        """
        R3.3.1: Check element present containing link to /logout
        """
        self.assert_element("#logout")
        self.assert_text("logout", "#logout") 
        #Find the logout element and confirm it contains the correct hyperlink
        logout_element=self.driver.find_element_by_id('logout')
        logout_link=logout_element.get_attribute("href")  
        self.assert_equal(logout_link, base_url + "/logout")
    @login_pass
    def test_ticket_list(self, *_):
        """
        R3.4.1: Check ticket table element present with a row matching a non expired ticket in the database
        """
        self.assert_element("#tickets")
        ticket_info = self.driver.find_element_by_id('tickets').text
        #Look within the text of the table and confirm all values of all tickets exist
        for ticket in test_tickets:
            self.assertIn(str(ticket.ticket_name),ticket_info)
            self.assertIn(str(ticket.num_tickets),ticket_info)
            self.assertIn(str(ticket.ticket_price),ticket_info)
            self.assertIn(str(ticket.ticket_date),ticket_info)
            self.assertIn(str(ticket.ticket_owner),ticket_info)
    @login_pass
    def test_sell_form_visuals(self, *_):
        """
        R3.5.1: Check sell form present with all fields
        """
        self.assert_element("#sell_ticket_name")
        self.assert_element("#sell_num_tickets")
        self.assert_element("#sell_ticket_price")
        self.assert_element("#sell_ticket_date")
        self.assert_element("#sell_btn-submit")    
    @login_pass
    def test_buy_form_visuals(self, *_):
        """
        R3.6.1: Check buy form present with all fields
        """ 
        self.assert_element("#buy_ticket_name")
        self.assert_element("#buy_num_tickets")
        self.assert_element("#buy_btn-submit")
    @login_pass
    def test_update_form_visuals(self, *_):
        """
        R3.7.1: Check update form present with all fields
        """
        self.assert_element("#update_ticket_name")  
        self.assert_element("#update_num_tickets")  
        self.assert_element("#update_ticket_price")  
        self.assert_element("#update_ticket_date")  
        self.assert_element("#update_btn-submit")  
    @login_pass
    def test_sell_post(self, *_):
        """
        R3.8.1: Check form POST to /sell
        """
        #Find the sell form, confirm the method and action attributes
        sell_form_info=self.driver.find_element_by_id('sell_form')
        sell_method=sell_form_info.get_attribute("method")
        sell_action=sell_form_info.get_attribute("action") 
        self.assertEqual(sell_method,"post")
        self.assertEqual(sell_action, base_url + "/sell")
        #Input ticket data
        self.type("#sell_ticket_name", "test sell post name")
        self.type("#sell_num_tickets", "10" )
        self.type("#sell_ticket_price", "50" )
        self.type("#sell_ticket_date",  "2022\t1231") 
        self.click('input[id="sell_btn-submit"]')
        #Confirm correct page and no 404 error /etc
        self.assert_element("#welcome-header")
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, base_url + "/sell")
    @login_pass
    @patch('qa327.backend.get_ticket', return_value=test_tickets[0])
    def test_buy_post(self, *_):
        """
        R3.9.1: Check form POST to /buy
        """
        #Find the buy form, confirm the method and action attributes
        buy_form_info=self.driver.find_element_by_id('buy_form')
        buy_method=buy_form_info.get_attribute("method")
        buy_action=buy_form_info.get_attribute("action") 
        self.assertEqual(buy_method , "post")
        self.assertEqual(buy_action, base_url + "/buy")
        #Input ticket data
        self.type("#buy_ticket_name", test_tickets[0].ticket_name)
        self.type("#buy_num_tickets", "1" )
        #Confirm correct page and no 404 error /etc
        self.assert_element("#welcome-header")
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, base_url + "/") 
    @login_pass
    @patch('qa327.backend.get_ticket', return_value=test_tickets[0])
    def test_update_post(self, *_):
        """
        R3.10.1: Check form POST to /update
        """
        #Find the update form, confirm the method and action attributes
        update_form_info=self.driver.find_element_by_id('update_form')
        update_method=update_form_info.get_attribute("method")
        update_action=update_form_info.get_attribute("action") 
        self.assertEqual(update_method,"post")
        self.assertEqual(update_action, base_url + "/update")
        #Input ticket data
        self.type("#update_ticket_name", test_tickets[0].ticket_name)
        self.type("#update_num_tickets", test_tickets[0].num_tickets)
        self.type("#update_ticket_price", test_tickets[0].ticket_price)
        self.type("#update_ticket_date",  "2022\t1231") 
        self.click('input[id="update_btn-submit"]')
        #Confirm correct page and no 404 error /etc
        self.assert_element("#welcome-header")
        cur_url = self.get_current_url()
        self.assertEqual(cur_url, base_url + "/update")
        
