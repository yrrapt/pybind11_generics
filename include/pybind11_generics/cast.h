#ifndef PYBIND11_GENERICS_CAST_H
#define PYBIND11_GENERICS_CAST_H

#include <iterator>
#include <type_traits>

#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace pybind11_generics {

template <typename T> T cast_from_handle(const py::handle &val) {
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
