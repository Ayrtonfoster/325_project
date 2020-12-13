import pytest
from seleniumbase import BaseCase

from unittest.mock import patch

from qa327_test.conftest import base_url
from qa327.models import User
from werkzeug.security import generate_password_hash
from datetime import date, timedelta

test_user = User(
    email='user@domain.com',
    name='test user',
    password=generate_password_hash('Password!1'),
    balance=5000
)

dateTime = date.today()
dateTime = dateTime + timedelta(days=10)
future_date = dateTime.strftime("%Y\t%m%d")
format_date = dateTime.strftime("%Y-%m-%d")


@pytest.mark.usefixtures('server')
@patch('qa327.backend.get_user', return_value=test_user)
class IntegrationPostingTest(BaseCase):

    def test_posting(self, *_):
        """
        Test that user can post a ticket for sale, using full system from login through logout
        """

        # log in patched user
        self.open(base_url + '/login')
        self.type('#email', 'user@domain.com')
        self.type('#password', 'Password!1')
        self.click('input[type="submit"]')

        # post a ticket for sale
        self.type("#sell_ticket_name", "PostingTestTicket")
        self.type("#sell_num_tickets", "15")
        self.type("#sell_ticket_price", "15")
        self.type("#sell_ticket_date", future_date)  # use date that is ahead of today's date
        self.click('input[id="sell_btn-submit"]')

        # Check for posted ticket in table
        self.driver.find_element_by_id(f'PostingTestTicket%15%15%{format_date}%user@domain.com')

        # check that url is /sell
        self.assertEqual(self.get_current_url(), base_url + "/sell")

        # logout
        self.open(base_url + '/logout')
