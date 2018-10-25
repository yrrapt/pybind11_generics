#ifndef PYBIND11_GENERICS_TUPLE_H
#define PYBIND11_GENERICS_TUPLE_H

#include <tuple>
#include <utility>

#include <pybind11_generics/type_name.h>

namespace py = pybind11;

namespace pybind11_generics {

using tuple_base = py::tuple;

template <typename... T> class Tuple : public tuple_base {
public:
  template <class... Args>
  Tuple(Args &&... args) : tuple_base(std::forward<Args>(args)...) {
    if (size() != sizeof...(T))
      throw std::runtime_error("Generic Tuple length mismatch!");
  }

  explicit Tuple(size_t size = 0) : tuple_base(sizeof...(T)) {}

  template <int I> std::tuple_element_t<I, std::tuple<T...>> get() {
    return tuple_base::operator[](I)
        .template cast<std::tuple_element_t<I, std::tuple<T...>>>();
  }
};

}; // namespace pybind11_generics

#endif
