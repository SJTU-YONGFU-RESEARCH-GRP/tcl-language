# 第 20 周 — 纯 Tcl 阶段毕业大作品 + Milestone 20 审计

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

独立完成 Milestone 20 纯 Tcl 毕业大作品（如简易 EDA 网表解析器或自动化报告引擎），通过 5 大维度审计，迈入 Calibre 版图自动化。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `Milestone 20 Capstone` | `Full-featured pure-Tcl architecture` | Prerequisite for Week 21 Calibre DESIGNrev physical design |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 20 Milestone Capstone: Pure-Tcl Netlist Parser Engine
proc audit_netlist {netlist_lines} {
    set instances 0
    set nets 0
    foreach l $netlist_lines {
        set trimmed [string trim $l]
        if {[string match "X*" $trimmed]} { incr instances }
        if {[string match "*.net*" $trimmed]} { incr nets }
    }
    return [dict create instances $instances nets $nets status "AUDIT_PASSED"]
}

set mock_netlist [list "X1 A B OUT INV_X1" "X2 C D OUT2 NAND2" ".net n1 n2"]
set res [audit_netlist $mock_netlist]
puts ">> Milestone 20 Capstone Result: [dict get $res status] (Instances: [dict get $res instances])"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
