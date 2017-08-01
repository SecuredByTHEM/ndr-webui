# Copyright (C) 2017  Secured By THEM
# Original Author: Michael Casadevall <michaelc@them.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''Users who access the WebUI component of NDR'''

from flask import render_template
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired

from ndr_webui import app, login_manager

import flask
import flask_login

import ndr_webui
import ndr_server

# First, handle routing for Flask login


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flask_login.login_user(form.user)
        flask.flash("Logged In Successfully")

        # Technically, we could redirect to where the user wanted to go,
        # but since we're a sensitive app, we'll go back to the index vs.

        return flask.redirect(flask.url_for('index'))

    return render_template('login.html',
                           title='Login',
                           form=form)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    flask.flash("Logged Out Successfully")
    return flask.redirect(flask.url_for("login"))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return flask.redirect('/login')

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

class LoginForm(Form):
    '''Validates the login form and checks that a username/password is correct'''
    username = TextField('email', [DataRequired()])
    password = PasswordField('password', [DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        '''Validates the user'''

        user = User.get_by_email(self.username.data)
        if user is None:
            flask.flash('Unknown username')
            return False

        if not user.check_password(self.password.data):
            flask.flash('Invalid password')
            return False

        self.user = user
        return True

class User(object):
    '''Represents a user who can log into the system and (possibly) manage recorders'''

    def __init__(self, email):
        self.email = email
        self.pg_id = 10

    @classmethod
    def get_by_email(cls, email):
        '''Gets a user account by email address'''
        user_obj = User(email)
        user_obj.pg_id = 11

        return user_obj

    @classmethod
    def get_by_id(cls, pg_id):
        '''Gets a user by ID number'''
        user_obj = User("test")
        user_obj.pg_id = pg_id

        return user_obj

    def is_active(self):
        '''Is the user account active and validated?'''
        return True

    def is_authenticated(self):
        '''Is this user authenticated to login'''
        return True

    def get_id(self):
        '''Return a unique identifer for this user'''
        return self.pg_id

    def check_password(self, password):
        '''Checks that the password is valid for a given user'''
        return True
