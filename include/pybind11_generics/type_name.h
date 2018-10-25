#ifndef PYBIND11_GENERICS_TYPE_NAME_H
#define PYBIND11_GENERICS_TYPE_NAME_H

#include <string>

#include <pybind11/pybind11.h>

namespace pybind11 {
namespace detail {

// common C++ types
template <> struct handle_type_name<double> {
  static PYBIND11_DESCR name() { return _("float"); }
};

template <> struct handle_type_name<std::string> {
  static PYBIND11_DESCR name() { return _("str"); }
};

} // namespace detail
} // namespace pybind11

#endif
