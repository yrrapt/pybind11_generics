#ifndef PYBIND11_GENERICS_ITERATOR_H
#define PYBIND11_GENERICS_ITERATOR_H

#include <iterator>
#include <optional>

#include <pybind11_generics/cast.h>
#include <pybind11_generics/cast_input_iterator.h>
#include <pybind11_generics/type_name.h>

namespace py = pybind11;

namespace pybind11_generics {

using iterator_base = py::object;

template<typename T>
class Iterator : public iterator_base {
public:
  using iterator_category = std::input_iterator_tag;
  using difference_type = Py_ssize_t;
  using value_type = T;
  using reference = const T &;
  using pointer = const T *;

private:
  std::optional<T> value = {};

  void advance() {
      PyObject *ptr = PyIter_Next(m_ptr);
      if (PyErr_Occurred()) {
          throw py::error_already_set();
      }
      if (ptr == nullptr) {
          m_ptr = nullptr;
          value.reset();
      } else {
          value = cast_from_handle_steal(py::handle(ptr));
      }
  }
public:
  static bool check_(const py::handle &h) { return h.ptr() != nullptr && PyIter_Check(h.ptr()); }

  static Iterator sentinel() { return {}; }

  using iterator_base::iterator_base;

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

  const std::optional<T> &evaluate() const {
      if (m_ptr && !value) {
          auto &self = const_cast<Iterator &>(*this);
          self.advance();
      }
      return value;
  }

  friend bool operator==(const Iterator &a, const Iterator &b) {
      if constexpr (pybind11::detail::is_pyobject<T>::value) {
        return a.evaluate() == b.evaluate();
      }
  }

  friend bool operator!=(const iterator &a, const iterator &b) {
      return !(a == b);
  }

};

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template<typename T>
struct handle_type_name<pybind11_generics::Iterator<T>> {
  static constexpr auto name = _("Iterator[") + handle_type_name<T>::name + _("]");
};

} // namespace detail
} // namespace pybind11

#endif
