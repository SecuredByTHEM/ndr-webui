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

import ndr_server
from ndr_webui import app
from flask import g

NDR_SERVER_CONFIG = '/etc/ndr/ndr_server.yml'

def init_ndr_server_config():
    '''Sets up the NDR server config on first run if it's not already'''
    g.nsc = ndr_server.Config(app.logger, NDR_SERVER_CONFIG)

def get_ndr_server_config():
    '''Returns the NDR server configuration'''
    if not hasattr(g, 'nsc'):
        init_ndr_server_config()

    return g.nsc

