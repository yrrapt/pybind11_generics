# -*- coding: utf-8 -*-

import pytest

import pyg_test

from .util import do_constructor_test, do_error_test, do_doc_test

test_data = [
    (pyg_test.TestList, []),
    (pyg_test.TestList, [1, 3, 5, 7, 6]),
    (pyg_test.TestList, [2, 4, 8]),
    (pyg_test.TestList, [13]),
]

fail_data = [
    (pyg_test.TestList, TypeError, [1, 2, 3.5]),
]

doc_data = [
    (pyg_test.TestList, 'List[int]'),
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
