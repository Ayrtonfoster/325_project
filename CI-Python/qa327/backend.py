from qa327.models import db, User, Ticket
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

"""
This file defines all backend logic that interacts with database and other services
"""


def get_user(email):
    """
    Get a user by a given email

    :param email: the email of the user
    :return: a User that has the matching email address
    """
    user = User.query.filter_by(email=email).first()
    return user


def login_user(email, password):
    """
    Check user authentication by comparing the password

    :param email: the email of the user
    :param password: the password input
    :return: the User if login succeeds, else None
    """
    # if this returns a user, then the name already exists in database
    user = get_user(email)
    if not user or not check_password_hash(user.password, password):
        return None
    return user


def post_tickets(ticket_name, num_tickets, ticket_price, ticket_date, email):
    """
    Add new tickets to the db

    :param ticket_name: The name of the ticket
    :param num_tickets: Number of tickets being created
    :param ticket_price: Price of each ticket
    :param email: email of the ticket owner
    :return: True when ticket created successfully
    """
    # store the encrypted password rather than the plain password
    new_ticket = Ticket(ticket_name=ticket_name, num_tickets=num_tickets,
        ticket_price=ticket_price, ticket_date=ticket_date, ticket_owner=email)

    db.session.add(new_ticket)

    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()  # Rollback the current transaction in progress
        db.session.flush()  # Reset non-commited .add()
        return False


def get_all_tickets():
    """
    Retrieve all tickets from db that are in the future

    :return: list of Tickets
    """
    # Only retrieve tickets that are in the future
    today = date.today()
    ticket = Ticket.query.filter(Ticket.ticket_date > today)

    return ticket


def buy_tickets(ticket_name, num_tickets):
    """
    Buy tickets from form to db

    :param ticket_name: The name of the ticket
    :param num_tickets: Number of tickets being purchased
    :return: True if purchase succeeds, else None
    """
    ticket = get_ticket(ticket_name)
    if not ticket:
        return None

    ticket.num_tickets = ticket.num_tickets - int(num_tickets)

    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()  # Rollback the current transaction in progress
        db.session.flush()  # Reset non-commited .add()
        return False


def get_ticket(ticket_name):
    """
    Get a ticket by a given ticket name

    :param ticket_name: the ticket to be found
    :return: a Ticket with the given ticket_name
    """
    ticket = Ticket.query.filter_by(ticket_name=ticket_name).first()
    return ticket


def update_ticket(ticket_name, num_tickets, ticket_price, date):
    """
    Update a ticket with new info

    :param ticket_name: the name ticket to be found
    :param num_tickets: new number of tickets
    :param ticket_price: new price for each ticket
    :param date: new date of ticket
    :return: True if update succeeds, else None
    """
    ticket = get_ticket(ticket_name)
    if not ticket:
        return None
    
    ticket.num_tickets = num_tickets
    ticket.ticket_price = ticket_price
    ticket.ticket_date = date

    db.session.commit()
    return True


def update_balance(buyer_email, seller_email, ticket_cost, overall_cost):
    """
    Update user balance amounts following ticket purchase

    :param buyer_email: email of ticket buyer
    :param seller_email: email of ticket seller
    :param ticket_cost: how much to be added to seller account
    :param overall_cost: overall cost to buyer
    :return: True if successful, None if buyer or seller not found
    """

    # Retrieve Buyer info
    buyer = get_user(buyer_email)
    if not buyer:
        return None
    
    # Retrieve Seller info
    seller = get_user(seller_email)
    if not seller:
        return None    
    
    # Update Buyer and seller balances
    buyer.balance = buyer.balance - overall_cost
    seller.balance = seller.balance + ticket_cost

    db.session.commit()
    return True


def register_user(email, name, password, password2):
    """
    Register the user to the database

    :param email: the email of the user
    :param name: the name of the user
    :param password: the password of user
    :param password2: another password input to make sure the input is correct
    :return: True if registration succeeds, otherwise False
    """

    hashed_pw = generate_password_hash(password, method='sha256')
    # store the encrypted password rather than the plain password
    new_user = User(email=email, name=name, password=hashed_pw, balance=5000)
    db.session.add(new_user)
    try:
        db.session.commit()
        return True             
    except Exception as e:
        db.session.rollback()   # Rollback the current transaction in progress
        db.session.flush()      # Reset non-commited .add()
        return False       
    