# Week 8 — Dictionaries (dict) & Associative Arrays (array)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M10 (Weeks 1–10: Tcl Core Syntax)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Master key-value data structures: deep dive into value-based Tcl 8.5+ `dict` and contrast with classic associative `array`.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `dict create` | `dict create k1 v1 k2 v2` | Initialize an immutable value-based dictionary |
| `dict get / set` | `dict get $d k1 / dict set d k1 v2` | Retrieve or update dictionary keys |
| `dict exists` | `dict exists $d key` | Query key existence without runtime error |
| `dict for` | `dict for {k v} $d { ... }` | Iterate over dictionary key-value pairs |
| `array set / get` | `array set arr {k1 v1 k2 v2}` | Classic variable-table associative storage |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 8 Example: Layer-to-Name Mapping Dictionary
set layer_map [dict create 1 "M1" 2 "VIA1" 3 "M2" 4 "VIA2" 5 "M3"]

# Query existing key
if {[dict exists $layer_map 3]} {
    puts "Layer 3 mapped to: [dict get $layer_map 3]"
}

# Update dictionary
dict set layer_map 6 "TOP_METAL"

# Iterate all layers
dict for {layer_num layer_name} $layer_map {
    puts "  GDS Layer $layer_num -> $layer_name"
}
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
