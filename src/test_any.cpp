#include <vector>

#include <pybind11/stl.h>

#include <pybind11_generics/any.h>
#include <pybind11_generics/list.h>

#include "test_any.h"

namespace py = pybind11;

namespace pyg = pybind11_generics;

class test_any_list {
  private:
    std::vector<pyg::Any> data_;

  public:
    test_any_list(pyg::List<pyg::Any> data) {
        data_.reserve(data.size());
        data_.insert(data_.end(), data.begin(), data.end());
    }

    pyg::List<pyg::Any> get_data() { return py::cast(data_); }
};

class test_any_val {
private:
    pyg::Any data_;

public:
    test_any_val(pyg::Any data) : data_(std::move(data)) {}

    pyg::Any get_data() { return data_; }
};

void bind_test_any(py::module &m) {
    py::class_<test_any_list>(m, "TestAnyList")
        .def(py::init<pyg::List<pyg::Any>>(), "Initializer.")
        .def("get_data", &test_any_list::get_data, "Get a copy of the data.");
    py::class_<test_any_val>(m, "TestAnyVal")
            .def(py::init<pyg::Any>(), "Initializer.")
            .def("get_data", &test_any_val::get_data, "Get a copy of the data.");
}
