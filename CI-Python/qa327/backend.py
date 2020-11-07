from qa327.models import db, User, Ticket
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

"""
This file defines all backend logic that interacts with database and other services
"""


def get_user(email):
    """
    Get a user by a given email
    :param email: the email of the user
    :return: a user that has the matched email address
    """
    user = User.query.filter_by(email=email).first()
    return user


def login_user(email, password):
    """
    Check user authentication by comparing the password
    :param email: the email of the user
    :param password: the password input
    :return: the user if login succeeds
    """
    # if this returns a user, then the name already exists in database
    user = get_user(email)
    if not user or not check_password_hash(user.password, password):
        return None
    return user


def post_tickets(ticket_name, num_tickets, ticket_price, ticket_date):
    """
    Add tickets from form to db
    """
    # store the encrypted password rather than the plain password
    new_ticket = Ticket(ticket_name=ticket_name, num_tickets=num_tickets, ticket_price=ticket_price, ticket_date=ticket_date)

    db.session.add(new_ticket)
    db.session.commit()
    return None


def get_all_tickets():
    """
    retrieve tickets from db
    """
    # store the encrypted password rather than the plain password
    #ticket = Ticket.all()
    return []

def register_user(email, name, password, password2):
    """
    Register the user to the database
    :param email: the email of the user
    :param name: the name of the user
    :param password: the password of user
    :param password2: another password input to make sure the input is correct
    :return: an error message if there is any, or None if register succeeds
    """

    hashed_pw = generate_password_hash(password, method='sha256')
    # store the encrypted password rather than the plain password
    new_user = User(email=email, name=name, password=hashed_pw, balance=5000)
    db.session.add(new_user)
    try:
        db.session.commit()
        return True
    except Exception as e:
    #log your exception in the way you want -> log to file, log as error with default logging, send by email. It's upon you
        db.session.rollback()
        db.session.flush() # for resetting non-commited .add()
        return False
    