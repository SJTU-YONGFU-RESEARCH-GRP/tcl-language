# 第 35 周 — iterator 计数与版图普查 (Census & Counting)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

不只列出图形，还要「人口普查」式统计：poly、wire、text、ref 等各类实体数量。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `iterator count poly` | `$L iterator count $cell 1 poly` | Count total polygons on layer |
| `iterator count wire` | `$L iterator count $cell 1 wire` | Count wire paths on layer |
| `iterator count ref` | `$L iterator count $cell ref` | Count instance placements |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 35 Example: Layout Census & Geometry Counting
set L [layout create]
$L create cell TOP
$L create polygon TOP 1 0 0 10 0 10 10 0 10
$L create polygon TOP 1 20 20 30 20 30 30 20 30

set poly_count [$L iterator count TOP 1 poly]
set ref_count [$L iterator count TOP ref]
puts "Layout Census -> Layer 1 Polygons: $poly_count, References: $ref_count"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
