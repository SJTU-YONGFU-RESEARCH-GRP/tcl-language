# Week 7 — Advanced Lists & Data Filtering

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M10 (Weeks 1–10: Tcl Core Syntax)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Master advanced list manipulation: sorting, searching, inserting, replacing, mapping (lmap), and string/list conversion (split/join).

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `lrange` | `lrange $lst 1 3` | Extract a sublist slice |
| `lsearch` | `lsearch -exact $lst $key` | Search for an element index |
| `lsort` | `lsort -dictionary $lst` | Sort list by alphabetical or numeric order |
| `linsert / lreplace` | `lreplace $lst 0 0 $new` | Insert or replace list elements |
| `lmap` | `lmap x $lst {expr {$x * 2}}` | Transform list elements with expression |
| `split / join` | `split $str ',' / join $lst ':'` | Convert between strings and lists |

---

## 💡 Code Blueprint & Mental Model

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

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
