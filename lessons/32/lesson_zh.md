# 第 32 周 — 层管理全家桶 (Layer Management Catalog)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

给层起名字、查是否为空、配置层属性与掩膜信息（Batch 批处理模式）。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `layernames` | `$L layernames` | List all named layers in layout |
| `layerconfigure` | `$L layerconfigure 1 -name "POLY"` | Configure layer display and metadata |
| `isLayerEmpty` | `$L isLayerEmpty 1` | Check if layer contains no geometry |
| `modify layer` | `$L modify layer 1 10` | Remap or change layer index |

---

## 💡 示范代码与工程蓝图

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

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
