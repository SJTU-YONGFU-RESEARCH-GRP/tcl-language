# Week 20 — Pure-Tcl Capstone Project & Milestone 20 Audit

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Complete the Milestone 20 Capstone Project (e.g. EDA netlist parser or report engine), pass audit benchmarks, and graduate to Calibre layout scripting.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `Milestone 20 Capstone` | `Full-featured pure-Tcl architecture` | Prerequisite for Week 21 Calibre DESIGNrev physical design |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 20 Milestone Capstone: Pure-Tcl Netlist Parser Engine
proc audit_netlist {netlist_lines} {
    set instances 0
    set nets 0
    foreach l $netlist_lines {
        set trimmed [string trim $l]
        if {[string match "X*" $trimmed]} { incr instances }
        if {[string match "*.net*" $trimmed]} { incr nets }
    }
    return [dict create instances $instances nets $nets status "AUDIT_PASSED"]
}

set mock_netlist [list "X1 A B OUT INV_X1" "X2 C D OUT2 NAND2" ".net n1 n2"]
set res [audit_netlist $mock_netlist]
puts ">> Milestone 20 Capstone Result: [dict get $res status] (Instances: [dict get $res instances])"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
