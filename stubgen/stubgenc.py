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

"""Stub generator for C modules.

The public interface is via the mypy.stubgen module.
"""

from typing import List, Tuple, Optional, Mapping, Any, Dict, IO
# noinspection PyUnresolvedReferences
from types import ModuleType

import os
import inspect
import importlib

from .parsedoc import get_prop_type, write_function_stubs

# list of base class names to ignore
skip_base_names = ('pybind11_object', 'object')
# list of attributes to not generate stubs for
skip_attrs = ('__getattribute__',
              '__str__',
              '__repr__',
              '__doc__',
              '__dict__',
              '__module__',
              '__new__',
              '__weakref__',
              )


def generate_stub_for_c_module(module_name: str,
                               target: str,
                               add_header: bool,
                               ) -> None:
    module = importlib.import_module(module_name)
    assert is_c_module(module), '%s is not a C module' % module_name
    os.makedirs(os.path.dirname(target), exist_ok=True)

    # parse all members of this module
    imports = {}  # type: Dict[str, str]
    types = []  # type: List[List[str]]
    variables = []  # type: List[str]
    functions = []  # type: List[str]
    for name, obj in sorted(module.__dict__.items(), key=lambda x: x[0]):
        if process_c_function(name, obj, functions, imports):
            pass
        elif process_c_type(name, obj, types, imports):
            pass
        else:
            process_c_var(name, obj, variables, imports)

    # write output to file
    with open(target, 'w') as file:
        if add_header:
            write_header(file, module_name)

        if imports:
            for c_name, m_name in sorted(imports.items(), key=lambda x: x[1]):
                if m_name != module_name:
                    # a class in a different module, write import statement
                    if c_name == 'ndarray':
                        # numpy array alias
                        file.write(f'from {m_name} import ndarray as array\n')
                    else:
                        file.write(f'from {m_name} import {c_name}\n')
            file.write('\n')
        if variables:
            for line in variables:
                file.write(line)
                file.write('\n')
            file.write('\n')
            file.write('\n')
        else:
            # if no variables section, add extra blank line so import/variable
            # section is 2 spaces from class/function section
            file.write('\n')

        for line in functions:
            file.write(line)
            file.write('\n')
            file.write('\n')
            file.write('\n')
        for cls_lines in types:
            for line in cls_lines:
                file.write(line)
                file.write('\n')
            file.write('\n')
            file.write('\n')


def process_c_var(name: str,
                  obj: object,
                  output: List[str],
                  imports: Dict[str, str],
                  check: bool = True,
                  ) -> bool:
    if name == '__hash__' and obj is None:
        # pybind11 will set __hash__ to None
        return False
    if check and ((name.startswith('__') and name.endswith('__')) or inspect.ismodule(obj)):
        return False

    type_obj = type(obj)
    imports[type_obj.__name__] = type_obj.__module__
    output.append(f'{name}: {type_obj.__name__} = ...')
    return True


def process_c_function(name: str,
                       obj: object,
                       output: List[str],
                       imports: Dict[str, str],
                       self_var: Optional[str] = None,
                       cls_name: Optional[str] = None,
                       check: bool = True,
                       ) -> bool:
    if check and not is_c_function(obj):
        return False

    write_function_stubs(name, getattr(obj, '__doc__', ''), self_var, cls_name, output, imports)
    return True


def process_c_type(cls_name: str,
                   obj: type,
                   output: List[List[str]],
                   imports: Dict[str, str],
                   ) -> bool:
    if (cls_name.startswith('__') and cls_name.endswith('__')) or not is_c_type(obj):
        return False

    # typeshed gives obj.__dict__ the not quite correct type Dict[str, Any]
    # (it could be a mappingproxy!), which makes mypyc mad, so obfuscate it.
    obj_dict = getattr(obj, '__dict__')  # type: Mapping[str, Any]

    # parse all members of this class
    methods = []  # type: List[str]
    variables = []  # type: List[str]
    properties = []  # type: List[str]
    for mem_name, mem_obj in sorted(obj_dict.items(), key=lambda x: method_name_sort_key(x[0])):
        if mem_name in skip_attrs:
            pass
        elif process_c_method(mem_name, mem_obj, methods, imports, cls_name):
            pass
        elif process_c_property(mem_name, mem_obj, properties, imports):
            pass
        else:
            process_c_var(mem_name, mem_obj, variables, imports, check=False)

    # determine the base class
    all_bases = obj.mro()
    # remove the class itself
    all_bases = all_bases[1:]
    # Remove base classes of other bases as redundant.
    bases = []  # type: List[type]
    for base in all_bases:
        if base.__name__ not in skip_base_names and not any(issubclass(b, base) for b in bases):
            bases.append(base)
    if bases:
        bases_str = f'({", ".join(base.__name__ for base in bases)})'
    else:
        bases_str = ''

    if not methods and not variables and not properties:
        output.append([f'class {cls_name}{bases_str}: ...'])
    else:
        cls_lines = [f'class {cls_name}{bases_str}:']
        cls_lines.extend((f'    {line}' for line in variables))
        cls_lines.extend((f'    {line}' for line in properties))
        cls_lines.extend((f'    {line}' for line in methods))
        output.append(cls_lines)

    return True


def process_c_method(name: str,
                     obj: object,
                     output: List[str],
                     imports: Dict[str, str],
                     cls_name: str,
                     ) -> bool:
    is_static = is_c_staticmethod(obj)
    if not is_c_method(obj) and not is_static:
        return False

    if is_static:
        output.append('@staticmethod')
        self_var = None
    else:
        self_var = 'self'

    return process_c_function(name, obj, output, imports, self_var=self_var,
                              cls_name=cls_name, check=False)


def process_c_property(name: str,
                       obj: object,
                       output: List[str],
                       imports: Dict[str, str],
                       ) -> bool:
    if not is_c_property(obj):
        return False

    readonly = is_c_property_readonly(obj)

    prop_type = get_prop_type(getattr(obj, '__doc__', ''), imports)

    output.append('@property')
    output.append(f'def {name}(self) -> {prop_type}: ...')
    if not readonly:
        output.append(f'@{name}.setter')
        output.append(f'def {name}(self, val: {prop_type}) -> None: ...')

    return True


def is_c_function(obj: object) -> bool:
    return is_c_staticmethod(obj) or type(obj) is type(ord)


def is_c_method(obj: object) -> bool:
    return inspect.ismethoddescriptor(obj) or type(obj) in (type(str.index),
                                                            type(str.__add__),
                                                            type(str.__new__))


def is_c_staticmethod(obj: object) -> bool:
    return isinstance(obj, staticmethod)


def is_c_property(obj: object) -> bool:
    return inspect.isdatadescriptor(obj) and hasattr(obj, 'fget')


def is_c_property_readonly(prop: object) -> bool:
    return getattr(prop, 'fset') is None


def is_c_type(obj: object) -> bool:
    return inspect.isclass(obj) or type(obj) is type(int)


def is_c_module(module: ModuleType) -> bool:
    return ('__file__' not in module.__dict__ or
            os.path.splitext(module.__dict__['__file__'])[-1] in ['.so', '.pyd'])


def method_name_sort_key(name: str) -> Tuple[int, str]:
    if name == '__init__':
        return 0, name
    if name.startswith('__') and name.endswith('__'):
        return 1, name
    return 2, name


def write_header(file: IO[str], module_name: Optional[str]) -> None:
    file.write('# -*- coding: utf-8 -*-\n')
    if module_name:
        file.write(f'# Stubs for {module_name}\n')
    file.write(
        '#\n'
        '# NOTE: This dynamically typed stub was automatically generated by stubgen.\n\n')
