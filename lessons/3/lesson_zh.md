# 第 3 周 — 一串糖果：列表（list）

> 本课对应总计划：[10 周 Tcl 学习计划](../../PLAN.md)。  
> 本周目标：会创建列表、用 `lindex` 取元素、用 `llength` 数个数、用 `lappend` 追加元素。

---

## 学习目标

学完这一周，你应该能够：

1. 用 `list 项1 项2 项3` 做列表，并存进变量。
2. 用 `lindex $L 0` 取 **第 1 个** 元素（记住：从 **0** 开始数）。
3. 用 `lindex $L end` 或配合 `llength` 的算式取 **最后一个** 元素。
4. 用 `llength $L` 数列表里有几个元素。
5. 用 `lappend` 在列表 **末尾** 追加新元素。
6. 完成「今日课表」小作品：从列表里打印指定第几节课。

当你能自己建列表、数数、取任意一项、追加新项（而不是逐行抄例题）时，第 3 周就过关了。

---

## 大想法（用生活比喻）

第 2 周是 **一个盒子装一个值**。第 3 周是 **一个盒子装一串值**——像一根绳子上串好多颗糖。

| Tcl 概念 | 生活比喻 | 本周你会做什么 |
|----------|----------|----------------|
| `list a b c` | 三颗糖穿在一根绳上 | 做水果清单、课表 |
| `set L [list ...]` | 整串糖放进一个 labeled 盒子 | 把列表存进变量 |
| `lindex $L 0` | 拿 **第 1 颗**（下标 0） | 取第一个颜色、第一节课 |
| `lindex $L end` | 拿 **最后一颗** | 取最后一个水果 |
| `llength $L` | 数有几颗糖 | 「共有 N 种水果」 |
| `lappend L 新项` | 在绳尾再系一颗 | 购物清单越来越长 |

你仍会用到第 1、2 周的 `set`、`$`、`puts`、`expr`。列表是本周的新工具。

---

## 开始前需要准备什么

### 要先会的内容

- 第 1 周：`puts`、脚本、`#` 注释。
- 第 2 周：`set`、`$变量`、`expr {$a - 1}`（算最后一个下标时会用到）。

### 工具

终端、`tclsh`、文本编辑器——与前几周相同。

### 快速检查

```bash
make check
make week3-01
```

预期输出包含：

```text
My fruit list: apple banana cherry
```

---

## 概念 1 — `list` 做出一串元素

### 一条 list 命令长什么样

```tcl
set fruits [list apple banana cherry]
puts $fruits
```

| 部分 | 含义 |
|------|------|
| `[list apple banana cherry]` | 建列表；`[...]` 执行命令并把结果交给 `set` |
| `$fruits` | 整个列表作为一个值 |
| 项与项之间的空格 | 简单列表里，每个词是一个元素 |

### 预期输出

```text
apple banana cherry
```

Tcl 打印列表时，项与项之间用空格分开，这是正常的。

### 分步练习：第一份水果清单（Day 1）

1. 新建 `my_fruits.tcl` 或打开 `01_list_fruits.tcl`。
2. 写 `set fruits [list apple banana cherry]`。
3. 用 `puts "My fruit list: $fruits"` 打印。
4. 保存并运行：`make week3-01`。
5. 改成你喜欢的水果，再运行一次。

---

## 概念 2 — `lindex` 取出其中一个（Day 2）

### 下标从 0 开始

| 人口头数 | Tcl 下标 | `{apple banana cherry}` 里是谁 |
|----------|----------|--------------------------------|
| 第 1 个 | `0` | apple |
| 第 2 个 | `1` | banana |
| 第 3 个 | `2` | cherry |

很多初学者会在这里栽跟头：**第 1 项的下标是 0，不是 1。**

### 取第 1、第 2 个

```tcl
set colors [list red green blue]
set first [lindex $colors 0]
set second [lindex $colors 1]
puts "第 1 个：$first"
puts "第 2 个：$second"
```

输出：

```text
第 1 个：red
第 2 个：green
```

### 取最后一个

简单写法：

```tcl
set last [lindex $fruits end]
```

算术写法（帮助理解）：

```tcl
set n [llength $fruits]
set lastIndex [expr {$n - 1}]
set last [lindex $fruits $lastIndex]
```

两种方法结果一样。见 `04_lindex_last.tcl`。

---

## 概念 3 — `llength` 数有几个（Day 3）

```tcl
set fruits [list apple banana cherry orange grape]
set n [llength $fruits]
puts "我的清单上一共有 $n 种水果。"
```

输出：

```text
我的清单上一共有 5 种水果。
```

只要问「有几个？」就用 `llength`——第 4 周学循环前，或要算最后一个下标时都会用到。

---

## 概念 4 — `lappend` 在末尾追加（Day 4）

```tcl
set fruits [list apple banana cherry]
lappend fruits orange
lappend fruits grape
puts $fruits
```

输出：

```text
apple banana cherry orange grape
```

规则：

1. 第一个参数是 **变量名**（不要 `$`）：`lappend fruits orange`。
2. 每次 `lappend` 在 **末尾** 加 **一项**。
3. 变量 `fruits` 会被直接更新——一般不必再 `set` 一遍。

---

## 概念 5 — 用手工 lindex 打印每一项（循环之前）

第 4 周会学 `foreach`。现在可以先用多个 `lindex`：

```tcl
set pets [list cat dog rabbit hamster]
puts "1. [lindex $pets 0]"
puts "2. [lindex $pets 1]"
puts "3. [lindex $pets 2]"
puts "4. [lindex $pets 3]"
```

见 `07_print_each_manual.tcl`。写很多遍？是的——所以下周要学循环。

---

## 每日练习（每次大约 30～45 分钟）

| 天 | 目标 | 具体要做什么 | 建议文件 |
|----|------|--------------|----------|
| Day 1 | 建列表 | 做水果清单；存变量并打印 | `01_list_fruits.tcl`、`02_store_and_print_list.tcl` |
| Day 2 | `lindex` | 打印第 1、第 2、最后一项 | `03_lindex_first.tcl`、`04_lindex_last.tcl` |
| Day 3 | `llength` | 打印「共有 N 种水果」 | `05_llength_count.tcl`、`08_fruit_count_message.tcl` |
| Day 4 | `lappend` | 往清单里加两种新水果 | `06_lappend_add.tcl`、`09_growing_shopping_list.tcl` |
| Day 5 | **本周作品** | 今日课表 + 打印第几节课 | `10_today_schedule.tcl` |

加分：`07_print_each_manual.tcl`、`11_list_of_lists.tcl`、`12_run_checklist.tcl`。

### 本周检查清单

- [ ] 我会用 `list` 创建列表。
- [ ] 我记得下标 **0** 是第 1 项。
- [ ] 我会用 `lindex` 取任意一项。
- [ ] 我会用 `lindex ... end` 取最后一项。
- [ ] 我会用 `llength` 数个数。
- [ ] 我会用 `lappend` 追加元素。
- [ ] 我完成了今日课表作品。

---

## 常见错误（和解决办法）

| 现象 | 常见原因 | 怎么办 |
|------|----------|--------|
| 想要第 1 个却用了 `lindex $L 1` | 人话「第 1」≠ 下标 1 | 第 1 项的下标是 **0** |
| 写了 `lindex fruits 0` | 读变量时忘了 `$` | 改成 `lindex $fruits 0` |
| 写了 `lappend $fruits x` | `lappend` 变量名误加 `$` | 写 `lappend fruits x` |
| 最后一项不对或为空 | 下标算错 | 试 `lindex $L end` |
| 嵌套列表搞混 | 列表里还有列表（加分题） | 先练扁平列表，再看 `11_list_of_lists.tcl` |

---

## 本文件夹里的示例脚本（完整列表）

在项目根目录：

```bash
make week3-01
make week3
make list WEEK=3
make run WEEK=3 EX=10
```

或：

```bash
tclsh lessons/3/01_list_fruits.tcl
tclsh lessons/3/02_store_and_print_list.tcl
tclsh lessons/3/03_lindex_first.tcl
tclsh lessons/3/04_lindex_last.tcl
tclsh lessons/3/05_llength_count.tcl
tclsh lessons/3/06_lappend_add.tcl
tclsh lessons/3/07_print_each_manual.tcl
tclsh lessons/3/08_fruit_count_message.tcl
tclsh lessons/3/09_growing_shopping_list.tcl
tclsh lessons/3/10_today_schedule.tcl
tclsh lessons/3/11_list_of_lists.tcl
tclsh lessons/3/12_run_checklist.tcl
```

| 编号 | 文件 | 练习重点 | 怎样算成功 |
|------|------|----------|------------|
| 01 | `01_list_fruits.tcl` | 第一个 `list` | 水果名打印出来 |
| 02 | `02_store_and_print_list.tcl` | 存列表 + 早期 `lindex` | 列表和前几项 |
| 03 | `03_lindex_first.tcl` | 下标 0 和 1 | 第 1、第 2 个颜色 |
| 04 | `04_lindex_last.tcl` | 最后一项两种取法 | 最后一个水果正确 |
| 05 | `05_llength_count.tcl` | 数个数 | 「N 种水果」 |
| 06 | `06_lappend_add.tcl` | 追加两项 | 列表变长 |
| 07 | `07_print_each_manual.tcl` | 手工打印全部 | 四行宠物 |
| 08 | `08_fruit_count_message.tcl` | 计数 + 首尾 | 库存卡片 |
| 09 | `09_growing_shopping_list.tcl` | 列表变长 | 从 2 项到 5 项 |
| 10 | `10_today_schedule.tcl` | **本周作品** | 完整课表 + 高亮一节 |
| 11 | `11_list_of_lists.tcl` | 加分：嵌套列表 | 表格行 |
| 12 | `12_run_checklist.tcl` | 第 3 周检查清单 | 方框正确显示 |

---

## 挑战题（可选，完整要求）

改写 `10_today_schedule.tcl`，让输出 **全部包含**：

1. 真实的星期几  
2. 至少 **六** 门课科目  
3. 变量 `period`（1～6）表示要高亮第几节  
4. 用 `lindex` 和 `expr {$period - 1}` 取出对应科目  
5. 一行 `Total: N periods`，`N` 来自 `llength`  
6. 列表建好后 **用一次** `lappend` 加一门 bonus 课  
7. 至少四条 `#` 注释和 `=` 边框  

---

## 下一周预告

**第 4 周** 学 **条件与循环**：

- `if {分数 >= 60} { puts "Pass" }` —— 会判断。
- `foreach item $list { puts $item }` —— 不用写五遍 `lindex` 也能遍历列表。
- `for`、`while` —— 重复做事。

列表负责 **装数据**；循环负责 **自动走遍** 这些数据。

---

## 给家长 / 老师

- 仍只需 `tclsh`，不需要 Calibre。
- 重点 drill：**下标 0 = 第 1 个**；可以画 0..n-1 数轴。
- `lappend` 第一个参数不加 `$`，和 `set` 一样。
- 成功标准：孩子改 `10_today_schedule.tcl` 里的科目、设 `period` 为 4，运行 `make week3-10`，并能解释为什么 `lindex` 要用 `expr {$period - 1}`。
