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
from ndr_webui import app

from flask import g

def init_ndr_server_config():
    '''Sets up the NDR server config on first run if it's not already'''
    ndr_webui.NSC = ndr_server.Config(app.logger, app.config['NDR_SERVER_CONFIG'])
    ndr_webui.NSC.logger.info("Initialized NSC Configuration")

def get_ndr_server_config():
    '''Returns the NDR server configuration'''
    if ndr_webui.NSC is None:
        init_ndr_server_config()

    return ndr_webui.NSC

def get_db_connection():
    '''For the life of the process, we'll have one connection open'''

    if not hasattr(g, 'db_conn'):
        nsc = get_ndr_server_config()
        g.db_conn = nsc.database.get_connection()

    return g.db_conn

@app.teardown_appcontext
def db_teardown(error):
    '''Commits or rolls back the DB if everything went as planned'''
    # If we're in test mode, we need to do a rollback instead of commit
    no_sql_commit = False
    if hasattr(app.config, 'NO_SQL_COMMIT'):
        no_sql_commit = True

    if hasattr(g, 'db_conn'):
        if error is None and no_sql_commit is False:
            g.db_conn.commit()
        else:
            g.db_conn.rollback()
