# this Cmakelist.txt is optional and not required for c++ development (ide ->
# autocompletion) dependencies evaluation.
cmake_minimum_required(VERSION 3.4...3.22)
project(_cornflakes LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

set(EXT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/inst/ext)

add_subdirectory(${EXT_DIR}/pybind11)

# include_directories(${CMAKE_CURRENT_SOURCE_DIR}/.venv/lib/python3.10/site-packages/pybind11/include)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/${PYTHON_SITE}/pybind11/include)
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
