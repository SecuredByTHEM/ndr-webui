#!flask/bin/python

import os
import ndr_webui

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG = THIS_DIR + '/config.cfg'

app = ndr_webui.init_app(CONFIG)
app.run(debug=True)
