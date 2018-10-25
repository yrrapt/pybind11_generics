#include <vector>

#include <pybind11/stl.h>

#include <pybind11_generics/any.h>
#include <pybind11_generics/list.h>

#include "test_any.h"

namespace py = pybind11;

namespace pyg = pybind11_generic;

class test_any {
private:
  pyg::Any val_;
  std::vector<pyg::Any> data_;

public:
  test_any(pyg::List<pyg::Any> data, pyg::Any val) : val_(std::move(val)) {
    data_.reserve(data.size());
    data_.insert(data_.end(), data.begin(), data.end());
  }

  pyg::List<pyg::Any> get_py_data() { return py::cast(data_); }
  pyg::Any get_val() { return val_; }
};

void bind_test_any(py::module &m) {
  py::class_<test_any>(m, "TestAny")
      .def(py::init<pyg::List<pyg::Any>, pyg::Any>(), "initializer.")
      .def("get_py_data", &test_any::get_py_data, "Get List[Any].")
      .def("get_val", &test_any::get_val, "Get Any.");
}
