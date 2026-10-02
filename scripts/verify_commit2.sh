#!/bin/bash
# commit 2 验证：场景A（正常启动）+ 场景B（user表不可读 → fail-fast 不再段错误）
# 用法: ./verify_commit2.sh A|B   （场景B需先把 user 表改名）
cd "$(dirname "$0")/.."

# libmysqlclient localhost → Unix socket 桥
mkdir -p /run/mysqld
pkill -f "socat UNIX-LISTEN:/run/mysqld" 2>/dev/null
setsid socat UNIX-LISTEN:/run/mysqld/mysqld.sock,fork TCP:127.0.0.1:3306 </dev/null >/dev/null 2>&1 &
sleep 1

LOG=$(ls -t *_ServerLog 2>/dev/null | head -1)
BEFORE=$( [ -f "$LOG" ] && wc -l < "$LOG" || echo 0)

./server -p 9006 >/dev/null 2>&1 &
SRV=$!
sleep 2

if kill -0 $SRV 2>/dev/null; then
    CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://127.0.0.1:9006/)
    echo "进程存活, HTTP=$CODE, 日志新增:"
    tail -n +$((BEFORE+1)) "$LOG" 2>/dev/null | head -3
    kill $SRV 2>/dev/null
    [ "$CODE" = "200" ] && echo "场景A: PASS" || echo "场景A: FAIL(非200)"
else
    wait $SRV; RC=$?
    echo "进程已退出, RC=$RC, 日志新增:"
    tail -n +$((BEFORE+1)) "$LOG" 2>/dev/null | head -3
    if [ "$RC" = "1" ]; then echo "场景B: PASS(fail-fast 退出码1, 无段错误)"; else echo "场景B: FAIL(异常退出码 $RC — 段错误是139)"; fi
fi
pkill -f "socat UNIX-LISTEN:/run/mysqld" 2>/dev/null
exit 0
