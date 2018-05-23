#! /bin/bash
: << 'COMMENT'
unittest start script
COMMENT

set -e

export DEBUG=True

python -m unittest discover -s . -p "*unittest.py" -v