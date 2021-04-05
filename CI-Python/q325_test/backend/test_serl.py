import pytest
from seleniumbase import BaseCase
from faker import Faker
from numpy import random
import q325.backend as bn
from datetime import date, timedelta
from q325_test.conftest import base_url
from unittest.mock import patch
from q325.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


class BackendSellTest(BaseCase):

    @staticmethod
    def test_post_tickets():

        # Create a user and store the seed values
        for n in range(100):
            rand_seed = random.randint(1, 999999)
            fake = Faker()
            Faker.seed(rand_seed)

            today = date.today()
            today = today + timedelta(days=1)
            ticket_name = fake.name()
            num_tickets = random.randint(1, 101)
            ticket_price = random.randint(10, 101)
            ticket_date = fake.date_between(start_date='today')
            email = fake.email()

            fail_seed = [rand_seed, num_tickets, ticket_price, ticket_date]

            # Run the backed function and grab boolean return
            bool_post_tickets = bn.post_tickets(ticket_name, num_tickets, ticket_price, ticket_date, email)

            if not bool_post_tickets:
                raise ValueError('A Failure was caused by the following seed:' + str(fail_seed))

    @staticmethod
    def test_post_duplicate_ticket():
        """
        Check that a ticket cannot be posted with a duplicate name
        """
        email = 'user@domain.com'
        ticket_name = 'testTicket'
        price = 20
        quantity = 15

        today = date.today()
        future_day = today + timedelta(days=10)
        future_date = future_day.strftime("%Y\t%m%d")

        if bn.get_ticket(ticket_name) is None:
            bn.post_tickets(ticket_name, quantity, price, future_date, email)

        assert bn.post_tickets(ticket_name, quantity, price, future_date, email) is False
