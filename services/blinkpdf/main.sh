#!/bin/bash
/usr/sbin/sshd -D

python3 -u /opt/init.py
python3 -u /opt/app.py 
