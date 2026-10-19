# 第 9 周 — 表达式运算、置换与格式化 (expr / subst / format)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M10 (Weeks 1–10: Tcl Core Syntax)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

掌握稳健且高效的数学运算与输出格式化：牢记花括号保护 `expr {$a + $b}` 的安全与字节编译准则，掌握 `format` 与 `scan`。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `expr { ... }` | `expr {$width * $height}` | Strict braced expression evaluation (anti-injection) |
| `format` | `format "%-10s : %8.3f" $name $val` | C-style printf formatting |
| `scan` | `scan $line "%s %f" name val` | Scan and extract typed values from strings |
| `subst` | `subst -nobackslashes $text` | Controlled selective substitution pass |
| `incr / append` | `incr counter / append text "..."` | In-place counter increment and string append |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 9 Example: Formatted Physical Coordinate Table
set cells [list [list "INV_X1" 0.0 0.0 1.2 2.4] [list "NAND2_X1" 2.5 0.0 4.3 2.4]]

puts [format "%-12s | %8s | %8s | %10s" "Cell Name" "X (um)" "Y (um)" "Area (um2)"]
puts [string repeat "-" 48]

foreach c $cells {
    lassign $c name x1 y1 x2 y2
    set w [expr {$x2 - $x1}]
    set h [expr {$y2 - $y1}]
    set area [expr {$w * $h}]
    puts [format "%-12s | %8.2f | %8.2f | %10.3f" $name $x1 $y1 $area]
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
