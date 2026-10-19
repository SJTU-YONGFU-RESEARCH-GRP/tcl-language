# Week 36 — Regional Clipping & RDB Defect Reports

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Clip layout within bounding boxes and generate RDB DRC defect reports.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `create clip` | `$L create clip $cell $bbox` | Extract geometry within spatial window |
| `clipsout` | `$L clipsout ...` | Export clipped regions to GDS |
| `rdbout` | `$L rdbout report.rdb ...` | Write Calibre Results Database report |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 36 Example: Clipping a Defect Region
set L [layout create]
$L create cell TOP
$L create polygon TOP 1 0 0 1000 0 1000 1000 0 1000

# Clip sub-region window [100 100 400 400]
puts "Clipping sub-window..."
# $L create clip TOP {100 100 400 400}
puts "Clip region defined for localized DRC review"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
