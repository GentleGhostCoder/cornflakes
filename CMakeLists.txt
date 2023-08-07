# this Cmakelist.txt is optional and not required for c++ development (ide ->
# autocompletion) dependencies evaluation.
cmake_minimum_required(VERSION 3.4...3.22)
project(_cornflakes LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

set(EXT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/inst/ext)

add_subdirectory(${EXT_DIR}/pybind11)

set(VENV_PATH "${CMAKE_CURRENT_SOURCE_DIR}/.venv")

# Set the path to the Python interpreter in the virtual environment
set(PYTHON_EXECUTABLE "${VENV_PATH}/bin/python")

execute_process(
  COMMAND
    ${PYTHON_EXECUTABLE} -c
    "import pkg_resources; print(f'{pkg_resources.get_distribution(\"pybind11\").location}/pybind11/share/cmake')"
  OUTPUT_VARIABLE pybind11_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE)
find_package(pybind11 REQUIRED PATHS ${pybind11_DIR} NO_DEFAULT_PATH)

include_directories(${EXT_DIR})
include_directories(${EXT_DIR}/rapidjson/include/rapidjson)
include_directories(${CMAKE_SOURCE_DIR}/inst/_cornflakes)

get_property(
  dirs
  DIRECTORY .
  PROPERTY INCLUDE_DIRECTORIES)
foreach(dir ${dirs})
  message(STATUS "dir='${dir}'")
endforeach()

file(GLOB_RECURSE HASH_LIB_SOURCE_FILES ${EXT_DIR}/hash-library/*.cpp)
list(FILTER HASH_LIB_SOURCE_FILES EXCLUDE REGEX ".*test.*")

file(GLOB_RECURSE SOURCE_FILES *.cpp)
list(FILTER SOURCE_FILES EXCLUDE REGEX ".*ext.*")
list(FILTER SOURCE_FILES EXCLUDE REGEX ".*cmake-build-debug.*")

pybind11_add_module(${PROJECT_NAME} MODULE NO_EXTRAS ${SOURCE_FILES}
                    ${HASH_LIB_SOURCE_FILES})

target_include_directories(${PROJECT_NAME} PUBLIC ${EXT_DIR})
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME ${PROJECT_NAME})
target_compile_definitions(${PROJECT_NAME} PRIVATE VERSION_INFO=${VERSION_INFO})

add_compile_options(
  "-Wall"
  "-Wpedantic"
  "-Wextra"
  "-fexceptions"
  "$<$<CONFIG:DEBUG>:-O0;-g3;-ggdb>"
  "-Wextra"
  "-Wundef"
  "-pedantic"
  "-msse2"
  "-msse3"
  "-mpopcnt"
  "-funsafe-math-optimizations"
  "-fno-math-errno")
