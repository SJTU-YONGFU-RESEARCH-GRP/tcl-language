# 第 11 周 — 运行时自省机制 (info 命令家族)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

掌握 Tcl 核心元编程能力：通过 `info` 家族实时查询变量、已定义过程、调用栈、版本及命令元数据。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `info exists` | `info exists varName` | Check if a variable is defined in current scope |
| `info procs / vars` | `info procs ::eda::* / info vars` | List declared procedures and variables |
| `info level` | `info level / info level 1` | Inspect call stack depth and caller arguments |
| `info script` | `info script` | Return current executing file path |
| `info patchlevel` | `info patchlevel` | Return exact Tcl interpreter patch version |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 11 Example: Runtime Introspection & Environment Probe
puts "Tcl Interpreter Version: [info patchlevel]"
puts "Current Script Location : [info script]"

proc calculate_die_area {w h} {
    set caller_frame [info level]
    puts "Called from stack depth: $caller_frame"
    return [expr {$w * $h}]
}

calculate_die_area 1000 1000
puts "Registered custom procs: [info procs calc*]"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
