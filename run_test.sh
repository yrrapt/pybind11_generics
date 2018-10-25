#!/usr/bin/env bash
# this script runs the python unit tests.

./build.sh

# smart prepend to PYTHONPATH even if variable is unset
export PYTHONPATH="_build/lib${PYTHONPATH:+:$PYTHONPATH}"

pytest tests
