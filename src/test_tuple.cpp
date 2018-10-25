#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include <pybind11/stl.h>

#include <pybind11_generics/tuple.h>

#include "test_tuple.h"

namespace pyg = pybind11_generics;

class test_tuple {
private:
  std::pair<int, double> pair_;
  std::tuple<int, double, std::string> tuple_;

public:
  explicit test_tuple(pyg::Tuple<int, double> v1,
                      pyg::Tuple<int, double, std::string> v2) {
    pair_.first = v1.get<0>();
    pair_.second = v1.get<1>();

    std::get<0>(tuple_) = v2.get<0>();
    std::get<1>(tuple_) = v2.get<1>();
    std::get<2>(tuple_) = v2.get<2>();
  }

  pyg::Tuple<int, double> get_pair() { return py::cast(pair_); }
  pyg::Tuple<int, double, std::string> get_tuple() { return py::cast(tuple_); }
};

void bind_test_tuple(py::module &m) {
  py::class_<test_tuple>(m, "TestTuple")
      .def(py::init<pyg::Tuple<int, double>,
                    pyg::Tuple<int, double, std::string>>(),
           "initializer.")
      .def("get_pair", &test_tuple::get_pair, "Get a copy of the data.")
      .def("get_tuple", &test_tuple::get_tuple, "Get a copy of the data.");
}
