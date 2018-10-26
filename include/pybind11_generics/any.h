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
