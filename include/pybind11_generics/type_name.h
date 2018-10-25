#ifndef PYBIND11_GENERICS_TYPE_NAME_H
#define PYBIND11_GENERICS_TYPE_NAME_H

#include <string>
#include <type_traits>

#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace pybind11_generics {

using Any = py::object;

template <typename T> class List;

template <typename... T> class Tuple;

}; // namespace pybind11_generics

namespace pybind11 {
namespace detail {

// common C++ types

template <> struct handle_type_name<double> {
  static PYBIND11_DESCR name() { return _("float"); }
};

template <> struct handle_type_name<std::string> {
  static PYBIND11_DESCR name() { return _("str"); }
};

template <> struct handle_type_name<py::object> {
  static PYBIND11_DESCR name() { return _("Any"); }
};

template <typename T> struct handle_type_name<pybind11_generics::List<T>> {
  static PYBIND11_DESCR name() {
    return _("List[") + handle_type_name<T>::name() + _("]");
  }
};

template <typename... T>
struct handle_type_name<pybind11_generics::Tuple<T...>> {
  static PYBIND11_DESCR name() {
    if constexpr (sizeof...(T) == 0)
      return _("Tuple[()]");
    return _("Tuple[") + concat(handle_type_name<T>::name()...) + _("]");
  }
};

} // namespace detail
} // namespace pybind11

#endif
