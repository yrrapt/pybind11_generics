# -*- coding: utf-8 -*-

import pytest

import test

test_data = [
    ([], "foobar"),
    ([1, 3, "hi", 7.5, [1, "hi"]], 17),
    ([2, 4, "hi"], [2.6, 7, "bye"]),
]


@pytest.mark.parametrize("data,val", test_data)
def test_constructor(data, val):
    """Check object is constructed properly."""
    obj = test.TestAny(data, val)
    assert obj.get_py_data() == data
    assert obj.get_val() == val


def test_error():
    """Check object errors when input has wrong data type."""
    with pytest.raises(TypeError):
        test.TestAny("foo", [1, 2, 3])
    with pytest.raises(TypeError):
        test.TestAny(3, [1, 2, 3])
