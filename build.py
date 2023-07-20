from glob import glob
import os
import pathlib
import re

import docutils.core
import pybind11
from pybind11.setup_helpers import Pybind11Extension, build_ext


def find_replace(file_list, find, replace, file_pattern):
    for file in [x for x in file_list if re.match(file_pattern, x)]:
        with open(file) as file_r:
            s = file_r.read()
        s = s.replace(find, replace)
        with open(file, "w") as file_w:
            file_w.write(s)


__version__ = "3.0.4"  # <<FORCE_BUMP>>
with open("cornflakes/__init__.py") as f:
    while line := f.readline():
        if "__version__" in line:
            __version__ = eval(line.split("=").pop().strip())

os.environ["VERSION_INFO"] = __version__

inst_path = "inst"
external_path = f"{inst_path}/ext"
path = f"{inst_path}/_cornflakes"
files = [
    f
    for f in [
        *glob(f"{path}/*/**", recursive=True),
        *glob(f"{path}/*", recursive=True),
        *glob(f"{external_path}/hash-library/*", recursive=True),
    ]
    if "test" not in f
    if os.path.splitext(f)[1] == ".cpp"
]

ext_paths = [external_path, f"{external_path}/pybind11/include", f"{external_path}/rapidjson/include/rapidjson"]

find_replace(glob(f"{external_path}/*/**"), "#include <endian.h>", "#include <cross_endian.h>", "^.*(.cpp|.h|.hpp)$")

docutils.core.publish_file(source_path="README.rst", destination_path="README.html", writer_name="html")

long_description = pathlib.Path("README.html").read_text()


def build(setup_kwargs):
    ext_modules = [
        Pybind11Extension("_cornflakes", [*files], include_dirs=[pybind11.get_include(), path, *ext_paths], cxx_std=17),
    ]
    setup_kwargs.update(
        {
            # "long_description": long_description,
            "long_description_content_type": "text/html",
            "ext_modules": ext_modules,
            "cmdclass": {
                "build_ext": build_ext,
            },
            "zip_safe": True,
        }
    )
