# Week 11 — Runtime Introspection (The info Family)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Master Tcl metaprogramming and reflection: query variable existence, registered procedures, call frames, and script versioning via `info`.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `info exists` | `info exists varName` | Check if a variable is defined in current scope |
| `info procs / vars` | `info procs ::eda::* / info vars` | List declared procedures and variables |
| `info level` | `info level / info level 1` | Inspect call stack depth and caller arguments |
| `info script` | `info script` | Return current executing file path |
| `info patchlevel` | `info patchlevel` | Return exact Tcl interpreter patch version |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 11 Example: Runtime Introspection & Environment Probe
puts "Tcl Interpreter Version: [info patchlevel]"
puts "Current Script Location : [info script]"

proc calculate_die_area {w h} {
    set caller_frame [info level]
    puts "Called from stack depth: $caller_frame"
    return [expr {$w * $h}]
}

calculate_die_area 1000 1000
puts "Registered custom procs: [info procs calc*]"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
