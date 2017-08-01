import ndr_webui

from flask import render_template
from ndr_webui import app


@app.route('/')
@app.route('/index')
def index():
    ndr_webui.config.get_ndr_server_config()
    return render_template('index.html',
                           title='Home')

# Login
@app.route('/login')
def login():
    return render_template('login.html',
                           title='Login')

# Site Overview

@app.route('/site/<site_id>')
def site_overview(site_id):
    return render_template('index.html',
                           title='Site Overview',
                           site_id=site_id,
                           active_page='overview')

# Site Syslog Info
@app.route('/site/<site_id>/logs')
def site_syslog(site_id):
    return render_template('syslog.html',
                           title='Site Logs',
                           site_id=site_id,
                           active_page='logs')


@app.route('/site/<site_id>/nmap')
def site_nmap(site_id):
    return render_template('nmap.html',
                           title='Site NMAP Information',
                           site_id=site_id,
                           active_page='nmap')
