#   Copyright 2020 Eric Chang
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


"""This package provides classes for building pybind11 extensions.
"""

from typing import Sequence, Dict, Any

import os
import re
import sys
import platform
import subprocess as sp
from pathlib import Path

from packaging import version
from setuptools import Extension
from setuptools.command.build_ext import build_ext


class CMakePyBind11Extension(Extension):
    def __init__(self, name: str, sourcedir: str = ".") -> None:
        super().__init__(name, sources=[])
        self.sourcedir = str(Path(sourcedir).resolve())


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
        try:
            out = sp.check_output(["cmake", "--version"])
        except OSError:
            err = RuntimeError(
                "CMake must be installed to build the following extensions: "
                f"{', '.join(e.name for e in self.extensions)}"
            )
            self._log(str(err), error=True)
            raise err

        if platform.system() == "Windows":
            cmake_version = re.search(r"version\s*([\d.]+)", out.decode()).group(1)
            if version.parse(cmake_version) < version.parse("3.1.0"):
                err = RuntimeError("CMake >= 3.1.0 is required on Windows")
                self._log(str(err), error=True)
                raise err

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext: CMakePyBind11Extension) -> None:
        # setup CMake initialization and build commands
        version = self.distribution.get_version()
        ext_dir = Path(self.get_ext_fullpath(ext.name)).parent.resolve()
        init_cmd = [
            "cmake",
            f"-S{ext.sourcedir}",
            f"-B{self.build_temp}",
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={ext_dir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
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
        self._log(f"[{ext.name}] Building {ext.name} version: {version}")
        self._log(f"[{ext.name}] CMake init command: {' '.join(init_cmd)}")
        self._log(f"[{ext.name}] CMake build command: {' '.join(build_cmd)}")

        if self.build_log:
            with open(self.build_log, "a") as f:
                sp.check_call(init_cmd, stdout=f, stderr=sp.STDOUT)
                sp.check_call(build_cmd, stdout=f, stderr=sp.STDOUT)
        else:
            sp.check_call(init_cmd, stdout=None, stderr=None)
            sp.check_call(build_cmd, stdout=None, stderr=None)

        # generate stubs
        # subprocess.check_call(["./gen_stubs.sh"])

        # Add an empty line for cleaner output

    def _log(self, msg: str, error: bool = False) -> None:
        if self.build_log:
            with open(self.build_log, "a") as f:
                if error:
                    f.write("[ERROR] ")
                f.write(msg)
                f.write("\n")


def update_setup_kwargs(
    setup_kwargs: Dict[str, Any], pkg_name: str, ext_list: Sequence[str]
) -> None:
    extensions = [CMakePyBind11Extension(f"{pkg_name}.{ext_name}") for ext_name in ext_list]

    setup_kwargs.update(
        ext_modules=extensions,
        cmdclass={"build_ext": CMakePyBind11Build},
        zip_safe=False,
    )
