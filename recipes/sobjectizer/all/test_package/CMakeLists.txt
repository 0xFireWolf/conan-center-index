cmake_minimum_required(VERSION 3.15)
project(test_package CXX)

find_package(sobjectizer REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_17)
if(TARGET sobjectizer::SharedLib)
    target_link_libraries(${PROJECT_NAME} sobjectizer::SharedLib)
else()
    target_link_libraries(${PROJECT_NAME} sobjectizer::StaticLib)
endif()
