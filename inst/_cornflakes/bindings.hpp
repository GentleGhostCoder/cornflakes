// Copyright (c) 2022 Semjon Geist.
#ifndef INST__CORNFLAKES_BINDINGS_HPP_
#define INST__CORNFLAKES_BINDINGS_HPP_

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// clang-format off
#include <string>
#include <vector>
#include <digest.hpp>
#include <ini.hpp>
// clang-format on

namespace py = pybind11;
#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#endif  // INST__CORNFLAKES_BINDINGS_HPP_
