#ifndef PYBIND11_GENERICS_ANY_H
#define PYBIND11_GENERICS_ANY_H

#include <pybind11_generics/type_name.h>

namespace pybind11_generics {

    using any_base = py::object;

    class Any : public any_base {
    public:
        using any_base::any_base;

        static bool check_(const handle &h) { return h.ptr() != nullptr; }
    };

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template <> struct handle_type_name<pybind11_generics::Any> { static constexpr auto name = _("Any"); };

} // namespace detail
} // namespace pybind11

#endif
