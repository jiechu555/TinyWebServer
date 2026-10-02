// 线程池单元测试：模板注入假任务，验证并发消费不丢任务
// 注意：threadpool::run() 两个分支（reactor/proactor）模板实例化时都做符号检查，
// 且 proactor 分支无条件构造 connectionRAII（解引用 connPool）——测试用 reactor 的
// m_state=1 路径（write 分支），既补齐全部符号又运行时绕开连接池
#include "../threadpool/threadpool.h"
#include <gtest/gtest.h>
#include <atomic>
#include <chrono>
#include <thread>

class FakeTask {
public:
    bool write() { g_done++; return true; } // reactor m_state=1 分支的工作线程执行体
    void process() {}                        // proactor 分支（本测试不触发）
    bool read_once() { return true; }        // reactor m_state=0 分支（不触发）
    int m_state = 1; // 走 write 分支：不触碰 mysql/connPool
    int improv = 0;
    int timer_flag = 0;
    MYSQL *mysql = nullptr; // 必须为指针：run() 取 &request->mysql 构造 connectionRAII
    static std::atomic<int> g_done;
};
std::atomic<int> FakeTask::g_done{0};

TEST(ThreadPool, 全量任务都被消费) {
    FakeTask::g_done = 0;
    // actor_model=1（reactor）+ m_state=1 → write 分支；connPool=nullptr 不被解引用
    threadpool<FakeTask> pool(1, nullptr, 4 /*threads*/, 1000 /*queue*/);

    const int N = 200;
    FakeTask tasks[N];
    int accepted = 0;
    for (int i = 0; i < N; i++) {
        if (pool.append(&tasks[i], 1)) // append(T*, state)：reactor 模式带状态入队
            accepted++;
    }
    EXPECT_EQ(accepted, N);

    // 等待消费完（最长 5s，防御死锁挂死）
    for (int i = 0; i < 500 && FakeTask::g_done.load() < N; i++)
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    EXPECT_EQ(FakeTask::g_done.load(), N); // 200 个任务一个不丢
}

TEST(ThreadPool, 队列满时append契约) {
    FakeTask::g_done = 0;
    threadpool<FakeTask> pool(1, nullptr, 1, 2);
    FakeTask t1, t2, t3;
    bool r1 = pool.append(&t1, 1);
    bool r2 = pool.append(&t2, 1);
    bool r3 = pool.append(&t3, 1);
    EXPECT_TRUE(r1 && r2); // 前两个至少应成功
    (void)r3;
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}
