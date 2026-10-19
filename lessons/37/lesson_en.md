# Week 37 — Export Formats (OASIS, ASCII & Instance Reports)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Multi-format layout export: high-compression OASIS, text ASCII, and hierarchical instance reports.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `oasisout` | `$L oasisout output.oas` | Export layout as modern OASIS format |
| `asciiout` | `$L asciiout output.txt` | Export human-readable layout ASCII dump |
| `report` | `$L report $cell` | Generate cell hierarchy report |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 37 Example: Multi-Format Export Pipeline
set L [layout create]
$L create cell TOP
$L create polygon TOP 1 0 0 500 0 500 500 0 500

puts "Ready for multi-format export:"
puts "  - GDS:   $L gdsout out.gds"
puts "  - OASIS: $L oasisout out.oas"
puts "  - ASCII: $L asciiout out.txt"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
