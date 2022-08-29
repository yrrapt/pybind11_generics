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

#ifndef PYBIND11_GENERICS_DICT_H
#define PYBIND11_GENERICS_DICT_H

#include <utility>

#include <pybind11_generics/cast_input_iterator.h>
#include <pybind11_generics/type_name.h>

namespace py = pybind11;

namespace pybind11_generics {

template <typename K, typename V, typename WrapIter> class dict_cast_input_iterator {
  public:
    using difference_type = std::size_t;
    using iterator_category = std::input_iterator_tag;
    using value_type = std::pair<K, V>;
    using reference = const value_type &;
    using pointer = const value_type *;
    using It = dict_cast_input_iterator;

  protected:
    WrapIter iter_, end_;
    value_type val_;

  public:
    dict_cast_input_iterator() = default;

    dict_cast_input_iterator(WrapIter iter, WrapIter end) : iter_(iter), end_(end) {
        if (iter_ != end_) {
            val_ = _get_value_from_iter();
        }
    }

    friend bool operator==(const It &a, const It &b) { return a.iter_ == b.iter_; }
    friend bool operator!=(const It &a, const It &b) { return !(a == b); }

    reference operator*() const { return val_; }
    pointer operator->() const { return &val_; }

    It &operator++() {
        ++iter_;
        if (iter_ != end_) {
            val_ = _get_value_from_iter();
        }
        return *this;
    }
    It operator++(int) {
        auto copy = *this;
        ++(*this);
        return copy;
    }

  private:
    value_type _get_value_from_iter() const {
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
    V operator[](KeyType &&key) const {
        auto key_obj = py::detail::object_or_cast(std::forward<KeyType>(key));
        auto result = PyObject_GetItem(ptr(), key_obj.ptr());

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

    const_iterator begin() const { return const_iterator(dict_base::begin(), dict_base::end()); }

    const_iterator end() const { return const_iterator(dict_base::end(), dict_base::end()); }

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
