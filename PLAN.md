# 小学生 Tcl + Calibre 学习计划（Tcl 优先 · 四大里程碑）

> 目标：先把 **Tcl 语法学透**，再学 **面向对象（OOP / TclOO）**，最后再用 Tcl 控制 Calibre DESIGNrev（calibredrv）画芯片版图。  
> **每 10 周一个里程碑**：M10（语法核心）→ M20（流畅 + OOP）→ M30（Calibre 核心）→ M40（Calibre 百科）。  
> **Phase C**（GUI 宏）仍放在 40 周之后。覆盖总表：[docs/COVERAGE.md](docs/COVERAGE.md)。
>
> 每周大约 **3～5 次练习**，每次 **30～45 分钟**。不怕慢，怕不练。

---

## 学习原则（贴在墙上）

1. **先玩后懂**：先让程序跑起来，再问「为什么」。
2. **一次只学一个小招**：今天学会 `puts`，明天再学变量。
3. **写小本子**：记下命令、报错、解决办法。
4. **每天一个小作品**：哪怕只打印一行字也算胜利。
5. **大人帮忙开环境**：第 1–20 周主要用 `tclsh`；calibredrv 从第 21 周起由家长/老师按本仓库脚本准备。
6. **查覆盖表**：不确定某个命令归哪一周时，打开 [docs/COVERAGE.md](docs/COVERAGE.md)（周次以本 PLAN 为准）。

---

## 路线图（总览）

| 阶段 | 周次 | 主题 |
|------|------|------|
| **M10 Tcl 语法核心** | 第 1–10 周 | `puts` → dict / 错误处理；毕业：能读懂 Tcl 语法 |
| **M20 Tcl 流畅 + OOP** | 第 11–20 周 | info / I/O / 正则 / namespace / TclOO + **纯 Tcl 毕业作品** |
| **M30 Calibre 核心** | 第 21–30 周 | `layout create` … boolean（原第 7–14 周）+ Catalog B 开头 |
| **M40 Calibre 百科** | 第 31–40 周 | 原 Catalog B 其余章节顺延；第 40 周做覆盖审计 |
| Phase C · GUI | 以后 | `cwbWorkBench`、Writing Macros（batch 完成后再学） |

本仓库已有示例：

- `examples/hello_calibre.tcl` — 在 calibredrv 里打招呼（第 21 周起）
- `examples/create_box.tcl` — 画正方形并写出 GDS
- `examples/inspect_gds.tcl` — 打开 GDS 查看
- `examples/my_graduation.tcl` — Calibre 毕业作品模板（第 24 周可改）
- 完整周课：`lessons/1` …（双语讲义 + 例题）；导读见 `lessons/README.md`
- 覆盖表：`docs/COVERAGE.md`
- 运行方式：前 20 周 `tclsh` / `make weekN`；第 21 周起 `./scripts/run_calibre_tcl.sh` 或 `make weekN`

### 官方手册在哪里（大人先收藏）

本机 Mentor/Siemens 安装里已有 **Calibre DESIGNrev Reference Manual**（批处理 Tcl API 权威来源）：

| 文档 | 本机路径 |
|------|----------|
| Reference（API 大全）PDF | `/data1/eda/eda/mentor/aoi_cal_2017.2_37.29/docs_cal_2017.2_16.14/docs/pdfdocs/calbr_drv_ref.pdf` |
| Reference HTML 目录 | `/data1/eda/eda/mentor/aoi_cal_2017.2_37.29/docs_cal_2017.2_16.14/docs/htmldocs/calbr_drv_ref/calbr_drv_ref_toc.html` |
| User’s Manual PDF | `/data1/eda/eda/mentor/aoi_cal_2017.2_37.29/docs_cal_2017.2_16.14/docs/pdfdocs/calbr_drv_user.pdf` |
| 当前工具版本（setup） | `CALIBRE_HOME=/data1/eda/eda/mentor/aoi_cal_2019.2_26.18`（API 用法与手册一致；查命令以 ref 手册为准） |

手册里和本计划最相关的章节（**第 21 周起**再细读）：

1. **Introduction to Using Tcl With the Calibre Layout Viewers** — handle、Tcl 对象 vs 数据库对象  
2. **Getting Started** — Interactive Shell / Batch / GUI 模式  
3. **Writing Layout Viewer Scripts** — 官方「生成新 layout」示例（Script 1）  
4. **Batch Commands for Layout Manipulation** — `layout create` / `layout peek` / `layout filemerge`  
5. **Layout Object（`$L ...`）** — 本计划第 21–24 周的核心 API  

产品介绍（非完整 API）：[Siemens Calibre DESIGNrev](https://www.siemens.com/en-us/products/ic/calibre-design/interfaces/designrev/)

> 小学生：每周只要学会表里的「本周必会」。大人：卡壳时在 HTML TOC 里搜命令名（如 `create polygon`）。

### 怎样查帮助（本仓库补充）

`tclsh` **没有**内建 `help` 命令；`calibredrv` 主要靠 **少写参数时打印的 Usage:** 行来教语法。本仓库整理了：

| 资源 | 用途 | 怎么用 |
|------|------|--------|
| [docs/COVERAGE.md](docs/COVERAGE.md) | 全部 tclsh / `$L` 命令 → 周次对照 | 查「这个命令在哪一周」 |
| [docs/TCL_HELP.md](docs/TCL_HELP.md) | Tcl / tclsh 怎么自学命令 | 读文档；或 `make help-tcl` |
| [docs/CALIBRE_HELP.md](docs/CALIBRE_HELP.md) | Calibre `layout` / `$L` Usage 速查 | 读文档；或 `make help-calibre` |
| `tools/show_tcl_help.tcl` | 打印本周相关 Tcl 命令名 | `tclsh tools/show_tcl_help.tcl` |
| `tools/show_calibre_help.tcl` | 向 calibredrv 追问 Usage | `./scripts/run_calibre_tcl.sh tools/show_calibre_help.tcl` |
| `lessons/N/lesson_en.md` + `lesson_zh.md` | 每周详细双语讲义 + ≥10 个例题 | `make weekN` / `make weekN-01` |

卡壳时顺序建议：**先跑例题 → 看 Usage / 报错 → 查本周 lesson → 再查手册 HTML TOC**。

---

## OOP 一句话地图（第 15 周起常看）

| OOP 词 | 小学生说法 | Tcl / Calibre 里长什么样 |
|--------|------------|--------------------------|
| **类（class）** | 玩具的「模具图纸」 | `oo::class create Pet { ... }` |
| **对象（object）** | 按模具做出的真实玩具 | `set cat [Pet new "Mimi"]` |
| **方法（method）** | 玩具会做的动作 | `$cat speak` |
| **属性 / 变量** | 玩具身上贴的标签（名字、颜色） | `variable name` |
| **构造** | 「刚做出来时」发生的事 | `constructor {n} { ... }` |

Calibre 里几乎一样（第 21 周起）：

```tcl
set L [layout create]    ;# 做出一个 layout「对象」
$L create cell TOP       ;# 让这个对象去做一件事（方法）
$L create layer 1
```

> 窍门：看到 `$某东西 动词 ...`，多半就是在跟一个对象说话。

---

## 旧周次对照（方便对照旧讲义 / COVERAGE）

| 旧计划 | 新计划 |
|--------|--------|
| 旧第 1–5 周 Tcl 入门 | 新第 1–5 周（第 2 周加强引用/替换） |
| 旧第 6 周 TclOO 入门 | **新第 15 周** |
| 旧第 7–14 周 Calibre 核心 | **新第 21–28 周** |
| 旧第 15–23 周 Catalog A Tcl | **新第 6–14 周** |
| 旧第 24 周 TclOO 进阶 | **新第 16 周** |
| 旧第 25–40 周 Catalog B | **新第 29–40 周**（第 40 周压缩收尾） |

---

# 第一阶段：M10 Tcl 语法核心（第 1–10 周）

> 毕业标准：能读懂常见 Tcl 语法（引用、替换、列表、过程、错误处理），不依赖「背命令」。

---

## 第 1 周 — 电脑会说话：`puts` 与脚本文件

**本周目标**  
让电脑按你的话打印文字；知道什么是 `.tcl` 文件。

**要学的概念（用生活比喻）**

| Tcl 概念 | 生活比喻 |
|----------|----------|
| 脚本 `.tcl` | 给机器人的一张「任务清单」 |
| `puts` | 「请把这句话说出来」 |
| `#` 注释 | 给自己看的小纸条，电脑会忽略 |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 安装/确认能运行 `tclsh`；打印 `Hello, I am learning Tcl!` |
| Day 2 | 打印自己的名字、年龄、喜欢的颜色（各一行） |
| Day 3 | 写 `my_first.tcl`，里面 5 行 `puts`，用 `tclsh my_first.tcl` 运行 |
| Day 4 | 在脚本里加 `#` 注释，解释每一行在干什么 |
| Day 5 | **小作品**：打印一张「自我介绍卡」 |

**本周检查**  
能独立写出并运行一个带注释的 `.tcl` 文件。

**下周预告**  
第 2 周是「语法周」：专门练 `"..."`、`{...}`、`$`、`[ ]`、`\`——把 Tcl 怎么「拆句子」搞清楚。

---

## 第 2 周 — 语法周：变量、引用与替换（重点）

**本周目标**  
会用 `set` 存东西；更重要的是搞清楚 Tcl **怎么读你的句子**：双引号、花括号、美元号、方括号、反斜杠。这是后面所有周的地基。

**要学的概念**

| Tcl 概念 | 生活比喻 | 本周必会 |
|----------|----------|----------|
| `set name "Amy"` | 在盒子上贴标签 `name` | 存与取 |
| `$name` / `${name}` | 打开盒子拿里面的东西 | 变量替换 |
| `"..."` 双引号 | 「半透明包装」——里面的 `$` 和 `[ ]` 还会生效 | 拼句子 |
| `{...}` 花括号 | 「密封包装」——里面几乎原样保留 | 保护特殊字符 |
| `[cmd ...]` 命令替换 | 「先算小纸条，再塞回句子」 | 嵌套命令 |
| `\` 反斜杠 | 「下一个字有特殊任务」 | 换行续行、字面 `$` 等 |
| `expr {$age + 1}` | 算数小计算器 | 简单加减 |

**五种替换对照（建议抄进小本子）**

```tcl
set name "Amy"
set age 10

puts "hello $name"           ;# 双引号：会替换 → hello Amy
puts {hello $name}           ;# 花括号：不替换 → hello $name
puts "sum=[expr {$age + 1}]" ;# 方括号：先跑 expr，再打印
puts "dollar=\$name"         ;# 反斜杠：字面打印 $name
puts "line1\nline2"          ;# 反斜杠：换行
```

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | `set` 三个变量：名字、学校、年级；用 `puts` 打印 |
| Day 2 | **对比实验**：同一句话分别用 `"..."` 和 `{...}`，写出结果差在哪 |
| Day 3 | 练习 `$var` 与 `[expr ...]`：年龄 +1、打印「明年 X 岁」 |
| Day 4 | 练习字面特殊字符：打印含 `$`、`[`、`]` 的说明文字（用 `{}` 或 `\`） |
| Day 5 | **小作品**：「成绩单」— 三门课分数 + 总分；注释里写清哪里用了哪种引用 |

**本周检查**  
- [ ] 能解释：双引号 vs 花括号差在哪  
- [ ] 能用 `$` 和 `[cmd]` 拼出一句话  
- [ ] 能用 `expr` 做简单加减  
- [ ] 遇到「奇怪的字面 `[ ]`」知道用 `{...}` 保护  

**下周预告**  
第 3 周学列表：一串糖果怎么取第几颗。

---

## 第 3 周 — 一串糖果：列表（list）

**本周目标**  
会创建列表、取第几个元素、数有多少个。

**要学的概念**

| Tcl 概念 | 生活比喻 |
|----------|----------|
| `list a b c` | 一串用空格隔开的糖果 |
| `lindex $L 0` | 拿第 1 颗（从 0 开始数！） |
| `llength $L` | 数有几颗 |
| `lappend` | 再往串上加一颗 |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 做「水果清单」列表并打印 |
| Day 2 | 用 `lindex` 打印第 1、第 2、最后一项 |
| Day 3 | 用 `llength` 打印「共有 N 种水果」 |
| Day 4 | 用 `lappend` 加两种新水果 |
| Day 5 | **小作品**：「今日课表」列表 + 打印第几节课 |

**本周检查**  
能创建列表、取值、数长度、追加元素。

**下周预告**  
第 4 周：如果……就……，以及循环重复做事。

---

## 第 4 周 — 如果……就……：条件与循环

**本周目标**  
让程序会判断、会重复做事。

**要学的概念**

| Tcl 概念 | 生活比喻 |
|----------|----------|
| `if {条件} { ... }` | 「如果下雨，就带伞」 |
| `for` / `foreach` | 「把每颗糖果都尝一遍」 |
| `while` | 「没做完就继续做」 |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 分数 ≥ 60 打印 Pass，否则 Fail |
| Day 2 | `foreach` 遍历水果列表，每行打印一种 |
| Day 3 | `for` 打印 1 到 10 |
| Day 4 | `while`：从 5 倒数到 1，再打印「发射！」 |
| Day 5 | **小作品**：猜数字小游戏（大人可先帮写骨架） |

**本周检查**  
能写带 `if` + `foreach` 或 `for` 的小脚本。

**下周预告**  
第 5 周：把重复动作做成 `proc`「小帮手」，并读写简单文件。

---

## 第 5 周 — 小帮手：过程（proc）与文件

**本周目标**  
把重复动作做成「小帮手」；能读写简单文本文件。  
（为第 15 周 OOP 打基础：`proc` ≈ 还没有「主人」的动作）

**要学的概念**

| Tcl 概念 | 生活比喻 |
|----------|----------|
| `proc 名字 {参数} {身体}` | 训练一只会做事的小狗 |
| `return` | 小狗带回结果 |
| `open` / `gets` / `puts` / `close` | 打开本子、读一行、写一行、合上 |
| `file mkdir` / `file join` | 建文件夹、拼路径 |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 写 `proc greet {name} { puts "Hi $name!" }` 并调用 |
| Day 2 | 写 `proc add {a b} { return [expr {$a + $b}] }` |
| Day 3 | 把几句话写入 `tmp/diary.txt` |
| Day 4 | 读回 `tmp/diary.txt` 并打印 |
| Day 5 | **小作品**：「工具箱」— 至少 3 个 proc（问好、加法、打印列表） |

**本周检查**  
独立完成一个小脚本：含变量、列表、`if`、循环、至少一个 `proc`、读写一个文件。

**通往后面的小问题（思考即可）**  
如果有很多宠物，每只都要 `greet`、`speak`，是不是希望「每只宠物自己会说话」？→ 那是第 15 周的对象。先把语法练扎实。

**下周预告**  
第 6 周进入「字符串全家桶」`string`——文字也能切、比、换。

---

## 第 6 周 — 字符串全家桶：`string`

**本周目标**  
学会 `string` 集合命令：量长度、切一段、比大小、换大小写、去空格、查找、替换。

**要学的概念 / 本周必会**

| API | 例子 | 说法 |
|-----|------|------|
| `string length` | `string length "hi"` | 几个字 |
| `string index` / `range` | `string range $s 0 2` | 第几个 / 切一段 |
| `string tolower` / `toupper` / `totitle` | | 大小写 |
| `string trim` / `trimleft` / `trimright` | | 去空格 |
| `string first` / `last` / `match` / `equal` / `compare` | | 找与比 |
| `string map` / `replace` / `repeat` / `reverse` / `cat` | | 变换 |
| `string is` | `string is integer 42` | 是不是某种类型 |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | length / index / range |
| Day 2 | case / trim |
| Day 3 | first / last / match / equal |
| Day 4 | map / replace / repeat |
| Day 5 | **小作品**：`string_toolkit.tcl` — 清洗一行输入文字并报告长度 |

**本周检查**  
能不查笔记用 `length` / `range` / `trim` / `match` / `map`。

**下周预告**  
第 7 周列表进阶：排序、搜索、切片、拆合。

---

## 第 7 周 — 列表进阶

**本周目标**  
在第 3 周基础上，学会排序、搜索、插入、替换、映射、拆合字符串与列表。

**本周必会**

| API | 说法 |
|-----|------|
| `lrange` `lsearch` `lsort` | 切一段、找、排序 |
| `linsert` `lreplace` `lset` | 插入、替换、改某一格 |
| `lmap` `lassign` `lreverse` `lrepeat` | 映射、拆到变量、倒序、重复 |
| `join` `split` `concat` | 列表↔字符串、拼接 |

**每日练习建议**  
Day1 排序名单 · Day2 搜索过滤 · Day3 insert/replace · Day4 join/split · Day5 **小作品**：排序过滤名单并写出 `tmp/week7_roster.txt`

**本周检查**  
能对列表做排序 + 搜索 + 写出文件。

---

## 第 8 周 — `dict` 与 `array`

**本周目标**  
学会「钥匙→盒子」的字典；对比 `array`（另一种标签柜）。

**本周必会**

| 族 | 命令 |
|----|------|
| dict | `dict create` `get` `set` `exists` `for` `keys` `values` `size` |
| array | `array set` `get` `names` `size` `exists` |

**每日练习建议**  
Day1 建 dict · Day2 get/set/exists · Day3 dict for · Day4 array 对照 · Day5 **小作品**：用 dict 存「层号→名字」对照表并打印

**本周检查**  
能解释 dict 与 list 的差别；能读写一层对照表。

---

## 第 9 周 — 表达式与拼装：`expr` / `eval` / `subst` / `format` / `scan`

**本周目标**  
把「算」和「拼句子」练稳：安全 `expr`、字符串格式化、扫描、以及何时才用 `eval`/`subst`。

**本周必会**

| API | 说法 |
|-----|------|
| `expr`（花括号包表达式） | 算数、比较 |
| `incr` `append` `unset` | 加一、拼字、扔掉变量 |
| `format` `scan` | 整齐打印 / 从字串抠数字 |
| `subst` `eval` | 再替换一次 / 把字串当命令跑（小心用） |

**每日练习建议**  
Day1 稳妥 expr · Day2 incr/append · Day3 format 坐标表 · Day4 scan 抠数字 · Day5 **小作品**：用 format 打印整齐的坐标表

**本周检查**  
能写出带 `format` 的表格；知道 `eval` 有风险、能少用就少用。

---

## 第 10 周 — 控制流与错误 + **Milestone 10**

**本周目标**  
学会 `switch`、`catch`、`try`；完成本阶段语法毕业小项目。  
**这是 M10 里程碑周。**

**要学的概念 / 本周必会**

| API | 说法 |
|-----|------|
| `switch` | 多路选择（比一长串 if 更清楚） |
| `catch` | 把可能炸的命令包起来 |
| `try` / `throw` / `error` | 更现代的错误处理（Tcl 8.6+） |
| `break` / `continue` | 跳出 / 跳过本轮循环 |
| `return` 码 | 小帮手带回成功或失败 |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 用 `switch` 把成绩换成等级 A/B/C |
| Day 2 | `catch` 打开不存在的文件，打印友好信息 |
| Day 3 | 试 `try { ... } on error { ... }` |
| Day 4–5 | **M10 毕业小作品**（见下） |

**Milestone 10 毕业项目（选一）**

1. **安全日记本** — `proc` 读写文件；失败时 `catch`/`try` 不崩溃  
2. **命令小词典** — dict 存「命令→一句话解释」；`switch` 选动作  
3. **成绩处理机** — list + string + format + 错误检查  

**Milestone 10 检查清单**

- [ ] 能解释第 2 周五种替换（`" "` `{ }` `$` `[ ]` `\`）  
- [ ] 能独立写含 `proc`、列表或 dict、条件/循环的脚本  
- [ ] 能用 `catch` 或 `try` 处理至少一种错误  
- [ ] 小作品能用 `tclsh` 跑通  
- [ ] （口头）能说：「我已经读得懂常见 Tcl 语法了」  

**下周预告**  
第 11 周起进入 M20：`info` 自省、更深的 I/O、正则、namespace，再到 TclOO，第 20 周交纯 Tcl 大作品。

---

# 第二阶段：M20 Tcl 流畅 + OOP（第 11–20 周）

> 毕业标准：写得出像样的纯 Tcl 脚本（模块感、错误处理、一点 OOP），再去碰 Calibre。

---

## 第 11 周 — `info` 自省

**本周目标**  
让脚本「问问自己」：有哪些命令、变量、过程？版本是多少？

**本周必会**  
`info commands` `vars` `exists` `procs` `args` `body` `script` `tclversion` `nameofexecutable`

**每日练习** Day1 commands/vars · Day2 exists · Day3 procs/args/body · Day4 script/version · Day5 **小作品**：打印「本脚本认识哪些命令」报告  

**本周检查**  
能写一份自省报告脚本。

---

## 第 12 周 — I/O 加深：`chan` / `glob` / `source` / `exec`

**本周目标**  
在第 5 周文件读写之上，学会通道、找文件、载入别的脚本、调用外部命令（谨慎）。

**本周必会**  
`chan`；`read` / `seek` / `tell`；`glob`；`pwd` / `cd`；`source`；`exec` / `pid`；`file` 其余常用子命令（`exists` `size` `mtime` `tail` `rootname` …）

**每日练习** Day1 chan 读写 · Day2 glob 列文件 · Day3 source 小库 · Day4 exec 安全试探 · Day5 **小作品**：列出 `lessons/*/*.tcl` 并计数  

**本周检查**  
能用 `glob` + 循环统计文件；会 `source` 自己的小库。

---

## 第 13 周 — 正则与时间：`regexp` / `clock`

**本周目标**  
从文字里「抠」出模式；学会打印和换算时间。

**本周必会**  
`regexp` `regsub`；`clock seconds` / `format` / `scan` / `add`

**每日练习** Day1 regexp 抽数字 · Day2 多个捕获组 · Day3 regsub · Day4 clock 今天 · Day5 **小作品**：从一行文本抽出数字 + 打印今天日期  

**本周检查**  
能写一个带捕获的 `regexp`；能 `clock format` 打印日期。

---

## 第 14 周 — `namespace` / `package` / 作用域

**本周目标**  
把工具函数放进「自己的房间」（namespace），避免名字打架；认识 `package`、`global`/`upvar`/`variable`。

**本周必会**  
`namespace eval` / `export` / `import`；`package require`；`apply`；`rename`；`global` / `upvar` / `variable`；轻量 `trace`（知道即可）

**每日练习** Day1 namespace eval · Day2 export/import · Day3 global/upvar · Day4 apply/rename · Day5 **小作品**：把工具函数放进自己的 namespace  

**本周检查**  
能写一个带 namespace 的小工具库并 `source` 使用。

---

## 第 15 周 — 会做事的小玩具：TclOO 入门（类、对象、方法）

**本周目标**  
用 Tcl 自带的 **TclOO**（`oo::class`）做出「模具 → 玩具 → 让玩具做事」。  
不要求一次学会所有 OOP 术语；先会写、会改、会讲故事。

**环境**  
继续用 `tclsh`（Tcl 8.6+ 自带 TclOO，一般不必额外安装）。

**要学的概念**

| OOP / TclOO | 生活比喻 |
|-------------|----------|
| `oo::class create ...` | 画出玩具模具 |
| `variable name` | 每个玩具自己的名字标签 |
| `constructor` | 玩具刚做好时要做的事（贴好名字） |
| `method` | 玩具会的动作 |
| `ClassName new ...` | 用模具做出一个真玩具 |
| `$obj methodName` | 对这个玩具喊：「去做某某事！」 |

**最小可运行例子（照抄 → 再改）**

```tcl
oo::class create Pet {
    variable name kind

    constructor {n k} {
        set name $n
        set kind $k
    }

    method introduce {} {
        puts "I am $name, a $kind."
    }

    method speak {} {
        if {$kind eq "cat"} {
            puts "$name: meow!"
        } else {
            puts "$name: woof!"
        }
    }
}

set a [Pet new "Mimi" "cat"]
set b [Pet new "Buddy" "dog"]
$a introduce
$a speak
$b introduce
$b speak
```

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 画图：模具（类）vs 两只真宠物（对象）；标出「方法」气泡 |
| Day 2 | 在 `tclsh` 里跑通上面的 `Pet` 例子 |
| Day 3 | 给 `Pet` 加方法 `rename {newName}`，能改名字再 `introduce` |
| Day 4 | 新建类 `Robot`：属性 `name`，方法 `beep`、`move {steps}` |
| Day 5 | **小作品**：「宠物店」— 至少 1 个类、2 个对象、3 个方法；写进 `examples/my_oop_pets.tcl` |

**可选加分（大人带着试，不强制）**

- 再做一个子类感觉：`oo::class create Cat { superclass Pet ... }`（知道「更专用的模具」即可）
- 用列表装着多个对象：`foreach p [list $a $b] { $p speak }`

**本周检查**  
能用自己的话解释：类 / 对象 / 方法；能独立写出并运行一个小 TclOO 脚本。

**和下周的桥梁**  
第 16 周学继承与 mixin；第 21 周起 Calibre 的 `layout` **用起来就像对象**：

```tcl
set L [layout create]   ;# 很像 Pet new
$L create cell TOP      ;# 很像 $cat speak
```

---

## 第 16 周 — TclOO 进阶

**本周目标**  
在第 15 周之上：继承、mixin、动态增补方法。

**本周必会**  
继承（`superclass`）、mixin、`oo::define` 增补、`oo::objdefine`、`self`、导出方法

**每日练习** Day1 继承 Shape→Box · Day2 覆盖 method · Day3 mixin · Day4 oo::define · Day5 **小作品**：可继承的 `Shape` → `Box` 类  

**本周检查**  
能写出带 `superclass` 的两个类并跑通。

**Bonus（写入 COVERAGE，不单独占主周）：** `binary` `zlib` `socket` `coroutine` `interp` `after`/`vwait` — 电源工具，名字认识即可。

---

## 第 17 周 — 脚本模式：小模块与库

**本周目标**  
学会把脚本组织成「可复用小模块」：`source` 库、`apply`、`rename`、简单 CLI（`argv`）。

**本周必会**  
`source` 多文件；`apply`；`rename`；`info script` 定位库路径；`lindex $argv`；约定 `namespace` + `proc` 导出

**每日练习** Day1 拆两个文件 · Day2 source 相对路径 · Day3 apply 小函数 · Day4 argv 开关 · Day5 **小作品**：`lib/util.tcl` + 主脚本调用  

**本周检查**  
能维护一个 ≥3 个命令的小库，主脚本只负责调用。

---

## 第 18 周 — 复习工坊 A（语法 + 列表/字典）

**本周目标**  
综合第 1–10 周：引用/替换、list、dict、string、错误处理，做一个「小工具合集」。

**本周必会（复习）**  
第 2 周五种替换；`string`/`lsearch`/`dict for`/`catch`

**每日练习** Day1 错题本复习 · Day2 字符串清洗器 · Day3 名单过滤器 · Day4 错误演示 · Day5 **小作品**：`workshop_a.tcl` — 至少组合 4 个命令族  

**本周检查**  
小作品无注释标出用到的周次知识点。

---

## 第 19 周 — 复习工坊 B（I/O + namespace + OOP）

**本周目标**  
综合第 11–17 周：文件扫描、namespace、TclOO，做一个带类的「文件报告器」。

**本周必会（复习）**  
`glob`/`source`/`namespace`/`oo::class`

**每日练习** Day1 glob 扫描 · Day2 namespace 包一层 · Day3 一个 Reporter 类 · Day4 写出报告文件 · Day5 **小作品**：`workshop_b.tcl`  

**本周检查**  
至少 1 个类 + 读目录 + 写报告。

---

## 第 20 周 — 纯 Tcl 毕业作品 + **Milestone 20**

**本周目标**  
不碰 Calibre，交出一份像样的 **纯 Tcl 毕业作品**。  
**这是 M20 里程碑周。**

**毕业项目（选一，鼓励组合）**

1. **迷你通讯录** — dict + 文件读写 + catch + namespace  
2. **作业批改助手** — string/list + format + switch + 友好错误  
3. **小游戏** — 循环 + proc +（加分）TclOO 角色  
4. **个人工具箱** — 多文件 `source` + 至少 1 个类  

**Milestone 20 检查清单**

- [ ] `tclsh` 跑通，有 README 注释说明怎么用  
- [ ] 使用 ≥1 个 namespace **或** ≥1 个 TclOO 类  
- [ ] 有文件 I/O 或 `glob`  
- [ ] 有错误处理（`catch`/`try`）  
- [ ] 能向别人讲清：类/对象/方法（对照 OOP 地图）  
- [ ] （口头）「我准备好用同样的方式去理解 `$L ...` 了」  

**下周预告**  
第 21 周起进入 Calibre：`layout create` 与句柄——带着 OOP 眼镜看 `$L`。

---

# 第三阶段：M30 Calibre 核心（第 21–30 周）

> 提醒：本阶段需要已配置好的 calibredrv 环境（见 `setup_calibredrv.sh`）。  
> 小学生主要学「写脚本 + 看结果」；GUI / VNC 由大人协助打开。  
> **带着第 15 周的 OOP 眼镜看每一行 `$L ...`。**  
> API 说明对齐官方 *Calibre DESIGNrev Reference Manual*（`calbr_drv_ref`）。完整语法以手册为准；下表是学习用「必会子集」。

### 手册里的三类 API（先建立地图）

| 类别 | 长什么样 | 干什么 | 本计划周次 |
|------|----------|--------|------------|
| **A. layout 命令**（全局） | `layout create` / `layout peek` / `layout filemerge` | 造图纸、偷看文件、合并文件 | 第 21、23、27 周 |
| **B. Layout 对象方法** | `$L create polygon ...` / `$L cells` | 对某一张图纸读写、画画、提问 | 第 21–28 周 |
| **C. GUI / Workbench**（选学） | `cwbWorkBench`、`$cwb cget -_layout` | 控制已经打开的桌面窗口 | 第 24 周可选；正式 Phase C |

手册要点（Introduction）：**Tcl Objects Have Handles** — `layout create` 返回的句柄存进 `$L`，之后都写 `$L 方法名 ...`。  
多数几何图形本身不是独立 Tcl 对象，而是通过 `$L` 的方法创建/查询。

---

## 第 21 周 — 启动方式 + API-A：`layout create` 与句柄

**本周目标**  
会跑脚本；理解 **handle（句柄）**；会用空 layout 和从文件打开 layout。

**运行方式（手册 Getting Started）**

| 模式 | 怎么跑 | 小学生怎么用 |
|------|--------|--------------|
| Batch / shell 脚本 | `./scripts/run_calibre_tcl.sh script.tcl`（内部 `calibredrv -shell -s ...`） | **主战场** |
| 打开 GDS 看图 | `calibredrv tmp/xxx.gds`（需 DISPLAY/VNC） | 大人协助「验收」 |
| 交互 shell | `calibredrv -shell` 后手动敲命令 | 可选试玩 |

**本周必会 API**

| API | 手册含义 | 小学生说法 | 最小例子 |
|-----|----------|------------|----------|
| `layout create` | 新建空 layout，返回 handle | 拿出空白图纸 | `set L [layout create]` |
| `layout create $file` | 从 GDS/OASIS 等加载 | 打开已有图纸 | `set L [layout create $gds]` |
| （常用选项）`-dt_expand` | 保留 layer/datatype 区分 | 别把不同颜色层糊成一层 | `layout create $gds -dt_expand` |
| （常用选项）`-preserveProperties` | 保留 property | 保住图纸上的小纸条 | 大人需要时再加 |

手册还支持从 RDB、LEF/DEF、OA、Milkyway 等创建 layout——第 21 周**不必学**，知道「同一条 `layout create` 很能干」即可。

**官方 Script 1 骨架**（Writing Layout Viewer Scripts）

```tcl
set L [layout create]      ;# 空容器：还没有 cell / layer
$L create cell TOP
$L create layer 1
$L create layer 2.7        ;# layer.datatype 写法
$L create polygon TOP 1 0 0 100 100
$L gdsout temp.gds
```

本仓库对照：`examples/hello_calibre.tcl`、`examples/create_box.tcl`。

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | `source setup_calibredrv.sh`；确认 `calibredrv`；打开 HTML TOC 找 `layout create` 那一页（大人带） |
| Day 2 | 跑 `examples/hello_calibre.tcl`；抄写「句柄」三个字到笔记本 |
| Day 3 | 写脚本：空 `layout create` → 打印 `$L` → `exit` |
| Day 4 | OOP 对照表：`Pet new` vs `layout create`；`$cat speak` vs `$L create cell` |
| Day 5 | **小作品**：`my_hello.tcl` — 自我介绍 + 创建空 layout 并 `puts` 句柄 |

**本周检查**  
能解释句柄；能独立用 `./scripts/run_calibre_tcl.sh` 跑脚本。

---

## 第 22 周 — API-B 创建几何：cell / layer / polygon / wire / text + 写出文件

**本周目标**  
按手册 **Layout Object → create\*** 系列，画出多种图形并导出 GDS（或 OASIS）。

**本周必会 API（创建 + 导出）**

| API | 语法要点（手册） | 小学生说法 |
|-----|------------------|------------|
| `$L units microns ?n?` | 设置数据库单位与微米关系 | 定尺子刻度（新建 layout 时常设，如 `1000`） |
| `$L create cell name` | 建 cell | 建一个房间 |
| `$L create layer L` 或 `L.D` | 层号或 `layer.datatype` | 选一张透明彩纸 |
| `$L create polygon cell layer x1 y1 ... xn yn` | **坐标必须是一个个数字**，不是一层 list | 用点连形状 |
| `$L create wire cell layer width x1 y1 ...` | path/导线 | 画有宽度的小路 |
| `$L create text cell layer x y text` | 文字标注 | 在图上写名字 |
| `$L gdsout file ?cell?` | 写出 GDS；可只写某个 cell 层次 | 存成 GDS |
| `$L oasisout file ...` | 写出 OASIS | 另一种图纸格式（知道即可） |

**层号两种写法（都会遇到）**

| 写法 | 例子 | 说明 |
|------|------|------|
| 整数层 | `1` | 手册 Script 1 用法 |
| `layer.datatype` | `1.0` / `2.7` | 手册推荐区分 datatype |
| `layer_datatype` | `1_0` | 本仓库 `create_box.tcl` 用法；以你环境实测为准 |

**坐标 list 小陷阱（很重要）**

手册要求：`create polygon` 的坐标是展开的数字。若变量是 list，要用 `eval`：

```tcl
set coords {0 0 100 0 100 100 0 100}
eval $L create polygon TOP 1.0 $coords
# 等价于：$L create polygon TOP 1.0 0 0 100 0 100 100 0 100
```

**矩形两种写法**

```tcl
# 手册：对角两点即可表示矩形 polygon
$L create polygon TOP 1 0 0 100 100

# 或完整四角（本仓库 create_box.tcl）
$L create polygon TOP 1_0 0 0 100 0 100 100 0 100
```

**综合小例子（多 API）**

```tcl
set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1.0
$L create layer 2.0
$L create polygon TOP 1.0 0 0 100 100
$L create wire TOP 2.0 10 0 50  50 50  100 50
$L create text TOP 1.0 10 110 "HELLO"
$L gdsout tmp/week22_multi.gds TOP
```

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 跑通 `examples/create_box.tcl`；对照手册 Script 1 |
| Day 2 | 改尺寸；试 `1` / `1.0` / `1_0` 哪种在你环境可用，记下来 |
| Day 3 | 加 `$L create text` 写自己名字缩写 |
| Day 4 | 加 `$L create wire` 画一条「小路」；坐标 list + `eval` 练一次 |
| Day 5 | **小作品**：`my_shapes.tcl` — 至少用 **polygon + text**（加分：wire）；写出 `tmp/` |

**本周检查**  
能创建 cell/layer，画 ≥2 种几何，成功 `gdsout`。

**可选**  
GUI 打开 GDS 验收；试 `$L oasisout tmp/week22.oas`。

---

## 第 23 周 — API-A/B 查询：打开、提问、peek（不瞎改）

**本周目标**  
读回 GDS；用查询 API「问图纸问题」；认识 `layout peek`（不完整加载也能偷看）。

**本周必会 API（查询）**

| API | 手册含义 | 小学生说法 |
|-----|----------|------------|
| `layout create $gds` | 加载文件得到 `$L` | 打开图纸 |
| `$L topcell` | 返回 topcell 名 | 最大的房间叫什么 |
| `$L cells` | 列出 cells | 有哪些房间 |
| `$L layers` | 列出 layers | 有哪些彩纸 |
| `$L exists cell name` | cell 是否存在 | 有没有叫 TOP 的房间 |
| `$L exists layer ...` | layer 是否存在 | 有没有这层 |
| `$L bbox cell` | cell 包围盒 | 房间有多大一圈 |
| `$L file` | 关联文件名等信息 | 这张图从哪来 |
| `layout peek $gds -cells` | 不完整加载就列 cell | 隔着窗户数房间 |
| `layout peek $gds -layers` | 偷看有哪些层 | 隔着窗户看彩纸 |
| `layout peek $gds -topcell` | 偷看 topcell | 隔着窗户看大门牌 |
| `layout peek $gds -precision` / `-units` | 精度与单位 | 尺子多细 |

进阶（知道名字即可）：`$L children`、`$L iterator poly|wire|text|ref`、`$L report`。

**报告脚本模板**

```tcl
set gds [lindex $argv 0]
if {$gds eq ""} {
  set gds [file normalize [file join [file dirname [info script]] .. tmp demo_box.gds]]
}
puts "peek cells:  [layout peek $gds -cells]"
puts "peek layers: [layout peek $gds -layers]"
puts "peek top:    [layout peek $gds -topcell]"

set L [layout create $gds -dt_expand]
puts "topcell=[$L topcell]"
puts "cells=[$L cells]"
puts "layers=[$L layers]"
if {[$L exists cell TOP]} {
  puts "bbox TOP = [$L bbox TOP]"
} else {
  puts "no cell TOP"
}
exit
```

对照：`examples/inspect_gds.tcl`。

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | 用第 22 周 GDS；跑 inspect；再写 `layout peek ... -cells/-layers` |
| Day 2 | 打印 `$L topcell`、`$L cells`、`$L layers` |
| Day 3 | `$L exists cell` + `$L bbox`；用 `if` 友好提示 |
| Day 4 | 对比：peek（不加载）vs `layout create`（加载）各打印一次，写一句差别 |
| Day 5 | **小作品**：`report_gds.tcl` — 接受可选路径参数，打印报告 |

**本周检查**  
能打开自己的 GDS，并用 ≥4 个查询 API 打出报告。

---

## 第 24 周 — API 层次：`create ref` + 多 API 毕业作品

**本周目标**  
学会 **cell 引用（placement）**；毕业作品至少组合 **创建 + 几何 + 查询** 三类 API。  
（对应旧计划第 10 周「Core Calibre 毕业」——现在放在 Tcl 扎实之后。）

**本周必会 API（层次）**

| API | 语法要点（手册） | 小学生说法 |
|-----|------------------|------------|
| `$L create ref incell refcell x y mirror angle mag` | 在 `incell` 里放置 `refcell` | 把零件盒摆进大厅 |
| 可选 `cols rows xspace yspace` | 阵列摆放 | 像橡皮图章盖很多个 |
| `$L children` / `$L refcount` | 看引用关系 | 谁装了谁、用了几次 |

最小层次例子：

```tcl
set L [layout create]
$L units microns 1000
$L create cell BOX
$L create layer 1.0
$L create polygon BOX 1.0 0 0 20 20

$L create cell TOP
# 在 TOP 里放两个 BOX：位置 (0,0) 与 (40,0)；不镜像；角度 0；放大 1
$L create ref TOP BOX 0 0 0 0 1
$L create ref TOP BOX 40 0 0 0 1

$L create text TOP 1.0 0 30 "TWO BOXES"
$L gdsout tmp/week24_refs.gds TOP

puts "top=[$L topcell] cells=[$L cells]"
exit
```

**毕业项目（选一，鼓励组合 API）**

1. **双层小房子** — polygon 两层 + text 门牌 + `gdsout` + report  
2. **积木阵列** — 一个小 cell + `$L create ref` 排成 2×2 或一排  
3. **首字母积木** — 多个 polygon（或多个小 cell + ref）拼字母  
4. **OOP 小工厂（加分）** — TclOO 类封装 `addRect` / `place` / `save` / `report`，内部调用 `$L ...`  
5. **GUI 选学（大人）** — 打开 DESIGNrev 后：`set wb [find objects -class cwbWorkBench]`；`set L [$wb cget -_layout]`；`puts [$L cells]`（手册 cwbWorkBench）

**本周日程**

| 天 | 任务 |
|----|------|
| Day 1 | 纸上设计：用到哪些 API（对照下方速查表打勾） |
| Day 2–3 | 实现创建 + 几何 +（推荐）`create ref` |
| Day 4 | 写 report（peek / topcell / cells / bbox）；修 bug |
| Day 5 | **展示日**：演示脚本；口述 3 个用过的 API；放入 `examples/` |

**第 24 周毕业检查清单**

- [ ] `./scripts/run_calibre_tcl.sh` 跑通  
- [ ] 生成 GDS（或 OASIS）  
- [ ] 使用 ≥1 个 **创建** API、≥2 个 **几何** API、≥2 个 **查询** API  
- [ ] （推荐）使用 `$L create ref` 或阵列参数  
- [ ] 能解释：句柄、`$L 方法`、layer/datatype、GDS  
- [ ] （加分）TclOO 封装；或 GUI `cwbWorkBench` 取当前 layout  

---

## 第 25 周 — 遍历图形：`$L iterator`（poly / wire / text）

**本周目标**  
用 `$L iterator` 把某个 cell、某层上的 polygon / wire / text **一个个列出来**。

**本周必会 API**

| API | 语法要点（本机实测） | 小学生说法 |
|-----|----------------------|------------|
| `$L iterator poly cell layers range lo hi` | 例：`$L iterator poly TOP 1 range 0 end` | 把这一层的每个多边形坐标列出来 |
| `$L iterator wire cell layers range lo hi` | 例：`$L iterator wire TOP 2 range 0 end` | 列出每条导线 |
| `$L iterator text cell layers range lo hi` | 例：`$L iterator text TOP 1 range 0 end` | 列出每个文字 |
| `foreach` + iterator 结果 | 遍历返回的 list | 一行行打印 |

**每日练习** Day1 iterator poly · Day2 wire/text · Day3 foreach 计数 · Day4 对比 layers vs iterator · Day5 **小作品**：`dump_shapes.tcl`  

**本周检查**  
能对一份自己的 GDS 跑通三种 iterator。

---

## 第 26 周 — 层次展开：`$L flatten` / `expand ref`

**本周目标**  
把「引用别的 cell」变成「本 cell 上真正的多边形」。

**本周必会 API**

| API | 说法 |
|-----|------|
| `$L flatten cell TOP` | 去掉 TOP 里所有 ref，图形画到 TOP 上 |
| `$L flatten cell TOP -withDelete` | 同上，并删掉不再被用的子 cell |
| `$L expand ref` / `$L flatten ref` | 只展开某一个实例 |
| `iterator ref` / `iterator poly` | 展开前后对比 |

**每日练习** Day1 建 BOX+TOP · Day2 flatten cell · Day3 -withDelete · Day4 expand 单个 · Day5 **小作品**：`flatten_report.tcl`  

**本周检查**  
能解释 flatten cell vs expand ref。

---

## 第 27 周 — 拼接版图：`layout filemerge` / `$L import layout`

**本周目标**  
把两份（或多份）小 GDS **拼成一份**。

**本周必会 API**

| API | 说法 |
|-----|------|
| `layout filemerge -in a.gds -in b.gds -out out.gds` | 文件合并 |
| `-createtop` / `-mode append\|overwrite\|rename` | 封面 cell / 重名策略 |
| `-infile` + `placecell` | 合并时按坐标放置 |
| `$L import layout $src $del $mode` | 内存里吸入另一 layout |
| `layout copy $src` | 复印一份（可选） |

**每日练习** Day1 两份小 GDS · Day2 filemerge · Day3 mode/createtop · Day4 import layout · Day5 **小作品**：`merge_kit.tcl`  

**本周检查**  
能说清 filemerge（文件）vs import layout（内存）。

---

## 第 28 周 — 图形运算：`$L AND` / `OR` / `NOT` / `SIZE`

**本周目标**  
像玩「剪纸叠纸」：相交、合并、相减，以及外形胖/瘦一圈。

**本周必会 API**

| API | 说法 |
|-----|------|
| `$L AND` / `OR` / `NOT` / `XOR` | 层运算 |
| `$L SIZE in out by amt` | 放大/缩小一圈 |
| 可选 `-cell TOP` | 只对某个 cell 算 |

**每日练习** Day1 AND · Day2 OR/NOT · Day3 SIZE · Day4 XOR/-cell · Day5 **小作品**：`boolean_poster.tcl`  

**本周检查**  
能解释 AND/OR/NOT；小作品有 GDS + 文字报告。

---

## 第 29 周 — 全局 `layout` 全家桶（Catalog B 开始）

**本周目标**  
补全全局 `layout` 命令族（巩固 filemerge/peek）。

**本周必会**  
`layout all` `delete` `copy` `copy2` `merge` `filtershapes` `droasis` `overlays` `tbmode`

**每日练习** Day1 layout all · Day2 copy/delete · Day3 merge vs filemerge · Day4 其余选项扫一眼 · Day5 **小作品**：列出内存中所有 layout 句柄并清理  

**本周检查**  
能列出并清理句柄，不留「幽灵图纸」。

---

## 第 30 周 — 单位与元数据 + **Milestone 30**

**本周目标**  
掌握单位、精度、文件元数据；完成本阶段 Calibre 核心里程碑回顾。  
**这是 M30 里程碑周（覆盖第 21–30 周）。**

**本周必会**  
`units database|microns|user`；`precision`；`format`；`file`；`layoutType`；`libname`；`readonly`；`ismodified`；`options`

**每日练习** Day1 units · Day2 precision/format · Day3 file/layoutType · Day4 readonly/ismodified · Day5 **小作品** + M30 回顾清单  

**Milestone 30 检查清单**

- [ ] 会 `layout create` / 几何 create / peek 查询 / `create ref`  
- [ ] 会 iterator、flatten、filemerge、boolean 中至少各跑通一次  
- [ ] 能打印单位与是否修改  
- [ ] 有一份可展示的 GDS + 报告脚本  
- [ ] （口头）「我能查手册、给 `$L` 下清楚的命令」  

---

# 第四阶段：M40 Calibre 百科（第 31–40 周）

> 按命令族补全 batch calibredrv。总表：[docs/COVERAGE.md](docs/COVERAGE.md)。  
> 讲义用 `content-generation` 技能按周生成到 `lessons/N/`。

---

## 第 31 周 — 层次查询加深

**本周目标**  
把 cell 关系问清楚：祖先、深度、引用次数。

**本周必会**  
`ancestors` `maxdepth` `refcount` `isReferenced` `duplicate cell` `cellname` `topcell` `viacell`

**小作品**  
打印某 cell 的祖先链。

**本周检查**  
能解释 ancestors vs children。

---

## 第 32 周 — 层管理全家桶

**本周目标**  
给层起名字、查是否为空、配置显示相关属性（batch 能做到的部分）。

**本周必会**  
`layernames` `layerconfigure` `layerFilters` `modify layer` `isLayerEmpty` `customLayerDrawOrder` `loadlayerprops` `MASK_LAYER_INFO`

**小作品**  
给层起名字并查询是否为空。

**本周检查**  
能改层名并验证。

---

## 第 33 周 — `delete` 全家桶

**本周目标**  
先会查再会删：安全删除 cell / layer / 几何 / ref。

**本周必会**  
`delete cell|layer|polygon|polygons|wire|ref|text|clip|objects|duplicate ref`

**小作品**  
建完再安全删掉指定多边形。

**本周检查**  
删除前后用 iterator/`exists` 对照。

---

## 第 34 周 — 修改与变换

**本周目标**  
移动原点、改文字、拷贝几何、缩放与对齐网格。

**本周必会**  
`modify origin` `modify text`；`COPY` `COPYCELL GEOM`；`scale`；`SNAP`；`gridsnap`

**小作品**  
移动原点并写出新 GDS。

**本周检查**  
改前改后 bbox 有可见变化。

---

## 第 35 周 — iterator 计数

**本周目标**  
不只列出图形，还要「人口普查」式计数。

**本周必会**  
`iterator count`（poly/wire/text/ref/sref/aref）

**小作品**  
shape census 报告。

**本周检查**  
一份 GDS 打出各类图形数量表。

---

## 第 36 周 — Clip 与 RDB

**本周目标**  
按区域裁剪；导出 RDB 类报告（以本机 Usage 为准）。

**本周必会**  
`create clip`；`clips`；`clipsout`；`rdbout`

**小作品**  
裁一块区域并导出报告。

**本周检查**  
能解释 clip 与普通 cell 的差别（按手册/实测）。

---

## 第 37 周 — 导出变体

**本周目标**  
同一 layout 导出多种格式。

**本周必会**  
`oasisout`（加深）；`asciiout`；`textout`；`instancedbout`；`report`

**小作品**  
同一 layout 导出两种格式。

**本周检查**  
至少两种输出文件存在于 `tmp/`。

---

## 第 38 周 — 连通与网络

**本周目标**  
按手册 Usage 理解 connect 族（以本机实测为准）。

**本周必会**  
`connect` `disconnect` `stopconnect` `extractNet`

**小作品**  
跑通最小 connect 示例。

**本周检查**  
记下本机可用的参数组合（写入小本子）。

---

## 第 39 周 — Peek 对象加深

**本周目标**  
把 `layout peek` 选项练全：不完整加载也能问很多问题。

**本周必会**  
`layout peek` 全选项（`-cells` `-layers` `-bbox` `-precision` `-units` …）

**小作品**  
不写全打开，peek 出 cell/layer/bbox 清单。

**本周检查**  
同一文件对比 peek vs `layout create` 的信息差异（写 3 句）。

---

## 第 40 周 — 收尾总览 + **Milestone 40**（peek/overlay/transcript/property/工具箱/审计）

**本周目标**  
压缩浏览其余 Catalog 主题，并对照 [docs/COVERAGE.md](docs/COVERAGE.md) 做覆盖审计。  
**这是 M40 里程碑周。**

**本周扫过的主题（每个至少跑 1 个最小例子或标 skip）**

| 主题 | 必会关键词 |
|------|------------|
| Overlay | `overlay create\|all\|delete\|filemerge`；`$L isOverlay` |
| Transcript / 更新 | `transcript`；`holdupdates` `allowupdates` `update`；`pushmarkers`；`ruler` |
| Property | `property`；`srefsFromAref` |
| 工具箱 | 把 create→boolean→flatten→filemerge→gdsout 封成 TclOO 类（可选复用第 24 周加分） |
| 审计 | COVERAGE 状态列；本机不可用 / GUI-only → `phaseC` 或 `skip` |

**每日练习建议**

| 天 | 任务 |
|----|------|
| Day 1 | Overlay 最小例子（或记录 Usage 失败原因） |
| Day 2 | transcript / holdupdates 试一次 |
| Day 3 | property 读写 |
| Day 4 | （可选）工具库类整理进 `examples/` |
| Day 5 | **审计日**：更新 COVERAGE + 写 `tmp/week40_audit.txt` |

**Milestone 40 检查清单**

- [ ] COVERAGE 中 batch 项大多已勾或标了 `skip`/`phaseC`  
- [ ] 有简短审计报告 `tmp/week40_audit.txt`  
- [ ] 能说出：哪些只能 GUI（留给 Phase C）  
- [ ] （口头）「百科周走完了；真正干活仍靠查手册 + 小例子」  

---

## Phase C — GUI（batch Catalog / M40 完成后再开）

| 主题 | 内容 |
|------|------|
| Writing Macros | 官方「写宏」章：命令过程 + GUI plug-in |
| `cwbWorkBench` | TOC 中 `Command_Cwb*`：选择、缩放、层可见、回调 |
| 作品集 | `examples/student_*.tcl` 继续积累 |

---

# 附录 A — CalibreDRV Tcl API 学习速查（手册子集）

> 完整列表见 `calbr_drv_ref` 目录：**Layout Commands** + **Layout Object**。此处只列学习路线上的高频命令。

### A1. layout 命令（全局）

| 命令 | 用途 |
|------|------|
| `layout create` | 空库 / 打开 GDS·OASIS·RDB 等 |
| `layout peek file options...` | 不完整加载，查询 cells/layers/topcell/bbox/precision… |
| `layout filemerge -in a -in b ...` | 合并多个版图 |
| `layout delete` / `layout copy` | 删除、复制 layout 句柄 |

### A2. `$L` 创建 / 修改

| 命令 | 用途 |
|------|------|
| `$L units microns` | 单位 |
| `$L create cell` / `layer` | 结构 |
| `$L create polygon` / `wire` / `text` / `ref` | 几何与层次 |
| `$L create clip` | 按区域/RDB 裁剪 |
| `$L delete cell\|layer\|polygon\|text\|wire\|ref` | 删除（先会查再学删） |
| `$L modify origin` / `modify text` / `modify layer` | 修改 |
| `$L import layout` | 导入另一 layout |

### A3. `$L` 导出

| 命令 | 用途 |
|------|------|
| `$L gdsout` | 写 GDS（可 `.gz`） |
| `$L oasisout` | 写 OASIS |
| `$L rdbout` / `$L asciiout` | RDB / ASCII |

### A4. `$L` 查询 / 遍历

| 命令 | 用途 |
|------|------|
| `$L topcell` / `$L cells` / `$L layers` / `$L layernames` | 结构总览 |
| `$L exists cell\|layer` | 存在性 |
| `$L bbox` / `$L children` / `$L ancestors` | 范围与层次 |
| `$L iterator poly\|wire\|text\|ref ...` | 逐个遍历图形 |
| `$L report` / `$L query` | 报告与查询 |
| `$L scale` / `$L SIZE` / `$L SNAP` | 变换 |

### A5. GUI（选学 · Phase C）

| 命令 | 用途 |
|------|------|
| `find objects -class cwbWorkBench` | 找到桌面主对象 |
| `$cwb cget -_layout` | 当前打开的 layout 句柄 |
| `$cwb zoomAllClbk` / `setLayerVisibility` … | 视图控制（大人演示即可） |

---

# 附录 B — 每周 API 打卡表（可打印 · Calibre 段）

| 周 | 我练过的命令（自己打勾） |
|----|--------------------------|
| 21 | □ `layout create` □ 打印句柄 `$L` □ `./scripts/run_calibre_tcl.sh` |
| 22 | □ `units microns` □ `create cell` □ `create layer` □ `create polygon` □ `create text` □ `create wire` □ `gdsout` □（选）`oasisout` □（选）`eval`+坐标 list |
| 23 | □ `layout create $gds` □ `topcell` □ `cells` □ `layers` □ `exists cell` □ `bbox` □ `layout peek -cells/-layers/-topcell` |
| 24 | □ `create ref` □ 组合报告 □（选）TclOO 封装 □（选）`cwbWorkBench` |
| 25 | □ `iterator poly/wire/text` |
| 26 | □ `flatten cell` □ `expand ref` |
| 27 | □ `layout filemerge` □ `import layout` |
| 28 | □ `AND`/`OR`/`NOT` □ `SIZE` |
| 29–30 | □ `layout all/copy/delete` □ `units`/`precision`/`file` |
| 31–40 | □ 按当周必会表自勾；第 40 周 □ COVERAGE 审计 |

---

# 每周固定节奏（建议）

```
周一：学一个新命令族（标题 + 最小例子）
周二：照着改数字 / 参数 / 坐标
周三：自己组合 2～3 个命令
周四：修 bug / 查 lesson 或手册 HTML TOC
周五：完成本周小作品
周末：可选复习 15 分钟，或休息
```

---

# 家长 / 老师辅助清单

| 事项 | 说明 |
|------|------|
| 环境 | 第 1–20 周：`tclsh` 即可。第 21 周起：`source setup_calibredrv.sh`；GUI 用 VNC/X11 |
| 运行 | Tcl：`tclsh` / `make weekN`。Calibre：优先 `./scripts/run_calibre_tcl.sh examples/xxx.tcl` |
| 手册 | 卡壳时打开 `calbr_drv_ref_toc.html`，搜索命令名；PDF 亦可 |
| 第 2 周 | 多花时间陪孩子做 `" "` vs `{ }` 对比实验——这是语法地基 |
| 第 15–16 周 | TclOO；用 OOP 地图讲故事即可 |
| 第 21–24 周 | 强调「先查手册再猜」；层号写法以本机实测为准；不代替孩子改完全部代码 |
| 安全 | 只在本项目目录写文件；不要改 license / EDA 安装目录 |
| 里程碑 | M10 / M20 可先庆祝再开下一阶段；不必赶进度 |

---

# 讲义生成说明（content-generation）

新周讲义按本 PLAN 的「第 N 周」节生成到 `lessons/N/`（双语 `lesson_en.md` / `lesson_zh.md` + ≥10 个 `.tcl`）。  
用 Cursor 技能 **content-generation**，并以本文件为权威周次来源。  
覆盖勾选同步维护 [docs/COVERAGE.md](docs/COVERAGE.md)（若表内仍写旧周次，以本 PLAN 对照表为准逐步改）。

---

# 鼓励语

> 芯片图纸很复杂，但你现在学的是：**先把 Tcl 话说清楚 → 再查手册 → 选对 API → 给 `$L` 下清楚的命令**。  
> M10 读懂语法、M20 写出纯 Tcl 作品、M30 会画会查版图、M40 把工具箱贴上标签——每一步都了不起。  
> 报错不是失败，是电脑在跟你玩「找不同」。继续加油！
