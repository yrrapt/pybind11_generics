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

"""This package provides classes for building pybind11 extensions.
"""

import os
import platform
import re
import subprocess as sp
import sys
from pathlib import Path
from typing import Any

from packaging import version
from setuptools import Extension
from setuptools.command.build_ext import build_ext


class CMakePyBind11Extension(Extension):
    def __init__(self, name: str, *, sourcedir: str = ".", gen_stubs: bool = True) -> None:
        super().__init__(name, sources=[])
        self.sourcedir = str(Path(sourcedir).resolve())
        self.gen_stubs = gen_stubs


class CMakePyBind11Build(build_ext):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # get build parameters from environment variables
        self.build_type: str = os.environ.get("PYBIND11EXT_BUILD_TYPE", "Debug")
        self.build_log: str = os.environ.get("PYBIND11EXT_BUILD_LOG", "")

    def initialize_options(self) -> None:
        super().initialize_options()

        # override how self.parallel is set.  Use environment variables instead.
        self.parallel: int = int(os.environ.get("PYBIND11EXT_BUILD_PARALLEL", 1))
        if self.parallel < 0:
            raise ValueError("PYBIND11_BUILD_PARALLEL must be nonnegative.")
        if self.parallel == 0:
            test_val = os.cpu_count()
            self.parallel = 1 if test_val is None else max(test_val // 2, 1)

    def run(self) -> None:
        version_check_cmd = ["cmake", "--version"]
        try:
            out = sp.check_output(version_check_cmd)
        except OSError:
            err = RuntimeError(
                "CMake must be installed to build the following extensions: "
                f"{', '.join(e.name for e in self.extensions)}"
            )
            self._log(str(err), error=True)
            raise err

        if platform.system() == "Windows":
            version_match = re.search(r"version\s*([\d.]+)", out.decode())
            if version_match is None:
                err = RuntimeError(
                    "Failed to get cmake version from command: " f"{' '.join(version_check_cmd)}"
                )
                self._log(str(err), error=True)
                raise err

            cmake_version = version_match.group(1)
            if version.parse(cmake_version) < version.parse("3.1.0"):
                err = RuntimeError("CMake >= 3.1.0 is required on Windows")
                self._log(str(err), error=True)
                raise err

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext: CMakePyBind11Extension) -> None:
        # setup CMake initialization and build commands
        ext_fullname = self.get_ext_fullname(ext.name)
        num_levels = len(ext_fullname.split("."))
        ext_fullpath = Path(self.get_ext_fullpath(ext.name)).resolve()
        pkg_root_dir = ext_fullpath.parents[num_levels - 1]
        ext_dir = ext_fullpath.parent
        init_cmd = [
            "cmake",
            f"-S{ext.sourcedir}",
            f"-B{self.build_temp}",
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={ext_dir}",
            f"-DCMAKE_BUILD_TYPE={self.build_type}",
        ]
        build_cmd = [
            "cmake",
            "--build",
            self.build_temp,
            "--",
        ]

        # handle Windows CMake arguments
        if platform.system() == "Windows":
            if sys.maxsize > 2 ** 32:
                init_cmd.append("-A")
                init_cmd.append("x64")
            build_cmd.append("/m")

        # set up parallel build arguments
        build_cmd.append(f"-j{self.parallel}")

        # run CMake
        Path(self.build_temp).mkdir(parents=True, exist_ok=True)
        cmd_sep = "  \\\n  "
        self._log(f"[{ext_fullname}] CMake init command:\n{cmd_sep.join(init_cmd)}")
        self._log(f"[{ext_fullname}] CMake build command:\n{' '.join(build_cmd)}")

        if self.build_log:
            with open(self.build_log, "a") as f:
                sp.check_call(init_cmd, stdout=f, stderr=sp.STDOUT)
                sp.check_call(build_cmd, stdout=f, stderr=sp.STDOUT)
        else:
            sp.check_call(init_cmd, stdout=None, stderr=sp.STDOUT)
            sp.check_call(build_cmd, stdout=None, stderr=sp.STDOUT)

        if ext.gen_stubs:
            # generate python stub file
            # NOTE: use python sub-process so we reload that pakage.
            sp.check_call(
                [sys.executable, "-m", "pybind11_generics.stubgen", str(pkg_root_dir), ext_fullname]
            )

    def _log(self, msg: str, error: bool = False) -> None:
        if error:
            msg = "[ERROR] " + msg

        print(msg)
        if self.build_log:
            with open(self.build_log, "a") as f:
                f.write(msg)
                f.write("\n")
