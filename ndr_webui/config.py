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

'''Handles configuration for NDR WebUI in Flask'''

# Well this is something of a special panda. For our sanity, we reuse a lost of the NDR
# server code which handles database connections, transaction management, and a bunch of
# other deep magicial voodoo. As such, we need to bring up an NDR server config, and then
# punt it into the Flask global context so database transactions can run in line with everything

# Yay for magic; we'll assume we're using the default NDR server config path for now

import logging

import ndr_webui
import ndr_server
import traceback

from flask import g, current_app
from flask_login import current_user

import psycopg2

import collections

ViewCommonVariables = collections.namedtuple(
    'ViewCommonVariables', ['nsc', 'db_conn', 'user']
)

def get_common_variables(title):
    '''Most of the views on the site requires a bunch of common variables such as the current
    user and such. This returns a tuple with NSC, the user, formatted title, and the DB
    connection'''

    nsc = get_ndr_server_config()
    db_conn = get_db_connection()

    user = None
    if current_user.get_id() is not None:
        user = ndr_webui.User.read_by_id(
            nsc,
            current_user.get_id(),
            db_conn=db_conn
        )

    vcv = ViewCommonVariables(
        nsc=nsc,
        db_conn=db_conn,
        user=user
    )

    return vcv

def site_name():
    '''Returns the name of the site'''
    return current_app.config.get('SITE_NAME', 'Unknown Site')

def get_ndr_server_config():
    '''Returns the NDR server configuration'''
    return ndr_webui.NSC

def get_db_connection():
    '''For the life of the process, we'll have one connection open'''

    if not hasattr(g, 'db_conn'):
        nsc = get_ndr_server_config()
        g.db_conn = nsc.database.get_connection()
    return g.db_conn

def db_teardown(error):
    '''Commits or rolls back the DB if everything went as planned'''

    # If we're in test mode, we need to do a rollback instead of commit
    nsc = get_ndr_server_config()
    no_sql_commit = current_app.config.get('NO_SQL_COMMIT', False)

    if hasattr(g, 'db_conn'):
        if error is None and no_sql_commit is False:
            g.db_conn.commit()
        else:
            g.db_conn.rollback()

        # Return the connection to the pool if it's open
        if g.db_conn.closed == 0:
            nsc.database.return_connection(g.db_conn)
