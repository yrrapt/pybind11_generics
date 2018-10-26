#ifndef PYBIND11_GENERICS_TYPE_NAME_H
#define PYBIND11_GENERICS_TYPE_NAME_H

#include <string>

#include <pybind11/detail/descr.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace pybind11 {
namespace detail {

// common C++ types
template <> struct handle_type_name<double> { static constexpr auto name = _("float"); };

template <> struct handle_type_name<std::string> { static constexpr auto name = _("str"); };

// type name overrides
template <> struct handle_type_name<py::int_> { static constexpr auto name = _("int"); };

template <> struct handle_type_name<py::float_> { static constexpr auto name = _("float"); };

template <> struct handle_type_name<py::list> { static constexpr auto name = _("List[Any]"); };

template <> struct handle_type_name<py::dict> { static constexpr auto name = _("Dict[Any, Any]"); };

template <> struct handle_type_name<py::tuple> {
    static constexpr auto name = _("Tuple[Any, ...]");
};

} // namespace detail
} // namespace pybind11

#endif
