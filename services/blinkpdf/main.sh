#!/bin/bash
/usr/sbin/sshd -D

# exec python -u /opt/init.py

sleep 2

exec python -u /opt/app.py 