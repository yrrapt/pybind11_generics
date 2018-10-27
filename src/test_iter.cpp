#include <vector>
#include <utility>

#include <pybind11/stl.h>

#include <pybind11_generics/iterator.h>

#include "test_iter.h"

namespace pyg = pybind11_generics;

using vec_str = std::vector<std::string>;

class test_iter_str {
  private:
    vec_str data_;

  public:
    explicit test_iter_str(pyg::Iterator<std::string> iter) {
        for (const auto &p : iter) {
            data_.emplace_back(p);
        }
    }

    const vec_str &get_data() const { return data_; }
    pyg::Iterator<std::string> get_iter() const {
        return pyg::make_iterator(data_.cbegin(), data_.cend());
    }
};

using vec_pair = std::vector<std::pair<int, int>>;

class test_iter_pair {
private:
    vec_pair data_;

public:
    explicit test_iter_pair(pyg::Iterator<std::pair<int, int>> iter) {
        for (const auto &p : iter) {
            data_.emplace_back(p);
        }
    }

    const vec_pair &get_data() const { return data_; }
    pyg::Iterator<std::pair<int, int>> get_iter() const {
        return pyg::make_iterator(data_.cbegin(), data_.cend());
    }
};

void bind_test_iter(py::module &m) {
    pyg::declare_iterator<vec_str::const_iterator>();
    pyg::declare_iterator<vec_pair::const_iterator>();

    py::class_<test_iter_str>(m, "TestIterString")
        .def(py::init<pyg::Iterator<std::string>>(), "initializer.")
        .def("get_iter", &test_iter_str::get_iter, "Get iterator.")
        .def("get_data", &test_iter_str::get_data, "Get a copy of the data.");

    py::class_<test_iter_pair>(m, "TestIterPair")
            .def(py::init<pyg::Iterator<std::pair<int, int>>>(), "initializer.")
            .def("get_iter", &test_iter_pair::get_iter, "Get iterator.")
            .def("get_data", &test_iter_pair::get_data, "Get a copy of the data.");
}
