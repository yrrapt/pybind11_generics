
#include "test_any.h"
#include "test_list.h"
#include "test_tuple.h"


PYBIND11_MODULE(test, m) {
  m.doc() = "This package contains test wrapper classes for generic "
            "data types.";

  bind_test_list(m);
  bind_test_any(m);
  bind_test_tuple(m);
}
