# Handle imports across the application
from flask import Flask
from flask_login import LoginManager

from ndr_webui.views import misc
from ndr_webui import login

import ndr_server

# Initialize global variables and such
app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(misc.misc_page)
app.register_blueprint(login.login_blueprint)

# NDR Server Configuration will be initialized as needed
NSC = None

from ndr_webui import views
from ndr_webui import users
from ndr_webui import config
from ndr_webui import utils

from ndr_webui.users import User
