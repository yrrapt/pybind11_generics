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

#ifndef PYBIND11_GENERICS_ANY_H
#define PYBIND11_GENERICS_ANY_H

#include <pybind11_generics/type_name.h>

namespace pybind11_generics {

using any_base = py::object;

class Any : public any_base {
  public:
    static bool true_check(PyObject *ptr) { return true; }

    PYBIND11_OBJECT_DEFAULT(Any, any_base, true_check);
};

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template <> struct handle_type_name<pybind11_generics::Any> {
    static constexpr auto name = _("Any");
};

} // namespace detail
} // namespace pybind11

#endif
