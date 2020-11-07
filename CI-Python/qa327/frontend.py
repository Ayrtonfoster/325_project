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


def login_redirect(inner_function):
    """
    :param inner_function: any python function that accepts a user object

    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.

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
                # if the user exists, call the inner_function
                # with user as parameter
                return redirect('/')
        else:
            # else, redirect to the login page
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

    # not sure if this needed for return value
    error_message = None

    # email and password not empty
    if email == "":
        return "Email"
        # return "Email cannot be empty"
    elif password == "":
        return "Password"
        # return "Password cannot be empty"

    # Email conforms to RFC 5322
    regexp = re.compile(r'([!#-\'*+/-9=?A-Z^-~-]+(\.[!#-\'*+/-9=?A-Z^-~-]+)*|"([]!#-[^-~ \t]|(\\[\t -~]))+")@([!#-\'*+/\
        -9=?A-Z^-~-]+(\.[!#-\'*+/-9=?A-Z^-~-]+)*|\[[\t -Z^-~]*])')
    if regexp.match(email) is None:
        return "Email"

    # password must have minimum length 6, at least one upper case, at least one lower case, and at least one
    # special character
    if len(password) < 6:  # minimum length 6,
        return "Password"
        # return "The password must have minimum length 6"
    lower = [char for char in password if char.islower()]
    if len(lower) == 0:  # at least one lower case,
        return "Password"
        # return "The password must have at least one lower case"
    upper = [char for char in password if char.isupper()]
    if len(upper) == 0:  # at least one upper case,
        return "Password"
        # return "The password must have at least one upper case"
    special = [char for char in password if not char.isalnum()]
    if len(special) == 0:  # at least one special character
        return "Password"
        # return "The password must have at least one special character"

    if name is None or password2 is None:
        # done checks for login
        return error_message

    # Now check name and password2 for register use case

    # User name has to be non-empty, longer than 2 characters and less than 20 characters.
    elif not 2 <= len(name) <= 20:
        return "Name"
        # return "name must be between 2 and 20 characters"

    # Space allowed only if it is not the first or the last character
    elif name[0] == " " or name[-1] == " ":
        return "Name"
        # return "First and last characters of name cannot be a space"

    # Name must be alphanumeric only
    elif not name.replace(" ", "").isalnum():
        return "Name"
        # return "Name must be alphanumeric only"

    elif password2 != password:
        return "Confirm Password"
        # return "Passwords must match"

    return error_message


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    format_error_attribute = check_user_format(email, password, name=name, password2=password2)

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
    ticket_name = request.form.get('ticket_name')
    num_tickets = request.form.get('num_tickets')
    ticket_price = request.form.get('ticket_price')
    ticket_date = request.form.get('ticket_date')
    error_message = None

    #ticket_date_2 = datetime.date(int(ticket_date))
    date = datetime.datetime.strptime(ticket_date, '%Y-%m-%d').date()


    if len(ticket_name) < 1:
        error_message = "format error"
    else:
        if not bn.post_tickets(ticket_name, num_tickets, ticket_price, date):
            error_message = "Failed to store ticket info."

    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    #if error_message:
    #    return render_template('index.html', message=error_message)
    return redirect('/', code=303)


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
