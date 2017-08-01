from flask import render_template
from ndr_webui import app

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html',
                           title='Home',
                           user=user)

# Site Overview
@app.route('/site/<site_id>')
def site_overview(site_id):
    return render_template('index.html',
                        title='Site Overview')

# Site Syslog Info
@app.route('/site/<site_id>/logs')
def site_syslog(site_id):
    return render_template('syslog.html',
                        title='Site Logs')

@app.route('/site/<site_id>/nmap')
def site_nmap(site_id):
    return render_template('nmap.html',
                        title='Site NMAP Information')