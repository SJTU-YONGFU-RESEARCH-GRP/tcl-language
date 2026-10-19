# 第 30 周 — 单位、网格精度与元数据 + Milestone 30 审计

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M30 (Weeks 21–30: Calibre Layout Core)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

深入集成电路制造精度要求：掌握 DBU（Database Units）与用户微米（User Microns）换算网格，达成 Milestone 30 版图核心毕业标准。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `Grid & Precision` | `DBU scaling (e.g. 1000 DBU = 1 um)` | Enforce DRC off-grid prevention |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 30 Example: DBU to Micron Conversion
set dbu_per_micron 1000
set poly_width_dbu 150
set poly_width_um [expr {double($poly_width_dbu) / $dbu_per_micron}]
puts [format "Width in microns: %.4f um" $poly_width_um]
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
