#ifndef PYBIND11_GENERICS_OPTIONAL_H
#define PYBIND11_GENERICS_OPTIONAL_H

#include <pybind11_generics/cast.h>
#include <pybind11_generics/type_name.h>

namespace py = pybind11;

namespace pybind11_generics {

using optional_base = py::object;

template <typename T> class Optional : public optional_base {
  public:
    static bool optional_check(const handle &h) { return h.is_none() || py::isinstance<T>(h); }

    PYBIND11_OBJECT_DEFAULT(Optional, optional_base, optional_check);

    constexpr explicit operator bool() const noexcept { return has_value(); }
    constexpr bool has_value() const noexcept { return is_none(); }
    constexpr const T value() const { return cast_from_handle<T>(py::handle(ptr())); }
    constexpr const T operator*() const { return value(); }
};

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template <typename T> struct handle_type_name<pybind11_generics::Optional<T>> {
    static constexpr auto name = _("Optional[") + handle_type_name<T>::name + _("]");
};

} // namespace detail
} // namespace pybind11

#endif
