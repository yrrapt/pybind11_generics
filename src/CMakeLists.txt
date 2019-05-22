set(SRC_FILES_TEST
  ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/move_cast.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/test_any.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/test_dict.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/test_iter.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/test_iterable.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/test_list.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/test_optional.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/test_tuple.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/test_union.cpp
  )

pybind11_add_module(pyg_test ${SRC_FILES_TEST})

target_include_directories(pyg_test
  PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}
  )

target_link_libraries(pyg_test
  PRIVATE
  pybind11_generics
  )
