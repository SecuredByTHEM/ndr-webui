# Handle imports across the application
from flask import Flask
from flask_login import LoginManager

from ndr_webui.views import misc
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
