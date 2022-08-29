# SPDX-License-Identifier: Apache-2.0
# Copyright 2021 Blue Cheetah Analog Design Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Python utilties for building C extensions created with pybind11_generics.

pybind11_generics is a C++ library that's forked from pybind11.  This fork
makes some minor modifications in Python bindings docstring generation and also
added various C++ classes, so that it is possible to generate typehint stubs for
C extensions libraries that has fully support of generic classes (such as List[int],
Dict[str, str], and so on).

This Python library provides various utilties that make packaging pybind11_generics C
extensions easier, such as a script that generates the stub file, and also classes to
help package C extensions using setuptools.
"""

try:
    from ._version import version  # type: ignore[import]

    __version__: str = version
except ImportError:
    pass
