#!/bin/bash
# valgrind 体检：SIGTERM 优雅退出路径（触发栈上 WebServer 析构）
# 用法: valgrind_check.sh [请求数]
cd "$(dirname "$0")/.."
N=${1:-10}
mkdir -p /run/mysqld
pkill -f "socat UNIX-LISTEN:/run/mysqld" 2>/dev/null
setsid socat UNIX-LISTEN:/run/mysqld/mysqld.sock,fork TCP:127.0.0.1:3306 </dev/null >/dev/null 2>&1 &
sleep 1
rm -f valgrind.log
valgrind --leak-check=full --show-leak-kinds=all --log-file=valgrind.log ./server -p 9006 >/dev/null 2>&1 &
VG=$!
sleep 3
for i in $(seq $N); do curl -s -o /dev/null http://127.0.0.1:9006/; done
kill -TERM $(pgrep -f "server -p 9006" | head -1) 2>/dev/null
sleep 3
pkill -f "server -p 9006" 2>/dev/null
pkill -f "socat UNIX-LISTEN:/run/mysqld" 2>/dev/null
grep -E "definitely lost|indirectly lost|possibly lost|still reachable" valgrind.log | head -4
grep "total heap usage\|ERROR SUMMARY" valgrind.log
