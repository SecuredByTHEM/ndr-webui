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

import unittest
import logging
import os

import psycopg2

import bcrypt
import ndr_server
import ndr_webui
from ndr_webui import app

import tests.common

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CONFIG = THIS_DIR + "/test_config.yml"

class TestLogin(unittest.TestCase):
    '''Tests login and log out behaviors'''

    @classmethod
    def setUpClass(cls):
        # Setup Flask basic configuration
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['NDR_SERVER_CONFIG'] = TEST_CONFIG
        app.config['NO_SQL_COMMIT'] = True
        cls.app = app.test_client()

        # Reinitialize NSC context with the test config
        ndr_webui.config.init_ndr_server_config()

    @classmethod
    def tearDownClass(cls):
        ndr_webui.NSC.database.close()

    def test_login(self):
        '''Tests logging in as the admin user'''

        with app.test_request_context():
            tests.common.create_admin_user(self)
            rv = tests.common.login(self, tests.common.ROOT_EMAIL, tests.common.ROOT_PW)
            self.assertIn(b"Logged In Successfully", rv.data)
