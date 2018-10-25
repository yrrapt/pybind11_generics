# -*- coding: utf-8 -*-

import pytest

import test

test_data = [
    [],
    [1, 3, 5, 7, 6],
    [2, 4, 8],
]


@pytest.mark.parametrize("data", test_data)
def test_constructor(data):
    """Check object is constructed properly."""
    obj = test.TestList(data)
    assert obj.get_data() == data


def test_error():
    """Check object errors when input has wrong data type."""
    with pytest.raises(RuntimeError):
        test.TestList([1, 2, 3.5])
