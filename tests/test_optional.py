# -*- coding: utf-8 -*-

import pytest

import test

test_data = [
    None,
    [],
    [1, 2],
]


@pytest.mark.parametrize("data", test_data)
def test_constructor(data):
    """Check object is constructed properly."""
    obj = test.TestOptional(data)
    if data is None:
        assert obj.get_data() is None
    else:
        assert obj.get_data() == data


def test_error():
    """Check object errors when input has wrong data type."""
    with pytest.raises(TypeError):
        test.TestOptional(())
    with pytest.raises(TypeError):
        test.TestOptional(3)
    with pytest.raises(TypeError):
        test.TestOptional("foobar")
