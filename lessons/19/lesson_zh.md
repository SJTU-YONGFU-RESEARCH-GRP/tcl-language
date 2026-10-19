# 第 19 周 — 综合复习工坊 B：I/O、命名空间与面向对象联调

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

融会贯通第 11–17 周高阶特性：搭建具备文件遍历、命名空间模块封装与 TclOO 实体建模的端到端数据流水线。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `System Integration` | `Combining glob, chan, namespace, and oo::class` | End-to-end design inspection and reporting |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 19 Example: Integrated Telemetry Parser Package
namespace eval ::eda_monitor {
    oo::class create LogWatcher {
        variable log_file
        constructor {path} { set log_file $path }
        method check_errors {} {
            if {![file exists $log_file]} { return 0 }
            set fh [open $log_file r]
            set errs 0
            while {[gets $fh line] >= 0} {
                if {[string match "*ERROR*" $line]} { incr errs }
            }
            close $fh
            return $errs
        }
    }
}
puts "LogWatcher class registered under ::eda_monitor"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
