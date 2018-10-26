#ifndef PYBIND11_GENERICS_ANY_H
#define PYBIND11_GENERICS_ANY_H

#include <pybind11_generics/type_name.h>

namespace pybind11_generics {

using Any = pybind11::object;

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template <> struct handle_type_name<pybind11::object> {
    static PYBIND11_DESCR name() { return _("Any"); }
};

} // namespace detail
} // namespace pybind11

#endif
