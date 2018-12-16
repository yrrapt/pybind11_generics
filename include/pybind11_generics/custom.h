#ifndef PYBIND11_GENERICS_CUSTOM_H
#define PYBIND11_GENERICS_CUSTOM_H

#include <pybind11_generics/type_name.h>

namespace pybind11_generics {

using custom_base = py::object;

template <typename T> class Custom : public custom_base {
  public:
    static bool true_check(PyObject *ptr) { return true; }

    PYBIND11_OBJECT_DEFAULT(Custom, custom_base, true_check);

    T *get() { return cast<T *>(); }
    T *operator->() { return cast<T *>(); }
};

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template <typename T> struct handle_type_name<pybind11_generics::Custom<T>> {
    static constexpr auto name = py::detail::make_caster<T>::name;
};

} // namespace detail
} // namespace pybind11

#endif
