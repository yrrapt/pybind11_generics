# -*- coding: utf-8 -*-

import pytest

import pyg_test

test_data = [
    (pyg_test.TestTuple, (1, 3.5), (2, 4.8, "foobar")),
    (pyg_test.TestTuple, (14, 4.0), (4, 3.2, "foobar")),
    (pyg_test.TestTuple, (29, 18.8), (5, 1.0, "")),
]

fail_data = [
    (pyg_test.TestTuple, TypeError, [1, 2.0], [1, 2.5, 'foobar']),
    (pyg_test.TestTuple, RuntimeError, (1, 2.0), (1.5, 2.5, 'foobar')),
    (pyg_test.TestTuple, TypeError, (1, 2.0, 3), (1, 2, 'foobar')),
    (pyg_test.TestTuple, TypeError, (1,), (1, 2, 'foobar')),
    (pyg_test.TestTuple, TypeError, (1, 2.5), (1, 2, 'foobar', 'baz')),
]


@pytest.mark.parametrize("cls,data,val", test_data)
def test_constructor(cls, data, val):
    """Check object is constructed properly."""
    obj = cls(data, val)
    assert obj.get_pair() == data
    assert obj.get_tuple() == val


@pytest.mark.parametrize("cls,err,data,val", fail_data)
def test_error(cls, err, data, val):
    """Check object errors when input has wrong data type."""
    with pytest.raises(err):
        cls(data, val)
