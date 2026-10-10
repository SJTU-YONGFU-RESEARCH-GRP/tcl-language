# 第 2 周 — 语法周：变量、引用与替换

> 本课对应总计划：[PLAN.md](../../PLAN.md)（**M10** 第 1–10 周）。  
> 本周目标：会用 `set` 存东西；更重要的是搞清楚 Tcl **怎么读你的句子**：`"..."`、`{...}`、`$`、`[cmd]`、`\`。

---

## 学习目标

学完这一周，你应该能够：

1. 用 `set` 把值放进带名字的标签盒（变量）里。
2. 用 `$变量名` 取出值，并用 `puts` 打印。
3. 用自己的话说明双引号与花括号的差别。
4. 在双引号里用 `[expr ...]` 做命令替换。
5. 用 `\` 打印字面 `$` 或换行。
6. 用 `expr {$a + $b}`、`expr {$age + 1}` 做简单加减。
7. 完成「成绩单」小作品：三门课分数 + 总分。

当你能解释引号规则，并自己写一段用变量组成的自我介绍时，第 2 周就过关了。

---

## 大想法（用生活比喻）

第 1 周你打印的是 **写死的文字**。本周学 **变量**，以及 Tcl 的 **替换规则**——后面每一周都靠它。

| Tcl 概念 | 生活比喻 | 本周你会做什么 |
|----------|----------|----------------|
| `set name "Amy"` | 在标签为 `name` 的盒子里放 `"Amy"` | 存名字、分数、年龄 |
| `$name` | 打开盒子 | 在 `puts` 或 `expr` 里用值 |
| `"..."` 双引号 | 半透明包装——`$` 和 `[ ]` 还会生效 | 拼句子 |
| `{...}` 花括号 | 密封袋——几乎原样保留 | 原样打印 `$name`、`[ ]` |
| `[cmd ...]` | 先算小纸条再塞回句子 | 嵌套 `expr` |
| `\` 反斜杠 | 下一个字有特殊任务 | 字面 `$`、换行 |
| `expr {$a + $b}` | 计算器 | 加总分、年龄 +1 |

### 五种替换（建议抄进小本子）

```tcl
set name "Amy"
set age 10

puts "hello $name"           ;# 双引号 → hello Amy
puts {hello $name}           ;# 花括号 → hello $name
puts "sum=[expr {$age + 1}]" ;# 方括号先跑 expr
puts "dollar=\$name"         ;# 反斜杠 → 字面 $name
puts "line1\nline2"          ;# 反斜杠 → 换行
```

实验室：`make week2-08`。

---

## 开始前需要准备什么

### 第 1 周要先会的内容

- 会用 `tclsh` 运行 `.tcl` 文件。
- 会用 `puts` 和 `#` 注释。
- 能看懂输出、修简单的引号错误。

### 工具

与第 1 周相同：终端、`tclsh`、文本编辑器。

### 确认 Tcl 仍可用

```bash
make check
```

或：

```bash
tclsh lessons/2/01_set_one_variable.tcl
```

预期输出：

```text
Amy
```

### 用 Make 运行第 2 周例题

在项目根目录：

```bash
make week2-01
make week2
make list WEEK=2
```

---

## 概念 1 — `set` 把值存进带标签的盒子

### 一条 set 命令长什么样

```tcl
set name "Amy"
```

| 部分 | 例子 | 含义 |
|------|------|------|
| 命令 | `set` | 存值 |
| 变量名 | `name` | 盒子上的标签（这里 **不要** 写 `$`） |
| 值 | `"Amy"` | 放进盒子的内容 |

### 要记住的规则

1. **创建**变量：`set 变量名 值` —— `set` 左边变量名 **不加** `$`。
2. 变量名通常是一个词：`name`、`school`、`mathScore`，中间不要有空格。
3. 文字值加引号：`set name "Amy"`。
4. 数字可以不加引号：`set age 10`（也可以写 `set age "10"`，初学两种都行）。

### 第一个完整例子

```tcl
set name "Amy"
puts $name
```

预期输出：

```text
Amy
```

注意：`puts $name` 里的 `$` 表示 **读取** 盒子，不是贴标签。

### 分步练习：三个变量（Day 1）

1. 打开 `02_three_variables.tcl` 或自己新建文件。
2. 写三行 `set`：名字、学校、年级。
3. 写三行 `puts`，分别打印三个变量。
4. 保存并运行：`make week2-02`
5. 把三个值改成你自己的信息，再运行，确认输出变了。

---

## 概念 2 — `$` 用来读取变量

### 什么时候写 `$`

| 情况 | 写法 | 例子 |
|------|------|------|
| 存值 | `set name "Amy"` | 变量名 **无** `$` |
| 单独读取 | `puts $name` | 变量名前 **有** `$` |
| 在字符串里读取 | `puts "你好，$name！"` | 双引号里的 `$` |

### 错与对

```tcl
set name "Amy"
puts name      ;# 错（初学阶段）—— 会打印单词 name，不是 Amy
puts $name     ;# 对 —— 打印 Amy
```

### 用两个变量拼成一句话（Day 2）

```tcl
set name "Amy"
set city "上海"
puts "你好，我叫 $name，住在 $city。"
```

预期输出：

```text
你好，我叫 Amy，住在 上海。
```

Tcl 会在打印 **之前** 把 `$name`、`$city` 换成盒子里的值。你只写一次句子模板，事实由变量提供。

---

## 概念 3 — 再次 `set` 可以改变变量（Day 3）

变量不是一次定终身。同一个标签可以装新值：

```tcl
set favoriteColor "blue"
puts "改之前：$favoriteColor"

set favoriteColor "green"
puts "改之后：$favoriteColor"
```

预期输出：

```text
改之前：blue
改之后：green
```

标签 `favoriteColor` 没变，变的是 **里面的内容**。之后任何 `$favoriteColor` 都用 **最新** 的值。

### 为什么重要

以后你会用来：

- 更新测验分数。
- 模拟「明年几岁」。
- 修错别字而不必换变量名。

---

## 概念 4 — 用 `expr` 做简单运算（Day 4）

### 为什么不能直接 `puts $a + $b`？

`puts` 负责 **显示**。要把数字 **相加**，要用 `expr`：

```tcl
set a 15
set b 4
set sum [expr {$a + $b}]
puts "a + b = $sum"
```

预期输出：

```text
a + b = 19
```

### 这个模式各部分

| 部分 | 含义 |
|------|------|
| `[expr {...}]` | 做运算，把结果返回 |
| expr 里的 `{...}` | 保护算式（好习惯） |
| expr 里的 `$a`、`$b` | 从变量里取数字 |

### 年龄 + 1（对应 PLAN）

```tcl
set age 10
set nextAge [expr {$age + 1}]
puts "明年我就 $nextAge 岁了。"
```

输出：

```text
明年我就 11 岁了。
```

### 减法也一样

```tcl
set apples 7
set eaten 2
set left [expr {$apples - $eaten}]
puts "还剩 $left 个苹果"
```

完整脚本见 `09_simple_math.tcl`。

---

## 概念 5 — 双引号与花括号的区别

### 双引号 `"..."` —— 会替换 `$`

```tcl
set name "Amy"
puts "你好，$name！"
```

打印：`你好，Amy！`

### 花括号 `{...}` —— 不会替换 `$`

```tcl
set name "Amy"
puts {你好，$name！}
```

打印：`你好，$name！`（原样显示 `$name`）

当你要在输出里 **展示** Tcl 语法，或避免特殊字符被解释时，用花括号。第 2 周：知道两者区别；日常消息多用双引号。

---

## 每日练习（每次大约 30～45 分钟）

| 天 | 目标 | 具体要做什么 | 建议文件 |
|----|------|--------------|----------|
| Day 1 | 第一次 `set` | 存名字、学校、年级；用 `$` 打印 | `01_set_one_variable.tcl`、`02_three_variables.tcl` |
| Day 2 | 句子里用 `$` | 在一个 `puts "..."` 里用两个以上变量 | `03_print_with_dollar.tcl`、`06_two_strings_join.tcl` |
| Day 3 | 改变量 | 对同一名字 `set` 两次；打印前后对比 | `04_change_value.tcl` |
| Day 4 | `expr` 运算 | 年龄 +1；两数加减 | `05_expr_add_one.tcl`、`09_simple_math.tcl` |
| Day 5 | **本周作品** | 成绩单：三门课 + 总分 | `10_report_card.tcl` |

加分练习：`07_numbers_and_strings.tcl`、`08_braces_literal.tcl`、`11_intro_with_variables.tcl`、`12_run_checklist.tcl`。

### 本周检查清单

- [ ] 我会用 `set` 存文字和数字。
- [ ] 我知道什么时候写 `name`、什么时候写 `$name`。
- [ ] 我会在双引号字符串里打印变量。
- [ ] 我会改变变量并看到新输出。
- [ ] 我会用 `expr` 做加法和减法。
- [ ] 我完成了带正确总分的成绩单。

---

## 常见错误（和解决办法）

| 现象 | 常见原因 | 怎么办 |
|------|----------|--------|
| `can't read "name": no such variable` | 还没 `set name` 就用了 `$name` | 在 `puts` 上面先写 `set name "..."` |
| 输出是 `name` 而不是 Amy | 写了 `puts name` 忘了 `$` | 改成 `puts $name` |
| `syntax error in expression` | `expr` 写法不对 | 用 `expr {$a + $b}`，`+`、`-` 两边留空格 |
| 把数字当文字加错了 | 在错误的地方用引号包数字 | 数字用 `set score 88`；运算用 `expr` |
| `set $name "Amy"` | 在 `set` 左边误加了 `$` | 只写 `set name "Amy"` |
| 总分像文字 `88 + 92` | 没有真正做运算 | 用 `expr {$math + $english + $science}` |

---

## 本文件夹里的示例脚本（完整列表）

最简单的方式（项目根目录）：

```bash
make week2-01
make week2
make list WEEK=2
make run WEEK=2 EX=10
```

或用 `tclsh`：

```bash
tclsh lessons/2/01_set_one_variable.tcl
tclsh lessons/2/02_three_variables.tcl
tclsh lessons/2/03_print_with_dollar.tcl
tclsh lessons/2/04_change_value.tcl
tclsh lessons/2/05_expr_add_one.tcl
tclsh lessons/2/06_two_strings_join.tcl
tclsh lessons/2/07_numbers_and_strings.tcl
tclsh lessons/2/08_braces_literal.tcl
tclsh lessons/2/09_simple_math.tcl
tclsh lessons/2/10_report_card.tcl
tclsh lessons/2/11_intro_with_variables.tcl
tclsh lessons/2/12_run_checklist.tcl
```

| 编号 | 文件 | 练习重点 | 怎样算成功 |
|------|------|----------|------------|
| 01 | `01_set_one_variable.tcl` | 第一个 `set` 和 `$` | 打印出名字 |
| 02 | `02_three_variables.tcl` | 三个变量 | 姓名、学校、年级三行 |
| 03 | `03_print_with_dollar.tcl` | 双引号里的 `$` | 完整句子 |
| 04 | `04_change_value.tcl` | 重新 `set` | 前后输出不同 |
| 05 | `05_expr_add_one.tcl` | `expr {$age + 1}` | 明年年龄正确 |
| 06 | `06_two_strings_join.tcl` | 拼一句话 | 两个变量合成一句 |
| 07 | `07_numbers_and_strings.tcl` | 文字 vs 数字 | 分数加 bonus 用 expr |
| 08 | `08_braces_literal.tcl` | `{...}` 不替换 | 原样显示 `$name` |
| 09 | `09_simple_math.tcl` | 加减法 | 和与差都正确 |
| 10 | `10_report_card.tcl` | **本周作品** | 三门课 + 总分 |
| 11 | `11_intro_with_variables.tcl` | 加分：变量版介绍卡 | 各字段来自变量 |
| 12 | `12_run_checklist.tcl` | 第 2 周检查清单 | 方框用花括号正确显示 |

---

## 挑战题（可选，完整要求）

改写 `10_report_card.tcl`（或复制为 `my_report_card.tcl`），让打印结果 **全部包含**：

1. 你的真名和学校  
2. 三门你自选科目的名字（不限于语数英）  
3. 每门课一个分数变量  
4. 总分用 **一个** `expr` 计算（不要手算写死）  
5. 一行平均分：`expr {$total / 3}`（整数除法可以）  
6. 至少四条 `#` 注释：页眉、分数、总分、页脚  
7. 用 `=` 字符做上下边框  

---

## 下一周预告

**第 3 周** 学 **列表**：像 `{apple banana cherry}` 这样一串东西。

- `list a b c` 做列表。
- `lindex $L 0` 取第 1 个（从 0 开始数）。
- `llength $L` 数有几个。

变量是一个盒子装 **一个** 值。列表是一个盒子装 **很多** 值——像一根棍子上串好多颗糖。

---

## 给家长 / 老师

- 仍只需 `tclsh`，不需要 Calibre。
- 孩子最容易混：存的时候不写 `$`，读的时候要写 `$`。多练 `set name` 与 `$name` 直到熟练。
- 挑战题里的平均分用整数除法即可；需要小数以后再教。
- 成功标准：孩子能改 `10_report_card.tcl` 里的 `set`，保存，运行 `make week2-10`，并能解释一处 `$` 和一处 `expr`。
