#   Copyright 2018 Eric Chang
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

"""Generate python stub files for pybind11 modules."""

import argparse
import importlib
import inspect
import os
import pkgutil
import sys
from typing import Iterator, List

from .stubgenc import generate_stub_for_c_module, is_c_module

out_dir_default = "out"


def parse_options() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Python stub files for pybind11 modules.")
    parser.add_argument(
        "--recursive",
        dest="recursive",
        action="store_true",
        default=False,
        help="generate stub files for submodules as well.",
    )
    parser.add_argument(
        "--ignore-errors",
        dest="ignore_errors",
        action="store_true",
        default=False,
        help="ignore errors during stub generation.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_dir",
        type=str,
        default=out_dir_default,
        help=f'The output folder (defaults to "{out_dir_default}").',
    )
    parser.add_argument(
        "modules", nargs="*", type=str, help="pybind11 modules to generate stubs for."
    )

    args = parser.parse_args()
    # Create the output folder if it doesn't already exist.
    os.makedirs(args.output_dir, exist_ok=True)
    return args


def walk_packages(packages: List[str]) -> Iterator[str]:
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


def main() -> None:
    # Make sure that the current directory is in sys.path so that
    # stubgen can be run on packages in the current directory.
    if "" not in sys.path:
        sys.path.insert(0, "")

    options = parse_options()
    if not os.path.isdir(options.output_dir):
        raise SystemExit('Directory "{options.output_dir}" does not exist')
    for module in options.modules if not options.recursive else walk_packages(options.modules):
        try:
            target = os.path.join(options.output_dir, module.replace(".", "/") + ".pyi")
            generate_stub_for_c_module(module_name=module, target=target, add_header=True)
            print("Created " + target)
        except Exception as e:
            if not options.ignore_errors:
                raise e
            else:
                print("Stub generation failed for: ", module, file=sys.stderr)


if __name__ == "__main__":
    main()
