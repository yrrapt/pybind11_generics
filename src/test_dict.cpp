#include <map>

#include <pybind11/stl.h>

#include <pybind11_generics/dict.h>

#include "test_dict.h"

namespace pyg = pybind11_generics;

class test_dict {
  private:
    std::map<std::string, int> data_;

  public:
    explicit test_dict(pyg::Dict<std::string, int> val) { data_.insert(val.begin(), val.end()); }

    pyg::Dict<std::string, int> get_data() { return py::cast(data_); }
};

void bind_test_dict(py::module &m) {
    py::class_<test_dict>(m, "TestDict")
        .def(py::init<pyg::Dict<std::string, int>>(), "Initializer.")
        .def("get_data", &test_dict::get_data, "Get a copy of the data.");
}
