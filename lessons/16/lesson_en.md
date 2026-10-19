# Week 16 — Advanced TclOO: Inheritance, Mixins & Destructors

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">Planned Syllabus</span>
  <span class="tcl-badge">Source: PLAN.md</span>
</div>

---

## 🎯 Weekly Learning Objectives

Master advanced OOP paradigms: class inheritance (superclass), mixin compositions, execution filters, and automatic memory cleanup via destructors.

---

## 📋 Core Commands & API Surface

| Command | Usage Example | Functional Description |
| :--- | :--- | :--- |
| `superclass` | `oo::class create Wire { superclass Geometry }` | Establish single and multiple class inheritance |
| `mixin` | `oo::define Wire mixin Loggable` | Inject cross-cutting logging or verification mixins |
| `destructor` | `destructor { puts "Shape destroyed" }` | Hook automatic cleanup when object handle is deleted |
| `my / self` | `my InternalMethod / self class` | Reference object identity and internal methods |

---

## 💡 Code Blueprint & Mental Model

```tcl
# Week 16 Example: Hierarchical Physical Geometry OOP Model
oo::class create Shape {
    variable x y
    constructor {init_x init_y} {
        set x $init_x; set y $init_y
    }
    method get_origin {} { list $x $y }
    destructor { puts "Shape at ($x, $y) decommissioned" }
}

oo::class create Rect {
    superclass Shape
    variable width height
    constructor {x y w h} {
        next $x $y
        set width $w; set height $h
    }
    method area {} { expr {$width * $height} }
}

set r [Rect new 0 0 50 100]
puts "Rectangle area: [$r area] um2"
$r destroy
```

---

## 🚀 Execution & Verification

Run this lesson script directly using standard `tclsh` (or `calibredrv` for physical layout weeks):

```bash
# Verify syllabus roadmap status
make check-env
```

Refer to full specifications in [PLAN.md](../../PLAN.md) and industrial guides in [docs/TCL_HELP.md](../../docs/TCL_HELP.md).
