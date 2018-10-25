#include <vector>

#include <pybind11/pybind11.h>

namespace py = pybind11;

class test_list {
private:
  std::vector<int> data_;

public:
  test_list(py::list val) {
    for (const auto &obj : val) {
      data_.push_back(obj.cast<py::int_>());
    }
  }

  std::vector<int> get_data() { return data_; }
};

PYBIND11_MODULE(base, m) {
  m.doc() = "This package contains test wrapper classes for generic "
            "data types.";

  py::class_<test_list>(m, "TestList")
      .def("get_data", &test_list::get_data, "Get a copy of the data.");
}
