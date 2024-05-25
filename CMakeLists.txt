cmake_minimum_required(VERSION 3.0)
set(CMAKE_FIND_PACKAGE_PREFER_CONFIG ON)

project(eCALcpp)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(eCAL REQUIRED)
find_package(Protobuf REQUIRED)
find_package(OpenCV REQUIRED)
message(STATUS "Protobuf found: = ${Protobuf_FOUND}")
message(STATUS "Protobuf version: = ${Protobuf_VERSION}")
message(STATUS "Protobuf DIR: = ${Protobuf_DIR}")

set(TARGET_NAME_PUB ecal_send)
set(TARGET_WEBCAM_PUB ecal_cam_send)
set(TARGET_WEBCAM_SUB ecal_cam_receive)

set(ecal_snd
        ${CMAKE_CURRENT_SOURCE_DIR}/cpp/send.cpp
)

set(ecal_cam_snd
        ${CMAKE_CURRENT_SOURCE_DIR}/cpp/send_webcam.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/cpp/ecal_interface.h
)

set(ecal_cam_rcv
        ${CMAKE_CURRENT_SOURCE_DIR}/cpp/receive_webcam.cpp
)

set(protobuf_files
        ${CMAKE_CURRENT_SOURCE_DIR}/proto/image.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/proto/mi_mensaje.proto
        )

add_executable(${TARGET_NAME_PUB} ${ecal_snd})
add_executable(${TARGET_WEBCAM_PUB} ${ecal_cam_snd})
add_executable(${TARGET_WEBCAM_SUB} ${ecal_cam_rcv})

PROTOBUF_TARGET_CPP(${TARGET_NAME_PUB} ${CMAKE_CURRENT_SOURCE_DIR}/proto/ ${protobuf_files})
PROTOBUF_TARGET_CPP(${TARGET_WEBCAM_PUB} ${CMAKE_CURRENT_SOURCE_DIR}/proto/ ${protobuf_files})
PROTOBUF_TARGET_CPP(${TARGET_WEBCAM_SUB} ${CMAKE_CURRENT_SOURCE_DIR}/proto/ ${protobuf_files})

target_link_libraries(${TARGET_NAME_PUB}
        PRIVATE
        eCAL::core
        ${Protobuf_LIBRARIES}
)

target_link_libraries(${TARGET_WEBCAM_PUB}
        PRIVATE
        eCAL::core
        ${Protobuf_LIBRARIES}
        ${OpenCV_LIBS}
)

target_link_libraries(${TARGET_WEBCAM_SUB}
        PRIVATE
        eCAL::core
        ${Protobuf_LIBRARIES}
        ${OpenCV_LIBS}
)
