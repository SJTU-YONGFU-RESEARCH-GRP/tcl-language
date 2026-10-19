# 第 29 周 — 全局 Layout 命令全家桶与多句柄协作

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

掌握 Calibre DESIGNrev 全局 `layout` 命令家族：多版图句柄并发操纵、跨图层克隆与内存资源回收。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `layout create` | `set L2 [layout create other.gds]` | Concurrent handles |
| `layout peek` | `layout peek file.gds -cells` | Query without full memory allocation |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 29 Example: Concurrent Layout Inspection
set L1 [layout create]
$L1 create cell TOP_A
set L2 [layout create]
$L2 create cell TOP_B

puts "Layout 1 top: [$L1 topcell]"
puts "Layout 2 top: [$L2 topcell]"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
