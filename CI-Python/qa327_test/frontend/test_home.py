import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

# Moch a sample user
test_user = User(
    email='testfrontend@test.com',
    name='test frontend',
    password=generate_password_hash('test_Frontend!2'),
    balance=5000
)

# Moch some sample ticksets
test_tickets = [
    {'name': 't1', 'price': '100'}
]

@patch('qa327.backend.get_user', return_value=test_user)
@patch('qa327.backend.login_user', return_value=test_user)
def login_decorator(inner_function, self, *_):
    def wrapped_inner(self, *_):
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", test_user.email)
        self.type("#password", "test_Frontend!2")
        # click enter button
        self.click('input[type="submit"]')
        
        cur_url = self.get_current_url()
        self.assertEquals(cur_url, "http://localhost:8081/")
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
    @login_decorator
    def test_main_header(self, *_):
        # open index page
        self.open(base_url + '/')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome " + test_user.name, "welcome-header")
        
    #This page shows user balance.
    @pytest.mark.skip(reason="Not testing yet")
    def test_user_balance(self, *_):
        
        pass
    #This page shows a logout link, pointing to /logout
    @pytest.mark.skip(reason="Not testing yet")
    def test_logout_visual(self, *_):
        pass
    #This page lists all available tickets. Information including the quantity of each ticket, the owner's email, and the price, for tickets that are not expired.
    @pytest.mark.skip(reason="Not testing yet")
    def test_ticket_list(self, *_):
        pass
    #This page contains a form that a user can submit new tickets for sell. Fields: name, quantity, price, expiration date
    @pytest.mark.skip(reason="Not testing yet")
    def test_sell_form_visuals(self, *_):
        pass
    #This page contains a form that a user can buy new tickets. Fields: name, quantity
    @pytest.mark.skip(reason="Not testing yet")
    def test_buy_form_visuals(self, *_):
        pass
    #This page contains a form that a user can update existing tickets. Fields: name, quantity, price, expiration date
    @pytest.mark.skip(reason="Not testing yet")
    def test_update_form_visuals(self, *_):
        pass
    #The ticket-selling form can be posted to /sell
    @pytest.mark.skip(reason="Not testing yet")
    def test_sell_post(self, *_):
        pass
    #The ticket-buying form can be posted to /buy
    @pytest.mark.skip(reason="Not testing yet")
    def test_buy_post(self, *_):
        pass
    #The ticket-update form can be posted to /update
    @pytest.mark.skip(reason="Not testing yet")
    def test_update_post(self, *_):
        pass
