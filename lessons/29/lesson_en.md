# Week 29 — Global Layout Command Catalog & Multi-Handle Workflows

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Master Calibre DESIGNrev global `layout` catalog: concurrent layout handles, cross-cell shape replication, and memory resource recycling.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `layout create` | `set L2 [layout create other.gds]` | Concurrent handles |
| `layout peek` | `layout peek file.gds -cells` | Query without full memory allocation |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 29 Example: Concurrent Layout Inspection
set L1 [layout create]
$L1 create cell TOP_A
set L2 [layout create]
$L2 create cell TOP_B

puts "Layout 1 top: [$L1 topcell]"
puts "Layout 2 top: [$L2 topcell]"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
