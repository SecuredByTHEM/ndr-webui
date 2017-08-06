import ndr_webui

import flask
from flask import render_template
from flask_login import login_required

misc_page = flask.Blueprint('misc_page', __name__,
                            template_folder='templates')

# Site Overview
@misc_page.route('/site/<site_id>')
@login_required
def site_overview(site_id):
    return render_template('index.html',
                           title='Site Overview',
                           site_id=site_id,
                           active_page='overview')

# Site Syslog Info
@misc_page.route('/site/<site_id>/logs')
@login_required
def site_syslog(site_id):
    return render_template('syslog.html',
                           title='Site Logs',
                           site_id=site_id,
                           active_page='logs')


@misc_page.route('/site/<site_id>/nmap')
@login_required
def site_nmap(site_id):
    return render_template('nmap.html',
                           title='Site NMAP Information',
                           site_id=site_id,
                           active_page='nmap')

# Recorder Information
@misc_page.route('/recorder/<recorder_id>')
@login_required
def recorder_overview(recorder_id):
    return render_template('recorder_details.html',
                           title='Recorder Overview',
                           recorder_id=recorder_id,
                           active_page='overview')

@misc_page.route('/snort_rules/<recorder_id>')
def snort_rule_overview(recorder_id):
    return render_template('snort_rules.html',
                           title='SNORT Rules Overview',
                           recorder_id=recorder_id,
                           active_page='overview')

@misc_page.route('/network_scan/<network_scan_id>')
def network_scan_overview(network_scan_id):
    return render_template('network_scan.html',
                           title='Network Scan',
                           network_scan_id=network_scan_id,
                           active_page='overview')
