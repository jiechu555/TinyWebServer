#!/bin/bash
# commit 4 对照实验矩阵：单一变量原则，每个配置跑 t4c100 + t8c1000 各 10s
# 用法: experiment_matrix.sh [server_args...]   (例: experiment_matrix.sh -l 1 -m 3)
cd "$(dirname "$0")/.."
ARGS="$@"
mkdir -p /run/mysqld
pkill -f "socat UNIX-LISTEN:/run/mysqld" 2>/dev/null
setsid socat UNIX-LISTEN:/run/mysqld/mysqld.sock,fork TCP:127.0.0.1:3306 </dev/null >/dev/null 2>&1 &
sleep 1
(./server -p 9006 $ARGS >/dev/null 2>&1 &)
sleep 1
echo "--- 参数: ${ARGS:-默认} ---"
for TIER in "4 100" "8 1000"; do
    set -- $TIER
    R=$(wrk -t$1 -c$2 -d10s http://127.0.0.1:9006/ 2>/dev/null | grep -E "Requests/sec|Socket errors" | tr '\n' ' ')
    echo "t$1c$2: $R"
done
pkill -f "./server -p 9006" 2>/dev/null
pkill -f "socat UNIX-LISTEN:/run/mysqld" 2>/dev/null
exit 0
