# Week 30 — Units, Grid Precision, Metadata & Milestone 30 Audit

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M30 (Weeks 21–30: Calibre Layout Core)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Deep dive into semiconductor manufacturing grids: master DBU to micron scaling, grid snapping, and achieve Milestone 30 certification.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `Grid & Precision` | `DBU scaling (e.g. 1000 DBU = 1 um)` | Enforce DRC off-grid prevention |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 30 Example: DBU to Micron Conversion
set dbu_per_micron 1000
set poly_width_dbu 150
set poly_width_um [expr {double($poly_width_dbu) / $dbu_per_micron}]
puts [format "Width in microns: %.4f um" $poly_width_um]
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
