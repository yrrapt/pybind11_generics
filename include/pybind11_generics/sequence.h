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

#ifndef PYBIND11_GENERICS_SEQUENCE_H
#define PYBIND11_GENERICS_SEQUENCE_H

#include <type_traits>

#include <pybind11_generics/cast_input_iterator.h>
#include <pybind11_generics/type_name.h>

namespace py = pybind11;

namespace pybind11_generics {

using sequence_base = py::sequence;

template <typename T> class Sequence : public sequence_base {
  private:
    class cast_seq_iterator {
      public:
        using difference_type = std::size_t;
        using iterator_category = std::input_iterator_tag;
        using value_type = std::remove_reference_t<T>;
        using reference = const value_type &;
        using pointer = const value_type *;
        using It = cast_seq_iterator;

      protected:
        Sequence seq_;
        std::size_t idx_;
        value_type val_;

      public:
        cast_seq_iterator() = default;

        explicit cast_seq_iterator(Sequence seq, std::size_t idx) : seq_(seq), idx_(idx) {
            if (idx_ < seq_.size()) {
                val_ = seq_[idx_];
            }
        }

        friend bool operator==(const It &a, const It &b) { return a.idx_ == b.idx_; }
        friend bool operator!=(const It &a, const It &b) { return !(a == b); }

        reference operator*() const { return val_; }
        pointer operator->() const { return &val_; }

        It &operator++() {
            ++idx_;
            if (idx_ < seq_.size()) {
                val_ = seq_[idx_];
            }
            return *this;
        }
        It operator++(int) {
            auto copy = *this;
            ++(*this);
            return copy;
        }
    };

  public:
    using value_type = std::remove_reference_t<T>;
    using const_iterator = cast_seq_iterator;

    template <typename V>
    using IsT =
        std::enable_if_t<std::is_same_v<value_type, std::remove_cv_t<std::remove_reference_t<V>>>,
                         int>;

    // inherit check_ so we can check if a python object matches this generic
    using sequence_base::check_;
    using sequence_base::sequence_base;

    value_type operator[](size_t index) const {
        PyObject *result = PySequence_GetItem(ptr(), static_cast<Py_ssize_t>(index));
        if (!result) {
            throw py::error_already_set();
        }
        // NOTE: PySequence_GetItem() returns a new reference instead of a borrowed reference,
        // so we need to steal the reference.
        return cast_from_handle_steal<value_type>(py::handle(result));
    }
    const_iterator begin() const { return const_iterator(*this, 0); }
    const_iterator end() const { return const_iterator(*this, PySequence_Size(m_ptr)); }
};

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template <typename T> struct handle_type_name<pybind11_generics::Sequence<T>> {
    static constexpr auto name = _("Sequence[") + py::detail::make_caster<T>::name + _("]");
};

} // namespace detail
} // namespace pybind11

#endif
