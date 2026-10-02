#!/bin/bash
# wrk 延迟直方图（用法: latency_hist.sh [t] [c]）
cd "$(dirname "$0")/.."
T=${1:-4}; C=${2:-100}
mkdir -p /run/mysqld
pkill -f "socat UNIX-LISTEN:/run/mysqld" 2>/dev/null
setsid socat UNIX-LISTEN:/run/mysqld/mysqld.sock,fork TCP:127.0.0.1:3306 </dev/null >/dev/null 2>&1 &
sleep 1
(./server -p 9006 ${EXTRA_ARGS:-} >/dev/null 2>&1 &)
sleep 1
wrk -t$T -c$C -d10s --latency http://127.0.0.1:9006/ 2>/dev/null | grep -E "Latency|Req/Sec|Requests/sec|errors|^[0-9]+%|Socket"
pkill -f "./server -p 9006" 2>/dev/null
pkill -f "socat UNIX-LISTEN:/run/mysqld" 2>/dev/null
exit 0
