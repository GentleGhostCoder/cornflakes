// Copyright (c) 2022 Semjon Geist.

#include <bindings.h>

//! pybind module declaration
PYBIND11_MODULE(_cornflakes, module) {
  module.doc() = R"pbdoc(
        _cornflakes (Pybind11 modules)
        ------------------------------
        .. currentmodule:: _cornflakes

        .. autosummary::
           :toctree: _generate

            ini_load
            eval_type
            eval_datetime
            eval_csv
            extract_between
            apply_match
            simple_hmac
            simple_sha256
    )pbdoc";

  //    py::object decimal = py::module::import("decimal").attr("Decimal");
  //    auto custom_decimal = py::reinterpret_borrow<py::object>((PyObject *)
  //    &PyType_Type); py::dict attributes;
  //
  //    py::class_<std::int64_t> custom_decimal_class =
  //    custom_decimal("Decimal", py::make_tuple(decimal), attributes);
  //
  //    custom_decimal_class.def("__str__", [](const py::object &self) ->
  //    std::string {
  //        auto str = self.attr("__repr__")().cast<std::string>();
  //        str = str.substr(9, str.size() - 11);
  //        std::string::const_iterator start_iter(str.begin());
  //        std::string::const_iterator end_iter(str.end());
  //        std::string::const_iterator e_idx = std::find(start_iter, end_iter,
  //        'E'); if (e_idx == end_iter) return str; if (str[0] == '-') {
  //            return "-0." + std::string((std::stoi(std::string(e_idx + 2,
  //            end_iter)) - 1), '0') +
  //                   str[1] + (start_iter + 3 < e_idx ? std::string(start_iter
  //                   + 3, e_idx) : "");
  //        }
  //        return "0." + std::string((std::stoi(std::string(e_idx + 2,
  //        end_iter)) - 1), '0') +
  //               str[0] + (start_iter + 2 < e_idx ? std::string(start_iter +
  //               2, e_idx) : "");
  //    }, R"pbdoc(Wrapper of decimal.Decimal class.)pbdoc");
  //
  //    module.attr("Decimal") = custom_decimal_class;

  module.def(
      "ini_load",
      [](const py::object &files, const py::object &sections,
         const py::object &keys, const py::object &defaults,
         const bool &eval_env) -> py::dict {
        const auto m_files = string_operations::convert_to_map_str(files);
        const auto m_sections = string_operations::convert_to_map_str(sections);
        const auto m_keys =
            keys.is_none()
                ? string_operations::convert_to_map_str(
                      defaults.is_none() ? defaults : defaults.attr("keys"))
                : string_operations::convert_to_map_str(keys);
        const auto m_defaults = string_operations::convert_to_map_py(defaults);
        return ini::ini_load(m_files, m_sections, m_keys, m_defaults, eval_env);
      },
      py::arg("files").none(true) = py::none(),
      py::arg("sections").none(true) = py::none(),
      py::arg("keys").none(true) = py::none(),
      py::arg("defaults").none(true) = py::none(),
      py::arg("eval_env").none(true) = py::cast(false),
      R"pbdoc(
        .. doxygenfunction:: ini::ini_load
            :project: _cornflakes
      )pbdoc");

  module.def(
      "eval_type",
      [](const std::string &value) -> py::object {
        return string_operations::eval_type(value);
      },
      py::arg("value").none(false),
      R"pbdoc(
        .. doxygenfunction:: string_operations::eval_type
            :project: _cornflakes
        )pbdoc");

  module.def(
      "eval_datetime",
      [](const std::string &value) -> py::object {
        return string_operations::eval_datetime(value);
      },
      py::arg("value").none(false),
      R"pbdoc(
        .. doxygenfunction:: string_operations::eval_datetime
            :project: _cornflakes
        )pbdoc");

  module.def(
      "eval_csv",
      [](const std::string &value) -> py::object {
        return string_operations::eval_csv(value);
      },
      py::arg("value").none(false),
      R"pbdoc(
        .. doxygenfunction:: string_operations::eval_csv
            :project: _cornflakes
        )pbdoc");

  module.def(
      "extract_between",
      [](const py::bytes &data, const py::str &start,
         const py::str &end) -> py::object {
        return string_operations::extract_between(
            data.cast<std::string>(), start.cast<std::string>(),
            end.cast<std::string>().at(0));
      },
      py::arg("data").none(false), py::arg("start").none(false),
      py::arg("end").none(false),
      R"pbdoc(
        .. doxygenfunction:: string_operations::extract_between
            :project: _cornflakes
        )pbdoc");

  module.def(
      "apply_match",
      [](const py::list &vec, const py::str &start) -> py::object {
        return string_operations::apply_match(
            vec.cast<std::vector<std::string>>(), start.cast<std::string>());
      },
      py::arg("vec").none(false), py::arg("start").none(false),
      R"pbdoc(
        .. doxygenfunction:: string_operations::apply_match
            :project: _cornflakes
        )pbdoc");

  module.def(
      "simple_hmac",
      [](const py::list &data, const std::string &algo) -> py::object {
        return py::cast(
            digest::simple_hmac(data.cast<std::vector<std::string>>(), algo));
      },
      py::arg("data").none(false), py::arg("algo").none(true) = "SHA256",
      R"pbdoc(
          .. doxygenfunction:: digest::simple_hmac
              :project: _cornflakes
          )pbdoc");

  module.def(
      "simple_sha256",
      [](const py::object &data) -> py::object {
        return py::cast(digest::simple_sha256(data.cast<std::string>()));
      },
      py::arg("data").none(false),
      R"pbdoc(
          .. doxygenfunction:: digest::simple_sha256
              :project: _cornflakes
          )pbdoc");

  module.attr("__name__") = "_cornflakes";
#ifdef VERSION_INFO
  module.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
  module.attr("__version__") = "dev";
#endif
}
