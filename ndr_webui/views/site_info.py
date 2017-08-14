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

'''Main View for Site Overview Index'''

import ndr_webui

import flask
from flask import render_template
from flask_login import login_required

from flask import current_app

site_info = flask.Blueprint('site_info', __name__,
                            template_folder='templates')

# Site Overview
@site_info.route('/site/<site_id>')
@login_required
def overview(site_id):
    '''Renders an overview of the site'''

    # Make sure our input parameters are sane
    site_id = int(site_id)

    vcv = ndr_webui.config.get_common_variables()

    # Load in the site
    site = ndr_webui.SiteACL.read_by_id(
        vcv.nsc, vcv.user, site_id, vcv.db_conn
    )

    # We need to pull the rest of the information based off the in the database

    recorders = vcv.user.get_recorders_in_site_for_user(
        site, vcv.db_conn
    )

    page_title = ndr_webui.config.site_name() + " - Sites Overview For " + site.name

    return render_template('site_overview.html',
                           title=page_title,
                           site_id=site_id,
                           recorders=recorders,
                           active_page='overview')
