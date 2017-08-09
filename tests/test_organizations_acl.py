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

class TestOrganizationsACL(unittest.TestCase):
    '''Tests organization ACL class'''

    @classmethod
    def setUpClass(cls):
        # Setup Flask basic configuration
        flask_app = ndr_webui.init_app(testing=True,
                                       config_file=TEST_FLASK_CONFIG)
        cls.flask_app = flask_app
        cls.app = flask_app.test_client()

    def test_organization_access_by_admin(self):
        '''Tests successful read of organizations by admin user'''
        # The admin is a superuser, we should see all organizations
        with self.flask_app.app_context():
            nsc = ndr_webui.config.get_ndr_server_config()
            db_conn = ndr_webui.config.get_db_connection()
            admin_user = tests.common.create_admin_user(self)
            org = tests.common.create_organization(self, "test org")

            acled_org = ndr_webui.OrganizationACL.read_by_id(
                nsc, admin_user, org.pg_id, db_conn
            )

            self.assertEqual(org, acled_org)

    def test_read_by_id_acl_failure(self):
        '''Tests that we blow up on an ACL read by id failure'''
        with self.flask_app.app_context():
            nsc = ndr_webui.config.get_ndr_server_config()
            db_conn = ndr_webui.config.get_db_connection()
            admin_user = tests.common.create_admin_user(self)

            non_priv_user = tests.common.create_unprivilleged_user(self, admin_user)

            org = tests.common.create_organization(self, "test org")

            self.assertRaises(
                psycopg2.InternalError,
                ndr_webui.OrganizationACL.read_by_id,
                nsc,
                non_priv_user,
                org.pg_id,
                db_conn
            )

    def test_read_by_name_acl_failure(self):
        '''Tests that we blow up on an ACL read by name failure'''
        with self.flask_app.app_context():
            nsc = ndr_webui.config.get_ndr_server_config()
            db_conn = ndr_webui.config.get_db_connection()
            admin_user = tests.common.create_admin_user(self)

            non_priv_user = tests.common.create_unprivilleged_user(self, admin_user)

            org = tests.common.create_organization(self, "test org")

            self.assertRaises(
                psycopg2.InternalError,
                ndr_webui.OrganizationACL.read_by_name,
                nsc,
                non_priv_user,
                "test org",
                db_conn
            )
