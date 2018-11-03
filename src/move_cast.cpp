#include <iostream>
#include <string>
#include <vector>

#include <pybind11/stl.h>

#include <pybind11_generics/list.h>

#include <move_cast.h>

namespace py = pybind11;

namespace pyg = pybind11_generics;

class data {
  private:
    int a_;
    std::string b_;
    std::vector<int> c_;

  public:
    data(int a, std::string b, pyg::List<int> c) : a_(a), b_(std::move(b)) {
        c_.reserve(c.size());
        c_.insert(c_.end(), c.begin(), c.end());
        std::cout << "data normal constructor called." << std::endl;
    }

    data(const data &other) : a_(other.a_), b_(other.b_), c_(other.c_) {
        std::cout << "data copy constructor called." << std::endl;
    }

    data(data &&other) : a_(other.a_), b_(std::move(other.b_)), c_(std::move(other.c_)) {
        std::cout << "data move constructor called." << std::endl;
    }

    int a() const { return a_; }

    std::string b() const { return b_; }

    std::vector<int> c() const { return c_; }

    void append(int val) { c_.push_back(val); }
};

class factory {
  private:
    data data_;

  public:
    factory(int a, std::string b, pyg::List<int> c) : data_(a, std::move(b), std::move(c)) {}

    int a() const { return data_.a(); }

    std::string b() const { return data_.b(); }

    std::vector<int> c() const { return data_.c(); }

    data get_default_cpp() const { return data_; }
    py::object get_default_copy() const { return py::cast(data_); }
    py::object get_default_move() const { return py::cast(std::move(data_)); }
    py::object get_default_move2() const {
        return py::cast(std::move(data_), py::return_value_policy::move);
    }
};

void bind_move_cast(py::module &m) {
    py::class_<data>(m, "Data")
        .def(py::init<int, std::string, pyg::List<int>>(), "Initializer.")
        .def("a", &data::a)
        .def("b", &data::b)
        .def("c", &data::c)
        .def("append", &data::append);
    py::class_<factory>(m, "Factory")
        .def(py::init<int, std::string, pyg::List<int>>(), "Initializer.")
        .def("a", &factory::a)
        .def("b", &factory::b)
        .def("c", &factory::c)
        .def("get_default_cpp", &factory::get_default_cpp)
        .def("get_default_copy", &factory::get_default_copy)
        .def("get_default_move", &factory::get_default_move)
        .def("get_default_move2", &factory::get_default_move2);
}
