// Copyright (c) 2022 Semjon Geist.

#include <string_operations.hpp>
#define strtk_no_tr1_or_boost
#include <datetime_utils.hpp>

//! implementations for string operations
namespace string_operations {

/// This is a simple C++ function to match a vector with values
///
/// @param vec vector of values
/// @param match value to match
/// @returns list of boolean
py::object apply_match(const std::vector<std::string> &vec, std::string match) {
  py::list result;

  for (auto value : vec) {
    std::string::const_iterator start_iter = value.begin();
    std::string::const_iterator end_iter = value.end();

    start_iter = std::search(start_iter, end_iter, match.begin(), match.end());
    // std::boyer_moore_horspool_searcher(...)

    result.append(py::cast(start_iter != end_iter));
  }

  return std::move(result);
}

/// This is a simple C++ function to extract values from data between two fixed
/// values
///
/// @param data string / bytes to extract from
/// @param start string / bytes for start-pattern
/// @param end string / bytes for end-pattern
/// @returns list with extracted values
py::list extract_between(const std::string &data, std::string start, char end) {
  py::list result;
  const int start_size = static_cast<int>(start.size());

  std::string::const_iterator start_iter = data.begin();
  std::string::const_iterator end_iter = data.end();
  std::string::const_iterator value_iter;

  while (true) {
    start_iter = std::search(start_iter, end_iter, start.begin(), start.end());
    // std::boyer_moore_horspool_searcher(...)

    if (start_iter == end_iter) {
      break;
    }
    start_iter += start_size;
    value_iter = std::find(start_iter + 1, end_iter, end);
    result.append(py::cast(std::string(start_iter, value_iter)));
  }

  return result;
}

template <class T_0, class T_1>
static bool compare_type() {
  return (typeid(T_0) == typeid(T_1));
}

template <class T_in, class T_out>
std::map<std::string, std::vector<T_out>> convert_to_map(
    const py::object &dictionary) {
  std::map<std::string, std::vector<T_out>> result;

  if (dictionary.is_none()) {
    return result;
  }
  if (py::isinstance<py::dict>(dictionary)) {
    for (std::pair<py::handle, py::handle> item : dictionary.cast<py::dict>()) {
      if (item.first.is_none()) {
        item.first = py::str("None");
      }
      if (item.second.is_none()) {
        result[item.first.cast<std::string>()] = {};
        continue;
      }
      if (py::isinstance<py::list>(item.second) &&
          !compare_type<py::object, T_out>() &&
          !compare_type<py::list, T_out>()) {
        result[item.first.cast<std::string>()] = std::vector<T_out>();
        for (auto item_value : item.second) {
          if (item_value.is_none()) {
            result[item.first.cast<std::string>()].push_back(
                py::str("None").cast<T_out>());
            continue;
          }
          if (py::isinstance<T_in>(item_value)) {
            result[item.first.cast<std::string>()].push_back(
                item_value.cast<T_out>());
          }
        }
        continue;
      }
      //                item.second = py::str(item.second);
      if (py::isinstance<T_in>(item.second)) {
        result[item.first.cast<std::string>()] = {item.second.cast<T_out>()};
      }
    }
  }
  if (py::isinstance<py::list>(dictionary)) {
    for (auto item : dictionary.cast<py::list>()) {
      if (py::isinstance<T_in>(item)) {
        auto key_val = item.cast<std::string>();
        result[key_val] = {item.cast<T_out>()};
      }
    }
  }
  if (py::isinstance<T_in>(dictionary)) {
    result[dictionary.cast<py::str>()] = {dictionary.cast<T_out>()};
  }
  return result;
}

std::map<std::string, std::vector<std::string>> convert_to_map_str(
    const py::object &dictionary) {
  return convert_to_map<py::str, std::string>(dictionary);
}

std::map<std::string, std::vector<py::object>> convert_to_map_py(
    const py::object &dictionary) {
  return convert_to_map<py::object, py::object>(dictionary);
}

bool is_nan(std::string value) {
  std::transform(value.begin(), value.end(), value.begin(), ::toupper);
  return std::find(NAN_STRINGS.begin(), NAN_STRINGS.end(), value) !=
         NAN_STRINGS.end();
}

bool is_quoted(const char &first_char, const char &last_char) {
  return (first_char == QUOTE_CHARS[0] && last_char == QUOTE_CHARS[0]) ||
         (first_char == QUOTE_CHARS[1] && last_char == QUOTE_CHARS[1]);
}

// get section index function
std::array<int, 2> idx_between(std::string::const_iterator start_iter,
                               std::string::const_iterator end_iter,
                               const std::string &begin_pattern,
                               const std::string &end_pattern, int skip = 0) {
  std::string::const_iterator skipped_iter = start_iter;
  std::advance(skipped_iter, skip);
  std::array<int, 2> idx{};

  // begin section index
  auto section_start_iter = std::search(
      skipped_iter, end_iter, begin_pattern.begin(), begin_pattern.end());
  // std::boyer_moore_horspool_searcher(...)

  idx[0] = static_cast<int>((section_start_iter - start_iter));
  if (idx[0] < 0) return (empty_idx);

  // end section index;
  idx[1] =
      static_cast<int>((std::search(section_start_iter, end_iter,
                                    end_pattern.begin(), end_pattern.end()) -
                        start_iter));
  // std::boyer_moore_horspool_searcher(...)

  if (idx[0] >= idx[1]) return (empty_idx);

  idx[1] += static_cast<int>((end_pattern.size()));

  return (idx);
}

std::string replace_all(const std::string &data, const std::string &to_search,
                        const std::string &replace_str) {
  std::string replacement = data;
  size_t pos = data.find(to_search);

  while (pos != std::string::npos) {
    replacement.replace(pos, to_search.size(), replace_str);
    pos = replacement.find(to_search, pos + replace_str.size());
  }

  return replacement;
}

std::string trim(const std::string &str, const std::string &whitespace) {
  const auto strBegin = str.find_first_not_of(whitespace);
  if (strBegin == std::string::npos) return "";  // no content

  const auto strEnd = str.find_last_not_of(whitespace);
  const auto strRange = strEnd - strBegin + 1;

  return str.substr(strBegin, strRange);
}

std::uint64_t parse8Chars(const char *string) noexcept {
  std::uint64_t chunk = 0;
  std::memcpy(&chunk, string, sizeof(chunk));

  // 1-byte mask trick (works on 4 pairs of single digits)
  std::uint64_t lower_digits = (chunk & 0x0f000f000f000f00) >> 8;
  std::uint64_t upper_digits = (chunk & 0x000f000f000f000f) * 10;
  chunk = lower_digits + upper_digits;

  // 2-byte mask trick (works on 2 pairs of two digits)
  lower_digits = (chunk & 0x00ff000000ff0000) >> 16;
  upper_digits = (chunk & 0x000000ff000000ff) * 100;
  chunk = lower_digits + upper_digits;

  // 4-byte mask trick (works on pair of four digits)
  lower_digits = (chunk & 0x0000ffff00000000) >> 32;
  upper_digits = (chunk & 0x000000000000ffff) * 10000;
  chunk = lower_digits + upper_digits;

  return chunk;
}

std::uint64_t parse64(std::string_view s) noexcept {
  std::uint64_t upper_digits = parse8Chars(s.data());
  std::uint64_t lower_digits = parse8Chars(s.data() + 8);
  return upper_digits * 100000000 + lower_digits;
}

#ifndef DOXYGEN_SHOULD_SKIP_THIS
dt_utils::datetime global_dt{};
dt_utils::date_format00 date_format00(global_dt);
dt_utils::date_format01 date_format01(global_dt);
dt_utils::date_format02 date_format02(global_dt);
dt_utils::date_format03 date_format03(global_dt);
dt_utils::date_format04 date_format04(global_dt);
dt_utils::date_format05 date_format05(global_dt);
dt_utils::date_format06 date_format06(global_dt);
dt_utils::date_format07 date_format07(global_dt);
dt_utils::date_format08 date_format08(global_dt);
dt_utils::date_format09 date_format09(global_dt);
dt_utils::date_format10 date_format10(global_dt);
dt_utils::date_format11 date_format11(global_dt);
dt_utils::date_format12 date_format12(global_dt);
dt_utils::date_format13 date_format13(global_dt);
dt_utils::date_format14 date_format14(global_dt);
dt_utils::date_format15 date_format15(global_dt);
dt_utils::datetime_format00 datetime_format00(global_dt);
dt_utils::datetime_format01 datetime_format01(global_dt);
dt_utils::datetime_format02 datetime_format02(global_dt);
dt_utils::datetime_format03 datetime_format03(global_dt);
dt_utils::datetime_format04 datetime_format04(global_dt);
dt_utils::datetime_format05 datetime_format05(global_dt);
dt_utils::datetime_format06 datetime_format06(global_dt);
dt_utils::datetime_format07 datetime_format07(global_dt);
dt_utils::datetime_format08 datetime_format08(global_dt);
dt_utils::datetime_format09 datetime_format09(global_dt);
dt_utils::datetime_format10 datetime_format10(global_dt);
dt_utils::datetime_format11 datetime_format11(global_dt);
dt_utils::datetime_format12 datetime_format12(global_dt);
dt_utils::datetime_format13 datetime_format13(global_dt);
dt_utils::datetime_format14 datetime_format14(global_dt);
dt_utils::datetime_format15 datetime_format15(global_dt);
dt_utils::datetime_format16 datetime_format16(global_dt);
dt_utils::datetime_format17 datetime_format17(global_dt);
dt_utils::datetime_format18 datetime_format18(global_dt);
dt_utils::datetime_format19 datetime_format19(global_dt);
dt_utils::datetime_format20 datetime_format20(global_dt);
dt_utils::datetime_format21 datetime_format21(global_dt);
dt_utils::datetime_format22 datetime_format22(global_dt);
dt_utils::datetime_format23 datetime_format23(global_dt);
dt_utils::datetime_format24 datetime_format24(global_dt);
dt_utils::datetime_format25 datetime_format25(global_dt);
dt_utils::datetime_format26 datetime_format26(global_dt);
dt_utils::datetime_format27 datetime_format27(global_dt);
dt_utils::datetime_format28 datetime_format28(global_dt);
dt_utils::datetime_format29 datetime_format29(global_dt);
dt_utils::datetime_format30 datetime_format30(global_dt);
dt_utils::datetime_format31 datetime_format31(global_dt);
dt_utils::datetime_format32 datetime_format32(global_dt);
dt_utils::datetime_format33 datetime_format33(global_dt);
dt_utils::time_format0 time_format0(global_dt);
dt_utils::time_format1 time_format1(global_dt);
dt_utils::time_format2 time_format2(global_dt);
dt_utils::time_format3 time_format3(global_dt);
dt_utils::time_format4 time_format4(global_dt);
dt_utils::time_format5 time_format5(global_dt);
dt_utils::time_format6 time_format6(global_dt);
dt_utils::time_format7 time_format7(global_dt);
dt_utils::time_format8 time_format8(global_dt);
dt_utils::time_format9 time_format9(global_dt);
dt_utils::time_format10 time_format10(global_dt);
dt_utils::time_format11 time_format11(global_dt);
dt_utils::time_format12 time_format12(global_dt);
#endif /* DOXYGEN_SHOULD_SKIP_THIS */

py::object get_global_datetime() {
  return py::module::import("datetime")
      .attr("datetime")(
          global_dt.year, global_dt.month, global_dt.day, global_dt.hour,
          global_dt.minute, global_dt.second,
          global_dt.microsecond ? global_dt.microsecond
                                : global_dt.millisecond * 1000,
          py::module::import("datetime")
              .attr("timezone")(py::module::import("datetime")
                                    .attr("timedelta")(0, global_dt.tzd * 60)));
}

py::object get_global_date() {
  return py::module::import("datetime")
      .attr("date")(global_dt.year, global_dt.month, global_dt.day);
}

py::object get_global_time() {
  return py::module::import("datetime")
      .attr("time")(
          global_dt.hour, global_dt.minute, global_dt.second,
          global_dt.microsecond ? global_dt.microsecond
                                : global_dt.millisecond * 1000,
          py::module::import("datetime")
              .attr("timezone")(py::module::import("datetime")
                                    .attr("timedelta")(0, global_dt.tzd * 60)));
}

py::object to_generic_datetime(const std::string &value) {
  global_dt.clear();
  try {
    if (strtk::string_to_type_converter(value, datetime_format00))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format01))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format02))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format03))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format04))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format05))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format06))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format07))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format08))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format09))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format10))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format11))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format12))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format13))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format14))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format15))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format16))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format17))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format18))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format19))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format20))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format21))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format22))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format23))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format24))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format25))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format26))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format27))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format28))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format29))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format30))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format31))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format32))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format33))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, date_format00))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format01))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format02))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format03))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format04))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format05))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format06))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format07))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format08))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format09))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format10))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format11))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format12))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format13))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format14))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format15))
      return get_global_date();
    if (strtk::string_to_type_converter(value, time_format0))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format1))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format2))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format3))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format4))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format5))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format6))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format7))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format8))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format9))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format10))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format11))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format12))
      return get_global_time();
  } catch (...) {
    return py::cast(value);
  }

  return py::cast(value);
}

// clang-format off
void preprocessJsonInPlace(std::string &input) {  // NOLINT
  char insideQuote = '\0';  // '\0' means outside any string
  size_t pos = 0;
  while (pos < input.size()) {
    size_t nextQuotePos;
    if (insideQuote) {
      // If inside a string, search for the ending quote type
      nextQuotePos = input.find(insideQuote, pos);
      if (nextQuotePos == std::string::npos) {
        break;  // No more of the current quote type found
      }
      insideQuote = '\0';  // Reset to outside any string
    } else {
      // If outside a string, search for both single and double quotes
      nextQuotePos = input.find_first_of("'\"", pos);
      if (nextQuotePos == std::string::npos) {
        break;  // No more quotes found
      }
      if (input[nextQuotePos] == '"') {
        insideQuote = '"';
      } else {
        input[nextQuotePos] = '"';
        insideQuote = '\0';
      }
    }
    pos = nextQuotePos + 1;
  }
}
//// clang-format on




/// This is a simple C++ function to cast strings into python objects with
/// specific type
///
/// @param value string to cast
/// @returns python object (none, boolean, int, time, date, datetime,
/// datetime_ms, ip_address)
py::object eval_type(std::string value) {
  if (value.empty()) {
    return py::none();
  }

  int char_size = static_cast<int>(value.size());

  if (char_size <= 1) {
    if (std::isdigit(value.back())) return (py::cast(std::stoi(value)));
    return (py::cast(value));
  }

  // remove quote
  if (is_quoted(value[0], value.back())) {
    value = value.erase(0, 1).erase(char_size - 2);
    char_size = char_size - 2;

    if (value.empty()) {
      return py::none();
    }

    if (char_size == 1) {
      if (std::isdigit(value[0])) return (py::cast(std::stoi(&value[0])));
      return (py::cast(value[0]));
    }
  }

  // parse numeric
  if (std::regex_match(value, numeric_regex)) {
    if (value.find_first_of('.') != std::string::npos || value.back() == '.') {
      if (char_size > 18) {
        return (py::module::import("decimal").attr("Decimal")(value));
      }

      // parse double
      return (py::cast(std::stod(value)));
    }

    // parse numeric
    if (value[0] == MINUS_CHAR) {
      value = value.erase(0, 1);
      uint64_t integer = parse64(value.c_str());
      if (integer < UINT_MAX) {
        return (py::cast(-integer));
      }
      return (-py::module::import("builtins").attr("int")(value));
    }

    uint64_t integer = parse64(value.c_str());
    if (integer < UINT_MAX) {
      return (py::cast(integer));
    }
    return (py::module::import("builtins").attr("int")(value));
  }

  if (value.length() <= 2 && value[0] == ESCAPE_CHAR[0]) {
    if (value == "\\n") {
      return py::str("\n");
    } else if (value == "\\r") {
      return py::str("\r");
    } else if (value == "\\t") {
      return py::str("\t");
    } else if (value == "\\\\") {
      return py::str("\\");
    }
  }

  // is hex char
  if (value.length() <= 4 && value[0] == HEX_CHAR[0] &&
      std::toupper(value[1]) == HEX_CHAR[1] &&
      std::regex_match(value, hex_regex)) {
    return py::cast(std::stoul(value, nullptr, 16));
  }

  const char upper_first_char = static_cast<char>(std::toupper(value[0]));

  // boolean true or boolan false
  if (char_size < 6 &&
      (upper_first_char == TRUE_CHAR || upper_first_char == FALSE_CHAR)) {
    if (std::regex_match(value, boolen_true_regex)) {
      return (py::cast(true));
    }

    if (std::regex_match(value, boolen_false_regex)) {
      return (py::cast(false));
    }
  }

  if (is_nan(value)) {
    return (py::cast<py::none>(Py_None));
  }

  if (char_size == 36 && std::regex_match(value, uuid_regex)) {
    return (py::module::import("uuid").attr("UUID")(value));
  }

  const char last_char = value.back();

  if ((value[0] == JSON_CHARS[0] && last_char == JSON_CHARS[1]) ||
      (value[0] == ARRAY_CHARS[0] && last_char == ARRAY_CHARS[1])) {
    std::string json_value =
        replace_all(value, ESCAPE_CHAR, PYTHON_ESCAPE_CHAR);
    preprocessJsonInPlace(json_value);
    if (!json_doc.Parse(const_cast<char *>(json_value.c_str()))
             .HasParseError()) {
      return py::eval(json_value);
    }
  }

  if (char_size < 6) {
    // normal string
    return py::cast(value);
  }

  // ipv4
  if (char_size < 39 && char_size > 6) {
    // ipv4
    if (std::count(value.begin(), value.end(), '.') == 3 &&
        std::regex_match(value, ipv4_regex)) {
      return (py::module::import("ipaddress").attr("IPv4Address")(value));
    }
    // ipv6
    if (std::count(value.begin(), value.end(), ':') > 5) {
      try {
        return (py::module::import("ipaddress").attr("IPv6Address")(value));
      } catch (...) {
      }
    }
    if (char_size > 7) {
      return (to_generic_datetime(value));
    }
  }

  // normal string
  return py::cast(value);
}

/// This is a simple C++ function to cast strings into python datetime object
///
/// @param value string to cast
/// @returns python object (time, date, datetime, datetime_ms)
/// @note This function returns the same value as string when no datetime type
/// is detected
py::object eval_datetime(const std::string &value) {
  return to_generic_datetime(value);
}

std::map<std::string, py::object> eval_csv(
    const std::string &input, const char *extra_disallowed_header_chars = "") {
  std::map<std::string, py::object> format;

  // Detect line separator
  std::vector<std::string> line_separators = {"\r\n", "\r", "\n"};
  std::string line_separator;
  for (const auto &sep : line_separators) {
    if (input.find(sep) != std::string::npos) {
      line_separator = sep;
      break;
    }
  }
  format["line_separator"] = py::cast(line_separator);

  // Split input into lines
  std::vector<std::string> lines;
  std::stringstream ss(input);
  std::string line;
  while (std::getline(ss, line, line_separator[0])) {
    lines.push_back(line);
  }

  format["parsed_line_count"] = py::cast(lines.size());

  // Detect column separator and quoting character
  std::vector<std::string> column_separators = {",", ";", "\t", "|", "\b"};
  std::string column_separator, quoting_character;
  for (const auto &sep : column_separators) {
    if (lines[0].find(sep) != std::string::npos) {
      column_separator = sep;
      break;
    }
  }
  format["column_separator"] = py::cast(column_separator);

  // Detect header
  std::vector<std::string> header;
  std::vector<std::string> column_types;
  bool has_header = true;
  std::stringstream line_stream(lines[0]);
  std::string cell;
  while (std::getline(line_stream, cell, column_separator[0])) {
    if ((!cell.empty() && !is_nan(cell) &&
         (cell[0] == QUOTE_CHARS[0] || cell[0] == QUOTE_CHARS[1]) &&
         (!is_quoted(cell[0], cell.back()) ||
          !(is_quoted(cell[0], cell.back()) &&
            std::count(cell.begin(), cell.end(), cell[0]) % 2 == 0))) ||
        (cell.length() == 1 &&
         (cell[0] == QUOTE_CHARS[0] || cell[0] == QUOTE_CHARS[1]))) {
      std::string full_cell = cell;
      quoting_character = cell[0];
      while (std::getline(line_stream, cell, column_separator[0])) {
        full_cell.append(column_separator[0] + cell);
        if (!cell.empty() &&
            (cell.back() == QUOTE_CHARS[0] || cell.back() == QUOTE_CHARS[1]) &&
            std::count(full_cell.begin(), full_cell.end(), full_cell[0]) % 2 ==
                0) {
          break;
        }
      }
      cell = full_cell;
    }
    if (!cell.empty() && is_quoted(cell[0], cell.back())) {
      cell = cell.erase(0, 1).erase(cell.size() - 1);
    }
    header.push_back(cell);
  }

  for (const auto &h : header) {
    column_types.push_back(
        eval_type(h).attr("__class__").attr("__name__").cast<std::string>());
    if (column_types.back() == "NoneType") {
      continue;
    }
    if (column_types.back() != "str" ||
        h.find_first_of(SPECIAL_CHARS + extra_disallowed_header_chars) !=
            std::string::npos ||
        h.empty()) {
      has_header = false;
    }
  }
  format["has_header"] = has_header ? py::str("True") : py::str("False");
  if (has_header) {
    format["header"] = py::cast(header);
    column_types.clear();
  }

  for (auto it = std::next(lines.begin()); it != lines.end(); ++it) {
    int col_idx = 0;
    line = *it;
    std::stringstream l_stream(line);
    while (std::getline(l_stream, cell, column_separator[0])) {
      if ((!cell.empty() && !is_nan(cell) &&
           (cell[0] == QUOTE_CHARS[0] || cell[0] == QUOTE_CHARS[1]) &&
           (!is_quoted(cell[0], cell.back()) ||
            !(is_quoted(cell[0], cell.back()) &&
              std::count(cell.begin(), cell.end(), cell[0]) % 2 == 0))) ||
          (cell.length() == 1 &&
           (cell[0] == QUOTE_CHARS[0] || cell[0] == QUOTE_CHARS[1]))) {
        std::string full_cell = cell;
        quoting_character = cell[0];
        while (std::getline(l_stream, cell, column_separator[0])) {
          full_cell.append(column_separator[0] + cell);
          if (!cell.empty() &&
              (cell.back() == QUOTE_CHARS[0] ||
               cell.back() == QUOTE_CHARS[1]) &&
              std::count(full_cell.begin(), full_cell.end(), full_cell[0]) %
                      2 ==
                  0) {
            break;
          }
        }
        cell = full_cell;
      }
      if (col_idx < static_cast<int>(column_types.size()) &&
          !is_nan(column_types[col_idx])) {
        col_idx++;
        continue;
      }
      if ((col_idx >= static_cast<int>(column_types.size())) != 0) {
        if (cell.empty() || is_nan(cell)) {
          column_types.emplace_back("NoneType");
          if (col_idx >= static_cast<int>(column_types.size())) {
            header.emplace_back("");  // fill header
          }
          col_idx++;
          continue;
        }
        column_types.push_back(eval_type(cell)
                                   .attr("__class__")
                                   .attr("__name__")
                                   .cast<std::string>());
        if (col_idx >= static_cast<int>(column_types.size())) {
          header.emplace_back("");  // fill header
        }
        col_idx++;
        continue;
      }
      if (!cell.empty() && !is_nan(cell)) {
        auto cell_type = eval_type(cell)
                             .attr("__class__")
                             .attr("__name__")
                             .cast<std::string>();
        column_types[col_idx] = cell_type;
      }
      col_idx++;
    }
  }
  format["column_types"] = py::cast(column_types);
  format["column_count"] =
      py::cast(!column_types.empty() ? column_types.size() : header.size());
  format["quoting_character"] = py::cast(quoting_character);
  return format;
}

std::string DetectType(const rapidjson::Value &value) {
  if (value.IsString()) return "string";
  if (value.IsInt()) return "int";
  if (value.IsBool()) return "boolean";
  if (value.IsDouble()) return "double";
  if (value.IsObject()) return "record";
  if (value.IsArray()) return "array";
  return "null";
}

void generateAvroSchema(const rapidjson::Value &value,
                        rapidjson::StringBuffer *buffer, int depth = 0) {
  if (depth >= MAX_DEPTH) {
    throw std::runtime_error("Failed to process parsed JSON string, "
                             "because recursion depth is to large!");
  }
  rapidjson::Writer<rapidjson::StringBuffer> writer(*buffer);

  std::string type = DetectType(value);

  if (type == "record") {
    writer.StartObject();
    writer.Key("type");
    writer.String("record");
    writer.Key("fields");
    writer.StartArray();

    for (rapidjson::Value::ConstMemberIterator itr = value.MemberBegin();
    itr != value.MemberEnd(); ++itr) {
      rapidjson::StringBuffer subBuffer;
      rapidjson::Writer<rapidjson::StringBuffer> subWriter(subBuffer);

      writer.StartObject();
      writer.Key("name");
      writer.String(itr->name.GetString());
      writer.Key("type");

      generateAvroSchema(itr->value, &subBuffer, depth + 1);
      writer.RawValue(subBuffer.GetString(),
                      subBuffer.GetSize(),
                      rapidjson::kNullType);

      writer.EndObject();
    }
    writer.EndArray();
    writer.EndObject();
  } else if (type == "array") {
    writer.StartObject();
    writer.Key("type");
    writer.String("array");
    writer.Key("items");

    // Handle arrays with elements of potentially different types
    writer.StartArray();
    for (rapidjson::SizeType i = 0; i < value.Size(); i++) {
      rapidjson::StringBuffer subBuffer;
      rapidjson::Writer<rapidjson::StringBuffer> subWriter(subBuffer);

      generateAvroSchema(value[i], &subBuffer, depth + 1);
      writer.RawValue(subBuffer.GetString(),
                      subBuffer.GetSize(),
                      rapidjson::kNullType);
    }
    writer.EndArray();

    writer.EndObject();

  } else {
    writer.String(type.c_str());
  }
}

py::dict generateAvroSchemaPy(const std::string &jsonChunk) {
  rapidjson::StringBuffer buffer;

  rapidjson::Document d;
  d.Parse(jsonChunk.c_str());
  if (d.HasParseError()) {
    throw std::runtime_error("Failed to parse the provided JSON string.");
  }
  generateAvroSchema(d, &buffer, 0);

  return py::eval(buffer.GetString());
}

}  // namespace string_operations
