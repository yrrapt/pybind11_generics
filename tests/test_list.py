# -*- coding: utf-8 -*-

import pytest

import pyg_test
from pyg_test import get_list, ListHolder

from .util import do_constructor_test, do_error_test, do_doc_test

class ChildList(pyg_test.TestList):
    def __init__(self, vec1, vec2):
        pyg_test.TestList.__init__(self, vec1)
        self._list2 = vec2

    def get_data(self):
        return self._list2

    def get_data_base(self):
        return pyg_test.TestList.get_data(self)


test_data = [
    (pyg_test.TestList, []),
    (pyg_test.TestList, [1, 3, 5, 7, 6]),
    (pyg_test.TestList, [2, 4, 8]),
    (pyg_test.TestList, [13]),
]

fail_data = [
    (pyg_test.TestList, TypeError, [1, 2, 3.5]),
]

doc_data = [
    (pyg_test.TestList, 'List[int]'),
]


@pytest.mark.parametrize("cls,data", test_data)
def test_constructor(cls, data):
    """Check object is constructed properly."""
    do_constructor_test(cls, data)


@pytest.mark.parametrize("cls,err,data", fail_data)
def test_error(cls, err, data):
    """Check object errors when input has wrong data type."""
    do_error_test(cls, err, data)


@pytest.mark.parametrize("cls,type_str", doc_data)
def test_doc(cls, type_str):
    """Check object has correct doc string."""
    do_doc_test(cls, type_str)


def test_inheritance():
    """Test inheritance behavior."""
    vec1 = [1, 2, 3, 4]
    vec2 = [5, 6, 7]

    obj = ChildList(vec1, vec2)

    assert obj.get_data() == vec2
    assert obj.get_data_base() == vec1
    assert get_list(obj) == vec1

    holder = ListHolder(obj)
    obj_ref = holder.get_obj_ref()
    obj_ptr = holder.get_obj_ptr()
    assert obj_ref is obj
    assert obj_ptr is obj
    assert isinstance(obj_ref, ChildList)
