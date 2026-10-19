# 第 37 周 — 版图导出变体 (OASIS / ASCII / Report)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

同一版图多格式导出：高效 OASIS 格式、文本 ASCII 格式与实例树状报告。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `oasisout` | `$L oasisout output.oas` | Export layout as modern OASIS format |
| `asciiout` | `$L asciiout output.txt` | Export human-readable layout ASCII dump |
| `report` | `$L report $cell` | Generate cell hierarchy report |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 37 Example: Multi-Format Export Pipeline
set L [layout create]
$L create cell TOP
$L create polygon TOP 1 0 0 500 0 500 500 0 500

puts "Ready for multi-format export:"
puts "  - GDS:   $L gdsout out.gds"
puts "  - OASIS: $L oasisout out.oas"
puts "  - ASCII: $L asciiout out.txt"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
