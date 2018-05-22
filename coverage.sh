#!/usr/bin/env bash
set -e

if [ -e ./.coverage ]
then
    rm ./.coverage
fi

coverage run -m unittest discover -s . -p "*unittest.py" -v

coverage report -m