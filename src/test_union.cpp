#include <variant>

#include <pybind11/stl.h>

#include "test_union.h"

class test_union {
public:
  using value_type = std::variant<std::string, int, double>;

private:
  value_type data_;

public:
  explicit test_union(value_type val) : data_(std::move(val)) {}

  const value_type &get_data() { return data_; }
};

void bind_test_union(py::module &m) {
  py::class_<test_union>(m, "TestUnion")
      .def(py::init<std::variant<std::string, int, double>>(), "initializer.")
      .def("get_data", &test_union::get_data, "get data.");
}
