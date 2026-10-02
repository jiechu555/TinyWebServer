cmake_minimum_required(VERSION 3.16)
project(TinyWebServer CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()
# 警告即门槛：commit 5 已清零，CI 里再冒警告会醒目可见（不设 -Werror 保留外部平台差异余地）
add_compile_options(-Wall -Wextra)

find_package(Threads REQUIRED)

# ==================== 主程序 ====================
add_executable(server
    main.cpp
    webserver.cpp
    config.cpp
    http/http_conn.cpp
    timer/lst_timer.cpp
    log/log.cpp
    CGImysql/sql_connection_pool.cpp
)
target_link_libraries(server PRIVATE Threads::Threads mysqlclient)

# ==================== 单元测试（可选，-DBUILD_TESTING=ON） ====================
if(BUILD_TESTING)
    include(FetchContent)
    # gtest 源内下载（CI 网络无障碍；本地若 github 不通用 gh-proxy 镜像替换 URL）
    FetchContent_Declare(googletest
        URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip)
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    FetchContent_MakeAvailable(googletest)

    enable_testing()
    # 依赖闭包：timer 引用 http_conn 静态成员、sql_connection_pool 引用 mysqlclient
    add_executable(unit_tests
        tests/test_block_queue.cpp
        tests/test_timer.cpp
        tests/test_threadpool.cpp
        timer/lst_timer.cpp
        log/log.cpp
        http/http_conn.cpp
        CGImysql/sql_connection_pool.cpp
    )
    target_link_libraries(unit_tests PRIVATE mysqlclient)
    target_link_libraries(unit_tests PRIVATE gtest_main Threads::Threads)
    add_test(NAME unit_tests COMMAND unit_tests)
endif()
