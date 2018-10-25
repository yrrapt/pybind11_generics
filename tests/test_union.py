# -*- coding: utf-8 -*-

import pytest

import test

test_data = [
    1,
    2.5,
    "foobar",
]


@pytest.mark.parametrize("data", test_data)
def test_constructor(data):
    """Check object is constructed properly."""
    obj = test.TestUnion(data)
    assert obj.get_data() == data


def test_error():
    """Check object errors when input has wrong data type."""
    with pytest.raises(TypeError):
        test.TestUnion([])
    with pytest.raises(TypeError):
        test.TestUnion(["hi"])
    with pytest.raises(TypeError):
        test.TestUnion((1, ))
    with pytest.raises(TypeError):
        test.TestUnion({3.5: 3.5})
