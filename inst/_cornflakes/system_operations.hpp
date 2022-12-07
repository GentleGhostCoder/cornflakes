// Copyright (c) 2022 Semjon Geist.

#ifndef INST__CORNFLAKES_SYSTEM_OPERATIONS_HPP_
#define INST__CORNFLAKES_SYSTEM_OPERATIONS_HPP_

#include <sys/stat.h>

#include <algorithm>
#include <cstring>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

namespace system_operations {  // cppcheck-suppress syntaxError

// Constants
// System-Line-Seperator
#ifdef _WIN32
#include <direct.h>  // make_directory
inline const char *LINE_SEPERATOR = "\r\n";
#elif defined macintosh  // OS 9
inline const char *LINE_SEPERATOR = "\r";
#else
inline const char *LINE_SEPERATOR = "\n";  // Mac OS X uses \n
#endif

// System-File-Seperator
#ifdef _WIN32
inline const char FILE_SEPERATOR = '\\';
#else
inline const char FILE_SEPERATOR = '/';  // Mac OS X uses \n
#endif

inline const char NEWLINE = LINE_SEPERATOR[std::strlen(LINE_SEPERATOR) - 1];
bool exists(const std::string &path);
bool dir_exists(const std::string &path);
bool file_exists(const std::string &path);
int make_directory(const char *path);
std::string path_exanduser(std::string value);
std::string read_file(const std::string &file);

}  // namespace system_operations

#endif  // INST__CORNFLAKES_SYSTEM_OPERATIONS_HPP_
