# Week 18 — Synthesis Workshop A: Syntax, Substitution & Data Structures

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Consolidate Weeks 1–10 foundations: execute complex mixed test cases on substitution, nested lists, multi-layer dictionaries, and robust error traps.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `Cross-Domain Synthesis` | `Combination of list, dict, expr, proc, and try` | Solve real-world EDA configuration parsing |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 18 Example: Multi-Corner STA Scenario Matrix
set corners [dict create]
dict set corners "ss_125c" [dict create voltage 0.72 temp 125 delay_scale 1.35]
dict set corners "ff_m40c" [dict create voltage 0.88 temp -40 delay_scale 0.78]
dict set corners "tt_25c"  [dict create voltage 0.80 temp 25  delay_scale 1.00]

dict for {corner_name params} $corners {
    set scale [dict get $params delay_scale]
    puts [format "Corner %-10s -> Delay Scale: %.2f (Nominal 100ps -> %d ps)"         $corner_name $scale [expr {round(100 * $scale)}]]
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
