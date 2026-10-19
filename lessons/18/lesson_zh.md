# 第 18 周 — 综合复习工坊 A：语法、置换与列表字典实战

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

融会贯通第 1–10 周语法基石：通过大规模混合测试用例，综合演练三步替换、嵌套列表、复杂字典构建与异常防护机制。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `Cross-Domain Synthesis` | `Combination of list, dict, expr, proc, and try` | Solve real-world EDA configuration parsing |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 18 Example: Multi-Corner STA Scenario Matrix
set corners [dict create]
dict set corners "ss_125c" [dict create voltage 0.72 temp 125 delay_scale 1.35]
dict set corners "ff_m40c" [dict create voltage 0.88 temp -40 delay_scale 0.78]
dict set corners "tt_25c"  [dict create voltage 0.80 temp 25  delay_scale 1.00]

dict for {corner_name params} $corners {
    set scale [dict get $params delay_scale]
    puts [format "Corner %-10s -> Delay Scale: %.2f (Nominal 100ps -> %d ps)"         $corner_name $scale [expr {round(100 * $scale)}]]
}
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
