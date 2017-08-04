# Handle imports across the application
from flask import Flask
from flask_login import LoginManager

import ndr_server

# Initialize global variables and such
app = Flask(__name__)
login_manager = LoginManager()
app.config.from_object('config')

# NDR Server Configuration will be initialized as needed
NSC = None

login_manager.init_app(app)

from ndr_webui import views
from ndr_webui import users
from ndr_webui import config
from ndr_webui import utils
from ndr_webui.views import login
from ndr_webui.views import misc

from ndr_webui.users import User
