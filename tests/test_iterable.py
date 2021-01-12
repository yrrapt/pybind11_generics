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

copy_data = [
    ["in", "out", "VDD", "VSS"],
    ["a", "bc", "dfe"],
    ["in", "out", "VDD", "VDD", "VSS"],
]


copy_data_dict = [
    {"a": 1, "b": 5, "def": 7},
]


doc_data = [
    (pyg_test.TestIterableString, "Iterable[str]"),
    (pyg_test.TestIterablePair, "Iterable[Tuple[int, int]]"),
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


@pytest.mark.parametrize("str_list", copy_data)
def test_copy_list_from_iterable(str_list):
    py_list = pyg_test.copy_list_from_iterable(str_list)
    assert py_list == str_list


@pytest.mark.parametrize("str_list", copy_data)
def test_copy_list_from_iterable_set(str_list):
    str_set = set(str_list)
    py_list = pyg_test.copy_list_from_iterable_set(str_set)
    assert sorted(py_list) == sorted(str_set)


@pytest.mark.parametrize("table", copy_data_dict)
def test_copy_list_from_iterable_dict(table):
    expect = list(table.keys())
    py_list = pyg_test.copy_list_from_iterable(table.keys())
    assert py_list == expect
