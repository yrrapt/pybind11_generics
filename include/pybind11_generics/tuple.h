#ifndef PYBIND11_GENERICS_TUPLE_H
#define PYBIND11_GENERICS_TUPLE_H

#include <tuple>
#include <utility>

#include <pybind11_generics/cast.h>
#include <pybind11_generics/type_name.h>

namespace py = pybind11;

namespace pybind11_generics {

using tuple_base = py::tuple;

template <typename... T> class Tuple : public tuple_base {
public:
  // inherit check_ so we can check if a python object matches this generic
  using tuple_base::check_;

  template <class... Args>
  Tuple(Args &&... args) : tuple_base(std::forward<Args>(args)...) {
    if (size() != sizeof...(T))
      throw std::runtime_error("Generic Tuple length mismatch!");
  }

  explicit Tuple(size_t size = 0) : tuple_base(sizeof...(T)) {}

  template <int I> std::tuple_element_t<I, std::tuple<T...>> get() {
    return cast_from_handle<std::tuple_element_t<I, std::tuple<T...>>>(
        tuple_base::operator[](I));
  }
};

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template <typename... T>
struct handle_type_name<pybind11_generics::Tuple<T...>> {
  static PYBIND11_DESCR name() {
    if constexpr (sizeof...(T) == 0)
      return _("Tuple[()]");
    return _("Tuple[") + concat(handle_type_name<T>::name()...) + _("]");
  }
};

} // namespace detail
} // namespace pybind11

#endif
