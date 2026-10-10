# 第 24 周 — API 层次：`create ref` + 多 API 毕业作品

> 本课对应总计划：[10 周 Tcl 学习计划](../../PLAN.md)。  
> 本周目标：用 `$L create ref` 做 cell 引用（摆放）；毕业作品至少组合 **创建 + 几何 + 查询**。

**环境：** Calibre DESIGNrev。帮助：[docs/CALIBRE_HELP.md](../../docs/CALIBRE_HELP.md)。

---

## 学习目标

学完这一周，你应该能够：

1. 解释 **create ref**：把一个 cell（零件）放进另一个 cell（房间）。
2. 写出 `$L create ref incell refcell x y mirror angle mag`。
3. 使用可选 **阵列** 参数：`cols rows xspace yspace`。
4. 用 `$L children`（以及第 9 周的 peek / bbox）查看层次。
5. 完成 **毕业作品**，至少包含：
   - ≥1 个创建 API（`layout create`、`create cell` / `layer`）
   - ≥2 个几何 API（`polygon` / `text` / `wire`）
   - `$L create ref`
   - `gdsout` + ≥2 个查询 API（`peek`、`cells`、`bbox` …）
6. 能口头说出自己用过的 3 个 API。

这是 10 周计划的最后一周。

---

## 大想法

| 想法 | 生活比喻 | Tcl |
|------|----------|-----|
| 叶子 cell | 一块积木 | `create cell BOX` + polygon |
| 父 cell | 桌子 / 房子 | `create cell TOP` |
| `create ref` | 把积木盖到桌子上 | `$L create ref TOP BOX x y …` |
| 阵列 ref | 像图章盖成网格 | 额外的 `cols rows xspace yspace` |

第 7–9 周的句柄、画图、提问本领都还要用。

---

## 概念 1 — `create ref` 语法

```tcl
$L create ref TOP BOX 0 0 0 0 1
#               ^    ^   ^ ^ ^ ^ ^
#               |    |   | | | | 放大倍数 mag
#               |    |   | | | 角度 angle
#               |    |   | | 镜像 mirror（0=不镜像）
#               |    |   x y
#               |    被放置的 cell
#               父 cell（放在哪里）
```

Calibre Usage：

`create ref <incell> <refcell> <x> <y> <mirror> <angle> <mag> [<cols> <rows> <xspace> <yspace>]`

见 `03_create_ref_once.tcl`、`04_create_ref_two.tcl`。

---

## 概念 2 — 阵列摆放

```tcl
# 2 列 x 2 行，间距 15
$L create ref GRID DOT 0 0 0 0 1 2 2 15 15
```

见 `05_create_ref_array.tcl`。

---

## 概念 3 — 引用之后的 children

```tcl
puts [$L children TOP]
```

通常会列出放进 `TOP` 的 cell（例如 `BOX`）。

见 `07_report_hierarchy.tcl`。

---

## 概念 4 — 毕业项目（选一）

来自 PLAN：

1. 双层小房子 + text + 报告  
2. 积木阵列 + `create ref`  
3. 用 polygon / ref 拼字母  
4. （加分）TclOO 小工厂封装 `$L`  
5. （家长选学）GUI `cwbWorkBench`

本文件夹默认作品：**积木阵列** → `10_graduation_project.tcl`。

OOP 加分版：`11_oop_layout_factory.tcl`。

---

## 每日练习

| 天 | 目标 | 文件 |
|----|------|------|
| Day 1 | 纸上规划 API | `01_api_plan_checklist.tcl` |
| Day 2 | 叶子 cell + 一次 ref | `02`、`03` |
| Day 3 | 两次 ref / 阵列 / 房子 | `04`、`05`、`06` |
| Day 4 | 报告 + 组合 | `07`、`08`、`09` |
| Day 5 | **毕业作品** | `10_graduation_project.tcl` |

### 本周检查清单

- [ ] 我懂 create ref  
- [ ] create + cell/layer  
- [ ] ≥2 个几何 API  
- [ ] 用过 create ref  
- [ ] gdsout 成功  
- [ ] ≥2 个查询 API  
- [ ] 能口头说出 3 个 API  

---

## 常见错误

| 现象 | 常见原因 | 怎么办 |
|------|----------|--------|
| 叶子 cell 还不存在就 ref | 顺序错了 | 先建 `BOX`（含图形）再 ref |
| 参数顺序乱 | x/y/mirror/angle/mag 搞混 | 对照 PLAN 例句 |
| peek 只看到 TOP | 叶子仍在 `$L cells` 里 | 再看 `$L cells` 与 `$L children` |
| 导出错 cell | gdsout 忘写 TOP | `$L gdsout file TOP` |

---

## 示例脚本

```bash
make week24-01
make week24
make week24-10
```

| 编号 | 文件 | 练习重点 |
|------|------|----------|
| 01 | `01_api_plan_checklist.tcl` | 规划 API |
| 02 | `02_leaf_cell_box.tcl` | 叶子 BOX |
| 03 | `03_create_ref_once.tcl` | 一次 ref |
| 04 | `04_create_ref_two.tcl` | PLAN 两次 ref |
| 05 | `05_create_ref_array.tcl` | 2×2 阵列 |
| 06 | `06_two_layer_house.tcl` | 房子思路 |
| 07 | `07_report_hierarchy.tcl` | 层次查询 |
| 08 | `08_ref_then_peek.tcl` | 创建 + peek |
| 09 | `09_mini_combo.tcl` | 迷你多 API |
| 10 | `10_graduation_project.tcl` | **毕业作品** |
| 11 | `11_oop_layout_factory.tcl` | TclOO 加分 |
| 12 | `12_run_checklist.tcl` | 检查清单 |

---

## 挑战题

1. 把毕业阵列改成 **4×3** 块积木。  
2. 用 `create text` 加上你的姓名缩写。  
3. 把完成脚本复制到 `examples/my_graduation.tcl`。  
4. 演示给家长：跑 `make week24-10`，说出三个 API。

---

## 10 周之后

见 PLAN 附录：iterator、filemerge、布尔运算、RDB、GUI 宏、自己的 TclOO 工具库。

---

## 给家长 / 老师

- 毕业成功标准：脚本能跑、生成 GDS、孩子能说出创建 / 几何 / 查询三类 API。  
- GUI 看图可选。  
- OOP 工厂（`11`）仅作加分。
