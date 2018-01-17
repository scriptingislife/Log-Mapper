#!/bin/bash

export FLASK_APP="application.py"
~/.local/bin/flask run 1>/home/ec2-user/environment/Log-Mapper/log/logmapper-web.log 2>&1
