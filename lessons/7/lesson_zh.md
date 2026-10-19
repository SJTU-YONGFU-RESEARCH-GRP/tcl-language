# 第 7 周 — 列表进阶与数据过滤

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M10 (Weeks 1–10: Tcl Core Syntax)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

掌握列表的高阶操纵：排序、搜索、插入、替换、映射（lmap）以及字符串与列表的拆分（split）与拼接（join）。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `lrange` | `lrange $lst 1 3` | Extract a sublist slice |
| `lsearch` | `lsearch -exact $lst $key` | Search for an element index |
| `lsort` | `lsort -dictionary $lst` | Sort list by alphabetical or numeric order |
| `linsert / lreplace` | `lreplace $lst 0 0 $new` | Insert or replace list elements |
| `lmap` | `lmap x $lst {expr {$x * 2}}` | Transform list elements with expression |
| `split / join` | `split $str ',' / join $lst ':'` | Convert between strings and lists |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 7 Example: Sorting and Filtering Telemetry Lists
set raw_servers [list "node-03:98" "node-01:45" "node-02:88" "node-04:12"]

# Split and sort servers alphabetically
set sorted_servers [lsort -dictionary $raw_servers]
puts "Sorted servers: $sorted_servers"

# Extract high-load servers (> 80%)
set high_load [list]
foreach s $sorted_servers {
    set parts [split $s ":"]
    set host [lindex $parts 0]
    set load [lindex $parts 1]
    if {$load > 80} {
        lappend high_load $host
    }
}
puts "Critical high-load nodes: $high_load"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
