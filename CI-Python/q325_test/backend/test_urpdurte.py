import pytest
from seleniumbase import BaseCase
from faker import Faker
from numpy import random
import q325.backend as bn
from datetime import datetime
from q325_test.conftest import base_url
from unittest.mock import patch
from q325.models import db, User, Ticket
from werkzeug.security import generate_password_hash, check_password_hash

seller = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)

test_tickets = Ticket(
    id = 1234,
    ticket_name = "test ticket",
    num_tickets = 20,
    ticket_price = 10,
    ticket_date = "2021-06-23",
    ticket_owner = "Uncle Steve"
)



class BackendUpdateTest(BaseCase):

    @patch('q325.backend.get_ticket', return_value=None)
    def no_ticket(self, *_):
        return bn.update_ticket("name", 10, 15, '2090-02-01')
        # should return None

    @patch('q325.backend.get_ticket', return_value=test_tickets)
    def ticket(self, *_):
        return bn.update_ticket("test ticket", 20, 10, '2021-06-23')
        # should return test_tickets

    def test_update_ticket(self, *_):
        # Will be performing a block coverage test
        # Although not efficient, there are only 8 statements in the entire method
        # Coverage testing is good enough in this case

        no_ticket_result = self.no_ticket()
        ticket_result = self.ticket()

        if no_ticket_result == None and ticket_result == True:
            pass
        else:
            raise ValueError("backend test case for update_ticket failed")






