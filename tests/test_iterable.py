# -*- coding: utf-8 -*-

import pytest

import pyg_test

from .util import do_error_test, get_signature, init_signature

test_data = [
    (pyg_test.TestIterableString, []),
    (pyg_test.TestIterableString, ["hi"]),
    (pyg_test.TestIterableString, ("foo", "bar", "baz")),
    (pyg_test.TestIterableString, ("", "boo")),
    (pyg_test.TestIterablePair, []),
    (pyg_test.TestIterablePair, [(1, 1)]),
    (pyg_test.TestIterablePair, [(1, 2), (-1, 3), (0, 7)]),
    (pyg_test.TestIterablePair, ((0, 0), (32, 14))),
]

fail_data = [
    (pyg_test.TestIterableString, TypeError, 3),
    (pyg_test.TestIterableString, TypeError, None),
    (pyg_test.TestIterableString, RuntimeError, [1, 2, 3]),
    (pyg_test.TestIterablePair, TypeError, 3),
    (pyg_test.TestIterablePair, TypeError, None),
    (pyg_test.TestIterablePair, RuntimeError, [1, 2, 3]),
    (pyg_test.TestIterablePair, RuntimeError, "abc"),
]

doc_data = [
    (pyg_test.TestIterableString, 'Iterable[str]'),
    (pyg_test.TestIterablePair, 'Iterable[Tuple[int, int]]'),
]


@pytest.mark.parametrize("cls,data", test_data)
def test_constructor(cls, data):
    """Check object is constructed properly."""
    obj = cls(data)
    val = obj.get_data()
    assert len(val) == len(data)
    for v1, v2 in zip(val, data):
        assert v1 == v2


@pytest.mark.parametrize("cls,err,data", fail_data)
def test_error(cls, err, data):
    """Check object errors when input has wrong data type."""
    do_error_test(cls, err, data)


@pytest.mark.parametrize("cls,type_str", doc_data)
def test_doc(cls, type_str):
    """Check object has correct doc string."""
    assert get_signature(cls.__init__) == init_signature.format(type_str)
