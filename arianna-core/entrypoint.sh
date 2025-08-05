#!/bin/sh
set -e
# Start health monitoring in the background
python3 /arianna_core/cmd/arianna.py health &
exec "$@"
