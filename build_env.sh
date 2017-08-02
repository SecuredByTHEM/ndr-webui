#!/bin/sh
virtualenv flask
flask/bin/pip3 install git+https://github.com/SecuredByTHEM/ndr-netcfg.git
flask/bin/pip3 install git+https://github.com/SecuredByTHEM/ndr.git
flask/bin/pip3 install git+https://github.com/SecuredByTHEM/ndr-server.git
flask/bin/python ./setup.py install
