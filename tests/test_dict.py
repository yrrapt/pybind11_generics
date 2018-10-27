# -*- coding: utf-8 -*-

import pytest

import pyg_test

test_data = [
    (pyg_test.TestDict, {}),
    (pyg_test.TestDict, {'hi': 1, 'bye': 2}),
    (pyg_test.TestDict, {'hi': 3, 'foo': 2, 'bar': -1}),
]

fail_data = [
    (pyg_test.TestDict, TypeError, [('hi', 2)]),
    (pyg_test.TestDict, RuntimeError, {'hi': 1.5}),
    (pyg_test.TestDict, RuntimeError, {1: 1}),
    (pyg_test.TestDict, RuntimeError, {1: 'bye'}),
]


@pytest.mark.parametrize("cls,data", test_data)
def test_constructor(cls, data):
    """Check object is constructed properly."""
    obj = cls(data)
    assert obj.get_data() == data


@pytest.mark.parametrize("cls,err,data", fail_data)
def test_error(cls, err, data):
    """Check object errors when input has wrong data type."""
    with pytest.raises(err):
        cls(data)
