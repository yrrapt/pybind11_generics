# -*- coding: utf-8 -*-

from typing import Type, List, Any

from itertools import zip_longest

import pytest

import test

from .util import get_help_str


test_data = [
    (test.TestIterString, []),
    (test.TestIterString, ["hi"]),
    (test.TestIterString, ["foo", "bar", "baz"]),
    (test.TestIterString, ["", "boo"]),
    (test.TestIterPair, []),
    (test.TestIterPair, [(1, 1)]),
    (test.TestIterPair, [(1, 2), (-1, 3), (0, 7)]),
    (test.TestIterPair, [(0, 0), (32, 14)]),
]

fail_data = [
    (test.TestIterString, ['a', 'b', 'c'], TypeError),
    (test.TestIterString, None, TypeError),
    (test.TestIterString, [], TypeError),
    (test.TestIterString, iter([1, 2, 3]), RuntimeError),
    (test.TestIterPair, [(1, 1), (2, 2), (3, 3)], TypeError),
    (test.TestIterPair, None, TypeError),
    (test.TestIterPair, [], TypeError),
    (test.TestIterPair, iter([1, 2, 3]), RuntimeError),
]

doc_data = [

]


@pytest.mark.parametrize("cls,data", test_data)
def test_constructor(cls, data):
    """Check object is constructed properly."""
    obj = cls(iter(data))
    assert obj.get_data() == data


@pytest.mark.parametrize("cls,data", test_data)
def test_iter(cls, data):
    """Check object is constructed properly."""
    obj = cls(iter(data))
    for a, b in zip_longest(obj.get_iter(), data):
        assert a == b


@pytest.mark.parametrize("cls,data,err", fail_data)
def test_error(cls, data, err):
    """Check object errors when input has wrong data type."""
    with pytest.raises(err):
        cls(data)
