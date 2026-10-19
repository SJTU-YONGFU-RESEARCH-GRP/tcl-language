# 第 16 周 — TclOO 进阶：继承、混入与析构机制

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M20 (Weeks 11–20: Fluency & TclOO)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

掌握面向对象高级特性：在第 15 周类与对象基础上，学习单继承与多继承（superclass）、混入类（mixin）、过滤器（filter）以及自动垃圾回收析构器（destructor）。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `superclass` | `oo::class create Wire { superclass Geometry }` | Establish single and multiple class inheritance |
| `mixin` | `oo::define Wire mixin Loggable` | Inject cross-cutting logging or verification mixins |
| `destructor` | `destructor { puts "Shape destroyed" }` | Hook automatic cleanup when object handle is deleted |
| `my / self` | `my InternalMethod / self class` | Reference object identity and internal methods |

---

## 💡 示范代码与工程蓝图

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

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
