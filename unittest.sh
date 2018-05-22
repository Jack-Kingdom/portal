#! /bin/bash
: << 'COMMENT'
unittest start script
COMMENT

set -e

python -m unittest discover -s . -p "*unittest.py" -v