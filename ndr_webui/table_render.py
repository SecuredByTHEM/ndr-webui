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

'''Renders HTML tables with information'''

import html

import flask

def a_link(url, text):
    '''Generates an a href'''
    return "<a href=\"" + url + "\">" + html.escape(text) + "</a>"

class TableRender(object):
    '''Renders an HTML table based on data

    Columns are a tuple of a human readable name, the tag in the dict, and a boolean
    if the information has to be escaped'''

    def __init__(self, columns, data_dicts):
        self.columns = columns
        self.data_dict = data_dicts

        # Allow HTML elements to be overridden
        self.div_class = "table-responsive"
        self.table_class = "table table-striped"

    def render(self):
        '''Generates HTML for the table'''

        html_data = ""

        # Output the opening class
        html_data += "<div class=\"" + self.div_class + "\">\n"

        # Start the table
        html_data += "<table class=\"" + self.table_class + "\">\n"

        # Write table headers
        html_data += "<thead>\n"

        for column in self.columns:
            html_data += "<th><tr>" + html.escape(column[0]) + "</th></tr>\n"
        html_data += "</thead>\n"

        # Now handle the body
        html_data += "<tdata>\n"

        for data_dict in self.data_dict:
            html_data += "<tr>"

            for column in self.columns:
                row_data = data_dict.get(column[1], "")

                if column[2] is True:
                    row_data = html.escape(row_data)

                html_data += "<td>" + row_data + "</td>"
            html_data += "</tr>\n"
        html_data += "</tdata>\n"

        # Close out tags out
        html_data += "</table>\n"
        html_data += "</div>\n"

        return html_data

# Helper classes for rendering the most common elements
class OrganizationsTable(TableRender):
    '''Renders organization tables'''

    def __init__(self, organizations):
        self.organizations = organizations

        # Build the columns for the organization
        columns = []

        columns.append(('Organization', 'org_link', False))
        table_data = []

        for organization in organizations:
            org_dict = {}
            org_dict['org_link'] = a_link(organization.name,
                                          flask.url_for('organizations.overview',
                                                        org_id=organization.pg_id))

            table_data.append(org_dict)

        TableRender.__init__(self, columns, table_data)
