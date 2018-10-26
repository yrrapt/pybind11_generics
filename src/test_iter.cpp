#include <vector>

#include <pybind11_generics/iterator.h>

#include "test_iter.h"

namespace pyg = pybind11_generics;

using vec_type = std::vector<std::string>;

class test_iter {
  private:
    vec_type data_;

  public:
    explicit test_iter(pyg::Iterator<std::string> iter) {
        for (const auto &p : iter) {
            data_.emplace_back(p);
        }
    }

    const vec_type &get_data() const { return data_; }
    pyg::Iterator<std::string> get_iter() const {
        return pyg::make_iterator(data_.cbegin(), data_.cend());
    }
};

void bind_test_iter(py::module &m) {
    pyg::declare_iterator<vec_type::const_iterator, vec_type::const_iterator>();

    py::class_<test_iter>(m, "TestIter")
        .def(py::init<pyg::Iterator<std::string>>(), "initializer.")
        .def("get_iter", &test_iter::get_iter, "Get iterator.")
        .def("get_data", &test_iter::get_data, "Get a copy of the data.");
}
