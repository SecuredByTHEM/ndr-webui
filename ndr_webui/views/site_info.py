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

    return render_template('site_overview.html',
                           title='Site Overview',
                           site_id=site_id,
                           active_page='overview')
