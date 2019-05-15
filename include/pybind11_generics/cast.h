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

#ifndef PYBIND11_GENERICS_CAST_H
#define PYBIND11_GENERICS_CAST_H

#include <iterator>
#include <type_traits>

#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace pybind11_generics {

// SFINAE used to prevent implicit conversion; input argument must be handle
// to avoid redundant reference creation
template <typename T, typename H, std::enable_if_t<std::is_same_v<py::handle, H>> * = nullptr>
T cast_from_handle(const H &val) {
    if constexpr (std::is_same_v<T, py::object>) {
        return pybind11::reinterpret_borrow<T>(val);
    } else if constexpr (pybind11::detail::is_pyobject<T>::value) {
        if (pybind11::isinstance<T>(val)) {
            return pybind11::reinterpret_borrow<T>(val);
        }
        throw py::type_error("Cannot cast item to generic type!");
    } else {
        return val.template cast<T>();
    }
}

// SFINAE used to prevent implicit conversion; input argument must be handle
// to avoid redundant reference creation
template <typename T, typename H, std::enable_if_t<std::is_same_v<py::handle, H>> * = nullptr>
T cast_from_handle_steal(const H &val) {
    if constexpr (std::is_same_v<T, py::object>) {
        return pybind11::reinterpret_steal<T>(val);
    } else if constexpr (pybind11::detail::is_pyobject<T>::value) {
        if (pybind11::isinstance<T>(val)) {
            return pybind11::reinterpret_steal<T>(val);
        }
        throw py::type_error("Cannot cast item to generic type!");
    } else {
        return val.template cast<T>();
    }
}

} // namespace pybind11_generics

#endif
