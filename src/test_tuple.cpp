#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include <pybind11/stl.h>

#include "test_tuple.h"

class test_tuple {
private:
  std::pair<int, double> pair_;
  std::tuple<int, double, std::string> tuple_;

public:
  explicit test_tuple(py::tuple v1, py::tuple v2) {
    pair_.first = v1[0].cast<int>();
    pair_.second = v1[1].cast<double>();

    std::get<0>(tuple_) = v2[0].cast<int>();
    std::get<1>(tuple_) = v2[1].cast<double>();
    std::get<2>(tuple_) = v2[2].cast<std::string>();
  }

  py::tuple get_pair() { return py::cast(pair_); }
  py::tuple get_tuple() { return py::cast(tuple_); }
};

void bind_test_tuple(py::module &m) {
  py::class_<test_tuple>(m, "TestTuple")
      .def(py::init<py::tuple, py::tuple>(), "initializer.")
      .def("get_pair", &test_tuple::get_pair, "Get a copy of the data.")
      .def("get_tuple", &test_tuple::get_tuple, "Get a copy of the data.");
}
