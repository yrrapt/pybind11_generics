#include <variant>

#include <pybind11/stl.h>

#include <pybind11_generics/union.h>

#include "test_union.h"

namespace pyg = pybind11_generics;

class test_union {
  public:
    using value_type = pyg::Union<py::str, py::int_, py::float_>;

  private:
    value_type data_;

  public:
    explicit test_union(value_type val) : data_(std::move(val)) {}

    const value_type &get_data() { return data_; }
    std::size_t index() { return data_.index(); }
};

void bind_test_union(py::module &m) {
    py::class_<test_union>(m, "TestUnion")
        .def(py::init<test_union::value_type>(), "initializer.")
        .def("get_data", &test_union::get_data, "get data.")
        .def("index", &test_union::index);
}
