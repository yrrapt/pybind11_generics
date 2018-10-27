#include <vector>

#include <pybind11/stl.h>

#include <pybind11_generics/list.h>

#include "test_list.h"

namespace pyg = pybind11_generics;

class test_list {
  private:
    std::vector<int> data_;

  public:
    explicit test_list(pyg::List<py::int_> val) {
        data_.reserve(val.size());
        data_.insert(data_.end(), val.begin(), val.end());
        if (val.size() > 0)
            data_[0] = val[0];
    }

    std::vector<int> get_data() { return data_; }
};

void bind_test_list(py::module &m) {
    py::class_<test_list>(m, "TestList")
        .def(py::init<pyg::List<py::int_>>(), "Initializer.")
        .def("get_data", &test_list::get_data, "Get a copy of the data.");
}
