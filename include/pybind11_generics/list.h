#ifndef PYBIND11_GENERICS_LIST_H
#define PYBIND11_GENERICS_LIST_H

#include <type_traits>

#include <pybind11_generics/cast_input_iterator.h>
#include <pybind11_generics/type_name.h>

namespace py = pybind11;

namespace pybind11_generics {

using list_base = py::list;

template <typename T> class List : public list_base {
  public:
    using value_type = std::remove_reference_t<T>;
    using const_reference = const value_type &;
    using base_iter_type = py::detail::list_iterator;
    using const_iterator = cast_input_iterator<value_type, base_iter_type>;

    // inherit check_ so we can check if a python object matches this generic
    using list_base::check_;
    using list_base::list_base;

    value_type operator[](size_t index) const {
        PyObject *result = PyList_GetItem(ptr(), static_cast<Py_ssize_t>(index));
        if (!result) {
            throw py::error_already_set();
        }
        return cast_from_handle<value_type>(py::handle(result));
    }
    const_iterator begin() const { return const_iterator(list_base::begin()); }
    const_iterator end() const { return const_iterator(list_base::end()); }

    template <class V, std::enable_if_t<
                           std::is_same_v<value_type, std::remove_cv_t<std::remove_reference_t<V>>>,
                           int> = 0>
    void append(V &&val) const {
        list_base::append(std::forward<V>(val));
    }
    template <class V, std::enable_if_t<
                           std::is_same_v<value_type, std::remove_cv_t<std::remove_reference_t<V>>>,
                           int> = 0>
    void push_back(V &&val) {
        list_base::append(std::forward<V>(val));
    }
    template <class... Args> void emplace_back(Args &&... args) {
        push_back(value_type(std::forward<Args>(args)...));
    }
    // empty method for compatibility reason
    void reserve(std::size_t size) {}
};

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template <typename T> struct handle_type_name<pybind11_generics::List<T>> {
    static constexpr auto name = _("List[") + py::detail::make_caster<T>::name + _("]");
};

} // namespace detail
} // namespace pybind11

#endif
