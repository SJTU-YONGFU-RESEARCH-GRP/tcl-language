# Week 38 — Connectivity & Netlist Extraction

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Understand physical layout connectivity: inter-layer connections and net tracing.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `connect` | `$L connect 1 2 3` | Define conductive via connection between layers |
| `extractNet` | `$L extractNet $cell $netname` | Trace and extract connected geometry net |
| `disconnect` | `$L disconnect 1 2 3` | Sever electrical connectivity rule |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 38 Example: Inter-Layer Via Connectivity
set L [layout create]
$L create cell TOP
# Define M1 (layer 1) connects to M2 (layer 3) through VIA1 (layer 2)
$L connect 1 2 3
puts "Defined electrical connectivity: Layer 1 <-> Layer 2 <-> Layer 3"
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
