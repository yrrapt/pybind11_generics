# -*- coding: utf-8 -*-

"""A package that generates python stub files for pybind11 modules.

This stub generation script parses the docstring of methods/properties in a pybind11
module in order to get type information.  I'm using my fork of the pybind11 library,
which has some custom changes to docstring generation to make the stub generation
easier.

The changes to pybind11 are:

1. Added type annotation to property docstrings using Google/Numpy docstring style.

2. Remove annotation on "self" variable in methods, and added "cls" variable in
   classmethod signatures.  As the result, the first line of the auto-generated
   docstring has PEP 484 compliant type annotations.

NOTE:
    As of now; there is one more minor performance optimization I did to the pybind11
    library: when calling py::cast on rvalue C++ object references, and the return
    value policy is set to be automatic, the move policy is used instead of the copy
    policy.
"""
