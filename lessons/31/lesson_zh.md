# 第 31 周 — 层次查询加深 (Hierarchy Deep Query)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

把 cell 层次关系问清楚：祖先（ancestors）、最大嵌套深度（maxdepth）、引用次数（refcount）与顶层判断。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `ancestors` | `$L ancestors $cell` | List all parent cells instantiating this cell |
| `maxdepth` | `$L maxdepth $cell` | Get maximum hierarchy nesting depth |
| `refcount` | `$L refcount $cell` | Query reference instantiation count |
| `isReferenced` | `$L isReferenced $cell` | Check if cell is placed as instance inside another cell |
| `duplicate cell` | `$L duplicate cell $src $dst` | Deep clone a cell definition and contents |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 31 Example: Hierarchical Tree & Ancestor Traversal
set L [layout create]
$L create cell TOP
$L create cell MID
$L create cell LEAF
$L create ref MID LEAF 0 0 0 0 1
$L create ref TOP MID 0 0 0 0 1

puts "Ancestors of LEAF: [$L ancestors LEAF]"
puts "LEAF isReferenced: [$L isReferenced LEAF]"
puts "TOP max nesting depth: [$L maxdepth TOP]"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
