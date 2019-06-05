/*
   Copyright 2018 Eric Chang

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

#ifndef PYBIND11_GENERICS_ITERATOR_H
#define PYBIND11_GENERICS_ITERATOR_H

#include <iterator>
#include <optional>
#include <type_traits>
#include <utility>

#include <pybind11_generics/cast.h>
#include <pybind11_generics/cast_input_iterator.h>
#include <pybind11_generics/type_name.h>

namespace py = pybind11;

namespace pybind11_generics {

using iterator_base = py::object;

// A class to return C++ iterators to Python.  Does nothing
// and is only used to get typehint strings to work.
template <typename T> class PyIterator : public iterator_base {
  public:
    PYBIND11_OBJECT_DEFAULT(PyIterator, iterator_base, PyIter_Check);
};

// A class to use Python iterators in C++
template <typename T> class Iterator : public iterator_base {
  public:
    using iterator_category = std::input_iterator_tag;
    using difference_type = Py_ssize_t;
    using value_type = std::remove_reference_t<T>;
    using reference = const value_type &;
    using pointer = const value_type *;

  private:
    std::optional<value_type> value_ = {};

  public:
    Iterator() : iterator_base() { _eval(); };
    Iterator(const py::object &o) : iterator_base(o) { _eval(); }
    Iterator(py::object &&o) : iterator_base(std::move(o)) { _eval(); }
    Iterator(py::handle h, borrowed_t) : iterator_base(h, borrowed_t{}) { _eval(); }
    Iterator(py::handle h, stolen_t) : iterator_base(h, stolen_t{}) { _eval(); }

    // explicitly prohibit converting PyIterator to Iterator.
    // PyIterator should not be used in C++ at all.
    Iterator(const PyIterator<T> &rhs) = delete;
    Iterator(PyIterator<T> &&rhs) = delete;

    static bool check_(handle h) {
        auto ptr = h.ptr();
        return ptr && PyIter_Check(ptr);
    }

    static Iterator sentinel() { return {}; }

    Iterator begin() const { return *this; }

    Iterator end() const { return sentinel(); }

    reference operator*() { return *value_; }

    pointer operator->() { return value_.operator->(); }

    Iterator &operator++() {
        if (m_ptr) {
            PyObject *ptr = PyIter_Next(m_ptr);
            if (PyErr_Occurred()) {
                throw py::error_already_set();
            }
            if (!ptr) {
                m_ptr = nullptr;
                value_.reset();
            } else {
                value_ = cast_from_handle_steal<value_type>(py::handle(ptr));
            }
        }
        return *this;
    }

    friend bool operator==(const Iterator &a, const Iterator &b) { return a.is(b); }

    friend bool operator!=(const Iterator &a, const Iterator &b) { return !(a == b); }

  private:
    void _eval() {
        if (m_ptr && !value_) {
            PyObject *ptr = PyIter_Next(m_ptr);
            if (PyErr_Occurred()) {
                throw py::error_already_set();
            }
            if (!ptr) {
                m_ptr = nullptr;
            } else {
                value_ = cast_from_handle_steal<value_type>(py::handle(ptr));
            }
        }
    }
};

template <typename Iter, typename Sentinel, py::return_value_policy Policy> class IteratorState {
  public:
    Iter it;
    Sentinel end;

    IteratorState &get_iter() { return *this; }
    auto get_next() -> std::remove_cv_t<std::remove_reference_t<decltype(*std::declval<Iter>())>> {
        if (it == end) {
            throw py::stop_iteration();
        }
        auto ans = *it;
        ++it;
        return ans;
    }
};

template <typename Iter, typename Sentinel = Iter,
          py::return_value_policy Policy = py::return_value_policy::reference_internal>
void declare_iterator() {
    using state = IteratorState<Iter, Sentinel, Policy>;

    py::class_<state>(py::handle(), "IteratorState", py::module_local())
        .def("__iter__", &state::get_iter)
        .def("__next__", &state::get_next, Policy);
}

template <typename Iter, typename Sentinel = Iter,
          py::return_value_policy Policy = py::return_value_policy::reference_internal>
auto make_iterator(Iter first, Sentinel last)
    -> PyIterator<std::remove_cv_t<std::remove_reference_t<decltype(*std::declval<Iter>())>>> {
    return py::cast(IteratorState<Iter, Sentinel, Policy>{std::move(first), std::move(last)});
}

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template <typename T> struct handle_type_name<pybind11_generics::Iterator<T>> {
    static constexpr auto name = _("Iterator[") + py::detail::make_caster<T>::name + _("]");
};

template <typename T> struct handle_type_name<pybind11_generics::PyIterator<T>> {
    static constexpr auto name = _("Iterator[") + py::detail::make_caster<T>::name + _("]");
};

} // namespace detail
} // namespace pybind11

#endif
