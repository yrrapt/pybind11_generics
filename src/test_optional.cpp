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

#include <optional>

#include <pybind11/stl.h>

#include <pybind11_generics/list.h>
#include <pybind11_generics/optional.h>

#include "test_optional.h"

namespace pyg = pybind11_generics;

class test_optional {
  public:
    using value_type = pyg::Optional<pyg::List<int>>;

  private:
    value_type data_;

  public:
    explicit test_optional(value_type val) : data_(std::move(val)) {}

    const value_type &get_data() const { return data_; }

    bool has_value() const { return data_.has_value(); }
};

void bind_test_optional(py::module &m) {
    py::class_<test_optional>(m, "TestOptional")
        .def(py::init<pyg::Optional<pyg::List<int>>>(), "Initializer.")
        .def("get_data", &test_optional::get_data, "Get a copy of the data.")
        .def("has_value", &test_optional::has_value, "True if the given data is not None.");
}
