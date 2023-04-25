// Copyright (c) 2022 Semjon Geist.
#include <ini.hpp>

//! Collection of structs and functions to parse ini files
namespace ini {

// Parser Config (User-Input)
struct ParserConfig {
  std::map<std::string, std::vector<std::string>> files;
  std::map<std::string, std::vector<std::string>> sections;
  std::map<std::string, std::vector<std::string>> keys;
  std::map<std::string, std::vector<py::object>> defaults;
  py::dict envir;  // MAIN ENVIRONMENT for configs
  ParserConfig(std::map<std::string, std::vector<std::string>> t_files,
               std::map<std::string, std::vector<std::string>> t_sections,
               std::map<std::string, std::vector<std::string>> t_keys,
               std::map<std::string, std::vector<py::object>> t_defaults,
               py::dict t_envir)
      : files(std::move(t_files)),
        sections(std::move(t_sections)),
        keys(std::move(t_keys)),
        defaults(std::move(t_defaults)),
        envir(std::move(t_envir)) {}
};

// Input File Data
struct FileData {
  py::dict file_envir;   // File ENVIRONMENT for configs
  std::string contents;  // content read into
  FileData(py::dict t_file_envir, std::string t_contents)
      : file_envir(std::move(t_file_envir)), contents(std::move(t_contents)) {}
};

// Section Meta Data
struct SectionData {
  py::dict section_envir;             // Section ENVIRONMENT for configs
  std::array<int, 2> section_cursor;  // section id / idx-begin idx-end
  FileData m_FileData;
  SectionData(py::dict t_section_envir, std::array<int, 2> t_section_cursor,
              FileData t_FileData)
      : section_envir(std::move(t_section_envir)),
        section_cursor(t_section_cursor),
        m_FileData(std::move(t_FileData)) {}
};

// Parser Process Data
struct ParserData {
  std::function<void(FileData data, ParserData m_ParserData)> ParseSections;
  std::function<void(SectionData data, ParserData m_ParserData)> ParseKeys;
  ParserConfig m_ParserConfig;
  const bool eval_env;
  ParserData(std::function<void(FileData data, ParserData m_ParserData)>
                 t_ParseSections,
             std::function<void(SectionData data, ParserData m_ParserData)>
                 t_ParseKeys,
             ParserConfig t_ParserConfig, const bool &t_eval_env)
      : ParseSections(std::move(t_ParseSections)),
        ParseKeys(std::move(t_ParseKeys)),
        m_ParserConfig(std::move(t_ParserConfig)),
        eval_env(t_eval_env) {}
};

inline void ParseAllKeys(SectionData t_SectionData,
                         const ParserData &t_ParserData) {
  std::string::const_iterator start_iter =
      t_SectionData.m_FileData.contents.begin();
  std::string::const_iterator end_iter =
      t_SectionData.m_FileData.contents.begin();

  std::advance(start_iter, t_SectionData.section_cursor[0]);
  std::advance(end_iter, t_SectionData.section_cursor[1]);
  start_iter =
      std::find(start_iter, end_iter,
                system_operations::NEWLINE);  // next line after section header

  std::string::const_iterator next_line_iter =
      std::find(start_iter, end_iter, system_operations::NEWLINE);
  std::string::const_iterator next_value_iter;

  // // split name and value for each line if not empty or comment
  while (next_line_iter != end_iter) {
    start_iter = next_line_iter + 1;  // skip line

    next_line_iter =
        std::find(start_iter, end_iter, system_operations::NEWLINE);
    next_line_iter = std::find(start_iter, next_line_iter, COMMENT_CHAR);
    next_value_iter = std::find(start_iter, next_line_iter, NEWVALUE);

    //            if () {
    //                break;
    //            }

    if (start_iter == next_value_iter) continue;

    std::string value = string_operations::trim(
        std::string(next_value_iter, next_line_iter).erase(0, 1));
    if (!value.empty())
      t_SectionData.section_envir[py::cast(string_operations::trim(std::string(
          start_iter, next_value_iter)))] = string_operations::eval_type(value);
  }
}

inline void ParseDefinedKeys(SectionData t_SectionData,
                             const ParserData &t_ParserData) {
  for (const auto &item : t_ParserData.m_ParserConfig.keys) {
    for (auto item_value : item.second) {
      int type = 0;  // default, 1=list, 2=dict
      std::string::const_iterator start_iter =
          t_SectionData.m_FileData.contents.begin();
      std::string::const_iterator end_iter =
          t_SectionData.m_FileData.contents.begin();
      std::advance(start_iter, t_SectionData.section_cursor[0]);
      std::advance(end_iter, t_SectionData.section_cursor[1]);

      std::string::const_iterator line_iter;
      std::string::const_iterator value_iter = std::find(
          start_iter, end_iter,
          system_operations::NEWLINE);  // next line after section header

      if (item_value == "*") {
        type = 1;
        item_value = item.first;
      }
      if (item_value == "**") {
        type = 2;
        item_value = item.first;
      }

      while (true) {
        // get value
        start_iter = std::search(value_iter, end_iter, item_value.begin(),
                                 item_value.end());
        if (start_iter == end_iter) {
          if (!t_SectionData.section_envir
                   .attr("get")(py::cast(item.first), py::none())
                   .is_none()) {
            break;
          }
          if (t_ParserData.eval_env) {
            char *env_value = std::getenv(item_value.c_str());
            if (env_value == nullptr) {
              std::transform(item_value.begin(), item_value.end(),
                             item_value.begin(), ::toupper);
              env_value = std::getenv(item_value.c_str());
            }
            if (env_value != nullptr) {
              t_SectionData.section_envir[py::cast(item.first)] =
                  t_SectionData.section_envir.attr("get")(
                      py::cast(item.first),
                      string_operations::eval_type(env_value));
              break;
            }
          }
          if (!t_ParserData.m_ParserConfig.defaults.empty()) {
            auto default_value =
                t_ParserData.m_ParserConfig.defaults.find(item.first);
            if (default_value != t_ParserData.m_ParserConfig.defaults.end()) {
              if (!default_value->second.empty()) {
                t_SectionData.section_envir[py::cast(item.first)] =
                    t_SectionData.section_envir.attr("get")(
                        py::cast(item.first), default_value->second[0]);
                break;
              }
              t_SectionData.section_envir[py::cast(item.first)] =
                  t_SectionData.section_envir.attr("get")(py::cast(item.first),
                                                          py::none());
            }
          }
          break;
        }

        line_iter =
            std::find(start_iter + 1, end_iter, system_operations::NEWLINE);
        value_iter = std::find(start_iter + 1, line_iter, NEWVALUE);

        // get total key name if only prefix
        while (true) {
          if (type || std::string(start_iter - 1, start_iter).c_str()[0] ==
                          system_operations::NEWLINE)
            break;
          --start_iter;
        }

        std::string value = string_operations::trim(
            std::string(value_iter, line_iter).erase(0, 1));

        if (!value.empty()) {
          switch (type) {
            case 1: {
              t_SectionData.section_envir[py::cast(item.first)] =
                  t_SectionData.section_envir.attr("get")(py::cast(item.first),
                                                          py::list());
              t_SectionData.section_envir[py::cast(item.first)].attr("append")(
                  string_operations::eval_type(value));
            } break;
            case 2: {
              t_SectionData.section_envir[py::cast(item.first)] =
                  t_SectionData.section_envir.attr("get")(py::cast(item.first),
                                                          py::dict());
              t_SectionData.section_envir[py::cast(item.first)][py::cast(
                  std::string(start_iter, value_iter))] =
                  string_operations::eval_type(value);
            } break;
            default: {
              if (string_operations::trim(
                      std::string(start_iter, value_iter)) != item_value)
                continue;
              t_SectionData.section_envir[py::cast(item.first)] =
                  string_operations::eval_type(value);
            } break;
          }
          continue;
        }

        start_iter += 1;
      }
    }
  }
}

inline int GetNextSectionIdx(FileData t_FileData, int idx) {
  idx = static_cast<int>(
      t_FileData.contents.find_first_of(SECTION_OPEN_CHAR, idx) + 1);
  while (idx && t_FileData.contents.at(idx - 2) != system_operations::NEWLINE) {
    idx = static_cast<int>(
        t_FileData.contents.find_first_of(SECTION_OPEN_CHAR, idx) + 1);
  }
  if (!idx) {
    idx = static_cast<int>(t_FileData.contents.size() - 1);
  }
  return idx;
}

inline void ParseSectionsDefault(FileData t_FileData,
                                 const ParserData &t_ParserData,
                                 py::dict section_envir,
                                 bool defaults_only = false,
                                 bool first_section_only = false) {
  std::array<int, 2> section_cursor{};
  t_FileData.contents.insert(0, 1, system_operations::NEWLINE);
  section_cursor[0] = static_cast<int>(
      defaults_only * static_cast<int>(t_FileData.contents.size()));
  section_cursor[1] = GetNextSectionIdx(
      t_FileData, first_section_only
                      ? GetNextSectionIdx(t_FileData, section_cursor[0])
                      : static_cast<int>(t_FileData.contents.size() - 1));
  // parse all keys in all sections for config without section
  t_ParserData.ParseKeys(
      SectionData(std::move(section_envir),  // Section Environment
                  section_cursor,            // Cursor for content
                  t_FileData),               // Parent ini data
      t_ParserData);
}

// parse all sections
inline void ParseAllSections(const FileData &t_FileData,
                             const ParserData &t_ParserData) {
  std::array<int, 2> section_cursor{};
  section_cursor[1] = (t_FileData.contents.empty() ||
                       t_FileData.contents.at(0) == SECTION_OPEN_CHAR.at(0))
                          ? 1
                          : GetNextSectionIdx(t_FileData, 0);

  if (section_cursor[1] >= static_cast<int>(t_FileData.contents.size() - 1)) {
    t_FileData.file_envir[py::none()] = py::dict();
    ParseSectionsDefault(t_FileData, t_ParserData,
                         t_FileData.file_envir[py::none()],
                         t_FileData.contents.empty());
    return;
  }
  // split name and value for each line if not empty or comment
  while (true) {
    section_cursor[0] = static_cast<int>(t_FileData.contents.find_first_of(
        SECTION_CLOSE_CHAR, section_cursor[1]));

    std::string section_name = t_FileData.contents.substr(
        section_cursor[1], section_cursor[0] - section_cursor[1]);

    t_FileData.file_envir[py::cast(section_name)] =
        t_FileData.file_envir.attr("get")(py::cast(section_name), py::dict());

    section_cursor[1] = GetNextSectionIdx(t_FileData, section_cursor[1]);

    if (section_cursor[1] == static_cast<int>(t_FileData.contents.size() - 1)) {
      t_ParserData.ParseKeys(
          SectionData(
              t_FileData
                  .file_envir[py::cast(section_name)],  // Section Environment
              section_cursor,                           // Cursor for content
              t_FileData),                              // Parent ini data
          t_ParserData);
      break;
    }

    t_ParserData.ParseKeys(
        SectionData(
            t_FileData
                .file_envir[py::cast(section_name)],  // Section Environment
            section_cursor,                           // Cursor for content
            t_FileData),                              // Parent ini data
        t_ParserData);
  }
}

inline void ParseDefinedSections(FileData t_FileData,
                                 const ParserData &t_ParserData) {
  for (const auto &item : t_ParserData.m_ParserConfig.sections) {
    py::dict section_envir;
    if (string_operations::is_nan(item.first)) {
      section_envir = t_FileData.file_envir;
    } else {
      t_FileData.file_envir[py::cast(item.first)] =
          t_FileData.file_envir.attr("get")(py::cast(item.first), py::dict());
      section_envir = t_FileData.file_envir[py::cast(item.first)];
    }
    if (item.second.empty()) {
      if (string_operations::is_nan(item.first)) {
        ParseSectionsDefault(t_FileData, t_ParserData, section_envir, false,
                             true);
        continue;
      }
      ParseSectionsDefault(t_FileData, t_ParserData, section_envir);
      continue;
    }

    for (const auto &item_value : item.second) {
      // config.begin_pattern is section name + pattern
      std::array<int, 2> section_cursor = string_operations::idx_between(
          t_FileData.contents.begin(), t_FileData.contents.end(),
          SECTION_OPEN_CHAR + item_value + SECTION_CLOSE_CHAR, BEGIN_PATTERN,
          0);

      if (section_cursor == string_operations::empty_idx) {
        // handling if section not found or has no section
        if (!string_operations::is_nan(item_value)) {
          continue;
        }
        if (string_operations::is_nan(item.first)) {
          ParseSectionsDefault(t_FileData, t_ParserData, section_envir, false,
                               true);
          continue;
        }
        ParseSectionsDefault(t_FileData, t_ParserData, section_envir);
        continue;
      }

      section_cursor[0] += static_cast<int>(item_value.size() + 1);
      section_cursor[1] -= static_cast<int>(BEGIN_PATTERN.size() - 1);

      // parse all keys
      t_ParserData.ParseKeys(SectionData(section_envir,   // Section Environment
                                         section_cursor,  // Cursor for content
                                         t_FileData),     // Parent ini data
                             t_ParserData);
    }

    if (!py::len(section_envir)) {
      ParseSectionsDefault(t_FileData, t_ParserData, section_envir, true);
    }
  }
}

inline void ParseAllFiles(const ParserData &t_ParserData) {
  for (const auto &item : t_ParserData.m_ParserConfig.files) {
    py::dict file_envir;
    if (t_ParserData.m_ParserConfig.files.size() == 1 &&
        string_operations::is_nan(item.first)) {
      file_envir = t_ParserData.m_ParserConfig.envir;
    } else {
      file_envir = t_ParserData.m_ParserConfig.envir.attr("get")(
          py::cast(item.first), py::dict());
      t_ParserData.m_ParserConfig.envir[py::cast(item.first)] = file_envir;
    }

    if (item.second.empty()) {
      FileData m_FileData(file_envir, "");
      t_ParserData.ParseSections(m_FileData, t_ParserData);
    }

    for (std::string item_value : item.second) {
      if (string_operations::is_nan(item_value)) {
        continue;
      }
      item_value = system_operations::path_exanduser(item_value);
      if (!system_operations::file_exists(item_value) &&
          !string_operations::is_nan(item_value)) {
        py::object logger = py::module::import("logging");
        logger.attr("debug")("skipping file '" + item_value +
                             "', because not exists!");
        continue;
      }
      FileData m_FileData(file_envir, system_operations::read_file(item_value));
      t_ParserData.ParseSections(m_FileData, t_ParserData);
    }
  }

  // load defaults if no file exists / providing
  if (t_ParserData.m_ParserConfig.envir.empty()) {
    py::object logger = py::module::import("logging");
    logger.attr("debug")(
        "no sections or files to load, loading default values only.");
    py::dict file_envir = t_ParserData.m_ParserConfig.envir;
    FileData m_FileData(file_envir, "");
    ParseSectionsDefault(m_FileData, t_ParserData, file_envir, true);
  }
}

/// This is a simple (lightweight) C++ function to parse ini file into python
///
/// @param files vector of string with files to read
/// @param sections vector of string with included sections
/// @param keys vector of string with included keys
/// @param defaults vector of python objects for default values
/// @returns environment(s) with configs
py::dict ini_load(
    const std::map<std::string, std::vector<std::string>> &files,
    const std::map<std::string, std::vector<std::string>> &sections,
    const std::map<std::string, std::vector<std::string>> &keys,
    const std::map<std::string, std::vector<py::object>> &defaults,
    const bool &eval_env = false) {
  py::dict envir;

  // Controller
  switch (!sections.empty() * 1 + !keys.empty() * 2) {
    case 0: {
      ParseAllFiles(ParserData(ParseAllSections, ParseAllKeys,
                               ParserConfig(files,
                                            // vector of strings (keys + names)
                                            {},  // sections && section_names
                                            {},  // keys && key_names
                                            defaults, envir),
                               eval_env));
    } break;
    case 1: {
      ParseAllFiles(ParserData(ParseDefinedSections, ParseAllKeys,
                               ParserConfig(files,
                                            // vector of strings (keys + names)
                                            sections,  // sections
                                            {},        // keys && key_names
                                            defaults, envir),
                               eval_env));
    } break;
    case 2: {
      ParseAllFiles(ParserData(ParseAllSections, ParseDefinedKeys,
                               ParserConfig(files,
                                            // vector of strings (keys + names)
                                            {},  // sections && section_names
                                            keys, defaults, envir),
                               eval_env));
    } break;
    case 3: {
      ParseAllFiles(ParserData(ParseDefinedSections, ParseDefinedKeys,
                               ParserConfig(files,
                                            // vector of strings (keys + names)
                                            sections,  // sections
                                            keys, defaults, envir),
                               eval_env));
    } break;
  }

  return envir;
}

}  // namespace ini
