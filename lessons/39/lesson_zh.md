# 第 39 周 — Peek 深入与快速版图探测 (Advanced Peek)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

把 layout peek 选项练全：不解析全部几何即可秒级提取 cell 列表、图层清单、bbox 与单位。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `layout peek -cells` | `layout peek file.gds -cells` | Query cell names without parsing hierarchy |
| `layout peek -layers` | `layout peek file.gds -layers` | Query occupied layers in GDS file |
| `layout peek -bbox` | `layout peek file.gds -bbox` | Fast extraction of chip boundaries |
| `layout peek -units` | `layout peek file.gds -units` | Query user units and precision scale |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 39 Example: Fast Header Probe via layout peek
# layout peek inspects multi-gigabyte GDS files in milliseconds!
puts "Syntax: layout peek <filename> -cells -layers -bbox -units"
puts "No memory overhead; ideal for continuous integration sanity checks."
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
