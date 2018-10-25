#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

namespace pybind11_generic {

using list_base = py::list;
template <typename T> class List : public py::list {
public:
  using list_base::list_base;
};

}; // namespace pybind11_generic

namespace pyg = pybind11_generic;

namespace pybind11 {
namespace detail {
template <typename T> struct handle_type_name<pyg::List<T>> {
  static PYBIND11_DESCR name() { return _("List[") + _<T>() + _("]"); }
};

} // namespace detail
} // namespace pybind11

class test_list {
private:
  std::vector<int> data_;

public:
  explicit test_list(pyg::List<int> val) {
    for (const auto &obj : val) {
      data_.push_back(obj.cast<int>());
    }
  }

  std::vector<int> get_data() { return data_; }
  pyg::List<int> get_py_data() { return py::cast(data_); }
};

PYBIND11_MODULE(test, m) {
  m.doc() = "This package contains test wrapper classes for generic "
            "data types.";

  py::class_<test_list>(m, "TestList")
      .def(py::init<pyg::List<int>>(), "initialize with given list.")
      .def("get_data", &test_list::get_data, "Get a copy of the data.")
      .def("get_py_data", &test_list::get_py_data, "Get a copy of the data.");
}
