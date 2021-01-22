
# Version 3.15 required because of FindPython module.
cmake_minimum_required(VERSION 3.15)

project(pybind11_generics)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# set(CMAKE_VERBOSE_MAKEFILE ON)

# set compile options
add_compile_options(
  "-fmax-errors=2" "-Wall" "-pedantic"
  "$<$<CONFIG:DEBUG>:-fno-omit-frame-pointer>"
)

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

# Call FindPython
find_package(Python COMPONENTS Development REQUIRED)

# Include pybind11
add_subdirectory(pybind11)

# Define pybind11_generics interface library
add_library(pybind11_generics INTERFACE)

target_link_libraries(pybind11_generics
  INTERFACE
  pybind11::module
  )

target_include_directories(pybind11_generics
  INTERFACE
  ${CMAKE_CURRENT_SOURCE_DIR}/include
  )
