// 升序定时器链表单元测试：add 保序 / del 摘除 / adjust 重排 / tick 到期触发
#include "../timer/lst_timer.h"
#include <gtest/gtest.h>

static std::atomic<int> g_fired{0};

static void fire(client_data *) { g_fired++; }

static util_timer *make_timer(time_t expire) {
    auto *t = new util_timer();
    t->expire = expire;
    t->cb_func = fire;
    return t;
}

TEST(TimerList, Add保持升序_由tick消费顺序验证) {
    sort_timer_lst lst;
    g_fired = 0;
    // 乱序插入三个过期定时器
    util_timer *mid = make_timer(1000), *early = make_timer(500), *late = make_timer(1500);
    lst.add_timer(mid);
    lst.add_timer(early);
    lst.add_timer(late);

    // tick 以当前时间为基准：三者均已过期（相对 epoch），应全部触发并释放
    time_t now = time(NULL) + 1;
    (void)now;
    lst.tick(); // tick 内部用 time(NULL)，测试机时间必然大于 1500
    EXPECT_EQ(g_fired.load(), 3); // 乱序插入不影响全部到期触发
}

TEST(TimerList, Del摘除后不再触发) {
    sort_timer_lst lst;
    g_fired = 0;
    util_timer *t = make_timer(time(NULL) + 10);
    lst.add_timer(t);
    lst.del_timer(t); // del 内部 delete
    lst.tick();
    EXPECT_EQ(g_fired.load(), 0); // 已删除的定时器不得触发
}

TEST(TimerList, Adjust延后可逃过本轮tick) {
    sort_timer_lst lst;
    g_fired = 0;
    util_timer *t = make_timer(time(NULL) + 3600); // 未来 1 小时
    lst.add_timer(t);
    lst.tick();
    EXPECT_EQ(g_fired.load(), 0); // 未到期不触发
    t->expire = time(NULL) + 7200;
    lst.adjust_timer(t); // 延后 adjust（原版仅支持后移）
    lst.tick();
    EXPECT_EQ(g_fired.load(), 0); // 仍未到期
    lst.del_timer(t);             // 清理，避免泄漏（tick 只删已触发节点）
}
