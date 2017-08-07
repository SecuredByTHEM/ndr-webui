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

import bcrypt
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

    return root_userid

def login(self, email, password):
    return self.app.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def logout(self):
    return self.app.get('/logout', follow_redirects=True)
