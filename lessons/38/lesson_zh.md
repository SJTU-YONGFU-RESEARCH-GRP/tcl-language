# 第 38 周 — 连通性与网络提取 (Connect & Net Extraction)

<div class="tcl-badge-cluster">
  <span class="tcl-badge">M40 (Weeks 31–40: Layout Catalog & Sign-Off)</span>
  <span class="tcl-badge amber">课程大纲已规划</span>
  <span class="tcl-badge">规划源：PLAN.md</span>
</div>

---

## 🎯 本周学习目标

理解版图连通性追踪：定义层间连接、断开关系与提取物理导线网络。

---

## 📋 本周核心命令与必会 API

| 核心命令 | 典型调用示例 | 功能与工程作用 |
| :--- | :--- | :--- |
| `connect` | `$L connect 1 2 3` | Define conductive via connection between layers |
| `extractNet` | `$L extractNet $cell $netname` | Trace and extract connected geometry net |
| `disconnect` | `$L disconnect 1 2 3` | Sever electrical connectivity rule |

---

## 💡 示范代码与工程蓝图

```tcl
# Week 38 Example: Inter-Layer Via Connectivity
set L [layout create]
$L create cell TOP
# Define M1 (layer 1) connects to M2 (layer 3) through VIA1 (layer 2)
$L connect 1 2 3
puts "Defined electrical connectivity: Layer 1 <-> Layer 2 <-> Layer 3"
```

---

## 🚀 本地运行与验证

在终端中执行测试或结合标准环境验证：

```bash
# 检查当前环境状态
make check-env
```

更多详细进阶任务与每日分解见根目录教学大纲 [PLAN.md](../../PLAN.md) 与 [docs/TCL_HELP.md](../../docs/TCL_HELP.md)。
