#!/bin/bash
# gdb 场景B：user 表缺失时启动，抓崩溃栈
cd "$(dirname "$0")/.."
mkdir -p /run/mysqld
pkill -f "socat UNIX-LISTEN:/run/mysqld" 2>/dev/null
setsid socat UNIX-LISTEN:/run/mysqld/mysqld.sock,fork TCP:127.0.0.1:3306 </dev/null >/dev/null 2>&1 &
sleep 1
timeout 20 gdb -batch -ex run -ex bt --args ./server -p 9006 2>&1 | grep -A 12 "SIGSEGV\|exited"
pkill -f "socat UNIX-LISTEN:/run/mysqld" 2>/dev/null
