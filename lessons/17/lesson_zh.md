# 第 17 周 — 脚本工程模式：模块化与代码复用

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

掌握工业级脚本架构设计：单例模式、工厂模式、观察者模式与配置管理中心，编写结构清晰、便于团队协作维护的 Tcl 代码库。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `Factory Pattern` | `proc create_eda_reader {type} { ... }` | Dynamically instantiate parser objects |
| `Config Store` | `dict / namespace configuration singleton` | Centralized environment and parameter management |
| `Command Pipeline` | `proc pipeline {data stages} { ... }` | Composable data transformation chains |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 17 Example: Pipeline Architecture Pattern
proc run_pipeline {input_data stages} {
    set cur $input_data
    foreach stage $stages {
        set cur [{*}$stage $cur]
    }
    return $cur
}

proc strip_comments {lines} {
    set out [list]
    foreach l $lines {
        if {![string match "#*" [string trim $l]]} { lappend out $l }
    }
    return $out
}

proc count_items {items} {
    return [format "Processed %d active items" [llength $items]]
}

set raw_lines [list "# Header comment" "pin A 10 20" "# Mid comment" "pin B 30 40"]
set result [run_pipeline $raw_lines [list strip_comments count_items]]
puts $result
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
