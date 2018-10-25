# -*- coding: utf-8 -*-

import pytest

import test

test_data = [
    (1, 1),
    (2.5, 2),
    ("foobar", 0),
]


@pytest.mark.parametrize("data,index", test_data)
def test_constructor(data, index):
    """Check object is constructed properly."""
    obj = test.TestUnion(data)
    assert obj.get_data() == data
    assert obj.index() == index


def test_error():
    with pytest.raises(TypeError):
        test.TestUnion([])
    with pytest.raises(TypeError):
        test.TestUnion(["hi"])
    with pytest.raises(TypeError):
        test.TestUnion((1, ))
    with pytest.raises(TypeError):
        test.TestUnion({3.5: 3.5})

