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

#ifndef PYBIND11_GENERICS_CAST_INPUT_ITERATOR_H
#define PYBIND11_GENERICS_CAST_INPUT_ITERATOR_H

#include <iterator>

#include <pybind11/pybind11.h>

#include <pybind11_generics/cast.h>

namespace py = pybind11;

namespace pybind11_generics {

template <typename T, typename WrapIter> class cast_input_iterator {
  public:
    using difference_type = std::size_t;
    using iterator_category = std::input_iterator_tag;
    using value_type = T;
    using reference = const value_type &;
    using pointer = const value_type *;
    using It = cast_input_iterator;

  protected:
    WrapIter iter_, end_;
    value_type val_;

  public:
    cast_input_iterator() = default;

    cast_input_iterator(WrapIter iter, WrapIter end) : iter_(iter), end_(end) {
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
    value_type _get_value_from_iter() const { return cast_from_handle<value_type>(*iter_); }
};

} // namespace pybind11_generics

#endif
