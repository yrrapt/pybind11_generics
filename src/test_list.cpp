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

    std::vector<int> get_data() const noexcept { return data_; }
};

std::vector<int> get_list(const test_list &obj) { return obj.get_data(); }

void bind_test_list(py::module &m) {
    m.def("get_list", &get_list, "Returns the data associated with the given object.",
          py::arg("obj"));
    py::class_<test_list>(m, "TestList")
        .def(py::init<pyg::List<py::int_>>(), "Initializer.")
        .def("get_data", &test_list::get_data, "Get a copy of the data.");
}
