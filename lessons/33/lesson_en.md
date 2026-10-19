# Week 33 — Safe Deletion Catalog (Cells, Layers & Geometries)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Inspect before destroying: safe deletion of cells, layers, polygons, wires, refs, and text.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `delete cell` | `$L delete cell $cell` | Safely delete unreferenced cell |
| `delete layer` | `$L delete layer 1` | Delete an entire layer |
| `delete polygon` | `$L delete polygon $cell 1 $poly_handle` | Delete specific polygon instance |
| `delete ref` | `$L delete ref $cell $ref_handle` | Delete cell instance reference |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 33 Example: Safe Deletion & Verification
set L [layout create]
$L create cell TOP
$L create cell TEMP
set p [$L create polygon TOP 1 0 0 50 0 50 50 0 50]
puts "Created polygon handle: $p"

# Delete the temporary polygon
$L delete polygon TOP 1 $p
puts "Polygon safely deleted"
$L delete cell TEMP
puts "Cell TEMP safely deleted"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
