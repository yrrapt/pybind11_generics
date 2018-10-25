include_directories(${CMAKE_CURRENT_SOURCE_DIR})

set(SRC_FILES_TEST
  ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/test_any.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/test_list.cpp
  )

pybind11_add_module(test ${SRC_FILES_TEST})

target_link_libraries(test
  PRIVATE
  pybind11_generics
  )
