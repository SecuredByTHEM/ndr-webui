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

'''Handling of site information for the webUI.

See organizations_acl for info on the ACL handling'''

import ndr_server

class SiteACL(ndr_server.Site):
    '''Representation of NDR site with access controls'''
    def __init__(self, config):
        self.user = None
        ndr_server.Site.__init__(self, config)

    @staticmethod
    def check_user_permissions_for_site(nsc, user_id, site_id, db_conn):
        '''Checks that a user can access an organization; raises exception
        if not true'''
        nsc.database.run_procedure_fetchone("webui.check_site_acl",
                                            [user_id, site_id],
                                            existing_db_conn=db_conn)
        return True

    @classmethod
    def read_by_id(cls, nsc, user, site_id, db_conn):
        '''Loads an organization from the database'''

        # Check ACL
        SiteACL.check_user_permissions_for_site(
            nsc, user.pg_id, site_id, db_conn
        )

        # Now load the organization
        org = super(SiteACL, cls).read_by_id(
            nsc, site_id, db_conn
        )

        # User has to be loaded after the fact
        org.user = user

        return org

    @classmethod
    def read_by_name(cls, nsc, user, site_name, db_conn):
        '''Loads an organization by name from the database subject to ACL checks'''

        # This is a little annoying. To check the organization's ACL, we need the org_id,
        # so we need to load the organization first, *then* try read the id

        # Now load the organization
        org = super(SiteACL, cls).read_by_name(
            nsc, site_name, db_conn
        )

        # Check ACL
        SiteACL.check_user_permissions_for_site(
            nsc, user.pg_id, org.pg_id, db_conn
        )
        org.user = user

        return org
