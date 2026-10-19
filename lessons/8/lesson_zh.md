# 第 8 周 — 字典 (dict) 与关联数组 (array)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M10 (Weeks 1–10: Tcl Core Syntax)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

掌握“键-值”映射数据结构：深入理解 Tcl 8.5+ 原生纯值字典 `dict`，对比传统关联数组 `array` 的异同与适用场景。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `dict create` | `dict create k1 v1 k2 v2` | Initialize an immutable value-based dictionary |
| `dict get / set` | `dict get $d k1 / dict set d k1 v2` | Retrieve or update dictionary keys |
| `dict exists` | `dict exists $d key` | Query key existence without runtime error |
| `dict for` | `dict for {k v} $d { ... }` | Iterate over dictionary key-value pairs |
| `array set / get` | `array set arr {k1 v1 k2 v2}` | Classic variable-table associative storage |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 8 Example: Layer-to-Name Mapping Dictionary
set layer_map [dict create 1 "M1" 2 "VIA1" 3 "M2" 4 "VIA2" 5 "M3"]

# Query existing key
if {[dict exists $layer_map 3]} {
    puts "Layer 3 mapped to: [dict get $layer_map 3]"
}

# Update dictionary
dict set layer_map 6 "TOP_METAL"

# Iterate all layers
dict for {layer_num layer_name} $layer_map {
    puts "  GDS Layer $layer_num -> $layer_name"
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
