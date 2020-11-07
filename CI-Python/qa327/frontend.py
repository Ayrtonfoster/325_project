from flask import render_template, request, session, redirect
from qa327 import app
import qa327.backend as bn
import datetime
import re


"""
This file defines the front-end part of the service.
It elaborates how the services should handle different
http requests from the client (browser) through templating.
The html templates are stored in the 'templates' folder. 
"""

# Reusable REGEX
ticket_name_reg = re.compile("^\S[a-zA-Z0-9_ ]{1,60}\S$")
"""The name of the ticket has to be alphanumeric-only, and space allowed only 
    if it is not the first or the last character. The name of the ticket is 
    no longer than 60 characters"""

def login_redirect(inner_function):
    """
    :param inner_function: any python function that accepts a user object

    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will redirect to the home page

    To wrap a function, we can put a decoration on that function.
    Example:

    @login_redirect
    def login_get():
        pass
    """
    def wrapped_inner():
        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            user = bn.get_user(email)
            if user:
                # if the user exists, redirect to /
                return redirect('/')
        else:
            # else, call the inner function
            return inner_function()

    # return the wrapped version of the inner_function:
    wrapped_inner.__name__ = inner_function.__name__
    return wrapped_inner


@app.route('/register', methods=['GET'])
@login_redirect
def register_get():

    # templates are stored in the templates folder
    return render_template('register.html', message='')


def check_user_format(email, password, name=None, password2=None):

    error_message = None

    # Email must conform to RFC 5322
    regexp = re.compile(r'([!#-\'*+/-9=?A-Z^-~-]+(\.[!#-\'*+/-9=?A-Z^-~-]+)*|"([]!#-[^-~ \t]|(\\[\t -~]))+")@([!#-\'*+/\
        -9=?A-Z^-~-]+(\.[!#-\'*+/-9=?A-Z^-~-]+)*|\[[\t -Z^-~]*])')
    if regexp.match(email) is None:

        return "Email"

    # password must have minimum length 6, at least one upper case, at least one lower case, and at least one
    # special character
    lower = [char for char in password if char.islower()]
    upper = [char for char in password if char.isupper()]
    special = [char for char in password if not char.isalnum()]
    if len(password) < 6\
            or len(lower) == 0\
            or len(upper) == 0\
            or len(special) == 0:

        return "Password"

    if name is None or password2 is None:

        # done checks for login
        return error_message

    # Now check name and password2 for register use case

    # User name has to be non-empty, longer than 2 characters and less than 20 characters.
    # Space allowed only if it is not the first or the last character
    # Name must be alphanumeric only
    if not 2 <= len(name) <= 20\
            or name[0] == " " or name[-1] == " "\
            or not name.replace(" ", "").isalnum():

        return "Name"

    # Passwords must match
    if password2 != password:

        return "Confirm Password"

    return error_message


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    format_error_attribute = check_user_format(email, password, name=name, password2=password2)

    error_message = None
    if format_error_attribute is not None:
        error_message = '{} format is incorrect.'.format(format_error_attribute)
    else:
        user = bn.get_user(email)
        if user:
            error_message = "This email is already in use"
        elif not bn.register_user(email, name, password, password2):
            error_message = "Failed to store user info."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/login', methods=['GET'])
@login_redirect
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    format_error_attribute = check_user_format(email, password)

    if format_error_attribute is not None:
        return render_template('login.html', message="email/password format is incorrect.")

    user = bn.login_user(email, password)
    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information 
        between browser and the end server. Typically it is encrypted 
        and stored in the browser cookies. They will be past 
        along between every request the browser made to this services.
        
        Here we store the user object into the session, so we can tell
        if the client has already login in the following sessions.

        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/sell', methods=['POST'])
def sell_tickets():

    # Retrieve info from forms
    ticket_name = request.form.get('ticket_name')
    num_tickets = request.form.get('num_tickets')
    ticket_price = request.form.get('ticket_price')
    ticket_date = request.form.get('ticket_date')

    # Check if the inputs are following correct format
    error_message = ticket_info_sanitizer(ticket_name, num_tickets, ticket_price = ticket_price)

    # Get info on the user
    email = session['logged_in']
    user = bn.get_user(email)

    #Convert datetime into something we can put in db
    date = datetime.datetime.strptime(ticket_date, '%Y-%m-%d').date()

    if error_message == None:
        if not bn.post_tickets(ticket_name, num_tickets, ticket_price, date, email):
            error_message = "Failed to store ticket info."

    # get Info on Tickets
    tickets = bn.get_all_tickets()

    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('index.html', user=user, sell_message=error_message, tickets=tickets)

    return render_template('index.html', user=user, tickets=tickets)

@app.route('/buy', methods=['POST'])
def buy_tickets():

    # Retrieve info from forms
    ticket_name = request.form.get('ticket_name')
    num_tickets = request.form.get('num_tickets')


    # Find out info on logged in user and tickets
    email = session['logged_in']
    user = bn.get_user(email)

    error_message = ticket_info_sanitizer(ticket_name, num_tickets)
    
    # Subtract the bought tickets from amount available
    if error_message is None:
        # Retrieve info on ticket being bought
        ticket_info = bn.get_ticket(ticket_name)

        if ticket_info is not None:
            # Calc cost of ticket
            ticket_cost = ticket_info.ticket_price * int(num_tickets)
            service_fee = ticket_cost * 0.35
            tax = ticket_cost * 0.05

            overall_cost = ticket_cost + service_fee + tax

            if (ticket_info.num_tickets < int(num_tickets)):
                error_message = "requested more than available tickets, "

            if (user.balance - overall_cost < 0):
                error_message = "Not enough money in balance"

            if not bn.buy_tickets(ticket_name, num_tickets):
                error_message = "Not a concert"


    # get Info on Tickets
    tickets = bn.get_all_tickets()

    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('index.html', user=user, buy_message=error_message, tickets=tickets)
    
    # Update the buyer ans sellers balance to reflect the transaction
    bn.update_balance(user.email, ticket_info.ticket_owner, ticket_cost, overall_cost)

    #Re-render page with updates
    return render_template('index.html', user=user, buy_message=error_message, tickets=tickets)


@app.route('/update', methods=['POST'])
def update_tickets():
    
    # Retrieve info from forms
    ticket_name = request.form.get('ticket_name')
    num_tickets = request.form.get('num_tickets')
    ticket_price = request.form.get('ticket_price')
    ticket_date = request.form.get('ticket_date')
    error_message = ticket_info_sanitizer(ticket_name, num_tickets, ticket_price = ticket_price)

    # Find out info on logged in user and tickets
    email = session['logged_in']
    user = bn.get_user(email)

    #Convert datetime into something we can put in db
    date = datetime.datetime.strptime(ticket_date, '%Y-%m-%d').date()

    if error_message == None:
        if not bn.update_ticket(ticket_name, num_tickets, ticket_price, date):
            error_message = "No such Ticket with that name."

    # get Info on Tickets
    tickets = bn.get_all_tickets()

    # if there is any error messages when updating ticket info
    # at the backend, go back to the register page.
    if error_message:
        return render_template('index.html', user=user, update_message=error_message, tickets=tickets)

    return render_template('index.html', user=user, update_message=error_message, tickets=tickets)

def ticket_info_sanitizer(ticket_name, num_tickets, ticket_price = 11):
    # Check if the inputs are following correct format

    if (not bool(ticket_name_reg.match(ticket_name))):
        return "Ticket name does not follow guideline"

    elif (int(num_tickets) < 1 or int(num_tickets) > 100):
        return "Number of tickets outside of range"

    elif (int(ticket_price) < 10 or int(ticket_price) > 100):
        return "Ticket price outside of range"

    else: return None

def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object

    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.

    To wrap a function, we can put a decoration on that function.
    Example:

    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            user = bn.get_user(email)
            if user:
                # if the user exists, call the inner_function
                # with user as parameter
                return inner_function(user)
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    wrapped_inner.__name__ = inner_function.__name__
    return wrapped_inner


@app.route('/')
@authenticate
def profile(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals
    tickets = bn.get_all_tickets()
    return render_template('index.html', user=user, tickets=tickets)
