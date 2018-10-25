#ifndef PYBIND11_GENERICS_TYPE_NAME_H
#define PYBIND11_GENERICS_TYPE_NAME_H

#include <string>

#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace pybind11 {
namespace detail {

// common C++ types
template <> struct handle_type_name<double> {
  static PYBIND11_DESCR name() { return _("float"); }
};

template <> struct handle_type_name<std::string> {
  static PYBIND11_DESCR name() { return _("str"); }
};

// type name overrides
template <> struct handle_type_name<py::int_> {
  static PYBIND11_DESCR name() { return _("int"); }
};

template <> struct handle_type_name<py::float_> {
  static PYBIND11_DESCR name() { return _("float"); }
};

template <> struct handle_type_name<py::list> {
  static PYBIND11_DESCR name() { return _("List[Any]"); }
};

template <> struct handle_type_name<py::dict> {
  static PYBIND11_DESCR name() { return _("Dict[Any, Any]"); }
};

template <> struct handle_type_name<py::tuple> {
  static PYBIND11_DESCR name() { return _("Tuple[Any, ...]"); }
};

} // namespace detail
} // namespace pybind11

#endif
