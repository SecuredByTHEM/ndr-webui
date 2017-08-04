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

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CONFIG = THIS_DIR + "/test_config.yml"

ROOT_USERNAME = "admin"
ROOT_PW = "rootpassword"
ROOT_EMAIL = "test_user@themtests.com"
ROOT_REAL_NAME = "Admin Test User"

class TestUsers(unittest.TestCase):
    '''Test user object behaviors'''

    @classmethod
    def setUpClass(cls):
        # Setup Flask basic configuration
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['NDR_SERVER_CONFIG'] = TEST_CONFIG
        cls.app = app.test_client()

        # Reinitialize NSC context with the test config
        ndr_webui.config.init_ndr_server_config()

        # We need to process test messages, so override the base directory for
        # this test
        cls._db_connection = ndr_webui.NSC.database.get_connection()

        crypted_pw = str(bcrypt.hashpw(bytes(ROOT_PW, 'utf-8'), bcrypt.gensalt()), 'utf-8')

        # We need to create the root user account which can manipulate the other ones
        cls._root_userid = ndr_webui.NSC.database.run_procedure_fetchone(
            "admin.create_user", [ROOT_USERNAME, ROOT_EMAIL, crypted_pw, ROOT_REAL_NAME],
            cls._db_connection
        )[0]

        # Activate the user, then make it a super-admin
        ndr_webui.NSC.database.run_procedure(
            "admin.activate_user", [cls._root_userid], cls._db_connection
        )

    @classmethod
    def tearDownClass(cls):
        cls._db_connection.rollback()
        ndr_webui.NSC.database.close()

    def test_get_admin_user(self):
        '''Tests getting the admin user'''
        admin_user = ndr_webui.User.get_by_id(ndr_webui.NSC,
                                              self._root_userid,
                                              db_conn=self._db_connection)

        self.assertEqual(ROOT_USERNAME, admin_user.username)
        self.assertEqual(ROOT_REAL_NAME, admin_user.real_name)
        self.assertEqual(ROOT_EMAIL, admin_user.email)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.check_password(ROOT_PW))

    def test_get_admin_user_by_email(self):
        '''Tests getting a user by email address'''
        admin_user = ndr_webui.User.get_by_email(ndr_webui.NSC,
                                                 ROOT_EMAIL,
                                                 db_conn=self._db_connection)

        self.assertEqual(ROOT_USERNAME, admin_user.username)
        self.assertEqual(ROOT_REAL_NAME, admin_user.real_name)
        self.assertEqual(ROOT_EMAIL, admin_user.email)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.check_password(ROOT_PW))

    def test_check_invalid_password(self):
        '''Tests that we properly error out on invalid passwords'''
        admin_user = ndr_webui.User.get_by_id(ndr_webui.NSC,
                                              self._root_userid,
                                              db_conn=self._db_connection)
        self.assertFalse(admin_user.check_password("not the right PW"))

    def test_invalid_user(self):
        '''Tests that we properly error out on invalid passwords'''
        self.assertRaises(psycopg2.InternalError,
                          ndr_webui.User.get_by_id,
                          ndr_webui.NSC,
                          1337,
                          db_conn=self._db_connection)
