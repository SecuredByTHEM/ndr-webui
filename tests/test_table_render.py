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
import os

import tests.common
import ndr_webui

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CONFIG = THIS_DIR + "/test_config.yml"
TEST_FLASK_CONFIG = THIS_DIR + "/flask_test_config.cfg"

RENDER_EXPECTED = THIS_DIR + "/expected_outputs/table_render.html"
ORG_EXPECTED = THIS_DIR + "/expected_outputs/org_render.html"

class TestTableRender(unittest.TestCase):
    '''Tests the table rendering class'''

    @classmethod
    def setUpClass(cls):
        # Setup Flask basic configuration
        flask_app = ndr_webui.init_app(testing=True,
                                       config_file=TEST_FLASK_CONFIG)
        cls.flask_app = flask_app
        cls.app = flask_app.test_client()

    def test_render_table(self):
        '''Compares a rendered table to the output'''
        columns = []
        columns.append(('Col1', 'col1_data', False))
        columns.append(('Col2', 'col2_data', False))
        columns.append(('Col3', 'col3_data', False))

        row1 = {}
        row1['col1_data'] = "Random1"
        row1['col2_data'] = "Random2"
        row1['col3_data'] = "Random3"

        row2 = {}
        row2['col1_data'] = "Thingy1"
        row2['col2_data'] = "Thingy2"
        row2['col3_data'] = "Thingy3"

        table_data = []
        table_data.append(row1)
        table_data.append(row2)

        render = ndr_webui.TableRender(columns, table_data)

        with open(RENDER_EXPECTED, 'r') as f:
            expected = f.read()
            self.assertEqual(expected, render.render())

        #print()
        #print(render.render())
        #print()

    def test_organization_render(self):
        '''Tests rendering organizations'''
        with self.flask_app.test_request_context():
            orgs = []

            # We need to override the pg_ids to get consistent results
            org1 = tests.common.create_organization(self, "test org")
            org1.pg_id = 1 
            orgs.append(org1)

            org2 = tests.common.create_organization(self, "test org2")
            org2.pg_id = 2

            orgs.append(org2)

            org_render = ndr_webui.OrganizationsTable(orgs)
            #print()
            #print(org_render.render())
            #print()

            with open(ORG_EXPECTED, 'r') as f:
                expected = f.read()
                self.assertEqual(expected, org_render.render())

if __name__ == "__main__":
    unittest.main()
