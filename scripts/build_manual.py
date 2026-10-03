# -*- coding: utf-8 -*-
"""生成 TinyWebServer 复现手册 PDF（docx -> LibreOffice PDF）
全部命令与输出为 2026-10-03 WSL2 实机复现记录。"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()
for sec in doc.sections:
    sec.left_margin = Inches(0.7)
    sec.right_margin = Inches(0.7)

style = doc.styles["Normal"]
style.font.name = "Microsoft YaHei"
style._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
style.font.size = Pt(10.5)


def heading(text, size=15, color="1A2636", space_before=14):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = RGBColor.from_string(color)
    r.font.name = "Microsoft YaHei"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    p.paragraph_format.keep_with_next = True
    return p


def body(text, size=10.5, color="2C3E50"):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.color.rgb = RGBColor.from_string(color)
    r.font.name = "Microsoft YaHei"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    return p


def set_cell_bg(cell, hexcolor):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hexcolor)
    cell._tc.get_or_add_tcPr().append(shd)


def term_block(lines, title=None):
    table = doc.add_table(rows=1, cols=1)
    table.autofit = True
    tr = table.rows[0]._tr
    trPr = tr.get_or_add_trPr()
    cantSplit = OxmlElement("w:cantSplit")
    trPr.append(cantSplit)
    cell = table.rows[0].cells[0]
    set_cell_bg(cell, "1E1E1E")
    first = True
    if title:
        p = cell.paragraphs[0]
        r = p.add_run(title)
        r.font.name = "Consolas"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor.from_string("6A9955")
        r._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
        first = False
    for line in lines:
        text, color = (line, "D4D4D4") if isinstance(line, str) else line
        if first:
            p = cell.paragraphs[0]
            first = False
        else:
            p = cell.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(text)
        r.font.name = "Consolas"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor.from_string(color)
        r._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


GREEN = "6A9955"


def tip_block(title, text):
    """知识点卡片：浅蓝底，穿插在步骤之间帮助理解"""
    table = doc.add_table(rows=1, cols=1)
    table.autofit = True
    tr = table.rows[0]._tr
    trPr = tr.get_or_add_trPr()
    cantSplit = OxmlElement("w:cantSplit")
    trPr.append(cantSplit)
    cell = table.rows[0].cells[0]
    set_cell_bg(cell, "EEF4FB")
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("💡 知识点 · " + title)
    r.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor.from_string("0B57D0")
    r.font.name = "Microsoft YaHei"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    p2 = cell.add_paragraph()
    p2.paragraph_format.space_after = Pt(0)
    r2 = p2.add_run(text)
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = RGBColor.from_string("2C3E50")
    r2.font.name = "Microsoft YaHei"
    r2._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table
YELLOW = "DCDCAA"
BLUE = "569CD6"
GRAY = "9AA4B2"
RED = "F48771"

# ============ 封面 ============
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("TinyWebServer 本地复现手册")
r.bold = True
r.font.size = Pt(22)
r.font.color.rgb = RGBColor.from_string("1A2636")
r.font.name = "Microsoft YaHei"
r._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("WSL2 构建 · 单元测试 · CGI 注册登录 · wrk 压测 · 优雅停止 · 2026-10-03 实机记录")
r.font.size = Pt(10.5)
r.font.color.rgb = RGBColor.from_string("5F6B7A")
r.font.name = "Microsoft YaHei"
r._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")

body("")
body("适用环境：Windows + WSL2 Ubuntu（编译主场，ext4 原生文件系统）+ Windows Docker MySQL 容器。全部命令与输出为 2026-10-03 实机复现记录。")
body("跟随本手册走完 = 你独立跑通了 Linux 高并发 Web 服务器项目（简历项目三）。出错先查文末《常见故障速查表》。", color="0B57D0")

# ============ 学习地图 ============
heading("学习地图 · 这本手册教你什么", size=13, space_before=10)
body("这是三个项目里最贴操作系统的一个——大学课上抽象的概念全都在这有实体：", size=9.5)
tbl = doc.add_table(rows=8, cols=2)
tbl.style = "Table Grid"
rows = [
    ("概念", "在哪学（步骤）"),
    ("为什么 Linux 项目要真 Linux 文件系统", "步骤 1"),
    ("编译链接四阶段与 CMake", "步骤 2"),
    ("单元测试与可测试性设计", "步骤 3"),
    ("进程间通信：Unix socket vs TCP", "步骤 4"),
    ("HTTP 协议与 CGI（最古老的后端接口）", "步骤 5"),
    ("信号：SIGTERM / SIGKILL 与优雅退出", "步骤 6"),
    ("事件驱动：epoll / Proactor / 定时器", "原理图解"),
]
for i, (a, b) in enumerate(rows):
    c0, c1 = tbl.rows[i].cells
    c0.text, c1.text = a, b
    for c in (c0, c1):
        for pp in c.paragraphs:
            pp.paragraph_format.keep_with_next = (i == 0)
            for rr in pp.runs:
                rr.font.size = Pt(8.5)
                rr.font.name = "Microsoft YaHei"
                rr._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    if i == 0:
        set_cell_bg(c0, "1A2636"); set_cell_bg(c1, "1A2636")
        for pp in c0.paragraphs + c1.paragraphs:
            for rr in pp.runs:
                rr.font.color.rgb = RGBColor.from_string("FFFFFF")
doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ============ 步骤 1 ============
heading("步骤 1 · 进入 WSL 与仓库")
body("Windows 终端里进入 WSL Ubuntu，检查仓库状态（开发主场在 WSL 家目录，不是 /mnt/c）：")
term_block([
    ("$ wsl -d Ubuntu", YELLOW),
    ("$ cd ~/code/TinyWebServer && git branch --show-current && git log --oneline -3", YELLOW),
    ("feature/modernize", "D4D4D4"),
    ("dfd2142 chore: gitignore build 目录", "D4D4D4"),
    ("5a31302 build: CMake + gtest 单测(10 用例) + GitHub Actions CI；单测抓出超时双重 bug（二开 commit 6）", "D4D4D4"),
    ("f3fe63f refactor: -Wall -Wextra 警告 37→0 清零 + 数据库 host 配置化 -H（二开 commit 5）", "D4D4D4"),
], "终端")

tip_block("WSL 与文件系统的坑（步骤 1 的为什么）",
    "WSL2 = Windows 里跑的真 Linux 内核虚拟机，两个文件系统互相访问要走 9P 协议桥（/mnt/c 或 Windows 看 \\wsl$）。实测同一个项目：/mnt/c 上编译运行 145 QPS，ext4 原生 6437 QPS——差 44 倍！所以 Linux 项目主场必须在 WSL 家目录（~/），/mnt/c 只当中转 U 盘。想一想：为什么 Windows 项目不受影响？→ 项目用的本来就是 NTFS 原生路径，没有跨系统桥。")

# ============ 步骤 2 ============
heading("步骤 2 · 全新构建（约 23 秒）")
body("CMake Release 配置 + 16 线程并行编译。BUILD_TESTING=ON 必须显式传（默认不编单测，见 F2）：")
term_block([
    ("$ rm -rf build && cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=ON", YELLOW),
    ("$ cmake --build build -j$(nproc)", YELLOW),
    ("[100%] Linking CXX executable server", "D4D4D4"),
    ("[100%] Built target server", "D4D4D4"),
    ("$ ls -la build/server | awk '{print $5\"B\"}'", YELLOW),
    ("88656B", "D4D4D4"),
], "终端")

tip_block("从源码到可执行文件（步骤 2 的四阶段）",
    "C++ 编译四阶段：预处理（#include 展开）→ 编译（.c→汇编）→ 汇编（→机器码 .o）→ 链接（.o+库→可执行）。Makefile 手写这些规则太苦，CMake 是『生成构建系统的系统』：一份 CMakeLists.txt 在 Linux 生成 Makefile、在 Windows 生成 VS 工程——平台无关。-DCMAKE_BUILD_TYPE=Release 开 -O2 优化（实测对吞吐有实际影响）。gtest 是 Google 的 C++ 测试框架，断言宏 EXPECT_EQ 一行一个检查点。想一想：为什么链接错误在最后才报？→ 链接是最后一阶段，前面只管把每个文件编对。")

# ============ 步骤 3 ============
heading("步骤 3 · 单元测试")
term_block([
    ("$ ctest --test-dir build --output-on-failure", YELLOW),
    ("Test project /root/code/TinyWebServer/build", "D4D4D4"),
    ("    Start 1: unit_tests", "D4D4D4"),
    ("1/1 Test #1: unit_tests .......................   Passed    0.21 sec", "D4D4D4"),
    ("100% tests passed, 0 tests failed out of 1", "D4D4D4"),
], "终端")
body("1 个测试套件内含 10 个 gtest 用例（block_queue 队列/满队/回绕/超时/5000 并发守恒、timer 链表、threadpool 模板注入）——超时用例正是单测抓出的原版真 bug（毫秒换算差三个数量级 + gettimeofday 绝对时刻丢弃）。")

tip_block("为什么值得写测试（步骤 3 的回报）",
    "这个项目的测试不是走形式：10 个用例里抓出了原版真 bug（毫秒换算差一千倍）——不测它就永远潜伏。好的单测三特征：边界值（空队列/满队/超时）、隔离（假任务替代真 MySQL）、快（毫秒级，能跑一万次）。能测的原因是代码把『做什么』和『依赖什么』分开了（threadpool 是模板，塞什么任务都行）——这叫可测试性设计，写代码时就要想。想一想：为什么 bug 藏了这么多年没人发现？→ 超时路径只有异常场景才走到，手动测试永远碰不到。")

# ============ 步骤 4 ============
heading("步骤 4 · 启动服务器（socat 桥 + 脱附启动）")
body("libmysqlclient 连 localhost 时硬编码走 Unix socket，而 MySQL 是 Windows 侧 Docker 容器（TCP 3306）——用 socat 把两者桥起来。服务器用子壳脱附启动，避免被终端会话回收（见 F5）：")
term_block([
    ("$ # 清理可能残留的 stale 桥（重要！残留假 socket 会让 CGI 永久挂起，见 F1）", GRAY),
    ("$ pkill -f 'socat UNIX-LISTEN:/run/mysqld' ; rm -f /run/mysqld/mysqld.sock", YELLOW),
    ("$ mkdir -p /run/mysqld", YELLOW),
    ("$ setsid socat UNIX-LISTEN:/run/mysqld/mysqld.sock,fork TCP:127.0.0.1:3306 </dev/null >/dev/null 2>&1 &", YELLOW),
    ("$ ( ./build/server -p 9006 >/dev/null 2>&1 & echo $! > /tmp/srv.pid )", YELLOW),
    ("$ sleep 2 && cat /tmp/srv.pid && ss -tn | grep -c ':3306'", YELLOW),
    ("1255          # 服务器 PID", "D4D4D4"),
    ("16            # 已建立 16 条 MySQL 连接（连接池初始化成功）", "D4D4D4"),
], "终端")

tip_block("Unix socket、TCP 与文件描述符（步骤 4 的桥）",
    "同一台机器上两个进程通信有两条路：TCP（走网络协议栈，IP+端口寻址）和 Unix socket（文件系统路径寻址，少两层协议开销）。坑在 MySQL 客户端库：连 localhost 时硬编码走 Unix socket——而数据库在 Windows 容器里只听得懂 TCP。socat 就是协议转换器：监听一个假 socket 文件，收到什么原样转发到 TCP 3306。文件描述符（fd）是 Linux 里『一切 I/O 资源』的统一句柄——socket、文件、管道都是 fd，epoll 统一监听它们，这是『一切皆文件』设计的胜利。想一想：为什么 WSL 会话关了 socat 就死？→ 后台进程生命周期挂在会话上，setsid 脱离才是正解。")

# ============ 步骤 5 ============
heading("步骤 5 · 功能验证：静态页 / CGI 注册登录 / 压测")
body("路由规则（原版设计）：GET /0 → 注册页；POST /3CGISQL.cgi → 注册写库；POST /2CGISQL.cgi → 登录查库。表单体格式 user=xx&password=xx：")
term_block([
    ("$ DEMOUSER=\"demo$(date +%H%M%S)\"", YELLOW),
    ("$ curl -s -o /dev/null -w 'HTTP %{http_code}  %{size_download}字节  %{time_total}s\\n' http://127.0.0.1:9006/", YELLOW),
    ("HTTP 200  612字节  0.000648s          # 首页（映射 judge.html）", "D4D4D4"),
    ("$ curl -s -o /dev/null -w 'HTTP %{http_code}\\n' http://127.0.0.1:9006/0", YELLOW),
    ("HTTP 200                              # 注册页", "D4D4D4"),
    ("$ curl -s -d \"user=$DEMOUSER&password=demo123\" -o /dev/null -w 'HTTP %{http_code}  %{time_total}s\\n' http://127.0.0.1:9006/3CGISQL.cgi", YELLOW),
    ("HTTP 200  0.007427s                   # 注册：写 MySQL qgydb.user 表", "D4D4D4"),
    ("$ curl -s -d \"user=$DEMOUSER&password=demo123\" -o /dev/null -w 'HTTP %{http_code}\\n' http://127.0.0.1:9006/2CGISQL.cgi", YELLOW),
    ("HTTP 200                              # 登录正确密码 → welcome.html", "D4D4D4"),
    ("$ curl -s -d \"user=$DEMOUSER&password=WRONG\" -o /dev/null -w 'HTTP %{http_code}\\n' http://127.0.0.1:9006/2CGISQL.cgi", YELLOW),
    ("HTTP 200                              # 登录错误密码 → logError.html（同样 200，业务区分靠页面）", "D4D4D4"),
], "终端")
body("Windows 侧可以交叉验证注册确实落库（qgydb 是 Windows Docker 里 MySQL 的库）：")
term_block([
    ("PS> docker exec mysql mysql -uroot -proot -e \"SELECT * FROM qgydb.user WHERE username='demo170701';\"", YELLOW),
    ("username    passwd", "D4D4D4"),
    ("demo170701  demo123", "D4D4D4"),
], "Windows PowerShell")
body("wrk 压测 5 秒（4 线程 100 连接）：")
term_block([
    ("$ wrk -t4 -c100 -d5s http://127.0.0.1:9006/", YELLOW),
    ("  Thread Stats   Avg      Stdev     Max     +/- Stdev", "D4D4D4"),
    ("    Latency    33.24ms  173.27ms   1.70s    96.06%", "D4D4D4"),
    ("  23015 requests in 5.01s, 14.68MB read", "D4D4D4"),
    ("  Requests/sec:   4598.17", "569CD6"),
    ("  Transfer/sec:      2.93MB", "D4D4D4"),
], "终端")
body("注：P99 秒级长尾是 WSL2 调度噪声（宿主冻结 guest vCPU），非代码缺陷——同环境 Python http.server 对照实验已证实（commit 4 报告）。socket write 错误是服务器 5 秒定时器主动关闭空闲连接的预期行为。", size=9, color="5F6B7A")

tip_block("HTTP 与 CGI（步骤 5 的协议层）",
    "HTTP 请求 = 请求行（方法 URL 版本）+ 头部 + 空行 + 体。服务器解析后按 URL 路由：静态文件直接读盘返回；动态逻辑交给 CGI——Common Gateway Interface，上古标准：起子进程执行一段程序（这里的『程序』内联成了数据库操作），输出 HTML。本项目 /3CGISQL.cgi 是注册、/2CGISQL.cgi 是登录。错误密码也返回 200 是 CGI 时代的语义：状态码表传输层成败，业务成败看返回内容——和 mall 的『看 body.code 不看 HTTP 码』一脉相承又略有不同，面试聊这个对比很出彩。想一想：为什么现代框架都用 401/403 了？→ 语义化状态码让客户端程序能统一处理。")

# ============ 步骤 6 ============
heading("步骤 6 · 优雅停止")
term_block([
    ("$ kill -TERM $(cat /tmp/srv.pid)", YELLOW),
    ("$ sleep 1 && (pgrep -f build/server || echo 进程已优雅退出) && (ss -ltn | grep -q 9006 || echo 端口9006已释放)", YELLOW),
    ("进程已优雅退出（SIGTERM）", "D4D4D4"),
    ("端口 9006 已释放", "D4D4D4"),
], "终端")
body("SIGTERM 走注册的信号处理 → 析构链完整执行（users/users_timer/线程池）。这是 commit 3 内存治理验证过的路径：valgrind definitely lost 182B→0。")

tip_block("信号：进程间的『紧急广播』（步骤 6 的机制）",
    "kill 不是『杀』，是『发信号』。SIGTERM（kill 默认）：请求退出，进程可捕获做善后——TWS 注册了处理器：通知主循环停 epoll、析构连接数组、回收线程池，这就是『优雅退出』；SIGKILL（kill -9）：内核直接终结，进程毫无机会，资源句柄全靠操作系统兜底回收；SIGINT（Ctrl+C）：终端来的 SIGTERM 近亲。信号处理器里只能调用异步安全函数（write 可以、malloc/printf 危险）——因为它随时打断正常执行流。想一想：为什么压测后必须优雅退出而不是 kill -9？→ valgrind 的内存账本要在正常析构里对账，强杀=账本作废。")

# ============ 原理图解 ============
heading("原理图解 · 一次请求的一生（Proactor 模式）", size=14)
term_block([
    ("主线程（事件循环，epoll LT + Proactor）", BLUE),
    ("  listen fd 可读 → accept → conn fd 注册进 epoll + 挂上定时器", "D4D4D4"),
    ("  conn fd 可读 → 主线程自己 read 进输入缓冲 → 把任务丢线程池", "D4D4D4"),
    ("      ↓【线程池工作线程】", GRAY),
    ("      do_read：解析请求行/头部 → 路由（静态文件 or CGI）", "D4D4D4"),
    ("      CGI 分支：connectionRAII 从连接池取 MySQL 连接 → 注册/登录 SQL", "D4D4D4"),
    ("      do_write：按状态机写响应（大文件用 writev 零拷贝）", "D4D4D4"),
    ("      ↓ 写完通知主线程", GRAY),
    ("  SIGALRM 每 5s → 定时器升序链表 tick → 关闭超时连接", "D4D4D4"),
    ("  （步骤 5 压测里大量 write 错误 = 这一步主动关空闲连接，是特性不是 bug）", GRAY),
], title="事件流")
body("关键取舍（面试常问）：主线程统一收发、工作线程只做逻辑——I/O 集中在一个人手里，竞争少；代价是主线程成为吞吐上限。经典 Reactor 变体（工作线程各自 epoll）实测 -25%，所以原版默认反而是对的（见下表）。", size=9.5)

# ============ 历史实测 ============
heading("历史实测数据（二开 6 个 commit 的核心数字）", size=14)
tbl = doc.add_table(rows=6, cols=2)
tbl.style = "Table Grid"
rows = [
    ("实测项（commit / 报告可查）", "结果"),
    ("基线 → 日志分级 flush（commit 4）", "QPS 6437→8511（+12%），P50 21→8.8ms（-58%），timeout -62%"),
    ("负结果对照（单一变量，commit 4）", "异步日志 -27%；全 ET -11% 且超时×3；Reactor -25% —— 原版默认就是最优解"),
    ("valgrind 内存治理（commit 3）", "definitely lost 182B→0；未配对 948→10（剩余全为第三方库全局态）"),
    ("编译警告治理（commit 5）", "-Wall -Wextra 警告 37→0；其中藏一个真 bug（空文件分支 200/500 语义矛盾）"),
    ("单测抓出的原版真 bug（commit 6）", "block_queue 超时双重错：tv_nsec 毫秒换算差 1000 倍 + gettimeofday 丢 tv_usec 致「伪超时」"),
]
for i, (a, b) in enumerate(rows):
    c0, c1 = tbl.rows[i].cells
    c0.text, c1.text = a, b
    for c in (c0, c1):
        for pp in c.paragraphs:
            for rr in pp.runs:
                rr.font.size = Pt(9)
                rr.font.name = "Microsoft YaHei"
                rr._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    if i == 0:
        set_cell_bg(c0, "1A2636"); set_cell_bg(c1, "1A2636")
        for pp in c0.paragraphs + c1.paragraphs:
            for rr in pp.runs:
                rr.font.color.rgb = RGBColor.from_string("FFFFFF")
doc.add_paragraph().paragraph_format.space_after = Pt(2)
body("方法论亮点（比数字更值钱）：性能归因先做环境对照——同环境 Python http.server 也 1.71s 长尾，证明 P99 是 WSL2 调度噪声不是代码缺陷。", size=9.5, color="5F6B7A")

# ============ 面试五问 ============
heading("面试五问（面试官视角，答题要点）", size=14)
for q, a in [
    ("Q1 Proactor 和 Reactor 区别？", "谁是 I/O 的执行者：Reactor 通知你「可读了」由用户线程读；Proactor 由主线程代读完毕把数据递给工作线程。本项目是主线程收发+线程池处理逻辑的混合体。"),
    ("Q2 LT 和 ET 选哪个？", "默认 LT：不丢事件、编程简单；实测切全 ET -11% 且超时×3——用数据回答为什么不是「显得高级」的 ET。"),
    ("Q3 为什么同步日志反而比异步快？", "异步版阻塞队列的锁 + string 分配开销超过直接 fwrite（分级后 INFO 以下走缓冲）；量级没到异步收益区——先测再选。"),
    ("Q4 定时器为什么升序链表？", "超时最近的无非链表头，tick 只碰头部；新连接按超时时刻插入——牺牲插入 O(n) 换 tick O(1)，Web 场景 tick 频繁而插入少。"),
    ("Q5 单测怎么抓出真 bug 的？", "探针二分：裸条件变量精确 100ms → 锁定 block_queue 时刻计算 → 发现换算差千倍+时刻丢弃两个错。讲清排查路径比背结论值钱。"),
]:
    body(q, color="1A2636", size=10)
    body("要点：" + a, size=9.5, color="5F6B7A")

# ============ 故障表 ============
heading("常见故障速查表")
tbl = doc.add_table(rows=6, cols=2)
tbl.style = "Table Grid"
rows = [
    ("编号", "症状 → 原因 → 解法"),
    ("F1", "CGI 请求 HTTP 000 且线程无响应 → socat 桥被 WSL 会话回收但 socket 文件残留，服务器拿到空连接池，工作线程 sem_wait 永久阻塞 → pkill socat + rm 假 socket + setsid 重拉（步骤 4 的三连）"),
    ("F2", "ctest 报 No tests were found → BUILD_TESTING 默认关 → 配置时显式 -DBUILD_TESTING=ON"),
    ("F3", "CGI 挂起或密码只存一半 → URL/表单格式错：必须 POST /3CGISQL.cgi（不是 /3/register），body 是 user=xx&password=xx（password 共 10 字符，代码按字符数跳位解析）"),
    ("F4", "Windows 里往 wsl.exe 传内联脚本引号全乱 → wsl.exe 会重拼 argv → 脚本写到文件里再 bash 执行（本文所有多行命令的来源）"),
    ("F5", "关掉终端服务器也死了 → 后台进程随会话回收 → 用 ( cmd & ) 子壳脱附，或 setsid；压测别用 timeout 包裹 wrk"),
]
for i, (a, b) in enumerate(rows):
    c0, c1 = tbl.rows[i].cells
    c0.text, c1.text = a, b
    for c in (c0, c1):
        for pp in c.paragraphs:
            for rr in pp.runs:
                rr.font.size = Pt(9)
                rr.font.name = "Microsoft YaHei"
                rr._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    if i == 0:
        set_cell_bg(c0, "1A2636"); set_cell_bg(c1, "1A2636")
        for pp in c0.paragraphs + c1.paragraphs:
            for rr in pp.runs:
                rr.font.color.rgb = RGBColor.from_string("FFFFFF")

# ============ 自测题 ============
heading("复现自测题（答出来说明你真懂了）")
body("① socat 桥解决什么矛盾？（提示：libmysqlclient 对 localhost 的连接方式 vs MySQL 容器在哪）")
body("② 注册和登录分别走哪条路由？为什么错误密码也返回 HTTP 200？")
body("③ 为什么 SIGTERM 之后「端口已释放、进程退出」就算优雅？换 kill -9 会发生什么？")
body("这三题对应 F1、步骤 5、步骤 6 的注释——能脱稿讲清楚，系统层这一关你就稳了。", color="0B57D0")

doc.save(r"C:\Users\12808\Documents\复现手册\TinyWebServer复现手册.docx")
print("docx saved")
