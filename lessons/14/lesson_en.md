# Week 14 — Namespaces, Scoping & Reusable Packages

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Master large-scale code organization: isolate global state via `namespace eval`, export public APIs, and build reusable packages via `package provide`.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `namespace eval` | `namespace eval ::eda { variable version 1.0 }` | Create encapsulated namespace and scope |
| `namespace export` | `namespace export analyze report` | Declare public exported commands |
| `namespace import` | `namespace import ::eda::*` | Import exported commands into local scope |
| `package provide` | `package provide my_eda 1.0` | Declare reusable Tcl library package |
| `package require` | `package require Tcl 8.6` | Assert dependency versions |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 14 Example: Encapsulated EDA Toolkit Namespace
namespace eval ::vlsi_tools {
    namespace export calculate_wns compute_density
    variable version "2.0"

    proc calculate_wns {slacks} {
        set wns 0.0
        foreach s $slacks {
            if {$s < $wns} { set wns $s }
        }
        return $wns
    }
}

namespace import ::vlsi_tools::*
set test_slacks [list 0.12 -0.05 0.34 -0.21 0.04]
puts "Worst Negative Slack (WNS): [calculate_wns $test_slacks] ns"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
