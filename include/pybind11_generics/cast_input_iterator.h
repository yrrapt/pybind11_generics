#ifndef PYBIND11_GENERICS_CAST_INPUT_ITERATOR_H
#define PYBIND11_GENERICS_CAST_INPUT_ITERATOR_H

#include <iterator>
#include <type_traits>

#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace pybind11_generics {

template <typename T, typename WrapIter> class cast_input_iterator {
public:
  using difference_type = std::size_t;
  using iterator_category = std::input_iterator_tag;
  using value_type = T;
  using reference = value_type &;
  using pointer = value_type *;
  using It = cast_input_iterator;

  struct arrow_proxy {
    value_type value;

    explicit arrow_proxy(value_type &&value) : value(std::move(value)) {}
    const pointer operator->() const { return &value; }
  };

protected:
  WrapIter iter_;

  static value_type cast_value(const py::handle &val) {
    if constexpr (std::is_same_v<value_type, py::object>) {
      return pybind11::reinterpret_borrow<value_type>(val);
    } else if constexpr (pybind11::detail::is_pyobject<value_type>::value) {
      if (pybind11::isinstance<value_type>(val)) {
        return pybind11::reinterpret_borrow<value_type>(val);
      }
      throw std::runtime_error("Cannot cast item to generic type!");
    } else {
      return val.template cast<value_type>();
    }
  }

public:
  cast_input_iterator() = default;

  explicit cast_input_iterator(WrapIter &&iter) : iter_(std::move(iter)) {}

  friend bool operator==(const It &a, const It &b) {
    return a.iter_ == b.iter_;
  }
  friend bool operator!=(const It &a, const It &b) { return !(a == b); }

  const value_type operator*() const { return cast_value(*iter_); }
  arrow_proxy operator->() const { return arrow_proxy(**this); }

  It &operator++() {
    ++iter_;
    return *this;
  }
  It operator++(int) {
    auto copy = *this;
    ++(*this);
    return copy;
  }
};

} // namespace pybind11_generics

#endif
