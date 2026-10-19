# Week 17 — Script Engineering Patterns & Code Reuse

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Master industrial script architecture: Singleton, Factory, and Observer patterns, centralized config stores, and maintainable team codebases.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `Factory Pattern` | `proc create_eda_reader {type} { ... }` | Dynamically instantiate parser objects |
| `Config Store` | `dict / namespace configuration singleton` | Centralized environment and parameter management |
| `Command Pipeline` | `proc pipeline {data stages} { ... }` | Composable data transformation chains |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 17 Example: Pipeline Architecture Pattern
proc run_pipeline {input_data stages} {
    set cur $input_data
    foreach stage $stages {
        set cur [{*}$stage $cur]
    }
    return $cur
}

proc strip_comments {lines} {
    set out [list]
    foreach l $lines {
        if {![string match "#*" [string trim $l]]} { lappend out $l }
    }
    return $out
}

proc count_items {items} {
    return [format "Processed %d active items" [llength $items]]
}

set raw_lines [list "# Header comment" "pin A 10 20" "# Mid comment" "pin B 30 40"]
set result [run_pipeline $raw_lines [list strip_comments count_items]]
puts $result
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
