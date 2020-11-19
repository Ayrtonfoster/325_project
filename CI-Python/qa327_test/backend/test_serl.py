import pytest
from seleniumbase import BaseCase
from faker import Faker
from numpy import random
import qa327.backend as bn
from datetime import date
from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


class BackendSellTest(BaseCase):
    def test_post_tickets(self, *_):

        # Create a user and store the seed values
        for n in range(100):
            rand_seed = random.randint(1, 999999)
            fake = Faker()
            Faker.seed(rand_seed)

            today = date.today()

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

