#!/bin/bash
# 压测脚本：启动服务 + wrk 指定档位（用法: bench.sh [t] [c] [dur]）
cd "$(dirname "$0")/.."
T=${1:-4}; C=${2:-100}; D=${3:-10s}
mkdir -p /run/mysqld
pkill -f "socat UNIX-LISTEN:/run/mysqld" 2>/dev/null
setsid socat UNIX-LISTEN:/run/mysqld/mysqld.sock,fork TCP:127.0.0.1:3306 </dev/null >/dev/null 2>&1 &
sleep 1
(./server -p 9006 >/dev/null 2>&1 &)
sleep 1
echo "=== wrk -t$T -c$C -d$D ==="
wrk -t$T -c$C -d$D http://127.0.0.1:9006/ 2>/dev/null | grep -E "Latency|Requests/sec|errors"
pkill -f "./server" 2>/dev/null
pkill -f "socat UNIX-LISTEN:/run/mysqld" 2>/dev/null
exit 0
