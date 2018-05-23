#! /bin/bash
: << 'COMMENT'
unittest start script
notice:
!!! unit test script will flush database.
!!! do not run under your in used database.
COMMENT

set -e

export DEBUG=True

python -m unittest discover -s . -p "*unittest.py" -v