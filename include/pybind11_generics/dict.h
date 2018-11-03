#ifndef PYBIND11_GENERICS_DICT_H
#define PYBIND11_GENERICS_DICT_H

#include <utility>

#include <pybind11_generics/cast_input_iterator.h>
#include <pybind11_generics/type_name.h>

namespace py = pybind11;

namespace pybind11_generics {

template <typename K, typename V, typename WrapIter>
class dict_cast_input_iterator : public cast_input_iterator<std::pair<K, V>, WrapIter> {
  private:
    using iter_base = cast_input_iterator<std::pair<K, V>, WrapIter>;

  public:
    using difference_type = typename iter_base::difference_type;
    using iterator_category = typename iter_base::iterator_category;
    using value_type = typename iter_base::value_type;
    using reference = typename iter_base::reference;
    using pointer = typename iter_base::pointer;

    using iter_base::iter_base;

    value_type operator*() const {
        auto py_pair = *(this->iter_);
        return std::make_pair(cast_from_handle<K>(py_pair.first),
                              cast_from_handle<V>(py_pair.second));
    }
};

using dict_base = py::dict;

template <typename K, typename V> class Dict : public dict_base {
  public:
    using value_type = std::pair<K, V>;
    using base_iter_type = py::detail::dict_iterator;
    using const_iterator = dict_cast_input_iterator<K, V, base_iter_type>;

  private:
    template <class M> void insert_or_assign_helper(PyObject *key_ptr, M &&obj) {
        int code;
        if constexpr (py::detail::is_pyobject<M>::value) {
            code = PyObject_SetItem(ptr(), key_ptr, obj.ptr());
        } else {
            auto val_obj = py::cast(V(std::forward<M>(obj)));
            code = PyObject_SetItem(ptr(), key_ptr, val_obj.ptr());
        }
        if (code != 0) {
            throw py::error_already_set();
        }
    }

  public:
    // inherit check_ so we can check if a python object matches this generic
    using dict_base::check_;
    using dict_base::dict_base;

    template <class KeyType,
              std::enable_if_t<
                  std::is_same_v<K, std::remove_cv_t<std::remove_reference_t<KeyType>>>, int> = 0>
    value_type operator[](KeyType &&key) const {
        PyObject *result;
        auto key_obj = py::detail::object_or_cast(std::forward<KeyType>(key));
        *result = PyObject_GetItem(ptr(), key_obj.ptr());

        if (!result) {
            throw py::error_already_set();
        }
        return cast_from_handle<V>(py::handle(result));
    }

    template <class KeyType, class M,
              std::enable_if_t<
                  std::is_same_v<K, std::remove_cv_t<std::remove_reference_t<KeyType>>>, int> = 0>
    void insert_or_assign(KeyType &&k, M &&obj) {
        auto key_obj = py::detail::object_or_cast(std::forward<KeyType>(k));
        insert_or_assign_helper(key_obj.ptr(), std::forward<M>(obj));
    }

    const_iterator begin() const { return const_iterator(dict_base::begin()); }

    const_iterator end() const { return const_iterator(dict_base::end()); }

    template <class KeyType,
              std::enable_if_t<
                  std::is_same_v<K, std::remove_cv_t<std::remove_reference_t<KeyType>>>, int> = 0>
    bool contains(KeyType &&key) const {
        return dict_base::contains(py::detail::object_or_cast(std::forward<KeyType>(key)));
    }
};

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template <typename K, typename V> struct handle_type_name<pybind11_generics::Dict<K, V>> {
    static constexpr auto name = _("Dict[") + py::detail::make_caster<K>::name + _(", ") +
                                 py::detail::make_caster<V>::name + _("]");
};

} // namespace detail
} // namespace pybind11

#endif
