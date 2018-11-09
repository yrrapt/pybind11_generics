# -*- coding: utf-8 -*-

"""This module handles parsing type hinting information from pybind11 docstrings."""

from typing import Dict, Optional

import ast

# list of classes we need to import from typing package if present
typing_imports = ('Any', 'Union', 'Tuple', 'Optional', 'List', 'Dict', 'Iterable', 'Iterator')


class PkgClsParser(ast.NodeVisitor):
    """This parser processes an ast.Attribute node to get the package name and class name.
    """
    def __init__(self) -> None:
        ast.NodeVisitor.__init__(self)

        self._modules = []
        self.class_name = ''
        self.package_name = ''

    # noinspection PyPep8Naming
    def visit_Attribute(self, node: ast.Attribute) -> None:
        if not self.class_name:
            self.class_name = node.attr
        else:
            self._modules.append(node.attr)
        self.generic_visit(node)

    # noinspection PyPep8Naming
    def visit_Name(self, node: ast.Name) -> None:
        self._modules.append(node.id)
        self.package_name = '.'.join(reversed(self._modules))


class ImportsParser(ast.NodeVisitor):
    """This parser process a method/property signature and gets all classes to import.
    """

    def __init__(self, imports: Dict[str, str]) -> None:
        ast.NodeVisitor.__init__(self)

        self._imports = imports

    # noinspection PyPep8Naming
    def visit_Name(self, node: ast.Name) -> None:
        if node.id in typing_imports:
            self._imports[node.id] = 'typing'

    # noinspection PyPep8Naming
    def visit_Attribute(self, node: ast.Attribute) -> None:
        pkg_cls_parser = PkgClsParser()
        pkg_cls_parser.visit(node)
        self._imports[pkg_cls_parser.class_name] = pkg_cls_parser.package_name


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
    type_str = docstr.split('\n', 1)[0].rsplit(':', 1)[0].strip()

    try:
        type_body = ast.parse(type_str).body
        if type_body:
            # parse successful and found content, record all imports
            ImportsParser(imports).visit(type_body[0])
            return type_str
    except SyntaxError:
        # parsing failed; fallback to default return value
        pass

    imports['Any'] = 'typing'
    return 'Any'


def get_function_stub(name: str,
                      docstr: str,
                      self_var: Optional[str],
                      cls_name: Optional[str],
                      imports: Dict[str, str],
                      ) -> str:
    declaration = 'def {}: ...'.format(docstr.split('\n', 1)[0].strip())

    try:
        func_node = ast.parse(declaration).body[0]
    except SyntaxError:
        pass

    # failed to get function stub, try to check for builtin method signature
    if self_var is not None and name.startswith('__') and name.endswith('__'):
        # check if this is a builtin method for a class
        test = check_builtin_sig(name[2:-2], cls_name, self_var)
        if test:
            return test

    imports['Any'] = 'typing'
    self_arg = self_var + ', ' if self_var else ''
    return 'def {}({}*args: Any, **kwargs: Any) -> Any: ...'.format(name, self_arg)


def check_builtin_sig(name: str,
                      cls_name: str,
                      self_var: str,
                      ) -> str:
    if name in ('int', 'float', 'complex', 'bool'):
        return 'def __{}__({}) -> {}: ...'.format(name, self_var, name)
    if name in ('hash', 'sizeof', 'trunc', 'floor', 'ceil'):
        return 'def __{}__({}) -> {}: ...'.format(name, self_var, 'int')
    if name in ('copy', 'deepcopy'):
        return 'def __{}__({}) -> {}: ...'.format(name, self_var, cls_name)
    if name == 'delattr':
        return 'def __{}__({}) -> {}: ...'.format(name, self_var, 'None')
    return ''
