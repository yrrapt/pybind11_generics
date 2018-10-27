# -*- coding: utf-8 -*-

import pytest

import pyg_test

test_data = [
    (pyg_test.TestOptional, None),
    (pyg_test.TestOptional, []),
    (pyg_test.TestOptional, [1, 2]),
]

fail_data = [
    (pyg_test.TestOptional, TypeError, ()),
    (pyg_test.TestOptional, TypeError, 3),
    (pyg_test.TestOptional, TypeError, 'foobar'),
]


@pytest.mark.parametrize("cls,data", test_data)
def test_constructor(cls, data):
    """Check object is constructed properly."""
    obj = cls(data)
    if data is None:
        assert obj.get_data() is None
    else:
        assert obj.get_data() == data


@pytest.mark.parametrize("cls,err,data", fail_data)
def test_error(cls, err, data):
    """Check object errors when input has wrong data type."""
    with pytest.raises(err):
        cls(data)
