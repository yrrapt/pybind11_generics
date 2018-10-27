# -*- coding: utf-8 -*-

import pytest

import pyg_test

test_data = [
    (pyg_test.TestAny, [], "foobar"),
    (pyg_test.TestAny, [1, 3, "hi", 7.5, [1, "hi"]], 17),
    (pyg_test.TestAny, [2, 4, "hi"], [2.6, 7, "bye"]),
]

fail_data = [
    (pyg_test.TestAny, TypeError, "foo", [1, 2, 3]),
    (pyg_test.TestAny, TypeError, 3, [1, 2, 3]),
]


@pytest.mark.parametrize("cls,data,val", test_data)
def test_constructor(cls, data, val):
    """Check object is constructed properly."""
    obj = cls(data, val)
    assert obj.get_py_data() == data
    assert obj.get_val() == val


@pytest.mark.parametrize("cls,err,data,val", fail_data)
def test_error(cls, err, data, val):
    """Check object errors when input has wrong data type."""
    with pytest.raises(err):
        cls(data, val)
