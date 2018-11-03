#!/usr/bin/env bash
# this script runs the python unit tests.

./build.sh || exit 1

# smart prepend to PYTHONPATH even if variable is unset
export PYTHONPATH="_build/lib${PYTHONPATH:+:$PYTHONPATH}"

pytest tests "$@"
