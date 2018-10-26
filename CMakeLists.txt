# Version 3.8 required because of C++17 support.
cmake_minimum_required(VERSION 3.1)
project(pybind11_generics)

# Check if pybind11 is being used directly or via add_subdirectory
set(PYBIND11_GENERICS_MASTER_PROJECT OFF)
if (CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
  set(PYBIND11_GENERICS_MASTER_PROJECT ON)
endif()

option(PYBIND11_GENERICS_TEST "Build pybind11_generics test suite?"
  ${PYBIND11_GENERICS_MASTER_PROJECT})

# Boost Spirit X3 requires C++14
# __has_include directive requires C++17
# std::variant requires C++17
# map::extract (use of node handles) requires C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# control compiler warnings
add_compile_options(-fexceptions)
add_compile_options(-g)
add_compile_options(-Wall)
add_compile_options(-Wno-delete-non-virtual-dtor)
# add_compile_options(-Wno-logical-op-parentheses)
# add_compile_options(-Wno-new-returns-null)
# set optimzation level for release
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
# generate compilation commands file for emacs
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# prefer pthreads
set(THREADS_PREFER_PTHREAD_FLAG ON)

# make sure linker raise errors if shared library has undefined symbols
# this makes it a lot easier to debug
set(CMAKE_SHARED_LINKER_FLAGS "-Wl,--no-undefined")
# add rpaths to the final install executable
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

# Must use GNUInstallDirs to install libraries into correct
# locations on all platforms.
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

# Include pybind11
# enable C++17 support for variant/optional wrapping
set(PYBIND11_CPP_STANDARD --std=c++1z)
add_subdirectory(pybind11)

# Define pybind11_generics interface library
add_library(pybind11_generics INTERFACE)
target_link_libraries(pybind11_generics INTERFACE pybind11::module)
target_include_directories(pybind11_generics INTERFACE include/)
target_sources(pybind11_generics INTERFACE
  ${CMAKE_CURRENT_SOURCE_DIR}/include/pybind11_generics/list.h
)

if (PYBIND11_GENERICS_TEST)
  add_subdirectory(src)
endif()
