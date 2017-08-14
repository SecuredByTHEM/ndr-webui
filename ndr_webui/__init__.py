# Handle imports across the application
from flask import Flask
from flask_login import LoginManager

from ndr_webui.views import misc
from ndr_webui.views import organizations
from ndr_webui.views import site_info

from ndr_webui import login
from ndr_webui import config

import ndr_server

# NDR Server Configuration will be initialized as needed
NSC = None

def init_app(config_file, testing=False):
    # Initialize global variables and such
    global NSC
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.register_blueprint(misc.misc_page)
    app.register_blueprint(login.login_blueprint)
    app.register_blueprint(organizations.organizations_page)
    app.register_blueprint(site_info.site_info)

    app.teardown_appcontext(config.db_teardown)

    if testing is True:
        app.testing = True

    # Initialize NSC
    NSC = ndr_server.Config(app.logger,
                            app.config['NDR_SERVER_CONFIG'])

    return app


from ndr_webui import views
from ndr_webui import users
from ndr_webui import utils

from ndr_webui.users import User
from ndr_webui.organizations_acl import OrganizationACL
from ndr_webui.sites_acl import SiteACL
from ndr_webui.recorders_acl import RecorderACL

from ndr_webui.table_render import TableRender
from ndr_webui.table_render import OrganizationsTable
