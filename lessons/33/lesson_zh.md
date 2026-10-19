# 第 33 周 — delete 全家桶 (Safe Geometry & Cell Deletion)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

先会查再会删：掌握安全删除 cell / layer / polygon / wire / ref / text 的生命周期管控。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `delete cell` | `$L delete cell $cell` | Safely delete unreferenced cell |
| `delete layer` | `$L delete layer 1` | Delete an entire layer |
| `delete polygon` | `$L delete polygon $cell 1 $poly_handle` | Delete specific polygon instance |
| `delete ref` | `$L delete ref $cell $ref_handle` | Delete cell instance reference |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 33 Example: Safe Deletion & Verification
set L [layout create]
$L create cell TOP
$L create cell TEMP
set p [$L create polygon TOP 1 0 0 50 0 50 50 0 50]
puts "Created polygon handle: $p"

# Delete the temporary polygon
$L delete polygon TOP 1 $p
puts "Polygon safely deleted"
$L delete cell TEMP
puts "Cell TEMP safely deleted"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
