from flask import Flask

app = Flask(__name__)
from ndr_webui import views
from ndr_webui import config
