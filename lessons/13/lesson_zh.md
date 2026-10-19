# 第 13 周 — 正则表达式与时间处理 (regexp / regsub / clock)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

掌握文本数据抽取与时间度量：深入运用 `regexp` 子匹配捕获、`regsub` 正则替换，以及 `clock` 时间戳转换与执行基准测试。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `regexp` | `regexp {Slack:\s+([\-\d\.]+)} $line -> slack` | Pattern matching and capture group assignment |
| `regsub` | `regsub -all {\s+} $text " " clean` | Global regular expression substitution |
| `clock seconds` | `clock seconds / clock milliseconds` | Fetch Unix epoch timestamp or millisecond ticks |
| `clock format` | `clock format [clock seconds] -format "%Y-%m-%d"` | Format timestamps into human-readable ISO dates |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 13 Example: Parse Slack and Measure Execution Time
set t0 [clock milliseconds]

set log_line "Path 14: Data arrival = 3.42 ns, Data required = 3.10 ns, Slack: -0.320 ns (VIOLATED)"
if {[regexp {Slack:\s+([\-\d\.]+)\s+ns} $log_line match slack_val]} {
    puts "Extracted Slack value: $slack_val ns"
}

set t1 [clock milliseconds]
puts "Parsed in [expr {$t1 - $t0}] ms"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
