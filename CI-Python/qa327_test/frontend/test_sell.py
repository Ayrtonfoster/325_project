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

    def test_sell_page_exists(self, *_):
        # R4.0.1

        # This requirement is deprecated, the /sell page is incorporated into the / page

        pass

    def test_sell_name_regex(self, *_):
        # R4.1.1
        pass

    def test_sell_name_length(self, *_):
        # R4.2.1
        pass

    def test_sell_name_length_long(self, *_):
        # R4.2.2
        pass

    def test_sell_qunatity_inside(self, *_):
        # R4.3.1
        pass

    def test_sell_qunatity_outside(self, *_):
        # R4.3.2
        pass

    def test_sell_price_inside(self, *_):
        # R4.4.1
        pass

    def test_sell_price_outside(self, *_):
        # R4.4.2
        pass

    def test_sell_date_proper(self, *_):
        # R4.5.1
        pass

    def test_sell_date_improper(self, *_):
        # R4.5.2
        pass

    def test_sell_date_not_exist(self, *_):
        # R4.5.3
        pass

    def test_sell_date_past(self, *_):
        # R4.5.4
        pass

    def test_sell_error_redirection(self, *_):
        # R4.6.1
        pass

    def test_sell_error_message(self, *_):
        # R4.6.2
        pass

    def test_sell_display_correct(self, *_):
        # R4.7.1
        pass

    def test_sell_display_duplicates(self, *_):
        # R4.7.2
        pass

