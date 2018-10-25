#ifndef PYBIND11_GENERICS_TYPE_NAME_H
#define PYBIND11_GENERICS_TYPE_NAME_H

#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace pybind11_generic {

using Any = py::object;

template <typename T> class List;

}; // namespace pybind11_generic

namespace pybind11 {
namespace detail {
template <> struct handle_type_name<py::object> {
  static PYBIND11_DESCR name() { return _("Any"); }
};

template <typename T> struct handle_type_name<pybind11_generic::List<T>> {
  static PYBIND11_DESCR name() {
    return _("List[") + handle_type_name<T>::name() + _("]");
  }
};

} // namespace detail
} // namespace pybind11

#endif
