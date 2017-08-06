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

'''Sends a message to the recorder to tell it to reboot at the next checkin to process
updates and reset state information'''

import argparse
import logging
import bcrypt

import ndr_server

def main():
    # Do our basic setup work
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(name=__name__)
    logger.setLevel(logging.DEBUG)

    # Load the NSC config
    nsc = ndr_server.Config(logger, "/etc/ndr/ndr_server.yml")

    parser = argparse.ArgumentParser(
        description="Creates an administrator user")
    parser.add_argument('-c', '--config',
                        help='NDR Server Config',
                        default='/etc/ndr/ndr_server.yml')
    parser.add_argument('-u', '--user',
                        help='username',
                        required=True)

    parser.add_argument('-e', '--email',
                        help='username',
                        required=True)

    parser.add_argument('-p', '--password',
                        help='password',
                        required=True)

    parser.add_argument('-r', '--realname',
                        help='real name',
                        required=True)

    args = parser.parse_args()


    # Load the NSC config
    nsc = ndr_server.Config(logger, "/etc/ndr/ndr_server.yml")
    db_connection = nsc.database.get_connection()

    # At some point we should have a proper method for this
    crypted_pw = str(bcrypt.hashpw(bytes(args.password, 'utf-8'), bcrypt.gensalt()), 'utf-8')
    pg_id = nsc.database.run_procedure_fetchone(
        "admin.create_user",
        [args.user, args.email, crypted_pw, args.realname],
        existing_db_conn=db_connection
    )[0]

    nsc.database.run_procedure_fetchone(
        "admin.activate_user", [pg_id],
        existing_db_conn=db_connection
    )

    nsc.database.run_procedure_fetchone(
        "admin.make_user_superadmin", [pg_id],
        existing_db_conn=db_connection
    )

    db_connection.commit()

    logger.info("Created user with ID %d", pg_id)

if __name__ == '__main__':
    main()
