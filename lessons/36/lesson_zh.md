# 第 36 周 — 区域裁剪与 RDB 报告 (Clip & RDB)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

按空间坐标窗口裁剪版图；导出 RDB（Results Database）违规报告。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `create clip` | `$L create clip $cell $bbox` | Extract geometry within spatial window |
| `clipsout` | `$L clipsout ...` | Export clipped regions to GDS |
| `rdbout` | `$L rdbout report.rdb ...` | Write Calibre Results Database report |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 36 Example: Clipping a Defect Region
set L [layout create]
$L create cell TOP
$L create polygon TOP 1 0 0 1000 0 1000 1000 0 1000

# Clip sub-region window [100 100 400 400]
puts "Clipping sub-window..."
# $L create clip TOP {100 100 400 400}
puts "Clip region defined for localized DRC review"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
