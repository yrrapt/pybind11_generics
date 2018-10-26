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
        throw std::runtime_error("Cannot cast item to generic type!");
    } else {
        return val.template cast<T>();
    }
}

} // namespace pybind11_generics

#endif
