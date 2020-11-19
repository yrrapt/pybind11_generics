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

from typing import Sequence

import pytest

import pyg_test
from pyg_test import get_sequence

from .util import do_constructor_test2, do_error_test, do_doc_test_init


class ChildSequence(pyg_test.TestSequence):
    def __init__(self, vec1, vec2):
        pyg_test.TestSequence.__init__(self, vec1)
        self._list2 = vec2

    def get_data(self):
        return self._list2

    def get_data_base(self):
        return pyg_test.TestSequence.get_data(self)


class NewList:
    def __init__(self, data):
        self._data = data
    
    def __getitem__(self, idx: int):
        return self._data[idx]

    def __len__(self):
        return len(self._data)


test_data = [
    (pyg_test.TestSequence, (), []),
    (pyg_test.TestSequence, [], []),
    (pyg_test.TestSequence, [1, 3, 5, 7, 6], [1, 3, 5, 7, 6]),
    (pyg_test.TestSequence, (2, 4, 8), [2, 4, 8]),
    (pyg_test.TestSequence, [13], [13]),
    (pyg_test.TestSequence, NewList([13, 28]), [13, 28]),
]

fail_data = [
    (pyg_test.TestSequence, TypeError, [1, 2, 3.5]),
    (pyg_test.TestSequence, TypeError, (1, 2, 3.5)),
]

doc_data = [
    (pyg_test.TestSequence, 'Sequence[int]'),
]


@pytest.mark.parametrize("cls,data,expect", test_data)
def test_constructor(cls, data, expect):
    """Check object is constructed properly."""
    do_constructor_test2(cls, data, expect)


@pytest.mark.parametrize("cls,err,data", fail_data)
def test_error(cls, err, data):
    """Check object errors when input has wrong data type."""
    do_error_test(cls, err, data)


@pytest.mark.parametrize("cls,type_str", doc_data)
def test_doc(cls, type_str):
    """Check object has correct doc string."""
    do_doc_test_init(cls, type_str)
