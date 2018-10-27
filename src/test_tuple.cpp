#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include <pybind11/stl.h>

#include <pybind11_generics/tuple.h>

#include "test_tuple.h"

namespace pyg = pybind11_generics;

class test_tuple_pair {
  private:
    std::pair<int, double> data_;

  public:
    explicit test_tuple_pair(pyg::Tuple<int, double> data) {
        data_.first = data.get<0>();
        data_.second = data.get<1>();
    }

    std::pair<int, double> get_data() { return data_; }
};

class test_tuple_tuple {
private:
    std::tuple<int, double, std::string> data_;

public:
    explicit test_tuple_tuple(pyg::Tuple<int, double, std::string> data) {
        std::get<0>(data_) = data.get<0>();
        std::get<1>(data_) = data.get<1>();
        std::get<2>(data_) = data.get<2>();
    }

    std::tuple<int, double, std::string> get_data() { return data_; }
};

void bind_test_tuple(py::module &m) {
    py::class_<test_tuple_pair>(m, "TestTuplePair")
        .def(py::init<pyg::Tuple<int, double>>(), "Initializer.")
        .def("get_data", &test_tuple_pair::get_data, "Get a copy of the data.");

    py::class_<test_tuple_tuple>(m, "TestTupleTuple")
            .def(py::init<pyg::Tuple<int, double, std::string>>(), "Initializer.")
    .def("get_data", &test_tuple_tuple::get_data, "Get a copy of the data.");
}
