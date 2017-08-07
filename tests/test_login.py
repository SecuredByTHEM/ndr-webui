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

import tests.common

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CONFIG = THIS_DIR + "/test_config.yml"
TEST_FLASK_CONFIG = THIS_DIR + "/flask_test_config.cfg"

class TestLogin(unittest.TestCase):
    '''Tests login and log out behaviors'''

    @classmethod
    def setUpClass(cls):
        # Setup Flask basic configuration
        flask_app = ndr_webui.init_app(testing=True,
                                       config_file=TEST_FLASK_CONFIG)
        cls.flask_app = flask_app
        cls.app = flask_app.test_client()

    def test_login(self):
        '''Tests logging in as the admin user'''

        with self.flask_app.app_context():
            rv = tests.common.login(self, tests.common.ROOT_EMAIL, tests.common.ROOT_PW)
            self.assertIn(b"Logged In Successfully", rv.data)

    def test_logout(self):
        '''Tests that logging out works successfully'''
        with self.flask_app.test_request_context():
            tests.common.create_admin_user(self)
            rv = tests.common.login(self, tests.common.ROOT_EMAIL, tests.common.ROOT_PW)
            rv = tests.common.logout(self)
            self.assertIn(b"Logged Out", rv.data)

if __name__ == "__main__":
    unittest.main()
