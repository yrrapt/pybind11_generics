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

"""Generate python stub files for pybind11 modules."""

import importlib
import inspect
import pkgutil
import sys
from pathlib import Path
from typing import Iterator, Sequence

import click

from .stubgenc import generate_stub_for_c_module, is_c_module


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("output_dir")
@click.argument("modules", nargs=-1)
@click.option("-r", "--recursive", is_flag=True, help="Generate stubs for submodules as well.")
@click.option("--ignore-errors", is_flag=True, help="Ignore errors during stub generation.")
def gen_pybind11_stubs(
    output_dir: str, modules: Sequence[str], recursive: bool, ignore_errors: bool
) -> None:
    """Generate Python stubs for pybind11 modules MODULES and output them in OUTPUT_DIR."""
    output_path = Path(output_dir).resolve()
    if not output_path.is_dir():
        raise SystemExit(f"Cannot find directory: {output_dir}")

    # NOTE: add output path to PYTHONPATH so we can import the module.
    sys.path.insert(0, str(output_path))
    for module in walk_packages(modules) if recursive else modules:
        try:
            target = generate_stub_for_c_module(module, output_path)
            print(f"Created stub: {target}")
        except Exception as e:
            if not ignore_errors:
                raise e
            else:
                print("Stub generation failed for: ", module, file=sys.stderr)


def walk_packages(packages: Sequence[str]) -> Iterator[str]:
    """Iterates through all packages and sub-packages in the given list.

    Python packages have a __path__ attribute defined, which pkgutil uses to determine
    the package hierarchy.  However, packages in C extensions do not have this attribute,
    so we have to roll out our own.
    """
    for package_name in packages:
        package = importlib.import_module(package_name)
        yield package.__name__
        # get the path of the object (needed by pkgutil)
        path = getattr(package, "__path__", None)
        if path is None:
            # object has no path; this means it's either a module inside a package
            # (and thus no sub-packages), or it could be a C extension package.
            if is_c_module(package):
                # This is a C extension module, now get the list of all sub-packages
                # using the inspect module
                subpackages = [
                    package.__name__ + "." + name
                    for name, val in inspect.getmembers(package)
                    if inspect.ismodule(val)
                ]
                # recursively iterate through the subpackages
                for submodule in walk_packages(subpackages):
                    yield submodule
            # It's a module inside a package.  There's nothing else to walk/yield.
        else:
            all_packages = pkgutil.walk_packages(
                path, prefix=package.__name__ + ".", onerror=lambda r: None
            )
            for _, qualified_name, _ in all_packages:
                yield qualified_name


if __name__ == "__main__":
    gen_pybind11_stubs()
