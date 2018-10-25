#ifndef PYBIND11_GENERICS_UNION_H
#define PYBIND11_GENERICS_UNION_H

#include <optional>
#include <variant>

#include <string>

#include <pybind11_generics/cast.h>
#include <pybind11_generics/type_name.h>

namespace py = pybind11;

namespace pybind11_generics {

using union_base = py::object;

template <typename... T> class Union : public union_base {
private:
  mutable std::optional<std::size_t> index_;

  template <typename... U> struct type_list {};

  template <typename U, typename... Us>
  static std::optional<std::size_t>
  find_index(handle src, std::size_t cur, bool convert, type_list<U, Us...>) {
    auto caster = py::detail::make_caster<U>();
    if (caster.load(src, convert))
      return cur;
    return find_index(src, cur + 1, convert, type_list<Us...>{});
  }

  static std::optional<std::size_t> find_index(handle, std::size_t, bool,
                                               type_list<>) {
    return {};
  }

  static std::optional<std::size_t> find_index(const handle &src) {
    // Do a first pass without conversions to improve constructor resolution.
    // E.g. `py::int_(1).cast<variant<double, int>>()` needs to fill the `int`
    // slot of the variant. Without two-pass loading `double` would be filled
    // because it appears first and a conversion is possible.
    auto tmp = find_index(src, 0, false, type_list<T...>{});
    return (tmp.has_value()) ? tmp
                             : find_index(src, 0, true, type_list<T...>{});
  }

public:
  static bool check_(const handle &h) { return find_index(h).has_value(); }

  template <class... Args>
  Union(Args &&... args) : union_base(std::forward<Args>(args)...), index_{} {}

  std::size_t index() const {
    if (index_.has_value())
      return index_.value();
    index_ = find_index(*this);
    if (!index_.has_value())
      throw std::runtime_error("Invalid union data type.");
    return index_.value();
  }

  template <std::size_t I>
  std::variant_alternative_t<I, std::variant<T...>> get() {
    if (I != index())
      throw std::bad_variant_access("Accessing invalid value in union.");
    return cast_from_handle<std::variant_alternative_t<I, std::variant<T...>>>(
        py::handle(ptr()));
  }
};

} // namespace pybind11_generics

namespace pybind11 {
namespace detail {

template <typename T> struct handle_type_name<pybind11_generics::Union<T>> {
  static PYBIND11_DESCR name() {
    return _("Union[") + handle_type_name<T>::name() + _("]");
  }
};

} // namespace detail
} // namespace pybind11

#endif
