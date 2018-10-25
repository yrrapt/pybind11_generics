#ifndef PYBIND11_GENERICS_TUPLE_H
#define PYBIND11_GENERICS_TUPLE_H

#include <tuple>

#include <pybind11/pybind11.h>

#include <pybind11_generics/type_name.h>

namespace py = pybind11;

namespace pybind11_generics {

using tuple_base = py::tuple;

template <typename... T> class Tuple : public tuple_base {
public:
  Tuple(handle h, borrowed_t) : tuple_base(h, borrowed_t{}) { size_check(); }
  Tuple(handle h, stolen_t) : tuple_base(h, stolen_t{}) { size_check(); }
  static bool check_(handle h) {
    return h.ptr() != nullptr && PyTuple_Check(h.ptr());
  }

  /* This is deliberately not 'explicit' to allow implicit conversion from
   * object: */
  Tuple(const object &o)
      : tuple_base(check_(o) ? o.inc_ref().ptr() : PySequence_Tuple(o.ptr()),
                   stolen_t{}) {
    if (!m_ptr)
      throw py::error_already_set();
    size_check();
  }
  Tuple(object &&o)
      : tuple_base(check_(o) ? o.release().ptr() : PySequence_Tuple(o.ptr()),
                   stolen_t{}) {
    if (!m_ptr)
      throw py::error_already_set();
    size_check();
  }
  template <typename Policy_>
  Tuple(const ::pybind11::detail::accessor<Policy_> &a) : Tuple(object(a)) {}

  explicit Tuple(size_t size = 0) : tuple_base(sizeof...(T)) {}

  void size_check() {
    if (size() != sizeof...(T))
      throw std::runtime_error("Generic Tuple length mismatch!");
  }

  template <int I> std::tuple_element_t<I, std::tuple<T...>> get() {
    return tuple_base::operator[](I)
        .template cast<std::tuple_element_t<I, std::tuple<T...>>>();
  }
};

}; // namespace pybind11_generics

#endif
