# -*- coding: utf-8 -*-

import pytest

import test

test_data = [
    ((1, 3.5), (2, 4.8, "foobar")),
    ((14, 4.0), (4, 3.2, "foobar")),
    ((29, 18.8), (5, 1.0, "")),
]


@pytest.mark.parametrize("data,val", test_data)
def test_constructor(data, val):
    """Check object is constructed properly."""
    obj = test.TestTuple(data, val)
    assert obj.get_pair() == data
    assert obj.get_tuple() == val

    
def test_error():
    """Check object errors when input has wrong data type."""
    with pytest.raises(TypeError):
        test.TestTuple([1, 2.0], [1, 2.5, 'foobar'])
    with pytest.raises(RuntimeError):
        test.TestTuple((1, 2.0), (1.5, 2.5, 'foobar'))
    with pytest.raises(TypeError):
        test.TestTuple((1, 2.0, 3), (1, 2, 'foobar'))
    with pytest.raises(TypeError):
        test.TestTuple((1,), (1, 2, 'foobar'))
    with pytest.raises(TypeError):
        test.TestTuple((1, 2.5), (1, 2, 'foobar', 'baz'))

