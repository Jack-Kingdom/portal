#! /bin/bash
set -e

python -m unittest discover -s . -p "*unittest.py" -v