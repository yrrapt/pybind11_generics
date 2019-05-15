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

#include <variant>

#include <pybind11/stl.h>

#include <pybind11_generics/union.h>

#include "test_union.h"

namespace pyg = pybind11_generics;

class test_union {
  public:
    using value_type = pyg::Union<py::str, py::int_, py::float_>;

  private:
    value_type data_;

  public:
    explicit test_union(value_type val) : data_(std::move(val)) {}

    const value_type &get_data() { return data_; }
    std::size_t index() { return data_.index(); }
};

void bind_test_union(py::module &m) {
    py::class_<test_union>(m, "TestUnion")
        .def(py::init<test_union::value_type>(), "Initializer.")
        .def("get_data", &test_union::get_data, "Get a copy of the data.")
        .def("index", &test_union::index);
}
