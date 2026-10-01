# 基线报告：原版 TinyWebServer 实测（commit 1）

> 2026-10-02 实测。环境：WSL2 Ubuntu 26.04.1（ext4 原生路径）/ g++ 15.2.0 / MySQL 8（Windows Docker，mirrored 网络 + socat 桥）/ wrk 4.1.0 / valgrind 3.26。
> 目的：不改一行代码，先拿真实基线——所有后续优化以此为对照。

## 性能基线（wrk 10s，首页 612B 静态页）

| 档位 | QPS | P50 延迟 | P99 延迟 | timeout |
|---|---|---|---|---|
| t4 c100 | **6437** | 15.2ms | 1.67s | 15 |
| t8 c500 | 6502 | — | — | — |
| t8 c1000 | **6515** | 18.6ms | 1.89s | 64 |

P99 高达秒级 + 1000 连接下 64 次 timeout：高并发下有请求长时间得不到服务（LT 触发 + 单线程事件循环 + 线程池协作模式的排队特征）——后续优化的主攻点。

## 环境变量（压测方法论，面试可讲）

- **drvfs 陷阱**：同一二进制跑在 `/mnt/c`（Windows 盘挂载）仅 **145 QPS**（P50 88ms），WSL 原生 ext4 路径 **6437 QPS**——**44 倍差距**。静态文件服务的 IO 全走文件系统，drvfs 每次文件操作的跨界开销放大了 44 倍。结论：Linux 性能测试必须在原生文件系统做。
- **libmysqlclient 的 localhost 语义**：代码硬编码 `localhost`，MySQL C 客户端对 localhost 走 **Unix socket** 而非 TCP（与直觉相反）；WSL2 mirrored 网络下用 socat 把 `/run/mysqld/mysqld.sock` 桥到 `TCP:127.0.0.1:3306`（Windows Docker MySQL），零代码改动跑通（scripts/run.sh 固化）。

## 启动即崩的 NULL 解引用（二开第一个修复对象）

`http/http_conn.cpp:36`：`initmysql_result` 中 `mysql_query` 失败（如 user 表不存在）只记日志**不返回**，`mysql_store_result` 返回 NULL，`mysql_num_fields(NULL)` 段错误，进程启动即崩。错误处理必须中止初始化，而不是带着 NULL 继续跑。

## valgrind 内存体检（10 个请求）

| 指标 | 值 |
|---|---|
| 堆分配/释放 | 7052 allocs / **6104 frees**（948 次未配对） |
| definitely lost | 182 B / 2 blocks（WebServer 构造 new、mysql_server_init） |
| possibly lost | 56 B+ |
| ERROR SUMMARY | 5 errors |

仅 10 请求即失衡 948 次——每连接的 http_conn 对象、定时器节点、日志缓冲是治理对象。大规模并发后泄漏规模将进一步放大。

## 编译警告（g++ 15 -std=gnu++17 默认）

`log.h:26/47`：返回非 void 的函数无 return 语句（UB）等多个警告。

## 已知问题清单（= 二开 backlog，按价值排序）

1. `initmysql_result` NULL 解引用崩溃（上）
2. 948 次分配未配对 / definitely lost —— 内存治理（智能指针 + RAII）
3. P99 秒级 + 高并发 timeout —— 性能主攻（触发模式/定时器/日志锁竞争逐项对照）
4. `log.h` 无 return UB + 编译警告清零
5. host 硬编码 localhost —— 数据库连接配置化
6. makefile 单文件无增量编译 —— CMake 化 + gtest + CI

## 复现

```bash
# WSL2 Ubuntu 26.04（原生路径 ~/code/TinyWebServer）
make                     # g++ 15 默认编译
./scripts/run.sh 9006    # socat 桥 + 启动
wrk -t4 -c100 -d10s http://127.0.0.1:9006/
valgrind --leak-check=full --log-file=valgrind.log ./server -p 9006
```
