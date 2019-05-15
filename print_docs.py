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

import pydoc
import pyg_test

test_classes = [
    pyg_test.TestList,
    pyg_test.TestAnyList,
    pyg_test.TestAnyVal,
    pyg_test.TestTuple,
    pyg_test.TestDict,
    pyg_test.TestUnion,
    pyg_test.TestOptional,
    pyg_test.TestIterString,
    pyg_test.TestIterPair,
]

for cls in test_classes:
    strhelp = pydoc.render_doc(cls)
    print(strhelp)
    print()
