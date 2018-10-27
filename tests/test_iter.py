# -*- coding: utf-8 -*-

from itertools import zip_longest

import pytest

import pyg_test

from .util import get_help_strs

test_data = [
    (pyg_test.TestIterString, []),
    (pyg_test.TestIterString, ["hi"]),
    (pyg_test.TestIterString, ["foo", "bar", "baz"]),
    (pyg_test.TestIterString, ["", "boo"]),
    (pyg_test.TestIterPair, []),
    (pyg_test.TestIterPair, [(1, 1)]),
    (pyg_test.TestIterPair, [(1, 2), (-1, 3), (0, 7)]),
    (pyg_test.TestIterPair, [(0, 0), (32, 14)]),
]

fail_data = [
    (pyg_test.TestIterString, TypeError, ['a', 'b', 'c']),
    (pyg_test.TestIterString, TypeError, None),
    (pyg_test.TestIterString, TypeError, []),
    (pyg_test.TestIterString, RuntimeError, iter([1, 2, 3])),
    (pyg_test.TestIterPair, TypeError, [(1, 1), (2, 2), (3, 3)]),
    (pyg_test.TestIterPair, TypeError, None),
    (pyg_test.TestIterPair, TypeError, []),
    (pyg_test.TestIterPair, RuntimeError, iter([1, 2, 3])),
]

doc_data = [
    (pyg_test.TestIterString.__init__,
     ['__init__(self, arg0: Iterator[str]) -> None',
      '',
      'initializer.',
      ],
     ),
    (pyg_test.TestIterString.get_iter,
     ['get_iter(self) -> Iterator[str]',
      '',
      'Get iterator.',
      ],
     ),
    (pyg_test.TestIterPair.__init__,
     ['__init__(self, arg0: Iterator[Tuple[int, int]]) -> None',
      '',
      'initializer.',
      ],
     ),
    (pyg_test.TestIterPair.get_iter,
     ['get_iter(self) -> Iterator[Tuple[int, int]]',
      '',
      'Get iterator.',
      ],
     ),
]


@pytest.mark.parametrize("cls,data", test_data)
def test_constructor(cls, data):
    """Check object is constructed properly."""
    obj = cls(iter(data))
    assert obj.get_data() == data


@pytest.mark.parametrize("cls,data", test_data)
def test_iter(cls, data):
    """Check object is constructed properly."""
    obj = cls(iter(data))
    for a, b in zip_longest(obj.get_iter(), data):
        assert a == b


@pytest.mark.parametrize("cls,err,data", fail_data)
def test_error(cls, err, data):
    """Check object errors when input has wrong data type."""
    with pytest.raises(err):
        cls(data)


@pytest.mark.parametrize("obj,doc_lines", doc_data)
def test_doc(obj, doc_lines):
    """Check object errors when input has wrong data type."""
    for line1, line2 in zip_longest(get_help_strs(obj), doc_lines):
        assert line1 == line2
