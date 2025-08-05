#!/bin/sh
set -e
python3 /arianna_core/cmd/health_monitor.py &
exec "$@"
