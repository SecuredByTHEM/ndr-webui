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
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from ndr_webui import app, login_manager

import bcrypt

import psycopg2

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
    '''Loads a user for Flask'''
    nsc = ndr_webui.config.get_ndr_server_config()
    db_conn = ndr_webui.config.get_db_connection()

    # Specification says this has to return none, not return an exception so
    try:
        return User.get_by_id(nsc, user_id, db_conn=db_conn)
    except psycopg2.InternalError:
        return None

class LoginForm(Form):
    '''Validates the login form and checks that a username/password is correct'''
    email = StringField('email', [DataRequired()])
    password = PasswordField('password', [DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        '''Validates the user'''
        nsc = ndr_webui.config.get_ndr_server_config()
        db_conn = ndr_webui.config.get_db_connection()

        try:
            user = User.get_by_email(nsc, self.email.data, db_conn=db_conn)
        except psycopg2.InternalError as e:
            flask.flash('1: Unknown email/password')
            # Reset the DB connection
            db_conn.rollback()
            return False

        if user.check_password(self.password.data) is False:
            flask.flash('Unknown email/password')
            return False

        self.user = user
        return True

class User(object):
    '''Represents a user who can log into the system and (possibly) manage recorders'''

    def __init__(self, nsc):
        self.nsc = nsc
        self.username = None
        self.email = None
        self.real_name = None
        self.password_hash = None
        self.pg_id = None
        self.org_id = None
        self.active = False
        self.superadmin = False

    @classmethod
    def from_dict(cls, nsc, user_dict):
        '''Creates a user object from a dictionary'''
        user_obj = User(nsc)

        user_obj.username = user_dict['username']
        user_obj.email = user_dict['email']
        user_obj.real_name = user_dict['real_name']
        user_obj.password_hash = user_dict['password_hash']
        user_obj.pg_id = user_dict['id']
        user_obj.active = user_dict['active']
        user_obj.superadmin = user_dict['superadmin']

        return user_obj

    @classmethod
    def get_by_username(cls, nsc, username, db_conn=None):
        '''Gets a user account by email address'''

        return cls.from_dict(nsc,
                             nsc.database.run_procedure_fetchone(
                                 "webui.select_user_by_username",
                                 [username],
                                 existing_db_conn=db_conn))

    @classmethod
    def get_by_email(cls, nsc, email, db_conn=None):
        '''Gets a user account by email address'''

        return cls.from_dict(nsc,
                             nsc.database.run_procedure_fetchone(
                                 "webui.select_user_by_email",
                                 [email],
                                 existing_db_conn=db_conn))

    @classmethod
    def get_by_id(cls, nsc, user_id, db_conn=None):
        '''Gets a user by ID number'''

        return cls.from_dict(nsc,
                             nsc.database.run_procedure_fetchone(
                                 "webui.select_user_by_id",
                                 [user_id],
                                 existing_db_conn=db_conn))

    @property
    def is_active(self):
        '''Is the user account active and validated?'''
        return self.active

    @property
    def is_anonymous(self):
        '''Is user anonymous (never used)'''
        return False

    @property
    def is_authenticated(self):
        '''Is this user authenticated to login'''
        return True

    def get_id(self):
        '''Return a unique identifer for this user'''
        return self.pg_id

    def check_password(self, password):
        '''Checks that the password is valid for a given user'''

        # I'd technically prefer to do this in the database as I feel like the PW hash
        # algo and such is an implementation detail, but it's always best practice to hash
        # the PW at the first possible point so here it is.

        if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(self.password_hash, 'utf-8')):
            return True

        return False
