#include <iostream>
#include <vector>

#include <pybind11/stl.h>

#include <pybind11_generics/list.h>

#include "test_list.h"

namespace pyg = pybind11_generics;

class test_list {
  private:
    std::vector<int> data_;

  public:
    explicit test_list(pyg::List<py::int_> val) {
        data_.reserve(val.size());
        data_.insert(data_.end(), val.begin(), val.end());
        if (val.size() > 0)
            data_[0] = val[0];
    }

    test_list(const test_list &rhs) : data_(rhs.data_) {}
    test_list(test_list &&rhs) : data_(std::move(rhs.data_)) {}
    test_list &operator=(const test_list &rhs) {
        data_ = rhs.data_;
        return *this;
    }
    test_list &operator=(test_list &&rhs) {
        data_ = std::move(rhs.data_);
        return *this;
    }

    ~test_list() { std::cout << "Deleting test_list" << std::endl; }

    std::vector<int> get_data() const noexcept { return data_; }
};

std::vector<int> get_list(const test_list &obj) { return obj.get_data(); }

class list_holder {
  private:
    const test_list *obj;

  public:
    explicit list_holder(const test_list *obj) : obj(obj) {}

    const test_list &get_obj_ref() { return *obj; }
    const test_list *get_obj_ptr() { return obj; }

    std::vector<int> get_data() { return obj->get_data(); }
};

void bind_test_list(py::module &m) {
    m.def("get_list", &get_list, "Returns the data associated with the given object.",
          py::arg("obj"));

    py::class_<test_list>(m, "TestList")
        .def(py::init<pyg::List<py::int_>>(), "Initializer.")
        .def("get_data", &test_list::get_data, "Get a copy of the data.");

    py::class_<list_holder>(m, "ListHolder")
        .def(py::init<const test_list *>(), "Initializer.")
        .def("get_obj_ref", &list_holder::get_obj_ref, "Get the underlying object as reference.")
        .def("get_obj_ptr", &list_holder::get_obj_ptr, "Get the underlying object as pointer.")
        .def("get_data", &list_holder::get_data, "Get a copy of the data.");
}
