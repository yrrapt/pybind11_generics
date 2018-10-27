# -*- coding: utf-8 -*-

from itertools import zip_longest

import pytest

import pyg_test

from .util import get_help_str


test_data = [
    (pyg_test.TestIterString, []),
    (pyg_test.TestIterString, ["hi"]),
    (pyg_test.TestIterString, ["foo", "bar", "baz"]),
    (pyg_test.TestIterString, ["", "boo"]),
    (pyg_test.TestIterPair, []),
    (pyg_test.TestIterPair, [(1, 1)]),
    (pyg_test.TestIterPair, [(1, 2), (-1, 3), (0, 7)]),
    (pyg_test.TestIterPair, [(0, 0), (32, 14)]),
]

fail_data = [
    (pyg_test.TestIterString, TypeError, ['a', 'b', 'c']),
    (pyg_test.TestIterString, TypeError, None),
    (pyg_test.TestIterString, TypeError, []),
    (pyg_test.TestIterString, RuntimeError, iter([1, 2, 3])),
    (pyg_test.TestIterPair, TypeError, [(1, 1), (2, 2), (3, 3)]),
    (pyg_test.TestIterPair, TypeError, None),
    (pyg_test.TestIterPair, TypeError, []),
    (pyg_test.TestIterPair, RuntimeError, iter([1, 2, 3])),
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


@pytest.mark.parametrize("cls,err,data", fail_data)
def test_error(cls, err, data):
    """Check object errors when input has wrong data type."""
    with pytest.raises(err):
        cls(data)
