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

'''Test helper code'''

ROOT_USERNAME = "admin"
ROOT_PW = "rootpassword"
ROOT_EMAIL = "test_user@themtests.com"
ROOT_REAL_NAME = "Admin Test User"

NO_ACL_USER = "noacl"
NO_ACL_PASSWORD = "noaclpassword"
NO_ACL_EMAIL = "noacl@noacl.com"
NO_ACL_REAL_NAME = "No ACL magic here"

import bcrypt
import ndr_server
import ndr_webui

def create_admin_user(self):
    nsc = ndr_webui.config.get_ndr_server_config()
    db_connection = ndr_webui.config.get_db_connection()

    crypted_pw = str(bcrypt.hashpw(bytes(ROOT_PW, 'utf-8'), bcrypt.gensalt()), 'utf-8')

    # We need to create the root user account which can manipulate the other ones
    root_userid = nsc.database.run_procedure_fetchone(
        "admin.create_user", [ROOT_USERNAME, ROOT_EMAIL, crypted_pw, ROOT_REAL_NAME],
        existing_db_conn=db_connection
    )[0]

    # Activate the user, then make it a super-admin
    nsc.database.run_procedure(
        "admin.activate_user", [root_userid], existing_db_conn=db_connection
    )

    nsc.database.run_procedure(
        "admin.make_user_superadmin", [root_userid], existing_db_conn=db_connection
    )

    return ndr_webui.User.read_by_id(nsc, root_userid, db_connection)

def create_unprivilleged_user(self, admin_user):
    '''Creates an unprivlleged user for ACL tests'''

    nsc = ndr_webui.config.get_ndr_server_config()
    db_conn = ndr_webui.config.get_db_connection()

    # Get the admin user obj
    new_user = ndr_webui.User.create(
        nsc, admin_user, NO_ACL_USER, NO_ACL_EMAIL, NO_ACL_PASSWORD, NO_ACL_REAL_NAME,
        db_conn
    )

    return new_user

def create_organization(self, org_name):
    '''Creates an organization for testing purposes'''
    nsc = ndr_webui.config.get_ndr_server_config()
    db_conn = ndr_webui.config.get_db_connection()

    # First we need to create a test organization
    org = ndr_server.Organization.create(
        nsc,
        org_name,
        db_conn=db_conn
    )

    return org

def create_site(self, org, site_name):
    '''Creates a site for testing purposes'''
    nsc = ndr_webui.config.get_ndr_server_config()
    db_conn = ndr_webui.config.get_db_connection()

    # First we need to create a test organization
    site = ndr_server.Site.create(
        nsc,
        org,
        site_name,
        db_conn
    )

    return site

def create_recorder(self, site, human_name, hostname):
    '''Creates a test recorder'''
    nsc = ndr_webui.config.get_ndr_server_config()
    db_conn = ndr_webui.config.get_db_connection()

    recorder = ndr_server.Recorder.create(
        nsc, site, human_name, hostname, db_conn)

    return recorder

def login(self, email, password):
    return self.app.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def logout(self):
    return self.app.get('/logout', follow_redirects=True)
