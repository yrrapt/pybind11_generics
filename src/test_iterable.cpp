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

#include <pybind11_generics/iterable.h>

#include "test_iterable.h"

namespace pyg = pybind11_generics;

using vec_str = std::vector<std::string>;

template <class T> class test_iterable {
  public:
    using value_type = T;
    using vector_type = std::vector<value_type>;

  private:
    vector_type data_;

  public:
    explicit test_iterable(pyg::Iterable<value_type> iter) {
        for (const auto &p : iter) {
            data_.emplace_back(p);
        }
    }

    const vector_type &get_data() const { return data_; }
};

void bind_test_iterable(py::module &m) {
    py::class_<test_iterable<std::string>>(m, "TestIterableString")
        .def(py::init<pyg::Iterable<std::string>>(), "Initializer.")
        .def("get_data", &test_iterable<std::string>::get_data, "Get a copy of the data.");
    py::class_<test_iterable<std::pair<int, int>>>(m, "TestIterablePair")
        .def(py::init<pyg::Iterable<std::pair<int, int>>>(), "Initializer.")
        .def("get_data", &test_iterable<std::pair<int, int>>::get_data, "Get a copy of the data.");
}
