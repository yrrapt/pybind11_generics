# -*- coding: utf-8 -*-

from itertools import zip_longest

import pytest

import test

test_data = [
    [],
    ["hi"],
    ["foo", "bar", "baz"],
    ["", "boo"],
]


@pytest.mark.parametrize("data", test_data)
def test_constructor(data):
    """Check object is constructed properly."""
    obj = test.TestIter(iter(data))
    assert obj.get_data() == data


@pytest.mark.parametrize("data", test_data)
def test_iter(data):
    """Check object is constructed properly."""
    obj = test.TestIter(iter(data))
    for a, b in zip_longest(obj.get_iter(), data):
        assert a == b


def test_error():
    """Check object errors when input has wrong data type."""
    with pytest.raises(TypeError):
        test.TestIter(["a", "b", "c"])
    with pytest.raises(TypeError):
        test.TestIter(None)
    with pytest.raises(TypeError):
        test.TestIter([])
    with pytest.raises(RuntimeError):
        test.TestIter(iter([1, 2, 3]))
