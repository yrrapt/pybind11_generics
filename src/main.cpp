
#include "move_cast.h"
#include "test_any.h"
#include "test_dict.h"
#include "test_iter.h"
#include "test_iterable.h"
#include "test_list.h"
#include "test_optional.h"
#include "test_tuple.h"
#include "test_union.h"

PYBIND11_MODULE(pyg_test, m) {
    m.doc() = "This package contains test wrapper classes for generic "
              "data types.";

    bind_test_list(m);
    bind_test_any(m);
    bind_test_tuple(m);
    bind_test_dict(m);
    bind_test_union(m);
    bind_test_optional(m);
    bind_test_iter(m);
    bind_test_iterable(m);
    bind_move_cast(m);
}
