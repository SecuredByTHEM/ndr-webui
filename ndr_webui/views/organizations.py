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

'''Main View for Organization Index'''

import ndr_webui

import flask
from flask import render_template
from flask_login import login_required

from flask_login import current_user
from flask import current_app

organizations_page = flask.Blueprint('organizations', __name__,
                                     template_folder='templates')
@organizations_page.route('/')
@organizations_page.route('/organizations')
@login_required
def index():
    '''Displays the master list of organizations'''
    nsc = ndr_webui.config.get_ndr_server_config()
    db_conn = ndr_webui.config.get_db_connection()

    # Retrieve our user
    user = ndr_webui.User.get_by_id(
        nsc,
        current_user.get_id(),
        db_conn=db_conn
    )

    page_title = ndr_webui.config.site_name() + " - Organizations"

    org_list = user.get_organizations_for_user()
    nsc.logger.info(org_list[0].name)
    return render_template('organizations.html',
                           title=page_title,
                           user=user,
                           organizations=org_list)

@organizations_page.route('/organization/<org_id>')
@login_required
def overview(org_id):
    '''Displays more in-depth information for an organization'''
    return "Here"
