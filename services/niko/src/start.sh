#!/bin/bash

/usr/sbin/sshd -D &
uvicorn server:app --host 0.0.0.0 --port 8000