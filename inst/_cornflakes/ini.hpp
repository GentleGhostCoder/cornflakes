// Copyright (c) 2022 Semjon Geist.
#ifndef INST__CORNFLAKES_INI_HPP_
#define INST__CORNFLAKES_INI_HPP_

// clang-format off
#include <algorithm>
#include <complex>
#include <map>
#include <string>
#include <utility>
#include <vector>
#include <string_operations.hpp>
#include <system_operations.hpp>
// clang-format on

namespace ini {  // cppcheck-suppress syntaxError
// constants
inline const char COMMENT_CHAR = '#';
inline const char NEWVALUE = '=';
inline const char WHITESPACE = ' ';
inline const std::string SECTION_OPEN_CHAR = "[";
inline const std::string SECTION_CLOSE_CHAR = "]";
inline const std::string BEGIN_PATTERN = '\n' + SECTION_OPEN_CHAR;
py::dict ini_load(
    const std::map<std::string, std::vector<std::string>> &files,
    const std::map<std::string, std::vector<std::string>> &sections,
    const std::map<std::string, std::vector<std::string>> &keys,
    const std::map<std::string, std::vector<py::object>> &defaults,
    const bool &eval_env);
}  // namespace ini

#endif  // INST__CORNFLAKES_INI_HPP_
