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

'''Recorder objects with ACL controls'''

import ndr_server

class RecorderACL(ndr_server.Recorder):
    '''Handles ACL controls for an organization'''
    def __init__(self, config):
        self.user = None
        ndr_server.Recorder.__init__(self, config)

    @staticmethod
    def check_user_permissions_for_recorder(nsc, user_id, rec_id, db_conn):
        '''Checks that a user can access an organization; raises exception
        if not true'''
        nsc.database.run_procedure_fetchone("webui.recorder_acl",
                                            [user_id, rec_id],
                                            existing_db_conn=db_conn)
        return True

    @classmethod
    def read_by_id(cls, nsc, user, rec_id, db_conn):
        '''Loads an recorder by pgid from the database'''

        # Check ACL
        RecorderACL.check_user_permissions_for_recorder(
            nsc, user.pg_id, rec_id, db_conn
        )

        # Now load the recorder
        recorder = super(RecorderACL, cls).read_by_id(
            nsc, rec_id, db_conn
        )

        # User has to be loaded after the fact
        recorder.user = user

        return recorder

    @classmethod
    def read_by_hostname(cls, nsc, user, hostname, db_conn):
        '''Loads an recorder by hostname from the database subject to ACL checks'''

        recorder = super(RecorderACL, cls).read_by_hostname(
            nsc, hostname, db_conn
        )

        # Check ACL
        RecorderACL.check_user_permissions_for_recorder(
            nsc, user.pg_id, recorder.pg_id, db_conn
        )

        recorder.user = user

        return recorder
