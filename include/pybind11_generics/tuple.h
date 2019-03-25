#ifndef PYBIND11_GENERICS_TUPLE_H
#define PYBIND11_GENERICS_TUPLE_H

#include <tuple>
#include <type_traits>
#include <utility>

#include <pybind11_generics/cast.h>
#include <pybind11_generics/type_name.h>

namespace py = pybind11;

namespace pybind11_generics {

namespace detail {

template <Py_ssize_t n> struct set_tuple {
    template <typename U, typename... Us>
    constexpr void operator()(PyObject *tup, U &&arg0, Us &&... args) {
        // PyTuple_SetItem steals reference
        if constexpr (py::detail::is_pyobject<U>::value) {
            if constexpr (std::is_lvalue_reference_v<U>) {
                // lvalue, incref before setItem steals reference
                PyTuple_SET_ITEM(tup, n, arg0.inc_ref().ptr());
            } else {
                // rvalue, release (so destructor don't dercrement reference) and steal reference
                PyTuple_SET_ITEM(tup, n, arg0.release().ptr());
            }
        } else {
            // create temporary object, release (so destructor don't decrement reference),
            // then pass the released pointer to SetItem for it to steal
            PyTuple_SET_ITEM(tup, n, py::cast(std::forward<U>(arg0)).release().ptr());
        }
        set_tuple<n + 1>{}(tup, args...);
    }
    constexpr void operator()(PyObject *tup) {}
};

} // namespace detail

using tuple_base = py::tuple;

template <typename... T> class Tuple : public tuple_base {
  public:
    // inherit check_ so we can check if a python object matches this generic
    using tuple_base::check_;

    template <class... Args> Tuple(Args &&... args) : tuple_base(std::forward<Args>(args)...) {
        if (size() != sizeof...(T))
            throw py::type_error("Generic Tuple length mismatch!");
    }

    explicit Tuple(size_t size = 0) : tuple_base(sizeof...(T)) {}

    template <std::size_t I> std::tuple_element_t<I, std::tuple<T...>> get() const {
        PyObject *result = PyTuple_GetItem(ptr(), static_cast<Py_ssize_t>(I));
        if (!result) {
            throw py::error_already_set();
        }

        return cast_from_handle<std::tuple_element_t<I, std::tuple<T...>>>(py::handle(result));
    }

    static Tuple make_tuple(T &&... args) {
        PyObject *result = PyTuple_New((Py_ssize_t)sizeof...(T));
        detail::set_tuple<0>{}(result, args...);

        return {result, stolen_t{}};
    }

    static Tuple make_tuple(const T &... args) {
        PyObject *result = PyTuple_New((Py_ssize_t)sizeof...(T));
        detail::set_tuple<0>{}(result, args...);

        return {result, stolen_t{}};
    }
};

} // namespace pybind11_generics

namespace std {

template <typename... T>
struct tuple_size<pybind11_generics::Tuple<T...>> : tuple_size<tuple<T...>> {};

template <size_t N, typename... T>
struct tuple_element<N, pybind11_generics::Tuple<T...>> : tuple_element<N, tuple<T...>> {};

} // namespace std

namespace pybind11 {
namespace detail {

template <typename... T> struct handle_type_name<pybind11_generics::Tuple<T...>> {
    static constexpr auto name_fun() {
        if constexpr (sizeof...(T) == 0)
            return _("Tuple[()]");
        else
            return _("Tuple[") + concat(py::detail::make_caster<T>::name...) + _("]");
    }

    static constexpr auto name = name_fun();
};

} // namespace detail
} // namespace pybind11

#endif
