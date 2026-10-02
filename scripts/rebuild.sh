#!/bin/bash
# 同步 Windows 侧改动到 WSL 主场并重编译（开发同步脚本）
# 用法: bash scripts/rebuild.sh
set -e
SRC=/mnt/c/Users/12808/Documents/code/TinyWebServer
cd "$(dirname "$0")/.."
cp -r "$SRC"/http/*.h "$SRC"/http/*.cpp http/ 2>/dev/null || true
cp "$SRC"/webserver.cpp "$SRC"/webserver.h "$SRC"/main.cpp "$SRC"/config.cpp "$SRC"/config.h . 2>/dev/null || true
cp -r "$SRC"/timer/*.h "$SRC"/timer/*.cpp timer/ 2>/dev/null || true
cp -r "$SRC"/log/*.h "$SRC"/log/*.cpp log/ 2>/dev/null || true
cp -r "$SRC"/threadpool/*.h "$SRC"/threadpool/*.cpp threadpool/ 2>/dev/null || true
cp -r "$SRC"/CGImysql/*.h "$SRC"/CGImysql/*.cpp CGImysql/ 2>/dev/null || true
cp "$SRC"/README.md . 2>/dev/null || true
rm -f server
make 2>&1 | grep -E "error" && { echo "编译失败"; exit 1; }
echo "同步+编译 OK: $(date +%H:%M:%S)"
