#!/bin/bash

# Load environment variables from .env file
set -a
. /opt/.env
set +a

exec python /opt/init.py

exec python -u /opt/app.py 