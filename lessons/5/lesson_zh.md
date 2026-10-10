# 第 5 周 — 小帮手：过程（proc）与文件

> 本课对应总计划：[10 周 Tcl 学习计划](../../PLAN.md)。  
> 本周目标：把重复动作做成 **过程（proc）**；能读写简单文本文件。

---

## 学习目标

学完这一周，你应该能够：

1. 定义过程：`proc greet {name} { puts "Hi $name!" }` 并调用它。
2. 用 `return` 从 proc 返回结果（例如 `add`）。
3. 打开文件写入、用 `puts $通道 ...` 写行、`close` 关闭。
4. 打开文件读取、在 `while` 里用 `gets` 逐行读。
5. 使用 `file mkdir` 和 `file join` 处理文件夹与路径。
6. 完成 **工具箱** 小作品：至少 3 个 proc + 文件日志。

当你能在一份脚本里组合变量、列表、`if`、循环、至少一个 `proc` 和文件读写时，第 5 周就过关了。

---

## 大想法（用生活比喻）

| Tcl 概念 | 生活比喻 | 本周你会做什么 |
|----------|----------|----------------|
| `proc greet {...}` | 训练小狗听口令打招呼 | 不用重复抄写代码 |
| `return` | 小狗把球叼回来 | `add` 返回数字 |
| `open` / `close` | 打开本子、写、合上 | 日记写到 `tmp/` |
| `gets` | 从本子上读一行 | 逐行打印文件 |
| `file join` | 安全地拼路径 | 拼出 `tmp/notes.txt` |

**通向 OOP（更远一点）：** `proc` 是「没有主人」的动作。对象与方法在 **第 15 周**；下周先学 `string` 全家桶。

---

## 开始前需要准备什么

### 要先会的内容

- 第 1–4 周：`puts`、变量、列表、`if`、循环。

### 工具

- `tclsh`、编辑器、终端。
- 项目根目录下可写的 `tmp/` 文件夹（例题会用 `file mkdir tmp` 创建）。

### 从项目根目录运行

例题里路径是相对于 **项目根目录**（`make` 的工作目录）：

```bash
make week5-05
make week5-07
```

---

## 概念 1 — `proc` 定义可重复使用的小帮手（Day 1）

```tcl
proc greet {name} {
    puts "Hi $name!"
}

greet "Amy"
greet "Bob"
```

| 部分 | 含义 |
|------|------|
| `proc` | 定义过程 |
| `greet` | 小帮手名字 |
| `{name}` | 参数列表 |
| `{ puts ... }` | 过程体——要执行的命令 |

像命令一样调用：`greet "Amy"`。

---

## 概念 2 — `return` 返回结果（Day 2）

```tcl
proc add {a b} {
    return [expr {$a + $b}]
}

set sum [add 15 4]
puts $sum
```

输出：`19`

当 proc **算出** 结果给后面用时，用 `return`。

---

## 概念 3 — 写文本文件（Day 3）

```tcl
file mkdir tmp

set path tmp/week5_diary.txt
set fh [open $path w]

puts $fh "第一行"
puts $fh "第二行"

close $fh
```

| 步骤 | 命令 | 说明 |
|------|------|------|
| 确保目录 | `file mkdir tmp` | 已有目录也安全 |
| 打开写 | `open $path w` | `w` = 写入（新建或覆盖） |
| 写入 | `puts $fh "文字"` | 注意是 `$fh`，不是屏幕 |
| 关闭 | `close $fh` | 用完要关 |

---

## 概念 4 — 读文本文件（Day 4）

```tcl
set fh [open $path r]

while {[gets $fh line] >= 0} {
    puts $line
}

close $fh
```

`gets $fh line` 读一行到 `line`。到文件末尾返回 `-1`，循环结束。

---

## 概念 5 — 路径：`file join` 与检查（Day 3–4）

```tcl
set path [file join tmp week5_notes.txt]
```

`file join` 在不同系统上都能正确拼路径。

```tcl
if {[file exists $path]} {
    puts "找到了：$path"
}
```

见 `09_file_exists_size.tcl`。

---

## 概念 6 — 工具箱小作品（Day 5）

`10_toolbox.tcl` 包含：

- `greet` — 返回问候字符串  
- `add` — 返回和  
- `printList` — 用 `foreach` 打印列表  
- `appendLog` — 追加写入日志文件  

最后读回日志并打印。

---

## 每日练习

| 天 | 目标 | 文件 |
|----|------|------|
| Day 1 | `proc greet` | `01_proc_greet.tcl`、`02_proc_greet_many.tcl` |
| Day 2 | `return`、proc + `if` | `03_proc_add_return.tcl`、`04_proc_pass_fail.tcl` |
| Day 3 | 写文件 | `05_write_diary.tcl`、`06_write_with_file_join.tcl` |
| Day 4 | 读文件 | `07_read_diary.tcl`、`08_read_line_by_line.tcl` |
| Day 5 | **工具箱** | `10_toolbox.tcl` |

加分：`09_file_exists_size.tcl`、`11_proc_double.tcl`、`12_run_checklist.tcl`。

### 本周检查清单

- [ ] 我会定义并调用 `proc`。
- [ ] 我会用 `return`。
- [ ] 我会写文本文件并 `close`。
- [ ] 我会用 `gets` 读文件。
- [ ] 我会用 `file join` / `file mkdir`。
- [ ] 我完成了工具箱作品。

---

## 常见错误

| 现象 | 常见原因 | 怎么办 |
|------|----------|--------|
| `can't read "fh"` | 还没 `open` 就用 `$fh` | 先 `set fh [open $path w]` |
| 文件是空的 | 写到屏幕而不是文件 | 用 `puts $fh`，不是单独 `puts` |
| `couldn't open` | 路径错或没有 `tmp/` | 在项目根运行；`file mkdir tmp` |
| 忘记 `close` | 文件一直开着 | 结束时 `close $fh` |
| proc 里参数名错 | 与 `{name}` 不一致 | 统一参数名和 `$name` |

---

## 示例脚本

```bash
make week5-01
make week5
make list WEEK=5
```

| 编号 | 文件 | 练习重点 |
|------|------|----------|
| 01 | `01_proc_greet.tcl` | 第一个 proc |
| 02 | `02_proc_greet_many.tcl` | proc + foreach |
| 03 | `03_proc_add_return.tcl` | return |
| 04 | `04_proc_pass_fail.tcl` | proc + if |
| 05 | `05_write_diary.tcl` | 写日记 |
| 06 | `06_write_with_file_join.tcl` | file join |
| 07 | `07_read_diary.tcl` | 读日记 |
| 08 | `08_read_line_by_line.tcl` | gets + while |
| 09 | `09_file_exists_size.tcl` | 文件存在/大小 |
| 10 | `10_toolbox.tcl` | **本周作品** |
| 11 | `11_proc_double.tcl` | proc 调用 proc |
| 12 | `12_run_checklist.tcl` | 检查清单 |

---

## 挑战题

扩展 `10_toolbox.tcl`：

1. 增加 `subtract {a b}` 并 `return`  
2. 增加 `writeReport {path scores}` 把分数写入文件  
3. proc 内用 `if` 判断 Pass/Fail  
4. 读回报告并带行号打印  
5. 四个 `#` 注释分别说明每个 proc  

---

## 下一周预告

**第 6 周 — `string`：** 长度、切片、大小写、查找、替换（继续 M10 语法）。  
TclOO 改到 **第 15 周**；本周的 proc 仍是全局小帮手。

---

## 给家长 / 老师

- 请在项目根目录运行 `make week5`，`tmp/` 路径才正确。
- `tmp/week5_*.txt` 由例题生成，可随时删除重来。
- 成功标准：孩子能解释 `puts "hi"` 和 `puts $fh "hi"` 的区别。
