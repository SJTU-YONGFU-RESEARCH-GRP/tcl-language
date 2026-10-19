# Week 9 — Math Expressions, Substitution & Formatting

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M10 (Weeks 1–10: Tcl Core Syntax)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Master robust arithmetic and output formatting: enforce braced `expr` for security and performance, and format tables with `format`/`scan`.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `expr { ... }` | `expr {$width * $height}` | Strict braced expression evaluation (anti-injection) |
| `format` | `format "%-10s : %8.3f" $name $val` | C-style printf formatting |
| `scan` | `scan $line "%s %f" name val` | Scan and extract typed values from strings |
| `subst` | `subst -nobackslashes $text` | Controlled selective substitution pass |
| `incr / append` | `incr counter / append text "..."` | In-place counter increment and string append |

---

## 💡 Code Blueprint & Mental Model

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

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
