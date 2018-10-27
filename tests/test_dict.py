# -*- coding: utf-8 -*-

import pytest

import pyg_test

from .util import do_constructor_test, do_error_test, do_doc_test

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

doc_data = [
    (pyg_test.TestDict, 'Dict[str, int]'),
]


@pytest.mark.parametrize("cls,data", test_data)
def test_constructor(cls, data):
    """Check object is constructed properly."""
    do_constructor_test(cls, data)


@pytest.mark.parametrize("cls,err,data", fail_data)
def test_error(cls, err, data):
    """Check object errors when input has wrong data type."""
    do_error_test(cls, err, data)


@pytest.mark.parametrize("cls,type_str", doc_data)
def test_doc(cls, type_str):
    """Check object has correct doc string."""
    do_doc_test(cls, type_str)
