# Week 34 — Transforms, Coordinates & Grid Snapping

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Move cell origins, modify text annotations, copy geometry, scale shapes, and snap to fabrication grid.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `modify origin` | `$L modify origin $cell 0 0` | Reset cell coordinate origin |
| `modify text` | `$L modify text $cell $handle -string "NEW"` | Update text annotation string |
| `COPY` | `$L COPYCELL GEOM ...` | Duplicate cell geometry |
| `gridsnap` | `$L gridsnap $cell 0.005` | Snap coordinates to manufacturing grid |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 34 Example: Origin Shift and Grid Snapping
set L [layout create]
$L create cell TOP
$L create polygon TOP 1 100 100 200 100 200 200 100 200
puts "Initial bbox: [$L bbox TOP]"

# Shift origin by (100, 100)
$L modify origin TOP 100 100
puts "New bbox after origin shift: [$L bbox TOP]"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
