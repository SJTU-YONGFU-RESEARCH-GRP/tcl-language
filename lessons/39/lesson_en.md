# Week 39 — Advanced Layout Peek & Rapid Header Inspection

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Master layout peek: instant zero-overhead inspection of cells, layers, bounding boxes, and units without loading full layout.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `layout peek -cells` | `layout peek file.gds -cells` | Query cell names without parsing hierarchy |
| `layout peek -layers` | `layout peek file.gds -layers` | Query occupied layers in GDS file |
| `layout peek -bbox` | `layout peek file.gds -bbox` | Fast extraction of chip boundaries |
| `layout peek -units` | `layout peek file.gds -units` | Query user units and precision scale |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 39 Example: Fast Header Probe via layout peek
# layout peek inspects multi-gigabyte GDS files in milliseconds!
puts "Syntax: layout peek <filename> -cells -layers -bbox -units"
puts "No memory overhead; ideal for continuous integration sanity checks."
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
