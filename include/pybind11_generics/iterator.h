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

template <typename T> class Iterator : public iterator_base {
  public:
    using iterator_category = std::input_iterator_tag;
    using difference_type = Py_ssize_t;
    using value_type = std::remove_reference_t<T>;
    using reference = const value_type &;
    using pointer = const value_type *;

  private:
    std::optional<value_type> value = {};

    void advance() {
        PyObject *ptr = PyIter_Next(m_ptr);
        if (PyErr_Occurred()) {
            throw py::error_already_set();
        }
        if (ptr == nullptr) {
            m_ptr = nullptr;
            value.reset();
        } else {
            value = cast_from_handle_steal<value_type>(py::handle(ptr));
        }
    }

  public:
    PYBIND11_OBJECT_DEFAULT(Iterator, iterator_base, PyIter_Check)

    static Iterator sentinel() { return {}; }

    Iterator begin() const { return *this; }

    Iterator end() const { return sentinel(); }

    Iterator &operator++() {
        advance();
        return *this;
    }

    Iterator operator++(int) {
        auto rv = *this;
        advance();
        return rv;
    }

    reference operator*() const {
        evaluate();
        return *value;
    }

    pointer operator->() const {
        evaluate();
        return value.operator->();
    }

    const std::optional<value_type> &evaluate() const {
        if (m_ptr && !value) {
            auto &self = const_cast<Iterator &>(*this);
            self.advance();
        }
        return value;
    }

    friend bool operator==(const Iterator &a, const Iterator &b) {
        return a.evaluate() == b.evaluate();
    }

    friend bool operator!=(const Iterator &a, const Iterator &b) { return !(a == b); }
};

template <typename Iter, typename Sentinel, py::return_value_policy Policy> class IteratorState {
  public:
    Iter it;
    Sentinel end;

    IteratorState &get_iter() { return *this; }
    auto get_next() -> std::remove_reference_t<decltype(*std::declval<Iter>())> {
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
    typedef IteratorState<Iter, Sentinel, Policy> state;

    py::class_<state>(py::handle(), "IteratorState", py::module_local())
        .def("__iter__", &state::get_iter)
        .def("__next__", &state::get_next, Policy);
}

template <typename Iter, typename Sentinel = Iter,
          py::return_value_policy Policy = py::return_value_policy::reference_internal>
auto make_iterator(Iter first, Sentinel last)
    -> Iterator<std::remove_cv_t<std::remove_reference_t<decltype(*std::declval<Iter>())>>> {
    typedef IteratorState<Iter, Sentinel, Policy> state;
    return py::cast(state{std::move(first), std::move(last)});
}

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template <typename T> struct handle_type_name<pybind11_generics::Iterator<T>> {
    static constexpr auto name = _("Iterator[") + handle_type_name<T>::name + _("]");
};

} // namespace detail
} // namespace pybind11

#endif
