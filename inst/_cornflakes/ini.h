// Copyright (c) 2022 Semjon Geist.

#ifndef INST__CORNFLAKES_INI_H_
#define INST__CORNFLAKES_INI_H_

#include <string_operations.h>
#include <system_operations.h>

#include <algorithm>
#include <map>
#include <string>
#include <vector>

namespace ini {
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

#endif  // INST__CORNFLAKES_INI_H_
