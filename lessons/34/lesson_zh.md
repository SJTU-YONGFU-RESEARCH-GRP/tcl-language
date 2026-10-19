# 第 34 周 — 修改与几何变换 (Transforms & Snapping)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

移动原点、改文字、拷贝几何、缩放与对齐生产制造网格。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `modify origin` | `$L modify origin $cell 0 0` | Reset cell coordinate origin |
| `modify text` | `$L modify text $cell $handle -string "NEW"` | Update text annotation string |
| `COPY` | `$L COPYCELL GEOM ...` | Duplicate cell geometry |
| `gridsnap` | `$L gridsnap $cell 0.005` | Snap coordinates to manufacturing grid |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 34 Example: Origin Shift and Grid Snapping
set L [layout create]
$L create cell TOP
$L create polygon TOP 1 100 100 200 100 200 200 100 200
puts "Initial bbox: [$L bbox TOP]"

# Shift origin by (100, 100)
$L modify origin TOP 100 100
puts "New bbox after origin shift: [$L bbox TOP]"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
