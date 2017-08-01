from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()
app.config.from_object('config')

login_manager.init_app(app)

from ndr_webui import views
from ndr_webui import users
from ndr_webui import config
from ndr_webui import utils
