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

#include <iostream>
#include <vector>

#include <pybind11/stl.h>

#include <pybind11_generics/sequence.h>

#include "test_sequence.h"

namespace pyg = pybind11_generics;

class test_sequence {
  private:
    std::vector<int> data_;

  public:
    explicit test_sequence(pyg::Sequence<py::int_> val) {
        data_.reserve(val.size());
        data_.insert(data_.end(), val.begin(), val.end());
        if (val.size() > 0)
            data_[0] = val[0];
    }

    test_sequence(const test_sequence &rhs) : data_(rhs.data_) {}
    test_sequence(test_sequence &&rhs) : data_(std::move(rhs.data_)) {}
    test_sequence &operator=(const test_sequence &rhs) {
        data_ = rhs.data_;
        return *this;
    }
    test_sequence &operator=(test_sequence &&rhs) {
        data_ = std::move(rhs.data_);
        return *this;
    }

    ~test_sequence() { std::cout << "Deleting test_sequence" << std::endl; }

    std::vector<int> get_data() const noexcept { return data_; }
};

std::vector<int> get_sequence(const test_sequence &obj) { return obj.get_data(); }

void bind_test_sequence(py::module &m) {
    m.def("get_sequence", &get_sequence, "Returns the data associated with the given object.",
          py::arg("obj"));

    py::class_<test_sequence>(m, "TestSequence")
        .def(py::init<pyg::Sequence<py::int_>>(), "Initializer.")
        .def("get_data", &test_sequence::get_data, "Get a copy of the data.");
}
