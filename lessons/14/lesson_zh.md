# 第 14 周 — 命名空间、作用域与程序包 (namespace / package)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

掌握大型软件工程的模块化组织：运用 `namespace eval` 隔离全局变量，导出公共过程 (`namespace export`)，构建标准 `package provide` 模块。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `namespace eval` | `namespace eval ::eda { variable version 1.0 }` | Create encapsulated namespace and scope |
| `namespace export` | `namespace export analyze report` | Declare public exported commands |
| `namespace import` | `namespace import ::eda::*` | Import exported commands into local scope |
| `package provide` | `package provide my_eda 1.0` | Declare reusable Tcl library package |
| `package require` | `package require Tcl 8.6` | Assert dependency versions |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 14 Example: Encapsulated EDA Toolkit Namespace
namespace eval ::vlsi_tools {
    namespace export calculate_wns compute_density
    variable version "2.0"

    proc calculate_wns {slacks} {
        set wns 0.0
        foreach s $slacks {
            if {$s < $wns} { set wns $s }
        }
        return $wns
    }
}

namespace import ::vlsi_tools::*
set test_slacks [list 0.12 -0.05 0.34 -0.21 0.04]
puts "Worst Negative Slack (WNS): [calculate_wns $test_slacks] ns"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
