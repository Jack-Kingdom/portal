#! /bin/bash
set -e

python -m unittest discover -s meta -p "*unittest.py" -v