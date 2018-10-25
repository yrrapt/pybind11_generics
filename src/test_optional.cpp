#include <optional>

#include <pybind11/stl.h>

#include <pybind11_generics/list.h>

#include "test_optional.h"

namespace pyg = pybind11_generics;

class test_optional {
public:
  using value_type = std::optional<pyg::List<int>>;

private:
  value_type data_;

public:
  explicit test_optional(value_type val) : data_(std::move(val)) {}

  const value_type &get_data() { return data_; }
};

void bind_test_optional(py::module &m) {
  py::class_<test_optional>(m, "TestOptional")
      .def(py::init<std::optional<pyg::List<int>>>(), "initializer.")
      .def("get_data", &test_optional::get_data, "get data.");
}
