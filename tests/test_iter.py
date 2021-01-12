#   Copyright 2018 Eric Chang
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.#

from itertools import zip_longest

import pytest

import pyg_test

from .util import do_error_test, do_doc_test

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
    (pyg_test.TestIterString, TypeError, ["a", "b", "c"]),
    (pyg_test.TestIterString, TypeError, None),
    (pyg_test.TestIterString, TypeError, []),
    (pyg_test.TestIterString, RuntimeError, iter([1, 2, 3])),
    (pyg_test.TestIterPair, TypeError, [(1, 1), (2, 2), (3, 3)]),
    (pyg_test.TestIterPair, TypeError, None),
    (pyg_test.TestIterPair, TypeError, []),
    (pyg_test.TestIterPair, RuntimeError, iter([1, 2, 3])),
]

doc_data = [
    (pyg_test.TestIterString, "Iterator[str]"),
    (pyg_test.TestIterPair, "Iterator[Tuple[int, int]]"),
]


@pytest.mark.parametrize("cls,data", test_data)
def test_constructor(cls, data):
    """Check object is constructed properly."""
    obj = cls(iter(data))
    assert obj.get_data() == data


@pytest.mark.parametrize("cls,data", test_data)
def test_iter(cls, data):
    """Check object iterator works properly."""
    obj = cls(iter(data))
    for a, b in zip_longest(obj.get_iter(), data):
        assert a == b


@pytest.mark.parametrize("cls,err,data", fail_data)
def test_error(cls, err, data):
    """Check object errors when input has wrong data type."""
    do_error_test(cls, err, data)


@pytest.mark.parametrize("cls,type_str", doc_data)
def test_doc(cls, type_str):
    """Check object has correct doc string."""
    method_name_sig = ("get_iter", "get_iter(self) -> {}")
    do_doc_test(cls, type_str, method_name_sig=method_name_sig)
