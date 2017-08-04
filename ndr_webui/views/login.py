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

# First, handle routing for Flask login

from flask import render_template
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from ndr_webui import app, login_manager

import psycopg2

import flask
import flask_login

import ndr_webui

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
        return ndr_webui.User.get_by_id(nsc, user_id, db_conn=db_conn)
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
            user = ndr_webui.User.get_by_email(nsc, self.email.data, db_conn=db_conn)
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
