/*
   Copyright 2018 Eric Chang

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

#include "move_cast.h"
#include "test_any.h"
#include "test_dict.h"
#include "test_iter.h"
#include "test_iterable.h"
#include "test_list.h"
#include "test_optional.h"
#include "test_tuple.h"
#include "test_union.h"

PYBIND11_MODULE(pyg_test, m) {
    m.doc() = "This package contains test wrapper classes for generic "
              "data types.";

    bind_test_list(m);
    bind_test_any(m);
    bind_test_tuple(m);
    bind_test_dict(m);
    bind_test_union(m);
    bind_test_optional(m);
    bind_test_iter(m);
    bind_test_iterable(m);
    bind_move_cast(m);
}
