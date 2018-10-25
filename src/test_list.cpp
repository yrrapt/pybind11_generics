#include <iostream>
#include <iterator>
#include <typeinfo>
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <pybind11_generics/list.h>

namespace py = pybind11;

namespace pyg = pybind11_generic;

class test_list {
private:
  std::vector<int> data_;

public:
  explicit test_list(pyg::List<int> val) {
    data_.reserve(val.size());
    data_.insert(data_.end(), val.begin(), val.end());
  }

  std::vector<int> get_data() { return data_; }
  pyg::List<int> get_py_data() { return py::cast(data_); }
};

PYBIND11_MODULE(test, m) {
  m.doc() = "This package contains test wrapper classes for generic "
            "data types.";

  py::class_<test_list>(m, "TestList")
      .def(py::init<pyg::List<int>>(), "initialize with given list.")
      .def("get_data", &test_list::get_data, "Get a copy of the data.")
      .def("get_py_data", &test_list::get_py_data, "Get a copy of the data.");
}
