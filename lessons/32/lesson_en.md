# Week 32 — Comprehensive Layer Management

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Assign layer names, inspect layer occupancy, configure layer properties and mask attributes in batch mode.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `layernames` | `$L layernames` | List all named layers in layout |
| `layerconfigure` | `$L layerconfigure 1 -name "POLY"` | Configure layer display and metadata |
| `isLayerEmpty` | `$L isLayerEmpty 1` | Check if layer contains no geometry |
| `modify layer` | `$L modify layer 1 10` | Remap or change layer index |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 32 Example: Layer Inspection & Configuration
set L [layout create]
$L create cell TOP
$L create layer 1
$L layerconfigure 1 -name "POLY_GATE"
puts "Is layer 1 empty? [$L isLayerEmpty 1]"

# Add shape to layer 1
$L create polygon TOP 1 0 0 100 0 100 100 0 100
puts "After draw, is layer 1 empty? [$L isLayerEmpty 1]"
puts "Named layers: [$L layernames]"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
