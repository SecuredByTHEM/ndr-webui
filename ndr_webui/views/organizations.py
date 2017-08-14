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

from flask import current_app

organizations_page = flask.Blueprint('organizations', __name__,
                                     template_folder='templates')


@organizations_page.route('/')
@organizations_page.route('/organizations')
@login_required
def index():
    '''Displays the master list of organizations'''
    vcv = ndr_webui.config.get_common_variables()

    org_list = vcv.user.get_organizations_for_user(db_conn=vcv.db_conn)
    page_title = ndr_webui.config.site_name() + " - Organizations"

    return render_template('organizations.html',
                           title=page_title,
                           vcv=vcv,
                           organizations=org_list)


@organizations_page.route('/organization/<org_id>')
@login_required
def overview(org_id):
    '''Displays more in-depth information for an organization'''
    # Make sure our input parameters are sane
    org_id = int(org_id)

    vcv = ndr_webui.config.get_common_variables()

    # Grab the organization via the ACL
    org = ndr_webui.OrganizationACL.read_by_id(
        vcv.nsc, vcv.user, org_id, vcv.db_conn)

    # Now grab the list of sites, and then amend the title
    sites = vcv.user.get_sites_in_organization_for_user(org, vcv.db_conn)
    page_title = ndr_webui.config.site_name() + " - Sites - " + org.name

    return render_template('sites.html',
                           title=page_title,
                           vcv=vcv,
                           org=org,
                           sites=sites)
