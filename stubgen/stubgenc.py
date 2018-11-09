# -*- coding: utf-8 -*-

"""Stub generator for C modules.

The public interface is via the mypy.stubgen module.
"""

from typing import List, Tuple, Optional, Mapping, Any, Dict, IO
# noinspection PyUnresolvedReferences
from types import ModuleType

import os
import re
import sys
import inspect
import importlib

# list of classes we need to import from typing package if present
typing_imports = ('Any', 'Union', 'Tuple', 'Optional', 'List', 'Dict', 'Iterable', 'Iterator')
# list of base class names to ignore
skip_base_names = ('pybind11_object', 'object')
# list of supported variable types
base_var_types = ('int', 'str', 'bytes', 'float', 'bool')
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
    types = []  # type: List[str]
    variables = []  # type: List[str]
    functions = []  # type: List[str]
    for name, obj in sorted(module.__dict__.items(), key=lambda x: x[0]):
        if process_c_function(module_name, name, obj, functions, imports):
            pass
        elif process_c_type(module_name, name, obj, types, imports):
            pass
        else:
            process_c_var(name, obj, variables, imports)

    # write output to file
    with open(target, 'w') as file:
        if add_header:
            write_header(file, module_name)

        if imports:
            for c_name, m_name in sorted(imports.items(), key=lambda x: x[1]):
                file.write('from {} import {}\n'.format(m_name, c_name))
            file.write('\n')
        if variables:
            for line in variables:
                file.write(line)
                file.write('\n')
            file.write('\n')
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


def process_c_var(name: str, obj: object, output: List[str], imports: Dict[str, str]) -> bool:
    if (name.startswith('__') and name.endswith('__')) or inspect.ismodule(obj):
        return False

    type_str = type(obj).__name__
    if type_str not in base_var_types:
        type_str = 'Any'
        imports['Any'] = 'typing'
    output.append('{}: {}'.format(name, type_str))
    return True


def process_c_function(module_name: str,
                       name: str,
                       obj: object,
                       output: List[str],
                       imports: Dict[str, str],
                       self_var: Optional[str] = None,
                       class_name: Optional[str] = None,
                       ) -> bool:
    if not is_c_function(obj):
        return False

    docstr = getattr(obj, '__doc__', '')
    if docstr:
        # get signature from docstring
        docstr = docstr.lstrip()
        # look for function signature, which is any string of the format
        # <function_name>(<signature>) -> <return type>
        # or perhaps without the return type

        # in the signature, we allow the following characters:
        # colon/equal: to match default values, like "a: int=1"
        # comma/space/brackets: for type hints like "a: Tuple[int, float]"
        # dot: for classes annotating using full path, like "a: foo.bar.baz"
        # to capture return type,
        sig_str = r'\([a-zA-Z0-9_=:, \[\]\.]*\)'
        sig_match = r'({}{} -> [a-zA-Z].*)$'.format(name, sig_str)
        # first, try to capture return type; we just match until end of line
        m = re.match(sig_match, docstr, re.MULTILINE)
        if m:
            # strip potential white spaces at the right of return type
            # remove module prefix on class names
            sig = m.group(1).rstrip().replace(module_name + '.', '')
            output.append('def {}: ...'.format(sig))
            return True
    elif self_var is not None and name.startswith('__') and name.endswith('__'):
        # check if this is a builtin method for a class
        test = name[2:-2]
        if check_builtin_sig(test, class_name, self_var, output):
            return True

    # cannot detect signature, use a catch all definition
    imports['Any'] = 'typing'
    self_arg = self_var + ', ' if self_var else ''
    output.append('def {}({}*args: Any, **kwargs: Any) -> Any: ...'.format(name, self_arg))
    return True


def process_c_type(module_name: str,
                   class_name: str,
                   obj: type,
                   output: List[str],
                   imports: Dict[str, str],
                   ) -> bool:
    if (class_name.startswith('__') and class_name.endswith('__')) or not is_c_type(obj):
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
        elif process_c_method(module_name, mem_name, mem_obj, methods, imports, class_name):
            pass
        elif process_c_property(mem_name, mem_obj, properties, imports):
            pass
        else:
            imports['Any'] = 'typing'
            variables.append(mem_name + ': Any = ...')

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
        bases_str = '({})'.format(', '.join(base.__name__ for base in bases))
    else:
        bases_str = ''

    if not methods and not variables and not properties:
        output.append('class {}{}: ...'.format(class_name, bases_str))
    else:
        output.append('class {}{}:'.format(class_name, bases_str))
        output.extend(('    {}'.format(line) for line in variables))
        output.extend(('    {}'.format(line) for line in properties))
        output.extend(('    {}'.format(line) for line in methods))

    return True


def process_c_method(module_name: str,
                     name: str,
                     obj: object,
                     output: List[str],
                     imports: Dict[str, str],
                     class_name: str,
                     ) -> bool:
    is_cls_method = is_c_classmethod(obj)
    if not is_c_method(obj) and not is_cls_method:
        return False

    if is_cls_method:
        output.append('@classmethod')
        self_var = 'cls'
    else:
        self_var = 'self'

    return process_c_function(module_name, name, obj, output, imports, self_var=self_var,
                              class_name=class_name)


def process_c_property(name: str,
                       obj: object,
                       output: List[str],
                       imports: Dict[str, str],
                       ) -> bool:
    if not is_c_property(obj):
        return False

    readonly = is_c_property_readonly(obj)

    # check for Google/Numpy style docstring type annotation
    # the docstring has the format "<type>: <descriptions>"
    # in the type string, we allow the following characters
    # dot: because something classes are annotated using full path,
    # brackets: to allow type hints like List[int]
    # comma/space: things like Tuple[int, int]
    test_str = r'^([a-zA-Z0-9_, \.\[\]]*): '
    m = re.match(test_str, getattr(obj, '__doc__', ''))
    if m:
        prop_type = m.group(1)
    else:
        imports['Any'] = 'typing'
        prop_type = 'Any'

    output.append('@property')
    output.append('def {}(self) -> {}: ...'.format(name, prop_type))
    if not readonly:
        output.append('@{}.setter'.format(name))
        output.append('def {}(self, val: {}) -> None: ...'.format(name, prop_type))

    return True


def check_builtin_sig(name: str,
                      cls_name: str,
                      self_var: str,
                      output: List[str],
                      ) -> bool:
    if name in ('int', 'float', 'complex', 'bool'):
        output.append('def __{}__({}) -> {}: ...'.format(name, self_var, name))
        return True
    if name in ('hash', 'sizeof', 'trunc', 'floor', 'ceil'):
        output.append('def __{}__({}) -> {}: ...'.format(name, self_var, 'int'))
        return True
    if name in ('copy', 'deepcopy'):
        output.append('def __{}__({}) -> {}: ...'.format(name, self_var, cls_name))
        return True
    if name == 'delattr':
        output.append('def __{}__({}) -> {}: ...'.format(name, self_var, 'None'))
        return True
    return False


def is_c_function(obj: object) -> bool:
    return inspect.isbuiltin(obj) or type(obj) is type(ord)


def is_c_method(obj: object) -> bool:
    return inspect.ismethoddescriptor(obj) or type(obj) in (type(str.index),
                                                            type(str.__add__),
                                                            type(str.__new__))


def is_c_classmethod(obj: object) -> bool:
    return inspect.isbuiltin(obj) or type(obj).__name__ in ('classmethod',
                                                            'classmethod_descriptor')


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
    if name in ('__new__', '__init__'):
        return 0, name
    if name.startswith('__') and name.endswith('__'):
        return 2, name
    return 1, name


def write_header(file: IO[str], module_name: Optional[str]) -> None:
    file.write('# -*- coding: utf-8 -*-\n')
    if module_name:
        version = '%d.%d' % (sys.version_info.major,
                             sys.version_info.minor)
        file.write('# Stubs for %s (Python %s)\n' % (module_name, version))
    file.write(
        '#\n'
        '# NOTE: This dynamically typed stub was automatically generated by stubgen.\n\n')
