# -*- coding: utf-8 -*-

import pytest

import pyg_test

test_data = [
    (pyg_test.TestList, []),
    (pyg_test.TestList, [1, 3, 5, 7, 6]),
    (pyg_test.TestList, [2, 4, 8]),
    (pyg_test.TestList, [13]),
]

fail_data = [
    (pyg_test.TestList, TypeError, [1, 2, 3.5]),
]


@pytest.mark.parametrize("cls,data", test_data)
def test_constructor(cls, data):
    """Check object is constructed properly."""
    obj = cls(data)
    assert obj.get_data() == data
    assert obj.get_py_data() == data


@pytest.mark.parametrize("cls,err,data", fail_data)
def test_error(cls, err, data):
    """Check object errors when input has wrong data type."""
    with pytest.raises(err):
        cls(data)
