# 第 10 周 — 控制流、错误处理与 M10 综合自测

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M10 (Weeks 1–10: Tcl Core Syntax)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

掌握分支控制与防御性编程：学会 `switch` 模式匹配，运用 `catch` 与现代 `try ... on error` 构建零崩溃脚本，达成 Milestone 10 毕业标准。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `switch` | `switch -glob -- $str { p1 { ... } p2 { ... } }` | Multi-branch pattern matching |
| `catch` | `catch { open $file r } err` | Trap runtime exceptions and return error code |
| `try ... on error` | `try { ... } trap {POSIX ENOENT} { ... }` | Modern structured exception handling (Tcl 8.6+) |
| `throw / error` | `error "Custom message" / throw CODE msg` | Raise intentional exceptions |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 10 Example: Safe File Reader with Structured try-trap
proc safe_read_report {filepath} {
    try {
        set fh [open $filepath r]
        set data [read $fh]
        close $fh
        return $data
    } trap {POSIX ENOENT} {msg} {
        puts ">> [WARNING]: File '$filepath' does not exist. Using fallback mock."
        return "# MOCK REPORT\nSlack: +0.25 ns"
    } on error {err} {
        puts ">> [ERROR]: Unexpected I/O failure: $err"
        return ""
    }
}

set content [safe_read_report "non_existent_timing.rpt"]
puts "Loaded content:\n$content"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
