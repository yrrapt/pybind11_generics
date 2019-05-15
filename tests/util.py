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

from typing import Type, Any, Optional, Tuple

import pytest


init_signature = '__init__(self, arg0: {}) -> None'
data_signature = 'get_data(self) -> {}'


def get_signature(obj: object) -> str:
    return obj.__doc__.splitlines()[0]


def do_constructor_test(cls: Type[Any], data: object) -> None:
    obj = cls(data)
    if data is None:
        assert obj.get_data() is None
    else:
        assert obj.get_data() == data


def do_error_test(cls: Type[Any], err: object, data: object) -> None:
    with pytest.raises(err):
        cls(data)


def do_doc_test(cls: Type[Any], type_str: str, method_name_sig: Optional[Tuple[str, str]] = None):
    assert get_signature(cls.__init__) == init_signature.format(type_str)
    if method_name_sig is None:
        method_name_sig = ('get_data', data_signature)
    assert get_signature(getattr(cls, method_name_sig[0])) == method_name_sig[1].format(type_str)
