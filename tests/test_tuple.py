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
