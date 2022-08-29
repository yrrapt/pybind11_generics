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

"""This module handles parsing type hinting information from pybind11 docstrings."""

import ast
from itertools import chain, islice
from typing import Dict, List, Optional

# list of classes we need to import from typing package if present
typing_imports = (
    "Any",
    "Union",
    "Tuple",
    "Optional",
    "List",
    "Dict",
    "Iterable",
    "Iterator",
    "Sequence",
)


class PkgClsParser(ast.NodeVisitor):
    """This parser processes an ast.Attribute node to get the package name and class name."""

    def __init__(self) -> None:
        ast.NodeVisitor.__init__(self)

        self._modules: List[str] = []
        self.class_name = ""
        self.package_name = ""

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if self.class_name:
            self._modules.append(node.attr)
        else:
            self.class_name = node.attr
        self.visit(node.value)

    def visit_Name(self, node: ast.Name) -> None:
        self._modules.append(node.id)
        self.package_name = ".".join(reversed(self._modules))


class ImportsParser(ast.NodeVisitor):
    """This parser process a method/property signature and gets all classes to import."""

    def __init__(self, imports: Dict[str, str]) -> None:
        ast.NodeVisitor.__init__(self)

        self._imports = imports
        self.replacements: Dict[str, str] = {}

    def visit_Str(self, node: ast.Str) -> None:
        """This method is here because type annotation could be string"""
        try:
            # try to parse the type annotation string with ast
            body = ast.parse(node.s).body
            if body:
                self.visit(body[0])
        except SyntaxError:
            pass

    def visit_Name(self, node: ast.Name) -> None:
        if node.id in typing_imports:
            self._imports[node.id] = "typing"
        elif node.id == "array":
            # Numpy array support
            self._imports["ndarray"] = "numpy"

    def visit_Attribute(self, node: ast.Attribute) -> None:
        pkg_cls_parser = PkgClsParser()
        pkg_cls_parser.visit(node)
        pkg_name = pkg_cls_parser.package_name
        cls_name = pkg_cls_parser.class_name
        self._imports[cls_name] = pkg_name
        self.replacements[pkg_name + "." + cls_name] = cls_name

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # only visit arguments and return type annotation since we just want
        # to get the names/attributes in type annotations
        if node.args is not None:
            self.generic_visit(node.args)
        if node.returns is not None:
            self.visit(node.returns)

    def visit_arguments(self, node: ast.arguments) -> None:
        # only visit arguments and not default values
        for arg in chain(node.posonlyargs, node.args, node.kwonlyargs):
            self.generic_visit(arg)
        if node.vararg is not None:
            self.visit(node.vararg)
        if node.kwarg is not None:
            self.visit(node.kwarg)

    def visit_arg(self, node: ast.arg) -> None:
        # only visit type annotation
        if node.annotation is not None:
            self.visit(node.annotation)


def process_ast_node(orig_str: str, node: ast.AST, imports: Dict[str, str]) -> str:
    # record all imports
    imp_parser = ImportsParser(imports)
    imp_parser.visit(node)

    # remove package name from full path class name
    for from_str, to_str in imp_parser.replacements.items():
        orig_str = orig_str.replace(from_str, to_str)
    return orig_str


def get_prop_type(docstr: str, imports: Dict[str, str]) -> str:
    """Get property type information from docstring.

    Assumes the docstring is following Google/Numpy style, that is, the first line of the docstring
    follows the format:

    <type>: <brief description>

    Returns 'Any' type if the docstring fails to parse.

    Parameters
    ----------
    docstr : str
        the docstring.
    imports : Dict[str, str]
        dictionary of all classes that need to be imported to understand the typehint.

    Returns
    -------
    prop_type : str
        a string representation of the property type.  'Any' if an error occurred.

    """
    # extract the type string from docstring
    # get just the first line, then get the expression to the left of the colon, then
    # remove white spaces
    type_str = docstr.split("\n", 1)[0].rsplit(":", 1)[0].strip()

    try:
        type_body = ast.parse(type_str).body
        if type_body:
            # parse successful and found content, record all imports
            return process_ast_node(type_str, type_body[0], imports)
    except SyntaxError:
        # parsing failed; fallback to default return value
        pass

    imports["Any"] = "typing"
    return "Any"


def write_function_stubs(
    name: str,
    docstr: str,
    self_var: Optional[str],
    cls_name: Optional[str],
    output: List[str],
    imports: Dict[str, str],
) -> None:
    docstr_lines = docstr.split("\n")
    first_line = docstr_lines[0].strip()
    overloaded = False
    if first_line == name + "(*args, **kwargs)" and len(docstr_lines) > 1:
        # we potentially have overloaded functions; check
        second_line = docstr_lines[1].strip()
        if second_line == "Overloaded function.":
            # we do have overloaded functions
            overloaded = True

    if overloaded:
        imports["overload"] = "typing"
        cnt = 1
        for line in islice(docstr_lines, 2, None):
            line = line.strip()
            prefix = str(cnt) + ". "
            if line.startswith(f"{prefix}{name}("):
                # this is a overload function definition line
                output.append("@overload")
                output.append(
                    process_function_def(
                        name, f"def {line[len(prefix):]}: ...", self_var, cls_name, imports
                    )
                )
                cnt += 1

    else:
        output.append(
            process_function_def(name, f"def {first_line}: ...", self_var, cls_name, imports)
        )


def process_function_def(
    name: str,
    declaration: str,
    self_var: Optional[str],
    cls_name: Optional[str],
    imports: Dict[str, str],
) -> str:
    try:
        func_node = ast.parse(declaration).body[0]
        # parse successful and found content, record all imports
        return process_ast_node(declaration, func_node, imports)
    except SyntaxError:
        pass

    # failed to get function stub, try to check for builtin method signature
    if self_var is not None and name.startswith("__") and name.endswith("__"):
        # check if this is a builtin method for a class
        test = check_builtin_sig(name[2:-2], cls_name, self_var)
        if test:
            return test

    imports["Any"] = "typing"
    self_arg = self_var + ", " if self_var else ""
    return f"def {name}({self_arg}*args: Any, **kwargs: Any) -> Any: ..."


def check_builtin_sig(
    name: str,
    cls_name: Optional[str],
    self_var: str,
) -> str:
    if name in ("int", "float", "complex", "bool"):
        return f"def __{name}__({self_var}) -> {name}: ..."
    if name in ("hash", "sizeof", "trunc", "floor", "ceil"):
        return f"def __{name}__({self_var}) -> int: ..."
    if name in ("copy", "deepcopy"):
        if not cls_name:
            raise ValueError("cls_name empty or unspecified.")
        return f"def __{name}__({self_var}) -> {cls_name}: ..."
    if name == "delattr":
        return f"def __{name}__({self_var}) -> None: ..."
    return ""
