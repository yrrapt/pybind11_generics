# -*- coding: utf-8 -*-

"""Stub generator for C modules.

The public interface is via the mypy.stubgen module.
"""

import importlib
import inspect
import os.path
import re
from typing import List, Tuple, Optional, Mapping, Any, Set
# noinspection PyUnresolvedReferences
from types import ModuleType

from .stubutil import (
    is_c_module, write_header, infer_sig_from_docstring,
    infer_prop_type_from_docstring
)

# list of classes we need to import from typing package if present
typing_imports = ['Any', 'Union', 'Tuple', 'Optional', 'List', 'Dict', 'Iterable', 'Iterator']
# list of base class names to ignore
skip_base_names = ['pybind11_object', 'object']


def generate_stub_for_c_module(module_name: str,
                               target: str,
                               add_header: bool,
                               ) -> None:
    module = importlib.import_module(module_name)
    assert is_c_module(module), '%s is not a C module' % module_name
    subdir = os.path.dirname(target)
    if subdir and not os.path.isdir(subdir):
        os.makedirs(subdir)
    functions = []  # type: List[str]
    done = set()
    items = sorted(module.__dict__.items(), key=lambda x: x[0])
    for name, obj in items:
        if is_c_function(obj):
            generate_c_function_stub(module_name, name, obj, functions)
            done.add(name)
    types = []  # type: List[str]
    for name, obj in items:
        if name.startswith('__') and name.endswith('__'):
            continue
        if is_c_type(obj):
            generate_c_type_stub(module_name, name, obj, types)
            done.add(name)
    variables = []
    for name, obj in items:
        if name.startswith('__') and name.endswith('__'):
            continue
        if name not in done and not inspect.ismodule(obj):
            type_str = type(obj).__name__
            if type_str not in ('int', 'str', 'bytes', 'float', 'bool'):
                type_str = 'Any'
            variables.append('%s: %s' % (name, type_str))
    output = []
    for line in variables:
        output.append(line)
    if output and functions:
        output.append('')
    for line in functions:
        output.append(line)
    for line in types:
        if line.startswith('class') and output and output[-1]:
            output.append('')
        output.append(line)
    output = add_typing_import(output)
    with open(target, 'w') as file:
        if add_header:
            write_header(file, module_name)
        for line in output:
            file.write('%s\n' % line)


def add_typing_import(output: List[str]) -> List[str]:
    names = []
    # These names include generic types from pybind11_generics, and also
    # types supported by pybind11
    for name in typing_imports:
        if any(re.search(r'\b%s\b' % name, line) for line in output):
            names.append(name)
    if names:
        return ['from typing import %s' % ', '.join(names), ''] + output
    else:
        return output[:]


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


def generate_c_function_stub(module_name: str,
                             name: str,
                             obj: object,
                             output: List[str],
                             self_var: Optional[str] = None,
                             class_name: Optional[str] = None,
                             ) -> None:
    ret_type = 'Any'

    if self_var:
        self_arg = '%s, ' % self_var
    else:
        self_arg = ''

    docstr = getattr(obj, '__doc__', None)
    inferred = infer_sig_from_docstring(docstr, name)
    if inferred:
        sig, ret_type = inferred
    else:
        if class_name:
            sig = infer_method_sig(name)
        else:
            sig = '(*args, **kwargs)'
    # strip away parenthesis
    sig = sig[1:-1]
    if sig:
        if self_var:
            # remove annotation on self from signature if present
            groups = sig.split(',', 1)
            if groups[0] == self_var or groups[0].startswith(self_var + ':'):
                self_arg = ''
                sig = '{},{}'.format(self_var, groups[1]) if len(groups) > 1 else self_var
    else:
        self_arg = self_arg.replace(', ', '')

    ans = 'def %s(%s%s) -> %s: ...' % (name, self_arg, sig, ret_type)
    # remove module prefix on class names
    ans = ans.replace(module_name + '.', '')
    output.append(ans)


def generate_c_property_stub(module_name: str, name: str, obj: object, output: List[str],
                             readonly: bool) -> None:
    docstr = getattr(obj, '__doc__', None)
    inferred = infer_prop_type_from_docstring(docstr)
    if not inferred:
        inferred = 'Any'
    else:
        # remove module prefix on class names
        inferred = inferred.replace(module_name + '.', '')

    output.append('@property')
    output.append('def {}(self) -> {}: ...'.format(name, inferred))
    if not readonly:
        output.append('@{}.setter'.format(name))
        output.append('def {}(self, val: {}) -> None: ...'.format(name, inferred))


def generate_c_type_stub(module_name: str,
                         class_name: str,
                         obj: type,
                         output: List[str],
                         ) -> None:
    # typeshed gives obj.__dict__ the not quite correct type Dict[str, Any]
    # (it could be a mappingproxy!), which makes mypyc mad, so obfuscate it.
    obj_dict = getattr(obj, '__dict__')  # type: Mapping[str, Any]
    items = sorted(obj_dict.items(), key=lambda x: method_name_sort_key(x[0]))
    methods = []  # type: List[str]
    properties = []  # type: List[str]
    done = set()  # type: Set[str]
    for attr, value in items:
        if is_c_method(value) or is_c_classmethod(value):
            done.add(attr)
            if not is_skipped_attribute(attr):
                if is_c_classmethod(value):
                    methods.append('@classmethod')
                    self_var = 'cls'
                else:
                    self_var = 'self'
                if attr == '__new__':
                    # TODO: We should support __new__.
                    if '__init__' in obj_dict:
                        # Avoid duplicate functions if both are present.
                        # But is there any case where .__new__() has a
                        # better signature than __init__() ?
                        continue
                    attr = '__init__'
                generate_c_function_stub(module_name, attr, value, methods, self_var,
                                         class_name=class_name)
        elif is_c_property(value):
            done.add(attr)
            generate_c_property_stub(module_name, attr, value, properties,
                                     is_c_property_readonly(value))

    variables = []
    for attr, value in items:
        if is_skipped_attribute(attr):
            continue
        if attr not in done:
            variables.append('%s: Any = ...' % attr)
    all_bases = obj.mro()
    # remove the class itself
    all_bases = all_bases[1:]
    # Remove base classes of other bases as redundant.
    bases = []  # type: List[type]
    for base in all_bases:
        if base.__name__ not in skip_base_names and not any(issubclass(b, base) for b in bases):
            bases.append(base)
    if bases:
        bases_str = '(%s)' % ', '.join(base.__name__ for base in bases)
    else:
        bases_str = ''
    if not methods and not variables and not properties:
        output.append('class %s%s: ...' % (class_name, bases_str))
    else:
        output.append('class %s%s:' % (class_name, bases_str))
        for variable in variables:
            output.append('    %s' % variable)
        for method in methods:
            output.append('    %s' % method)
        for prop in properties:
            output.append('    %s' % prop)


def method_name_sort_key(name: str) -> Tuple[int, str]:
    if name in ('__new__', '__init__'):
        return 0, name
    if name.startswith('__') and name.endswith('__'):
        return 2, name
    return 1, name


def is_skipped_attribute(attr: str) -> bool:
    return attr in ('__getattribute__',
                    '__str__',
                    '__repr__',
                    '__doc__',
                    '__dict__',
                    '__module__',
                    '__weakref__')  # For pickling


def infer_method_sig(name: str) -> str:
    if name.startswith('__') and name.endswith('__'):
        name = name[2:-2]
        if name in ('hash', 'iter', 'next', 'sizeof', 'copy', 'deepcopy', 'reduce', 'getinitargs',
                    'int', 'float', 'trunc', 'complex', 'bool'):
            return '()'
        if name == 'getitem':
            return '(index)'
        if name == 'setitem':
            return '(index, object)'
        if name in ('delattr', 'getattr'):
            return '(name)'
        if name == 'setattr':
            return '(name, value)'
        if name == 'getstate':
            return '()'
        if name == 'setstate':
            return '(state)'
        if name in ('eq', 'ne', 'lt', 'le', 'gt', 'ge',
                    'add', 'radd', 'sub', 'rsub', 'mul', 'rmul',
                    'mod', 'rmod', 'floordiv', 'rfloordiv', 'truediv', 'rtruediv',
                    'divmod', 'rdivmod', 'pow', 'rpow'):
            return '(other)'
        if name in ('neg', 'pos'):
            return '()'
    return '(*args, **kwargs)'
