#ifndef PYBIND11_GENERICS_ITERABLE_H
#define PYBIND11_GENERICS_ITERABLE_H

#include <pybind11_generics/iterator.h>

namespace py = pybind11;

namespace pybind11_generics {

using iterable_base = py::object;

template <typename T> class Iterable : public iterable_base {
    using const_iterator = Iterator<T>;

  public:
    static bool iterable_check(const handle &h) {
        return PyObject_HasAttrString(h.ptr(), "__iter__");
    }

    PYBIND11_OBJECT_DEFAULT(Iterable, iterable_base, iterable_check)

    Iterator<T> begin() const {
        PyObject *iter_obj = PyObject_GetIter(m_ptr);
        if (PyErr_Occurred()) {
            throw py::error_already_set();
        }
        if (iter_obj == nullptr) {
            throw std::runtime_error("Cannot get iterator from python object.");
        }
        return py::reinterpret_steal<Iterator<T>>(py::handle(iter_obj));
    }

    Iterator<T> end() const { return Iterator<T>::sentinel(); }
};

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template <typename T> struct handle_type_name<pybind11_generics::Iterable<T>> {
    static constexpr auto name = _("Iterable[") + py::detail::make_caster<T>::name + _("]");
};

} // namespace detail
} // namespace pybind11

#endif
