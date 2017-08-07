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
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_login import LoginManager

import psycopg2

import flask
import flask_login

import ndr_webui

login_blueprint = flask.Blueprint('login', __name__,
                                  template_folder='templates')
login_manager = LoginManager()

@login_blueprint.record_once
def on_load(state):
    '''Initialized login manager for the app'''
    login_manager.init_app(state.app)

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    '''Display and generate the login form'''
    form = LoginForm()

    vcv = ndr_webui.config.get_common_variables("Login")

    if form.validate_on_submit():
        flask_login.login_user(form.user)
        flask.flash("Logged In Successfully", 'success')

        # Technically, we could redirect to where the user wanted to go,
        # but since we're a sensitive app, we'll go back to the index vs.

        return flask.redirect(flask.url_for('organizations.index'))

    return render_template('login.html',
                           vcv=vcv,
                           form=form)

@login_blueprint.route('/logout')
def logout():
    flask_login.logout_user()
    flask.flash("Logged Out Successfully", 'success')
    return flask.redirect(flask.url_for(".login"))

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

class LoginForm(FlaskForm):
    '''Validates the login form and checks that a username/password is correct'''
    email = StringField('email', [DataRequired()])
    password = PasswordField('password', [DataRequired()])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        '''Validates the user'''
        nsc = ndr_webui.config.get_ndr_server_config()
        db_conn = ndr_webui.config.get_db_connection()

        try:
            user = ndr_webui.User.get_by_email(nsc, self.email.data, db_conn=db_conn)
        except psycopg2.InternalError:
            flask.flash('Unknown email/password', 'danger')
            return False

        if user.check_password(self.password.data) is False:
            flask.flash('Unknown email/password', 'danger')
            return False

        self.user = user
        return True
