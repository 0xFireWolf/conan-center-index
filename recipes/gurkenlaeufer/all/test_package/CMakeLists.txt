cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

find_package(gurkenlaeufer REQUIRED)

add_executable(${PROJECT_NAME} main.cpp parsertests.cpp)

target_link_libraries(${PROJECT_NAME} PRIVATE gurkenlaeufer::gurkenlaeufer)

target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)
