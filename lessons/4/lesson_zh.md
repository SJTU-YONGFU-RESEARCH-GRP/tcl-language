# 第 4 周 — 如果……就……：条件与循环

> 本课对应总计划：[10 周 Tcl 学习计划](../../PLAN.md)。  
> 本周目标：让程序会 **判断**（`if`）和 **重复做事**（`foreach`、`for`、`while`）。

---

## 学习目标

学完这一周，你应该能够：

1. 写 `if {条件} { ... } else { ... }` 在不同情况做不同事。
2. 用 `foreach item $list { ... }` 遍历列表里的每一项。
3. 用 `for {set i 1} {$i <= 10} {incr i} { ... }` 带循环变量数数。
4. 用 `while {条件} { ... }` 重复执行直到条件不成立。
5. 把 `if` 和循环组合（例如：列表里每个分数判断 Pass/Fail）。
6. 完成猜数字小脚本：把猜测与秘密数字比较。

当你能独立写含至少一个 `if` 和一个循环的小脚本时，第 4 周就过关了。

---

## 大想法（用生活比喻）

以前的脚本大多 **从上到下** 一行行执行。本周学会 **岔路** 和 **绕圈**。

| Tcl 概念 | 生活比喻 | 本周你会做什么 |
|----------|----------|----------------|
| `if {下雨} { 带伞 }` | 如果下雨，就带伞 | 按分数 Pass/Fail |
| `foreach fruit $list` | 把串上每颗糖都尝一遍 | 打印每种水果 |
| `for {set i 1} ...` | 按步数数：1、2、3 … 10 | 打印数字、乘法表 |
| `while {$n > 0}` | 没做完就继续做 | 倒数 5…1，再「发射！」 |

你仍会用到第 1–3 周的变量、列表、`puts`、`expr`。

---

## 开始前需要准备什么

### 要先会的内容

- 第 2 周：`set`、`$`、`expr`。
- 第 3 周：`list`、`lindex`、`llength`、`lappend`。

### 工具

终端、`tclsh`、文本编辑器。

### 快速检查

```bash
make week4-01
```

---

## 概念 1 — `if` 做判断（Day 1）

### if / else 长什么样

```tcl
set score 75

if {$score >= 60} {
    puts "Pass"
} else {
    puts "Fail"
}
```

### 要记住的规则

1. **条件** 放在 `{ 花括号 }` 里：`{ $score >= 60 }`。
2. **要做的事** 也在 `{ ... }` 块里。
3. 比较符：`>=`、`<=`、`==`、`!=`、`<`、`>`。
4. 多个分支可用 `elseif`（见 `02_if_else_messages.tcl`）。

### 预期输出（分数 75）

```text
Pass
```

### 为什么条件要加花括号？

让 Tcl **整段** 当作表达式稍后再判断。初学者请固定用 `{ $score >= 60 }` 这种写法。

---

## 概念 2 — `foreach` 遍历列表（Day 2）

```tcl
set fruits [list apple banana cherry]

foreach fruit $fruits {
    puts "I like $fruit."
}
```

输出：

```text
I like apple.
I like banana.
I like cherry.
```

每走一圈，`fruit` 里是 **下一个** 元素。不必再手写 `lindex 0`、`lindex 1` …

### foreach + 计数（可选）

```tcl
set n 0
foreach color $colors {
    incr n
    puts "$n. $color"
}
```

见 `05_foreach_with_index.tcl`。

---

## 概念 3 — `for` 用循环变量数数（Day 3）

```tcl
for {set i 1} {$i <= 10} {incr i} {
    puts $i
}
```

`for` 里三部分：

| 部分 | 例子 | 作用 |
|------|------|------|
| 开始 | `set i 1` | 创建循环变量 |
| 条件 | `$i <= 10` | 为真就继续 |
| 步进 | `incr i` | 每次 +1 |

输出：1 到 10，每行一个数。

见 `07_for_times_table.tcl`：在循环里用 `expr` 算乘积。

---

## 概念 4 — `while` 重复直到结束（Day 4）

```tcl
set n 5
while {$n > 0} {
    puts $n
    incr n -1
}
puts "Launch!"
```

输出：

```text
5
4
3
2
1
Launch!
```

每次循环 **开始前** 检查 `$n > 0`。当 `n` 变成 0，循环停止。

**重要：** 循环里必须改变 `n`（这里用 `incr n -1`），否则会 **死循环**。

---

## 概念 5 — 猜数字小作品（Day 5）

作品组合 `foreach`、`if`、`elseif`、`else` 和 `break`。

本仓库用 **猜测列表** 代替键盘输入，方便 `make week4-10` 批处理运行：

```tcl
set secret 7
foreach guess $guesses {
    if {$guess == $secret} {
        puts "猜对了！"
        break
    } elseif {$guess < $secret} {
        puts "太小"
    } else {
        puts "太大"
    }
}
```

猜对时 `break` 提前跳出循环。

以后（第 5 周及以后）可在家长帮助下加 `gets stdin` 做交互版。

---

## 每日练习（每次大约 30～45 分钟）

| 天 | 目标 | 建议文件 |
|----|------|----------|
| Day 1 | `if` Pass/Fail | `01_if_pass_fail.tcl`、`02_if_else_messages.tcl`、`03_if_check_three_scores.tcl` |
| Day 2 | `foreach` | `04_foreach_fruits.tcl`、`05_foreach_with_index.tcl` |
| Day 3 | `for` 1..10 | `06_for_one_to_ten.tcl`、`07_for_times_table.tcl` |
| Day 4 | `while` 倒数 | `08_while_countdown.tcl`、`09_while_add_until.tcl` |
| Day 5 | **本周作品** | `10_guess_number_game.tcl` |

加分：`11_if_foreach_combined.tcl`、`12_run_checklist.tcl`。

### 本周检查清单

- [ ] 我会写带花括号条件的 `if / else`。
- [ ] 我会用 `foreach` 遍历列表。
- [ ] 我会用 `for` 数数。
- [ ] 我会用 `while` 直到条件不成立。
- [ ] 我完成了猜数字游戏。

---

## 常见错误（和解决办法）

| 现象 | 常见原因 | 怎么办 |
|------|----------|--------|
| `syntax error in expression` | 条件没包在花括号里 | 写 `if {$x >= 60} {` |
| `while` 死循环 | 变量一直没变 | 加 `incr n -1` 等 |
| `foreach` 什么都不打印 | 变量名错或列表空 | 检查 `set fruits [list ...]` |
| `if $score >= 60` 报错 | 缺花括号 | 条件写成 `{ $score >= 60 }` |
| 循环多一次或少一次 | 边界 off-by-one | 检查 `<=` 还是 `<` |

---

## 示例脚本（完整列表）

```bash
make week4-01
make week4
make list WEEK=4
```

| 编号 | 文件 | 练习重点 |
|------|------|----------|
| 01 | `01_if_pass_fail.tcl` | 基本 Pass/Fail |
| 02 | `02_if_else_messages.tcl` | elseif 分级 |
| 03 | `03_if_check_three_scores.tcl` | 三门课 |
| 04 | `04_foreach_fruits.tcl` | foreach 基础 |
| 05 | `05_foreach_with_index.tcl` | foreach + 计数 |
| 06 | `06_for_one_to_ten.tcl` | for 1..10 |
| 07 | `07_for_times_table.tcl` | for + expr |
| 08 | `08_while_countdown.tcl` | 倒数 + 发射 |
| 09 | `09_while_add_until.tcl` | while 直到达标 |
| 10 | `10_guess_number_game.tcl` | **本周作品** |
| 11 | `11_if_foreach_combined.tcl` | foreach + if |
| 12 | `12_run_checklist.tcl` | 检查清单 |

---

## 挑战题（可选）

扩展 `10_guess_number_game.tcl`：

1. 秘密数字在 1～20  
2. 猜测列表至少 6 个数  
3. 猜对时打印用了几次  
4. 全错则打印 Game over  
5. 用 `while` + 下标从列表里逐个取猜测  

---

## 下一周预告

**第 5 周** 学 **过程（`proc`）** 和 **文件读写**：

- `proc greet {name} { puts "Hi $name" }` — 可重复使用的小帮手。
- `open`、`gets`、`puts`、`close` — 读写文本文件。

你写的 `if` 和循环会放进 **proc** 里复用。

---

## 给家长 / 老师

- 条件和循环头几乎都要 `{ 花括号 }` — 尽早练熟。
- `10_guess_number_game.tcl` 故意做成批处理版；交互式 `gets` 作选做。
- 成功标准：孩子改通过分数线或猜测列表，运行 `make week4-10`，能解释一处 `if` 和一处循环。
