/*
   Copyright 2018 Eric Chang

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

#include <utility>
#include <vector>

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
        .def(py::init<pyg::Iterator<std::string>>(), "Initializer.")
        .def("get_iter", &test_iter_str::get_iter, "Get iterator.")
        .def("get_data", &test_iter_str::get_data, "Get a copy of the data.");

    py::class_<test_iter_pair>(m, "TestIterPair")
        .def(py::init<pyg::Iterator<std::pair<int, int>>>(), "Initializer.")
        .def("get_iter", &test_iter_pair::get_iter, "Get iterator.")
        .def("get_data", &test_iter_pair::get_data, "Get a copy of the data.");
}
