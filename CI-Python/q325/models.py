from q325 import app
from flask_sqlalchemy import SQLAlchemy

"""
This file defines all models used by the server
These models provide us a object-oriented access
to the underlying database, so we don't need to 
write SQL queries such as 'select', 'update' etc.
"""


db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    """
    A user model which defines the sql table
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    balance = db.Column(db.Integer)


class Ticket(db.Model):
    """
    A ticket model which defines the sql table
    """
    id = db.Column(db.Integer, primary_key=True)
    ticket_name = db.Column(db.String(100))
    num_tickets = db.Column(db.Integer)
    ticket_price = db.Column(db.Integer)
    ticket_date = db.Column(db.Date)
    ticket_owner = db.Column(db.String(100))

# it creates all the SQL tables if they do not exist
with app.app_context():
    db.create_all()
    db.session.commit()
