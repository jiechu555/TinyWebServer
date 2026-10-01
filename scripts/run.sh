#!/bin/bash
# TinyWebServer 启动脚本（基线环境，WSL2 + Windows Docker MySQL）
# 用法: ./run.sh [端口]
# 前置: WSL2 mirrored 网络——localhost:3306 直通 Windows 宿主 MySQL 容器
set -e
PORT=9006

# libmysqlclient 对 "localhost" 走 Unix socket（代码硬编码），桥接到 TCP 的宿主 MySQL
if [ ! -S /run/mysqld/mysqld.sock ]; then
    mkdir -p /run/mysqld
    socat UNIX-LISTEN:/run/mysqld/mysqld.sock,fork TCP:127.0.0.1:3306 &
    echo "socat 桥已启动 (unix:/run/mysqld/mysqld.sock -> tcp:127.0.0.1:3306)"
fi

./server -p ""
