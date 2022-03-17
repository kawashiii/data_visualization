cmake_minimum_required(VERSION 3.4)

set(CMAKE_CXX_FLAGS "-std=c++11")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

project(data_visualization_tool)

add_executable(${PROJECT_NAME} src/main.cpp)


