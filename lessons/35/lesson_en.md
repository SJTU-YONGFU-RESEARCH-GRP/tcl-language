# Week 35 — Iterator Counting & Shape Census

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Perform comprehensive layout census: count polygons, wires, text, and references per cell/layer.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `iterator count poly` | `$L iterator count $cell 1 poly` | Count total polygons on layer |
| `iterator count wire` | `$L iterator count $cell 1 wire` | Count wire paths on layer |
| `iterator count ref` | `$L iterator count $cell ref` | Count instance placements |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 35 Example: Layout Census & Geometry Counting
set L [layout create]
$L create cell TOP
$L create polygon TOP 1 0 0 10 0 10 10 0 10
$L create polygon TOP 1 20 20 30 20 30 30 20 30

set poly_count [$L iterator count TOP 1 poly]
set ref_count [$L iterator count TOP ref]
puts "Layout Census -> Layer 1 Polygons: $poly_count, References: $ref_count"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
