# -*- coding: utf-8 -*-

import pytest

import test

test_data = [
    {},
    {'hi': 1, 'bye': 2},
    {'hi': 3, 'foo': 2, 'bar': -1},
]


@pytest.mark.parametrize("data", test_data)
def test_constructor(data):
    """Check object is constructed properly."""
    obj = test.TestDict(data)
    assert obj.get_data() == data


def test_error():
    """Check object errors when input has wrong data type."""
    with pytest.raises(TypeError):
        test.TestDict([('hi', 2)])
    with pytest.raises(RuntimeError):
        test.TestDict({'hi': 1.5})
    with pytest.raises(RuntimeError):
        test.TestDict({1: 1})
    with pytest.raises(RuntimeError):
        test.TestDict({1: 'bye'})
