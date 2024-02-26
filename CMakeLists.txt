cmake_minimum_required(VERSION 3.0)
set(CMAKE_FIND_PACKAGE_PREFER_CONFIG ON)

project(eCALcpp)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(eCAL REQUIRED)
find_package(Protobuf REQUIRED)
message(STATUS "Protobuf found: = ${Protobuf_FOUND}")
message(STATUS "Protobuf version: = ${Protobuf_VERSION}")
message(STATUS "Protobuf DIR: = ${Protobuf_DIR}")

set(TARGET_NAME_PUB ecal_send)

set(ecal_snd
        ${CMAKE_CURRENT_SOURCE_DIR}/cpp/send.cpp
)

set(protobuf_files
        ${CMAKE_CURRENT_SOURCE_DIR}/proto/image.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/proto/mi_mensaje.proto
        )

add_executable(${TARGET_NAME_PUB} ${ecal_snd})

PROTOBUF_TARGET_CPP(${TARGET_NAME_PUB} ${CMAKE_CURRENT_SOURCE_DIR}/proto/ ${protobuf_files})

target_link_libraries(${TARGET_NAME_PUB}
        PRIVATE
        eCAL::core
        ${Protobuf_LIBRARIES}
)

