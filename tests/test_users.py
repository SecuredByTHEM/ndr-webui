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

import bcrypt
import ndr_server
import ndr_webui
from ndr_webui import app

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CONFIG = THIS_DIR + "/test_config.yml"

ROOT_USERNAME = "admin"
ROOT_PW = b"rootpassword"
ROOT_EMAIL = "test_user@themtests.com"
ROOT_NAME = "Admin Test User"

class TestUsers(unittest.TestCase):
    '''Test user object behaviors'''

    def setUp(self):
        # Setup Flask basic configuration
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['NDR_SERVER_CONFIG'] = TEST_CONFIG
        self.app = app.test_client()

        self._nsc = ndr_server.Config(logging.getLogger(), TEST_CONFIG)

        # We need to process test messages, so override the base directory for
        # this test
        self._db_connection = self._nsc.database.get_connection()

        crypted_pw = str(bcrypt.hashpw(ROOT_PW, bcrypt.gensalt()), 'utf-8')

        # We need to create the root user account which can manipulate the other ones
        root_userid = self._nsc.database.run_procedure_fetchone(
            "admin.create_user", [ROOT_USERNAME, ROOT_EMAIL, crypted_pw, ROOT_NAME],
            self._db_connection
        )[0]

        # Activate the user, then make it a super-admin
        self._nsc.database.run_procedure(
            "admin.activate_user", [root_userid], self._db_connection
        )

    def tearDown(self):
        self._db_connection.rollback()
        self._nsc.database.close()

    def test_create_user(self):
        '''Tests creation of a user'''
