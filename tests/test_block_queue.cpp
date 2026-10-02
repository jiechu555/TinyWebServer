// 阻塞队列单元测试：环形语义/满队拒绝/超时唤醒
#include "../log/block_queue.h"
#include <gtest/gtest.h>
#include <thread>

TEST(BlockQueue, PushPop保序) {
    block_queue<int> q(4);
    ASSERT_TRUE(q.push(1));
    ASSERT_TRUE(q.push(2));
    ASSERT_TRUE(q.push(3));
    int v = 0;
    ASSERT_TRUE(q.pop(v));
    EXPECT_EQ(v, 1); // FIFO：先入先出
    ASSERT_TRUE(q.pop(v));
    EXPECT_EQ(v, 2);
}

TEST(BlockQueue, 满队拒绝push) {
    block_queue<int> q(2);
    EXPECT_TRUE(q.push(1));
    EXPECT_TRUE(q.push(2));
    EXPECT_FALSE(q.push(3)); // 容量 2：第三次应被拒绝而非覆盖
    EXPECT_EQ(q.size(), 2);
}

TEST(BlockQueue, 环形回绕后保序) {
    block_queue<int> q(2);
    q.push(1);
    q.push(2);
    int v;
    q.pop(v); // 出队 1，腾出 1 格
    ASSERT_TRUE(q.push(3)); // 回绕写入
    q.pop(v);
    EXPECT_EQ(v, 2); // 顺序仍正确
    q.pop(v);
    EXPECT_EQ(v, 3);
}

TEST(BlockQueue, 空队pop带超时返回) {
    block_queue<int> q(2);
    int v = -1;
    auto t0 = std::chrono::steady_clock::now();
    bool ok = q.pop(v, 100); // 100ms 超时
    auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(
                       std::chrono::steady_clock::now() - t0).count();
    EXPECT_FALSE(ok);         // 无数据应超时失败
    EXPECT_GE(elapsed, 90);   // 且确实等待了（留 10ms 时钟容差）
    EXPECT_LT(elapsed, 2000); // 但没有死等
}

TEST(BlockQueue, 并发pushPop总量守恒) {
    block_queue<int> q(1000);
    const int N = 5000;
    std::thread producer([&] {
        for (int i = 0; i < N; i++)
            while (!q.push(i))
                std::this_thread::yield(); // 满则让出重试
    });
    int received = 0;
    std::thread consumer([&] {
        int v;
        while (received < N)
            if (q.pop(v))
                received++;
    });
    producer.join();
    consumer.join();
    EXPECT_EQ(received, N); // 5000 个经生产消费不丢不重（值序不作断言：多生产者下非确定）
}
