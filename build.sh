#!/usr/bin/env bash
# this script builds the C++ extension

python setup.py build --parallel 8 --build-temp "_build/temp" --build-lib "_build/lib"
