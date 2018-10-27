# -*- coding: utf-8 -*-

import pytest

import pyg_test

test_data = [
    (pyg_test.TestUnion, 1, 1),
    (pyg_test.TestUnion, 2.5, 2),
    (pyg_test.TestUnion, "foobar", 0),
]

fail_data = [
    (pyg_test.TestUnion, TypeError, []),
    (pyg_test.TestUnion, TypeError, ['hi']),
    (pyg_test.TestUnion, TypeError, (1, )),
    (pyg_test.TestUnion, TypeError, {3.5: 4.5}),
]


@pytest.mark.parametrize("cls, data,index", test_data)
def test_constructor(cls, data, index):
    """Check object is constructed properly."""
    obj = cls(data)
    assert obj.get_data() == data
    assert obj.index() == index


@pytest.mark.parametrize("cls,err,data", fail_data)
def test_error(cls, err, data):
    with pytest.raises(err):
        cls(data)
