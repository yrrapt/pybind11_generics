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

#ifndef PYBIND11_GENERICS_TYPE_NAME_H
#define PYBIND11_GENERICS_TYPE_NAME_H

#include <string>

#include <pybind11/detail/descr.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace pybind11 {
namespace detail {

template <> struct handle_type_name<py::int_> { static constexpr auto name = _("int"); };

template <> struct handle_type_name<py::float_> { static constexpr auto name = _("float"); };

template <> struct handle_type_name<py::list> { static constexpr auto name = _("List[Any]"); };

template <> struct handle_type_name<py::dict> { static constexpr auto name = _("Dict[Any, Any]"); };

template <> struct handle_type_name<py::tuple> {
    static constexpr auto name = _("Tuple[Any, ...]");
};

} // namespace detail
} // namespace pybind11

#endif
