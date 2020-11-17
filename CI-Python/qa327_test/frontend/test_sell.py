import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the frontend of the sell function outlined as R4/sell
in A1_Testcase_Summary.md file.

The tests will only test the frontend portion of the program by patching the backend to return
the correct data base values.
"""

test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)

# Moch some sample tickets
test_tickets = [
    {'name': 't1', 'price': '100'}
]

class FrontEndSellFunctionTest(BaseCase):

    # def test_sell_page_exists(self, *_):
    #     # R4.0.1
    #     # This requirement is deprecated, the /sell page is incorporated into the / page
    #     pass

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.login_user', return_value=test_user)
    def test_sell_name_regex(self, *_):
        # R4.1.1
        # self.open(base_url + '/') # Go to page with ticket sale ability
        #
        # # Fill in ticket information
        # self.type("#ticket_name", "  weinyHut")
        # self.type("#num_tickets", "15")
        # self.type("#ticket_price", "15")
        # self.type("#ticket_date", "2021-06-23")
        #
        # # Hit 'Post Ticket'
        # self.click('input[id="btn-submit"]')
        #
        # # Check for failed to sell ticket message
        # self.assert_element("#sell_message")
        # self.assert_text("Ticket name does not follow guideline", "#sell_message")

        pass


    # def test_sell_name_length(self, *_):
    #     # R4.2.1
    #     pass
    #
    # def test_sell_name_length_long(self, *_):
    #     # R4.2.2
    #     pass
    #
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

